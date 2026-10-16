// Talks to the Pyodide worker. Restarts it if code runs too long.
export function createRunner(onStatus) {
  let worker = null, ready = null, seq = 0, pending = new Map(), version = '';

  function start() {
    onStatus('loading');
    worker = new Worker(new URL('./worker.js', import.meta.url), { type: 'module' });
    ready = new Promise((res, rej) => {
      worker.onmessage = (ev) => {
        const m = ev.data;
        if (m.type === 'ready') { version = m.version; onStatus('ready', version); res(); return; }
        if (m.type === 'fatal') { onStatus('error', m.error); rej(new Error(m.error)); return; }
        const p = pending.get(m.id);
        if (!p) return;
        pending.delete(m.id);
        clearTimeout(p.timer);
        m.ok ? p.res(m.result) : p.rej(new Error(m.error));
      };
      worker.onerror = (e) => { onStatus('error', e.message || 'worker failed'); rej(new Error(e.message || 'worker failed')); };
    });
    ready.catch(() => {});
  }

  function restart(reason) {
    try { worker.terminate(); } catch (e) {}
    for (const [, p] of pending) { clearTimeout(p.timer); p.rej(new Error(reason)); }
    pending.clear();
    start();
  }

  async function call(type, payload, timeoutMs) {
    if (!worker) start();
    await ready;
    const id = ++seq;
    return new Promise((res, rej) => {
      const timer = setTimeout(() => {
        if (pending.has(id)) restart('Your code took too long and was stopped.');
      }, timeoutMs || 20000);
      pending.set(id, { res, rej, timer });
      worker.postMessage({ id, type, payload });
    });
  }

  start();
  return {
    trace: (p) => call('trace', p, 20000),
    tests: (p) => call('tests', p, 20000),
    cancelAll: () => restart('cancelled'),
    get version() { return version; },
  };
}
