---
name: async-edges
description: Build async/event continuation edges into per-target snapshot DB so interprocedural taint reaches handler bodies. Run after js-index + db-isolate + implicit-tags, before extract_chains_bounded or chain-triage. Idempotent.
---

# async-edges

## Purpose

The static callgraph already captures `f()` calls but misses the
handler dispatch through async producers:

```js
el.addEventListener('click', onClick);   // onClick callee but no edge
Promise.resolve(x).then(handler);        // handler unreachable
window.addEventListener('message', recv);// postMessage taint orphan
setTimeout(fn, 10);                      // timer callbacks invisible
```

This skill scans `edges.raw` for producer patterns, resolves each
handler reference to a node id, and writes a synthetic edge with
`edge_class='continuation'` plus a `continuations` metadata row.
Downstream chain extraction picks them up identically to sync edges.

Plan: `plans/ARCHITECTURE_EVOLUTION.md §3`.

## Producers detected

| Producer | Handler arg | Event-taint paths |
|---|---|---|
| `addEventListener('message', fn)` | arg[1] | `data`, `origin`, `source` |
| `addEventListener('*', fn)` | arg[1] | `target.value`, `detail`, `data` |
| `.onmessage = fn` | arg[0] | `data`, `origin`, `source` |
| `.then(fn)` | arg[0] | `__resolved__` |
| `.catch(fn)` | arg[0] | `__rejected__` |
| `.finally(fn)` | arg[0] | — (not taint-through) |
| `setTimeout` / `setInterval` / `setImmediate` / `requestAnimationFrame` / `requestIdleCallback` | arg[0] | — (not taint-through) |
| `new MutationObserver(fn)` | arg[0] | `0.target` |
| `new IntersectionObserver(fn)` | arg[0] | — |
| `.subscribe(fn)` (RxJS) | arg[0] | `__emit__` |
| `ws.onmessage = fn` | arg[0] | `data` |
| `fetch(...).then(fn)` | arg[0] | `__resolved__` |

## When to run

After `js-index` has populated `targets/<name>/db/js_analyzer.db`,
ideally also after `implicit-tags` so closure-expanded tags can flow
through continuation edges. Before `chain-triage` /
`extract_chains_bounded` so the new edges enter the BFS.

Skip if `status.json.phases.async_edges.status == "done"` and the
snapshot has not been re-indexed since.

## Steps

1. **Build edges:**
   ```bash
   python3 bin/build_async_edges.py <target>
   ```
   Idempotent — prior continuation edges are cleared. Output JSON
   reports detected matches, inserted edges, and breakdown by
   producer kind.

2. **Optional dry-run** (does not modify the DB):
   ```bash
   python3 bin/build_async_edges.py <target> --dry-run
   ```

3. **Sanity-check via SQL:**
   ```bash
   sqlite3 targets/<name>/db/js_analyzer.db \
       "SELECT producer_kind, COUNT(*) FROM continuations GROUP BY producer_kind ORDER BY 2 DESC;"
   ```

## Outputs

- Schema change: `edges` table gains `edge_class` column
  (default `'sync'`). All new continuation rows carry
  `edge_class='continuation'` and `resolved_kind='continuation'`.
- New table `continuations`:
  - `(caller_id, line, callee_raw)` PK
  - `producer_kind`, `event_taint_paths` (JSON list),
    `taint_through`, `handler_is_inline`
- `status.json.phases.async_edges` gets `{status, edges_inserted,
  continuations_inserted, by_kind, elapsed_s, ts}`.

## Failure modes

- Handler text is `obj.method.deeply.nested` and the last segment has
  many candidates → handler resolution falls back to the first
  same-name node (low confidence). Same fallback the regular
  `name_match` resolver uses.
- Inline arrow handlers (no name): we match by file + ±5-line proximity
  to the call line. If the anonymous handler's start line is more than
  5 lines away from the call, the edge is dropped (rare in practice).
- Heavily minified bundle where handler text is `n` or `a`: same-name
  fallback may produce phantom edges. The chain extractor's
  `--max-name-match-candidates` threshold defends against this; the
  continuation edge follows the same rule because it inherits the
  resolved-kind drop logic in `extract_chains_bounded._load_edges`.

## Boundary conditions

- No edges in DB at all: 0 matches, 0 inserts; status still written.
- ast_extractor.js has not been re-run since older snapshots: pattern
  still works — it scans `edges.raw` only.
