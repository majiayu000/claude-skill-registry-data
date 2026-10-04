---
name: engineering-databricks-pipelines
description: Build reliable Databricks pipelines on the lakehouse — Delta Lake tables, MERGE and time travel, Delta Live Tables / Lakeflow declarative pipelines, Unity Catalog governance, Photon, Auto Loader ingestion, and cluster/job sizing. Use when building Databricks jobs or DLT pipelines, working with Delta tables, ingesting with Auto Loader, or organizing Unity Catalog.
---

# Engineering Databricks Pipelines

## When to use

- Building Databricks jobs, notebooks, or Delta Live Tables (DLT) pipelines.
- Working with Delta Lake (MERGE, OPTIMIZE, time travel, schema evolution).
- Ingesting files incrementally with Auto Loader.
- Organizing data under Unity Catalog (catalog.schema.table) and sizing clusters.
- Do NOT use for generic Spark tuning (use `optimizing-pyspark-jobs`).

## Workflow

```
- [ ] Model tables as Delta under Unity Catalog (catalog.schema.table)
- [ ] Ingest raw with Auto Loader (incremental, schema-tracked)
- [ ] Transform in medallion layers (bronze -> silver -> gold)
- [ ] Use MERGE for idempotent upserts; OPTIMIZE/Z-ORDER for read speed
- [ ] Right-size the cluster/job; enable Photon for SQL-heavy work
```

1. **Delta + Unity Catalog** are the defaults: ACID tables with governance,
   lineage, and access control. Use three-level names `catalog.schema.table`.
2. **Auto Loader** (`cloudFiles`) ingests new files incrementally and tracks
   schema, avoiding full re-lists of cloud storage.
3. **Medallion layers** — bronze (raw), silver (cleaned/conformed), gold
   (aggregated marts) — keep transformations testable and replayable.
4. **MERGE** makes loads idempotent; **OPTIMIZE** + **Z-ORDER** on filter columns
   speed reads.

## Patterns

**Idempotent upsert with Delta MERGE:**

```python
from delta.tables import DeltaTable
(DeltaTable.forName(spark, "main.sales.fct_orders").alias("t")
   .merge(updates.alias("s"), "t.order_id = s.order_id")
   .whenMatchedUpdateAll()
   .whenNotMatchedInsertAll()
   .execute())
```

**Auto Loader ingestion (bronze):**

```python
(spark.readStream.format("cloudFiles")
   .option("cloudFiles.format", "json")
   .option("cloudFiles.schemaLocation", "/chk/orders_schema")
   .load("/landing/orders")
 .writeStream.option("checkpointLocation", "/chk/orders")
   .toTable("main.sales.bronze_orders"))
```

**DLT / declarative pipeline** — define expectations that quarantine or drop bad
rows automatically:

```python
import dlt
@dlt.table
@dlt.expect_or_drop("valid_id", "order_id IS NOT NULL")
def silver_orders():
    return dlt.read_stream("bronze_orders").dropDuplicates(["order_id"])
```

**Maintain tables:** `OPTIMIZE main.sales.fct_orders ZORDER BY (customer_id)`, and
`VACUUM` old files past the retention window.

## Common pitfalls

- **Overwriting instead of MERGE** for updates — loses history and duplicates on
  retry; use MERGE or partition overwrite.
- **Skipping OPTIMIZE** on streaming/append tables — small-file explosion slows
  reads; schedule OPTIMIZE (or use predictive/auto optimize).
- **`VACUUM` with a too-short retention** — breaks time travel and running readers;
  keep the default retention unless you understand the impact.
- **Not enabling Photon** for SQL/ETL-heavy jobs — leaves significant speed on the
  table.
- **Oversized always-on clusters** — use job clusters that spin up per run and
  autoscale; reserve all-purpose clusters for interactive work.
- **Ignoring Unity Catalog** — managing raw paths loses lineage and access control.
