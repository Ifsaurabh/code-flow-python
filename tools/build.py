#!/usr/bin/env python3
"""Builds app/data/questions/*.json from tools/src/*.py, running every reference solution
through the same comparison rules the app uses. Fails loudly on any mismatch."""
import json, sys, os, glob, importlib.util, copy, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import qlib

PRE = {}


def load_prelude():
    # reuse the exact prelude and converters that ship in app/js/trace.py
    src = open(os.path.join(ROOT, 'app/js/trace.py')).read()
    ns = {}
    # trace.py only needs the stdlib, so it can be imported as plain Python
    exec(compile(src, 'trace.py', 'exec'), ns)
    return ns


NS = load_prelude()


def run_ref(d, args):
    g = {'__name__': '__main__'}
    p = NS['_prelude_src'](d.get('prelude'))
    if p:
        exec(p, g)
    exec(d['ref'], g)
    a = NS['_conv_args'](g, copy.deepcopy(args), d.get('conv'))
    got = g[d['fn']](*a)
    if d.get('inplace') is not None:
        got = a[d['inplace']]
    if d.get('conv_ret'):
        got = g[NS['_CONV_OUT'][d['conv_ret']]](got)
    return got


def jsonable(x):
    if isinstance(x, tuple) or isinstance(x, set):
        x = list(x)
    if isinstance(x, list):
        return [jsonable(i) for i in x]
    if isinstance(x, dict):
        return {str(k): jsonable(v) for k, v in x.items()}
    return x


def check(d):
    errs = []
    if d['kind'] == 'function':
        for i, t in enumerate(d['tests']):
            try:
                got = jsonable(run_ref(d, t['args']))
            except Exception as e:
                errs.append('%s test %d raised %r' % (d['id'], i, e))
                continue
            if 'expect' in t:
                if not NS['_same'](got, t['expect'], d['compare']):
                    errs.append('%s test %d: ref gave %r but statement example says %r' % (d['id'], i, got, t['expect']))
            else:
                t['expect'] = got
        # starter must at least compile
        try:
            compile(d['starter'], 's', 'exec')
        except SyntaxError as e:
            errs.append(d['id'] + ' starter: ' + str(e))
        if len(d['tests']) < 3:
            errs.append(d['id'] + ': needs at least 3 tests')
    elif d['kind'] == 'script':
        import io, contextlib
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                g = {}
                exec(d['setup'], g)
                exec(d['ref'], g)
        except Exception as e:
            errs.append('%s script ref raised %r' % (d['id'], e))
        if not buf.getvalue().strip():
            errs.append(d['id'] + ': script ref prints nothing')
    elif d['kind'] == 'qa':
        if len(d['answer']) < 40:
            errs.append(d['id'] + ': answer too short')
    return errs


def main():
    all_q, errs = [], []
    for path in sorted(glob.glob(os.path.join(ROOT, 'tools/src/*.py'))):
        qlib.Q.clear()
        spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        batch = [copy.deepcopy(x) for x in qlib.Q]
        all_q.extend(batch)
    for jp in sorted(glob.glob(os.path.join(ROOT, 'tools/src/*.json'))):
        all_q.extend(json.load(open(jp)))
    ids = collections.Counter(q['id'] for q in all_q)
    errs += ['duplicate id ' + i for i, c in ids.items() if c > 1]
    for d in all_q:
        errs += check(d)
    if errs:
        print('\n'.join(errs))
        print('%d problems' % len(errs))
        sys.exit(1)
    by_file = collections.OrderedDict()
    for d in all_q:
        by_file.setdefault(d['section'].lower().replace(' & ', '-').replace(' ', '-'), []).append(d)
    outdir = os.path.join(ROOT, 'app/data/questions')
    os.makedirs(outdir, exist_ok=True)
    for f in glob.glob(outdir + '/*.json'):
        os.remove(f)
    index = []
    for name, items in by_file.items():
        fn = name + '.json'
        json.dump(items, open(os.path.join(outdir, fn), 'w'), ensure_ascii=False, separators=(',', ':'))
        index.append({'file': 'data/questions/' + fn, 'section': items[0]['section'], 'count': len(items)})
    json.dump({'version': 1, 'files': index, 'total': len(all_q)}, open(os.path.join(ROOT, 'app/data/index.json'), 'w'), indent=1)
    print('OK: %d questions in %d files' % (len(all_q), len(index)))


main()
