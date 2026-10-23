---
name: new-silver-model
description: Create a new dbt Silver model with SQL + YAML contract. Use when adding a new Silver layer model from a raw source table.
disable-model-invocation: true
argument-hint: "<source>__<entity>"
---

# Skill: Add a New Silver dbt Model

## Steps

1. **Identify the raw source table** — check `dbt/models/sources.yml`; add it if missing.

2. **Create the SQL model** at `dbt/models/silver/<layer>_<source>__<entity>.sql`:
   ```sql
   {{ config(materialized='table') }}

   SELECT
       {{ clean_text('col') }}   AS col,
       {{ parse_bdpm_date('date_col') }} AS date_col
   FROM {{ source('raw', 'table_name') }}
   WHERE {{ is_valid_cis('cis') }}
   ```

3. **Create the contract** at `dbt/models/silver/<layer>_<source>__<entity>.yml`:
   ```yaml
   version: 2
   models:
     - name: <layer>_<source>__<entity>
       description: "..."
       columns:
         - name: <pk>
           data_tests: [unique, not_null]
   ```

4. **Add a new macro** in `dbt/macros/` if any transformation is reused across models.

5. **Validate** locally:
   ```bash
   uv run dotenv -f dbt/.env run -- uv run dbt run --project-dir dbt --profiles-dir dbt --select <model_name>
   uv run dotenv -f dbt/.env run -- uv run dbt test --project-dir dbt --profiles-dir dbt --select <model_name>
   ```
