---
name: optimizing-snowflake-workloads
description: Reduce Snowflake cost and latency — right-size and auto-suspend warehouses, use multi-cluster for concurrency, apply clustering keys, read the Query Profile, exploit result/warehouse caching, and control credit spend. Use when Snowflake queries are slow or expensive, warehouses spill or queue, credits are high, or you need to size a warehouse.
---

# Optimizing Snowflake Workloads

## When to use

- Snowflake queries are slow, queue, or spill to remote storage.
- Credit/cost is higher than expected.
- Choosing warehouse size, multi-cluster settings, or clustering keys.
- Do NOT use for writing the SQL logic itself (use `optimizing-sql-queries`).

## Workflow

```
- [ ] Open the Query Profile: check partitions scanned, spilling, and pruning
- [ ] Right-size: scale UP for heavy single queries, OUT for concurrency
- [ ] Set auto-suspend low and auto-resume on
- [ ] Add clustering only to very large, selectively-filtered tables
- [ ] Verify with ACCOUNT_USAGE / WAREHOUSE_METERING history
```

1. **Read the Query Profile.** Key signals: "Partitions scanned vs total"
   (pruning), "Bytes spilled to local/remote storage" (warehouse too small), and
   the most expensive operator.
2. **Right-size the warehouse.** Scale **up** (bigger size) for one heavy query
   that spills; scale **out** (multi-cluster) for many concurrent queries that
   queue. Bigger warehouses cost more per second but can be cheaper if they finish
   proportionally faster.
3. **Auto-suspend + auto-resume** — you pay per running second. Set auto-suspend to
   ~60s so idle warehouses stop.
4. **Clustering keys** only on large tables filtered by a high-cardinality column;
   check `SYSTEM$CLUSTERING_INFORMATION` and beware reclustering cost.

## Patterns

**Right-sizing decision:** spilling to remote storage → scale up; queries
`QUEUED` under concurrency → add clusters (multi-cluster min>1) rather than a
bigger size.

**Separate warehouses per workload** (ELT vs BI vs ad-hoc) so a heavy job doesn't
starve dashboards and each can be sized/monitored independently.

**Exploit caching (free):**

- Result cache: identical query text + unchanged data returns instantly, no
  compute.
- Warehouse (local) cache: keep related queries on the same warehouse to reuse
  cached micro-partitions.

**Find cost drivers:**

```sql
select warehouse_name, sum(credits_used) as credits
from snowflake.account_usage.warehouse_metering_history
where start_time >= dateadd('day', -7, current_timestamp())
group by 1 order by 2 desc;
```

## Common pitfalls

- **Always-on warehouses** with no/high auto-suspend — the top source of wasted
  credits.
- **Scaling up for a concurrency problem** — a bigger warehouse doesn't fix
  queuing; add clusters instead.
- **Clustering small or low-selectivity tables** — reclustering costs more than it
  saves; only cluster large, selectively-filtered tables.
- **`SELECT *` in dashboards** — reads all columns' micro-partitions; select what
  you need.
- **One shared warehouse for everything** — noisy neighbors; split by workload.
- **Ignoring spilling** — remote spill silently multiplies runtime and cost.

## References

- [Snowflake cost monitoring queries](references/COST.md)
