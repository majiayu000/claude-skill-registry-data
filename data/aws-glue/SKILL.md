---
name: aws-glue
description: "AWS Glue specialist for serverless data integration on AWS. Deep expertise in ETL jobs, Data Catalog, crawlers, DynamicFrames, Spark tuning, job bookmarks, data quality (DQDL), Glue Studio, streaming ETL, and cost optimization. WHEN: \"AWS Glue\", \"Glue job\", \"Glue crawler\", \"Data Catalog\", \"DynamicFrame\", \"Glue Studio\", \"Glue bookmark\", \"job bookmark\", \"transformation_ctx\", \"Glue DPU\", \"Glue worker\", \"Glue 5.0\", \"Glue 5.1\", \"Glue Data Quality\", \"DQDL\", \"DataBrew\", \"Glue streaming\", \"Glue connection\", \"Glue classifier\", \"Glue Auto Scaling\", \"Glue Flex\", \"Glue Ray\", \"Glue vs ADF\", \"Glue vs Fivetran\"."
license: MIT
---

# AWS Glue

This skill covers AWS Glue, Amazon's fully managed, serverless data integration service. AWS Glue is a managed service -- the runtime evolves through versioned releases (current: Glue 5.1 with Spark 3.5.6). It provides deep knowledge of:

- Data Catalog (centralized Hive-compatible metadata repository, databases, tables, partitions, connections)
- Crawlers and classifiers (automated schema discovery, format detection, catalog population)
- ETL engine (Spark-based with DynamicFrame extensions, Ray-based for distributed Python, Python Shell for lightweight tasks)
- Glue Studio (visual ETL authoring, data preview, data quality transforms, DataBrew recipe integration)
- Job system (DPU/worker types, job bookmarks, triggers, workflows, EventBridge integration)
- Data Quality (DQDL rule language, ML-powered anomaly detection, auto-recommendation)
- Streaming ETL (Spark Structured Streaming from Kinesis/Kafka/MSK)
- Open table formats (Iceberg, Hudi, Delta Lake with Glue 5.x native support)
- Cost optimization (Auto Scaling, Flex execution, worker right-sizing, pushdown predicates)

## How to Approach Tasks

When you receive a request:

1. **Classify** the request:
   - **Architecture / job design** -- Load `references/architecture.md` for Data Catalog, crawlers, ETL engine, DPU/worker types, job bookmarks, connections, pricing
   - **Performance / best practices** -- Load `references/best-practices.md` for job design, DPU sizing, partitioning, crawler management, cost optimization, testing
   - **Troubleshooting / diagnostics** -- Load `references/diagnostics.md` for OOM errors, crawler issues, slow jobs, CloudWatch metrics, error message reference
   - **Cross-tool comparison** -- See the `integration` skill for Glue vs ADF, Fivetran, NiFi, etc.

2. **Gather context** -- Determine:
   - What type of job? (batch ETL, streaming, data quality, crawling)
   - What Glue version? (5.1 current, 4.0 common, older versions)
   - What worker type? (G.1X, G.2X, G.4X, R-series, Z.2X for Ray)
   - What data format and volume? (Parquet, CSV, JSON, small files problem)
   - Is this on S3, JDBC, or streaming from Kinesis/Kafka?

3. **Analyze** -- Apply Glue-specific reasoning. Consider DynamicFrame vs DataFrame trade-offs, job bookmark configuration, pushdown predicates, partition strategy, and CloudWatch metrics.

4. **Recommend** -- Provide actionable guidance with specific Glue job parameters, AWS CLI commands, CloudWatch metric names, and code patterns where appropriate.

5. **Verify** -- Suggest validation steps (CloudWatch metrics review, Spark UI inspection, Job Run Insights, interactive session testing).

## Core Architecture

### Five Pillars

```
┌────────────────────────────────────────────────────┐
│  AWS Glue                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │
│  │  Data    │  │ Crawlers │  │   ETL Engine     │ │
│  │ Catalog  │  │ & Class. │  │ Spark/Ray/Shell  │ │
│  └────┬─────┘  └────┬─────┘  └───────┬──────────┘ │
│       │              │                │            │
│  ┌────▼──────────────▼────────────────▼──────────┐ │
│  │              Glue Studio                      │ │
│  │        (Visual ETL + Data Quality)            │ │
│  └────────────────────┬──────────────────────────┘ │
│                       │                            │
│  ┌────────────────────▼──────────────────────────┐ │
│  │           Job System                          │ │
│  │    Triggers / Workflows / EventBridge         │ │
│  └───────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────┘
```

### Data Catalog

The Data Catalog is a centralized, persistent metadata repository -- one per AWS account per region. It serves as a drop-in replacement for the Apache Hive Metastore.

**Structure**:
- **Databases** -- logical groupings of table definitions
- **Tables** -- metadata describing schema, location, format, and properties of data in S3, JDBC, or other stores
- **Partitions** -- subdivisions by column values (e.g., `year=2025/month=08/day=15`)
- **Connections** -- JDBC endpoints, VPC config, credentials via Secrets Manager

**Integration**: Amazon Athena, Redshift Spectrum, and EMR query directly against the Data Catalog. AWS Lake Formation extends it with fine-grained access control.

### Crawlers and Classifiers

Crawlers are automated programs that scan data stores, infer schemas, and populate the Data Catalog:

1. Connect to source (S3, JDBC, DynamoDB, MongoDB)
2. Read first megabyte of each file to classify format
3. Apply classifiers in priority order (built-in: CSV, JSON, Parquet, ORC, Avro, XML; custom: Grok, CSV, JSON, XML)
4. Group compatible schemas, create/update table definitions
5. Automatically create partition indexes for S3 and Delta Lake

Crawlers can run on-demand, on a cron schedule, or event-driven via EventBridge.

### ETL Engine

**Spark Runtime** (primary): Managed Apache Spark with DynamicFrame extensions. DynamicFrames handle schema inconsistencies (mixed types in the same column) without upfront schema definition. They integrate with the Data Catalog and support Glue-specific features like job bookmarks and `groupFiles`.

**Current runtime (Glue 5.1)**: Spark 3.5.6, Python 3.11, Scala 2.12.18, Java 17. Iceberg format v3 support, S3A default connector, fine-grained Lake Formation access control.

**Ray Runtime**: Distributed Python via Ray.io for non-Spark workloads (pandas, NumPy, scikit-learn at scale). Uses Z.2X workers.

**Python Shell**: Single-node Python for lightweight tasks (1 DPU max).

### Worker Types

| Worker | DPU | vCPU | Memory | Use Case |
|---|---|---|---|---|
| G.025X | 0.25 | 2 | 4 GB | Python Shell |
| G.1X | 1 | 4 | 16 GB | General-purpose ETL |
| G.2X | 2 | 8 | 32 GB | Memory-intensive transforms |
| G.4X | 4 | 16 | 64 GB | Large dataset processing |
| G.8X | 8 | 32 | 128 GB | ML transforms, heavy computation |
| R.1X | 1 | 4 | 32 GB | Memory-optimized (2x memory/DPU) |
| R.2X | 2 | 8 | 64 GB | Large in-memory joins and caching |
| Z.2X | -- | -- | -- | Ray distributed Python |

**Auto Scaling** (Glue 3.0+): Dynamically adjusts worker count based on workload parallelism. Set max workers; Glue optimizes per stage.

**Flex Execution**: 34% cost reduction ($0.29/DPU-hr vs $0.44) for non-urgent batch jobs that can tolerate delayed start times.

### Job Bookmarks

Job bookmarks persist state between runs for incremental processing:

- **S3 sources**: Track file timestamps and paths already processed
- **JDBC sources**: Track primary key boundaries of processed rows
- **Critical requirement**: Every source and sink must have a unique `transformation_ctx` string for bookmarks to work. Omitting `transformation_ctx` silently disables incremental processing.

States: `enabled`, `disabled`, `paused` (retain state but don't use it).

### Glue Studio

Visual drag-and-drop ETL authoring:
- Source nodes (S3, JDBC, Kinesis, Kafka, Data Catalog tables)
- Transform nodes (ApplyMapping, Filter, Join, SelectFields, SQL Query, Custom Code, Data Quality)
- Target nodes (S3, JDBC, Data Catalog tables)
- Real-time data preview and output schema inspection
- Auto-generates PySpark/Scala from the visual DAG
- Embedded DataBrew recipe nodes and data quality transforms

### Data Quality (DQDL)

Built on the open-source DeeQu framework:

```
Rules = [
    Completeness "email" > 0.95,
    IsUnique "customer_id",
    ColumnValues "status" in ["active", "inactive", "pending"],
    DataFreshness "updated_at" <= 24 hours,
    ReferentialIntegrity "orders.customer_id" "customers.id" > 0.99,
    RowCount between 1000 and 1000000
]
```

Advanced features: `NOT` operator, `WHERE` clause for conditional rules, composite rules, ML-powered anomaly detection via `DetectAnomalies`, auto-recommendation engine.

### Streaming ETL

Built on Spark Structured Streaming:
- Sources: Kinesis Data Streams, Apache Kafka, Amazon MSK
- Processing: Micro-batch or continuous, windowed aggregations, stateful operations
- Targets: S3, JDBC, Data Catalog tables, Iceberg/Hudi/Delta Lake
- Automatic checkpointing for fault tolerance
- Auto Scaling based on stream throughput

### Orchestration

**Triggers**: Scheduled (cron), conditional (job/crawler completion), on-demand (API-driven).

**Workflows**: Chain crawlers and jobs into DAGs with dependency management, run history, and parameterization.

**EventBridge**: Glue publishes events for job state changes, crawler completions, and catalog updates.

## Pricing

| Component | Unit | Rate (US East) |
|---|---|---|
| ETL Jobs (Standard) | DPU-hour | $0.44 |
| ETL Jobs (Flex) | DPU-hour | $0.29 |
| Interactive Sessions | DPU-hour | $0.44 |
| Data Catalog Storage | Per 100K objects/month | $1.00 (first 1M free) |
| Crawlers | DPU-hour | $0.44 |
| DataBrew | Node-hour | $0.48 |

Billing: per-second with 1-minute minimum (Glue 3.0+), 10-minute minimum (Glue 2.0).

## Anti-Patterns

1. **Starting with 10 DPUs** -- The legacy default of 10 workers is excessive for most jobs. Start with 2-5 G.1X workers and scale based on CloudWatch metrics, not assumptions.
2. **Ignoring `transformation_ctx`** -- Omitting the `transformation_ctx` parameter on DynamicFrame sources and sinks silently disables job bookmarks. Every source and sink needs a unique context string.
3. **Using `.collect()` or `.toPandas()` on large datasets** -- These pull data to the driver node, causing driver OOM. Use distributed writes or sample-based operations.
4. **Millions of small files without `groupFiles`** -- Small files exhaust driver memory building file indexes. Enable `groupFiles: 'inPartition'` in DynamicFrame options or run compaction jobs.
5. **Full table scans without pushdown predicates** -- Always use `push_down_predicate` to filter at the catalog level and read only relevant partitions.
6. **One crawler for the entire data lake** -- A single crawler scanning millions of files across all domains is slow and expensive. Create targeted crawlers per domain or table group.
7. **Not using Flex for batch jobs** -- Non-urgent batch jobs should use Flex execution for 34% cost savings. The only trade-off is potential start delay.
8. **Ignoring Auto Scaling** -- For Glue 3.0+, enable Auto Scaling instead of guessing worker count. Set max workers and let Glue optimize.

## AWS CLI Reference

```bash
# Start a job run
aws glue start-job-run --job-name my-etl-job \
  --arguments '{"--source_path":"s3://bucket/raw/","--target_path":"s3://bucket/curated/"}'

# Check job run status
aws glue get-job-run --job-name my-etl-job --run-id jr_abc123

# Reset job bookmark
aws glue reset-job-bookmark --job-name my-etl-job

# Start a crawler
aws glue start-crawler --name my-crawler

# Get table from Data Catalog
aws glue get-table --database-name my_database --name my_table
```

## Reference Files

- `references/architecture.md` -- Data Catalog deep dive, crawler mechanics, ETL engine (Spark/Ray/Shell), DPU and worker types, job bookmarks, Glue Studio, connections, orchestration, security, pricing
- `references/best-practices.md` -- Job design patterns, DPU sizing strategy, partitioning, Data Catalog organization, crawler management, cost optimization, testing (Docker, pytest, CI/CD), operational practices
- `references/diagnostics.md` -- OOM debugging (driver vs executor), crawler issues, slow job diagnosis, CloudWatch metrics reference, alarm thresholds, error message lookup, debugging workflow

## Cross-References

- `spark` skill -- Apache Spark context for Spark-specific tuning beyond Glue's managed environment
- `adf` skill -- Azure Data Factory for cross-cloud comparison
- `fivetran` skill -- Fivetran for managed EL comparison
- `overview` skill -- Cross-tool comparisons and paradigm routing
