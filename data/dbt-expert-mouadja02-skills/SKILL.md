---
name: dbt-expert
description: >-
  Writes and reviews dbt projects targeting Snowflake: models, schema.yml metadata, sources, tests,
  macros, and project structure. Use when building or reviewing dbt models, generating dbt YAML, or
  applying dbt best practices.
---

# dbt Expert

You are working with dbt (data build tool) targeting Snowflake. Apply production-grade patterns at every level — clean SQL, thorough YAML metadata, sensible tests, and a project structure that scales.

---

## Model Materializations

| Type | When to use |
|------|-------------|
| `view` | Lightweight lookups, rarely-queried transformations |
| `table` | Stable staging/intermediate layers queried often |
| `incremental` | Large fact tables — only process new/changed rows |
| `ephemeral` | CTEs you want to reuse across models — no physical table |
| `snapshot` | Slowly changing dimensions (SCD Type 2) |
| `dynamic_table` | Snowflake-native: auto-refresh on a lag, no dbt run needed |

Configure at the model level (override project defaults):
```sql
{{ config(
    materialized='incremental',
    unique_key='event_id',
    incremental_strategy='merge',
    cluster_by=['date_day', 'account_id']
) }}
```

---

## Incremental Strategies on Snowflake

**merge** (default) — upsert by `unique_key`
```sql
{{ config(materialized='incremental', unique_key='id', incremental_strategy='merge') }}

select ...
from {{ source('raw', 'events') }}
{% if is_incremental() %}
  where loaded_at > (select max(loaded_at) from {{ this }})
{% endif %}
```

**delete+insert** — for partitioned tables without a reliable unique key
```sql
{{ config(
    materialized='incremental',
    unique_key=['date_day', 'account_id'],
    incremental_strategy='delete+insert',
    partition_by={'field': 'date_day', 'data_type': 'date'}
) }}
```

**append** — event logs, audit tables where duplicates are acceptable
```sql
{{ config(materialized='incremental', incremental_strategy='append') }}
```

**insert_overwrite** — replace entire partitions (Snowflake dynamic partition pruning)

**On schema changes:** always add `on_schema_change='sync_all_columns'` for production incremental models — silently ignoring schema drift causes silent data loss.

---

## Project Structure

```
dbt_project/
├── dbt_project.yml          # Project config
├── profiles.yml             # Connection config (NOT in git)
├── packages.yml             # dbt-utils, dbt-expectations, etc.
├── models/
│   ├── staging/             # 1:1 with source tables, light casting only
│   │   ├── _sources.yml     # source() definitions + freshness
│   │   ├── _staging.yml     # staging model docs + tests
│   │   └── stg_*.sql
│   ├── intermediate/        # Business logic joins, not exposed
│   │   └── int_*.sql
│   ├── marts/               # Final models consumed by BI/apps
│   │   ├── core/
│   │   └── finance/
│   └── utils/               # Generic macros used across layers
├── macros/
├── seeds/                   # Small reference CSVs
├── snapshots/               # SCD Type 2 models
├── tests/                   # Singular (custom SQL) tests
└── analyses/                # Ad hoc SQL, not materialized
```

**Naming rule:** `stg_<source>__<entity>`, `int_<entity>__<verb>`, `fct_<event>`, `dim_<entity>`

---

## Schema YAML — Complete Structure

```yaml
# models/staging/_staging.yml
version: 2

models:
  - name: stg_salesforce__accounts
    description: "One row per Salesforce account, cast and renamed."
    config:
      tags: ["salesforce", "staging"]
    columns:
      - name: account_id
        description: "Natural key from Salesforce."
        data_tests:
          - not_null
          - unique
      - name: created_at
        description: "UTC timestamp of account creation."
        data_tests:
          - not_null
      - name: account_type
        data_tests:
          - accepted_values:
              values: ["Customer", "Partner", "Prospect"]
```

```yaml
# models/staging/_sources.yml
version: 2

sources:
  - name: salesforce
    database: RAW_DB
    schema: SALESFORCE
    freshness:
      warn_after: {count: 12, period: hour}
      error_after: {count: 24, period: hour}
    loaded_at_field: _loaded_at
    tables:
      - name: account
        identifier: ACCOUNT  # actual table name if different
        description: "Raw Salesforce accounts."
        columns:
          - name: Id
            data_tests:
              - not_null
              - unique
```

---

## Tests — Layered Strategy

**Generic tests** (in schema.yml): `not_null`, `unique`, `accepted_values`, `relationships`

**dbt-utils tests** (install `dbt-utils`):
```yaml
- dbt_utils.expression_is_true:
    expression: "amount >= 0"
- dbt_utils.unique_combination_of_columns:
    combination_of_columns: ["date_day", "account_id", "metric"]
- dbt_utils.not_empty_string:
    column_name: account_name
```

**dbt-expectations** for statistical tests:
```yaml
- dbt_expectations.expect_column_values_to_be_between:
    min_value: 0
    max_value: 1
```

**Singular tests** (`tests/` folder) — custom SQL that returns rows on failure:
```sql
-- tests/assert_fct_orders_amount_positive.sql
select order_id
from {{ ref('fct_orders') }}
where amount < 0
```

---

## Macros

**Date spine:**
```sql
-- macros/generate_date_spine.sql
{% macro generate_date_spine(start_date, end_date) %}
  {{ dbt_utils.date_spine(
      datepart="day",
      start_date="cast('" ~ start_date ~ "' as date)",
      end_date="cast('" ~ end_date ~ "' as date)"
  ) }}
{% endmacro %}
```

**Surrogate key:**
```sql
select
  {{ dbt_utils.generate_surrogate_key(['account_id', 'date_day']) }} as sk_account_day,
  ...
```

**Safe divide:**
```sql
{% macro safe_divide(numerator, denominator) %}
  iff({{ denominator }} = 0, null, {{ numerator }} / {{ denominator }})
{% endmacro %}
```

---

## Snapshots (SCD Type 2)

```sql
-- snapshots/snp_accounts.sql
{% snapshot snp_accounts %}
  {{
    config(
      target_schema='SNAPSHOTS',
      unique_key='account_id',
      strategy='timestamp',
      updated_at='updated_at',
      invalidate_hard_deletes=True
    )
  }}
  select * from {{ source('crm', 'accounts') }}
{% endsnapshot %}
```

---

## Snowflake-specific dbt Patterns

**Clustering keys** (for large tables queried by date range):
```sql
{{ config(cluster_by=["date_day", "account_id"]) }}
```

**Dynamic tables** (Snowflake-native, set `materialized='dynamic_table'`):
```sql
{{ config(
    materialized='dynamic_table',
    snowflake_warehouse='TRANSFORM_WH',
    target_lag='5 minutes'
) }}
```

**Warehouse override** for expensive models:
```sql
{{ config(snowflake_warehouse='LARGE_WH') }}
```

**Copy grants** so downstream roles keep access after `table` rebuild:
```sql
{{ config(materialized='table', copy_grants=True) }}
```

**Stage-based seed loading** for large reference files (avoid in-YAML seed if >10k rows):
```sql
-- Use a model that reads from a named Snowflake stage instead of dbt seed
select $1::varchar as code, $2::varchar as label
from @RAW_DB.PUBLIC.REFERENCE_STAGE/lookup.csv
(file_format => 'CSV_FORMAT')
```

---

## dbt_project.yml Key Config

```yaml
name: 'my_project'
version: '1.0.0'
config-version: 2

profile: 'snowflake_prod'

model-paths: ["models"]
test-paths: ["tests"]
snapshot-paths: ["snapshots"]
seed-paths: ["seeds"]
macro-paths: ["macros"]

target-path: "target"
clean-targets: ["target", "dbt_packages"]

models:
  my_project:
    staging:
      +materialized: view
      +schema: STAGING
    intermediate:
      +materialized: ephemeral
    marts:
      +materialized: table
      +schema: MARTS
      core:
        +tags: ["core", "daily"]

vars:
  start_date: "2020-01-01"
```

---

## Generating dbt Projects Programmatically

When generating dbt YAML files from code (e.g., from ETL metadata), follow these rules:

- **sources.yml**: one file per source system, in `models/staging/`
- **schema.yml**: one file per subfolder (staging, marts, etc.), named `_<layer>.yml`
- Always include `version: 2` at the top of every YAML file
- Columns referenced in `data_tests` must match the SQL output column names exactly
- `identifier` field in sources is only needed when the dbt model name differs from the actual table name
- Freshness config only belongs on sources, not models
- `ref()` creates lineage — always use it instead of hardcoding table names
- `source()` for raw tables — never `ref()` a staging model that wraps a source

---

## Quick Diagnostics

```bash
dbt debug                          # Test connection
dbt compile --select my_model      # See rendered SQL without running
dbt run --select +my_model         # Run model + all ancestors
dbt test --select my_model         # Run tests for one model
dbt docs generate && dbt docs serve  # Browse lineage DAG
dbt source freshness               # Check source staleness
dbt list --select tag:daily        # Find all models tagged daily
```
