---
name: parser-pipeline-fuzz
description: Local fuzzing of HTML/sanitizer pipelines (DOMPurify + parse5 + JSXSS) at versions pinned from target bundle. Use when target uses a known sanitizer and you want bypass inputs. Hands off to browser-confirm for live verification.
---

# parser-pipeline-fuzz

## Purpose
DOMPurify bypasses are valuable but rare and version-dependent. Build a
local pipeline at the EXACT version pinned in the target bundle (read
from `package.json` or webpack chunk metadata), fuzz with the standard
mutation/grammar corpus, surface bypasses, and only escalate the single
survivor to live target. This is the cheap-stage filter before you
spend a Caido replay slot.

## Status
**Stub.** The skill scaffold is in place; the vendored sanitizer
pinning + fuzz corpus under `bin/parser_fuzz/` is left as a per-target
build. See "Implementation TODO" below.

## Inputs
- Target's `package.json` or extracted bundle `__webpack_modules__`
  pinning DOMPurify / parse5 / JSXSS versions.
- Local `node` + `npm` for installing the pinned sanitizer.

## Steps (when implemented)
1. Detect sanitizer + version from bundle:
   - DOMPurify: search `targets/<name>/raw/**/*.js` for
     `DOMPurify.version` or the `Symbol(DOMPurify.version)` constant.
   - parse5: search for `parse5.version` and `parse5.parserState`.
2. `npm i dompurify@<version>` into `bin/parser_fuzz/local_<version>/`.
3. Run the corpus from `bin/parser_fuzz/corpus/` through the pinned
   sanitizer. Collect inputs whose output, when re-parsed, contains
   any active script / event handler / `javascript:` URL.
4. Write survivors to `targets/<name>/fuzz/parser_pipeline.jsonl`.
5. For each survivor, generate a `browser-confirm` PoC URL and queue.

## Outputs
- `targets/<name>/fuzz/parser_pipeline.jsonl`
- `status.json.phases.parser_pipeline_fuzz`

## Implementation TODO
- `bin/parser_fuzz/runner.js` — Node CLI that takes
  `--sanitizer=dompurify --version=X.Y.Z --corpus=corpus.txt` and
  emits JSONL survivors.
- `bin/parser_fuzz/corpus/dompurify-bypasses.txt` — seed corpus
  (Hackvertor + GitHub-Issues archive of historical bypasses).
- `bin/parser_pipeline_fuzz.py` — Python wrapper that boots the
  Node runner per detected sanitizer.

## Failure modes
- Sanitizer version not detectable → fall back to "latest pinned in
  package.json" with a `confidence: low` note in the result.
- All survivors are duplicates of known historical bypasses → drop
  per public CVE; only flag novel bypasses.

## Result block
```json
"phases": { "parser_pipeline_fuzz": {
    "status": "stub|done", "ts": "<iso>",
    "sanitizer": "dompurify|parse5|jsxss",
    "version": "X.Y.Z",
    "survivors": N,
    "output_file": "fuzz/parser_pipeline.jsonl" } }
```
