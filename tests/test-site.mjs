import { readFileSync } from 'node:fs';
import assert from 'node:assert/strict';

const html = readFileSync(new URL('../index.html', import.meta.url), 'utf8');
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/gi)];
assert.equal(scripts.length, 1, 'Expected exactly one inline application script');
new Function(scripts[0][1]);
const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map(m => m[1]);
assert.equal(ids.length, new Set(ids).size, 'HTML contains duplicate IDs');
for (const id of ['view-home','view-chat','view-knowledge','view-models','view-security','messages','prompt','fileInput','provider','apiKey']) {
  assert.ok(ids.includes(id), `Missing required UI element: ${id}`);
}
for (const feature of ['askModel','retrieve','uploadFiles','attachFolder','learnUrl','exportData']) {
  assert.ok(scripts[0][1].includes(`function ${feature}`) || scripts[0][1].includes(`async function ${feature}`), `Missing feature function: ${feature}`);
}
assert.ok(!/AIza[0-9A-Za-z_-]{30,}/.test(html), 'A Google API key must never be committed to frontend source');
console.log('KHUDA AI checks passed: inline JavaScript parses, required views and controls exist, IDs are unique, and no Google API key is hard-coded.');
