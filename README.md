# Code Flow Python

Learn Python by **watching your code run, line by line**. Write code on the left; on the right you see the loop walk through your data, variables change, the call stack grow, and the output appear. It updates while you type, even when the code is only half written.

- **Real Python 3** (CPython compiled to WebAssembly with [Pyodide](https://pyodide.org)). Not a lookalike: the whole standard library works.
- **Works offline** once installed. No server, no account, your code never leaves your device.
- **207 built-in questions** in four sections, browsable by **section, topic, pattern or question set**.
- **Bulk add**: paste a list copied from a PDF or web page (or upload the PDF) and it is split into separate questions.
- Installs as an **app** on phone and desktop (PWA), and can be built as an **Android APK**.

## What is inside

| Section | Questions | What |
|---|---|---|
| Python Basics | 33 | Variables, if/else, loops over lists, `range`/`while`, strings. Script style: you get data, you write the code, output is checked. |
| Core Python | 15 | Strings, dicts, recursion, comprehensions, generators, decorators, classes, exceptions. |
| Data Structures & Algorithms | 123 | Arrays and hashing, two pointers, sliding window, stack, binary search, linked list, trees, heap, backtracking, graphs, 1-D/2-D DP, greedy, intervals, math and bits, design. Every problem has several test cases, hints and a reference solution. |
| Interview Q&A | 36 | Basic to advanced Python interview questions with model answers (self-check mode). |

DSA problems are tagged with the lists they belong to in spirit (**NeetCode 150 style**, **Blind 75 style**, **Top Interview 150 style**) and with an algorithm **pattern** (e.g. "Hash map complement", "Monotonic stack"). All problem statements are original wording. The tags are a guide, not an official copy of those lists, and this is a starter set, not the complete 150 or 250. See "Adding more" below.

## How to use it on your phone (install)

1. Turn on GitHub Pages: repo **Settings > Pages > Source: GitHub Actions**. The workflow in `.github/workflows/pages.yml` publishes it.
2. Open `https://<your-username>.github.io/code-flow-python/` on the phone, in Chrome.
3. Menu (⋮) > **Install app** / **Add to Home screen**. The first open downloads about 17 MB (the Python engine) and then it works offline.

## Android APK (optional)

Repo **Actions > Build Android APK > Run workflow**. When it finishes, download `code-flow-python-debug-apk` from the run page, copy it to the phone and install it (allow "install unknown apps"). It wraps the same app with Capacitor. This route is **untested on a real device**; if the Python engine does not start inside the Android WebView, use the PWA install above, which is tested.

## Adding more questions

**In the app:** tap **+ Add**, paste text (or choose a `.txt`, `.md`, `.pdf` or `.json` file), tap **Split into questions**, fix titles, tick what to keep, set section/topic/pattern/set, **Add selected**. Notes:

- Splitting understands `1.`, `Q2)`, `Problem 3:`, lines of `---`, and blank-line gaps.
- PDFs must contain real text. Scanned-image PDFs need OCR first.
- Questions you add have no tests or solution, so you work them out and check the flow and output yourself. They are stored on your device (use **Export my data** to back up).
- To add questions that have tests, paste JSON in the schema below.

**In the repo:** write a Python file in `tools/src/` using `add(...)` (see `tools/qlib.py` and any file there), then run `python3 tools/build.py`. The build **runs every reference solution against its tests with real Python** and fails if anything disagrees, then `python3 tools/make_sw.py` refreshes the offline cache list.

### Question JSON

```json
{
  "id": "my-1", "kind": "function", "title": "Two sum",
  "section": "My Questions", "topic": "Arrays & Hashing", "pattern": "Hash map",
  "difficulty": "Easy", "sets": ["My list"],
  "q": "Return indices of the two numbers that add up to target.",
  "fn": "two_sum", "starter": "def two_sum(nums, target):\n    pass",
  "tests": [{"args": [[2, 7, 11, 15], 9], "expect": [0, 1]}],
  "compare": "exact", "ref": "def two_sum(nums, target): ..."
}
```

`kind`: `function` (tests), `script` (data in `setup`, output compared with `ref`), `free` (no checking), `qa` (interview answer). `compare`: `exact`, `unordered`, `nested_unordered`, `float`. For linked lists and trees add `"prelude": "ds", "conv": ["ll"], "conv_ret": "ll"` (`"tree"` for trees): test lists become `ListNode` / `TreeNode` objects for you.

## Develop

```
npm install            # only needed to refresh vendored files
python3 tools/build.py # validate all questions with real Python, write app/data
python3 tools/make_sw.py
python3 -m http.server 8000 -d app   # open http://localhost:8000
python3 tests/e2e.py   # browser test with Playwright (real Python in Chromium)
```

How the tracer works: `app/js/trace.py` runs your code inside Pyodide with `sys.settrace`, records the variables after each line, and wraps `for` loops so the app knows which item the loop is on. Runaway code is stopped after 8 seconds or 600,000 events and reported as "Does a loop never end?". Partly written code that does not parse still runs up to the last good line.

## Licence

MIT for this project's code. Pyodide (MPL-2.0) and pdf.js (Apache-2.0) are bundled unmodified in `app/vendor/`.
