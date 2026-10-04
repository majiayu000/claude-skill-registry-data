---
name: reviewing-data-pipeline-code
description: Review data engineering pull requests with a data-specific checklist — idempotency, correct grain, incremental logic, cost impact, data quality tests, PII handling, and backward compatibility — that generic code review misses. Use when reviewing a dbt/SQL/Spark/Airflow PR, a data pipeline change, or a new model, and you want to catch data-correctness and cost issues before merge.
---

# Reviewing Data Pipeline Code

## When to use

- Reviewing a PR that changes SQL, dbt models, Spark jobs, or orchestration.
- Adding a new model, transformation, or ingestion step.
- You want to catch data-correctness and cost issues generic review misses.
- Do NOT use for pure application code review (use standard code review).

## The data-engineering review checklist

Copy this into the review and check each item:

```
- [ ] Grain: is the output grain declared and enforced (unique key test)?
- [ ] Idempotency: safe to re-run? upsert/partition-overwrite, not blind append?
- [ ] Incremental: unique_key set? lookback for late data? no missed rows?
- [ ] Correctness: joins can't fan out; NULL/timezone/dedup handled?
- [ ] Tests: unique/not_null/relationships on keys; business-rule checks added?
- [ ] Cost: partition/cluster pruning used? no SELECT *? bounded scans?
- [ ] Backward compat: schema change additive? downstream/exposures considered?
- [ ] PII/security: sensitive fields masked/limited? no secrets in code?
- [ ] Observability: freshness/volume covered for a new critical dataset?
```

## What to look for

1. **Grain and fan-out.** The most damaging bug is a join that multiplies rows.
   Confirm the grain is declared and a uniqueness test guards it.
2. **Idempotency.** Ask: what happens on retry or backfill? Reject blind
   `INSERT`-append; require MERGE/upsert or partition overwrite.
3. **Incremental logic.** Check `unique_key`, the `is_incremental()` filter, and a
   lookback window so late data isn't dropped.
4. **Cost.** In columnar warehouses, look for `SELECT *`, function-wrapped
   partition filters, and unbounded scans — they turn into recurring bills.
5. **Tests + observability.** A new critical model without key tests and freshness
   coverage is a future 2am page.
6. **PII and secrets.** No credentials in code; sensitive columns masked or
   access-controlled.
7. **Backward compatibility.** Schema changes should be additive; flag renames/
   drops and check exposures/downstream models.

## Patterns

**Ask "what happens on re-run?"** for every write path — if the author can't
answer, the change probably isn't idempotent.

**Trace one row** mentally through the change: does the grain hold end to end? Do
joins stay 1:1 or intentionally 1:many with correct aggregation?

**Diff the compiled SQL** for dbt changes to see what actually runs, not just the
Jinja.

## Common pitfalls (in reviews)

- **Approving on style only** — LGTM on formatting while a fan-out join ships.
- **Missing the retry question** — non-idempotent writes pass review and duplicate
  in production.
- **Ignoring cost** — a `SELECT *` on a huge table is correct but expensive
  forever.
- **No test requirement** — new keys/models merge without uniqueness/freshness
  guards.
- **Overlooking downstream** — a "small" schema change breaks marts/dashboards not
  visible in the diff.
