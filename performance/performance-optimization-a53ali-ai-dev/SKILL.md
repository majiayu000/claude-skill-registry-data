---
name: performance-optimization
description: Systematically profile, identify, and fix performance bottlenecks using a measure-first workflow covering CPU, memory, I/O, network, and database hot paths — never guess, always instrument
triggers:
  - "performance optimization"
  - "slow performance"
  - "profiling"
  - "bottleneck"
  - "performance investigation"
  - "flame graph"
  - "memory leak"
  - "N+1 query"
  - "performance budget"
  - "latency"
  - "throughput"
audience: engineer
---

# Performance Optimization

## Context
Performance work that starts without measurement is waste. As Donald Knuth wrote: *"Premature optimization is the root of all evil."* The corollary is equally important: when performance does matter, optimization without profiling data is guesswork that often makes things worse.

Use this skill when:
- A service or function is slower than its SLO or performance budget
- A code review surfaces a pattern that could be a bottleneck at scale
- Load testing or production monitoring reveals latency regression
- Memory usage is growing unboundedly or OOM events are occurring
- You are about to optimize something and need to confirm it's actually the bottleneck

The workflow is always: **Find → Measure → Fix → Verify**. Never skip steps.

Martin Fowler's principle: *"Make it work, make it right, make it fast — in that order."* Performance optimization comes last because it trades simplicity for speed, and you need correct code to optimize against.

---

## Instructions / Steps

### Step 1: Define the Target Before Touching Code

1. Establish the **performance budget** — what is "fast enough"?
   - p50, p95, p99 latency targets (e.g., p99 < 200ms)
   - Throughput requirement (e.g., 1000 req/s sustained)
   - Memory ceiling (e.g., < 512MB RSS under load)
2. Identify the **workload profile** — synthetic benchmark or production replay?
3. Reproduce the slow path **locally or in staging** — never optimize blind in production.
4. Confirm the bottleneck is real: check existing metrics (APM traces, dashboards) before writing a single line of code.

### Step 2: Instrument and Profile

Select the profiler for your runtime:

| Runtime      | Tool                          | Command |
|--------------|-------------------------------|---------|
| Node.js      | V8 CPU profiler               | `node --prof app.js` then `node --prof-process isolate-*.log > profile.txt` |
| Node.js      | Clinic.js (higher-level)      | `clinic doctor -- node app.js` |
| Python       | py-spy (sampling, low-overhead)| `py-spy record -o profile.svg --pid <PID>` |
| Python       | cProfile (deterministic)      | `python -m cProfile -o out.prof script.py && python -m pstats out.prof` |
| JVM (Java/Kotlin/Scala) | async-profiler      | `./profiler.sh -d 30 -f profile.html <PID>` |
| Go           | pprof                         | `go tool pprof -http=:8080 cpu.prof` |
| Go (in-process) | net/http/pprof             | `import _ "net/http/pprof"` then `curl localhost:6060/debug/pprof/profile?seconds=30 > cpu.prof` |
| Rust         | perf + flamegraph             | `cargo flamegraph` |
| Native / any | perf (Linux)                  | `perf record -g ./binary && perf report` |

**Flame graph reading rules:**
- X-axis = sample count (width = time spent, not time of execution)
- Y-axis = call stack depth
- Wide flat bars at the top = hot functions — these are your targets
- Narrow slivers everywhere = well-distributed work, investigate algorithmic complexity instead

### Step 3: Identify Bottleneck Category

#### CPU Bottlenecks
- Flame graph shows a wide hot function
- `top` / `htop` shows consistently high CPU
- Fixes: algorithmic improvement (O(n²) → O(n log n)), avoid re-computing in tight loops, compile/WASM hot path, use SIMD where applicable

```bash
# Linux CPU profiling with perf
perf stat -e cycles,instructions,cache-misses ./your-binary
```

#### Memory Bottlenecks / Leaks
- RSS grows indefinitely, never stabilises
- GC pauses increasing over time
- Fixes: find the retention path (what's holding the reference), reduce allocation rate in hot paths, switch to object pooling

```bash
# Node.js heap snapshot (in code)
const v8 = require('v8');
v8.writeHeapSnapshot();

# Python — tracemalloc
python -c "
import tracemalloc, your_module
tracemalloc.start()
your_module.run()
snapshot = tracemalloc.take_snapshot()
for stat in snapshot.statistics('lineno')[:10]: print(stat)
"

# Go — memory profile
go tool pprof -http=:8080 mem.prof
```

#### I/O Bottlenecks
- CPU iowait high in `top`
- `iostat -x 1` shows high `%util` on disk
- Fixes: async I/O, batching reads/writes, pre-fetching, read-ahead buffers, caching hot data in memory

```bash
iostat -x 1 5          # disk utilisation
lsof -p <PID> | wc -l  # count open file descriptors
strace -p <PID> -e trace=read,write,open 2>&1 | head -50  # syscall trace
```

#### Network Bottlenecks
- High latency or bandwidth saturation
- Fixes: connection pooling, HTTP/2 multiplexing, payload compression, CDN for static assets, reduce chattiness (batch calls, GraphQL)

```bash
ss -s              # socket summary
netstat -an | grep CLOSE_WAIT | wc -l  # detect connection leaks
tcpdump -i any -n 'port 5432' -c 100   # inspect DB traffic
```

#### N+1 Query Detection
- ORM emits one query per loop iteration
- APM trace shows hundreds of near-identical queries
- Total DB time >> any single query time

```bash
# PostgreSQL: log all queries exceeding 100ms
ALTER SYSTEM SET log_min_duration_statement = 100;
SELECT pg_reload_conf();

# Then tail the log:
tail -f /var/log/postgresql/postgresql-*.log | grep duration
```

Fix N+1 with eager loading (SQL JOIN or `IN` clause), not ORM lazy loading:

```sql
-- Instead of looping and calling SELECT for each user_id:
SELECT orders.*, users.name
FROM orders
JOIN users ON orders.user_id = users.id
WHERE orders.created_at > now() - interval '7 days';
```

### Step 4: Database Query Analysis

Always run `EXPLAIN ANALYZE` before tuning queries:

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM orders
WHERE customer_id = 42
  AND status = 'pending'
ORDER BY created_at DESC
LIMIT 20;
```

**Reading EXPLAIN ANALYZE output:**

| Term | What it means |
|------|---------------|
| `Seq Scan` | Full table scan — likely missing index |
| `Index Scan` | Uses index, good for selective queries |
| `Bitmap Heap Scan` | Batched index lookup, efficient for moderate selectivity |
| `Hash Join` | Good for large unsorted joins |
| `Nested Loop` | Efficient when inner side is small and indexed |
| `actual time=X..Y` | X = first row, Y = last row — high Y on early steps = bottleneck |
| `rows=N (actual N)` | Large discrepancy = stale statistics, run `ANALYZE tablename` |
| `Buffers: shared hit=X read=Y` | `read` means disk I/O — increase `shared_buffers` or add index |

### Step 5: Caching Strategies

Choose the right layer:

| Strategy | When to use | Tool/Pattern |
|---|---|---|
| Memoization | Pure function, repeated input | In-memory dict/Map, `functools.lru_cache` |
| HTTP cache | Public/semi-public responses | `Cache-Control: max-age=N`, ETags, CDN |
| Application cache | Cross-request, shared state | Redis, Memcached |
| DB query cache | Expensive queries, tolerable staleness | Redis with TTL, materialized views |
| Edge cache | Global latency | Cloudflare, Fastly, CloudFront |

**Cache invalidation rule:** prefer TTL-based expiry over event-based invalidation until you've measured that staleness is actually a problem. Invalidation bugs are harder to debug than stale reads.

### Step 6: Async and Concurrency Improvements

- Move CPU-heavy work off the request path: message queues (SQS, RabbitMQ, Kafka)
- Use connection pooling — never open a new DB connection per request
- Parallelise independent I/O calls (Promise.all, asyncio.gather, goroutines)
- Set timeouts on all outbound calls to prevent cascading slowness

### Step 7: Verify the Fix

1. Re-run the **same profiler** with the same workload — confirm the hot path is gone
2. Run your original benchmark — confirm the target metric improved
3. Check **regression risk**: did p99 improve while p50 regressed? Did memory improve while CPU spiked?
4. Add the performance metric to your CI load test so regressions are caught automatically

---

## Performance Investigation Template

Use this as a structured comment in PRs or incident docs:

```
## Performance Investigation

**Symptom:** [e.g., p99 latency 1.8s, SLO is 500ms]
**Workload:** [production / load test / benchmark — describe traffic profile]
**Profiler used:** [py-spy / pprof / async-profiler / etc.]

### Findings
- Hot path: [function/query/syscall]
- Category: [CPU / Memory / I/O / Network / DB]
- Root cause: [e.g., N+1 query in OrderService.getByUser()]

### Fix Applied
- [Change 1]
- [Change 2]

### Before / After
| Metric | Before | After |
|--------|--------|-------|
| p50 latency | Xms | Yms |
| p99 latency | Xms | Yms |
| Memory RSS | XMB | YMB |
| DB query count per request | N | M |

### Verification
- [ ] Profiler confirms hot path removed
- [ ] Load test confirms SLO met
- [ ] No regressions in adjacent metrics
```

---

## Performance Budgets

Define budgets per service tier and enforce them in CI:

| Tier | p50 | p95 | p99 | Memory | Notes |
|------|-----|-----|-----|--------|-------|
| Critical path (checkout, auth) | 50ms | 150ms | 300ms | 256MB | Synchronous, user-blocking |
| Standard APIs | 100ms | 400ms | 800ms | 512MB | Most CRUD |
| Async / background jobs | N/A | 5s | 30s | 1GB | Batch processing |
| Static assets | 5ms | 20ms | 50ms | N/A | Should be CDN-served |

---

## Common Anti-Patterns

| Anti-Pattern | Impact | Fix |
|---|---|---|
| Optimizing before profiling | Wasted effort, often makes things worse | Always profile first |
| Caching inside a transaction | Stale reads, deadlocks | Cache outside transaction boundaries |
| Loading full objects when only IDs needed | Memory waste, serialization cost | Use projections / `SELECT id` |
| Synchronous network call in a loop | Latency multiplied by N | Batch or parallelise |
| Unbounded result sets | Memory exhaustion | Always paginate with LIMIT |
| String concatenation in a loop | O(n²) allocation | Use StringBuilder / join |
| Missing index on foreign key | Slow joins at scale | Index all FK columns |

---

## Output Format
When applying this skill, the agent should:
- Identify which bottleneck category applies (CPU / memory / I/O / network / DB) before suggesting a fix
- Provide the specific profiler command for the detected runtime
- Run or suggest `EXPLAIN ANALYZE` for any query performance concern
- Fill in the Performance Investigation Template with findings
- Quantify the improvement expected, not just describe the change
- Verify the fix with a before/after metric comparison
- Flag if the fix introduces a new trade-off (e.g., memory for speed)

---

## References
- [Refactoring for Performance — Martin Fowler](https://martinfowler.com/articles/refactoring-performance.html)
- [DORA Metrics and Deployment Frequency](https://dora.dev/guides/dora-metrics-four-keys/)
- [Flame Graphs — Brendan Gregg](https://www.brendangregg.com/flamegraphs.html)
- [USE Method (Utilisation, Saturation, Errors) — Brendan Gregg](https://www.brendangregg.com/usemethod.html)
- [pprof documentation — Go](https://pkg.go.dev/net/http/pprof)
- [async-profiler — GitHub](https://github.com/async-profiler/async-profiler)
- [py-spy — GitHub](https://github.com/benfred/py-spy)
- [PostgreSQL EXPLAIN documentation](https://www.postgresql.org/docs/current/sql-explain.html)
