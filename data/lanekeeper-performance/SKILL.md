---
name: lanekeeper-performance
description: How to meet and prove Lanekeeper's performance budgets (P1–P15), such as drift in 15 s, the grid across 40 swimlanes in 150 ms, text search in 400 ms, and live updates in 1 s. Covers writing criterion benchmarks at design scale, registering them in perf/budgets.toml, running cargo xtask bench-check, profiling with flamegraphs and EXPLAIN ANALYZE, and the mechanisms that make the budgets achievable (content addressing, settings and tree indexes, incremental recompute, moka caches, keyset pagination, zstd, rayon, virtualisation). Use this skill whenever you implement or change a hot path, query, cache, background job, agent scan, MCP read tool or heavy UI view, whenever a prompt lists a P#, and before escalating that a budget can't be met.
---

# Lanekeeper performance

Performance is the second priority (D61). Budgets are checked by machines, not by opinion: a P# without a registered benchmark or load test counts as unmet. Budgets live in `docs/performance.md`, and the numbers enforced are in `perf/budgets.toml`.

## Workflow for any P# in your prompt

1. **Locate the budget.** Note the P#, the threshold, and the scale it's measured at. Design scale is 40 swimlanes × 2,000 files, 100 web users and 30 MCP sessions.
2. **Generate realistic data.** Run `cargo xtask gen-fixtures --scale target`. It's deterministic, and it includes CRLF files, 6,000-line YAML, images, channel folders and duplicate names. Never benchmark on toy data; budgets fail at scale for different reasons.
3. **Write the benchmark** with criterion, in your crate's `benches/`, measuring the real hot path end to end within your crate. A benchmark of a helper that skips the database or the parse doesn't count.
4. **Register it in `perf/budgets.toml`:**

   ```toml
   [[budget]]
   id = "P7.grid"
   bench = "hub-registry/grid_40_swimlanes"
   statistic = "p95"
   threshold_ms = 150
   scale = "target"
   ```

   This file is a contract, so new entries go through a `contract-change` PR (the `lanekeeper-contract-change` skill).
5. **Check it:** `just bench && cargo xtask bench-check`. Paste the table into the PR.
6. **If it misses, profile before optimising:**
   - CPU: `cargo flamegraph --bench <name>`.
   - Allocations: dhat or heaptrack.
   - SQL: `EXPLAIN (ANALYZE, BUFFERS)`.
   - Async stalls: tokio-console.

## Mechanisms to reach for, in order

1. **Don't do the work twice.**
   - Content-address everything (SHA-256).
   - Parse each unique blob once into `settings_index`.
   - Index each Git commit once into `git_tree_index`.
   - Cache derived results in moka, keyed by input hashes. They never go stale, so they never need invalidating.
2. **Don't do work that didn't change.**
   - Recompute incrementally, from events.
   - Agents send Merkle deltas.
   - Whole-swimlane compare skips subtrees whose effective tree hashes are equal.
3. **Push filtering into indexed SQL.**
   - pg_trgm for setting paths.
   - Keyset pagination.
   - No N+1 queries; batch with `= ANY($1)`.
4. **Use the cores.** rayon over deduplicated blobs, inside `spawn_blocking`.
5. **Move fewer bytes.**
   - zstd on agent streams.
   - `Bytes` instead of copies.
   - Immutable blob URLs with ETags.
   - Server-computed diff hunks.
   - MCP output capped at 16 KB.
6. **Render less.**
   - Virtualised lists with fixed row heights.
   - Lazy-loaded Monaco.
   - Route-level code splitting.
   - Query keys that include content hashes, so cached data is safe to reuse.

## Anti-patterns that have sunk budgets elsewhere

- Parsing YAML per request instead of reading `settings_index`.
- Building the grid by loading whole files for 40 swimlanes.
- `OFFSET` pagination on large tables.
- Holding a database transaction across an agent round trip.
- Unbounded fan-out: one SSE event triggering a refetch of everything on every client. Invalidate the precise query keys.
- Cloning large `Vec<u8>` buffers between layers.
- Synchronous filesystem access inside async code.

## Escalating a miss

If you can't meet a budget with your prompt's approach, stop and write in the PR:

- the P#;
- the measured p50, p95 and p99;
- a flamegraph or `EXPLAIN` excerpt;
- what you tried;
- the options, each with its trade-off: an index change, a contract change, or a scale assumption.

A human decides. Never loosen `perf/budgets.toml` yourself.
