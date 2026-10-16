"""Code Flow Python: step tracer and test runner. Runs inside Pyodide (real CPython).

trace_run(json)  -> json   records line-by-line steps with variables, loop context, output
run_tests(json)  -> json   runs a function against test cases (no tracing)
"""
import sys, ast, json, types, time, copy, io, builtins, itertools, math, collections, traceback

_USER = '<user>'
_MAX_STEPS = 600
_MAX_EVENTS = 600000
_MAX_SECONDS = 8.0
_CUR = None



PRELUDES = {
'ds': """
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    def __repr__(self):
        out, n, k = [], self, 0
        while n is not None and k < 12:
            out.append(str(n.val)); n = n.next; k += 1
        return ' -> '.join(out) + (' ...' if n is not None else '')

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
    def __repr__(self):
        return 'TreeNode(' + str(self.val) + ')'

def list_to_ll(a):
    head = None
    for v in reversed(a):
        head = ListNode(v, head)
    return head

def ll_to_list(h):
    out, k = [], 0
    while h is not None and k < 10000:
        out.append(h.val); h = h.next; k += 1
    return out

def list_to_tree(a):
    if not a or a[0] is None:
        return None
    root = TreeNode(a[0])
    q, i = [root], 1
    while q and i < len(a):
        n = q.pop(0)
        if i < len(a) and a[i] is not None:
            n.left = TreeNode(a[i]); q.append(n.left)
        i += 1
        if i < len(a) and a[i] is not None:
            n.right = TreeNode(a[i]); q.append(n.right)
        i += 1
    return root

def tree_to_list(r):
    if r is None:
        return []
    out, q = [], [r]
    while q:
        n = q.pop(0)
        if n is None:
            out.append(None)
        else:
            out.append(n.val); q.append(n.left); q.append(n.right)
    while out and out[-1] is None:
        out.pop()
    return out
"""
}

_CONV_IN = {'ll': 'list_to_ll', 'tree': 'list_to_tree'}
_CONV_OUT = {'ll': 'll_to_list', 'tree': 'tree_to_list'}


def _prelude_src(name_or_src):
    if not name_or_src:
        return ''
    return PRELUDES.get(name_or_src, name_or_src)


def _conv_args(g, args, conv):
    out = []
    for i, a in enumerate(args):
        c = conv[i] if conv and i < len(conv) else None
        out.append(g[_CONV_IN[c]](a) if c else a)
    return out


class _Abort(BaseException):
    """Stops runaway code. Not an Exception subclass so user try/except can't swallow it."""


def _short(s, n=70):
    return s if len(s) <= n else s[:n - 1] + '…'


def _desc(v, depth=0):
    """JSON-friendly description of a value for the variables panel."""
    t = type(v)
    try:
        if v is None or t is bool:
            return {'k': 'v', 'r': repr(v)}
        if t is int:
            r = repr(v)
            return {'k': 'v', 'r': r if len(r) < 40 else r[:36] + '…'}
        if t is float or t is complex:
            return {'k': 'v', 'r': repr(v)}
        if t is str:
            return {'k': 's', 'r': _short(repr(v), 90)}
        if depth > 2:
            return {'k': 'v', 'r': _short(repr(v), 40)}
        if t in (list, tuple, set, frozenset) or t is collections.deque:
            items = list(v)
            more = max(0, len(items) - 40)
            return {'k': 'list', 'ty': t.__name__, 'items': [_desc(x, depth + 1) for x in items[:40]], 'more': more}
        if isinstance(v, dict):
            items = list(v.items())
            more = max(0, len(items) - 24)
            return {'k': 'dict', 'ty': t.__name__, 'items': [[_desc(a, depth + 1), _desc(b, depth + 1)] for a, b in items[:24]], 'more': more}
        if isinstance(v, (types.FunctionType, types.BuiltinFunctionType, types.MethodType)):
            return {'k': 'v', 'r': '<function ' + getattr(v, '__name__', '?') + '>'}
        if hasattr(v, '__dict__') and not isinstance(v, type) and not isinstance(v, types.ModuleType):
            attrs = [[k, _desc(a, depth + 1)] for k, a in list(vars(v).items())[:12] if not k.startswith('__')]
            return {'k': 'obj', 'n': t.__name__, 'attrs': attrs}
        return {'k': 'v', 'r': _short(repr(v), 60)}
    except Exception:
        return {'k': 'v', 'r': '<' + t.__name__ + '>'}


def _frame_vars(frame, module):
    d = frame.f_globals if module else frame.f_locals
    out = []
    for k, v in list(d.items()):
        if k.startswith('__'):
            continue
        if module and isinstance(v, (types.ModuleType, types.FunctionType, types.BuiltinFunctionType, type)):
            continue
        out.append([k, _desc(v)])
    return out


class _Out(io.TextIOBase):
    def __init__(self):
        self.parts = []
        self.n = 0

    def write(self, s):
        s = str(s)
        self.parts.append(s)
        self.n += len(s)
        return len(s)

    def flush(self):
        pass

    def text(self):
        return ''.join(self.parts)


class _Tracer:
    def __init__(self, skip_module=False):
        self.steps = []
        self.loop_items = {}
        self.loops = []
        self.stack = []
        self.byframe = {}
        self.events = 0
        self.t0 = time.monotonic()
        self.truncated = False
        self.skip_module = skip_module
        self.out = _Out()
        self.next_loop = 1

    # ---- guards
    def check(self):
        self.events += 1
        if self.events > _MAX_EVENTS or (self.events % 2000 == 0 and time.monotonic() - self.t0 > _MAX_SECONDS):
            raise _Abort('Your code ran for too long. Does a loop never end?')

    # ---- trace callbacks
    def trace(self, frame, event, arg):
        code = frame.f_code
        if code.co_filename != _USER or code.co_name == '<genexpr>':
            return None
        self.check()
        if event == 'call':
            self.on_call(frame)
        return self.local

    def local(self, frame, event, arg):
        self.check()
        if event == 'line':
            self.on_line(frame)
        elif event == 'return':
            self.on_return(frame, arg)
        return self.local

    def label(self, frame):
        code = frame.f_code
        if code.co_name == '<module>':
            return 'main'
        names = code.co_varnames[:code.co_argcount]
        parts = []
        for n in names:
            if n in frame.f_locals:
                parts.append(n + '=' + _short(repr(frame.f_locals[n]), 18))
        return code.co_name + '(' + ', '.join(parts) + ')'

    def on_call(self, frame):
        module = frame.f_code.co_name == '<module>'
        rec = {'frame': frame, 'module': module, 'label': self.label(frame), 'cur': None, 'snap': {}}
        if module:
            for k, d in _frame_vars(frame, True):
                rec['snap'][k] = json.dumps(d)
        if self.stack:
            parent = self.stack[-1]
            if parent['cur'] and not parent['cur']['interrupted']:
                self.emit(parent, 'calls', parent['cur']['line'], callee=rec['label'])
                parent['cur']['interrupted'] = True
        self.stack.append(rec)
        self.byframe[id(frame)] = rec

    def on_line(self, frame):
        rec = self.byframe.get(id(frame))
        if rec is None:
            return
        if rec['cur']:
            self.emit(rec, 'finish' if rec['cur']['interrupted'] else 'line', rec['cur']['line'])
        rec['cur'] = {'line': frame.f_lineno, 'interrupted': False}

    def on_return(self, frame, value):
        rec = self.byframe.pop(id(frame), None)
        if rec is None:
            return
        if rec['cur']:
            if rec['module']:
                self.emit(rec, 'finish' if rec['cur']['interrupted'] else 'line', rec['cur']['line'])
            else:
                self.emit(rec, 'return', rec['cur']['line'], ret=value)
        rec['cur'] = None
        while self.stack and self.stack[-1] is not rec:
            self.stack.pop()
        if self.stack:
            self.stack.pop()

    # ---- loops
    def loop_gen(self, it, line, target, name, fid):
        items = [_short(repr(x), 22) for x in list(it)]
        lid = self.next_loop
        self.next_loop += 1
        if len(self.steps) < _MAX_STEPS:
            self.loop_items[lid] = items
        ctx = {'id': lid, 'i': -1, 'total': len(items), 'v': target, 'name': name, 'line': line, 'fid': fid}
        self.loops.append(ctx)
        try:
            for i, x in enumerate(it):
                ctx['i'] = i
                yield x
            ctx['i'] = len(items) - 1
            self.loop_done(ctx)
        finally:
            if ctx in self.loops:
                self.loops.remove(ctx)

    def loop_done(self, ctx):
        rec = self.byframe.get(ctx['fid'])
        if rec is None:
            return
        if rec['cur']:
            self.emit(rec, 'finish' if rec['cur']['interrupted'] else 'line', rec['cur']['line'])
            rec['cur'] = None
        self.emit(rec, 'loopdone', ctx['line'], loopdone=dict(ctx))

    # ---- step recording
    def emit(self, rec, typ, line, ret=None, callee=None, loopdone=None):
        if rec['module'] and self.skip_module:
            return
        if len(self.steps) >= _MAX_STEPS:
            self.truncated = True
            return
        frame = rec['frame']
        vars_ = _frame_vars(frame, rec['module'])
        changes = []
        snap = rec['snap']
        for k, d in vars_:
            j = json.dumps(d)
            old = snap.get(k)
            if old != j:
                oldd = json.loads(old) if old is not None else None
                ch = {'n': k, 'old': oldd, 'new': d}
                if oldd and oldd.get('k') == 'list' and d.get('k') == 'list' and len(d['items']) == len(oldd['items']) + 1 and d['more'] == 0:
                    ch['append'] = True
                if len(changes) < 6:
                    changes.append(ch)
                snap[k] = j
        step = {'line': line, 't': typ, 'vars': vars_, 'ch': changes,
                'st': [r['label'] for r in self.stack if not (r['module'] and self.skip_module)],
                'o': self.out.n}
        lp = loopdone
        if lp is None:
            fid = id(frame)
            for c in reversed(self.loops):
                if c['fid'] == fid:
                    lp = c
                    break
        if lp is not None:
            step['loop'] = {'id': lp['id'], 'i': lp['i'], 'total': lp['total'], 'v': lp['v'], 'name': lp['name'],
                            'line': lp['line'], 'done': loopdone is not None}
        if typ == 'return':
            step['ret'] = _desc(ret)
        if callee:
            step['callee'] = callee
        self.steps.append(step)


class _ForT(ast.NodeTransformer):
    def visit_For(self, node):
        self.generic_visit(node)
        tname = ast.unparse(node.target)
        iname = node.iter.id if isinstance(node.iter, ast.Name) else None
        call = ast.Call(func=ast.Name('__cfl_iter', ast.Load()),
                        args=[node.iter, ast.Constant(node.lineno), ast.Constant(tname), ast.Constant(iname)],
                        keywords=[])
        node.iter = ast.copy_location(call, node.iter)
        return node


def _iter_wrapper(it, line, target, name):
    T = _CUR
    if T is None:
        return it
    try:
        if isinstance(it, (enumerate, zip, reversed, map, filter)):
            lst = list(itertools.islice(it, 301))
            if len(lst) > 300:
                return itertools.chain(lst, it)
            it = lst
        if isinstance(it, (list, tuple, str, range, dict, set, frozenset)) and len(it) <= 300:
            fid = id(sys._getframe(1))
            return T.loop_gen(it, line, target, name, fid)
    except Exception:
        pass
    return it


def _err_info(e):
    line = None
    tb = e.__traceback__
    for fs in traceback.extract_tb(tb):
        if fs.filename == _USER:
            line = fs.lineno
    if isinstance(e, SyntaxError) and e.lineno:
        line = e.lineno
    msg = ''.join(traceback.format_exception_only(type(e), e)).strip()
    if isinstance(e, SyntaxError):
        msg = type(e).__name__ + ': ' + str(e.msg)
    return {'type': type(e).__name__, 'msg': msg, 'line': line}


def _compile_partial(code, err_line):
    """Code has a syntax error at err_line. Find the longest earlier prefix that compiles, so the
    lines the learner has already written still run."""
    lines = code.split('\n')
    upto = max(0, min(len(lines), (err_line or len(lines)) - 1))
    while upto > 0:
        chunk = lines[:upto]
        while chunk and (not chunk[-1].strip() or chunk[-1].strip().startswith('#')):
            chunk.pop()
        if not chunk:
            return None, 0
        last = chunk[-1]
        attempt = list(chunk)
        if last.rstrip().endswith(':'):
            indent = len(last) - len(last.lstrip())
            attempt.append(' ' * (indent + 4) + 'pass')
        src = '\n'.join(attempt)
        try:
            tree = ast.parse(src, _USER)
            return tree, len(chunk)
        except SyntaxError:
            upto = len(chunk) - 1
    return None, 0


def trace_run(payload_json):
    global _CUR
    P = json.loads(payload_json)
    code = P.get('code', '')
    prelude = _prelude_src(P.get('prelude', ''))
    setup = P.get('setup', '')
    call_fn = P.get('fn') if P.get('args') is not None else None
    call_args = P.get('args') or []
    conv = P.get('conv')
    conv_ret = P.get('conv_ret')
    skip_module = bool(P.get('skip_module'))
    stdin_lines = (P.get('stdin') or '').split('\n') if P.get('stdin') else []

    result = {'steps': [], 'loops': {}, 'out': '', 'error': None, 'syntax': None, 'truncated': False,
              'partial': None, 'result': None}

    tree = None
    try:
        tree = ast.parse(code, _USER)
    except SyntaxError as e:
        result['syntax'] = _err_info(e)
        tree, n = _compile_partial(code, e.lineno)
        result['partial'] = n
    if tree is None and result['syntax'] is None:
        tree = ast.parse('', _USER)
    if tree is None:
        tree = ast.parse('', _USER)

    tree = _ForT().visit(tree)
    ast.fix_missing_locations(tree)
    compiled = compile(tree, _USER, 'exec')

    T = _Tracer(skip_module)
    bi = dict(vars(builtins))
    stdin_iter = iter(stdin_lines)

    def my_input(prompt=''):
        T.out.write(str(prompt))
        try:
            v = next(stdin_iter)
        except StopIteration:
            raise EOFError('input() was called but there is no more input. Add lines in the Input box.')
        T.out.write(v + '\n')
        return v
    bi['input'] = my_input
    g = {'__name__': '__main__', '__builtins__': bi, '__cfl_iter': _iter_wrapper}

    old_out, old_trace = sys.stdout, sys.gettrace()
    sys.stdout = T.out
    _CUR = T
    try:
        try:
            if prelude:
                exec(compile(prelude, '<input>', 'exec'), g)
            if setup:
                exec(compile(setup, '<input>', 'exec'), g)
            sys.settrace(T.trace)
            exec(compiled, g)
            if call_fn:
                if call_fn not in g:
                    raise NameError("Your code needs a function named '" + call_fn + "'")
                argv = _conv_args(g, copy.deepcopy(call_args), conv)
                r = g[call_fn](*argv)
                if conv_ret:
                    sys.settrace(None)
                    r = g[_CONV_OUT[conv_ret]](r)
                g['__cfl_result'] = r
        except _Abort as e:
            result['error'] = {'type': 'TooLong', 'msg': str(e), 'line': (T.stack[-1]['cur']['line'] if T.stack and T.stack[-1]['cur'] else None)}
        except BaseException as e:
            result['error'] = _err_info(e)
    finally:
        sys.settrace(old_trace)
        sys.stdout = old_out
        _CUR = None
    if call_fn and '__cfl_result' in g:
        result['result'] = _desc(g['__cfl_result'])
    result['steps'] = T.steps
    result['loops'] = {str(k): v for k, v in T.loop_items.items()}
    result['out'] = T.out.text()
    result['truncated'] = T.truncated
    return json.dumps(result, ensure_ascii=False)


# ---------------------------------------------------------------- tests

def _norm(x):
    if isinstance(x, (tuple, list)):
        return [_norm(i) for i in x]
    if isinstance(x, (set, frozenset)):
        return sorted((_norm(i) for i in x), key=lambda v: json.dumps(v, sort_keys=True, default=str))
    if isinstance(x, dict):
        return {str(k): _norm(v) for k, v in x.items()}
    return x


def _sortkey(v):
    return json.dumps(v, sort_keys=True, default=str)


def _deep_sorted(x):
    if isinstance(x, list):
        return sorted((_deep_sorted(i) for i in x), key=_sortkey)
    return x


def _close(a, b):
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(_close(p, q) for p, q in zip(a, b))
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool) and not isinstance(b, bool):
        return math.isclose(a, b, rel_tol=1e-5, abs_tol=1e-6)
    return a == b


def _same(got, expect, mode):
    g, e = _norm(got), _norm(expect)
    if mode == 'unordered':
        return isinstance(g, list) and isinstance(e, list) and sorted(g, key=_sortkey) == sorted(e, key=_sortkey)
    if mode == 'nested_unordered':
        return _deep_sorted(g) == _deep_sorted(e)
    if mode == 'float':
        return _close(g, e)
    return g == e


def run_tests(payload_json):
    P = json.loads(payload_json)
    code, fn = P['code'], P['fn']
    mode = P.get('compare', 'exact')
    inplace = P.get('inplace')
    prelude = _prelude_src(P.get('prelude', ''))
    conv = P.get('conv')
    conv_ret = P.get('conv_ret')
    out = {'compile_error': None, 'results': []}
    try:
        compiled = compile(code, _USER, 'exec')
    except SyntaxError as e:
        out['compile_error'] = _err_info(e)
        return json.dumps(out, ensure_ascii=False)
    for idx, t in enumerate(P['tests']):
        res = {'i': idx, 'ok': False, 'args': _short(', '.join(repr(a) for a in t.get('args', [])), 120),
               'expect': _short(repr(t.get('expect')), 120), 'got': None, 'error': None, 'stdout': ''}
        buf = _Out()
        old = sys.stdout
        sys.stdout = buf
        t0 = time.monotonic()
        try:
            g = {'__name__': '__main__'}
            if prelude:
                exec(compile(prelude, '<input>', 'exec'), g)
            exec(compiled, g)
            if fn not in g:
                raise NameError("Your code needs a function named '" + fn + "'")
            args = _conv_args(g, copy.deepcopy(t.get('args', [])), conv)
            got = g[fn](*args)
            if inplace is not None:
                got = args[inplace]
            if conv_ret:
                got = g[_CONV_OUT[conv_ret]](got)
            res['got'] = _short(repr(got), 120)
            res['ok'] = _same(got, t.get('expect'), mode)
        except BaseException as e:
            info = _err_info(e)
            res['error'] = info['msg'] + (' (line ' + str(info['line']) + ')' if info['line'] else '')
        finally:
            sys.stdout = old
        res['ms'] = int((time.monotonic() - t0) * 1000)
        res['stdout'] = _short(buf.text(), 200)
        out['results'].append(res)
    return json.dumps(out, ensure_ascii=False)
