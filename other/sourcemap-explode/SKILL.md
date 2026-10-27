---
name: sourcemap-explode
description: Decode every .js.map under targets/<name>/raw/ and write the original source tree under targets/<name>/sources/. Run after js-harvest when raw/ contains .js.map files and sources/ is missing. Preserves the sourcesContent[i] root layout so js_analyzer's path-relative tagging works.
---

# sourcemap-explode

## Purpose
Restore the original (pre-minified, pre-bundled) source tree from
sourcemaps so the static analyzer reads humanly meaningful code instead
of minified blobs.

## Inputs
- `targets/<name>/raw/**.js.map` files (output of `js-harvest`).

## Steps
1. For each `*.js.map`, parse JSON. Extract `sources[]` and
   `sourcesContent[]`. If `sourcesContent` is absent, log and skip —
   we cannot recover content from URLs alone (and we don't fetch them
   because they may be off-scope CDNs).
2. For each `(src_path, src_content)` pair:
   - Normalize `src_path` (strip `webpack:///`, `webpack-internal:///`,
     query strings, leading `./`).
   - Write `targets/<name>/sources/<normalized_path>`. Create dirs as
     needed. Skip if the destination already exists with identical
     content (idempotent).
3. For every `.js` in `raw/` that has no `.js.map` sibling AND was
   not referenced as a chunk of a mapped bundle, copy it to
   `targets/<name>/sources/_nomap/<host>/<path>.js`. These get
   analyzed too — just at lower confidence.
4. Write `targets/<name>/sources/_manifest.json` describing each
   mapping origin (which `.js.map` produced which source files).

## Outputs
- `targets/<name>/sources/**` (original tree)
- `targets/<name>/sources/_nomap/**` (chunks without maps)
- `targets/<name>/sources/_manifest.json`

## Failure modes
- Malformed sourcemap JSON → skip that file; log to
  `status.json.explode.malformed_maps[]`.
- Path collision (two maps want to write the same `sources/foo.js`
  with different content) → keep the longer one; log conflict.
- `sourcesContent` missing → log; the file remains analyzable as a
  `_nomap` chunk.

## Result block
```json
"phases": { "explode": { "status": "done", "ts": "<iso>",
  "original_files": N, "nomap_files": M, "conflicts": K } }
```
