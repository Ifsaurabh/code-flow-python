// Run: node tests/importer.test.mjs
import { draftsFromText } from '../app/js/importer.js';
let bad = 0;
const eq = (name, got, want) => { const ok = JSON.stringify(got) === JSON.stringify(want); console.log((ok ? 'PASS ' : 'FAIL ') + name, ok ? '' : JSON.stringify(got)); if (!ok) bad++; };

// PDF text often drops the space after the number, puts menu items "4.exit" on their own line, or leaves "20." alone.
const pdfLike = `Python Practice Problems
1.User will input 3 ages. Find the oldest one
2. Write a program to convert celsius to fahrenheit
21. Write a menu driven program - 1.cm to ft 2.kl to miles 3.usd to inr
4.exit

22.Write a program that counts dogs and chickens
20.

Write a program for salary after deductions
23. Print the sum of first n numbers. Eg if n=10 the output should be
55.
24.Print the value of 3.14 times a radius`;
const d = draftsFromText(pdfLike);
eq('chain ignores out-of-order numbers', d.length >= 5, true);
eq('"4.exit" is not a new question', d.some(x => x.title === 'exit'), false);
eq('no-space "22.Write" is detected', d.some(x => x.title.startsWith('Write a program that counts dogs')), true);

const full = Array.from({ length: 100 }, (_, i) => `${i + 1}.Write program number ${i + 1} that does something useful`).join('\n');
const f = draftsFromText(full);
eq('100 numbered lines without spaces -> 100 drafts', f.length, 100);
eq('report says all present', f.report.includes('all present'), true);
const gap = draftsFromText(full.split('\n').filter((_, i) => i !== 4 && i !== 9).join('\n'));
eq('gap report names missing numbers', gap.report.includes('5, 10'), true);
eq('decimals are not question numbers', draftsFromText('1. a thing\n2. another thing\n3.14 is pi so use it\n3. last thing').length, 3);
process.exit(bad ? 1 : 0);
