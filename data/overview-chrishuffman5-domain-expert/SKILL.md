---
name: overview
description: "Top-level guidance for ALL ETL, data integration, and data pipeline technologies. Provides cross-platform expertise in data orchestration, transformation, integration, and streaming. WHEN: \"ETL\", \"data pipeline\", \"data integration\", \"ELT\", \"data movement\", \"data transformation\", \"Airflow\", \"SSIS\", \"dbt\", \"Spark\", \"Kafka\", \"NiFi\", \"Azure Data Factory\", \"Fivetran\", \"data quality\", \"CDC\", \"data warehouse loading\"."
license: MIT
---

# ETL / Data Integration Overview

This skill provides cross-platform expertise in data orchestration, transformation, integration, and streaming for ETL, ELT, and data pipeline technologies. It coordinates with the sibling technology skills in this plugin for deep implementation details.

## When to Use This Skill vs. a Technology Skill

**Use this skill when the question is cross-platform or strategic:**
- "Should I use Airflow or Azure Data Factory?"
- "Design a data pipeline for our data warehouse"
- "Compare ELT approaches (dbt vs Spark)"
- "What's the right CDC strategy for our OLTP-to-warehouse sync?"
- "How should we handle schema evolution across pipelines?"
- "Batch vs streaming -- which and when?"
- "Data quality framework design"
- "ETL architecture assessment"

**See a technology skill when the question is technology-specific:**
- "Airflow DAG not scheduling correctly" --> `airflow` skill
- "SSIS package deployment model" --> `ssis` skill
- "dbt incremental model not merging" --> `dbt-core` skill
- "dbt Cloud CI job setup" --> `dbt-cloud` skill
- "Spark DataFrame shuffle tuning" --> `spark` skill
- "ADF linked service authentication" --> `adf` skill
- "NiFi backpressure configuration" --> `nifi` skill
- "Informatica mapping task error" --> `informatica` skill
- "Talend tMap join configuration" --> `talend` skill
- "Fivetran connector sync failure" --> `fivetran` skill
- "AWS Glue job bookmark issue" --> `aws-glue` skill
- "Synapse Pipelines copy activity" --> `synapse-pipelines` skill
- "Kafka consumer lag investigation" --> `kafka` skill

## How to Approach Tasks

1. **Classify** the request:
   - **Tool/platform selection** -- Use the comparison tables below
   - **Architecture / pipeline design** -- Load `references/concepts.md` for ETL/ELT fundamentals
   - **Orchestration** -- See the `orchestration` skill
   - **Transformation** -- See the `transformation` skill
   - **Integration / data movement** -- See the `integration` skill
   - **Streaming / real-time** -- See the `streaming` skill
   - **Technology-specific** -- See the matching technology skill directly

2. **Gather context** -- Data volume, latency requirements, source/target systems, existing tooling, team skills, cloud provider, compliance requirements, budget constraints

3. **Analyze** -- Apply data integration principles (idempotency, schema evolution, data quality, lineage)

4. **Recommend** -- Actionable guidance with trade-offs, not a single answer

## Data Integration Principles

1. **Idempotency is non-negotiable** -- Every pipeline must produce the same result when run multiple times with the same input. Use MERGE/upsert patterns, not blind INSERT. Partition-based overwrites are inherently idempotent.
2. **Prefer incremental over full loads** -- Full table scans don't scale. Use watermarks (timestamps, sequence IDs), CDC, or partition pruning. Fall back to full loads only for small reference tables or when source lacks change tracking.
3. **Separate extraction from transformation** -- ELT (extract-load-transform) scales better than ETL because you transform in the warehouse's compute, not in an external engine. Extract raw, land in staging, transform in place.
4. **Schema evolution is inevitable** -- Sources add columns, change types, rename fields. Design for it: use schema registries, backward-compatible contracts, and staging layers that absorb changes before they propagate.
5. **Data quality is a pipeline concern, not a downstream concern** -- Validate at ingestion: null checks, range checks, referential integrity, freshness. Quarantine bad records (dead letter tables) rather than failing entire batches.
6. **Lineage and observability are first-class** -- Every record should be traceable from source to target. Track row counts, load timestamps, source system identifiers. Instrument pipelines with metrics (rows processed, duration, error rate).
7. **Exactly-once is hard; at-least-once plus idempotent targets is practical** -- True exactly-once semantics require transactional coordination between source, pipeline, and sink. In practice, design for at-least-once delivery with idempotent writes.
8. **Partition and parallelize by design** -- Large datasets need partitioning strategies (date, region, entity) that align with both source extraction and target query patterns. Misaligned partitions cause either extraction bottlenecks or query performance issues.

## Technology Comparison

### Orchestration

| Technology | Model | Scheduling | Best For | Trade-offs |
|---|---|---|---|---|
| **Apache Airflow** | DAG-based (Python) | Cron, data-aware, event-driven (3.x) | Complex dependency graphs, multi-system orchestration, open-source teams | Operational overhead (self-hosted), scheduler bottleneck at scale, Python-only DAGs |
| **SSIS** | Control flow + data flow | SQL Agent jobs, catalog scheduling | SQL Server ecosystem, Windows/.NET shops, visual ETL | Windows-only, limited cloud-native support, vendor lock-in |

### Transformation

| Technology | Model | Language | Best For | Trade-offs |
|---|---|---|---|---|
| **dbt Core** | SQL-first, model DAG | SQL + Jinja2 | Warehouse-native transforms, analytics engineering, version-controlled SQL | SQL-only (no Python transforms in Core), requires warehouse compute, learning curve for Jinja |
| **dbt Cloud** | Managed dbt | SQL + Jinja2 + Python models | Teams wanting managed scheduling, IDE, CI, docs | Cost at scale, vendor dependency, feature parity lag with Core |
| **Apache Spark** | Distributed DataFrame/RDD | Python/Scala/Java/SQL | Large-scale transforms (TB+), ML pipelines, complex logic beyond SQL | JVM overhead, cluster management, overkill for < 100GB |
| **DuckDB** | In-process analytical | SQL | Single-node transforms, local development, CI testing, file-based ETL | Single-machine only, no distributed execution, memory-bound |

### Integration / EL (Extract-Load)

| Technology | Model | Hosting | Connectors | Best For | Trade-offs |
|---|---|---|---|---|---|
| **Azure Data Factory** | Visual pipelines + code | Azure-managed | 100+ built-in | Azure ecosystem, hybrid data movement, enterprise | Azure lock-in, debugging complexity, expression language quirks |
| **Apache NiFi** | Flow-based (drag-drop) | Self-hosted | 300+ processors | Real-time data routing, provenance tracking, government/regulated | Operational overhead, JVM memory, stateful clustering |
| **Informatica IDMC** | Visual mapping + AI | Managed (cloud) | 500+ | Enterprise integration, MDM, data governance | Cost, vendor lock-in, legacy migration complexity |
| **Talend** | Java code generation | Self-hosted or cloud | 900+ | Complex enterprise integrations, real-time + batch | Java overhead, steep learning curve, Qlik acquisition uncertainty |
| **Fivetran** | Managed EL (no-code) | Fully managed | 500+ pre-built | Automated source-to-warehouse replication, SaaS data | Cost per connector/row, limited transformation, black-box sync |
| **AWS Glue** | Spark-based serverless | AWS-managed | AWS ecosystem + JDBC | AWS-native ETL, crawlers for schema discovery | Cold start latency, Spark debugging, AWS lock-in |
| **Synapse Pipelines** | ADF-based + Spark pools | Azure-managed | ADF connectors + Spark | Unified analytics + ETL in Synapse workspace | Feature subset of ADF, Synapse-specific quirks, pricing complexity |

### Streaming

| Technology | Model | Delivery | Best For | Trade-offs |
|---|---|---|---|---|
| **Apache Kafka** | Distributed log, pub/sub | At-least-once (exactly-once with transactions) | Event streaming, CDC pipelines, microservice integration, high-throughput | Operational complexity (self-managed), partition design critical, consumer group management |

## Decision Framework

### Step 1: What kind of data movement?

| Pattern | Description | Typical Tools |
|---|---|---|
| **ELT** | Extract raw, load to warehouse, transform in-place | Fivetran/ADF (EL) + dbt (T) |
| **ETL** | Extract, transform in external engine, load | Spark, SSIS, Informatica, Talend |
| **CDC** | Capture changes from source transaction log | Kafka Connect + Debezium, ADF CDC, NiFi CDC |
| **Streaming** | Continuous event processing, low-latency | Kafka, Kafka Streams, Flink |
| **Reverse ETL** | Push warehouse data back to operational systems | Census, Hightouch, custom (ADF/Airflow) |

### Step 2: Batch vs streaming?

| Factor | Batch | Streaming |
|---|---|---|
| **Latency tolerance** | Minutes to hours is acceptable | Seconds to sub-second required |
| **Data volume** | Any size (partition and parallelize) | Sustained high throughput |
| **Complexity** | Simpler to build, test, debug | Harder to reason about (ordering, late data, backpressure) |
| **Cost** | Pay per run (compute scales to zero) | Always-on infrastructure |
| **Use case** | Reporting, analytics, warehouse loading | Fraud detection, real-time dashboards, event-driven architecture |

### Step 3: Data volume and team skills?

- **< 10 GB, small team** --> DuckDB or dbt + managed EL (Fivetran)
- **10-500 GB, SQL-heavy team** --> dbt + ADF/Fivetran + Airflow
- **500 GB - 10 TB, mixed skills** --> Spark + Airflow + managed EL
- **> 10 TB, dedicated platform team** --> Spark/Databricks + Kafka + Airflow + custom EL
- **SQL Server shop** --> SSIS + dbt + Synapse Pipelines
- **Real-time requirement** --> Kafka + Kafka Streams/Flink + materialized views

### Step 4: Cloud provider alignment?

| Cloud | Native Integration | Native Orchestration | Native Transformation | Streaming |
|---|---|---|---|---|
| **Azure** | ADF, Synapse Pipelines | ADF triggers, Synapse | Synapse SQL/Spark, Databricks | Event Hubs (Kafka API) |
| **AWS** | Glue, DMS, AppFlow | Step Functions, MWAA (Airflow) | Glue Spark, Redshift, EMR | Kinesis, MSK (managed Kafka) |
| **GCP** | Dataflow, Cloud Data Fusion | Cloud Composer (Airflow) | BigQuery, Dataproc (Spark) | Pub/Sub, managed Kafka |
| **Multi-cloud** | Fivetran, Airbyte | Airflow (self-hosted, Astronomer) | dbt, Spark on K8s | Confluent Cloud (Kafka) |

### Step 5: Governance and compliance?

| Requirement | Recommended Approach |
|---|---|
| Data lineage (end-to-end) | dbt lineage + OpenLineage + Atlan/Collibra for catalog |
| PII masking / GDPR | Mask at ingestion (ADF mapping data flows, NiFi processors, custom Spark UDFs) |
| Data contracts | Schema registry (Confluent, Glue) for streaming; dbt contracts for warehouse |
| Audit trail | NiFi provenance, ADF monitoring, Airflow audit logs, Kafka topic retention |
| Data quality SLAs | dbt tests + Great Expectations + freshness monitoring (elementary, Monte Carlo) |

## Cross-Domain References

| Technology | Cross-Reference | When |
|---|---|---|
| DuckDB | `duckdb` skill | DuckDB as a transformation engine for small-to-medium ETL workloads |
| SQL Server | The database plugin's `sql-server` skill | SSIS platform context, SQL Server as source/target |
| Databricks | The database plugin's `databricks` skill | Spark on Databricks, Delta Lake, Unity Catalog |
| Kafka | Future: the messaging plugin's `kafka` skill | Kafka as messaging infrastructure (non-ETL use cases) |

## Subcategory Routing

| Request Pattern | See Skill |
|---|---|
| **Orchestration** | |
| Airflow, DAG, XCom, TaskFlow, Executor, Provider, scheduler | `airflow` |
| SSIS, DTSX, Integration Services, SQL Agent, SSISDB | `ssis` |
| Orchestration comparison, Airflow vs ADF, scheduling strategy | `orchestration` |
| **Transformation** | |
| dbt, model, ref(), source(), macro, Jinja, incremental, snapshot | `dbt-core` |
| dbt Cloud, dbt Cloud CLI, dbt Mesh, Semantic Layer | `dbt-cloud` |
| Spark, PySpark, DataFrame, RDD, SparkSQL, Catalyst, Tungsten | `spark` |
| DuckDB for ETL, local transformation, file-based SQL | `duckdb` |
| Transformation comparison, dbt vs Spark, SQL vs DataFrame | `transformation` |
| **Integration / EL** | |
| Azure Data Factory, ADF, pipeline, linked service, integration runtime | `adf` |
| NiFi, processor, flow file, process group, provenance | `nifi` |
| Informatica, IDMC, PowerCenter, mapping, pushdown optimization | `informatica` |
| Talend, tMap, tFileInput, Job, Route, ESB | `talend` |
| Fivetran, connector, sync, transformation, destination | `fivetran` |
| AWS Glue, crawler, job, catalog, bookmark, DynamicFrame | `aws-glue` |
| Synapse Pipelines, Synapse workspace, Spark pool, SQL pool | `synapse-pipelines` |
| Integration comparison, ADF vs Fivetran, managed vs self-hosted | `integration` |
| **Streaming** | |
| Kafka, topic, partition, consumer group, offset, Connect, Streams | `kafka` |
| Streaming comparison, Kafka vs Kinesis, event-driven architecture | `streaming` |

## Anti-Patterns

1. **"Transform in the extraction layer"** -- Running complex business logic inside ADF data flows or Fivetran transformations. These tools are optimized for data movement, not computation. Extract raw, transform in the warehouse (dbt) or in Spark.
2. **"One monolithic pipeline"** -- A single Airflow DAG or SSIS package that extracts, transforms, validates, and loads everything. Break pipelines into discrete stages (extract, stage, transform, publish) with clear contracts between them.
3. **"No idempotency"** -- Pipelines that append without deduplication. Every rerun creates duplicates. Use MERGE, partition overwrite, or upsert patterns so re-execution is safe.
4. **"Full loads because CDC is hard"** -- Scanning entire source tables every run. This doesn't scale and puts unnecessary load on production databases. Invest in CDC (Debezium, log-based) or at minimum timestamp-based incremental extraction.
5. **"Ignoring late-arriving data"** -- Assuming all data arrives within the batch window. Late-arriving facts corrupt aggregations. Design for reprocessing: re-run affected partitions, use watermarks, maintain correction pipelines.
6. **"Treating the warehouse as the data quality layer"** -- Pushing all validation downstream. By the time analysts find bad data, it has already propagated. Validate at ingestion with data contracts and circuit breakers.

## Reference Files

- `references/concepts.md` -- ETL/ELT fundamentals (batch vs streaming, CDC patterns, SCD types, data quality dimensions, schema evolution, partitioning strategies, error handling). Read for architecture and comparison questions.
- `references/paradigm-orchestration.md` -- When and why to use orchestration tools (DAG-based scheduling, dependency management, workflow automation). Read when evaluating orchestration approaches.
- `references/paradigm-transformation.md` -- When and why to use transformation tools (SQL-first vs DataFrame, in-warehouse vs external engine). Read when evaluating transformation approaches.
- `references/paradigm-integration.md` -- When and why to use integration/EL tools (managed vs self-hosted, visual vs code, connector ecosystems). Read when evaluating data movement approaches.
- `references/paradigm-streaming.md` -- When and why to use streaming tools (event-driven architecture, exactly-once semantics, backpressure). Read when evaluating real-time requirements.
