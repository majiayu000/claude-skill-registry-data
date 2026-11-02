---
name: postgres-index-design
description: Evaluate PostgreSQL index choices against query patterns, write costs, selectivity, ordering, and real execution plans.
---

# Postgres Index Design

## Goal

Choose indexes that improve meaningful workloads without accumulating redundant or write-expensive structures.

## Inputs to inspect

Table schema and size, frequent queries, existing indexes, cardinality/selectivity evidence, and migration constraints.

## Workflow

1. Map critical WHERE, JOIN, ORDER BY, and GROUP BY patterns to candidate index keys and required ordering or included columns.
2. Inspect cardinality and selectivity, data skew, null frequency, and whether a partial or composite index matches the actual predicate.
3. Compare query plans and buffer usage before/after in a representative environment; include write/update cost and index size in the evaluation.
4. Check for overlapping indexes, redundant left-prefix coverage, uniqueness semantics, and constraints that must remain enforced.
5. Plan safe index creation/removal with lock and disk considerations; verify that the intended query benefits after statistics refresh.

## Validation checklist

- [ ] Each candidate index maps to a real query or integrity constraint.
- [ ] Composite column order matches predicate and ordering usage rather than intuition alone.
- [ ] Write amplification and storage cost are considered alongside read gains.
- [ ] Redundant indexes are removed only after dependency and workload review.
- [ ] Migration behavior is appropriate for the production database version and availability requirements.

## Required output

Deliver a query-to-index matrix, measured plan comparison, storage/write-cost estimate, and safe migration recommendation.

## Boundaries and failure handling

Do not add indexes to every filtered column automatically; do not drop a constraint-backed index as if it were ordinary optional acceleration.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
