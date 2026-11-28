---
name: performance-investigation
description: Measurement-first performance work — baseline, profile, fix by leverage (do less work → cache → parallelize → tune constants), verify with the same measurement. Use for any "make it faster", "why is this slow", latency/memory/CPU investigation, timeout or p95 regression, or before adding caching, memoization, indexes or parallelism on intuition. Not for reviewing new code for complexity-class mistakes (see perf-sanity).
---

# Performance Investigation

Weak performance work looks like: read the code → spot something that "looks slow" → add a cache or parallelise it → declare it faster. Strong performance work is a measurement loop: nothing is edited until a number exists, and nothing is called an improvement until the same number moves. Do not skip stages.

## 1. Define the metric and record the baseline

Pick ONE number that captures the complaint: p95 latency of endpoint X, wall time of job Y, MB of heap after Z. Write down the exact command that measures it and run it at least 5 times on the same input; record median and spread. If the spread is larger than the improvement you expect, fix the measurement first (warm-up runs, prod build, bigger input, quieter machine) — a noisy baseline proves nothing either way.

Measure on an input representative of the complaint, not the test fixture: a 10-row run says nothing about 100k rows. Where cheap, also run at 10× the input — how the time grows (linear, quadratic) locates the problem faster than any profiler.

Beware benchmark lies: cold vs warm caches, dev-mode builds, first-iteration JIT/warm-up, laptop-vs-prod hardware, and a metric that doesn't match the complaint (CPU time when the user feels wall time).

If the baseline already meets the target, report that and stop.

## 2. Find where the time goes — waiting or working?

First split wall time from CPU time (`time`, a timer around the call, request duration vs CPU). Wall ≫ CPU means the process is waiting — on a query, a network call, a lock, a disk — and a CPU profiler will show nothing useful; use query logs + EXPLAIN, traces, or timestamps around each I/O call. Wall ≈ CPU means compute: CPU profiler or flamegraph. Memory complaints get a heap snapshot or allocation profile.

The bottleneck is a measurement result, not an opinion: name the frame, query, or call and the share of time it accounts for. Expect one or two items to dominate. A flat profile usually means per-item overhead in a loop (allocation, serialization, sync I/O) or doing N× more work than the task needs.

## 3. Fix in order of leverage, one change at a time

1. **Do less work** — N+1 queries → batch/join; O(n²) scan → index/map lookup; recomputing invariants inside loops → hoist; fetching/serializing fields nobody reads → trim.
2. **Do work once** — cache/memoize, only with a written invalidation story; a stale cache is a correctness bug traded for speed.
3. **Do work elsewhere/later** — off the critical path: lazy, background, stream the first byte early.
4. **Do work in parallel** — after the above; a parallelised N+1 is still N+1.
5. **Tune constants last** — micro-optimisations only with a profiler receipt that the line is hot.

Apply one change, rerun the stage-1 command, record the number. If it didn't move, revert that change before trying the next — never keep an "optimisation" that bought nothing, and never stack two unmeasured changes.

## 4. Verify with the SAME measurement, then check for damage

Rerun the exact baseline command under the same conditions. Then run the correctness suite — perf fixes break edge cases (stale cached data, reordered side effects, errors swallowed in parallel code).

## Bottleneck signatures (check before deep-diving)

- Latency scales with item count → N+1 (queries, HTTP calls, file reads per item).
- Slow only in prod → missing index at prod data volume, cold cache, network hops dev lacks.
- Grows over time → leak (unbounded cache/listener/array), fragmentation, log growth.
- Occasional spikes → GC pauses, lock contention, batch jobs sharing resources, retry storms.
- "Fast function, slow system" → serialization at boundaries, chatty protocols, sync-over-async.

## Report

When the deliverable is a findings list or a plan rather than a fix you measured, the measurement is the first item: name the baseline you would take (which request, which metric, which command) and say the same measurement is re-run after each change. Order the findings by their measured or estimated share of the cost and say how you attributed it (which instrument, or which arithmetic); mark any attribution you could not make from the material as unverified. Name which proposed fixes are constant-tuning or caching that you would defer until the underlying work is reduced.

Include: the measurement command; baseline and final numbers with units, run count, spread and conditions ("p95 420ms → 95ms, median of 5, warm, prod build, dataset X"); what the profile showed; each change tried with its measured effect, including reverted ones; and the trade made — readability, memory, or freshness for speed. If the target is not met, say what remains and where the remaining time goes.
