---
name: scenario-composer
description: Compose deterministic DSDS simulation scenarios from resilience hypotheses, load-test goals, or failure drills. Use when defining workload plus fault plus invariant bundles, built-in presets, and chaos experiments with reproducible seeds and explicit pass/fail criteria.
---

# Scenario Composer

## Overview

Design reproducible scenarios that test one clear system behavior at a time. Package each scenario with deterministic timing, explicit hypotheses, and measurable success criteria.

## Workflow

1. Define experiment intent
- Write one hypothesis in observable terms.
- Choose the primary target metric (`p99 latency`, `error rate`, `recovery time`, or `cost`).

2. Freeze deterministic controls
- Set `seed`, `simulationDuration`, and `warmupDuration`.
- Avoid changing more than one major variable per scenario version.

3. Compose traffic profile
- Select one workload pattern and justify it (`constant`, `poisson`, `spike`, `diurnal`, `bursty`, `sawtooth`, `replay`).
- Define request mix and base load.
- For scale tests, define the step-up schedule and stop condition.

4. Compose failure and resilience conditions
- Inject the minimum fault set needed to test the hypothesis.
- Specify timing mode (`deterministic`, `probabilistic`, `conditional`) and fault duration.
- Include resilience controls relevant to the scenario (retry, breaker, bulkhead, rate limit).

5. Define checks and expected outcomes
- Add invariants and SLO checks that can fail the run.
- Record expected qualitative behavior (for example, queue growth at gateway before API timeout cascade).

6. Deliver scenario package
- Provide scenario name and intent, topology deltas (or full config), workload config, fault list, invariants, and pass/fail rubric.

## Scenario quality rules

- Keep each scenario focused on one dominant failure pattern.
- Separate baseline and stressed variants.
- Reuse seeds when comparing design alternatives.
- Prefer deterministic schedules for regression suites.

## References

- Read `references/scenario-patterns.md` for templates, built-in mappings, and anti-pattern guardrails.
- Use these repo sources:
- `canonical-catalogue/DSDS Canonical Catalogue - scenarios to ship.csv`
- `canonical-catalogue/DSDS Canonical Catalogue - Failure modes & propagation semantics.csv`
- `canonical-catalogue/DSDS Canonical Catalogue - Patterns for scenario generation.csv`
- `planning/IMPLEMENTATION_PLAN.md` (Phase 7)
