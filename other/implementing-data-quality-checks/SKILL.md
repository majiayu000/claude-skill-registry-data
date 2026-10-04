---
name: implementing-data-quality-checks
description: Add data quality checks to pipelines — freshness, volume/row-count anomalies, schema drift, null/uniqueness/referential integrity, and value distributions — using dbt tests, Great Expectations, or Soda, and deciding warn vs block. Use when adding data quality validation, catching bad data before it reaches consumers, setting up freshness/volume checks, or defining expectations.
---

# Implementing Data Quality Checks

## When to use

- Adding validation so bad data is caught before consumers see it.
- Setting up freshness, volume, schema-drift, or integrity checks.
- Choosing a tool (dbt tests, Great Expectations, Soda) and where to place checks.
- Do NOT use for dbt-specific test syntax only (use `testing-dbt-projects` for
  the dbt details).

## The six dimensions to cover

1. **Freshness** — did the data arrive on time? (max load timestamp vs SLA)
2. **Volume** — is the row count in the expected range? (catches partial loads and
   duplication)
3. **Schema** — did columns/types change unexpectedly? (drift)
4. **Completeness** — required fields not null.
5. **Uniqueness / integrity** — keys unique, foreign keys valid.
6. **Validity / distribution** — values in allowed ranges/sets; no sudden
   distribution shifts.

## Workflow

```
- [ ] Put blocking checks at the entry point (raw/staging) so bad data stops early
- [ ] Cover the six dimensions on critical tables
- [ ] Decide warn vs block per check by business impact
- [ ] Route failures to alerts + a quarantine/failure store
- [ ] Add reconciliation between source and target for critical flows
```

1. **Check early.** Validate at ingestion/staging so bad data fails fast rather
   than propagating into marts and dashboards.
2. **Cover the six dimensions** on tables that feed decisions/SLAs.
3. **Warn vs block.** Block (fail the run) on integrity-critical checks; warn on
   soft signals. Blocking everything causes alert fatigue and pipeline gridlock.
4. **Act on failures** — alert an owner and store failing rows for triage;
   optionally quarantine and continue.

## Patterns

**Great Expectations** — declarative expectations on a batch:

```python
validator.expect_column_values_to_not_be_null("order_id")
validator.expect_column_values_to_be_unique("order_id")
validator.expect_column_values_to_be_between("amount", min_value=0)
validator.expect_table_row_count_to_be_between(min_value=1000)
```

**Soda (SodaCL)** — freshness, volume, and integrity in YAML:

```yaml
checks for fct_orders:
  - freshness(ordered_at) < 24h
  - row_count between 1000 and 1000000
  - missing_count(order_id) = 0
  - duplicate_count(order_id) = 0
```

**Volume anomaly** — compare today's count to the trailing average and alert on a
large deviation, catching partial loads and accidental duplication.

## Common pitfalls

- **Checking only at the end** — bad data has already reached consumers; validate
  at entry.
- **Blocking on every soft check** — alert fatigue; reserve blocking for
  integrity-critical rules.
- **No owner/routing** — failures no one sees are worthless; route to a person and
  a failure store.
- **Freshness ignored** — stale data looks "correct" but is wrong; it is the most
  commonly missed dimension.
- **No reconciliation** — row-level checks pass while totals drift from source;
  add source-vs-target count/sum reconciliation for critical flows.
- **Static thresholds on seasonal data** — use trailing baselines, not fixed
  numbers, where volume varies.
