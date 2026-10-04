---
name: performance
description: "Improves measured performance while preserving correctness, reliability, and maintainability."
---

# Skill: performance

## Purpose

Improve performance only when it matters, and without breaking correctness.

## Rules

- Correctness comes first.
- Identify the bottleneck before optimizing.
- Prefer measurement over intuition.
- Do not add caching unless invalidation is clear.
- Do not trade data integrity or safety for speed.
- Do not make code clever merely to save imaginary nanoseconds.

## Common Bottlenecks

Check for:

- repeated I/O;
- N+1 queries;
- unbounded memory growth;
- unnecessary allocations;
- blocking work in async/event-loop contexts;
- inefficient serialization;
- overly broad database queries;
- missing indexes when schema context confirms it;
- excessive polling;
- hardware update intervals that cause instability or wear.

## Optimization Workflow

1. Define performance goal.
2. Identify current behavior.
3. Measure or reason from evidence.
4. Make focused change.
5. Validate correctness.
6. Validate performance impact if possible.
7. Document tradeoffs.

## Caching Rules

Add caching only when:

- correctness is preserved;
- invalidation is understood;
- cache size is bounded or controlled;
- stale data behavior is acceptable;
- failure behavior is defined;
- observability exists when needed.

## Reporting

Report:

- bottleneck;
- change;
- correctness validation;
- performance validation;
- tradeoffs/risks.
## Extended References


For deeper work, read:

- `../../engineering/18_performance_philosophy.md`
