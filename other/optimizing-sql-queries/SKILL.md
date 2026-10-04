---
name: optimizing-sql-queries
description: Optimize slow analytical SQL by reading query/EXPLAIN plans, cutting scanned data, fixing join strategy, and using partitioning, clustering, and indexes across Postgres, Snowflake, BigQuery, Databricks/Spark SQL, and Redshift. Use when a query is slow, times out, costs too much, scans too many rows/bytes, or spills to disk.
---

# Optimizing SQL Queries

## When to use

- A query is slow, times out, or is expensive (bytes/credits/slots scanned).
- A dashboard or model run regressed after data grew.
- You see full-table scans, large shuffles, disk spills, or exploding row counts.
- Do NOT use for query _correctness_ bugs — this skill assumes results are correct.

## Workflow

```
- [ ] Read the actual query/EXPLAIN plan (not guesses)
- [ ] Find the dominant cost: scan, join, aggregation, or sort/spill
- [ ] Reduce data read (predicates, partition/cluster pruning, column pruning)
- [ ] Fix join strategy (order, keys, broadcast vs shuffle, skew)
- [ ] Re-measure and confirm the plan changed
```

1. **Get the plan.** Never optimize blind:
   - Postgres: `EXPLAIN (ANALYZE, BUFFERS) <query>`
   - Snowflake: Query Profile UI, or `SYSTEM$EXPLAIN_PLAN_JSON`
   - BigQuery: execution details / `--dry_run` for bytes billed
   - Spark/Databricks: `df.explain("formatted")` or the SQL plan tab
2. **Identify the dominant operator** by time/rows/bytes. Optimize that first;
   ignore cheap nodes.
3. **Reduce data scanned** before anything else — it usually dominates cost.
4. **Fix the join** only after the scan is minimal.
5. **Re-run the plan** and verify the change (row estimates, join type, pruning).

## Patterns

**Enable partition/cluster pruning** — push filters on the partition/cluster key
so the engine skips files. On BigQuery/Snowflake this is the single biggest lever.

```sql
-- Good: filter on the partitioning column with a literal/range so pruning applies
SELECT user_id, SUM(amount)
FROM orders
WHERE order_date >= '2026-01-01' AND order_date < '2026-02-01'  -- prunes partitions
GROUP BY user_id;
```

**Filter before joining, not after.** Reduce each side to the needed rows/columns
first so the join processes less data.

**Prefer explicit column lists over `SELECT *`** in columnar warehouses — reading
fewer columns reads fewer bytes.

**Choose the right join for the sizes.** A small dimension joined to a large fact
should broadcast (map-side) rather than shuffle. In Spark, let Adaptive Query
Execution pick, or hint `/*+ BROADCAST(dim) */`.

**Aggregate/pre-filter in a CTE** to shrink data before an expensive window or
join, rather than computing over the full table.

## Common pitfalls

- **Wrapping the partition key in a function** (`WHERE DATE(ts) = ...`) disables
  pruning — filter on a raw range instead.
- **Implicit type casts on join keys** (string vs int) force full scans and block
  index/pruning use — align types.
- **`SELECT DISTINCT` to hide a fan-out join** — fix the join grain instead; it is
  cheaper and correct.
- **`OR` across columns** often prevents index/pruning use — rewrite as `UNION ALL`
  or `IN`.
- **Optimizing a cheap node** — always target the dominant operator in the plan.
- **Chasing indexes on columnar warehouses** — Snowflake/BigQuery have no
  row-store indexes; use clustering/partitioning and result caching instead.

## References

- [Engine-specific tuning notes](references/ENGINES.md)
