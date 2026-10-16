// Turns pasted text (from a PDF, a web page, notes) into draft questions.
const LEAD = /^\s*(?:(?:Q(?:uestion)?|Problem|Ex(?:ercise)?)\.?\s*)?(\d{1,4})\s*[\.\):\-]\s+(?=\S)/i;

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
  const idx = [];
  lines.forEach((l, i) => { if (LEAD.test(l)) idx.push(i); });
  if (idx.length >= 2 && looksSequential(lines, idx)) return cut(lines, idx);
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

function looksSequential(lines, idx) {
  const nums = idx.map(i => +LEAD.exec(lines[i])[1]);
  let up = 0;
  for (let k = 1; k < nums.length; k++) if (nums[k] >= nums[k - 1]) up++;
  return up >= (nums.length - 1) * 0.7;
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
  body = body.replace(LEAD, '');
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
  return splitQuestions(raw).map(toDraft);
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
