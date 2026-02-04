---
name: data-warehouse
description: Data warehouse (大数据/数仓) ops skill for designing and operating analytical data platforms. Use for tasks like defining source-of-truth, building ETL/ELT pipelines, dimensional modeling (star schema), data quality checks, partitioning strategies, cost/performance tuning, governance, lineage, and SLA monitoring.
---

# data-warehouse

Use this skill for 大数据/数仓（DW）建设与运维：从数据接入到指标交付与治理。

## Defaults / assumptions to confirm

- Warehouse tech: BigQuery/Snowflake/Redshift/Hive/ClickHouse/etc.
- Orchestration: Airflow/Dagster/Argo/dbt
- Ingestion: CDC vs batch, streaming (Kafka) vs file
- Data consumers: BI dashboards, product analytics, ML features

## Core outputs

- Warehouse architecture (sources → staging → warehouse → marts)
- Data model (facts/dimensions) + metric definitions
- Pipeline plan (DAGs, schedules, dependencies, SLAs)
- Data quality plan (checks, thresholds, alerts)
- Cost/performance plan (partitioning, clustering, materialization)
- Governance plan (access control, PII handling, retention)

## Workflow

1) Understand the business questions
- What decisions will this warehouse support?
- Define critical metrics and their definitions (single source of truth).

2) Source & ingestion design
- Identify systems of record and ownership.
- Choose ingestion: CDC for mutable OLTP, append-only logs for events.
- Define late-arriving data strategy and backfills.

3) Modeling (practical)
- Prefer star schema for BI: Fact tables + Dimension tables.
- Keep grain explicit (one row represents what?).
- Separate raw/staging from curated models; avoid mixing.

4) ETL/ELT pipelines
- Define DAGs with clear inputs/outputs and idempotency.
- Handle retries, partial failures, and reprocessing windows.
- Provide backfill procedures and runbook.

5) Data quality & observability
- Validate freshness, volume, schema drift, null ratios, referential consistency (logical).
- Add anomaly detection for key metrics.
- Track pipeline success rate, duration, and SLA misses.

6) Performance & cost
- Partition by date/time for large facts; cluster by common filters/joins.
- Materialize expensive queries (summary tables, incremental models).
- Control scan cost with column pruning and predicate pushdown.

7) Governance & security
- PII classification, masking, and retention.
- RBAC/ABAC for datasets; audit logging.
- Document lineage and ownership for each table/model.

## Templates

### Table spec
- Name:
- Grain:
- Partition/cluster keys:
- Key columns:
- Sources:
- Refresh cadence:
- Consumers:
- Quality checks:
- Owner:

### Metric spec
- Name:
- Definition:
- Numerator/denominator:
- Filters:
- Time window:
- Known caveats:

