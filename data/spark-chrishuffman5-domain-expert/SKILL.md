---
name: spark
description: "Apache Spark skill for ETL and data transformation across all versions (3.5 LTS through 4.2). Deep expertise in DataFrame API, Spark SQL, Catalyst optimizer, Structured Streaming, partition tuning, join strategies, and lakehouse integration. WHEN: \"Spark\", \"PySpark\", \"SparkSQL\", \"spark-submit\", \"DataFrame\", \"RDD\", \"Catalyst\", \"Tungsten\", \"AQE\", \"Spark Structured Streaming\", \"Spark partition\", \"Spark shuffle\", \"Spark join\", \"Spark UDF\", \"Spark performance\", \"Spark ETL\", \"Spark pipeline\", \"spark.conf\", \"SparkSession\". Do NOT use for Databricks-managed features (Unity Catalog, Photon, workspace/cluster administration) -- that's the `databricks` skill in the database plugin. Do NOT use for BI/reporting tool selection or dashboarding on top of Spark output -- that's the analytics plugin."
license: MIT
---

# Apache Spark

This skill covers Apache Spark across all supported versions (3.5 LTS through 4.2). It provides deep knowledge of the distributed execution model, DataFrame and SQL APIs, Catalyst optimizer, Tungsten engine, Structured Streaming, and integration with open table formats (Delta Lake, Iceberg, Hudi). When a question is version-specific, read the appropriate version reference.

## When to Use This Skill's General Guidance vs. a Version Reference

**Use the general guidance in this file when the question spans versions or is version-agnostic:**
- "How does the Catalyst optimizer work?"
- "Tune Spark shuffle partitions for a 2TB join"
- "Broadcast join vs sort-merge join -- which and when?"
- "Structured Streaming checkpointing and watermarks"
- "Spark executor memory sizing"
- "Design a medallion architecture pipeline in Spark"
- "Debug a slow Spark SQL query"
- "Spark vs Flink for streaming"

**Read a version reference when the question is version-specific:**
- "Spark Connect architecture" --> `references/versions/3.5.md`
- "Spark 4.0 ANSI mode migration" --> `references/versions/4.0.md`
- "VARIANT data type in Spark" --> `references/versions/4.0.md`
- "Spark Declarative Pipelines" --> `references/versions/4.2.md`
- "Real-Time Mode streaming" --> `references/versions/4.2.md`
- "SQL scripting in Spark" --> `references/versions/4.2.md`
- "Migrate from Spark 3.5 to 4.0" --> `references/versions/4.0.md`

## How to Approach Tasks

1. **Classify** the request:
   - **Performance/tuning** -- Load `references/diagnostics.md` for Spark UI analysis, common errors, tuning configs
   - **Architecture/internals** -- Load `references/architecture.md` for execution model, Catalyst, Tungsten, memory model, AQE
   - **Best practices/pipeline design** -- Load `references/best-practices.md` for partitioning, joins, skew, UDFs, resource sizing, medallion patterns
   - **Version-specific feature** -- Read the applicable version reference
   - **Databricks-specific** -- See the database plugin's `databricks` skill

2. **Determine version** -- Ask if unclear. Key version gates:
   - Spark Connect GA: 3.5+
   - VARIANT type: 4.0+
   - ANSI mode default: 4.0+
   - Java 17 required: 4.0+
   - Python Data Source API: 4.0+
   - Declarative Pipelines: 4.1+ (covered in 4.2 agent)
   - Real-Time Mode: 4.1+ (covered in 4.2 agent)
   - SQL Scripting GA: 4.1+ (covered in 4.2 agent)

3. **Analyze** -- Apply Spark-specific reasoning: execution model (DAG, stages, tasks), shuffle impact, data skew, memory pressure, serialization, partition sizing.

4. **Recommend** -- Provide actionable guidance with PySpark/SQL examples and specific configs. Explain why, not just what.

5. **Verify** -- Suggest validation: `explain()`, Spark UI tabs, `query.lastProgress` for streaming, test patterns.

## Core Architecture

### Execution Model

Spark runs as a Driver-Executor system. The Driver translates user code into a DAG of stages and tasks. Executors run tasks in parallel across the cluster.

```
User Code (DataFrame/SQL)
    │
    ▼
Catalyst Optimizer (Analysis → Logical Optimization → Physical Planning)
    │
    ▼
Tungsten Code Generation (whole-stage codegen → JVM bytecode)
    │
    ▼
DAG Scheduler (splits plan into stages at shuffle boundaries)
    │
    ▼
Task Scheduler (assigns tasks to executor slots)
    │
    ▼
Executors (run tasks in parallel, store cached data)
```

**Key concepts:**
- **Narrow dependencies** (map, filter): pipelined on a single node, no shuffle
- **Wide dependencies** (groupBy, join, repartition): require shuffle across network
- **Shuffle**: most expensive operation -- redistributes data across partitions. Minimize shuffles for performance.
- **AQE** (Adaptive Query Execution): re-optimizes plans at runtime using actual data statistics. Enabled by default since 3.2. Handles partition coalescing, join strategy switching, and skew joins automatically.

### API Layers

| API | Type Safety | Optimization | Use Case |
|---|---|---|---|
| **DataFrame** | Schema-aware (runtime) | Full Catalyst + Tungsten | Primary API for ETL. Available in Python, Scala, Java, R |
| **Spark SQL** | Schema-aware (runtime) | Full Catalyst + Tungsten | SQL interface over DataFrames. ANSI SQL (default in 4.0+) |
| **Dataset** | Compile-time (Scala/Java) | Partial Catalyst | Type-safe API. Scala/Java only. Not available in PySpark |
| **RDD** | Strongly typed | None (opaque to Catalyst) | Low-level control, custom partitioning. Rarely needed for ETL |

### Storage Integration

**File formats:** Parquet (default, columnar, predicate pushdown) > ORC (Hive ecosystem) > Avro (streaming/writes) > JSON/CSV (avoid for production ETL).

**Open table formats:**
- **Delta Lake** -- ACID transactions, time travel, MERGE, schema evolution. Deep Databricks integration. Default COW, Liquid Clustering.
- **Apache Iceberg** -- Vendor-neutral, broadest engine support (Spark, Trino, Flink). Hidden partitioning, partition evolution.
- **Apache Hudi** -- Near-real-time CDC. COW and MOR table types.

## Spark SQL and DataFrame Patterns

### DataFrame Essentials

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, count, when, lit, broadcast

spark = SparkSession.builder.appName("etl").getOrCreate()

# Read
df = spark.read.parquet("s3://bucket/data/")
df = spark.read.format("delta").load("/lakehouse/bronze/events")

# Transform
result = (
    df
    .filter(col("status") == "active")
    .withColumn("revenue", col("price") * col("quantity"))
    .groupBy("region", "product")
    .agg(
        sum("revenue").alias("total_revenue"),
        count("*").alias("order_count")
    )
    .orderBy(col("total_revenue").desc())
)

# Write
result.write.format("delta").mode("overwrite").save("/lakehouse/gold/revenue")
```

### Spark SQL

```python
df.createOrReplaceTempView("orders")

result = spark.sql("""
    SELECT region, product,
           SUM(price * quantity) AS total_revenue,
           COUNT(*) AS order_count
    FROM orders
    WHERE status = 'active'
    GROUP BY region, product
    ORDER BY total_revenue DESC
""")
```

DataFrame API and SQL are interchangeable -- both compile to the same physical plan via Catalyst. Choose based on team preference and complexity.

### Key DataFrame Operations

```python
# Joins
result = orders.join(broadcast(customers), "customer_id")           # broadcast small table
result = orders.join(products, orders.product_id == products.id)    # equi-join

# Window functions
from pyspark.sql.window import Window
w = Window.partitionBy("customer_id").orderBy("order_date")
df.withColumn("running_total", sum("amount").over(w))
df.withColumn("row_num", row_number().over(w))

# Deduplication
df.dropDuplicates(["id", "timestamp"])

# Schema handling
df.printSchema()
df.select(col("nested_col.*"))                    # flatten struct
df.select(explode("array_col").alias("element"))  # explode array
```

## Structured Streaming

### Processing Modes

| Mode | Latency | Guarantee | When |
|---|---|---|---|
| **Micro-batch** (default) | ~100ms+ | Exactly-once | Production default for most streaming ETL |
| **Real-Time Mode** (4.1+) | Single-digit ms | Exactly-once | Sub-second latency requirements |
| **Continuous** (experimental) | ~1ms | At-least-once only | Not recommended for production |
| **Trigger.AvailableNow** | Batch-like | Exactly-once | Process all available data then stop |

### Streaming Pattern

```python
# Read stream
stream_df = (
    spark.readStream
    .format("delta")
    .option("maxFilesPerTrigger", 100)
    .load("/bronze/events")
)

# Transform (same DataFrame API as batch)
transformed = stream_df.filter(col("valid") == True).select("id", "value", "ts")

# Write stream
query = (
    transformed.writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "/checkpoints/events")
    .trigger(processingTime="30 seconds")
    .start("/silver/events")
)

query.awaitTermination()
```

### Key Concepts
- **Watermark**: handles late data. `df.withWatermark("event_time", "10 minutes")` -- Spark waits 10 minutes for late events before finalizing aggregations.
- **Checkpointing**: Required for fault tolerance. Stores offsets and state to durable storage. Always set `checkpointLocation`.
- **Output modes**: `append` (new rows only), `complete` (full result set), `update` (changed rows).
- **foreachBatch**: Custom sink logic with exactly-once guarantees.

```python
def process_batch(batch_df, batch_id):
    # Custom logic per micro-batch (e.g., MERGE, multi-table writes)
    delta_table.alias("t").merge(batch_df.alias("s"), "t.id = s.id") \
        .whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()

query = stream_df.writeStream.foreachBatch(process_batch).start()
```

## Version-Specific Guidance

| Version | Status | Reference | What's Version-Specific |
|---|---|---|---|
| **3.5** | Extended LTS (EOL Nov 2027) | `references/versions/3.5.md` | Spark Connect GA, last version with Java 8/11 support |
| **4.0** | Stable | `references/versions/4.0.md` | ANSI mode default, VARIANT type, Java 17 required, breaking changes |
| **4.2** | Preview (GA mid-2026) | `references/versions/4.2.md` | Declarative Pipelines, Real-Time Mode, SQL Scripting GA (covers 4.1 GA features too) |

## Performance Quick Reference

### Shuffle Partitions

```python
# With AQE (recommended): set high, let AQE coalesce
spark.conf.set("spark.sql.shuffle.partitions", "2000")
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")

# Without AQE: calculate based on data volume
# Target 128-256 MB per partition
# partitions = total_shuffle_data_bytes / target_partition_size
```

### Join Strategy Selection

| Scenario | Strategy | Config/Hint |
|---|---|---|
| One side < 50MB | Broadcast hash join | `broadcast(small_df)` or increase `autoBroadcastJoinThreshold` |
| Both sides large, equi-join | Sort-merge join (default) | No action needed |
| Repeated large-large joins on same key | Bucketed join (shuffle-free) | `df.write.bucketBy(N, "key").saveAsTable(...)` |
| Non-equi join, one side small | Broadcast nested loop | `broadcast(small_df)` |

### Data Skew First Response

1. Enable AQE (default since 3.2) -- handles most skew automatically
2. Check Spark UI > Stages > task duration variance
3. If AQE insufficient: salt the skewed key, isolate hot keys, or pre-aggregate

### UDF Decision Tree

1. Can it be expressed with `pyspark.sql.functions.*`? --> Use built-in (fastest)
2. Can it be expressed as a SQL expression? --> Use `expr()` (Catalyst-optimized)
3. Need custom logic? --> Use Pandas UDF (10-100x faster than Python UDF)
4. Need table output? --> Use Python UDTF (4.0+)
5. Last resort --> Python UDF (avoid if possible)

## Anti-Patterns

1. **Using `collect()` on large datasets** -- Pulls all data to the driver, causing OOM. Use `take(N)`, `show()`, or write to storage. The only valid use of `collect()` is for small lookup results.

2. **Python UDFs for transformable logic** -- Python UDFs serialize row-by-row between JVM and Python, breaking Catalyst. Use built-in functions first, Pandas UDFs (10-100x faster) when custom logic is unavoidable.

3. **Ignoring shuffle partitions** -- Default `spark.sql.shuffle.partitions=200` is wrong for most workloads. With AQE enabled, set high (e.g., 2000) and let AQE coalesce. Without AQE, calculate based on data volume (128-256 MB per partition).

4. **Caching everything** -- Caching DataFrames used only once adds overhead. Cache only DataFrames reused across multiple actions, and always `unpersist()` when done.

5. **`coalesce(1)` on large datasets** -- Creates a single-threaded bottleneck. For small outputs, `repartition(1)` is slightly better. For large outputs, target file count with `maxRecordsPerFile` or table format compaction.

6. **Inferring schema on every read** -- Schema inference scans files, adding latency and risking inconsistency. Define schemas explicitly: `spark.read.schema(defined_schema).parquet(...)`.

7. **Neglecting data skew** -- One skewed partition makes the entire stage run as slowly as the slowest task. Check for skew in Spark UI, try AQE first, then salting or hot-key isolation.

8. **Spark for small data** -- A Spark cluster for datasets under 100 GB adds JVM overhead, cluster management, and cost. Use DuckDB or dbt for small-scale transforms.

## Cross-Domain References

| Technology | Reference | When |
|---|---|---|
| Databricks | The database plugin's `databricks` skill | Databricks Runtime, Unity Catalog, Photon, Databricks-specific Spark features |
| ETL Domain | `overview` skill | Cross-platform ETL architecture, tool selection |
| Transformation | `transformation` skill | Comparing Spark vs dbt vs DuckDB |

## Reference Files

Load these when you need deep knowledge for a specific area:

- `references/architecture.md` -- Execution engine (Driver/Executor, DAG, stages, tasks), Catalyst optimizer internals, Tungsten codegen, memory model (unified memory manager, off-heap), AQE mechanics, deployment modes, Data Source API v2
- `references/best-practices.md` -- Partition strategies (sizing, repartition vs coalesce, pruning), join optimization (broadcast, sort-merge, bucketing), data skew handling (AQE, salting, hot-key isolation), UDF performance hierarchy, resource sizing formulas, pipeline patterns (medallion, CDC, incremental), caching, testing, cost optimization
- `references/diagnostics.md` -- Spark UI interpretation (Jobs, Stages, SQL, Storage, Executors tabs), common errors (OOM, shuffle fetch failures, serialization, GC pressure, small files, schema drift), performance tuning configs (shuffle, AQE, memory, I/O, timeouts), reading query plans (`explain()`), monitoring (event logs, History Server, Prometheus)

## Diagnostic Scripts

Ready-made History Server REST API scripts (bash + curl + jq) in `scripts/`, numbered by investigation order. All read-only; also work against a live driver UI (port 4040).

- `scripts/01-recent-applications.sh` -- Recent applications with durations and dirty-exit detection
- `scripts/02-app-failed-stages.sh` -- Failed jobs/stages with failure reasons (OOM vs fetch-failure vs executor loss)
- `scripts/03-slow-stages.sh` -- Slowest stages plus task-time quantiles (the skew detector)
- `scripts/04-executor-usage.sh` -- Executor memory/GC/failure profile (resourcing vs code discriminator)
