// news-image-01 entry (Node 22, standard library only).
// The entry is a single pre-drawn image: this program copies ./entry.png
// (a 1024x1024 editorial front page summing up Friday 13 November 2026)
// to the output directory. No network, no model calls, no other reads.
// The image itself was drawn procedurally (see draw.py) with flat
// vector-style shapes and DejaVu Sans text, so every label is crisp
// and exactly as written - no garbled text. A plain copy is
// deterministic by construction: two runs write the same bytes.
//
// Run locally:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
