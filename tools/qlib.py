"""Helpers for authoring questions. Each tools/src/*.py defines Q via add()/qa()."""
import ast

Q = []
DIFF = {1: 'Easy', 2: 'Medium', 3: 'Hard'}


def _starter(ref, fn):
    tree = ast.parse(ref)
    for n in tree.body:
        if isinstance(n, ast.FunctionDef) and n.name == fn:
            return 'def %s(%s):\n    # your code here\n    pass' % (fn, ', '.join(a.arg for a in n.args.args))
    raise ValueError('no function ' + fn)


def add(id, title, section, topic, pattern, diff, sets, q, fn, ref, ex, more=(), compare='exact',
        hints=(), inplace=None, prelude=None, conv=None, conv_ret=None, starter=None, note=None):
    """ex = (args_list, expect) explicit example from the statement; more = arg lists whose
    expected value is computed from ref by tools/build.py."""
    tests = [{'args': ex[0], 'expect': ex[1]}]
    for a in more:
        tests.append({'args': a})
    d = dict(id=id, kind='function', title=title, section=section, topic=topic, pattern=pattern,
             difficulty=DIFF[diff], sets=list(sets), q=q, fn=fn, starter=starter or _starter(ref, fn),
             ref=ref, tests=tests, compare=compare, hints=list(hints))
    if inplace is not None:
        d['inplace'] = inplace
    if prelude:
        d['prelude'] = prelude
    if conv:
        d['conv'] = conv
    if conv_ret:
        d['conv_ret'] = conv_ret
    if note:
        d['note'] = note
    Q.append(d)


def qa(id, title, topic, level, q, answer, hints=(), sets=('Interview Q&A',), code=None):
    d = dict(id=id, kind='qa', title=title, section='Interview Q&A', topic=topic, pattern=level,
             difficulty={'Basic': 'Easy', 'Intermediate': 'Medium', 'Advanced': 'Hard'}[level],
             sets=list(sets), q=q, answer=answer, hints=list(hints))
    if code:
        d['code'] = code
    Q.append(d)
