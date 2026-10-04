---
name: apple-performance-cleanup
description: "Diagnose or improve SwiftUI responsiveness, startup, memory, energy, and hot paths. Use measurements and explicit behavior contracts before optimization or broad compaction."
---

# Apple performance and behavior-preserving cleanup

## Inputs

Identify the workload, affected devices/build configuration, observed cost, user-visible behavior, existing measurements, and change authority. Distinguish diagnosis from a requested implementation.

## Rules

- **PERF-001 — Establish a baseline.** Reproduce the workload and record toolchain, configuration, input size, device, and measurement method before comparing results.
- **PERF-002 — Fix demonstrated work.** Trace invalidation, layout, CPU, allocations, I/O, or contention. Do not ban APIs by name or claim an unmeasured percentage improvement.
- **PERF-003 — Preserve semantics.** Keep ordering, identity, cancellation, errors, stale/empty distinctions, persistence, and accessibility behavior intact.
- **PERF-004 — Bound resources.** Give tasks, observers, caches, buffers, logging, and polling a lifecycle and a resource limit appropriate to the workload.
- **PERF-005 — Prove two claims separately.** Behavior tests establish correctness; comparable measurements establish speed, memory, or energy effects.

## Workflow

1. Reproduce and classify the cost with the available profiler or trace.
2. Find the owner and smallest useful correction; state the expected mechanism.
3. Add or retain focused behavior tests before changing a hot path.
4. Measure before/after under comparable conditions and inspect regressions.
5. Stop when further reduction would weaken clarity, compatibility, or evidence.

## Verify

Compare representative and worst-reasonable workloads, repeated runs, memory after repeated entry/exit, and release-like builds where appropriate. Distinguish a structural reduction in work from a measured runtime improvement.

## Output

Report the bottleneck evidence, code change, preserved invariants, measurement method/results, and remaining uncertainty. Never replace unique tests or diagnostics merely to lower line count.

## References

Read the [playbook](references/performance-cleanup-patterns.md) for decisions, failure cases, and source links.

For trace-led runtime performance work, read the [focused reference](references/trace-led-performance.md).
