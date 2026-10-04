---
name: game-performance-budget
description: Use when defining or reviewing game frame-time, memory, loading, network, CPU, GPU, allocation, or thermal budgets against captured measurements and target hardware tiers.
version: 0.1.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [engine-agnostic]
  versions: [any]
  platforms: [windows, macos, linux, console, mobile, web]
metadata:
  studio:
    type: gate
    lifecycle_stage: verify
    risk_level: read-only
    packs: [production-design-liveops]
    side_effects: none
    artifact: performance-budget-report.json
    required_evidence: [target-hardware, measurement-method, observed-metrics, budget-thresholds]
    owner: HoaTV Studio
    reviewer: null
    maturity: beta
    last_reviewed: 2026-08-08
    provenance:
      derived_from: none
      patterns_from: [registry/capabilities.yaml production catalog, build-and-runtime-verification]
      copied_text: none
---
# Game Performance Budget

## Overview
Compare reproducible performance measurements with explicit budgets instead of treating a fast developer machine or average frame rate as proof.

## When to use
Use for milestone gates, optimization reviews, target-hardware qualification, regression checks, memory reviews, loading tests, and network performance budgets.

## When NOT to use
Do not use to guess performance without captures, to optimize before a measured bottleneck, or to certify hardware that was not tested.

## Required inputs and context discovery
Collect build ID, scene or scenario, target hardware tier, quality settings, warm-up method, capture duration, measurement tool, percentile metrics, memory categories, loading phases, network conditions, and thresholds.

## Safety and risk level
Read-only analysis. Profiling unavailable hardware or builds is `BLOCKED`; estimates may be `Unverified` but never PASS.

## Workflow
1. Define budgets per target hardware tier and gameplay scenario.
   Completion criterion: units, thresholds, and allowed variance are explicit.
2. Validate capture identity and measurement method.
   Completion criterion: build, settings, warm-up, duration, and profiler source are recorded.
3. Compare observed percentiles and peaks with each budget.
   Completion criterion: every metric reports target, observed value, delta, and verdict.
4. Attribute exceeded budgets to measured subsystems or mark attribution unresolved.
   Completion criterion: bottleneck claims cite profiler evidence rather than intuition.
5. Define optimization experiments and regression gates.
   Completion criterion: each action includes a metric, target, owner, and retest scenario.

## Evidence and output contract
Produce `performance-budget-report.json` with build and hardware identity, scenarios, targets, observations, deltas, verdicts, profiler artifacts, limitations, and retest actions.

## Handoff contract
Record failing tiers, worst scenarios, capture paths, suspected subsystems, known measurement noise, owners, and exact retest commands or steps.

## Pitfalls and anti-rationalization
- Average FPS hides spikes; use percentiles and peaks.
- Editor measurements do not certify player builds.
- One hardware tier cannot stand in for another.
- Missing captures remain `BLOCKED`, not estimated PASS.

## Verification checklist
- [ ] Build, hardware, settings, and scenarios are exact.
- [ ] Budgets include units and thresholds.
- [ ] Observations cite profiler artifacts.
- [ ] Percentiles and peaks are reported where relevant.
- [ ] Retest actions preserve the same measurement method.

## References and scripts
Use the bundled [scripts/performance_budget.py](scripts/performance_budget.py) for normalized budget comparisons and project profilers for captures. The helper does not launch or profile a live build.
