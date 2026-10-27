---
name: chain-bestfirst
description: Confidence-driven best-first chain extractor. Heap-ordered BFS keyed by partial P(chain) with sanitizer and viability discounts. Opt-in alongside extract_chains_bounded. Run after async-edges, browser-context-infer, implicit-tags.
---

# chain-bestfirst

## Purpose

`extract_chains_bounded.py` walks the call graph breadth-first up to a
fixed `--max-paths`. With large bundles (>500k edges) and abundant
implicit-source tags, the budget is exhausted before the most likely
chains surface. This skill replaces the BFS with a **best-first
heap**: at every step the frontier with the highest partial P(chain)
expands first, frontiers below `--p-cutoff` are dropped.

Plan: `plans/ARCHITECTURE_EVOLUTION.md §8`.

## P(chain) model

```
P(chain) = P_source                                     # taxonomy + tag confidence
         × Π P_edge(resolved_kind, candidate_count)     # per-hop confidence
         × Π (1 − P_block(sanitizer_confidence))        # per-sanitizer
         × P_viability(sink_id, browser_context)        # §4
         × 0.95^continuation_hops                       # §3 async discount
         × 0.90^dynamic_hops                            # §2 dynamic discount
```

Edge confidences:

| resolved_kind | base |
|---|---|
| `exact` | 1.00 |
| `this_cross_file` | 0.95 |
| `runtime_observed` | 1.00 |
| `continuation` (async) | 0.85 |
| `name_match` | 0.80 / √candidate_count |
| `prop_shape` (future §2) | 0.70 |
| `dynamic` | 0.30 |
| `unresolved` | 0.10 |

## When to run

After `js-index`, `db-isolate`, `implicit-tags`, `async-edges`, and
`browser-context-infer`. Best-first depends on those inputs to compute
a non-trivial P(chain).

Skip if the target has fewer than a few hundred chains in
`extract_chains_bounded` output — the bounded BFS is plenty fast there.

## Steps

```bash
# Prereqs (each idempotent; rerun on demand)
python3 bin/build_async_edges.py <target>
python3 bin/infer_browser_context.py <target>

# Best-first extraction
python3 bin/extract_chains_bestfirst.py <target> \
    --severity high \
    --max-chains 4000 \
    --max-hot 50 \
    --p-cutoff 0.05
```

Outputs:

- `targets/<name>/chains/all_bestfirst.jsonl` — every chain that
  survived the cutoff, sorted by `score = P(chain) × 100`.
- `targets/<name>/chains/hot_bestfirst.jsonl` — top 10% (capped at
  `--max-hot`).
- `status.json.phases.extract_chains_bestfirst`.

Per-chain JSON adds:

```json
{
  "p_chain": 0.42,
  "p_calibrated": 0.55,
  "confidence_breakdown": {
    "p_source": 0.95,
    "p_edges": 0.78,
    "p_unsanitized": 1.0,
    "p_viability": 1.0,
    "p_async": 1.0,
    "p_dynamic": 1.0,
    "p_raw": 0.74,
    "breakdown": [{"stage": "source", "p": 0.95}, ...]
  },
  "viability_factor": 1.0,
  "continuation_hops": 0,
  "has_continuation": false
}
```

Calibration: if `targets/_calibration/confidence_model.json` exists, the
raw probability is mapped to P(true_positive) via a logistic fit and
stored as `p_calibrated`. Without a model, `p_calibrated` is null.

## Tuning

| Flag | Default | When to change |
|---|---|---|
| `--p-cutoff` | 0.05 | Raise to 0.10 on very large bundles to shrink output; lower to 0.02 to surface long-tail chains |
| `--max-paths-per-source` | 64 | Lower if a single source emits hundreds of chains |
| `--no-continuation` | off | Use to A/B against bounded BFS without async edges |
| `--severity` | high | Same semantics as bounded extractor |

## Coexistence with bounded extractor

This skill writes `*_bestfirst.jsonl` files, NOT `all.jsonl` /
`hot.jsonl`. Downstream skills (`sanitizer-on-path`, `dom-xss-hunt`,
`opus-deep-audit`) continue reading the bounded extractor's output by
default. Operators choose which file to feed:

```bash
# Use best-first hot list for opus
ln -sf hot_bestfirst.jsonl targets/<name>/chains/hot.jsonl
```

The two extractors are deliberately additive until the confidence
calibration has been validated against the engagement corpus.
