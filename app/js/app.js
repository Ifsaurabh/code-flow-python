import { createRunner } from './runner.js';
import { draftsFromText, guessSetup, textFromPdf } from './importer.js';

const $ = (s, r = document) => r.querySelector(s);
const el = (tag, attrs = {}, ...kids) => {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === 'class') e.className = v; else if (k === 'html') e.innerHTML = v;
    else if (k.startsWith('on')) e.addEventListener(k.slice(2), v); else if (v !== false && v != null) e.setAttribute(k, v === true ? '' : v);
  }
  for (const k of kids.flat()) if (k != null) e.append(k.nodeType ? k : document.createTextNode(k));
  return e;
};
const esc = (s) => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

// ------------------------------------------------------------ state + storage
const KEY = 'codeflowpython.v1';
let store = { solved: {}, review: {}, code: {}, input: {}, custom: [], last: null, hints: {} };
try { Object.assign(store, JSON.parse(localStorage.getItem(KEY) || '{}')); } catch (e) {}
let saveT = 0;
const save = () => { clearTimeout(saveT); saveT = setTimeout(() => { try { localStorage.setItem(KEY, JSON.stringify(store)); } catch (e) {} }, 250); };

let QS = [];            // all questions (built-in + custom)
let byId = new Map();
let cur = null;         // current question
let view = 'browse';
let listIds = [];       // ids in current browse order (for prev/next)
let groupBy = 'section';
const F = { search: '', section: '', topic: '', pattern: '', set: '', diff: '', status: '' };

// ------------------------------------------------------------ python runner
const pill = $('#pill');
let pyReady = false;
const runner = window.CFP_RUNNER || createRunner((st, info) => {
  pyReady = st === 'ready';
  pill.className = 'pill ' + (st === 'ready' ? 'ready' : st === 'error' ? 'err' : '');
  pill.textContent = st === 'ready' ? 'Python ' + info : st === 'error' ? 'Python failed: ' + info : 'Python loading…';
  if (st === 'ready' && view !== 'browse' && cur) schedule(10);
});

// ------------------------------------------------------------ data
async function loadQuestions() {
  const idx = await (await fetch('data/index.json')).json();
  const all = [];
  for (const f of idx.files) all.push(...await (await fetch(f.file)).json());
  QS = all.concat(store.custom.map(q => ({ ...q, custom: true })));
  byId = new Map(QS.map(q => [q.id, q]));
}
const status = (id) => store.solved[id] ? 'solved' : store.review[id] ? 'review' : 'todo';
const SECTION_ORDER = ['Python Basics', 'Core Python', 'Data Structures & Algorithms', 'Interview Q&A', 'My Questions'];
const TOPIC_ORDER = ['Arrays & Hashing', 'Two Pointers', 'Sliding Window', 'Stack', 'Binary Search', 'Linked List', 'Trees', 'Heap / Priority Queue', 'Backtracking', 'Graphs', '1-D Dynamic Programming', '2-D Dynamic Programming', 'Greedy', 'Intervals', 'Math & Bit Manipulation', 'Design'];

// ------------------------------------------------------------ browse
function matches(q) {
  if (F.section && q.section !== F.section) return false;
  if (F.topic && q.topic !== F.topic) return false;
  if (F.pattern && q.pattern !== F.pattern) return false;
  if (F.set && !(q.sets || []).includes(F.set)) return false;
  if (F.diff && q.difficulty !== F.diff) return false;
  if (F.status && status(q.id) !== F.status) return false;
  if (F.search) {
    const s = F.search.toLowerCase();
    if (!(q.title + ' ' + q.q + ' ' + q.topic + ' ' + q.pattern).toLowerCase().includes(s)) return false;
  }
  return true;
}
const uniq = (arr) => [...new Set(arr)].filter(Boolean);
function fillSelect(sel, label, values, key) {
  const old = F[key];
  sel.innerHTML = '';
  sel.append(el('option', { value: '' }, label));
  for (const v of values) sel.append(el('option', { value: v }, v));
  sel.value = values.includes(old) ? old : '';
  F[key] = sel.value;
}
function buildFilters() {
  const ord = (vals, order) => vals.sort((a, b) => { const x = order.indexOf(a), y = order.indexOf(b); return (x < 0 ? 99 : x) - (y < 0 ? 99 : y) || a.localeCompare(b); });
  fillSelect($('#f-section'), 'All sections', ord(uniq(QS.map(q => q.section)), SECTION_ORDER), 'section');
  const inSec = QS.filter(q => !F.section || q.section === F.section);
  fillSelect($('#f-topic'), 'All topics', ord(uniq(inSec.map(q => q.topic)), TOPIC_ORDER), 'topic');
  const inTop = inSec.filter(q => !F.topic || q.topic === F.topic);
  fillSelect($('#f-pattern'), 'All patterns', uniq(inTop.map(q => q.pattern)).sort(), 'pattern');
  fillSelect($('#f-set'), 'All question sets', uniq(QS.flatMap(q => q.sets || [])).sort(), 'set');
  fillSelect($('#f-diff'), 'Any difficulty', ['Easy', 'Medium', 'Hard'], 'diff');
  const st = $('#f-status'); st.innerHTML = '';
  [['', 'Any status'], ['todo', 'Not done'], ['solved', 'Solved'], ['review', 'Needs review']].forEach(([v, l]) => st.append(el('option', { value: v }, l)));
  st.value = F.status;
}
function renderBrowse() {
  const list = QS.filter(matches);
  const groups = new Map();
  for (const q of list) {
    const keys = groupBy === 'set' ? ((q.sets && q.sets.length) ? q.sets : ['No set']) : [q[groupBy] || '—'];
    for (const k of keys) { if (!groups.has(k)) groups.set(k, []); groups.get(k).push(q); }
  }
  const order = groupBy === 'section' ? SECTION_ORDER : groupBy === 'topic' ? TOPIC_ORDER : [];
  const keys = [...groups.keys()].sort((a, b) => { const x = order.indexOf(a), y = order.indexOf(b); return (x < 0 ? 99 : x) - (y < 0 ? 99 : y) || a.localeCompare(b); });
  const root = $('#groups'); root.innerHTML = '';
  listIds = [];
  const doneAll = QS.filter(q => store.solved[q.id]).length;
  $('#summary').textContent = `${list.length} of ${QS.length} questions · ${doneAll} solved`;
  const openAll = keys.length <= 3 || !!F.search;
  for (const k of keys) {
    const qs = groups.get(k);
    const done = qs.filter(q => store.solved[q.id]).length;
    const d = el('details', { class: 'group' });
    if (openAll || sessionStorage.getItem('open:' + groupBy + k)) d.open = true;
    d.addEventListener('toggle', () => { try { d.open ? sessionStorage.setItem('open:' + groupBy + k, '1') : sessionStorage.removeItem('open:' + groupBy + k); } catch (e) {} });
    d.append(el('summary', {}, k, el('span', { class: 'cnt' }, `${done}/${qs.length}`), el('div', { class: 'bar' }, el('b', { style: `width:${Math.round(100 * done / qs.length)}%` }))));
    for (const q of qs) {
      listIds.push(q.id);
      const s = status(q.id);
      d.append(el('div', { class: 'qrow', onclick: () => openQuestion(q.id) },
        el('div', { class: 'dot ' + (s === 'solved' ? 'done' : s === 'review' ? 'rev' : '') }, s === 'solved' ? '✓' : s === 'review' ? '↻' : ''),
        el('div', { class: 't' }, el('b', {}, q.title), el('span', {}, [q.topic, q.pattern].filter(Boolean).join(' · '))),
        q.kind === 'qa' ? el('span', { class: 'tag' }, 'Q&A') : null,
        el('span', { class: 'tag ' + q.difficulty }, q.difficulty || '—')));
    }
    root.append(d);
  }
  if (!keys.length) root.append(el('div', { class: 'card mute' }, 'No questions match these filters.'));
}

// ------------------------------------------------------------ practice
let steps = [], loops = {}, result = null, pos = 0, playing = false, playT = 0, runSeq = 0, debT = 0;
let expectedOut = null, testRes = null, testIdx = 0, ed = null, gut = null, inputBox = null, stdinBox = null;

function setView(v) {
  view = v;
  for (const id of ['browse', 'practice']) $('#v-' + id).classList.toggle('hide', (v === 'browse') !== (id === 'browse'));
  document.querySelectorAll('#tabs button').forEach(b => b.classList.toggle('on', b.dataset.v === v));
  if (v !== 'browse') window.scrollTo(0, 0);
}
function sandboxQ() {
  return { id: 'sandbox', kind: 'free', title: 'Sandbox', section: 'Sandbox', topic: '', pattern: '', difficulty: '', sets: [], q: 'Write any Python 3 code. Watch it run line by line. Use the Input box to define data, e.g. numbers = [3, 7, 2, 5].', setup: 'numbers = [3, 7, 2, 5]', starter: '', hints: [] };
}
function openQuestion(id) {
  const q = id === 'sandbox' ? sandboxQ() : byId.get(id);
  if (!q) return;
  stopPlay();
  cur = q; store.last = id; save();
  steps = []; loops = {}; result = null; pos = 0; testRes = null; testIdx = 0; expectedOut = null;
  setView(id === 'sandbox' ? 'sandbox' : 'practice');
  buildPractice();
  if (q.kind !== 'qa') { fetchExpected(); schedule(10); }
}
function curCode() {
  const c = store.code[cur.id];
  return c != null ? c : (cur.starter || '');
}

function buildPractice() {
  const q = cur;
  const isQA = q.kind === 'qa';
  // question card
  const cq = $('#c-question'); cq.innerHTML = '';
  const idx = listIds.indexOf(q.id);
  cq.append(el('h3', {}, 'Question', el('span', { class: 'sp row' },
    el('button', { class: 'btn sm', disabled: idx <= 0, onclick: () => openQuestion(listIds[idx - 1]) }, '‹ Prev'),
    el('button', { class: 'btn sm', disabled: idx < 0 || idx >= listIds.length - 1, onclick: () => openQuestion(listIds[idx + 1]) }, 'Next ›'))));
  cq.append(el('div', { class: 'qtitle' }, q.title));
  cq.append(el('div', { class: 'row small' }, ...[q.section, q.topic, q.pattern].filter(Boolean).map(x => el('span', { class: 'tag' }, x)),
    q.difficulty ? el('span', { class: 'tag ' + q.difficulty }, q.difficulty) : null, ...(q.sets || []).map(x => el('span', { class: 'tag' }, x))));
  cq.append(el('p', { class: 'qtext' }, q.q));
  if (q.note) cq.append(el('div', { class: 'msg info' }, q.note));
  const ci = $('#c-input'), cc = $('#c-code'), cx = $('#c-extra'), cf = $('#c-flow'), co = $('#c-output'), ct = $('#c-tests'), cs = $('#c-solution');
  for (const c of [ci, cc, cx, cf, co, ct, cs]) { c.innerHTML = ''; c.classList.remove('hide'); }
  ct.classList.toggle('hide', q.kind !== 'function');
  cs.classList.add('hide');
  ed = gut = inputBox = stdinBox = null;

  if (isQA) { buildQA(q, ci, cc, cx); cf.classList.add('hide'); co.classList.add('hide'); buildSolutionQA(q, cs); return; }
  cf.classList.remove('hide'); co.classList.remove('hide');

  // input card
  if (q.kind === 'function') {
    ci.append(el('h3', {}, 'Input', el('span', { class: 'sp' }, 'pick a test case to watch')));
    ci.append(el('select', { id: 'test-pick', class: 'input-box', style: 'min-height:0;width:100%', onchange: (e) => { testIdx = +e.target.value; updateCall(); schedule(10); } },
      ...q.tests.map((t, i) => el('option', { value: i }, 'Test ' + (i + 1) + ': ' + q.fn + '(' + t.args.map(a => JSON.stringify(a)).join(', ') + ')'))));
    ci.append(el('div', { class: 'small mute', style: 'margin-top:6px' }, 'Your function gets this test input. Edit your code and the flow updates live.'));
  } else {
    ci.append(el('h3', {}, 'Input', el('span', { class: 'sp' }, 'edit the data and see what changes')));
    inputBox = el('textarea', { class: 'input-box', rows: 2, spellcheck: 'false', placeholder: 'e.g. numbers = [3, 7, 2, 5]' });
    inputBox.value = store.input[q.id] != null ? store.input[q.id] : (q.setup || '');
    inputBox.addEventListener('input', () => { store.input[q.id] = inputBox.value; save(); schedule(350); });
    ci.append(inputBox);
    stdinBox = el('textarea', { class: 'input-box', rows: 1, spellcheck: 'false', placeholder: 'Lines for input(), one per line (optional)' });
    stdinBox.style.marginTop = '6px';
    stdinBox.addEventListener('input', () => schedule(350));
    ci.append(stdinBox);
  }

  // code card
  cc.append(el('h3', {}, 'Your Python', el('span', { class: 'sp row' },
    el('button', { class: 'btn sm', onclick: () => { if (confirm('Reset your code for this question?')) { delete store.code[q.id]; ed.value = q.starter || ''; onEdit(); } } }, 'Reset'))));
  gut = el('div', { class: 'gutter' });
  ed = el('textarea', { spellcheck: 'false', autocapitalize: 'off', autocomplete: 'off', autocorrect: 'off', placeholder: q.kind === 'function' ? '' : '# type your code here' });
  ed.value = curCode();
  cc.append(el('div', { class: 'editor' }, gut, ed));
  ed.addEventListener('input', onEdit);
  ed.addEventListener('scroll', () => { gut.scrollTop = ed.scrollTop; });
  ed.addEventListener('keydown', onKey);
  const keys = el('div', { class: 'keys' });
  ['Tab', ':', '(', ')', '[', ']', '{', '}', '"', "'", '=', '==', '+', '-', '*', '/', '%', '#', ',', '.', '_'].forEach(k => keys.append(el('button', { type: 'button', onmousedown: (e) => e.preventDefault(), onclick: () => insertText(k === 'Tab' ? '    ' : k) }, k)));
  cc.append(keys);
  cc.append(el('div', { id: 'code-msg' }));
  drawGutter();

  // flow + output + tests + solution
  buildFlowShell(cf);
  co.append(el('h3', {}, 'Output', el('span', { class: 'sp', id: 'out-state' })));
  co.append(el('pre', { class: 'out', id: 'out' }));
  co.append(el('div', { id: 'out-expect' }));
  if (q.kind === 'function') {
    ct.append(el('h3', {}, 'Tests', el('span', { class: 'sp', id: 'test-sum' }), el('button', { class: 'btn sm', onclick: () => runTests() }, 'Run all')));
    ct.append(el('div', { class: 'tests', id: 'tests' }));
    updateTests();
  }
  buildSolution(q, cs);
  if (q.kind === 'function') updateCall();
}

// ---- editor helpers
function onEdit() { store.code[cur.id] = ed.value; save(); drawGutter(); schedule(450); }
function insertText(t) {
  const s = ed.selectionStart, e = ed.selectionEnd;
  ed.setRangeText(t, s, e, 'end'); ed.focus(); onEdit();
}
function onKey(e) {
  if (e.key === 'Tab') { e.preventDefault(); insertText('    '); return; }
  if (e.key === 'Enter') {
    const s = ed.selectionStart, v = ed.value;
    const ls = v.lastIndexOf('\n', s - 1) + 1;
    const line = v.slice(ls, s);
    const indent = /^\s*/.exec(line)[0];
    const extra = /:\s*(#.*)?$/.test(line) ? '    ' : '';
    e.preventDefault(); insertText('\n' + indent + extra);
  }
}
let curLine = 0, errLine = 0, partialN = null;
function drawGutter() {
  if (!gut) return;
  const n = ed.value.split('\n').length;
  gut.innerHTML = '';
  for (let i = 1; i <= n; i++) {
    gut.append(el('div', { class: (i === curLine ? 'cur ' : '') + (i === errLine ? 'err ' : '') + (partialN != null && i > partialN && ed.value.split('\n')[i - 1].trim() ? 'skip' : '') }, String(i)));
  }
  gut.scrollTop = ed.scrollTop;
}

// ---- running
function schedule(ms) {
  clearTimeout(debT);
  debT = setTimeout(run, ms);
}
function updateCall() { /* the call is built in payload() */ }
function payload() {
  const q = cur;
  const code = ed ? ed.value : '';
  if (q.kind === 'function') {
    const t = q.tests[testIdx] || q.tests[0];
    return { code, fn: q.fn, args: t.args, prelude: q.prelude || '', conv: q.conv || null, conv_ret: q.conv_ret || null, skip_module: true };
  }
  return { code, setup: inputBox ? inputBox.value : '', stdin: stdinBox ? stdinBox.value : '' };
}
async function run() {
  if (!cur || cur.kind === 'qa' || !ed) return;
  const my = ++runSeq;
  const p = payload();
  if (!p.code.trim()) { result = null; steps = []; renderAll(true); return; }
  $('#out-state').textContent = 'running…';
  let r;
  try { r = await runner.trace(p); } catch (e) { if (my !== runSeq) return; showFatal(e.message); return; }
  if (my !== runSeq) return;
  result = r; steps = r.steps; loops = r.loops || {};
  pos = Math.max(0, steps.length - 1);
  errLine = r.error && r.error.line ? r.error.line : (r.syntax ? r.syntax.line : 0);
  partialN = r.syntax ? r.partial : null;
  renderAll(false);
  if (cur.kind === 'function' && !r.error && !r.syntax) runTests(true);
  else if (cur.kind === 'function') { testRes = null; updateTests(); }
  checkScriptDone();
}
function showFatal(msg) { $('#out-state').textContent = ''; $('#code-msg').innerHTML = ''; $('#code-msg').append(el('div', { class: 'msg bad' }, msg)); }
async function fetchExpected() {
  const q = cur;
  if (q.kind === 'qa' || !q.ref) return;
  if (q.kind === 'script') {
    try { const r = await runner.trace({ code: q.ref, setup: q.setup || '' }); if (cur === q) { expectedOut = r.out; showExpected(); } } catch (e) {}
  }
}
function showExpected() {
  const box = $('#out-expect'); if (!box) return;
  box.innerHTML = '';
  if (expectedOut != null && cur.kind === 'script') {
    const same = result && result.out === expectedOut && !result.error;
    box.append(el('div', { class: 'small ' + (same ? 't-ok' : 'mute'), style: 'margin-top:6px' }, same ? '✓ Matches the expected output' : 'Expected output: ' + (expectedOut.trim() ? '' : '(nothing)')));
    if (!same && expectedOut.trim()) box.append(el('pre', { class: 'out', style: 'margin-top:4px;min-height:0' }, expectedOut));
  }
}
function checkScriptDone() {
  showExpected();
  if (cur.kind === 'script' && expectedOut != null && result && !result.error && !result.syntax && result.out === expectedOut && ed.value.trim() && ed.value.trim() !== (cur.ref || '').trim()) markSolved(true);
  else if (cur.kind === 'script' && expectedOut != null && result && !result.error && result.out === expectedOut && ed.value.trim()) markSolved(true);
}
function markSolved(auto) {
  if (store.solved[cur.id]) return;
  store.solved[cur.id] = Date.now(); delete store.review[cur.id]; save();
  toast(auto ? '✓ Solved! Nice work.' : 'Marked solved');
}
async function runTests(auto) {
  if (cur.kind !== 'function' || !ed) return;
  const my = runSeq;
  $('#test-sum').textContent = 'running…';
  try {
    const r = await runner.tests({ code: ed.value, fn: cur.fn, tests: cur.tests, compare: cur.compare, inplace: cur.inplace ?? null, prelude: cur.prelude || '', conv: cur.conv || null, conv_ret: cur.conv_ret || null });
    if (my !== runSeq && auto) { /* a newer edit exists */ }
    testRes = r; updateTests();
    if (r.results && r.results.length && r.results.every(x => x.ok)) { if (!store.solved[cur.id]) markSolved(true); }
  } catch (e) { $('#test-sum').textContent = e.message; }
}
function updateTests() {
  const box = $('#tests'); if (!box) return;
  box.innerHTML = '';
  const sum = $('#test-sum');
  if (!testRes) { sum.textContent = 'not run yet'; box.append(el('div', { class: 'mute small' }, 'Tests run automatically once your code runs without errors.')); return; }
  if (testRes.compile_error) { sum.textContent = ''; box.append(el('div', { class: 'msg bad' }, testRes.compile_error.msg)); return; }
  const pass = testRes.results.filter(x => x.ok).length;
  sum.innerHTML = `<span class="${pass === testRes.results.length ? 't-ok' : 't-bad'}">${pass}/${testRes.results.length} passed</span>`;
  testRes.results.forEach((r, i) => {
    box.append(el('div', { class: 'test ' + (r.ok ? 'ok' : 'no') },
      el('div', { class: r.ok ? 't-ok' : 't-bad' }, r.ok ? '✓' : '✗'),
      el('div', {}, el('div', {}, cur.fn + '(' + r.args + ')'),
        r.ok ? null : el('div', { class: 'mute' }, 'expected ' + r.expect),
        r.error ? el('div', { class: 't-bad' }, r.error) : (r.ok ? null : el('div', {}, 'got ' + r.got)),
        r.stdout ? el('div', { class: 'mute' }, 'printed: ' + r.stdout) : null,
        el('button', { class: 'btn sm', style: 'margin-top:3px', onclick: () => { testIdx = i; const sel = $('#test-pick'); if (sel) sel.value = i; schedule(10); window.scrollTo({ top: 0, behavior: 'smooth' }); } }, 'Watch this test'))));
  });
}

// ---- flow view
function buildFlowShell(cf) {
  cf.append(el('h3', {}, 'Live flow', el('span', { class: 'sp', id: 'step-lbl' })));
  cf.append(el('div', { id: 'code-note' }));
  cf.append(el('div', { class: 'pb' },
    el('button', { class: 'btn sm', id: 'pb-first', title: 'Start', onclick: () => { stopPlay(); pos = 0; renderFlow(); } }, '⏮'),
    el('button', { class: 'btn sm', id: 'pb-prev', onclick: () => { stopPlay(); pos = Math.max(0, pos - 1); renderFlow(); } }, '◀'),
    el('button', { class: 'btn sm pri', id: 'pb-play', onclick: togglePlay }, '▶ Play'),
    el('button', { class: 'btn sm', id: 'pb-next', onclick: () => { stopPlay(); pos = Math.min(steps.length - 1, pos + 1); renderFlow(); } }, '▶|'),
    el('button', { class: 'btn sm', id: 'pb-last', title: 'End', onclick: () => { stopPlay(); pos = steps.length - 1; renderFlow(); } }, '⏭'),
    el('input', { type: 'range', id: 'pb-range', min: 0, max: 0, value: 0, oninput: (e) => { stopPlay(); pos = +e.target.value; renderFlow(); } }),
    el('select', { id: 'pb-speed', class: 'btn sm' }, el('option', { value: 900 }, 'Slow'), el('option', { value: 450, selected: true }, 'Normal'), el('option', { value: 160 }, 'Fast'))));
  cf.append(el('div', { class: 'now', id: 'now' }));
  cf.append(el('div', { id: 'loopbox' }));
  cf.append(el('div', { class: 'stack', id: 'stackbox' }));
  cf.append(el('div', { class: 'vars', id: 'varbox' }));
}
function renderAll(empty) {
  $('#code-msg').innerHTML = ''; $('#code-note').innerHTML = '';
  if (empty) { curLine = 0; errLine = 0; partialN = null; drawGutter(); $('#out').textContent = ''; $('#out-state').textContent = ''; $('#now').textContent = 'Start typing. Every line you write runs here as real Python.'; $('#varbox').innerHTML = ''; $('#loopbox').innerHTML = ''; $('#stackbox').innerHTML = ''; $('#step-lbl').textContent = ''; return; }
  const r = result;
  const msg = $('#code-msg');
  if (r.syntax) msg.append(el('div', { class: 'msg warn' }, `Line ${r.syntax.line || '?'}: ${r.syntax.msg}` + (r.partial ? `. Running the ${r.partial} line${r.partial > 1 ? 's' : ''} before it.` : '. Nothing can run yet.')));
  if (r.error) msg.append(el('div', { class: 'msg bad' }, (r.error.line ? `Line ${r.error.line}: ` : '') + r.error.msg));
  if (r.truncated) msg.append(el('div', { class: 'msg info' }, 'This run has many steps, showing the first ' + steps.length + '. The output is complete.'));
  $('#out').textContent = r.out;
  $('#out-state').textContent = r.error ? 'stopped by an error' : (r.syntax ? 'partial code' : 'finished');
  if (cur.kind === 'function' && r.result && !r.error) $('#out').textContent = (r.out ? r.out + '\n' : '') + '→ returned ' + descText(r.result);
  const range = $('#pb-range'); range.max = Math.max(0, steps.length - 1);
  renderFlow();
  drawGutter();
}
function descText(d) {
  if (!d) return '';
  if (d.k === 'v' || d.k === 's') return d.r;
  if (d.k === 'list') return (d.ty === 'list' ? '[' : d.ty + '(') + d.items.map(descText).join(', ') + (d.more ? ', …' : '') + (d.ty === 'list' ? ']' : ')');
  if (d.k === 'dict') return '{' + d.items.map(([a, b]) => descText(a) + ': ' + descText(b)).join(', ') + (d.more ? ', …' : '') + '}';
  return d.n || '?';
}
function renderVal(d, newIdx) {
  if (!d) return el('span', { class: 'v' }, '—');
  if (d.k === 'v') return el('span', { class: 'v' }, d.r);
  if (d.k === 's') return el('span', { class: 'v' }, d.r);
  if (d.k === 'list') {
    const box = el('div', { class: 'cells' });
    if (!d.items.length) box.append(el('span', { class: 'mute small' }, d.ty === 'list' ? '[ ] empty' : d.ty + ' empty'));
    d.items.forEach((x, i) => box.append(el('span', { class: 'cell' + (newIdx === i ? ' new' : '') }, descText(x))));
    if (d.more) box.append(el('span', { class: 'cell' }, '+' + d.more + ' more'));
    return el('div', {}, d.ty !== 'list' ? el('span', { class: 'mute small' }, d.ty + ' ') : null, box);
  }
  if (d.k === 'dict') {
    const t = el('table', { class: 'kv' });
    if (!d.items.length) return el('span', { class: 'mute small' }, '{ } empty');
    d.items.forEach(([a, b]) => t.append(el('tr', {}, el('td', {}, descText(a)), el('td', {}, descText(b)))));
    if (d.more) t.append(el('tr', {}, el('td', { colspan: 2 }, '+' + d.more + ' more')));
    return t;
  }
  if (d.k === 'obj') return el('div', { class: 'v' }, d.n + ' { ' + d.attrs.map(([k, v]) => k + '=' + descText(v)).join(', ') + ' }');
  return el('span', {}, '?');
}
function renderFlow() {
  const s = steps[pos];
  $('#pb-range').value = pos;
  $('#step-lbl').textContent = steps.length ? `step ${pos + 1} / ${steps.length}` : '';
  $('#pb-play').textContent = playing ? '⏸ Pause' : '▶ Play';
  const now = $('#now'), vb = $('#varbox'), lb = $('#loopbox'), sb = $('#stackbox');
  vb.innerHTML = ''; lb.innerHTML = ''; sb.innerHTML = '';
  if (!s) {
    now.textContent = result && (result.syntax || result.error) ? 'Nothing has run yet. Fix the message under your code.' : 'Nothing ran. Write some code.';
    curLine = 0; drawGutter(); return;
  }
  const lines = ed.value.split('\n');
  const text = (lines[s.line - 1] || '').trim();
  curLine = s.line;
  const verb = { line: 'ran', finish: 'ran', calls: 'is calling ' + (s.callee || ''), return: 'returns ' + (s.ret ? descText(s.ret) : ''), loopdone: 'the loop finished' }[s.t] || '';
  now.innerHTML = `line ${s.line}: <b>${esc(text)}</b>` + (verb && s.t !== 'line' && s.t !== 'finish' ? `  →  ${esc(verb)}` : '');
  if (s.ch && s.ch.length && s.t !== 'loopdone') now.innerHTML += '\n' + s.ch.map(c => `${esc(c.n)}: ${c.old ? esc(descText(c.old)) + ' → ' : 'new '}<b>${esc(descText(c.new))}</b>`).join('   ');
  // loop strip
  if (s.loop) {
    const items = loops[s.loop.id] || [];
    const done = s.loop.done;
    lb.append(el('div', { class: 'small mute' }, `for ${s.loop.v} in ${s.loop.name || '…'} · ` + (done ? 'finished all ' + s.loop.total : `item ${s.loop.i + 1} of ${s.loop.total}`)));
    const row = el('div', { class: 'chips' });
    items.forEach((it, i) => row.append(el('span', { class: 'chip ' + (done || i < s.loop.i ? 'past' : i === s.loop.i ? 'cur' : '') }, it)));
    lb.append(row);
  }
  if (s.st && s.st.length > 1) s.st.forEach(x => sb.append(el('span', {}, x)));
  const chgNames = new Map((s.ch || []).map(c => [c.n, c]));
  if (!s.vars.length) vb.append(el('div', { class: 'mute small' }, 'No variables yet.'));
  s.vars.forEach(([n, d]) => {
    const c = chgNames.get(n);
    const card = el('div', { class: 'var' + (c ? ' chg' : '') }, el('div', { class: 'n' }, n));
    if (c && c.old && d.k !== 'list' && d.k !== 'dict') card.append(el('div', { class: 'o' }, descText(c.old)));
    card.append(renderVal(d, c && c.append ? d.items.length - 1 : -1));
    vb.append(card);
  });
  // output so far
  if (result) {
    const sofar = result.out.slice(0, s.o);
    if (steps.length > 1) $('#out').textContent = (cur.kind === 'function' && pos === steps.length - 1 && result.result && !result.error) ? (result.out ? result.out + '\n' : '') + '→ returned ' + descText(result.result) : sofar;
    else $('#out').textContent = result.out;
  }
  drawGutter();
}
function togglePlay() {
  if (playing) { stopPlay(); renderFlow(); return; }
  if (!steps.length) return;
  if (pos >= steps.length - 1) pos = 0;
  playing = true; renderFlow();
  const base = +$('#pb-speed').value;
  const tick = () => {
    if (!playing) return;
    if (pos >= steps.length - 1) { stopPlay(); renderFlow(); return; }
    pos++; renderFlow();
    playT = setTimeout(tick, steps.length > 120 ? Math.min(base, 120) : base);
  };
  renderFlow();
  playT = setTimeout(tick, 200);
}
function stopPlay() { playing = false; clearTimeout(playT); }

// ---- solution + QA
function buildSolution(q, cs) {
  cs.classList.remove('hide');
  cs.append(el('h3', {}, 'Help & solution'));
  const hints = q.hints || [];
  if (hints.length) {
    const box = el('div', {});
    const shown = store.hints[q.id] || 0;
    const draw = () => {
      box.innerHTML = '';
      (q.hints || []).slice(0, store.hints[q.id] || 0).forEach((h, i) => box.append(el('div', { class: 'msg info' }, 'Hint ' + (i + 1) + ': ' + h)));
      if ((store.hints[q.id] || 0) < hints.length) box.append(el('button', { class: 'btn sm', style: 'margin-top:8px', onclick: () => { store.hints[q.id] = (store.hints[q.id] || 0) + 1; save(); draw(); } }, 'Show hint ' + ((store.hints[q.id] || 0) + 1) + ' of ' + hints.length));
    };
    draw(); cs.append(box);
  }
  if (q.ref) {
    const d = el('details', { class: 'sol', style: 'margin-top:8px' }, el('summary', {}, 'Show a solution (try first!)'),
      el('pre', { class: 'out', style: 'margin-top:8px' }, q.ref),
      el('button', { class: 'btn sm', style: 'margin-top:6px', onclick: () => { ed.value = q.ref; onEdit(); } }, 'Load it in the editor and watch it run'));
    cs.append(d);
  } else cs.append(el('div', { class: 'mute small' }, 'This is your own question, so there is no stored solution. Work it out and check the flow and output yourself.'));
  cs.append(statusRow(q));
}
function statusRow(q) {
  return el('div', { class: 'row', style: 'margin-top:10px' },
    el('button', { class: 'btn sm', onclick: () => { if (store.solved[q.id]) { delete store.solved[q.id]; toast('Marked not solved'); } else markSolved(false); save(); } }, store.solved[q.id] ? '✓ Solved (tap to undo)' : 'Mark solved'),
    el('button', { class: 'btn sm', onclick: () => { store.review[q.id] ? delete store.review[q.id] : store.review[q.id] = 1; save(); toast(store.review[q.id] ? 'Added to review' : 'Removed from review'); } }, 'Review later'),
    q.custom ? el('button', { class: 'btn sm', onclick: () => deleteCustom(q.id) }, 'Delete question') : null);
}
function buildQA(q, ci, cc, cx) {
  ci.classList.add('hide'); cc.classList.remove('hide');
  cc.append(el('h3', {}, 'Answer it yourself first'));
  if (q.code) {
    cc.append(el('pre', { class: 'out' }, q.code));
    cc.append(el('button', { class: 'btn sm', style: 'margin-top:6px', onclick: () => { store.code.sandbox = q.code; openQuestion('sandbox'); } }, 'Run this in the Sandbox'));
  }
  const ta = el('textarea', { class: 'ans', placeholder: 'Write your answer in your own words, like in an interview…' });
  ta.value = store.code[q.id] || '';
  ta.addEventListener('input', () => { store.code[q.id] = ta.value; save(); });
  cc.append(ta);
  cx.classList.add('hide');
}
function buildSolutionQA(q, cs) {
  cs.classList.remove('hide');
  const box = el('div', {});
  cs.append(el('h3', {}, 'Model answer'));
  (q.hints || []).forEach(h => cs.append(el('div', { class: 'msg info' }, 'Hint: ' + h)));
  const btn = el('button', { class: 'btn pri', style: 'margin-top:8px', onclick: () => { btn.classList.add('hide'); box.append(el('div', { class: 'answer' }, q.answer)); box.append(el('div', { class: 'row', style: 'margin-top:8px' },
    el('button', { class: 'btn sm', onclick: () => { markSolved(false); } }, 'I knew it ✓'), el('button', { class: 'btn sm', onclick: () => { store.review[q.id] = 1; save(); toast('Added to review'); } }, 'Need more practice ↻'))); } }, 'Reveal answer');
  cs.append(btn, box);
}
function deleteCustom(id) {
  if (!confirm('Delete this question?')) return;
  store.custom = store.custom.filter(q => q.id !== id); save();
  QS = QS.filter(q => q.id !== id); byId.delete(id);
  buildFilters(); renderBrowse(); setView('browse');
}

// ------------------------------------------------------------ add questions (bulk import)
function modal(content) {
  const root = $('#modal-root'); root.innerHTML = '';
  const m = el('div', { class: 'modal', onclick: (e) => { if (e.target === m) root.innerHTML = ''; } }, el('div', { class: 'sheet' }, content));
  root.append(m);
  return () => { root.innerHTML = ''; };
}
function openAdd() {
  let drafts = [];
  const close = () => { $('#modal-root').innerHTML = ''; };
  const ta = el('textarea', { class: 'big', placeholder: 'Paste questions here (from a PDF, web page, notes).\n\n1. First question…\n2. Second question…\n\nOr drop a .txt / .md / .pdf / .json file below.' });
  const file = el('input', { type: 'file', accept: '.txt,.md,.pdf,.json,.csv,text/plain,application/pdf,application/json' });
  const f = {
    section: el('input', { type: 'text', value: 'My Questions' }), topic: el('input', { type: 'text', placeholder: 'e.g. Arrays & Hashing' }),
    pattern: el('input', { type: 'text', placeholder: 'e.g. Two pointers' }), set: el('input', { type: 'text', placeholder: 'e.g. NeetCode 150' }),
    diff: el('select', {}, ...['', 'Easy', 'Medium', 'Hard'].map(x => el('option', { value: x }, x || 'Difficulty: as detected / none'))),
  };
  const status = el('div', { class: 'small mute' });
  const pv = el('div', {});
  const drawPreview = () => {
    pv.innerHTML = '';
    drafts.forEach((d, i) => {
      const keep = el('input', { type: 'checkbox' }); keep.checked = d.keep; keep.onchange = () => { d.keep = keep.checked; countLbl(); };
      const title = el('input', { type: 'text', value: d.title }); title.oninput = () => d.title = title.value;
      const body = el('textarea', {}); body.value = d.q; body.oninput = () => d.q = body.value;
      const setup = el('input', { type: 'text', placeholder: 'Optional starting data, e.g. nums = [1, 2, 3]', value: d.setup || '' }); setup.oninput = () => d.setup = setup.value;
      pv.append(el('div', { class: 'pv' }, el('div', { class: 'row' }, keep, el('b', {}, '#' + (i + 1)), title), body, setup));
    });
    countLbl();
  };
  const countLbl = () => { status.textContent = drafts.length ? `${drafts.filter(d => d.keep).length} of ${drafts.length} questions will be added` + (drafts.report ? '. ' + drafts.report : '') : ''; };
  const split = () => {
    const t = ta.value.trim();
    if (!t) { status.textContent = 'Paste some text first.'; return; }
    if (t.startsWith('[') || t.startsWith('{')) { try { importJson(JSON.parse(t)); return; } catch (e) { /* plain text then */ } }
    const found = draftsFromText(t); const rep = found.report;
    drafts = found.map(d => ({ ...d, setup: guessSetup(d.q) })); drafts.report = rep;
    drawPreview();
  };
  const importJson = (data) => {
    const arr = Array.isArray(data) ? data : (data.questions || (data.id ? [data] : []));
    drafts = arr.filter(x => x && (x.title || x.q)).map(x => ({ keep: true, raw: x, title: x.title || 'Untitled', q: x.q || '', difficulty: x.difficulty || '', topic: x.topic || '', setup: x.setup || '' }));
    drawPreview();
  };
  file.onchange = async () => {
    const fl = file.files[0]; if (!fl) return;
    try {
      if (/\.pdf$/i.test(fl.name)) {
        status.textContent = 'Reading PDF…';
        const txt = await textFromPdf(fl, (p, n) => { status.textContent = `Reading PDF page ${p}/${n}…`; });
        if (txt.replace(/\s/g, '').length < 30) { status.textContent = 'No text found in this PDF. It is probably scanned images. Copy the text out with an OCR tool and paste it here.'; return; }
        ta.value = txt;
      } else ta.value = await fl.text();
      split();
    } catch (e) { status.textContent = 'Could not read that file: ' + e.message; }
  };
  const add = () => {
    const keep = drafts.filter(d => d.keep && (d.title.trim() || d.q.trim()));
    if (!keep.length) { status.textContent = 'Nothing selected.'; return; }
    let n = 0;
    for (const d of keep) {
      const base = d.raw ? { ...d.raw } : {};
      const id = 'my-' + Date.now().toString(36) + '-' + (n++);
      const q = Object.assign({ kind: 'free', sets: [], hints: [], ref: '', starter: '' }, base, {
        id, title: d.title.trim() || 'Untitled', q: d.q.trim(), setup: d.setup || base.setup || '',
        section: f.section.value.trim() || base.section || 'My Questions', topic: f.topic.value.trim() || d.topic || base.topic || 'Imported',
        pattern: f.pattern.value.trim() || base.pattern || '', difficulty: f.diff.value || d.difficulty || base.difficulty || '',
      });
      if (!d.raw || !base.kind) q.kind = q.kind === 'qa' || q.kind === 'function' ? q.kind : 'free';
      if (f.set.value.trim()) q.sets = uniq([...(q.sets || []), f.set.value.trim()]);
      store.custom.push(q);
    }
    save();
    QS = QS.concat(store.custom.slice(-keep.length).map(q => ({ ...q, custom: true }))); byId = new Map(QS.map(q => [q.id, q]));
    F.section = ''; F.topic = ''; F.pattern = ''; buildFilters(); renderBrowse(); close(); setView('browse');
    toast(keep.length + ' question' + (keep.length > 1 ? 's' : '') + ' added');
  };
  const field = (lbl, node) => el('div', {}, el('label', {}, lbl), node);
  modal([
    el('h2', {}, 'Add questions'),
    el('p', { class: 'mute small', style: 'margin:0 0 8px' }, 'Paste a whole list at once. The app splits it into separate questions (numbered "1." "Q2)" "Problem 3:", lines of ---, or blank-line gaps), and you check the result before adding. Works with text copied from a PDF, or upload the PDF itself.'),
    ta, el('div', { class: 'row', style: 'margin:8px 0' }, file, el('button', { class: 'btn pri', onclick: split }, 'Split into questions')),
    el('div', { class: 'fields' }, field('Section', f.section), field('Topic', f.topic), field('Pattern', f.pattern), field('Question set', f.set), field('Difficulty', f.diff)),
    status, pv,
    el('div', { class: 'row', style: 'margin-top:10px' }, el('button', { class: 'btn pri', onclick: add }, 'Add selected'), el('button', { class: 'btn', onclick: close }, 'Cancel')),
  ]);
}

// ------------------------------------------------------------ misc
function toast(msg) {
  const t = el('div', { class: 'toast' }, msg); document.body.append(t); setTimeout(() => t.remove(), 1800);
}
function exportData() {
  const blob = new Blob([JSON.stringify({ app: 'code-flow-python', exported: new Date().toISOString(), solved: store.solved, review: store.review, custom: store.custom }, null, 1)], { type: 'application/json' });
  const a = el('a', { href: URL.createObjectURL(blob), download: 'code-flow-python-backup.json' }); document.body.append(a); a.click(); a.remove();
}

function wire() {
  document.querySelectorAll('#tabs button').forEach(b => b.onclick = () => {
    const v = b.dataset.v;
    if (v === 'browse') { stopPlay(); setView('browse'); renderBrowse(); }
    else if (v === 'sandbox') openQuestion('sandbox');
    else if (cur && cur.id !== 'sandbox') setView('practice'); else if (store.last && byId.has(store.last)) openQuestion(store.last); else { setView('browse'); toast('Pick a question first'); }
  });
  document.querySelectorAll('#groupby button').forEach(b => b.onclick = () => {
    groupBy = b.dataset.g; document.querySelectorAll('#groupby button').forEach(x => x.classList.toggle('on', x === b)); renderBrowse();
  });
  const bind = (id, key) => $(id).addEventListener(key === 'search' ? 'input' : 'change', (e) => { F[key] = e.target.value; if (key === 'section' || key === 'topic') { if (key === 'section') F.topic = ''; F.pattern = ''; buildFilters(); } renderBrowse(); });
  bind('#f-search', 'search'); bind('#f-section', 'section'); bind('#f-topic', 'topic'); bind('#f-pattern', 'pattern'); bind('#f-set', 'set'); bind('#f-diff', 'diff'); bind('#f-status', 'status');
  $('#btn-add').onclick = openAdd;
  $('#btn-export').onclick = exportData;
}

(async function main() {
  wire();
  try { await loadQuestions(); } catch (e) { $('#groups').append(el('div', { class: 'msg bad' }, 'Could not load questions: ' + e.message)); return; }
  buildFilters(); renderBrowse();
  window.__cfp = { openQuestion, get state() { return { cur, steps, result, store }; } };
  if ('serviceWorker' in navigator && location.protocol.startsWith('http')) navigator.serviceWorker.register('sw.js').catch(() => {});
})();
