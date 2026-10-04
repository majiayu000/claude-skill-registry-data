---
name: codex-performance-goal
description: Use when the user wants measurable performance optimization, latency/cost/memory/throughput improvement, benchmark-driven tuning, evaluator-gated optimization, or a goal-mode performance loop; require a baseline, evaluator command or measurement protocol, pass/fail contract, reversible patches, and final evidence.
---

# Codex Performance Goal

Optimize performance only against an explicit evaluator. This is the native Codex adaptation of OMX `$performance-goal`: keep evaluator-gated progress, goal honesty, small reversible patches, and completion audit; replace `.omx/goals/performance` with repo-local benchmark artifacts or task/work-trace files when durable state is needed.

## Contract

- Do not optimize before a baseline and pass/fail contract exist.
- Define the metric: latency, throughput, memory, cost, bundle size, accuracy/latency tradeoff, or another measurable target.
- Prefer existing project benchmarks and profiling scripts.
- Keep changes small and reversible.
- Record every measurement with command, environment, inputs, and result.
- Do not mark a goal complete until the evaluator passes and regression checks are clean.

## Workflow

1. Clarify objective and metric.
2. Find or create the evaluator: command, benchmark script, profiling procedure, or reproducible manual measurement.
3. Capture baseline before edits.
4. Identify bottleneck hypotheses from evidence.
5. Apply one optimization at a time.
6. Rerun evaluator and regression tests.
7. Keep, revert, or revise based on evidence.
8. Finish with before/after results and residual risk.

## Goal Mode

When Codex goal tools are active, treat the active goal as focus/accounting only. Call `update_goal({status:"complete"})` only after evaluator pass plus completion audit proves the whole objective.

## Output Shape

- Objective and metric
- Evaluator contract
- Baseline
- Changes tried
- Final measurement
- Regression checks
- Kept/reverted decisions
- Residual risk and follow-up

## References

Read `references/performance-evidence-checklist.html` for measurement quality gates.
