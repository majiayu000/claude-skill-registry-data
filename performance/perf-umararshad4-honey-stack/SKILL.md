---
name: perf
description: "Performance engineering: profile to find the real bottleneck, fix the hot path, add caching, and load-test with before/after numbers. Use when something is slow, costs too much, or misses an SLO. Measure first."
license: MIT
metadata:
  reviewed: "2026-10-18"
  sources: "honey-stack research 2026-10-18 (USE/RED methods, profilers per stack, caching, k6 load testing, percentiles); cursor/plugins 4dd1d05818d19792e7cd6e818f1667f95f7e1dbe pstack/skills/benchmark-checklist/SKILL.md. Motion details owned by frontend references."
---

# perf

Make it faster, but only where it's actually slow. The bottleneck is almost never where intuition says — measure, fix the hot path, prove the win.

Before reporting a measured speedup or choosing between implementations, read [the benchmark checklist](references/benchmark-checklist.md). For stuttering application animations, read [motion performance](../frontend/references/motion-performance.md) and record frames/long tasks on the target device; source inspection alone cannot establish smoothness.

## Discipline
1. **Baseline first** — numbers + environment + input, before any change.
2. **Profile, don't guess.** Find the real bottleneck (`references/profiling.md` has the tool per stack).
3. **Amdahl's law:** a path that's 5% of total time caps your gain at 5%. Optimize the top of the profile only.
4. **Verify** with before/after on the same workload; keep the change only if the delta beats noise. Report **p50/p95/p99**, not the mean.
5. **Stop at the target.** Hit the SLO, document the baseline and win, don't chase diminishing returns.

**Premature when:** no measurement, no user-facing problem, no SLO breach, not a hot path. Correctness and clarity first.

## Find the bottleneck
- **USE** (resources): for CPU/memory/disk/network/DB pool check **U**tilization, **S**aturation (queue/wait), **E**rrors.
- **RED** (services): per endpoint track **R**ate, **E**rrors, **D**uration distribution.
- RED shows the symptom; USE finds the saturated resource behind it. (Both reappear in `observability`.)

## Profiling
Pick CPU vs memory vs allocation profiling to match the symptom (high CPU vs OOM vs GC pauses). Tools per stack — Node (`--cpu-prof`/`--heap-prof`, 0x, clinic), Python (**py-spy** attaches to a live process, cProfile, Scalene, memray), Go (`pprof`, `go tool trace`), JVM (async-profiler), Linux (`perf` + flamegraphs, eBPF, off-CPU analysis): `references/profiling.md`.

## Common backend bottlenecks
N+1 and slow queries (usually #1 — see the `database` skill), missing caching, serialization cost, synchronous/blocking I/O on the event loop, O(n²) algorithms, unbounded concurrency, GC pressure / memory leaks, serverless cold starts. Fixes in `references/bottlenecks.md`.

## Caching
Layers closest-first: CDN/edge → HTTP cache headers (`Cache-Control`, `ETag`, `stale-while-revalidate`) → in-process LRU (bounded) → Redis/memcached → DB (materialized views). Invalidate by TTL + jitter, write-through, or event/tag; protect against stampede with single-flight. Never cache secrets/PII in a shared cache, or anything where staleness causes a correctness bug (balances, inventory). `references/caching.md`.

## Load & stress testing
Tools: **k6** (default), Gatling, Locust, wrk2, vegeta. Types: smoke → load → stress → spike → **soak** (hours, catches leaks). Define the SLO before testing (e.g. "p99 < 300ms at 2k rps"). **Averages lie** — one slow request per thousand ruins p99 but barely moves the mean; use coordinated-omission-aware tools (wrk2, k6). Ramp to the knee (latency rises sharply / throughput plateaus) to find capacity. `references/load-testing.md`.

## Confirm before (never on your own)
- Load/stress testing anything **live or shared** — it can take down prod and dependencies. Use a dedicated/staging env, coordinate with on-call, never point a stress test at a third-party API.
- Profiling or `EXPLAIN ANALYZE` that adds prod overhead or mutates data.

Done when: the bottleneck is identified from a profile, the fix is on the hot path, and before/after numbers (at p95/p99) show the win against the target.
