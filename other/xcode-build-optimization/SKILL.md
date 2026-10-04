---
name: xcode-build-optimization
description: "Benchmark and improve Xcode clean, no-change, and edit-build latency; analyze compiler hotspots, script phases, target graphs, SwiftPM plugins, and measured rollback decisions."
---

# Evidence-based Xcode build optimization

## Inputs

Record exact build graph, source, toolchain, destination, workload, caches, baseline samples, user objective, and authorized changes.

## Rules

- **XBUILD-001 — Measure the right cost.** Separate elapsed wait from cumulative parallel work, and clean from no-op and edit builds.
- **XBUILD-002 — Preserve comparable evidence.** Keep commands, caches, dependencies, workload, and environment comparable; retain failures and spread.
- **XBUILD-003 — Inspect the critical path.** Use task dependencies and timelines before assuming the largest cumulative category limits elapsed time.
- **XBUILD-004 — Change real owners.** Fix source-owned settings, scripts, or package boundaries without disabling correctness checks or shipping requirements.
- **XBUILD-005 — Keep rollback available.** No recommended setting outranks measured regressions or compatibility. Retain non-performance changes only with an explicit rationale.

## Workflow

1. Capture a baseline and classify the bottleneck.
2. Use only the matching specialist references.
3. Apply authorized, reversible hypotheses and verify effective output.
4. Repeat the same workload and report gains, tradeoffs, or inconclusive evidence.

## Verify

Build the final candidate, run behavior tests, compare all measured categories, and inspect generated resources. Do not count a timing-summary parse failure as zero work.

## Output

Return baseline/after samples, elapsed deltas, uncertainty, changed files, and retained/reverted/blocked decisions.

## References

- [Build optimization orchestration](references/orchestration.md).
- [Clean, no-op, and edit-build benchmarks](references/benchmarking.md).
- [Compiler hotspots and source complexity](references/compiler.md).
- [Build settings, scripts, and dependency graphs](references/project.md).
- [SwiftPM graph, plugins, and generated code](references/packages.md).
- [Fix, compare, and report](references/verification.md).
