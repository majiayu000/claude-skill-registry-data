---
name: building-dbt-models
description: Build well-structured dbt models — staging/intermediate/marts layers, ref() and source(), materializations, and incremental models with the right strategy. Use when creating or refactoring dbt models, choosing table vs view vs incremental, structuring a dbt project, or writing incremental logic.
---

# Building dbt Models

## When to use

- Creating or refactoring `.sql` models in a dbt project.
- Deciding materialization (view / table / incremental / ephemeral).
- Structuring layers (staging → intermediate → marts).
- Writing incremental models for large, growing tables.
- Do NOT use for test authoring (use `testing-dbt-projects`) or run failures
  (use `debugging-dbt-runs`).

## Workflow

```
- [ ] Place the model in the right layer (staging/intermediate/marts)
- [ ] Reference upstream only via ref()/source() — never hard-coded names
- [ ] Choose materialization by size and refresh needs
- [ ] For incremental, set unique_key + is_incremental() filter
- [ ] Add a schema.yml entry with tests
```

1. **Layer it.** `staging/` = one model per source table, light renaming/typing,
   materialized as views. `intermediate/` = reusable business logic. `marts/` =
   final dimensional models consumed by BI, materialized as tables.
2. **Reference correctly.** Use `{{ ref('stg_orders') }}` and
   `{{ source('shop', 'orders') }}` so dbt builds the DAG and manages
   environments. Never write raw schema.table.
3. **Pick materialization:** view (cheap, always fresh, small), table (fast reads,
   rebuilt each run), incremental (large append/update tables), ephemeral (inlined
   CTE, no object).
4. **Incremental models** process only new/changed rows.

## Patterns

**Staging model** — one per source, thin and consistent:

```sql
-- models/staging/shop/stg_orders.sql
with source as (select * from {{ source('shop', 'orders') }})
select
    order_id,
    customer_id,
    cast(order_ts as timestamp) as ordered_at,
    round(amount_cents / 100.0, 2) as amount
from source
```

**Incremental model** — filter to new rows and set an idempotent merge key:

```sql
{{ config(materialized='incremental', unique_key='order_id',
          incremental_strategy='merge') }}

select * from {{ ref('stg_orders') }}
{% if is_incremental() %}
  -- only rows newer than what we already loaded, with a lookback for late data
  where ordered_at >= (select coalesce(max(ordered_at), '1900-01-01') from {{ this }})
                      - interval '3 days'
{% endif %}
```

The `unique_key` + `merge` makes re-runs idempotent; the lookback catches
late-arriving rows. On BigQuery/Spark, prefer `insert_overwrite` on a date
partition.

## Common pitfalls

- **Hard-coded table names** instead of `ref()`/`source()` — breaks the DAG,
  lineage, and environment switching.
- **Incremental without `unique_key`** — re-runs append duplicates.
- **`max(id)` incremental filter with no lookback** — silently drops late data.
- **Business logic in staging** — keep staging thin; joins/aggregation belong in
  intermediate/marts.
- **Everything materialized as `table`** — wastes warehouse time; use views for
  small/cheap models and incremental for large ones.
- **One giant model** — split into intermediate steps for testability and reuse.

## References

- [dbt project structure conventions](references/STRUCTURE.md)
