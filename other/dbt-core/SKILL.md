---
name: dbt-core
description: "dbt Core skill for SQL-based data transformation in warehouses. Deep expertise in project structure, materializations (view, table, incremental, microbatch), Jinja templating, testing framework, macros, packages, MetricFlow, dbt Mesh, and CI/CD workflows. WHEN: \"dbt\", \"dbt Core\", \"dbt run\", \"dbt build\", \"dbt test\", \"ref()\", \"source()\", \"incremental model\", \"dbt macro\", \"dbt snapshot\", \"dbt seed\", \"Jinja SQL\", \"dbt materialization\", \"dbt package\", \"dbt_utils\", \"dbt project\", \"profiles.yml\", \"dbt_project.yml\", \"dbt incremental\", \"dbt microbatch\", \"dbt Mesh\", \"MetricFlow\", \"dbt semantic layer\", \"model contract\", \"dbt unit test\", \"staging intermediate marts\", \"dbt CI\", \"state:modified\", \"dbt compile\", \"dbt debug\". Do NOT use for dbt Cloud-only surfaces (Cloud IDE/Studio, Canvas, Copilot, Cloud scheduling, Discovery/Admin API, RBAC/SSO) -- use the `dbt-cloud` skill."
license: MIT
---

# dbt Core

This skill covers dbt Core (data build tool), the open-source SQL transformation framework for the ELT pattern. It provides deep knowledge of project structure, materializations, Jinja2 templating, the testing framework, incremental strategies, macros, packages, MetricFlow, dbt Mesh, and CI/CD workflows. Coverage spans the current release (dbt Core 1.11) and recent major features (1.8-1.10). For dbt Cloud-specific features (IDE, scheduling, Canvas, Copilot, Explorer), see the `dbt-cloud` skill.

## When to Use This Skill
- "How do I structure a dbt project?"
- "Incremental model not merging correctly"
- "Write a Jinja macro for dynamic pivoting"
- "dbt test failures in CI"
- "Optimize a slow dbt model"
- "Set up dbt Mesh cross-project references"
- "Define a metric with MetricFlow"
- "Migrate from views to incremental models"
- "dbt snapshot SCD Type 2 setup"
- "dbt build vs dbt run + dbt test"
- "CI pipeline with state:modified"
- "Which incremental strategy for 500M rows?"

**See a different skill for:**
- dbt Cloud IDE, scheduling, Canvas, Copilot, Explorer --> `dbt-cloud` skill
- Spark DataFrame transformations --> `spark` skill
- Warehouse-specific tuning (Snowflake, BigQuery, Redshift) --> the database plugin's `{platform}` skill
- Comparing dbt vs Spark vs DuckDB --> `transformation` skill
- ETL architecture, tool selection --> `overview` skill

## How to Approach Tasks

1. **Classify** the request:
   - **Project structure/conventions** -- Load `references/best-practices.md` for staging/intermediate/marts, naming, code style
   - **Architecture/internals** -- Load `references/architecture.md` for execution model, materializations, Jinja, adapters, DAG
   - **Performance/debugging** -- Load `references/diagnostics.md` for error messages, compiled SQL, slow models, CI failures
   - **Best practices/patterns** -- Load `references/best-practices.md` for incrementals, testing, CI/CD, cost optimization
   - **dbt Cloud feature** -- See the `dbt-cloud` skill

2. **Determine context** -- Ask if unclear: which warehouse adapter (Snowflake, BigQuery, Redshift, Databricks, Postgres), dbt version, data volume, team size.

3. **Analyze** -- Apply dbt-specific reasoning: materialization choice, incremental strategy, ref/source dependency graph, Jinja compilation, test coverage.

4. **Recommend** -- Provide actionable guidance with SQL/YAML/Jinja examples, specific CLI commands, and config snippets. Explain trade-offs.

5. **Verify** -- Suggest validation: `dbt compile` for SQL inspection, `dbt debug` for connection, `dbt show` for preview, compiled SQL in `target/compiled/`.

## Core Architecture

### Execution Model

dbt transforms SQL SELECT statements into tables and views in the warehouse. It compiles Jinja-templated SQL, resolves dependencies via `ref()` and `source()`, builds a DAG, and executes models in topological order.

```
SQL + Jinja Models (.sql files)
    |
    v
Jinja Compilation (resolve ref/source/config/var/macros)
    |
    v
DAG Resolution (topological sort by ref/source dependencies)
    |
    v
Compiled SQL (target/compiled/)
    |
    v
DDL/DML Generation (CREATE TABLE AS, INSERT, MERGE)
    |
    v
Warehouse Execution (adapter sends SQL to database)
```

**Key concepts:**
- **ref()**: Declares a dependency on another model. `{{ ref('stg_orders') }}` resolves to the correct database.schema.table and registers a DAG edge.
- **source()**: Declares a dependency on a raw table. `{{ source('stripe', 'payments') }}` enables lineage tracking and freshness monitoring.
- **Materializations**: How dbt persists model output -- view, table, incremental, ephemeral, materialized view.
- **Jinja2**: Templating engine that adds control flow (if/for), macros, variables, and environment access to SQL.

### Project Structure

```
my_project/
 dbt_project.yml          # Project configuration
 profiles.yml             # Connection profiles (~/.dbt/ for security)
 packages.yml             # Package dependencies
 models/                  # SQL transformation models
   staging/               # Source-conformed cleaning (views)
   intermediate/          # Business logic (ephemeral/views)
   marts/                 # Business-ready output (tables/incremental)
 seeds/                   # CSV reference data
 snapshots/               # SCD Type 2 tracking
 tests/                   # Singular data tests
 macros/                  # Reusable Jinja functions
 functions/               # UDFs (1.11+)
 target/                  # Compiled output (gitignored)
 dbt_packages/            # Installed packages (gitignored)
```

### Materializations

| Type | Mechanism | Storage | Freshness | Best For |
|---|---|---|---|---|
| **view** (default) | `CREATE VIEW AS` | None | Always current | Staging models, lightweight transforms |
| **table** | `CREATE TABLE AS` | Full copy | On `dbt run` only | BI-facing marts, frequently queried |
| **incremental** | `INSERT`/`MERGE`/`DELETE+INSERT` | Full + appends | New/changed rows | Large event tables, time-series |
| **ephemeral** | Inlined as CTE | None | N/A (not queryable) | Lightweight intermediate logic |
| **materialized_view** | Database-native MV | Managed by DB | Database-managed | Auto-refresh needed |

**Golden rule**: Start with views. When they take too long to query, make them tables. When the tables take too long to build, make them incremental.

## Model Patterns

### Staging Model

```sql
-- models/staging/stripe/stg_stripe__payments.sql
with source as (
    select * from {{ source('stripe', 'payments') }}
),

renamed as (
    select
        id as payment_id,
        order_id,
        amount::numeric(16, 2) as amount,
        status,
        created_at
    from source
)

select * from renamed
```

### Incremental Model

```sql
-- models/marts/fct_events.sql
{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key='event_id',
    on_schema_change='append_new_columns'
) }}

select
    event_id,
    user_id,
    event_type,
    event_timestamp,
    properties
from {{ ref('stg_events') }}
{% if is_incremental() %}
where event_timestamp > (
    select max(event_timestamp) - interval '2 hours'
    from {{ this }}
)
{% endif %}
```

### Microbatch Model (1.9+)

```sql
-- models/marts/fct_page_views.sql
{{ config(
    materialized='incremental',
    incremental_strategy='microbatch',
    event_time='viewed_at',
    begin='2023-01-01',
    batch_size='day',
    lookback=3
) }}

select * from {{ ref('stg_page_views') }}
```

No `is_incremental()` logic needed. Each batch is independent and idempotent. Parallel execution across batches. Selective backfill via `--event-time-start` and `--event-time-end`.

## Incremental Strategy Selection

| Scenario | Strategy | Why |
|---|---|---|
| Append-only event stream | `append` | No dedup needed, fastest |
| Small-medium table with unique key | `merge` | Standard upsert |
| Large table (>100M rows) with unique key | `delete+insert` | 3.4x faster than merge at scale |
| Date-partitioned data | `insert_overwrite` | Replace full partitions |
| Large time-series (>1B rows) | `microbatch` | Parallel batches, automatic late-data handling |

## Testing Framework

### Generic Tests (YAML)

```yaml
models:
  - name: fct_orders
    columns:
      - name: order_id
        data_tests:
          - unique
          - not_null
      - name: status
        data_tests:
          - accepted_values:
              values: ['placed', 'shipped', 'completed', 'returned']
      - name: customer_id
        data_tests:
          - relationships:
              to: ref('dim_customers')
              field: customer_id
```

### Unit Tests (1.8+)

```yaml
unit_tests:
  - name: test_order_total
    model: fct_orders
    given:
      - input: ref('stg_orders')
        rows:
          - {order_id: 1, amount: 100, status: completed}
          - {order_id: 2, amount: 200, status: returned}
    expect:
      rows:
        - {order_id: 1, amount: 100, is_valid: true}
        - {order_id: 2, amount: 200, is_valid: false}
```

### What to Always Test

- Primary keys: `unique` + `not_null` on every model
- Foreign keys: `relationships` on join columns
- Critical business columns: `not_null` on required fields
- Source freshness: `freshness` config on all source tables

## CLI Quick Reference

| Command | Purpose |
|---|---|
| `dbt build` | Run + test + snapshot + seed in DAG order (preferred) |
| `dbt run` | Build models only |
| `dbt test` | Run data tests only |
| `dbt build --select state:modified+ --defer --state ./prod-artifacts/` | Slim CI |
| `dbt run --full-refresh --select my_model` | Force complete rebuild |
| `dbt compile` | Compile SQL without executing |
| `dbt debug` | Validate connection and configuration |
| `dbt show --select my_model --limit 10` | Preview query results |
| `dbt source freshness` | Check source data freshness |
| `dbt deps` | Install package dependencies |
| `dbt docs generate && dbt docs serve` | Generate and serve documentation |

## dbt Mesh (Multi-Project)

For scaling data teams across organizational boundaries:

- **Cross-project refs**: `{{ ref('upstream_project', 'shared_model') }}`
- **Access modifiers**: `private` (same group), `protected` (same project, default), `public` (any project)
- **Model contracts**: Enforce column names, types, and constraints at build time
- **Model versions**: Treat public models as APIs with versioning and deprecation dates

```yaml
models:
  - name: dim_customers
    access: public
    config:
      contract:
        enforced: true
    columns:
      - name: customer_id
        data_type: int
      - name: customer_name
        data_type: varchar(100)
```

## Anti-Patterns

1. **Skipping tests** -- dbt tests are zero-cost to define and catch data quality issues before they reach dashboards. At minimum: `unique` + `not_null` on every primary key.

2. **`source()` outside staging** -- Only staging models should reference `source()`. All other models use `ref()`. This enforces a single entry point from raw data.

3. **Complex logic in staging** -- Staging models should only rename, cast, and filter. Business logic belongs in intermediate or marts layers.

4. **`SELECT *` in production models** -- Pulling all columns wastes compute and breaks when source schemas change. Select explicitly.

5. **Skipping `--defer` in CI** -- Without `--defer`, CI must build the entire upstream DAG. Use `--defer --state ./prod-artifacts/` to reference production tables for unmodified models.

6. **Tables for staging** -- Staging models should be views. Tables waste storage and add build time for models that are simple passthrough transforms.

7. **Ignoring incremental for large tables** -- Full table rebuilds on 100M+ row tables burn compute. Switch to incremental with an appropriate strategy.

8. **Over-abstracting with macros** -- Macros should simplify, not obscure. If a macro requires more than a few parameters and conditional blocks, the SQL is likely clearer written directly.

## Key Packages

| Package | Purpose |
|---|---|
| **dbt-utils** | Surrogate keys, pivot, union, date spine, generic tests |
| **dbt-expectations** | 40+ data quality tests (Great Expectations-inspired) |
| **codegen** | Auto-generate base models, YAML schema files, sources |
| **audit-helper** | Compare datasets for migration validation |
| **dbt-project-evaluator** | Lint project structure against best practices |

## Cross-Domain References

| Technology | Reference | When |
|---|---|---|
| dbt Cloud | `dbt-cloud` skill | IDE, scheduling, Canvas, Copilot, Explorer, Semantic Layer API |
| Spark | `spark` skill | When transformations exceed SQL (ML, complex parsing, >TB scale) |
| Transformation | `transformation` skill | Comparing dbt vs Spark vs DuckDB |
| ETL Domain | `overview` skill | Cross-platform ETL architecture |

## Reference Files

Load these when you need deep knowledge for a specific area:

- `references/architecture.md` -- Execution model (DAG, ref/source, compilation), materializations, Jinja templating (syntax, macros, key functions), adapters (official and community), testing framework (generic, singular, unit), documentation system, packages, dbt Mesh, MetricFlow/Semantic Layer, incremental strategies, snapshots
- `references/best-practices.md` -- Project structure (staging/intermediate/marts), naming conventions, incremental model selection, testing strategy, performance optimization (partitioning, clustering, query tips), CI/CD workflows (Slim CI, state:modified, --defer), code style guide (SQL formatting, CTE organization, Jinja patterns)
- `references/diagnostics.md` -- Error categories (runtime, compilation, dependency, database), common errors and solutions, debugging tools (dbt debug, compiled SQL, logs, artifacts), performance diagnostics (slow models, full refresh triggers, warehouse tuning), CI/CD diagnostics (state comparison, environment issues, pipeline failures)

## Diagnostic Scripts

Ready-made artifact-inspection scripts (bash + jq over `target/*.json`) in `scripts/`, numbered by investigation order. All read-only.

- `scripts/01-run-results-summary.sh` -- Last invocation: status mix, errors/failures, slowest models
- `scripts/02-model-timing.sh` -- All models ranked by execution time (incremental-strategy review list)
- `scripts/03-test-failures.sh` -- Failed and warning data-quality tests with violating row counts
- `scripts/04-manifest-governance-audit.sh` -- Models missing tests or descriptions (governance gaps)
