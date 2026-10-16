// Copies the Python runtime (Pyodide) and the PDF reader (pdf.js) into app/vendor from node_modules.
import fs from 'node:fs';
const cp = (from, to) => { fs.mkdirSync(to.replace(/\/[^/]+$/, ''), { recursive: true }); fs.copyFileSync(from, to); console.log('copied', to); };
for (const f of ['pyodide.mjs', 'pyodide.asm.mjs', 'pyodide.asm.wasm', 'python_stdlib.zip', 'pyodide-lock.json']) cp('node_modules/pyodide/' + f, 'app/vendor/pyodide/' + f);
for (const f of ['pdf.min.mjs', 'pdf.worker.min.mjs']) cp('node_modules/pdfjs-dist/build/' + f, 'app/vendor/pdfjs/' + f);
