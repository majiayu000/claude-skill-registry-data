---
name: spark
description: Use when building distributed data pipelines with Apache Spark. Covers partitioning, shuffles, skew, joins, caching, and reading the Spark UI to find why a job is slow.
metadata:
  category: data
  version: 1.0.0
  tags: [spark, distributed, etl, shuffle, skew]
---

# Spark

## Purpose

Write Spark jobs whose cost is understood. Almost all Spark performance problems are one of three things: too much shuffle, skewed partitions, or reading far more data than the query needs.

## When to Use

- Building or reviewing a Spark pipeline.
- A job that is slow, failing with out-of-memory errors, or has one straggling task.
- Tuning partitioning and join strategy.
- Reading the Spark UI to diagnose a stage.

## Capabilities

- Partitioning strategy and repartitioning.
- Shuffle minimization and broadcast joins.
- Skew detection and mitigation.
- Caching and persistence levels.
- File-format and predicate-pushdown optimization.
- Spark UI interpretation.

## Inputs

- The job, its input data volume, and its physical plan.
- The Spark UI: stage timings, task distribution, shuffle read/write.
- Cluster resources.

## Outputs

- A plan with fewer or smaller shuffles.
- Balanced partitions with no straggling tasks.
- Measured improvement in wall-clock time and cost.

## Workflow

1. **Read the plan first** — `df.explain(True)`. Every `Exchange` is a shuffle, and a shuffle writes to disk and crosses the network. It is the dominant cost.
2. **Prune early** — Select the columns and filter the rows you need before joining, not after. With Parquet, this pushes down to the file reader and never reads the data at all.
3. **Broadcast the small side** — A join where one side fits in memory (roughly under 100 MB) should be a broadcast join. That eliminates the shuffle entirely.
4. **Find the skew** — In the Spark UI, look at the task duration distribution within a stage. If the max is 50x the median, one partition holds most of the data. That single task is your job's runtime.
5. **Mitigate the skew** — Salting the key, or enabling adaptive query execution's skew join handling.
6. **Cache only what is reused** — Caching a DataFrame used once costs memory and gains nothing.

## Best Practices

- Enable adaptive query execution (`spark.sql.adaptive.enabled=true`). It coalesces partitions, converts joins to broadcasts at runtime, and handles skew automatically. It is on by default from Spark 3.2 and is the single largest free improvement available.
- A shuffle is the most expensive operation in Spark. `groupBy`, `join`, `distinct`, and `repartition` all shuffle. Count them in the plan.
- `collect()` brings the entire dataset to the driver. On anything non-trivial this is an out-of-memory error waiting for a larger input.
- Use Parquet or Delta, never CSV or JSON, for anything that will be read more than once. Columnar formats support predicate and projection pushdown; row formats do not.
- Too many small partitions means task-scheduling overhead dominates; too few means poor parallelism and memory pressure. Aim for partitions of roughly 128 MB.
- `cache()` is lazy. It does nothing until an action runs, and it can silently fall back to recomputation if it does not fit in memory.

## Examples

**Prune, broadcast, and avoid the shuffle:**

```python
from pyspark.sql import functions as F

# Costly: joins the full orders table, then filters. The shuffle moves
# everything, including the rows about to be discarded.
result = (
    orders.join(customers, "customer_id")
          .filter(F.col("created_at") >= "2026-01-01")
          .select("order_id", "segment", "total_cents")
)

# Better: filter and project first (pushed into the Parquet reader), and
# broadcast the small dimension so the large side is never shuffled.
result = (
    orders
      .filter(F.col("created_at") >= "2026-01-01")     # predicate pushdown
      .select("order_id", "customer_id", "total_cents") # projection pushdown
      .join(F.broadcast(customers.select("customer_id", "segment")), "customer_id")
)
```

**Diagnosing and fixing skew:**

```python
# Symptom in the Spark UI: stage 7 has 200 tasks; 199 finish in ~4s and one
# runs for 22 minutes. That one task is the entire job's runtime.

# Confirm: one key dominates.
orders.groupBy("customer_id").count().orderBy(F.desc("count")).show(5)
# +------------+---------+
# | customer_id|    count|
# +------------+---------+
# | cus_bulk_01| 41200000|   <-- 68% of all rows: a single bulk-import account
# | cus_9f2a3b |    18400|

# Fix: salt the hot key so it spreads across partitions.
SALTS = 64
orders_salted = orders.withColumn(
    "salt",
    F.when(F.col("customer_id") == "cus_bulk_01",
           (F.rand() * SALTS).cast("int")).otherwise(F.lit(0)),
)
customers_exploded = customers.withColumn(
    "salt",
    F.explode(F.when(F.col("customer_id") == "cus_bulk_01",
                     F.array([F.lit(i) for i in range(SALTS)])).otherwise(F.array(F.lit(0)))),
)
result = orders_salted.join(customers_exploded, ["customer_id", "salt"])
```

## Notes

- Adaptive query execution handles most skew automatically from Spark 3.2 onward (`spark.sql.adaptive.skewJoin.enabled`). Manual salting is still needed for extreme skew and for non-join operations.
- `spark.sql.shuffle.partitions` defaults to 200 regardless of your data size, which is wrong for both small and large jobs. AQE's coalescing largely fixes this, but the default is still worth setting deliberately.
- If the job fits comfortably on one machine, do not use Spark. A single-node DuckDB or Polars job will be faster and dramatically simpler than a distributed one.
