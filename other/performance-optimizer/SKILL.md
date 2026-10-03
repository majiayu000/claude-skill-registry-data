---
name: performance-optimizer
description: Expert performance analysis and optimization guidance. Use when the user asks about frontend optimization, API latency, database optimization, memory leaks, CPU bottlenecks, or profiling.
---

# Performance Optimization

Approach every performance task as an engineer who measures before cutting. Premature optimization is the source of more production incidents than slow code. The process is always: measure → identify the actual bottleneck → fix the bottleneck → measure again. Intuition about where the slowness is has a poor track record. Data does not.

---

## Step 0: Measure First, Optimize Second

Before touching any code:

1. **Reproduce the problem with numbers** — "it feels slow" is not a problem statement; "p99 latency is 4.2s under 100 concurrent users" is
2. **Identify the bottleneck** — use profiling tools to find where time is actually spent; it is almost never where you expect
3. **Establish a baseline** — measure before making any change; you cannot prove improvement without a before number
4. **Change one thing at a time** — multiple simultaneous optimizations make it impossible to know what helped
5. **Measure the result** — verify the optimization worked and did not regress something else

**Optimization priority order:**
1. Algorithmic complexity — O(n²) becoming O(n log n) beats any micro-optimization
2. I/O reduction — fewer DB queries, fewer HTTP calls, smaller payloads
3. Caching — avoid recomputing or re-fetching what has not changed
4. Parallelism — do independent work concurrently instead of sequentially
5. Micro-optimization — only after the above have been exhausted

---

## Frontend Performance

**Measure with real tools:**
- Lighthouse CI in the CI pipeline — fail builds that regress Core Web Vitals
- Chrome DevTools Performance panel — flame charts for CPU, network waterfall for load
- WebPageTest — real device testing, multiple geographic locations
- `web-vitals` library — measure LCP, FID/INP, CLS in production with real user data

**Core Web Vitals targets:**
- LCP (Largest Contentful Paint) < 2.5s
- INP (Interaction to Next Paint) < 200ms
- CLS (Cumulative Layout Shift) < 0.1

**Bundle size:**
- Analyze with `webpack-bundle-analyzer` or `vite-bundle-visualizer` — know what is in the bundle
- Code split at route boundaries — never ship one monolithic bundle
- Tree-shake unused exports — ensure bundler tree-shaking is working
- Lazy-load heavy components and libraries: charting, rich text editors, PDF renderers
- Audit and remove unused dependencies — they ship to the client even if unused
- Target: initial JS bundle < 200KB gzipped for most applications

**Images:**
- Use `next/image` or equivalent — automatic WebP, lazy loading, correct sizing
- Specify `width` and `height` on every image — prevents layout shift
- Use CSS sprites or SVG for icons — not dozens of small PNG requests
- Compress images before serving — never serve raw camera images

**JavaScript execution:**
- Avoid long tasks on the main thread (> 50ms) — they block user interaction
- Move heavy computation to Web Workers
- Debounce / throttle scroll, resize, and input event handlers
- Avoid layout thrashing — batch DOM reads and writes; do not interleave them
- `React.memo`, `useMemo`, `useCallback` only when profiling shows a measurable benefit — they add complexity and are commonly overused

**Network:**
- HTTP/2 or HTTP/3 — multiplexing eliminates per-request connection overhead
- Preconnect to critical third-party origins: `<link rel="preconnect">`
- Preload critical assets: fonts, hero images, above-the-fold CSS
- Use a CDN for static assets — serve from the edge, not the origin
- Cache static assets aggressively with content-hashed filenames — `main.abc123.js` can be cached forever

---

## API Latency

**Find the bottleneck — use distributed tracing:**
- OpenTelemetry spans on every significant operation — DB query, external HTTP call, cache lookup, business logic
- Look for: sequential calls that could be parallel, N+1 patterns, slow DB queries, unnecessary external calls

**Common API latency culprits and fixes:**

| Problem | Diagnosis | Fix |
|---------|-----------|-----|
| N+1 queries | ORM generates one query per item in a list | Eager load with joins or `IN` query |
| Missing index | `EXPLAIN ANALYZE` shows seq scan | Add targeted index |
| Synchronous external calls | Trace shows sequential HTTP calls | Fan out with `Promise.all` / `asyncio.gather` |
| Oversized response | Response payload is large | Paginate; return only requested fields |
| No caching | Same data fetched on every request | Cache at service or HTTP layer |
| Connection overhead | New DB connection per request | Connection pooling |
| Serialization overhead | Large object serialized repeatedly | Cache serialized form |

**Response size matters:**
- Return only the fields the client needs — avoid `SELECT *` and avoid serializing entire domain objects to API responses
- Compress responses with gzip or brotli — most frameworks enable this with one config line
- Paginate — a response with 10,000 items is slow to serialize, transmit, and parse

**Caching strategy:**
- Cache at the layer closest to the consumer
- HTTP cache headers for public, stable content — `Cache-Control: public, max-age=3600`
- Application cache (Redis) for: computed results, external API responses, expensive DB queries
- Define invalidation before caching — stale data is a correctness bug, not just a performance issue
- Cache hit rate is a metric — monitor it; a low hit rate means the cache is not helping

---

## Database Performance

**Slow query workflow:**
1. Enable slow query log — capture all queries above a threshold (e.g., > 100ms)
2. `EXPLAIN ANALYZE` on the slow query — read the actual plan, not the estimated one
3. Look for: seq scans on large tables, nested loops on large sets, high row estimates vs. actuals
4. Add the appropriate index — verify with `EXPLAIN ANALYZE` that it is used
5. Run `ANALYZE` if estimates are far off — statistics may be stale

**N+1 query pattern:**
```
# ❌ N+1 — one query for the list, one per item
orders = db.query("SELECT * FROM orders WHERE user_id = ?", user_id)
for order in orders:
    items = db.query("SELECT * FROM order_items WHERE order_id = ?", order.id)

# ✅ Single query with join or IN clause
orders = db.query("""
    SELECT o.*, oi.*
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.id
    WHERE o.user_id = ?
""", user_id)
```

**Index effectiveness:**
- Use covering indexes for hot read paths — include all columns the query needs to avoid heap fetches
- Use partial indexes for sparse conditions — index only the subset of rows the query filters on
- Monitor index usage — drop indexes that are never used; they slow every write
- Index bloat accumulates over time — `REINDEX CONCURRENTLY` periodically on heavily updated tables

**Connection pooling:**
- Never open a new DB connection per request — pool connections at the application layer (PgBouncer, SQLAlchemy pool, HikariCP)
- Monitor connection pool utilisation — exhausted pools queue requests and spike latency
- Set pool size based on DB server capacity, not application concurrency

**Query patterns:**
- Avoid `SELECT *` — fetch only needed columns; reduces data transfer and enables covering indexes
- Avoid `OFFSET` pagination at scale — use cursor-based pagination
- Avoid `LIKE '%term%'` on large tables — use full-text search indexes
- Use `EXISTS` instead of `COUNT` when checking existence — stops scanning after the first match

---

## Memory Leak Detection

**Node.js:**
- Heap snapshots in Chrome DevTools — take two snapshots separated by a period of activity; compare retained objects
- `--inspect` flag to attach Chrome DevTools to a Node process
- Common sources: event listeners not removed, global state that accumulates, closures holding large objects, unbounded caches

**Python:**
- `tracemalloc` — trace memory allocations to their source
- `memory_profiler` — line-by-line memory usage
- Common sources: growing lists/dicts never cleared, circular references (though Python GC handles most), large objects cached without eviction

**General signals:**
- Steady memory growth that does not plateau — the hallmark of a leak
- Memory growth correlated with request count — something is accumulating per request
- Out-of-memory crashes on long-running processes

**Prevention:**
- Bounded caches — LRU cache with a max size; unbounded caches are memory leaks
- Remove event listeners on cleanup — every `addEventListener` needs a corresponding `removeEventListener` on teardown
- Weak references for caches where eviction on GC is acceptable

---

## CPU Bottlenecks

**Profiling tools:**
- Node.js: `--prof` flag + `node --prof-process`; Chrome DevTools flame chart
- Python: `cProfile` + `snakeviz` for visualisation; `py-spy` for sampling a live process without restart
- Go: `pprof`

**Common CPU bottlenecks:**
- Synchronous JSON serialization of large objects — consider streaming serialization or pre-serialization
- Regular expression on large inputs — catastrophic backtracking on poorly written regex; test with ReDoS tools
- Cryptographic operations on the request path — move to background workers if not latency-critical
- Sorting large collections — O(n log n) on every request; cache sorted results
- Unnecessary re-renders in React — profile with the React DevTools Profiler

**Parallelism:**
- CPU-bound work in Node.js blocks the event loop — offload to worker threads or a separate process
- Python GIL limits CPU parallelism in threads — use `multiprocessing` for CPU-bound work; async/threads for I/O-bound work
- Horizontal scaling is not a substitute for fixing an O(n²) algorithm — fix the algorithm first

---

## Bundled Reference

Read [measurement-plan.md](./references/measurement-plan.md) before collecting a baseline or interpreting a before/after performance result.

## Definition of Done — Performance Work

- [ ] Baseline measured before optimization with specific numbers
- [ ] Bottleneck identified with profiling tools — not intuition
- [ ] One change made at a time
- [ ] Improvement verified against baseline with the same measurement method
- [ ] No regressions in correctness, memory usage, or latency on other paths
- [ ] Performance budget or SLO defined and monitored going forward
- [ ] CI check added to prevent regression (Lighthouse CI, latency threshold test, or equivalent)
