---
name: performance
description: Improve a measured bottleneck under representative workload. Triggers on "webperf", "慢".
---

# Performance Optimization

## When to use

- Improve a measured bottleneck under representative workload.

**Not for:** debugging for unexplained failures; cost-optimization for spending.

## Steps

1. Define the slow operation and target; record workload, environment and measured baseline.

2. Profile and identify dominant CPU, I/O, query, rendering, network or contention costs.

3. Change one justified cause while preserving behavior; bound cache size, invalidation and concurrency where relevant.

4. Compare under the same conditions, inspect variance and regressions, and retain only justified improvements.

## Verify

- Comparable before/after measurements exist; correctness and resource regressions are checked.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [human-audit.md](../../../references/human-audit.md) — document consent, readability and human review.
- [references/bottlenecks.md](references/bottlenecks.md) — symptom→cause decision tree, frontend/backend bottleneck tables, Core Web Vitals targets, performance budgets
- [references/anti-patterns.md](references/anti-patterns.md) — N+1, unbounded fetching, image optimization, re-renders, bundle splitting, caching (with code examples)
- [references/database-performance.md](references/database-performance.md) — DB-specific: EXPLAIN plan reading, index maintenance, slow-query analysis, N+1 detection, query anti-patterns, connection pooling
- [references/sql-optimization.md](references/sql-optimization.md) — SQL-design optimization: composite/covering/partial index strategy, missing-vs-unused index audit, cursor vs offset pagination, materialized views, partitioning
