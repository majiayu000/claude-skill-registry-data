---
name: dbt-expert
description: dbt best practices for models, tests, documentation, and project organization.
---

# dbt Expert

## Project Structure

```
dbt_project/
├── models/
│   ├── staging/        # 1:1 with sources
│   │   └── stg_*.sql
│   ├── intermediate/   # Business logic
│   │   └── int_*.sql
│   └── marts/          # Final tables
│       ├── dim_*.sql
│       └── fct_*.sql
├── tests/
├── macros/
├── seeds/
└── dbt_project.yml
```

## Model Patterns

### Staging

```sql
-- models/staging/stg_orders.sql
with source as (
    select * from {{ source('raw', 'orders') }}
),

renamed as (
    select
        id as order_id,
        customer_id,
        cast(amount as decimal(10,2)) as order_amount,
        created_at::timestamp as ordered_at
    from source
)

select * from renamed
```

### Intermediate

```sql
-- models/intermediate/int_orders_by_customer.sql
select
    customer_id,
    count(*) as order_count,
    sum(order_amount) as total_amount,
    min(ordered_at) as first_order_at
from {{ ref('stg_orders') }}
group by 1
```

### Mart

```sql
-- models/marts/dim_customer.sql
select
    c.customer_id,
    c.name,
    c.email,
    o.order_count,
    o.total_amount,
    o.first_order_at
from {{ ref('stg_customers') }} c
left join {{ ref('int_orders_by_customer') }} o using (customer_id)
```

## Testing

```yaml
# schema.yml
models:
  - name: stg_orders
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: order_amount
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
```

## Documentation

```yaml
models:
  - name: dim_customer
    description: "Customer dimension with order metrics"
    columns:
      - name: customer_id
        description: "Primary key"
      - name: total_amount
        description: "Lifetime order value"
```
