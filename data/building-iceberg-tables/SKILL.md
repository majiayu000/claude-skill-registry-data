---
name: building-iceberg-tables
description: Design and operate Apache Iceberg tables — partitioning and hidden partitioning, partition/schema evolution, snapshots and time travel, compaction and small-file cleanup, and MERGE/upsert for lakehouse tables on Spark, Flink, Trino, or Snowflake. Use when creating or maintaining Iceberg tables, choosing partitioning, evolving schema/partitions, or fixing small-file and metadata bloat.
---

# Building Iceberg Tables

## When to use

- Creating or maintaining Apache Iceberg tables on a lakehouse.
- Choosing partitioning, or evolving partitioning/schema without rewrites.
- Managing snapshots, time travel, compaction, and small files.
- Do NOT use for Delta-specific work (use `engineering-databricks-pipelines`).

## Workflow

```
- [ ] Partition by query filter columns; use hidden partition transforms
- [ ] Use MERGE for idempotent upserts
- [ ] Schedule compaction (rewrite_data_files) to fix small files
- [ ] Expire old snapshots + remove orphan files to control metadata/storage
- [ ] Evolve partitioning/schema by field ID (no data rewrite)
```

1. **Partition on filter columns** using hidden partition transforms
   (`days(ts)`, `bucket(N, id)`), so queries prune without users adding derived
   partition columns.
2. **Idempotent writes** via `MERGE INTO` keyed on the business key.
3. **Compact regularly** — streaming/small-batch writes create many small files;
   `rewrite_data_files` restores read performance.
4. **Maintain metadata** — expire old snapshots and remove orphan files, or
   snapshot history and storage grow without bound.
5. **Evolve freely** — Iceberg tracks columns/partitions by ID, so add/drop/rename
   and even partition-spec changes need no data rewrite.

## Patterns

**Create with hidden partitioning + MERGE upsert:**

```sql
CREATE TABLE lake.db.orders (order_id BIGINT, customer_id BIGINT, amount DECIMAL, ordered_at TIMESTAMP)
USING iceberg PARTITIONED BY (days(ordered_at));

MERGE INTO lake.db.orders t USING staging s ON t.order_id = s.order_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
```

**Maintenance (Spark procedures):**

```sql
CALL lake.system.rewrite_data_files('db.orders');       -- compact small files
CALL lake.system.expire_snapshots('db.orders', TIMESTAMP '2026-08-01 00:00:00');
CALL lake.system.remove_orphan_files(table => 'db.orders');
```

**Time travel** — read a prior snapshot for audit or recovery:
`SELECT * FROM lake.db.orders VERSION AS OF <snapshot_id>`.

**Partition evolution** — `ALTER TABLE ... ADD PARTITION FIELD bucket(16, customer_id)`
applies to new data only; old data stays valid.

## Common pitfalls

- **No compaction on streaming tables** — small-file explosion tanks read speed.
- **Never expiring snapshots** — metadata and storage grow unbounded; schedule
  expiry within your time-travel retention.
- **Over-partitioning** (e.g. by hour on low volume) — too many tiny partitions;
  match granularity to data size.
- **Adding explicit derived partition columns** — defeats the point of hidden
  partitioning; use transforms.
- **Blind overwrite instead of MERGE** — loses idempotency; MERGE by key.
- **Removing orphan files with a too-short window** — can delete files in-flight
  writers still need; use a safe cutoff.
