---
name: optimizing-bigquery-queries
description: Reduce Google BigQuery cost and runtime — partitioning and clustering, minimizing bytes processed, avoiding SELECT * and full scans, slot usage and reservations, approximate functions, and materialized views. Use when BigQuery queries are expensive or slow, bytes billed are high, a query scans full tables, or you need to size slots.
---

# Optimizing BigQuery Queries

## When to use

- BigQuery queries cost too much (bytes billed) or run slowly.
- A query scans full tables or ignores partitions.
- Choosing partitioning/clustering, or sizing slots/reservations.
- Do NOT use for query logic correctness (this assumes correct results).

## Workflow

```
- [ ] Estimate bytes: query validator or --dry_run BEFORE running
- [ ] Partition by date/timestamp; cluster by most-filtered columns
- [ ] Select only needed columns; filter on the partition column
- [ ] Replace exact-distinct/full scans with approx / incremental
- [ ] Materialize repeated aggregates
```

1. **Estimate first.** On-demand billing = bytes processed. Use the editor's
   validator or `bq query --dry_run` to see bytes billed before spending.
2. **Partition + cluster.** Partition large tables by date/timestamp; cluster by
   the columns you filter/join on most. Filtering on the partition column prunes
   scanned bytes dramatically.
3. **Read fewer columns.** BigQuery is columnar — `SELECT *` reads every column's
   bytes. List only what you need.
4. **Avoid full scans.** Filter on the partition column with literals/ranges (not
   wrapped in functions) so pruning applies.
5. **Approximate + materialize.** Use `APPROX_COUNT_DISTINCT` for big cardinality;
   use materialized views for common aggregates.

## Patterns

**Partitioned + clustered table:**

```sql
CREATE TABLE sales.orders
PARTITION BY DATE(ordered_at)
CLUSTER BY customer_id, status AS
SELECT ...;
```

**Prune-friendly filter** (keeps the partition column bare):

```sql
-- Good: prunes partitions
WHERE ordered_at >= '2026-01-01' AND ordered_at < '2026-02-01'
-- Bad: function on the column disables pruning
WHERE DATE(ordered_at) = '2026-01-15'
```

**Dry run to see cost:**

```bash
bq query --use_legacy_sql=false --dry_run 'SELECT ... FROM sales.orders WHERE ...'
```

**Slots:** on-demand gives per-query slots with fair scheduling; buy
reservations/editions for predictable heavy workloads and isolate ELT from BI with
separate reservations.

## Common pitfalls

- **`SELECT *`** — reads all columns' bytes; the most common cost mistake.
- **Function-wrapped partition filter** (`DATE(ts) = ...`) — disables pruning and
  scans the whole table.
- **No partitioning on large tables** — every query full-scans.
- **`COUNT(DISTINCT ...)` on huge columns** — expensive; use
  `APPROX_COUNT_DISTINCT` when exactness isn't required.
- **Re-running the same heavy aggregate** — cache with a materialized view or a
  scheduled summary table.
- **Ignoring the dry-run estimate** — surprise bills; always estimate first.
- **Cross-joins / unintentional fan-out** — explode bytes and slot time; check the
  execution graph.
