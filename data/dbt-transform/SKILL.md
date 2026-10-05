---
name: dbt-transform
description: Use when dbt data transformation — models, tests, macros, sources, snapshots,
  documentation, packages. Use when working with dbt transform.
domain: data
author: oyi77
license: Apache-2.0
subdomain: data-engineering
tags:
- analytics
- data-analysis
- dbt
- transform
- visualization
version: 1.0.0
category: data
---



## Overview

dbt (data build tool) enables analytics engineers to transform data in the warehouse using SQL SELECT statements. It handles dependency management, testing, documentation, and incremental materializations.

## Capabilities

- Define transformations as SQL SELECT models
- Build dependency DAGs with ref() and source()
- Write data tests (unique, not_null, accepted_values, relationships)
- Create reusable macros with Jinja
- Snapshot slowly changing dimensions (SCD Type 2)
- Generate and serve documentation
- Use packages for community macros and models

## When to Use
**Trigger phrases:**
- "dbt transform"
- "dbt data transformation — models, tests, macros, sources, snapshots, documentati"


- Transforming raw data into analytics-ready models in a warehouse
- Needing version-controlled, testable SQL transformations
- Building incremental models for large datasets
- Documenting data lineage and schemas
- Reusing transformation logic across projects

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code

The dbt-transform workflow follows a standard pipeline pattern.

Core flow:
```
# dbt-transform primary flow
input = prepare(raw_data)
result = process(input, config={data, dbt, documentation, macros, models})
validate(result)
deliver(result)
```

Error handling:
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Model Definition

```sql
-- models/staging/stg_orders.sql
{{ config(materialized='view') }}

with source as (
    select * from {{ source('raw', 'orders') }}
),

renamed as (
    select
        order_id,
        customer_id,
        order_date,
        status,
        amount,
        created_at
    from source
    where order_date >= '2020-01-01'
)

select * from renamed
```

### Incremental Model

```sql
-- models/marts/fct_orders.sql
{{ config(
    materialized='incremental',
    unique_key='order_id',
    incremental_strategy='merge',
    on_schema_change='sync_all_columns',
) }}

with orders as (
    select * from {{ ref('stg_orders') }}
    {% if is_incremental() %}
        where order_date > (select max(order_date) from {{ this }})
    {% endif %}
)

select
    order_id,
    customer_id,
    order_date,
    status,
    amount
from orders
```

### Source Definition

```yaml
# models/staging/sources.yml
version: 2
sources:
  - name: raw
    database: warehouse
    schema: raw_data
    tables:
      - name: orders
        columns:
          - name: order_id
            tests:
              - unique
              - not_null
      - name: customers
```

### Data Tests

```yaml
# models/marts/schema.yml
version: 2
models:
  - name: fct_orders
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: status
        tests:
          - accepted_values:
              values: ['pending', 'shipped', 'delivered', 'cancelled']
      - name: customer_id
        tests:
          - relationships:
              to: ref('dim_customers')
              field: customer_id
```

### Custom Test

```sql
-- tests/assert_positive_amounts.sql
select order_id, amount
from {{ ref('fct_orders') }}
where amount <= 0
```

### Macro

```sql
-- macros/generate_schema_name.sql
{% macro generate_schema_name(custom_schema_name, node) %}
    {% if custom_schema_name is none %}
        {{ target.schema }}
    {% else %}
        {{ custom_schema_name }}
    {% endif %}
{% endmacro %}

-- macros/cents_to_dollars.sql
{% macro cents_to_dollars(column_name, precision=2) %}
    round({{ column_name }} / 100, {{ precision }})
{% endmacro %}

-- Usage in model:
-- select {{ cents_to_dollars('amount_cents') }} as amount
```

### Snapshot (SCD Type 2)

```sql
-- snapshots/customers_snapshot.sql
{% snapshot customers_snapshot %}

{{
    config(
        target_schema='snapshots',
        unique_key='customer_id',
        strategy='timestamp',
        updated_at='updated_at',
    )
}}

select * from {{ source('raw', 'customers') }}

{% endsnapshot %}
```

### Documentation

```yaml
# models/marts/fct_orders.yml
version: 2
models:
  - name: fct_orders
    description: "Fact table containing all customer orders"
    columns:
      - name: order_id
        description: "Primary key — unique order identifier"
      - name: amount
        description: "Order total in USD"
```

```bash
# Generate and serve docs
dbt docs generate
dbt docs serve --port 8080
```

### Packages

```yaml
# packages.yml
packages:
  - package: dbt-labs/dbt_utils
    version: ">=1.0.0"
  - package: calogica/dbt_expectations
    version: ">=0.9.0"
```

```bash
dbt deps
```

## Common Patterns

| Pattern | When to Use |
|---------|------------|
| `materialized='view'` | Staging models (lightweight, always fresh) |
| `materialized='table'` | Small dimension tables |
| `materialized='incremental'` | Large fact tables (process new data only) |
| `is_incremental()` | Filter for new rows in incremental runs |
| `{{ ref('model') }}` | Inter-model dependencies |
| `{{ source('name', 'table') }}` | Source table references |
| Snapshots | Track slowly changing dimensions |

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `Compilation Error` | Syntax error or missing ref | Check model SQL and dependency names |
| `Schema Change Detected` | Upstream column change | Use `on_schema_change='sync_all_columns'` |
| `Duplicate key` | Incremental strategy mismatch | Check `unique_key` and `incremental_strategy` |
| `Source not found` | Missing sources.yml | Add source definition |

## How to Use

1. Define data sources, sinks, and transformation requirements
2. Implement extraction with error handling and schema validation
3. Add transformation logic with idempotency guarantees
4. Configure loading with conflict resolution (upsert/append)
5. Set up monitoring for pipeline health and data freshness
6. Test with representative sample data before production

## Red Flags

- **Data pipeline has no error handling**: Silent failures corrupt downstream datasets
- **No data validation at boundaries**: Bad input propagates through entire pipeline
- **Missing monitoring for data freshness**: Stale data causes wrong business decisions
- **No rollback on failed transforms**: Failed transforms without rollback require manual recovery
- **Hardcoded connection strings**: Credentials in code get committed to version control

## Verification

- [ ] Skill output matches expected behavior

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "CSV is fine for everything" | Structured databases enable queries, integrity, and scale. |
| "I will add data validation later" | Bad data propagates silently. Validate at ingestion. |
| "Small datasets do not need optimization" | Even small datasets benefit from proper indexing and schema design. |