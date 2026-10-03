---
name: perf-lab
description: Diagnose and improve performance with measurements. Use when the user asks about slow code, latency, throughput, memory, bundle size, database query cost, rendering jank, profiling, benchmarking, or optimization. Do not use for correctness bugs unless the main symptom is performance.
---

# Perf Lab

Optimize only after creating a measurement loop.

## Workflow

1. Define the target metric: latency, throughput, memory, CPU, query count, bundle size, render frames, or startup time.
2. Build a baseline using the repo's tools first: benchmark, profiler, logs, trace, query plan, browser performance panel, or a focused script.
3. Reproduce the slow path with representative data.
4. Rank hypotheses by likely impact and cost.
5. Change one variable at a time.
6. Compare before/after numbers and preserve behavior with tests where possible.

## Common Checks

- Accidental N+1 queries or missing indexes.
- Repeated parsing, serialization, regex, or filesystem work.
- Unbounded loops, deep copies, or needless allocations.
- Chatty network calls or waterfall loading.
- Large client bundles, hydration cost, and expensive renders.
- Cache invalidation that is too broad or too sticky.

## Output

Include:

- Baseline command and result.
- Hypotheses considered.
- Changes made or recommended.
- After result.
- Tradeoffs and remaining bottlenecks.

If measurement is blocked, state the missing fixture, traffic shape, or profiler
access instead of guessing.
