// Turns pasted text (from a PDF, a web page, notes) into draft questions.
// "1. text", "1.text" (PDFs often drop the space), "Q2)", "Problem 3:". The text after the number must start
// with a letter, quote or bracket, so "3.14" or "1,000" are not mistaken for question numbers.
const LEAD = /^\s*(?:(?:Q(?:uestion)?|Problem|Ex(?:ercise)?)\.?\s*)?(\d{1,4})\s*[\.\):\-]\s*(?=[A-Za-z\u0900-\u097F"'\u2018\u201C(\[<#])/i;

export function cleanText(t) {
  return String(t || '')
    .replace(/\r\n?/g, '\n').replace(/ /g, ' ').replace(/[​﻿]/g, '')
    .replace(/[ \t]+\n/g, '\n').replace(/\n{4,}/g, '\n\n\n')
    // join words hyphenated across a PDF line break
    .replace(/(\w)-\n(\w)/g, '$1$2');
}

// Split into chunks, one per question. Strategy picks the first marker that gives 2+ chunks.
export function splitQuestions(raw) {
  const text = cleanText(raw).trim();
  if (!text) return [];
  const lines = text.split('\n');
  // 1) numbered markers: "1.", "Q2)", "Problem 3:"
  const idx = numberedMarkers(lines);
  if (idx.length >= 2) return cut(lines, idx);
  // 2) separator lines: ---, ===, ***
  const sep = lines.map((l, i) => (/^\s*([-=*_~]){3,}\s*$/.test(l) ? i : -1)).filter(i => i >= 0);
  if (sep.length) {
    const parts = []; let from = 0;
    sep.concat([lines.length]).forEach(i => { parts.push(lines.slice(from, i).join('\n')); from = i + 1; });
    const ok = parts.map(s => s.trim()).filter(Boolean);
    if (ok.length >= 2) return ok;
  }
  // 3) "Problem:" / "Question:" headings
  const hd = [];
  lines.forEach((l, i) => { if (/^\s*(Problem|Question|Exercise|Task)\b[^\n]{0,60}:?\s*$/i.test(l) || /^#{1,4}\s+\S/.test(l)) hd.push(i); });
  if (hd.length >= 2) return cut(lines, hd);
  // 4) blank-line separated paragraphs, each at least a sentence
  const paras = text.split(/\n\s*\n/).map(s => s.trim()).filter(Boolean);
  if (paras.length >= 2) return mergeShort(paras);
  return [text];
}

// Keep only the markers that form a running 1, 2, 3 ... chain. A line like "4.exit" inside question 21's
// menu, or "10th year - 10000" in a worked example, is rejected because its number does not continue the chain.
function numberedMarkers(lines) {
  const cand = [];
  lines.forEach((l, i) => {
    let m = LEAD.exec(l);
    if (!m) {
      // number alone on its line ("20."), with the text on the next non-empty line
      const a = /^\s*(\d{1,4})\s*[\.\)]\s*$/.exec(l);
      if (a) { let j = i + 1; while (j < lines.length && !lines[j].trim()) j++; if (j < lines.length && /^[A-Za-z"'(]/.test(lines[j].trim())) m = a; }
    }
    if (m) cand.push({ i, n: +m[1] });
  });
  if (cand.length < 2) return [];
  // try each early candidate as the chain start and keep the longest chain
  let best = [];
  for (let s = 0; s < Math.min(cand.length, 6); s++) {
    const chain = [cand[s]];
    let last = cand[s].n;
    for (let k = s + 1; k < cand.length; k++) {
      const n = cand[k].n;
      if (n > last && n <= last + 4) { chain.push(cand[k]); last = n; }
    }
    if (chain.length > best.length) best = chain;
  }
  return best.length >= 2 ? best.map(c => c.i) : [];
}

// Tells the user if the numbering has gaps, e.g. "numbers 22, 23 were not found".
export function numberingReport(chunks) {
  const nums = chunks.map(c => { const m = LEAD.exec(c.split('\n')[0]) || /^\s*(\d{1,4})\s*[\.\)]\s*$/.exec(c.split('\n')[0]); return m ? +m[1] : null; }).filter(n => n != null);
  if (nums.length < 2) return '';
  const have = new Set(nums), missing = [];
  for (let n = Math.min(...nums); n <= Math.max(...nums); n++) if (!have.has(n)) missing.push(n);
  return missing.length ? `Question numbers ${Math.min(...nums)} to ${Math.max(...nums)} found. Missing numbers: ${missing.slice(0, 30).join(', ')}${missing.length > 30 ? '…' : ''}. Check the source for those.` : `Numbers ${Math.min(...nums)} to ${Math.max(...nums)} are all present.`;
}

function cut(lines, idx) {
  const out = [];
  for (let k = 0; k < idx.length; k++) {
    const part = lines.slice(idx[k], k + 1 < idx.length ? idx[k + 1] : lines.length).join('\n').trim();
    if (part) out.push(part);
  }
  return out;
}

// Paragraph mode: lines that are only an example/code line stick to the paragraph before.
function mergeShort(paras) {
  const out = [];
  for (const p of paras) {
    const isFollow = /^(example|input|output|explanation|constraints?|note|hint)\b/i.test(p) || p.length < 25 && out.length;
    if (isFollow && out.length) out[out.length - 1] += '\n\n' + p; else out.push(p);
  }
  return out;
}

const DIFF_RE = /\b(?:difficulty|level)\s*[:\-]\s*(easy|medium|hard|basic|intermediate|advanced)\b/i;
const TOPIC_RE = /\b(?:topics?|tags?|pattern|category)\s*[:\-]\s*([^\n]{2,80})/i;

export function toDraft(chunk, i) {
  let body = chunk.trim();
  body = body.replace(/^\s*\d{1,4}\s*[\.\)]\s*\n+/, '').replace(LEAD, '');
  let lines = body.split('\n');
  let title = lines[0].replace(/^[#\s]+/, '').replace(/^(?:problem|question)\s*:?\s*/i, '').trim();
  let rest = lines.slice(1).join('\n').trim();
  // a long first line is the whole question; make a short title from it
  if (title.length > 70 || !rest) {
    const m = /^(.{15,70}?)(?:[.?!:]\s|$)/.exec(title);
    const short = m ? m[1] : title.slice(0, 60);
    rest = (title.length > short.length ? body : rest).trim();
    title = short.replace(/[.:]$/, '');
  }
  const d = DIFF_RE.exec(body);
  const t = TOPIC_RE.exec(body);
  const diff = d ? d[1][0].toUpperCase() + d[1].slice(1).toLowerCase() : '';
  const norm = { Basic: 'Easy', Intermediate: 'Medium', Advanced: 'Hard' };
  return {
    keep: true,
    title: title || ('Question ' + (i + 1)),
    q: rest || body,
    difficulty: norm[diff] || diff || '',
    topic: t ? t[1].trim() : '',
    setup: '',
  };
}

export function draftsFromText(raw) {
  const chunks = splitQuestions(raw);
  const d = chunks.map(toDraft);
  d.report = numberingReport(chunks);
  return d;
}

// Optional: pull a "Python value" out of an "Input: nums = [1,2,3]" style line so the Input box is pre-filled.
export function guessSetup(q) {
  const m = /^\s*Input\s*:\s*(.+)$/im.exec(q);
  if (!m) return '';
  const line = m[1].trim();
  if (/^[A-Za-z_]\w*\s*=/.test(line)) return line.replace(/,\s*(?=[A-Za-z_]\w*\s*=)/g, '\n');
  return '';
}

export async function textFromPdf(file, onProgress) {
  const pdfjs = await import('../vendor/pdfjs/pdf.min.mjs');
  pdfjs.GlobalWorkerOptions.workerSrc = new URL('../vendor/pdfjs/pdf.worker.min.mjs', import.meta.url).href;
  const data = new Uint8Array(await file.arrayBuffer());
  const pdf = await pdfjs.getDocument({ data }).promise;
  let out = '';
  for (let p = 1; p <= pdf.numPages; p++) {
    const page = await pdf.getPage(p);
    const content = await page.getTextContent();
    let lastY = null, line = '';
    for (const it of content.items) {
      const y = it.transform ? Math.round(it.transform[5]) : 0;
      if (lastY !== null && Math.abs(y - lastY) > 3) { out += line.trimEnd() + '\n'; line = ''; }
      line += it.str + (it.hasEOL ? '\n' : '');
      lastY = y;
    }
    out += line.trimEnd() + '\n\n';
    if (onProgress) onProgress(p, pdf.numPages);
  }
  return out;
}
