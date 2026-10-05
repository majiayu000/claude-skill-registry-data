---
name: performance-optimization
description: "The instruction to profile before optimizing survives because intuition about"
---

# Performance Optimization (Verbose)

## Core Patterns

### Measure, Don't Guess

The instruction to profile before optimizing survives because intuition about
performance is unusually bad — worse than intuition about correctness. Code that
*looks* expensive (a nested loop, a regex, a hand-rolled parser) is often trivial
next to code that looks free (an ORM attribute access that lazily fires a query, a
logging call that formats a large object at DEBUG level even though DEBUG is off).

Profiling does more than rank candidates: it changes the plan. A meaningful share
of investigations end with "the fix is a connection-pool setting" or "we call this
three times and only need it once," making the week of rewriting you had scheduled
unnecessary.

```bash
# Sampling profiler — low overhead, attaches to a running production process
py-spy record --pid 4821 --duration 60 --output flame.svg

# Deterministic, high overhead, good for a single hot function
python -m cProfile -s cumtime script.py | head -40

# Line-level, once you know the function
kernprof -l -v hot_module.py
```

Read a flame graph by width, not by height. Width is time spent; depth is only call
nesting. The widest plateau is your target.

| Tool class | Use when | Cost |
|---|---|---|
| Sampling profiler (py-spy, async-profiler, perf) | Production, unknown hotspot | 1–5% |
| Deterministic profiler (cProfile) | Local, need exact call counts | 2–10× slowdown |
| Distributed tracing | Latency spread across services | Per-request span overhead |
| `EXPLAIN ANALYZE` | Time is inside the database | Runs the query |

If tracing shows most of the request budget inside a single query, this skill is
the wrong one — go to `sql-optimization`.

### Define the Target

Optimization without a target never terminates. State the goal as a percentile, a
load level, and a workload:

> p99 latency of `POST /checkout` under 300 ms at 500 rps with the production
> catalog size, measured at the load balancer.

Attach a budget breakdown so you know when a component is out of line:

| Stage | Budget | Actual |
|---|---|---|
| TLS + routing | 15 ms | 12 ms |
| Auth lookup | 10 ms | 45 ms ← |
| Cart read | 40 ms | 38 ms |
| Pricing service | 120 ms | 110 ms |
| Payment authorize | 100 ms | 96 ms |

The over-budget line is where you start, and you stop when it fits. Establishing
the load level matters as much as the latency number — see `load-testing` for
generating the traffic honestly.

### Amdahl's Law and Where to Aim

Overall speedup from improving one component is bounded by that component's share
of total time:

```
speedup_total = 1 / ((1 - p) + p / s)

p = fraction of time in the component
s = speedup of that component
```

| Component share | 2× faster | 10× faster | Infinitely faster |
|---|---|---|---|
| 5% | 1.03× | 1.05× | 1.05× |
| 20% | 1.11× | 1.22× | 1.25× |
| 50% | 1.33× | 1.82× | 2.00× |
| 80% | 1.67× | 3.57× | 5.00× |

Two consequences. First, compute the ceiling before you commit — a heroic 10×
rewrite of a 5% component buys 4.5% and costs you readability permanently. Second,
re-profile after every fix: once you remove the top contributor, the ranking is
different, and the second-largest item from the old profile is frequently not the
new top.

### The Latency Hierarchy

| Operation | Time | Relative to L1 |
|---|---|---|
| L1 cache reference | 1 ns | 1× |
| Branch mispredict | 3 ns | 3× |
| L2 cache reference | 4 ns | 4× |
| Main memory reference | 100 ns | 100× |
| SSD random read | 100 µs | 100,000× |
| Round trip in datacenter | 500 µs | 500,000× |
| Spinning disk seek | 10 ms | 10,000,000× |
| Round trip California→Netherlands | 150 ms | 150,000,000× |

Read this as a strategy, not trivia: the ratio between a memory access and a
network hop is so large that eliminating a single remote call dominates any amount
of CPU tuning. Most real wins are structural — batch N calls into one, cache the
result, move the computation next to the data, or stop doing the work at all.

### Algorithmic Complexity Before Constants

```python
# Accidental quadratic: `in` on a list is O(n)
def find_dupes(new_ids, existing_ids):          # 41 s at n = 50_000
    return [x for x in new_ids if x in existing_ids]

# Linear: hash membership
def find_dupes(new_ids, existing_ids):          # 0.02 s, ~2000× faster
    existing = set(existing_ids)
    return [x for x in new_ids if x in existing]
```

Other quadratics that hide well: string concatenation in a loop (each `+=` copies
the whole string), `list.pop(0)` in a loop (each pop shifts every element),
repeated `DataFrame.append` or `pd.concat` inside a loop (each call copies the
frame), and re-sorting inside a loop that could sort once outside it.

A change in complexity class is the only optimization that keeps paying as data
grows. Constant-factor work is worth doing after the class is right, not before.

### Tail Latency

```python
lat = sorted(samples)
p50 = lat[int(0.50 * len(lat))]
p95 = lat[int(0.95 * len(lat))]
p99 = lat[int(0.99 * len(lat))]
```

Averages are actively misleading: a mean of 60 ms is consistent with everything
being 60 ms, and equally consistent with 99% at 40 ms and 1% at 2.5 s. The second
system feels broken and the first feels fine.

Tail amplification is why this matters more than it seems. If a page makes 100
independent backend calls, the probability at least one hits the p99 path is
`1 − 0.99^100 ≈ 63%`. A one-in-a-hundred backend event becomes a two-in-three page
event. Fan-out systems live and die on p99, not p50.

Common tail causes: garbage collection pauses, cold caches, connection pool
exhaustion, lock contention, a retry storm, and one slow shard in a scatter-gather.

### Caching — After Measurement, Not Before

Caching is the most-reached-for and least-analyzed optimization. It is right when
reads greatly outnumber writes, the computation is expensive, and staleness is
tolerable. It is wrong when it hides an O(n²) you could have fixed, because now you
have a quadratic *and* an invalidation problem.

| Layer | Latency | Invalidation difficulty | Good for |
|---|---|---|---|
| Local in-process (LRU) | ~100 ns | Hard — per-instance drift | Small, hot, tolerant of staleness |
| Redis / Memcached | ~0.5 ms | Manageable, centralized | Shared derived data |
| CDN / edge | ~10 ms to origin-free | Purge APIs, TTL | Static and semi-static responses |
| Materialized view | Query-time | Refresh schedule | Expensive aggregates |

Always measure the hit rate. A cache at 40% hit rate on an expensive path is often
worse than no cache once you count the added latency, memory, and the class of bugs
where two instances disagree.

### Benchmark Honestly

```python
import statistics, time

def bench(fn, n=50, warmup=5):
    for _ in range(warmup):
        fn()                                   # let JIT/caches/pools settle
    times = []
    for _ in range(n):
        t0 = time.perf_counter()
        fn()
        times.append(time.perf_counter() - t0)
    return {
        "median": statistics.median(times),
        "p95": sorted(times)[int(0.95 * n)],
        "stdev": statistics.stdev(times),
    }
```

Use production-shaped data volume. Behavior is not linear in size: performance is
often fine until the working set stops fitting in memory or the index stops fitting
in the buffer pool, and then the curve bends sharply. A benchmark at 1,000 rows
predicts nothing about 10 million.

## Common Anti-Patterns

❌ **Optimizing from intuition** — a week spent on a 3% component.
✅ Profile first; let the flame graph pick the target.

❌ **"Make it faster" with no number** — no way to know when you are done.
✅ A percentile, a load level, and a workload, agreed up front.

❌ **Reporting averages** — hides the tail that users actually experience.
✅ p50/p95/p99, and alert on p99.

❌ **Caching before profiling** — masks the real defect and adds invalidation bugs.
✅ Find the hot path first; cache only what measurement justifies.

❌ **Micro-optimizing inside a loop that makes a network call per iteration.**
✅ Batch or eliminate the I/O; the loop body is noise next to it.

❌ **Benchmarking on toy data, once, cold.**
✅ Production-shaped volume, warmed, repeated, reported as a distribution.

❌ **Landing an unreadable optimization with no recorded before/after.**
✅ Record the measurement in the PR; if the gain is not measurable, revert it.

❌ **Assuming a rewrite in a faster language fixes it** — a 3× constant factor does
not rescue the wrong complexity class or an N+1 pattern.
✅ Fix the algorithm and the I/O shape first; the language rarely turns out to be
the constraint.

## Performance Optimization Checklist

- [ ] Target stated as percentile + load + workload before work starts
- [ ] Baseline measured and recorded
- [ ] Profile captured under realistic load, not synthetic ideal traffic
- [ ] Top contributor identified from the profile, not from a hunch
- [ ] Amdahl ceiling computed before committing to a rewrite
- [ ] Algorithmic complexity checked for accidental quadratics
- [ ] I/O count per request measured; N+1 patterns eliminated
- [ ] p50/p95/p99 reported; averages not used alone
- [ ] Tail causes investigated (GC, pools, locks, cold cache, slow shard)
- [ ] Cache hit rate measured where caching was added
- [ ] Benchmarks warmed, repeated, and run at production data volume
- [ ] Re-profiled after each change; ranking re-derived
- [ ] Before/after numbers recorded in the change description
- [ ] Regression guard in place so the win does not silently erode
