---
name: dbt
description: dbt with TD Trino. Covers profiles.yml setup (method:none, user:TD_API_KEY), required override macros (no CREATE VIEW), TD_INTERVAL in models, and TD Workflow deployment.
---

# dbt with Treasure Data Trino

## Installation

```bash
uv venv && source .venv/bin/activate
uv pip install dbt-core dbt-trino==1.9.3
```

## profiles.yml

```yaml
td:
  target: dev
  outputs:
    dev:
      type: trino
      method: none                          # Not 'ldap'
      user: "{{ env_var('TD_API_KEY') }}"
      password: dummy                       # Not used
      host: api-presto.treasuredata.com
      port: 443
      database: td                          # Always 'td'
      schema: your_dev_database             # Your TD database name
      threads: 4
      http_scheme: https
      session_properties:
        query_max_run_time: 1h
```

**Key TD settings:**
- `method: none` for API key auth
- `database: td` (always)
- `schema: your_td_database` (what you see in TD Console)

## Required Override Macros

TD doesn't support `CREATE VIEW`. Create `macros/override_dbt_trino.sql`:

```sql
{% macro trino__create_view_as(relation, sql) -%}
  create or replace table {{ relation }} as (
    {{ sql }}
  );
{%- endmacro %}

{% macro trino__list_relations_without_caching(schema_relation) %}
  {% call statement('list_relations_without_caching', fetch_result=True) %}
    select
      table_catalog as "database",
      table_schema as "schema",
      table_name as "name",
      table_type as "type"
    from {{ schema_relation }}.information_schema.tables
    where table_schema = '{{ schema_relation.schema }}'
  {% endcall %}
  {{ return(load_result('list_relations_without_caching').table) }}
{% endmacro %}
```

## dbt_project.yml

```yaml
name: 'my_td_project'
version: '1.0.0'
config-version: 2
profile: 'td'

flags:
  require_certificate_validation: true

vars:
  target_range: '-3M/now'

models:
  my_td_project:
    +materialized: table
    +on_schema_change: "append_new_columns"
```

## Model Patterns

**Basic model:**
```sql
{{
  config(materialized='table')
}}

SELECT
  TD_TIME_STRING(time, 'd!', 'JST') as date,
  COUNT(*) as event_count
FROM {{ source('raw', 'events') }}
WHERE TD_INTERVAL(time, '{{ var("target_range", "-7d") }}', 'JST')
GROUP BY 1
```

**Incremental model:**
```sql
{{
  config(
    materialized='incremental',
    unique_key='event_id'
  )
}}

SELECT *
FROM {{ source('raw', 'events') }}
WHERE TD_INTERVAL(time, '{{ var("target_range", "-1d") }}', 'JST')
{% if is_incremental() %}
  AND time > (SELECT MAX(time) FROM {{ this }})
{% endif %}
```

## Commands

```bash
dbt debug                                    # Test connection
dbt run                                      # Run all
dbt run --select daily_events                # Run specific
dbt run --vars '{"target_range": "-1d"}'     # Override variable
dbt run --full-refresh                       # Rebuild incremental
dbt test                                     # Run tests
```

## TD Workflow Deployment

```yaml
# dbt_workflow.dig
timezone: Asia/Tokyo

schedule:
  daily>: 03:00:00

_export:
  docker:
    image: "treasuredata/customscript-python:3.12.11-td1"
  _env:
    TD_API_KEY: ${secret:td.apikey}

+setup:
  py>: tasks.InstallPackages

+dbt_run:
  py>: dbt_wrapper.run_dbt
  command_args: ['run', '--target', 'prod']
```

**tasks.py:**
```python
def InstallPackages():
    import subprocess, sys
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'dbt-core==1.10.9', 'dbt-trino==1.9.3'])
```

## Common Errors

| Error | Fix |
|-------|-----|
| connector does not support creating views | Add override macro above |
| Table ownership information not available | Add override macro for list_relations |
| Var 'target_range' is undefined | Add default: `{{ var('target_range', '-1d') }}` |

## Resources

- https://docs.getdbt.com/
- https://github.com/starburstdata/dbt-trino
