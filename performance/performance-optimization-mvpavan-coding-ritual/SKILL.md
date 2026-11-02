---
name: performance-optimization
description: Use for measured latency, throughput, memory or cost problems, profiling, or explicit resource targets. Skip prose optimization and speculative tuning.
---

# Performance Optimization

Improve a named user outcome with comparable evidence. Prose shortening and
ordinary cleanup are outside this skill. A newly introduced regression whose
cause is the main question is a bug. To fix it, route to the bug-fix playbook:
at top level return to `mvp-mode`; inside a delegated task, report that route to
the parent. For the diagnosis alone, use `systematic-debugging`.

1. Define the relevant metric, workload and target. If unclear, propose the
   measurement or ask about the consequential tradeoff before tuning code.
2. Capture a baseline with representative data, cache state, concurrency and
   environment. Repeat enough to estimate variability for the decision; use
   percentiles when the service target concerns tail latency. Record the command,
   conditions and results rather than assuming a fixed repeat count proves significance.
3. Locate the material cost using existing measurements, focused instrumentation
   or profiling. Code inspection can suggest candidates; measurements determine
   whether they matter. Use `references/measurement-recipes.md` for unfamiliar
   tools and `references/frontend-performance.md` for browser performance.
4. Change one attributable factor where practical. For an inseparable set, explain
   the coupling. Preserve required semantics, freshness, safety and accessibility.
5. Compare under the same conditions and run applicable correctness checks. Keep
   changes whose benefit justifies their complexity; remove only your ineffective
   experimental edits, preserving other work. A result within noise is inconclusive,
   not evidence of a speedup. Record cost/latency/memory tradeoffs explicitly.

Keep a compact attempt record with baseline → result, decision and reason so failed
experiments are not repeated after context recovery. Persist it in the task/report
when the work needs handoff, not as an extra artifact for every tiny experiment.

For a material recurring risk, add an economical regression guard: query counts,
bounded allocations or a controlled benchmark, using existing tooling. Scale its
cost to the risk; avoid flaky wall-clock assertions and unnecessary frameworks.
Report measured outcomes, applicable checks and limits. Performance improvement
does not excuse a correctness regression or authorize unrelated edits.
