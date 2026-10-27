---
name: sanitizer-on-path
description: Per-chain sanitizer check — walk path qnames, match sanitizer categories against sink/source. Splits chains/all.jsonl into sanitized.jsonl + clean.jsonl. Use --coarse for lenient mode. Run after extract_chains_bounded.
---

# sanitizer-on-path

## Purpose

Reduce audit FP rate by dropping chains whose path already passes a
sanitizer that clears the relevant taxonomy category. coralbug3 audited
4 chains, all 4 confirmed FP — sanitizers in the path were not visible
to the chain extractor. This skill makes them visible at chain-triage
time so the adversarial / opus audit budget isn't wasted on
pre-defused chains.

## When to run

After `bin/extract_chains_bounded.py` has produced `chains/all.jsonl`,
BEFORE `chain-triage` writes `hot.jsonl` and BEFORE
`cc-taint-adversarial` runs. Re-running is idempotent — `*.jsonl`
files are atomically rewritten.

Skip if:
- `status.json.phases.sanitizer_on_path.status == "done"` and
  `chains/all.jsonl` hasn't been re-extracted since.

## Inputs

- `targets/<name>/db/js_analyzer.db` (per-target snapshot).
- `targets/<name>/chains/all.jsonl` (from extract_chains_bounded).

## Steps

1. **Run the scanner (strict-dominance by default).**
   ```bash
   python3 bin/sanitizer_on_path.py <target_name>
   ```
   Default behaviour: per chain, for each qname on `chain.path`,
   pull `node_sanitizers` rows. A chain is sanitized when any
   sanitizer's `clears` category intersects with the chain's
   sink/source category mapping (`html`, `attribute`, `url`, `js`),
   or `clears` is `any`, AND the sanitizer's line < the next
   call-out line on the same function (cheap CFG-dominance proxy).

2. **(Opt-out) coarse mode.**
   ```bash
   python3 bin/sanitizer_on_path.py <target_name> --coarse
   ```
   Treat any sanitizer anywhere in the function as clearing the
   chain. Higher FP-reduction rate but higher risk of false-clearing
   when `clears=any` sanitizers like `Number_coerce` appear on side
   values not in the taint flow. Use only when strict mode misses
   known defensive patterns.

## Outputs

```
targets/<name>/chains/
├── all.jsonl              # rewritten in place with sanitized + sanitizer_evidence
├── sanitized.jsonl        # chains the scanner believes are defused
├── clean.jsonl            # chains with no matching sanitizer (the audit queue)
└── triage_sanitizer.json  # sanitizer hit distribution + counts
```

`chain.sanitizer_evidence` shape:
```json
{
  "sanitizer_id": "sanitizer_dompurify",
  "qname": "app.js::renderUserBio",
  "line": 42,
  "clears": ["html", "attribute"],
  "matched_categories": ["html"],
  "path_index": 1,
  "strict_dominance": true
}
```

`status.json.phases.sanitizer_on_path`:
```json
{
  "status": "done",
  "ts": "...",
  "total_chains": 2000,
  "sanitized": 488,
  "clean": 1512,
  "sanitized_pct": 24.4,
  "strict_dominance": false,
  "elapsed_s": 0.1
}
```

## Failure modes / FP-of-sanitization

`sanitizer_Number_coerce` and `sanitizer_parseInt_parseFloat` carry
`clears=any`, which is **conservative-by-design**: a `Number()` call
ANYWHERE in the path's functions will mark the chain as sanitized.
That can over-defuse — the `Number(...)` may operate on a side value
that isn't part of the taint flow. If you suspect over-defusing on a
target:
- Re-run with `--strict-dominance` for tighter line-order matching.
- Inspect `triage_sanitizer.sanitizer_dist`. If `Number_coerce` and
  `parseInt_parseFloat` dominate the sanitized set, the over-defuse
  pattern is likely active; spot-check a sample of `sanitized.jsonl`
  before discarding them from audit.

The opposite (under-defusing): coarse-grained categories miss
sanitizers that work via custom escape functions not in
`taxonomies/sanitizers.json`. Add them to the taxonomy if you find
a recurring custom pattern.

## Plan reference

Phase 2 of `project_implicit_tags_plan.md`. Stands alone; can run
without implicit-tags. Implicit-tag chains carry confidence < 1.0;
if such a chain is ALSO sanitized, treat the combined low-confidence
+ sanitized signal as strong-drop.

## Calibration

**coolblue-intigriti (2000 chains, legacy DB rows with `clears=any`):**

| Mode | Sanitized | Clean | Elapsed |
|---|---:|---:|---:|
| coarse (legacy default) | 488 (24.4%) | 1512 | 0.10s |
| strict-dominance | 25 (1.2%) | 1975 | 0.37s |

**netlify-h1 (2000 chains, strict + canonical-clears override, 2026-05-19):**

| Mode | Sanitized | Clean | Elapsed |
|---|---:|---:|---:|
| strict-dominance (current default) | 8 (0.4%) | 1992 | 0.15s |

The 2026-05-19 change loads the canonical `clears` set per sanitizer
id from `tlx/.../taxonomies/sanitizers.json` and overrides stale DB
rows. Concretely: `sanitizer_Number_coerce` and
`sanitizer_parseInt_parseFloat` carried `clears=any` in older
snapshots but the JSON narrowed them to `clears=numeric` (which no
sink category in the mapping matches). On netlify, 17559 stale rows
were overridden at scan time; sanitized dropped from 90.1% (over-
defused) to 0.4% (defensible).

Spot-check `sanitized.jsonl` before fully discarding from audit; the
remaining matches should be `encodeURIComponent` on url sinks +
`textContent_assign` / `dompurify_namespaced` / `createTextNode` on
html sinks.
