---
name: implicit-tags
description: Closure-expand source/sink tags along the callgraph so wrapper functions inherit tags with confidence decay 0.7^hop. Writes tags_discovered.jsonl, merges into node_tags. Run after js-index + db-isolate, before chain-triage.
---

# implicit-tags

## Purpose

Static regex/AST tags only fire on the *immediate* function that calls a
dangerous primitive. Wrappers stay invisible:

```js
function renderHTML(el, s) { el.innerHTML = s; }  // direct: tagged
function display(msg)      { renderHTML(slot, msg); }  // invisible
function onEvent(e)        { display(e.data); }  // also invisible
```

This skill walks the callgraph outward from every direct sink (callers)
and direct source (callees) up to 2 hops, emitting derived tags with
confidence `0.7^hop`. Downstream chain extraction picks them up
naturally via `node_tags`, with a confidence multiplier that keeps
direct chains dominant in `hot.jsonl` while implicit chains expand
the `all.jsonl` coverage surface.

## When to run

After `js-index` has built the per-target callgraph and `db-isolate`
has snapshotted it to `targets/<name>/db/js_analyzer.db`, but BEFORE
`chain-triage` / `bin/extract_chains_bounded.py` runs. Re-running is
idempotent — prior `implicit_*`-source rows are cleared before the new
ones land.

Skip if:
- `status.json.phases.implicit_tags.status == "done"` and the snapshot
  hasn't been re-indexed since.
- The user has explicitly disabled implicit tags for this engagement
  (e.g. small target where direct coverage is already complete).

## Inputs

- `targets/<name>/db/js_analyzer.db` (per-target snapshot from
  `bin/db-isolate.py snapshot`).
- Optional flags: `--decay 0.7`, `--max-hops 2`, `--min-confidence 0.0`.

## Steps

1. **Discovery + persist.**
   ```bash
   python3 bin/implicit_tags.py <target_name>
   ```
   This:
   * Reads direct tags from the per-target DB.
   * Walks `edges` (resolved kinds only: `exact`, `this_cross_file`,
     `name_match`) — backward for sinks, forward for sources.
   * Emits one `DerivedTag` per (node, taxonomy_id) reachable within
     `max_hops` hops, shortest-path-wins.
   * Writes `targets/<name>/tags_discovered.jsonl` (one JSON per row).
   * Inserts into `node_tags` with `source='implicit_closure'`,
     `confidence = 0.7^hop`, `evidence = {"hop": N, "path": [...]}`.
   * Updates `status.json.phases.implicit_tags`.

2. **Re-run chain extraction.**
   ```bash
   python3 bin/extract_chains_bounded.py targets/<name>
   ```
   The extractor:
   * Splits sinks into direct (`conf >= 0.99`) vs implicit
     (`conf < 0.99`).
   * Pass 1: walks BFS from every source (direct + implicit) into
     direct sinks. Guarantees baseline coverage even when implicit
     adds thousands of derived tags.
   * Pass 2: walks BFS from *direct* sources only into implicit sinks
     to surface wrapper-coverage chains. Implicit×implicit is skipped
     (confidence ~0.24, signal-to-noise too low).
   * Score multiplier `_score(...) × src_conf × sink_conf` demotes
     implicit chains; `hot.jsonl` stays direct-dominated.
   * Chains carry `confidence`, `tag_source`, and
     `implicit_evidence: {source?: {tag_source, confidence, evidence},
     sink?: {...}}` fields so `cc-taint-adversarial` can show
     evidence trails to its sub-agent.

3. **Sanity-check the inflation.**
   * `triage.json` will show the new chain count; if implicit chains
     dominate `all.jsonl` (>5x direct) check `--decay` (lower it) or
     drop `--max-hops` to 1.
   * `hot.jsonl` should remain ≤15% implicit. If implicit chains
     leak into hot, raise `--min-confidence` (e.g. 0.7) so only
     1-hop derivations participate.

## Outputs

```
targets/<name>/
├── tags_discovered.jsonl     # one DerivedTag JSON per row
├── db/js_analyzer.db         # node_tags rows added with source='implicit_closure'
└── status.json
    └── phases.implicit_tags
        ├── status: done
        ├── discovered: <count>
        ├── by_kind: {sink: N, source: M}
        ├── by_hop:  {1: A, 2: B}
        ├── inserted: <new rows>
        ├── cleared: <prior implicit rows wiped>
        └── elapsed_s: <wall-clock>
```

## Configuration knobs

- `--decay 0.7` (default). Multiplier per hop.
- `--max-hops 2` (default). Wrappers > 2 hops are usually noise.
- `--min-confidence 0.0` (default). Drop tags with conf below this.
  Set to 0.7 to keep only 1-hop derivations.

## Failure handling

- Missing per-target DB → exit 2, logs to `status.json.errors[]`.
- Schema-mismatch (DB indexed pre-confidence-column) → script
  auto-migrates the snapshot in place (adds `confidence`, `evidence`,
  `source` columns with safe defaults).

## Plan reference

Built per `project_implicit_tags_plan.md` Phase 1. Phases 2-5 are
follow-ups (see plan): sanitizer-on-path CFG dominance, framework-aware
tables, naming heuristic seeder, bucket inversion. The closure expander
alone unblocks the chain-surface acceptance criterion (≥30% growth).

## Calibration notes

Validated on `coolblue-intigriti` (57k nodes, 314k edges):
- Direct tags: 8631 sinks + 4247 sources.
- Implicit derivations: 33,655 sinks + 15,000 sources.
- Runtime: 1.7s end-to-end on the full snapshot.
- Chain surface with default cap (max_total=2000): 859 → 2000
  (+132.8%); hot stayed 20/20 direct.
- Uncapped: 17,423 total chains = 7,903 direct + 9,520 implicit;
  5 novel taxonomy pairs from implicit-only chains.
