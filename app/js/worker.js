// Runs real CPython (Pyodide) off the main thread.
import { loadPyodide } from '../vendor/pyodide/pyodide.mjs';

let py = null, traceRun = null, runTests = null;

async function init() {
  const base = new URL('../vendor/pyodide/', import.meta.url).href;
  py = await loadPyodide({ indexURL: base });
  const src = await (await fetch(new URL('./trace.py', import.meta.url))).text();
  py.runPython(src);
  traceRun = py.globals.get('trace_run');
  runTests = py.globals.get('run_tests');
  py.runPython('import sys; sys.version');
  return py.runPython('sys.version.split()[0]');
}

const ready = init().then(v => { postMessage({ type: 'ready', version: v }); }).catch(e => {
  postMessage({ type: 'fatal', error: String(e && e.message || e) });
});

onmessage = async (ev) => {
  const { id, type, payload } = ev.data;
  try {
    await ready;
    if (!py) throw new Error('Python failed to start');
    let out;
    if (type === 'trace') out = traceRun(JSON.stringify(payload));
    else if (type === 'tests') out = runTests(JSON.stringify(payload));
    else throw new Error('unknown message ' + type);
    postMessage({ id, ok: true, result: JSON.parse(out) });
  } catch (e) {
    postMessage({ id, ok: false, error: String(e && e.message || e) });
  }
};
