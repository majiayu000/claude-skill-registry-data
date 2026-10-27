---
name: cspt-csrf
description: Surface CSPT-to-CSRF candidates — path traversal landing in fetch/XHR/axios URLs. Scans dom_reachable.jsonl for cspt_* sinks, ranks by verb severity, writes cspt_csrf.jsonl. Run after dom-xss-hunt, before browser-confirm.
---

# cspt-csrf

## Purpose
Doyensec's CSPT2CSRF research showed that chains where attacker
controls a path segment of a fetch/XHR URL can be escalated to CSRF on
cookie-authenticated mutation endpoints. This skill is the static-pass
candidate generator. Live confirmation is `browser-confirm`.

## Inputs
- `targets/<name>/chains/dom_reachable.jsonl` (preferred) or
  `chains/hot.jsonl`.
- `targets/<name>/db/js_analyzer.db` (per-target snapshot — used to
  cross-check `cspt_path_traversal_marker` tags from the
  `extra_cspt.json` taxonomy).

## Steps
1. Ensure `dom-xss-hunt` has produced `chains/dom_reachable.jsonl`,
   or fall back to `chains/hot.jsonl`.
2. Run:
   ```
   python3 bin/cspt_csrf_scan.py targets/<name>
   ```
3. Inspect `chains/cspt_csrf.jsonl`. Each line:
   ```json
   {
     "chain_id": "...",
     "kind": "cspt_csrf_candidate",
     "severity": "critical|high|medium|low",
     "sink": { "qname", "file", "line", "taxonomy_id" },
     "source": { ... },
     "path": [...],
     "mutating_verb_hint": bool,
     "has_path_traversal_marker": bool
   }
   ```
4. For each candidate (start with `critical`), feed into
   `browser-confirm` live mode with a CSPT-style PoC: a same-origin
   request whose URL contains a path-traversal segment that pivots to
   a different endpoint. Verify the cookie is sent automatically (no
   Authorization header that would otherwise gate CSRF).
5. Confirmed CSPT-CSRF chains write to
   `targets/<name>/findings/<chain_id>/confirmed.json` with
   `kind: cspt_csrf` plus the redirected endpoint.

## Outputs
- `targets/<name>/chains/cspt_csrf.jsonl`
- `status.json.phases.cspt_csrf`

## Failure modes
- `chains_scanned == 0` → run `chain-triage` and `dom-xss-hunt` first.
- `matched_cspt_sink == 0` → indexer didn't tag any chain sink with a
  CSPT-family taxonomy. Verify `extra_cspt.json` is loaded
  (`taxonomy.load_default()` auto-loads `extra_*.json`); re-run
  `js-index`.
- `with_path_traversal_marker == 0` → CSPT family hits exist but no
  path-traversal markers were tagged on intermediate nodes. Lower-
  confidence candidates still emit; mark accordingly during
  `browser-confirm`.

## Result block
```json
"phases": { "cspt_csrf": {
    "status": "done", "ts": "<iso>",
    "input": "chains/...jsonl",
    "chains_scanned": N,
    "matched_cspt_sink": N,
    "with_path_traversal_marker": N,
    "candidates_written": N,
    "output_file": "chains/cspt_csrf.jsonl" } }
```
