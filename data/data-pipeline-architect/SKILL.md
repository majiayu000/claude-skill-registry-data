---
name: data-pipeline-architect
description: Designs ETL/ELT data pipelines with proper extraction, transformation, and loading patterns, including orchestration, error handling, and data quality validation.
license: MIT
---

# Data Pipeline Architect

This skill provides guidance for designing robust, scalable data pipelines that move data reliably from sources to destinations.

## Core Competencies

- **ETL vs ELT**: Traditional Extract-Transform-Load vs modern Extract-Load-Transform patterns
- **Orchestration**: Airflow, Dagster, Prefect, dbt for workflow management
- **Data Quality**: Validation, monitoring, lineage tracking
- **Scalability**: Batch vs streaming, partitioning, parallelization

## Pipeline Design Process

### 1. Requirements Analysis

To begin pipeline design, gather:
- Source systems and data formats (APIs, databases, files, streams)
- Target destinations (data warehouse, lake, lakehouse)
- Freshness requirements (real-time, hourly, daily)
- Data volume and velocity estimates
- Quality and compliance requirements

### 2. Architecture Selection

**Batch Pipelines** - For periodic bulk processing:
- Schedule-driven (hourly, daily, weekly)
- Higher latency tolerance
- Simpler error recovery (re-run entire batch)
- Tools: Airflow, dbt, Spark

**Streaming Pipelines** - For real-time requirements:
- Event-driven processing
- Sub-second to minute latency
- Complex state management
- Tools: Kafka, Flink, Spark Streaming

**Hybrid Approaches** - Lambda or Kappa architecture:
- Batch layer for completeness
- Speed layer for low latency
- Serving layer for queries

### 3. ETL vs ELT Decision

**ETL (Transform before Load)**:
- When target has limited compute
- When transformation reduces data volume significantly
- When sensitive data must be masked before landing
- Legacy data warehouse patterns

**ELT (Transform after Load)**:
- Modern cloud warehouses with cheap compute
- When raw data preservation is needed
- When transformations change frequently
- dbt-style transformations in warehouse

### 4. Pipeline Components

**Extraction Layer**:
- Full extraction vs incremental (CDC, timestamp-based)
- API pagination and rate limiting
- Connection pooling and retry logic
- Schema detection and drift handling

**Transformation Layer**:
- Data cleansing and standardization
- Business logic application
- Aggregation and denormalization
- Type casting and null handling

**Loading Layer**:
- Upsert strategies (merge, delete+insert)
- Partitioning schemes (time, hash, range)
- Index management
- Transaction boundaries

### 5. Error Handling Patterns

```
┌─────────────────────────────────────────────────────────┐
│                    Pipeline Execution                    │
├─────────────────────────────────────────────────────────┤
│  ┌─────────┐    ┌───────────┐    ┌──────────┐          │
│  │ Extract │───▶│ Transform │───▶│   Load   │          │
│  └────┬────┘    └─────┬─────┘    └────┬─────┘          │
│       │               │               │                 │
│       ▼               ▼               ▼                 │
│  ┌─────────┐    ┌───────────┐    ┌──────────┐          │
│  │  Retry  │    │ Dead Letter│    │ Rollback │          │
│  │ w/Backoff│   │   Queue   │    │ Checkpoint│          │
│  └─────────┘    └───────────┘    └──────────┘          │
└─────────────────────────────────────────────────────────┘
```

- **Retry with backoff**: Transient failures (network, rate limits)
- **Dead letter queues**: Poison messages that can't be processed
- **Checkpointing**: Resume from last successful point
- **Idempotency**: Safe to re-run without duplicates

### 6. Data Quality Framework

Implement checks at each stage:

| Stage | Check Type | Example |
|-------|------------|---------|
| Extract | Completeness | Row count matches source |
| Extract | Freshness | Data timestamp within SLA |
| Transform | Validity | Values in expected ranges |
| Transform | Uniqueness | Primary keys unique |
| Load | Reconciliation | Target matches source totals |
| Load | Integrity | Foreign keys valid |

### 7. Monitoring and Observability

Essential metrics to track:
- Pipeline duration and trends
- Row counts at each stage
- Error rates and types
- Data freshness (time since last successful run)
- Resource utilization

Alert on:
- SLA breaches (data not fresh)
- Anomalous row counts (±20% from baseline)
- Schema changes in sources
- Repeated failures

## Common Patterns

### Slowly Changing Dimensions (SCD)

- **Type 1**: Overwrite (no history)
- **Type 2**: Add row with validity dates
- **Type 3**: Previous value column
- **Type 4**: History table

### Incremental Processing

```sql
-- Timestamp-based incremental
SELECT * FROM source
WHERE updated_at > {{ last_run_timestamp }}

-- CDC-based (Change Data Capture)
-- Captures inserts, updates, deletes from transaction log
```

### Idempotent Loads

```sql
-- Delete + Insert pattern
DELETE FROM target WHERE date_partition = '2024-01-15';
INSERT INTO target SELECT * FROM staging WHERE date_partition = '2024-01-15';

-- Merge/Upsert pattern
MERGE INTO target t
USING staging s ON t.id = s.id
WHEN MATCHED THEN UPDATE SET ...
WHEN NOT MATCHED THEN INSERT ...
```

## References

- `references/orchestration-patterns.md` - Airflow, Dagster, Prefect patterns
- `references/data-quality-checks.md` - Validation frameworks and rules
- `references/pipeline-templates.md` - Common pipeline architectures
