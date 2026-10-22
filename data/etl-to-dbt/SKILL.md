---
name: etl-to-dbt
description: >-
  Converts ETL pipeline metadata (Informatica IICS, PowerCenter XML, and similar) into clean dbt
  models, SQL, and YAML rather than a mechanical one-to-one translation. Use when migrating legacy ETL
  mappings to dbt.
---

# ETL to dbt Migration

You are converting ETL pipeline metadata (Informatica IICS, PowerCenter XML, or similar) into clean, production-grade dbt models. The goal is not a mechanical 1:1 translation but generating SQL that a data engineer would be proud to maintain.

## The Migration Workflow

```
1. Analyze   → Read the mapping/workflow file, identify sources, targets, transformations
2. Plan      → Sketch the dbt model graph (staging → intermediate → final)
3. Generate  → Write SQL models + YAML metadata
4. Validate  → Check column coverage, data type fidelity, test coverage
```

---

## Step 1: Analyze the Mapping

When given an IICS/Informatica mapping (XML or JSON), extract:

**Sources** — from Source Qualifier or Read transformations:
- Source connection / schema / table name
- Selected columns and their data types
- Filter conditions (WHERE clause on the source)
- Source join conditions (when the SQ joins multiple tables)

**Target** — from Target Definition or Write transformations:
- Target schema / table name
- Column mapping (source expression → target column)
- Write mode (insert, update, upsert, delete)

**Transformations** in order — see the transformation reference below.

---

## Step 2: Map the Model Graph

Typical mapping → model graph:

```
Raw source table(s)
    ↓
stg_<source>__<table>.sql      (one per source table, light casting)
    ↓
int_<entity>__<verb>.sql       (joins, lookups, aggregations)
    ↓
fct_<fact>.sql / dim_<dim>.sql (final mart model)
```

Simple mappings (single source, expression only) collapse to two layers.
Complex mappings (multiple sources, lookups, aggregations) use all three.

---

## Step 3: Informatica Transformation → SQL

### Source Qualifier (SQ)
The entry point — generates the staging SELECT.
```sql
-- stg_crm__customers.sql
select
    cast(CUST_ID as varchar(36))  as customer_id,
    cast(CUST_NAME as varchar(255)) as customer_name,
    cast(CREATED_DT as timestamp_ntz) as created_at
from {{ source('crm', 'customers') }}
-- If SQ has a filter:
where IS_ACTIVE = 'Y'
```

### Expression Transformation (EXP)
Computed columns → computed expressions in SELECT or a CTE.
```sql
-- Informatica: IIF(STATUS = 'A', 'Active', 'Inactive')
case when status = 'A' then 'Active' else 'Inactive' end as status_label,

-- Informatica: TO_DATE(DATE_STR, 'YYYY-MM-DD')
try_to_date(date_str, 'YYYY-MM-DD') as parsed_date,

-- Informatica: ISNULL(AMOUNT) → NVL(AMOUNT, 0)
coalesce(amount, 0) as amount,

-- Informatica: SUBSTR(NAME, 1, 50)
left(name, 50) as short_name,

-- Informatica: SYSTIMESTAMP
current_timestamp() as processed_at
```

### Filter Transformation (FIL)
Becomes a WHERE clause in the current CTE.
```sql
where status = 'ACTIVE'
  and amount > 0
```

### Joiner Transformation (JNR)
Becomes a SQL JOIN. Check the join condition and type (normal = inner, master-outer = left join).
```sql
-- Master: orders, Detail: customers → left join orders to customers
select
    o.order_id,
    o.amount,
    c.customer_name
from {{ ref('stg_oms__orders') }} o
left join {{ ref('stg_crm__customers') }} c
    on o.customer_id = c.customer_id
```

### Lookup Transformation (LKP)
Becomes a LEFT JOIN or a scalar subquery. Lookup condition = ON clause.
```sql
-- Lookup: find product_name from products table by product_id
left join {{ ref('stg_catalog__products') }} p
    on f.product_id = p.product_id
-- Then reference p.product_name in the SELECT
```

When the lookup returns a single value and the source is small, a subquery works:
```sql
(select product_name from {{ ref('dim_products') }} where product_id = f.product_id limit 1)
  as product_name
```

### Aggregator Transformation (AGG)
Becomes GROUP BY.
```sql
select
    account_id,
    date_trunc('month', order_date) as order_month,
    sum(amount) as total_amount,
    count(*) as order_count
from {{ ref('int_orders__enriched') }}
group by 1, 2
```

### Router Transformation (RTR)
Splits a stream by condition — becomes either:
- Multiple CTEs with different WHERE clauses (if they land in different targets)
- A CASE expression (if they're combined in one target with a type column)

```sql
-- Router with 3 groups landing in one target:
with routed as (
    select *,
        case
            when region = 'EMEA' then 'europe'
            when region = 'AMER' then 'americas'
            else 'apac'
        end as region_group
    from source
)
```

### Sorter Transformation (SRT)
Informatica sorts for dedup or ordered processing. In SQL, use window functions:
```sql
-- Instead of ORDER BY (which is meaningless without LIMIT), use ROW_NUMBER for dedup:
qualify row_number() over (partition by account_id order by updated_at desc) = 1
```

### Union Transformation (UNI)
→ `UNION ALL` (Informatica Union always includes all rows)
```sql
select account_id, amount, 'source_a' as data_source from {{ ref('stg_a__accounts') }}
union all
select account_id, amount, 'source_b' as data_source from {{ ref('stg_b__accounts') }}
```

### Normalizer Transformation (NRM)
Pivots columns into rows — use UNPIVOT or LATERAL FLATTEN (Snowflake):
```sql
select account_id, key as metric_name, value as metric_value
from source
unpivot (value for key in (metric_q1, metric_q2, metric_q3, metric_q4))
```

### Rank Transformation (RNK)
```sql
row_number() over (partition by account_id order by score desc) as rnk
-- or:
rank() over (...)
dense_rank() over (...)
```

### Sequence Generator (SEQ)
Use ROW_NUMBER() for surrogate keys, or `{{ dbt_utils.generate_surrogate_key([...]) }}` for deterministic hashes.
```sql
row_number() over (order by created_at) as sequence_num
```

### Update Strategy Transformation (UPD)
Maps to an incremental model with merge strategy:
```sql
{{ config(
    materialized='incremental',
    unique_key='account_id',
    incremental_strategy='merge'
) }}

select ...
{% if is_incremental() %}
where updated_at > (select max(updated_at) from {{ this }})
{% endif %}
```

### Data Masking / Anonymization
```sql
-- Hash PII
sha2(email, 256) as email_hash,
-- Truncate precision
date_trunc('month', birth_date) as birth_month,
-- Redact
'***REDACTED***' as ssn
```

---

## Data Type Mapping

| Informatica Type | Snowflake Type |
|-----------------|----------------|
| String(n) | VARCHAR(n) |
| Nstring(n) | VARCHAR(n) |
| Integer | NUMBER(10,0) |
| Small Integer | NUMBER(5,0) |
| Big Integer | NUMBER(19,0) |
| Decimal(p,s) | NUMBER(p,s) |
| Float | FLOAT |
| Double | DOUBLE |
| Date/Time | TIMESTAMP_NTZ |
| Date | DATE |
| Time | TIME |
| Binary | BINARY |
| Text / Memo | VARCHAR(16777216) |

Always cast at the staging layer — never propagate raw string types into marts.

---

## Generating sources.yml

From Source Qualifier metadata:
```yaml
version: 2

sources:
  - name: crm                          # logical source name (short, snake_case)
    database: RAW_DB                   # Snowflake database
    schema: SALESFORCE_CRM             # Snowflake schema
    freshness:
      warn_after: {count: 6, period: hour}
      error_after: {count: 24, period: hour}
    loaded_at_field: _loaded_at
    tables:
      - name: account                  # dbt source table name
        identifier: ACCOUNT_TABLE      # actual Snowflake table name (if different)
        description: "Raw CRM accounts from Salesforce."
```

---

## Generating models/_staging.yml

```yaml
version: 2

models:
  - name: stg_crm__accounts
    description: "Staged CRM accounts — cast and renamed."
    columns:
      - name: account_id
        data_tests: [not_null, unique]
      - name: account_name
        data_tests: [not_null]
      - name: created_at
        data_tests: [not_null]
      - name: status
        data_tests:
          - accepted_values:
              values: ["Active", "Inactive", "Pending"]
```

---

## Naming Conventions

| Layer | Pattern | Example |
|-------|---------|---------|
| Staging | `stg_<source>__<table>` | `stg_crm__accounts` |
| Intermediate | `int_<entity>__<verb>` | `int_orders__enriched` |
| Fact | `fct_<event_plural>` | `fct_order_lines` |
| Dimension | `dim_<entity>` | `dim_customers` |
| Snapshot | `snp_<entity>` | `snp_accounts` |

Source names: the ETL connection/schema name, lowercased.
Table names: the source table name, lowercased, no prefixes.

---

## Complete Model Template

```sql
-- models/staging/stg_crm__accounts.sql
with source as (

    select * from {{ source('crm', 'account') }}

),

renamed as (

    select
        -- ids
        cast(id as varchar(36))                          as account_id,
        cast(parent_id as varchar(36))                   as parent_account_id,

        -- attributes
        cast(name as varchar(255))                       as account_name,
        lower(cast(type as varchar(50)))                 as account_type,
        cast(industry as varchar(100))                   as industry,

        -- booleans
        is_deleted::boolean                              as is_deleted,

        -- dates
        cast(created_date as timestamp_ntz)              as created_at,
        cast(last_modified_date as timestamp_ntz)        as updated_at,

        -- metadata
        _loaded_at                                       as _loaded_at

    from source
    where is_deleted = false   -- apply SQ filter here

)

select * from renamed
```

---

## Quality Checklist

Before declaring a migration done:
- [ ] All source tables have a `source()` reference and freshness config
- [ ] Every staging model casts columns to final types (no implicit casting downstream)
- [ ] Primary keys have `not_null` + `unique` tests
- [ ] Foreign key relationships have `relationships` tests
- [ ] Incremental models have a `unique_key` and a filter on `is_incremental()`
- [ ] No hardcoded database/schema names — only `ref()` and `source()`
- [ ] Model names follow the layer naming convention
- [ ] All transformations from the mapping are accounted for
