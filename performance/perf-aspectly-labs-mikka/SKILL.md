---
name: perf
description: Identify and fix performance bottlenecks in applications and services. Always use this skill when investigating slow requests, high latency, memory pressure, CPU usage, cache misses, N+1 queries, or when profiling or benchmarking. Use when the user says "this is slow", "help me optimize this", "why is this taking so long", "response times are too high", "high CPU/memory", "I want to add caching", "how do I detect N+1 queries", or any request to find and fix a bottleneck. Do not recommend optimizations without reading this skill first.
---

# Perf

Performance work has one rule: measure first. Intuition about where time goes is usually wrong. Profile before optimizing, or you'll spend time speeding up code that isn't the bottleneck.

## The performance investigation workflow

1. **Define the problem precisely.** "Slow" is not a specification. What's the current latency at p50, p95, p99? What's the target? Under what load? Without a number, you can't tell if you've improved anything.

2. **Reproduce it.** Find a request, a data set, or a load pattern that reliably triggers the problem. If you can't reproduce it, you can't fix it or verify the fix.

3. **Profile, don't guess.** Run the workload under a profiler and read the flame graph or call tree. The hot path is where to look: not the code you wrote most recently, not the code that looks most suspicious.

4. **Fix the biggest thing first.** A 40% improvement on a function that takes 5% of total time is a 2% overall win. A 20% improvement on the function that takes 70% of total time is a 14% win. Work top-down on the profiler output.

5. **Measure after each change.** Don't batch optimizations and measure once at the end; you won't know which change did what, and you risk optimizing away something that was actually hurting you elsewhere.

## Database / data access

This is the most common bottleneck in web applications. Check here first.

**N+1 queries**: executing one query to get a list, then one query per item. Symptoms: query count per request scales linearly with result set size; each query is fast but total time is high. Fix: eager load with a JOIN or a batched secondary query.

**Missing indexes on frequent queries**: symptoms include sequential scans in EXPLAIN output and high rows-examined / rows-returned ratios. Fix: add the right index (see db-review skill for indexing strategy).

**Overly broad queries**: `SELECT *` when only 3 columns are needed, loading 10,000 rows into memory to display 20. Fix: select only needed columns; add limits and filters at the query layer.

**Slow query log**: enable it (Postgres: `log_min_duration_statement`, MySQL: `slow_query_log`). A baseline of your slowest queries is the fastest way to find the biggest wins.

**Connection pool exhaustion**: symptoms include requests queuing while waiting for a DB connection; high wait time even though queries are fast. Fix: tune pool size (usually max: 10–20 per app instance is enough; bigger isn't better), or reduce connection hold time.

**Read replicas for read-heavy workloads**: if writes are fast but reads are the bottleneck, offloading reads to a replica can multiply throughput. Be aware of replication lag: don't read from a replica immediately after a write the user just made.

## Caching

Cache only after measuring. Premature caching introduces complexity and bugs (stale data, invalidation races) with no guaranteed payoff.

**What's worth caching:**

- Data that's expensive to compute and changes infrequently
- External API responses where the upstream is slow or rate-limited
- Computed aggregates or roll-ups that would require large queries to recompute

**What's not worth caching:**

- Fast DB queries on indexed columns: the gain is marginal, the complexity is real
- User-specific data that changes frequently: cache hit rates will be low
- Anything where serving stale data would be harmful

**Cache invalidation strategy**: decide before implementing. Options:

- **TTL-based**: simple, always eventually consistent, can serve stale data up to TTL duration
- **Write-through**: update cache on every write; cache is always fresh; coupling between write path and cache
- **Event-based invalidation**: invalidate on domain events; works well with a message bus; harder to reason about
- **Cache-aside**: read from cache, fall back to source on miss, populate cache on miss; simple, no write coupling, but thundering herd on cold cache

**Thundering herd on cache miss**: when a popular key expires, many concurrent requests all miss and all hit the database simultaneously. Mitigations: probabilistic early expiration (refresh before TTL expires), mutex/lock on the first miss, or background refresh.

## CPU / compute

**Flame graphs** are the right tool. A flame graph shows where CPU time is spent, including call stacks. Learn to read them: the wide bars at the top of the stack are where time is consumed.

Common CPU bottlenecks:

- JSON serialization/deserialization: often surprisingly expensive at scale; consider binary formats (protobuf, msgpack) or partial serialization
- Cryptography: bcrypt is intentionally slow; if you're hashing many passwords per request, rethink the design
- Regex on large inputs or with catastrophic backtracking: test regex with adversarial inputs before using them on untrusted data
- Sorting or aggregation on large in-memory datasets: move these operations to the database or streaming layer
- Memory allocation / GC pressure: excessive object creation in a hot loop causes frequent garbage collection; profile heap allocation, not just CPU

## Memory

**GC pressure** masquerades as CPU load. If GC pause time is high, reducing allocation in the hot path is more effective than optimizing the computation.

**Memory leaks in long-running processes**: common causes include event listeners not removed, caches with no eviction policy, or accumulated references in closures. Profile heap snapshots over time; if heap size grows monotonically and never drops, something is leaking.

**Buffer/stream large payloads**: loading a 500MB file into memory to process it fails under load. Stream it: process chunks as they arrive instead of buffering the whole thing.

## Network / I/O

**Parallelize independent I/O.** If a request makes three independent API calls sequentially, it takes the sum of their latencies. Made in parallel, it takes the max. This is often the fastest win available in service-to-service systems.

**Latency budget awareness**: map out where time goes in a typical request. If your target is 200ms p95 and you're making 4 sequential external calls averaging 60ms each, you've already spent 240ms before doing anything else. Either parallelize or reduce the number of calls.

**Connection reuse**: don't create a new HTTP client per request; reuse connections. Most HTTP client libraries do this by default if you reuse the client instance.

**Payload size**: large response bodies cost bandwidth and serialization time. Check if clients actually use everything in the response. For internal APIs, consider a projection parameter or field filtering.

## Load testing

You can't know if a fix works at scale without testing at scale. Tools: k6, Locust, wrk, hey.

A minimal load test:

1. Identify the critical path (the endpoint or workflow that must be fast)
2. Run at the current production load level and verify you hit your latency targets
3. Find the break point: increase load until latency degrades or errors appear
4. Fix the bottleneck, repeat

Test on a realistic data set. A database with 100 rows and one with 100 million rows behave completely differently; the former gives you no signal about production behavior.
