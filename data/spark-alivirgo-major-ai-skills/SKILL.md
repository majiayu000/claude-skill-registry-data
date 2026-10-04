---
name: spark
description: "Build Spark DataFrame and SQL jobs, tune partitions and shuffle behavior, and diagnose local or cluster execution failures."
category: scientific
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["spark", "pyspark", "dataframe", "big-data", "sql", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Apache Spark AI Skill Guide

## Overview & Engine Architecture

Spark distributes DataFrame/Dataset work across executors. Transformations build a lineage; actions (`count`, `write`) trigger jobs split into stages at shuffle boundaries. Agents design partition keys, avoid wide shuffles, cache only reused hot datasets, and read Spark UI / explain plans before throwing more cores at a bad query.

```
Driver (SparkSession)
   -> jobs / stages / tasks
        -> executors (partitions)
             -> shuffle / reduce
             -> sink (Parquet, table)
```

## When to use this skill

- Multi-node ETL beyond single-machine Polars/DuckDB
- Lakehouse table transforms (Parquet/Delta/Iceberg via connectors)
- Spark SQL shared with analytics engineers

## Operational directives

1. Prefer DataFrame API / Spark SQL over RDDs for optimizer benefits.
2. Repartition or bucket on join/group keys intentionally; do not `repartition(200)` blindly.
3. Filter and project before joins.
4. Treat `collect()` to the driver as a bug on large results.
5. Size AQE / broadcast hints with measured data, not folklore.

## PySpark transform example

```python
from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.appName("orders-mart").getOrCreate()

orders = spark.read.parquet("s3a://lake/orders/")
daily = (
    orders
    .where(F.col("created_at") >= "2025-01-01")
    .groupBy(F.to_date("created_at").alias("day"), "customer_id")
    .agg(F.sum("amount").alias("revenue"), F.count("*").alias("orders"))
)

daily.write.mode("overwrite").parquet("s3a://lake/marts/daily_revenue/")
```

## Diagnose skew

```python
daily.explain(extended=True)
# Spark UI: Stages -> look for long-tail tasks / spill
```

## Common failures

| Symptom | Cause | Fix |
| --- | --- | --- |
| Shuffle spill | uneven keys / wide join | salt keys; broadcast small side |
| Driver OOM | `.collect` / huge broadcast | write out; sample |
| Tiny files | too many partitions on write | `coalesce` / maxRecordsPerFile |
| Slow job | UDF per row | built-in functions / Pandas UDFs carefully |

## Best practices

- Idempotent writes to dated paths or transactional tables.
- Persist (`cache`) only multi-action reuse; then `unpersist`.
- Align partition columns with filter patterns (`dt=YYYY-MM-DD`).
- Pin Spark + connector versions with the cluster runtime.

## Limitations

- Local mode is for unit tests, not production scale claims.
- Streaming Structured Streaming needs separate checkpoint design.
- Cloud IAM/storage credentials are environment-specific.

## Related skills

- `@duckdb` / `@polars` - single-node alternatives
- `@airflow` / `@prefect` - schedule Spark jobs
- `@dbt` - SQL models on Spark/Databricks SQL warehouses
