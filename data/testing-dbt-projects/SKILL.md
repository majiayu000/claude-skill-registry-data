---
name: testing-dbt-projects
description: Add data quality tests to a dbt project — generic tests (unique, not_null, accepted_values, relationships), singular tests, unit tests, dbt-utils and dbt-expectations packages, and source freshness. Use when adding tests to dbt models, catching data quality regressions, validating assumptions, or setting up source freshness checks.
---

# Testing dbt Projects

## When to use

- Adding or improving tests on dbt models and sources.
- Guarding a known assumption (grain, referential integrity, value ranges).
- Validating transformation logic with fixed inputs (unit tests).
- Setting up source freshness monitoring.
- Do NOT use for optimizing model SQL (use `building-dbt-models`).

## Workflow

```
- [ ] Add grain test: unique + not_null on the primary/surrogate key
- [ ] Add relationships tests for every foreign key
- [ ] Add accepted_values / range tests for constrained columns
- [ ] Add singular/unit tests for critical business logic
- [ ] Configure source freshness
- [ ] Run: dbt test (and dbt build to test as you materialize)
```

1. **Test the grain first** — `unique` + `not_null` on the key catches the most
   common and most damaging bug (fan-out duplicates).
2. **Test relationships** — every foreign key should point to an existing parent.
3. **Constrain values** — `accepted_values` for enums, range checks for numerics.
4. **Unit-test logic** — for tricky CASE/window/dedup logic, assert exact output
   from fixed input (dbt 1.8+ `unit_tests`).
5. **Freshness** — alert when a source stops updating before models run stale.

## Patterns

**Generic tests in schema.yml:**

```yaml
models:
  - name: fct_orders
    columns:
      - name: order_id
        tests: [unique, not_null]
      - name: customer_id
        tests:
          - relationships:
              to: ref('dim_customer')
              field: customer_id
      - name: status
        tests:
          - accepted_values:
              values: ["placed", "shipped", "delivered", "cancelled"]
```

**Range/expression test (dbt-utils / dbt-expectations):**

```yaml
- name: amount
  tests:
    - dbt_expectations.expect_column_values_to_be_between:
        min_value: 0
```

**Unit test (fixed input → expected output):**

```yaml
unit_tests:
  - name: test_net_amount_excludes_tax
    model: fct_orders
    given:
      - input: ref('stg_orders')
        rows:
          - { order_id: 1, gross: 110, tax: 10 }
    expect:
      rows:
        - { order_id: 1, net_amount: 100 }
```

**Source freshness:**

```yaml
sources:
  - name: shop
    freshness:
      warn_after: { count: 12, period: hour }
      error_after: { count: 24, period: hour }
    loaded_at_field: _loaded_at
```

## Common pitfalls

- **No uniqueness test on the grain** — duplicates slip through and inflate metrics.
- **Testing only staging** — bugs are introduced in joins; test marts too.
- **Warn severity on critical tests** — set `severity: error` (or thresholds) so
  bad data actually blocks the run.
- **Slow tests on huge tables** — add `where`/`limit` config or sampling; use
  `store_failures` to inspect offenders.
- **Unit tests over real data** — unit tests must use fixed `given` rows, not
  live tables.

## References

- [Recommended test coverage per layer](references/COVERAGE.md)
