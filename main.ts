// News image for Wednesday 25 November 2026 (make.fun news-image-20261125).
//
// The image is bundled in this repository as entry.jpg: a 1024x1024 JPEG
// that sums up the day — China investigating Shanghai party chief
// Chen Jining, Shenzhou-24 lifting off with the first Pakistani national
// on board, a US jury convicting Huawei, and gunmen taking 25 hostages
// at a Cartagena supermarket — plus a footer strip with four more
// stories from the day.
//
// This program copies the bundled image byte-for-byte to
// <output>/entry.png (the name stays entry.png even though the bytes are
// JPEG, as the bounty rules allow). It uses only the Node standard
// library and makes no network calls, so repeated runs produce
// identical output. Before writing, it checks the bundled file's JPEG
// magic bytes, the 1 MiB size cap and its expected SHA-256, so a
// corrupted bundle fails loudly instead of shipping a bad entry; after
// writing, it reads the output back and compares bytes.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
// /output:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';

const MAX_BYTES = 1_048_576;
const JPEG_MAGIC = [0xff, 0xd8, 0xff];
const EXPECTED_SHA256 =
  'b08b2b6f04505120536ad648dc702e9fc784d529c0940b1d7c2885b0c032a4ff';

const here = dirname(fileURLToPath(import.meta.url));
const data = readFileSync(join(here, 'entry.jpg'));

if (data.length < 3 || JPEG_MAGIC.some((b, i) => data[i] !== b)) {
  throw new Error('entry.jpg is not a JPEG (bad magic bytes)');
}
if (data.length > MAX_BYTES) {
  throw new Error(`entry.jpg is ${data.length} bytes, over the 1 MiB cap`);
}
const digest = createHash('sha256').update(data).digest('hex');
if (digest !== EXPECTED_SHA256) {
  throw new Error(`entry.jpg sha256 mismatch: ${digest}`);
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const dest = join(outDir, 'entry.png');
writeFileSync(dest, data);
if (!readFileSync(dest).equals(data)) {
  throw new Error('output differs from the bundled image');
}
console.log(`wrote ${dest} (${data.length} bytes, sha256 ${digest})`);
