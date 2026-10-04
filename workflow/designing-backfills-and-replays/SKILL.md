---
name: designing-backfills-and-replays
description: Plan and run safe data backfills and replays — idempotent reprocessing of historical windows, partition-by-partition execution, isolating backfill compute from production, verifying results, and avoiding double-counting or changed history. Use when backfilling a new or fixed model, reprocessing after a bug, replaying events, or loading history for a new pipeline without corrupting existing data.
---

# Designing Backfills and Replays

## When to use

- Loading history for a new model/pipeline.
- Reprocessing past windows after fixing a transformation bug.
- Replaying events or re-deriving a table from raw.
- Do NOT use for normal incremental runs (use `building-dbt-models` /
  `authoring-airflow-dags`).

## Why it deserves care

Backfills are the most dangerous routine operation in data engineering: they
rewrite history. Done wrong, they double-count, change yesterday's numbers, or
overload production. Done right, they are boring and repeatable. The prerequisite
is idempotency (see `writing-idempotent-transformations`).

## Workflow

```
- [ ] Confirm the transform is idempotent (rerun == run once) BEFORE backfilling
- [ ] Define the exact window and partition granularity
- [ ] Dry-run one partition; verify counts/sums vs source
- [ ] Run partition-by-partition (bounded parallelism), not all at once
- [ ] Isolate backfill compute from production workloads
- [ ] Verify totals and reconcile; then resume normal scheduling
```

1. **Prove idempotency first.** If re-running a window can change results, fix that
   before touching history. Backfilling a non-idempotent job multiplies data.
2. **Scope precisely.** Exact start/end and the partition unit (day/hour/region).
3. **Dry-run one partition** and reconcile against source before scaling out.
4. **Chunk the run.** Process partitions in bounded batches so you can monitor,
   pause, and resume — never one giant unbounded job.
5. **Isolate compute.** Use a separate warehouse/cluster/pool so the backfill
   doesn't starve production SLAs.
6. **Verify + resume.** Reconcile totals over the backfilled range, then hand back
   to the normal schedule.

## Patterns

**Idempotent per-partition backfill** — each partition overwrite is independent
and safe to retry:

```bash
# Bounded parallelism, one day at a time; each day overwrites its own partition.
for day in $(seq_dates 2026-01-01 2026-01-31); do
  run_transform --run-date "$day"   # delete-insert / MERGE for that day only
done
```

**Airflow** — `catchup`/`backfill` reruns intervals; only safe when tasks are
idempotent and parameterized by the data interval. **dbt** — filter the
incremental model to the target window, or `--full-refresh` a bounded window.

**Isolate + throttle** — dedicated warehouse/cluster and a concurrency cap so the
backfill can't degrade live dashboards.

## Common pitfalls

- **Backfilling a non-idempotent job** — duplicates or shifting totals; make it
  idempotent first.
- **One giant unbounded run** — can't monitor or resume, and it overloads
  production; go partition-by-partition.
- **Sharing production compute** — backfills spike load and blow SLAs; isolate.
- **No verification** — assuming success; reconcile counts/sums over the range.
- **Changing logic mid-backfill** — inconsistent history; pin the code version for
  the whole run.
- **Forgetting downstream** — backfilling a base table without refreshing dependent
  marts/aggregates leaves them inconsistent.
