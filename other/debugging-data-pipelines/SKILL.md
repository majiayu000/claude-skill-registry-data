---
name: debugging-data-pipelines
description: Systematically root-cause data pipeline failures and data incidents — job errors, wrong or missing data, duplicates, and freshness misses — by tracing lineage upstream, isolating the failing stage, reconciling against source, and planning a safe fix and backfill. Use when a pipeline fails, numbers look wrong, data is missing or duplicated, a dashboard is stale, or a stakeholder reports a data discrepancy.
---

# Debugging Data Pipelines

## When to use

- A pipeline job failed, or output data is wrong/missing/duplicated.
- A dashboard is stale or a metric doesn't reconcile with the source.
- A stakeholder reports a discrepancy and you must find the cause.
- Do NOT use for tool-specific run errors already covered by
  `debugging-dbt-runs` / `debugging-airflow-pipelines` (start there, then use
  this for data-correctness incidents).

## Workflow

```
- [ ] Define the symptom precisely (which table, column, rows, time window)
- [ ] Trace lineage upstream to find the first stage where data is wrong
- [ ] Isolate: is it a code bug, bad input, late data, or a run failure?
- [ ] Reconcile the suspect stage against its source (counts/sums)
- [ ] Fix root cause, then plan an idempotent backfill of affected windows
- [ ] Add a check so it can't recur silently
```

1. **Pin the symptom.** "Revenue for 2026-01-15 is ~30% low in `fct_orders`" is
   debuggable; "numbers look off" is not. Get the table, column, rows, and window.
2. **Trace lineage upstream.** Walk from the wrong output backward through models/
   tasks to find the **first** stage where the data is already wrong. Binary-search
   the DAG rather than reading every stage.
3. **Classify the cause:** code change, bad/late source data, a failed/partial
   run, or a non-idempotent duplicate.
4. **Reconcile** the suspect stage vs its input (row counts, key counts, sums) to
   confirm where the delta appears.
5. **Fix + backfill** the affected windows idempotently (see
   `designing-backfills-and-replays`).
6. **Prevent recurrence** with a targeted data quality check.

## Patterns

**Lineage binary search** — check a stage halfway up the DAG: if its data is
correct, the bug is downstream; if wrong, go further up. Repeat.

**Reconcile source vs target** for the affected window:

```sql
-- Do counts/sums match between the stage and its input for the bad window?
SELECT 'source' AS layer, COUNT(*) n, SUM(amount) total
FROM staging.orders WHERE order_date = DATE '2026-01-15'
UNION ALL
SELECT 'target', COUNT(*), SUM(amount)
FROM marts.fct_orders WHERE order_date = DATE '2026-01-15';
```

A count gap → dropped/filtered rows or a failed partial load. A sum gap with equal
counts → a transformation/logic bug. Higher target count → duplication
(non-idempotent load).

**Timeline check** — correlate the incident window with deploys, source schema
changes, and run history; most incidents start at a change.

## Common pitfalls

- **Fixing symptoms downstream** — patching the mart when the bug is in staging
  means it recurs; fix the first bad stage.
- **Manual one-off fixes to prod data** — un-auditable and unrepeatable; fix the
  code and re-run idempotently instead.
- **Reading the whole DAG linearly** — binary-search lineage instead.
- **Skipping reconciliation** — guessing where data diverged wastes time; measure
  counts/sums per stage.
- **No preventive check after the fix** — the same class of bug returns unseen.
