---
name: sqlmesh
description: SQLMesh patterns for data transformation with column-level lineage and virtual environments. Use when building data pipelines that need advanced features like automatic DAG inference and efficient incremental processing.
---

# SQLMesh Skill

This skill provides SQLMesh patterns for data transformation.

## Project Structure

```
sqlmesh_project/
├── config.yaml
├── models/
│   ├── staging/
│   │   └── stg_customers.sql
│   └── marts/
│       └── dim_customers.sql
├── macros/
├── seeds/
├── audits/
└── tests/
```

## Model Definition

```sql
-- models/staging/stg_customers.sql
MODEL (
    name staging.stg_customers,
    kind INCREMENTAL_BY_TIME_RANGE (
        time_column created_at
    ),
    cron '@daily'
);

SELECT
    id AS customer_id,
    LOWER(email) AS email,
    created_at
FROM raw.customers
WHERE created_at BETWEEN @start_ds AND @end_ds
```

## Model Kinds

| Kind | Use Case |
|------|----------|
| `FULL` | Complete refresh each run |
| `INCREMENTAL_BY_TIME_RANGE` | Time-based incremental |
| `INCREMENTAL_BY_UNIQUE_KEY` | Key-based merge |
| `VIEW` | Virtual table |
| `SEED` | Static CSV data |

## Virtual Environments

```bash
# Create a virtual environment for testing
sqlmesh plan dev

# Apply to production
sqlmesh plan prod
```

## Audits

```sql
-- audits/no_nulls.sql
AUDIT (
    name assert_no_null_customer_id,
    model staging.stg_customers
);

SELECT * FROM staging.stg_customers
WHERE customer_id IS NULL
```

## Best Practices

- Use column-level lineage for impact analysis
- Leverage virtual environments for testing
- Define audits for data quality
- Use incremental models for efficiency
