---
name: kit-performance
description: Improve the speed or resource use of existing code by measuring first, finding the actual hotspot, changing it, and measuring again with the behavior kept the same. Use when the user reports that something is slow, uses too much memory or CPU, or asks to optimize, speed up, or profile code. Do not use for failures or wrong results (use kit-debugging), for restructuring without a performance goal (use kit-refactoring), or for database query review alone (use the matching review skill).
---

# Performance

## 1. Define the target

- Identify what is slow (an endpoint, a job, a function, a build), the workload that shows it, and the goal (latency, throughput, memory). If the user gave no numbers, state the assumption.
- Read the code path end to end before guessing. Note callers and tests that pin its behavior.

## 2. Measure a baseline

- If the project already has a benchmark (`npm run bench`, `make bench`, `go test -bench`), run it unchanged first.
- Otherwise reproduce the slowness with a benchmark or timing harness that uses representative input: `go test -bench`, `pytest-benchmark` or `timeit`, `node --cpu-prof` or a small script with `performance.now()`, the database's `EXPLAIN ANALYZE` (it executes the statement: wrap writes in a transaction you roll back or use plain `EXPLAIN`, and never run it against production without approval).
- Profile instead of guessing: CPU profiles (`pprof`, `py-spy`, `--cpu-prof`), allocation profiles, query logs. Record the numbers and the environment.
- If you cannot measure, say so and stop at a hypothesis; do not ship speculative optimizations.

## 3. Change the hotspot

- Fix the largest measured cost first. Typical wins: removing repeated work in loops (N+1 queries, repeated parsing, recomputing in render), choosing a better algorithm or data structure (a set or map lookup instead of a linear scan), batching I/O, adding an index, streaming instead of loading everything, and caching only with a clear invalidation rule.
- Keep behavior the same: run the existing tests, and add a test for edge cases the optimization touches (empty input, duplicates, ordering).
- Prefer a simple change with most of the gain over a clever one with slightly more. Leave a short comment when the faster code is less obvious.

## 4. Measure again and report

Rerun the same benchmark under the same conditions. Report the baseline and new numbers, what changed and why it helped, test results, and remaining hotspots with their measured share. If the gain is within noise, say so and suggest reverting.

## Examples

- Use: "The /reports endpoint takes 4 seconds." "Speed up this CSV import." "Why does this job use 2 GB of memory?"
- Skip: "This endpoint returns the wrong total." (kit-debugging) "Clean up this module." (kit-refactoring)
