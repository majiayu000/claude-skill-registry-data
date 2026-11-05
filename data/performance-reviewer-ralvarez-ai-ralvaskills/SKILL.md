---
name: performance-reviewer
version: 1.0.0
description: Cross-language perf review — N+1, missing indexes, blocking I/O in async, allocation hot paths, unbounded memory, slow algorithms. Findings grounded in EXPLAIN / pprof / py-spy / metrics. Use when reviewing for perf or investigating a slow endpoint.
---

# Performance Reviewer

Reviews code for performance issues before they show up in production metrics. **Measurement-grounded** — every finding references a profiler output, an `EXPLAIN` plan, or a metric from [observability-architect](../../infra/observability-architect/SKILL.md). Guesses don't go in the report. Findings table + severity guide + tooling reference in [RECIPES.md](RECIPES.md).

## 1. When to invoke

- PR touches a hot path (request handler, DB query, loop over large data, queue consumer).
- Endpoint shows up in latency p99 / error-rate dashboards.
- Before a planned load test.
- After a metric regression — dashboard burn, SLO degradation.
- New code with `for` + `await` / `for` + DB call patterns (the N+1 detector).

## 2. Output format

Same shape as other reviewers — findings table + summary. Sample row layout and severity rubric in [RECIPES § 1–2](RECIPES.md#1-example-findings-report).

**Every finding must include a measurement** — `EXPLAIN ANALYZE`, a pprof flame, a histogram bucket, a `hyperfine` result. *"Looks slow"* is not a finding.

## 3. Review approach

1. **Measure first.** Without a measurement, there's nothing to review. Run `EXPLAIN ANALYZE` on the suspect query, attach the profiler to the running process, or check the dashboard for the endpoint's p99.
2. **Read the diff with measurement in hand.** The measurement narrows where to look.
3. **Propose fixes that produce another measurement.** A fix without "and the new latency is X" is incomplete.

## 4. What to check — by category

### Database — N+1 and unindexed scans

The single most common perf bug. Per [sql-architect §5](../../databases/sql-architect/SKILL.md#5-joins--n1-prevention):

- **N+1 detection.** A list endpoint that fires one query for parents, then one per parent for children. Look for `for x in xs: y = repo.get(x.id)`. Fix: batch with `IN (?, ?, ?)`, a single JOIN, or a DataLoader-style batcher.
- **In tests:** log every SQL statement; a handler emitting > 3 queries per request is suspect.
- **Missing indexes.** Per [sql-architect §3](../../databases/sql-architect/SKILL.md#3-indexing-strategy): index every FK; index columns used in `WHERE`; composite column order is most-selective-first.
- **`EXPLAIN ANALYZE` shows the truth.** Look for `Seq Scan` on large tables, `Sort` operations spilling to disk, `actual rows` >> `plan rows` (stale stats — run `ANALYZE`).
- **Pagination by OFFSET is O(N).** Switch to cursor per [sql-architect §4](../../databases/sql-architect/SKILL.md#4-query-patterns).
- **Connection pooling** — any handler opening a connection per request is a bug. Pool in the lifespan.

### Async — blocking I/O in event loop

The Python async equivalent of N+1.

- **`time.sleep` inside `async def`** — blocks the event loop. Use `await asyncio.sleep(d)`.
- **`requests.get(...)` inside `async def`** — blocking HTTP. Use `httpx.AsyncClient`.
- **Sync DB driver (`psycopg2`) inside `async def`** — blocking. Use `psycopg 3` async.
- **Detection:** `asyncio.get_event_loop().slow_callback_duration = 0.1` in dev logs callbacks over 100 ms.
- **`asyncio.to_thread(blocking_fn, args)`** when you genuinely must call a sync API.
- **`asyncio.TaskGroup`**, not bare `asyncio.gather` — handles cancellation and exception aggregation properly per [python-architect §4](../../languages/python-architect/SKILL.md#4-concurrency--resources).

### Go — goroutine and allocation issues

- **Unbounded goroutine spawn.** A loop firing `go func()` per item without backpressure. Use a worker pool or `errgroup` with `SetLimit(n)`.
- **`sync.WaitGroup.Go(fn)`** per [go-architect §7](../../languages/go-architect/SKILL.md#7-concurrency) — Go 1.25+, cleaner than `Add(1) / defer Done()`.
- **Channels with wrong direction or buffer.** Unbuffered + goroutine on each side = deadlock waiting to happen.
- **`context.Background()` in handlers** — request context not propagated; cancellation never reaches downstream calls.
- **Allocation hot paths.** `pprof` heap profile; if `runtime.makeslice` / `runtime.newobject` tops `alloc_objects`, reuse buffers via `sync.Pool`.
- **Slice growth** — appending without `make([]T, 0, capacity)` reallocates. If you know the size, set it.

### Algorithms and data structures

- **O(N²) loops over growing collections.** Nested `for` with linear lookups (`if x in list`) — convert the inner lookup to a `set` / `map`.
- **`sort.Slice` in a hot path** when items arrive sorted from upstream — trust upstream order.
- **Eager materialization of iterators.** `list(big_generator)` defeats the purpose. Stay lazy.
- **String concatenation in loops** — quadratic in both languages with `+`. Use `"".join(parts)` / `strings.Builder`.
- **Regex in hot paths** — compile once at module load, never inside the function.

### Memory

- **Unbounded caches.** A `dict` / `map` growing without eviction is a memory leak. LRU with max size, or TTL.
- **Long-lived references to short-lived data.** Closures capture the parent frame; if the closure outlives the function, the frame stays alive.
- **Large struct copies.** A 2 KB struct passed by value through 10 layers — pointer once size justifies it (~64 bytes is a rough Go cutoff).
- **Goroutine leaks** — a goroutine waiting on a never-closed channel is a leak. Go 1.26's experimental `goroutineleak` profile catches them.

### Network / external calls

- **Missing timeouts** — every outbound HTTP / DB / queue / RPC call has a context deadline. Unbounded waits cause cascading failures.
- **No retry with backoff** — flaky downstream gets hammered in a tight loop. Jittered exponential backoff is mandatory.
- **HTTP keep-alive disabled** — TLS handshake per request. Reuse the client.
- **Single-flight** — N concurrent requests for the same key dedupe via `singleflight` (Go) / a request-scoped cache (Python). Otherwise a cache miss for a hot key floods downstream.

### Sampling and observability cost

- **High-cardinality labels in metrics** — per [observability-architect §2](../../infra/observability-architect/SKILL.md#2-metrics-prometheus): metric explosion is a perf issue for Prometheus too.
- **Logging in tight loops** — `log.Info` inside a 1M-iteration loop dominates the runtime. Log once at the end with a summary.
- **Tracing every internal call** — per-call spans for hot inner loops kill throughput. Trace request boundaries + major sub-ops, not every function.

## 5. Tooling

Tools that ground the findings — full reference in [RECIPES § 3](RECIPES.md#3-tooling-reference). Always reference the tool output in the Evidence column.

Quick picks: **SQL** → `EXPLAIN (ANALYZE, BUFFERS)` + `pg_stat_statements`. **Go** → `pprof`. **Python** → `py-spy`. **Bench** → `hyperfine` (CLI), `go test -bench`, `pytest-benchmark`. **Load** → `wrk` / `k6`. **Symptom** → Grafana RED+USE.

## 6. What this skill does NOT do

- **Load testing.** Generating load is operational work — `k6` / `wrk` runs against staging, not in a code review.
- **Capacity planning.** "How many instances at 2× traffic" is a different conversation.
- **Premature optimization.** A finding requires a measurement; gut-feel optimizations are rejected. If the code isn't measurably slow, don't change it.

## 7. Cross-skill ties

- [sql-architect §3–§5, §9](../../databases/sql-architect/SKILL.md) — indexing, query patterns, N+1, `EXPLAIN ANALYZE`. Most common source of findings.
- [observability-architect](../../infra/observability-architect/SKILL.md) — RED/USE metrics reveal where to look. Findings often start with "this dashboard shows..."
- [grafana-architect](../../infra/grafana-architect/SKILL.md) — burn rate / SLO dashboards trigger reviews.
- [go-architect §7](../../languages/go-architect/SKILL.md#7-concurrency) / [python-architect §4](../../languages/python-architect/SKILL.md#4-concurrency--resources) — concurrency primitives.
- [rest-api-architect §5](../../protocols/rest-api-architect/SKILL.md#5-pagination--cursor-not-offset) / [§14](../../protocols/rest-api-architect/SKILL.md#14-rate-limiting) — cursor pagination, rate limiting at the API layer.
- [improve-codebase-architecture](../../refactoring/improve-codebase-architecture/SKILL.md) — when a finding requires structural change, promote to architecture review.
