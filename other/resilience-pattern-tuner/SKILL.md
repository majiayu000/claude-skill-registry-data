---
name: resilience-pattern-tuner
description: Tune DSDS resilience controls including retries, deadlines, circuit breakers, rate limits, bulkheads, and load shedding. Use when balancing availability, latency, and resource protection under failure and saturation conditions.
---

# Resilience Pattern Tuner

## Overview
Adjust resilience controls to reduce cascade risk without causing retry storms or unnecessary rejections. Produce configuration recommendations tied to measurable outcomes.

## Workflow

1. Establish baseline behavior
- Record current latency, error, and queue metrics under normal and stressed loads.
- Identify whether failures are timeout-dominated, saturation-dominated, or dependency-dominated.

2. Tune timeout and retry chain
- Set bounded end-to-end deadlines.
- Tune retries with exponential backoff and jitter.
- Prevent retries from exceeding user-visible deadlines.

3. Tune isolation controls
- Configure circuit breaker thresholds and recovery windows.
- Configure bulkhead limits per critical path.
- Configure rate limits and load shedding policy.

4. Evaluate tradeoffs
- Measure changes in `p99`, error rate, and throughput.
- Check for side effects (false opens, early shedding, starvation).

5. Deliver tuning profile
- Provide settings, rationale, and expected impact.
- Include rollback conditions if regression appears.

## Output format
1. `Baseline issues`
2. `Proposed settings`
3. `Expected impact`
4. `Validation plan`
5. `Rollback criteria`

## References
- Read `references/resilience-tuning-matrix.md` for parameter heuristics.
- Use these repo sources:
- `planning/IMPLEMENTATION_PLAN.md` (Phase 5)
- `docs/04-distributed-systems-and-failures.md` (Chapter 24)
- `canonical-catalogue/DSDS Canonical Catalogue - Patterns for scenario generation.csv`
