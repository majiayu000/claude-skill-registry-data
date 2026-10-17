---
name: data-ml-pipelines
description: Ship data and ML pipelines that hold — quality checks, reproducibility, lineage, drift monitoring.
version: 1
triggers: data pipeline, ml pipeline, data quality, lineage, drift monitoring, etl
category: Engineering & code
blurb: Ship data and ML pipelines that hold — quality checks, reproducibility, lineage and drift monitoring.
archetype: knowledge
example: Design a data pipeline with quality checks and lineage.
---

# Data & ML Pipelines

Data breaks quietly and models lie politely. Pipelines need the same rigor as code: contracts, tests, versioning, and monitoring — or they rot silently.

## When to use
- Ingesting, transforming, or exporting data (batch or stream).
- Training, evaluating, registering, or serving ML models.
- Debugging "the numbers changed" or "the model got worse".

## Method
1. **Contracts at the edges**: schemas + expectations for every input/output (types, ranges, nullability); validate on arrival; refuse bad data loudly — never coerce silently.
2. **Idempotent steps**: rerunnable stages; exactly-once effects at sinks (upserts/keys); safe retries; cheap backfills.
3. **Orchestration**: explicit step dependencies; schedules documented; failures alert + retry; no unrecorded "just rerun it" habits.
4. **Quality gates between stages**: row counts, freshness, null/uniqueness/distribution checks; quarantine bad partitions; pipeline-health dashboards.
5. **Lineage & versioning**: source → transform → sink tracked; code + config + data snapshots versioned where it matters; same inputs → same outputs.
6. **ML — data hygiene**: leakage checks (time/target/cross-splits); split by time/user when reality is temporal; class-balance awareness; feature stores only when justified.
7. **ML — lifecycle**: reproducible training (seeds, pinned env); eval suites versioned with the model; registry + model card (data, metrics, limits); deployment pattern (batch vs service) with latency/cost budgets.
8. **Monitoring & drift**: input drift, output drift, performance decay vs baselines; thresholds tied to a retraining policy — retraining is a pipeline, not a heroic weekend.

## Quality gates
- [ ] Schemas + quality checks active at every boundary.
- [ ] Pipelines rerun idempotently; a backfill was tested once.
- [ ] Training reproducible; model card + registry entry exist.
- [ ] Drift/performance monitoring live with alert thresholds.

## Red lines
- No PII in training data without a lawful basis (`privacy-compliance`); no silent coercion; no model to prod without offline eval + rollout plan.

## Related
`backend-engineering` · `agent-evaluation` · `sql-engineering`.
