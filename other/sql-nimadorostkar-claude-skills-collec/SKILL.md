---
name: sql
description: Use when writing or optimizing SQL. Covers query planning, indexing strategy, window functions, CTEs, transaction isolation, and reading EXPLAIN output.
metadata:
  category: languages
  version: 1.0.0
  tags: [sql, query-optimization, indexing, explain, transactions]
---

# SQL

## Purpose

Write SQL that the planner can execute efficiently, and read execution plans well enough to know why it did not.

## When to Use

- Writing non-trivial queries: aggregations, window functions, recursive CTEs.
- Diagnosing a slow query.
- Designing indexes for a known access pattern.
- Choosing a transaction isolation level.
- Reviewing migrations for lock risk.

## Capabilities

- Query authoring: joins, CTEs, window functions, lateral joins, upserts.
- Index design: composite ordering, covering indexes, partial indexes.
- Plan reading: `EXPLAIN (ANALYZE, BUFFERS)` and the shapes that signal trouble.
- Isolation levels and the anomalies each one permits.
- Safe migrations: concurrent index builds, backfills, lock avoidance.

## Inputs

- The query, the schema, and the row counts of the tables involved.
- Existing indexes.
- The actual execution plan, not a guess about it.

## Outputs

- A rewritten query, an index, or both — with a before/after plan.
- Migration statements that do not hold long locks.

## Workflow

1. **Get the plan** — `EXPLAIN (ANALYZE, BUFFERS)`. Never optimize a query you have not profiled.
2. **Find the expensive node** — Look for sequential scans on large tables, nested loops with high row counts, and estimates that diverge from actuals by an order of magnitude.
3. **Fix the cause** — Bad estimate means stale statistics. Sequential scan on a selective filter means a missing index. High row counts through a join means the filter is applied too late.
4. **Index deliberately** — Column order in a composite index is equality columns first, then the range or sort column.
5. **Re-measure** — Confirm with a fresh plan, and check that write throughput did not regress.

## Best Practices

- An index on `(a, b)` serves queries filtering on `a`, and on `a` and `b` — but not on `b` alone.
- Wrapping an indexed column in a function (`WHERE lower(email) = ...`) disables the index unless the index is on the expression.
- `SELECT *` in application code prevents index-only scans and breaks when the schema changes.
- Never run an unbounded `UPDATE` or `DELETE` on a large table in one transaction — batch it.
- `CREATE INDEX CONCURRENTLY` in production; the plain form locks writes for the duration.
- Prefer keyset pagination (`WHERE id > :last`) over `OFFSET` — offset cost grows linearly with page depth.

## Examples

**Window function instead of a correlated subquery:**

```sql
-- Latest order per customer, one pass.
SELECT customer_id, order_id, placed_at, total_cents
FROM (
  SELECT
    o.customer_id,
    o.id AS order_id,
    o.placed_at,
    o.total_cents,
    ROW_NUMBER() OVER (
      PARTITION BY o.customer_id
      ORDER BY o.placed_at DESC
    ) AS rn
  FROM orders o
  WHERE o.placed_at >= now() - interval '90 days'
) ranked
WHERE rn = 1;
```

**Index matching the access pattern:**

```sql
-- Query: WHERE tenant_id = $1 AND status = 'open' ORDER BY created_at DESC LIMIT 50
CREATE INDEX CONCURRENTLY idx_tickets_tenant_open_recent
  ON tickets (tenant_id, status, created_at DESC)
  WHERE deleted_at IS NULL;
```

## Notes

- The partial index above only covers live rows, keeping it small and hot in cache.
- `READ COMMITTED` (the default in PostgreSQL) permits non-repeatable reads. If a transaction reads a row, decides, and writes based on that decision, you need `REPEATABLE READ` plus retry logic, or `SELECT ... FOR UPDATE`.
- Statistics drift after bulk loads. Run `ANALYZE` before benchmarking anything.
