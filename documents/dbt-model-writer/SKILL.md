---
name: dbt-model-writer
description: Writes, edits, and creates dbt models following best practices. Use when user needs to create new dbt SQL models, update existing models, or convert raw SQL to dbt format. Handles staging, intermediate, and mart models with proper config blocks, CTEs, and documentation.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# dbt Model Writer

Expert dbt model creation and editing skill for analytics engineering.

## When to Use This Skill

Activate this skill when the user mentions:
- "Create a dbt model"
- "Write a dbt SQL file"
- "Convert this SQL to dbt"
- "Add a staging/intermediate/mart model"
- "Update this dbt model"
- "Fix this dbt model"

## Core Capabilities

### 1. Model Creation
Create new dbt models with:
- Proper config blocks (materialization, tags, schema)
- Descriptive CTE structure
- Inline documentation comments
- Source and ref() functions
- Appropriate Jinja templating

### 2. Model Types

**Staging Models** (`stg_*.sql`)
- Purpose: Clean and standardize raw source data
- Materialization: Usually `view`
- Pattern: One-to-one with source tables
- Transformations: Column renaming, type casting, basic cleaning

```sql
{{
  config(
    materialized='view',
    tags=['staging']
  )
}}

with source as (
    select * from {{ source('raw', 'orders') }}
),

renamed as (
    select
        order_id,
        customer_id,
        order_date,
        status,
        -- Standardize column names and types
        cast(total_amount as decimal(10,2)) as total_amount,
        created_at,
        updated_at
    from source
)

select * from renamed
```

**Intermediate Models** (`int_*.sql`)
- Purpose: Complex business logic, joins, denormalization
- Materialization: Usually `ephemeral` or `view`
- Pattern: Combine multiple staging models
- Transformations: Business calculations, complex joins

```sql
{{
  config(
    materialized='ephemeral',
    tags=['intermediate']
  )
}}

with orders as (
    select * from {{ ref('stg_orders') }}
),

customers as (
    select * from {{ ref('stg_customers') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

order_totals as (
    select
        order_id,
        count(*) as item_count,
        sum(quantity) as total_quantity,
        sum(quantity * price) as gross_total
    from order_items
    group by order_id
),

joined as (
    select
        o.order_id,
        o.customer_id,
        c.customer_name,
        o.order_date,
        ot.item_count,
        ot.total_quantity,
        ot.gross_total
    from orders o
    join customers c on o.customer_id = c.customer_id
    join order_totals ot on o.order_id = ot.order_id
)

select * from joined
```

**Mart Models** (`fct_*.sql` or `dim_*.sql`)
- Purpose: Analytics-ready tables optimized for BI tools
- Materialization: Usually `table` or `incremental`
- Pattern: Final dimensional models (facts and dimensions)
- Transformations: Aggregations, final business metrics

```sql
{{
  config(
    materialized='incremental',
    unique_key='order_id',
    cluster_by=['order_date'],
    tags=['mart', 'daily']
  )
}}

with orders as (
    select * from {{ ref('int_order_details') }}
)

select
    order_id,
    customer_id,
    order_date,
    item_count,
    total_quantity,
    gross_total,
    current_timestamp() as dbt_updated_at
from orders

{% if is_incremental() %}
    -- Only process new or updated orders
    where order_date >= (select max(order_date) from {{ this }})
{% endif %}
```

### 3. Config Block Standards

Essential config parameters:
```sql
{{
  config(
    materialized='table',  -- table|view|incremental|ephemeral
    schema='analytics',    -- custom schema
    alias='my_table',      -- custom table name
    tags=['daily', 'core'], -- organizational tags
    cluster_by=['date', 'id'], -- Snowflake clustering
    unique_key='id',       -- for incremental
    on_schema_change='sync_all_columns', -- incremental schema changes
    pre_hook="ALTER TABLE {{ this }} ...",
    post_hook="GRANT SELECT ON {{ this }} ..."
  )
}}
```

### 4. Incremental Strategy Patterns

**Append-Only (Insert New Records)**
```sql
{% if is_incremental() %}
    where created_at > (select max(created_at) from {{ this }})
{% endif %}
```

**Update Existing Records (Merge)**
```sql
{{
  config(
    materialized='incremental',
    unique_key='id',
    incremental_strategy='merge'
  )
}}
```

**Delete + Insert**
```sql
{{
  config(
    materialized='incremental',
    unique_key='date_day',
    incremental_strategy='delete+insert'
  )
}}
```

### 5. Documentation Standards

Always create corresponding schema.yml entries:

```yaml
version: 2

models:
  - name: fct_orders
    description: "Fact table for order transactions"
    columns:
      - name: order_id
        description: "Unique order identifier"
        tests:
          - unique
          - not_null
      - name: customer_id
        description: "Foreign key to dim_customers"
        tests:
          - not_null
          - relationships:
              to: ref('dim_customers')
              field: customer_id
      - name: order_date
        description: "Date order was placed"
        tests:
          - not_null
      - name: total_amount
        description: "Total order value in USD"
        tests:
          - not_null
```

### 6. Jinja Best Practices

**Use ref() for model dependencies**
```sql
select * from {{ ref('stg_orders') }}
```

**Use source() for raw data**
```sql
select * from {{ source('raw_db', 'orders') }}
```

**Environment-specific logic**
```sql
{% if target.name == 'prod' %}
    -- Production-specific logic
{% else %}
    -- Dev/test logic
{% endif %}
```

**Macros for reusable logic**
```sql
{{ cents_to_dollars('price_cents') }} as price_dollars
```

## Workflow Process

1. **Understand Requirements**
   - Ask about model purpose and layer (staging/intermediate/mart)
   - Identify source tables or upstream models
   - Determine materialization needs
   - Clarify any business logic

2. **Read Existing Context**
   - Check `dbt_project.yml` for project structure
   - Look for similar existing models
   - Review naming conventions in use
   - Check for available macros

3. **Write the Model**
   - Start with config block
   - Build CTEs from source up
   - Apply transformations step-by-step
   - Add inline comments for complex logic
   - Final select statement

4. **Create Documentation**
   - Generate schema.yml entry
   - Add column descriptions
   - Include appropriate tests

5. **Validate**
   - Check for syntax errors
   - Ensure all refs/sources exist
   - Verify config parameters
   - Confirm naming conventions

## Common Patterns to Apply

### Deduplication
```sql
with deduped as (
    select
        *,
        row_number() over (
            partition by id 
            order by updated_at desc
        ) as row_num
    from source
    where row_num = 1
)
```

### Type 2 SCD (Slowly Changing Dimension)
```sql
with current_records as (
    select * from {{ ref('stg_customers') }}
),

historical_records as (
    select * from {{ this }}
    where is_current = true
),

changes as (
    select
        c.*,
        h.customer_key,
        case
            when h.customer_key is null then true
            when c.customer_name != h.customer_name then true
            else false
        end as has_changed
    from current_records c
    left join historical_records h
        on c.customer_id = h.customer_id
)
-- ... SCD logic continues
```

### Surrogate Key Generation
```sql
{{ dbt_utils.generate_surrogate_key(['order_id', 'line_number']) }} as order_line_key
```

## Error Handling

If encountering issues:
1. Check compiled SQL in `target/compiled/`
2. Verify all referenced models exist
3. Validate Jinja syntax
4. Ensure source definitions exist
5. Check for circular dependencies

## Quality Checklist

Before completing, verify:
- [ ] Config block with appropriate materialization
- [ ] All CTEs have descriptive names
- [ ] Complex logic has comments
- [ ] Uses ref() for models, source() for raw data
- [ ] schema.yml entry created with tests
- [ ] Column descriptions added
- [ ] Follows project naming conventions
- [ ] No hardcoded values (use vars or macros)
- [ ] Incremental logic correct (if applicable)
- [ ] Efficient SQL (appropriate JOINs and filters)
