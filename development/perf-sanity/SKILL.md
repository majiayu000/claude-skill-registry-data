---
name: perf-sanity
description: Catch the algorithmic and I/O performance classics before shipping — O(n²) on unbounded input, N+1 queries, load-everything-to-use-a-piece, sync calls in async/hot paths, unbounded memory growth. Use when writing or reviewing loops over data of unknown size, database/API/file access inside loops, request handlers, batch jobs, or anything on a hot path. Not for measured optimisation of existing slow code (see performance-investigation).
---

# perf-sanity

Not optimisation. Weak perf-sanity looks like: the code passes tests on a 10-row fixture, so it ships — and dies at 100k rows in prod. Strong perf-sanity names the realistic size of every input the diff iterates and refuses to ship the five classics against an unbounded one.

## The five classics

1. **Nested iteration over the same collection** — `for x in items: if y in items`, or `.find()`/`.includes()`/`in list` inside a loop over the same data — is O(n²): fine at 100 items, dead at 100k. Build a set/map once and look up.
2. **Query-in-a-loop is the N+1.** A DB/API/RPC call inside `for row in rows` turns one round-trip into a thousand. Batch it: `WHERE id IN (...)`, a join, the bulk endpoint, a prefetch. Same for file opens, subprocess spawns, and per-item logging to a slow sink.
3. **Loading the whole thing to use a piece:** reading a full file for its first line, fetching all rows to count them, deserialising a payload to check one field. Stream, `LIMIT`, or push the filter/aggregate down to the source.
4. **Sync blocking in async/hot paths:** a synchronous HTTP call, file read, or `sleep` inside an async handler stalls the event loop for every caller. Use the async client or move it off-path.
5. **Unbounded growth:** caches without eviction, module-level lists appended per request, listeners registered but never removed, unbounded queues. Anything that grows with traffic needs a bound or an eviction rule.

## The check (before reporting done)

1. **Bound inventory.** For every loop, comprehension, `map`/`filter`/`reduce`, and recursive walk the diff adds, write down what it iterates and its realistic maximum: the source (user data, DB table, API page, log file, config) and a number. If you don't know the number, measure it — `SELECT COUNT(*)`, `wc -l`, the API's page size × page count — don't guess. Config lists and enum tables are bounded; anything a user or the system can grow is not.
2. **Loop-body scan.** For each loop over an unbounded input, list every I/O call, nested search, and fresh large allocation in its body. Each one is batched/hoisted or explicitly justified in the report.
3. **Growth scan.** For every new cache, list, map, queue, or listener that outlives a request, name what bounds it.
4. **Run it once at realistic size** when that is cheap (a generated fixture, a prod-sized dev table). Tiny-fixture tests don't catch complexity-class bugs; they hide them.

## Calibration

The bar is "no complexity-class surprises on realistic input sizes" — not micro-optimisation. A readable O(n) beats a clever O(n log n); a loop over a 20-entry config list needs no fix, and rewriting bounded code for hypothetical scale is scope creep. When you fix a classic, keep the diff minimal and behaviour identical: same ordering, same handling of duplicates, same error on a missing key.

## Report

State the input-size assumption: "safe up to ~N items because X is bounded by Y; the previous version was O(n²) in Z." If a classic remains because fixing it is out of scope, flag it with the input size it fails at rather than shipping it silently.
