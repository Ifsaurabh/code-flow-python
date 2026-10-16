import subprocess, sys, time, os
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8124', '-d', os.path.join(ROOT, 'app')], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
ok = False
try:
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--no-sandbox'])
        ctx = b.new_context(viewport={'width': 390, 'height': 800})
        page = ctx.new_page()
        page.goto('http://localhost:8124/index.html'); page.wait_for_selector('.group')
        page.wait_for_function("navigator.serviceWorker.controller !== null || true")
        page.evaluate("navigator.serviceWorker.ready.then(()=>1)")
        page.wait_for_timeout(8000)
        keys = page.evaluate("caches.keys().then(k=>Promise.all(k.map(n=>caches.open(n).then(c=>c.keys().then(r=>r.length)))))")
        print('cache entries', keys)
        page.screenshot(path=os.path.join(ROOT, 'tests', 'mobile-home.png'))
        srv.terminate(); time.sleep(1)   # server gone = offline
        page.reload(); page.wait_for_selector('.group', timeout=15000)
        page.evaluate("window.__cfp.openQuestion('l-sum')"); page.wait_for_selector('#c-code textarea')
        page.fill('#c-code textarea', 'print(sum(numbers))')
        page.wait_for_function("document.querySelector('#out').textContent.trim()=='17'", timeout=60000)
        ok = True
        b.close()
finally:
    srv.terminate()
print('OFFLINE OK' if ok else 'OFFLINE FAILED')
sys.exit(0 if ok else 1)
