---
name: sota-data-engineering
description: >-
  State-of-the-art data engineering rules (2026) for building and auditing
  data pipelines and analytics infrastructure. Covers architecture and
  modeling (ELT, lakehouse vs warehouse, dimensional models, medallion
  layering), pipeline and orchestration discipline (idempotency, incremental
  loads, backfills, dbt-style transformations), streaming and CDC (Kafka,
  exactly-once reality, schema evolution, Debezium-style capture), data
  quality and contracts, columnar storage and table-format performance
  (Parquet, Iceberg, Delta), and pipeline operations/governance. Use when
  designing, implementing, reviewing, or auditing batch/streaming pipelines,
  warehouses, or lakehouses. Trigger keywords: data pipeline, ETL, ELT,
  Kafka, streaming, data warehouse, dbt, Airflow, orchestration, data
  quality, lakehouse, Iceberg, Delta, CDC, Parquet, backfill, watermark,
  Spark, DuckDB, data contract, medallion, dimensional model.
---

# SOTA Data Engineering

Expert rules for analytical data systems: pipelines, streaming, warehousing,
lakehouse storage, data quality, and operations. OLTP schema/query/index craft
is owned by `sota-databases` — reference it, do not duplicate it. Outbox and
event-driven service patterns live in `sota-architecture`; backpressure
mechanics in `sota-async-concurrency`; PII handling in
`sota-privacy-compliance` (or `sota-code-security` if absent).

Two modes. Pick by intent, then load only the `rules/` files the task needs.

## BUILD mode

Use when designing or implementing pipelines, models, streaming jobs, or
storage layouts.

1. **Size the problem first.** Read `rules/01-architecture-and-modeling.md`
   before choosing tools. Most "big data" is small data; DuckDB/Polars on one
   node before a distributed engine. ELT into a warehouse/lakehouse is the
   default shape, not a decision to revisit per pipeline.
2. **Idempotency is the prime directive.** Every pipeline you write must be
   safe to rerun for any interval at any time. No blind appends. Design the
   write strategy (partition overwrite / merge key / insert-overwrite) before
   the transform logic (`rules/02-pipelines-and-orchestration.md`).
3. **Batch unless a consumer needs sub-minute data.** Justify streaming in
   writing before building it (`rules/03-streaming-and-cdc.md`).
4. **Quality checks ship with the pipeline, not after.** Every new model gets
   freshness, volume, uniqueness, and not-null checks tiered block/warn
   (`rules/04-data-quality-and-contracts.md`).
5. **Decide the physical layout when you create the table.** Partitioning,
   clustering/sort, file sizing, and the maintenance job are part of the
   table's definition (`rules/05-storage-and-performance.md`).
6. **Ship with operability.** Dev/prod isolation, write-audit-publish for
   risky changes, freshness alerting, a runbook entry
   (`rules/06-operations-and-governance.md`).

## AUDIT mode

Use when reviewing an existing pipeline repo, dbt project, streaming topology,
or warehouse.

Procedure:
1. Inventory: orchestrator + scheduler config, transformation tool (dbt or
   other), storage/table formats, streaming components, quality tooling,
   environments. Read the actual DAGs/models — never audit from README claims.
2. Load the rules files matching what exists (no Kafka → skip 03).
3. Verify every finding against real code/config/SQL. Confirm a non-idempotent
   write by reading the write statement, not by inferring from naming.
4. Report findings in the format below, ordered by severity.

Severity conventions:
- **CRITICAL** — data corruption or silent wrongness: non-idempotent writes
  that double-count on retry, reruns that duplicate or lose data, CDC deletes
  not applied, PII landing in unprotected zones, prod credentials in dev.
- **HIGH** — likely incident or unbounded cost: no failure alerting on
  business-critical pipelines, unbounded retries, full-table rescans of large
  sources each run, no backfill path, schema changes that break consumers.
- **MEDIUM** — erodes trust/efficiency: missing quality checks, `SELECT *`
  staging, small-files accumulation, no documentation/lineage, warn-tier
  checks failing for weeks.
- **LOW** — hygiene: naming inconsistency, missing column descriptions,
  suboptimal compression.

Finding format:
```
[SEVERITY] <one-line title>
Where: <file:line / model / DAG / topic>
Evidence: <the actual code/config/SQL that proves it>
Impact: <what goes wrong, when>
Fix: <concrete change, smallest safe diff>
```

## Rules index

| File | Read this when... |
|---|---|
| `rules/01-architecture-and-modeling.md` | Choosing engines/architecture (warehouse vs lakehouse vs DuckDB), designing layers (staging/core/mart), dimensional modeling, SCDs, One Big Table, semantic layers, evaluating a data-mesh pitch. |
| `rules/02-pipelines-and-orchestration.md` | Writing or reviewing any batch pipeline: idempotency, incremental loads, watermarks, late data, backfills, Airflow/orchestrator DAG design, dbt project discipline, scheduling strategy. |
| `rules/03-streaming-and-cdc.md` | Anything Kafka/Flink/CDC: deciding streaming vs micro-batch, partition keys, consumer groups, offsets, exactly-once claims, schema registry, Debezium, tombstones, DLQs, windowing. |
| `rules/04-data-quality-and-contracts.md` | Defining data contracts, adding expectation tests, tiering checks block vs warn, drift/anomaly detection, lineage, responding to a data incident, testing transforms in CI. |
| `rules/05-storage-and-performance.md` | Creating tables, Parquet tuning, partitioning vs clustering, small-files/compaction, Iceberg/Delta features and maintenance, compression, reducing scan cost / warehouse spend. |
| `rules/06-operations-and-governance.md` | Environments and deployment of pipeline changes, write-audit-publish, blue-green tables, access control, GDPR deletion in lakehouses, pipeline observability, runbooks. |

## Top 10 non-negotiables

1. **Every pipeline is idempotent.** Rerunning any task for any interval
   produces the same result. Overwrite partitions or MERGE on keys; a blind
   `INSERT INTO ... SELECT` in a scheduled job is a CRITICAL finding.
2. **No silent failure.** Business-critical pipelines have failure AND
   freshness alerts routed to an owner. A pipeline that fails quietly is
   worse than one that doesn't exist — people keep trusting its output.
3. **Right-size the engine.** Under ~100 GB working set, single-node
   DuckDB/Polars beats a cluster on cost, speed, and ops. Spark/distributed
   engines need a stated reason (data volume, existing platform, ML scale).
4. **Incremental by watermark, never by `NOW()` arithmetic in the task.**
   Process data by the orchestrator-supplied logical interval; reruns and
   backfills must produce identical results regardless of wall-clock time.
5. **Schema changes are backward-compatible or coordinated.** Add columns
   freely; never rename, retype, or drop in place. Producers that break
   consumers without a contract bump are HIGH findings.
6. **Quality checks are tiered.** Block (fail the pipeline, stop downstream)
   for uniqueness/null/contract violations on critical models; warn (alert,
   continue) for distribution drift. Everything-blocks and nothing-blocks are
   both failure modes.
7. **Streaming requires a written justification.** Name the consumer that
   needs sub-minute latency. Hourly micro-batch covers most "real-time"
   requests at a tenth of the operational cost.
8. **Exactly-once is end-to-end or it's a lie.** Kafka transactions cover
   Kafka; your sink makes it true via idempotent writes (merge keys,
   deterministic IDs). Audit the sink, not the producer config.
9. **No `SELECT *` across layer boundaries.** Staging models enumerate,
   rename, and type columns. Upstream schema drift must break loudly in your
   staging layer, not silently in a dashboard.
10. **Tables get maintenance from day one.** Compaction, snapshot/manifest
    cleanup, and retention jobs are part of creating an Iceberg/Delta table.
    A lakehouse without maintenance jobs is a slow-motion outage.
