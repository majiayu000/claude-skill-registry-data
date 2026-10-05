---
name: dbt-sql
description: >-
  Use for creating, reviewing, debugging, or testing dbt SQL projects involving
  models, sources, ref, tests, macros, materializations, incremental models,
  snapshots, seeds, selectors, compiled SQL, or dbt artifacts. Do not use for
  generic SQL with no dbt graph, warehouse administration, semantic-layer
  product configuration, or orchestration outside dbt.
argument-hint: "[dbt model or project task, adapter, grain, materialization, and tests]"
---

# dbt graph and relation contracts

dbt code compiles a dependency graph into warehouse-specific SQL and executes
selected resources. Distinguish source text, compiled SQL, manifest/run results,
and actual warehouse relations.

## Workflow

1. Inspect dbt implementation/version, adapter, project/profile configuration,
   targets, package locks, existing conventions, model contracts, state
   artifacts, and warehouse authority. Never print credentials.
2. Define each model's entity and grain, unique key, columns, null policy,
   freshness, and materialization before writing SQL.
3. Use `source()` for declared raw sources and `ref()` for dbt dependencies.
   Do not hard-code environment-specific database/schema names where graph
   references provide the contract.
4. Keep one semantic grain per CTE/model. Add generic or singular tests for
   uniqueness, not-null, relationships, allowed values, reconciliation, and
   business invariants proportionate to consequence.
5. Choose view/table/incremental/ephemeral from consumer, cost, rebuild, and
   lineage needs. An incremental model must define cutoff, late-arrival,
   updates/deletes, unique key, schema change, and full-refresh behavior.
6. Compile first and inspect target SQL. Run the narrow selector in a safe
   target, then tests; use `dbt build` when ordered model/seed/snapshot/test
   execution is intended.
7. Inspect `manifest.json`, `run_results.json`, relation row/grain checks, and
   warehouse query behavior before declaring completion.

## Invariants

- `ref()` establishes graph order but does not prove join cardinality or model
  grain.
- Tests are executable contracts, not documentation decoration.
- Incremental correctness includes late and changed records; a fast append-only
  query is wrong when source semantics permit updates.
- Macros generate SQL and can hide dialect behavior. Inspect compiled SQL and
  test every supported adapter branch.
- Snapshots model change history; define check/timestamp strategy and invalidate
  hard deletes deliberately.

```sql
with orders as (
    select * from {{ ref('stg_orders') }}
),
customer_month as (
    select customer_id, date_trunc('month', ordered_at) as month,
           sum(net_revenue) as net_revenue
    from orders
    group by 1, 2
)
select * from customer_month
```

Read [graph and model design](references/models.md), [incremental and snapshot
semantics](references/stateful.md), and [compile/run verification](references/verification.md).
