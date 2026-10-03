---
name: backfill
description: Plan and execute historical data backfills with bounded scope, deterministic transformations, idempotent partitions, capacity controls, validation, resumability, and safe downstream reconciliation.
---
# Backfill

Use when historical records must be recomputed, corrected, enriched, migrated, or populated after a pipeline/schema/logic change.

## Procedure
1. Define the exact historical scope, target dataset/fields, transformation revision, source-of-truth inputs, and reason the backfill is needed.
2. Estimate record/byte volume, read/write load, runtime, cost, rate limits, storage growth, and impact on live pipelines or databases before execution.
3. Partition the work into deterministic bounded units with stable identifiers or ranges so progress can be retried, audited, and resumed.
4. Make each unit idempotent or define a safe replace/upsert strategy. Re-running a completed partition must not duplicate or compound the transformation.
5. Freeze or version the transformation and dependencies used for the run so a multi-day backfill does not silently change behavior midstream.
6. Define concurrency and throttling based on source/target capacity. Protect production latency and live ingestion with explicit limits and pause controls.
7. Track checkpoint/progress, failures, retries, input/output counts, and transformation version. Failed partitions should be identifiable without rescanning everything.
8. Validate a small representative sample and aggregate invariants before expanding, then validate counts, quality rules, distributions, and downstream effects after completion.
9. Define how downstream caches, aggregates, indexes, materializations, or consumers are refreshed or invalidated after historical values change.
10. Preserve run metadata and cleanup temporary state only after the final dataset and dependent outputs are verified.

## Decision rules
- A backfill is a production workload and must respect production capacity.
- Never rely on “run the script again” unless the operation is actually idempotent or replace-safe.
- Historical correction can change downstream business metrics; coordinate consumer expectations when semantics change.
- Prefer bounded resumable work over one uncheckpointed full-table/full-history job.

## Quality gate
The backfill is complete when every intended partition is accounted for, retries cannot corrupt results, the exact transformation is traceable, live systems remained within accepted limits, data quality and downstream reconciliation are verified, and the run can be audited or resumed from recorded state.