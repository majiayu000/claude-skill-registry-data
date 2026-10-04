---
name: dbt
description: "Build dbt models with refs, data tests, and generated documentation for version-controlled warehouse transformations."
category: devops
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["dbt", "analytics-engineering", "sql", "warehouse", "testing", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# dbt Analytics Engineering AI Skill Guide

## Overview & Engine Architecture

dbt compiles Jinja-SQL models into warehouse DDL/DML, managed via a DAG of `ref()` / `source()` edges. Runs materialize views/tables/incremental models; tests and documentation live beside SQL. Agents keep models thin and tested, prefer incremental strategies for large facts, and never hardcode environment-specific database names inside model bodies.

```
sources.yml -> staging models -> intermediate -> marts
                     |
              dbt compile/run/test
                     |
              warehouse relations + docs
```

## When to use this skill

- Versioned SQL transforms in Snowflake/BigQuery/Redshift/DuckDB/etc.
- Data tests (unique, not_null, relationships, custom)
- Documenting marts for analysts

## Operational directives

1. Stage raw sources 1:1 (`stg_*`) before business logic.
2. Use `{{ ref('model') }}` and `{{ source('src','table') }}` - never hardcode prod relations.
3. Add primary-key and relationship tests on mart grains.
4. Prefer `incremental` with a clear `unique_key` and bounded predicate for large facts.
5. Run `dbt build` (run+test) in CI on changed selectors when possible.

## Model sketch

```sql
-- models/marts/fct_orders.sql
{{ config(materialized='incremental', unique_key='order_id', on_schema_change='append_new_columns') }}

select
  o.order_id,
  o.customer_id,
  o.amount,
  o.created_at
from {{ ref('stg_orders') }} o
{% if is_incremental() %}
where o.created_at > (select coalesce(max(created_at), '1970-01-01') from {{ this }})
{% endif %}
```

## Commands

```bash
dbt deps
dbt run --select marts.fct_orders+
dbt test --select fct_orders
dbt build --select state:modified+   # with defer/state artifacts in CI
dbt docs generate && dbt docs serve
```

## Common failures

| Symptom | Cause | Fix |
| --- | --- | --- |
| Compilation error | bad Jinja/ref | `dbt compile`; check node name |
| Full-refresh surprise | incremental misconfig | review unique_key / predicates |
| Flaky tests | late-arriving data | warn severity; quarantine models |
| Slow CI | building entire project | select ancestors/descendants only |

## Best practices

- Contract tests on public marts; keep staging columns renamed and typed.
- YAML docs for columns business users query.
- Separate `dev` targets with schemas per developer/PR.
- Pin adapter versions with `dbt-core`.

## Limitations

- Orchestration is external (`@airflow`, `@prefect`, dbt Cloud jobs).
- Warehouse cost/permissions still owned by the platform team.
- Python models are adapter-specific and not a substitute for clear SQL.

## Related skills

- `@snowflake` / `@clickhouse` / `@duckdb` - warehouse dialects
- `@great-expectations` - deeper data quality beyond dbt tests
- `@airflow` - schedule dbt jobs
