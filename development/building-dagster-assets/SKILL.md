---
name: building-dagster-assets
description: Build Dagster pipelines using software-defined assets — asset dependencies, partitions, resources and IO managers, asset checks, and schedules/sensors. Use when creating Dagster assets or jobs, modeling data as assets, adding partitions or backfills, wiring resources/IO managers, or migrating from task-based orchestration to assets.
---

# Building Dagster Assets

## When to use

- Creating or refactoring Dagster software-defined assets and jobs.
- Modeling tables/files/ML models as assets with lineage.
- Adding partitions, backfills, asset checks, schedules, or sensors.
- Do NOT use for Airflow (use the Airflow skills).

## Workflow

```
- [ ] Model each output as an @asset; declare deps via function args
- [ ] Add partitions for time/category-sliced data
- [ ] Move IO (reads/writes) into IO managers or resources
- [ ] Add asset checks for data quality
- [ ] Schedule/sensor to materialize
```

1. **Think in assets, not tasks.** An asset is a persistent object (a table, file,
   model). Declare dependencies by referencing upstream assets as function
   parameters — Dagster builds the lineage graph automatically.
2. **Partition** assets that are naturally sliced (by day, region) so you can
   materialize/backfill one slice at a time.
3. **Resources and IO managers** hold connections and read/write logic, keeping
   asset bodies focused on transformation and making them testable.
4. **Asset checks** attach data quality assertions to an asset.

## Patterns

**Partitioned assets with a dependency:**

```python
import dagster as dg

daily = dg.DailyPartitionsDefinition(start_date="2026-01-01")

@dg.asset(partitions_def=daily)
def raw_orders(context: dg.AssetExecutionContext) -> None:
    day = context.partition_key
    write_parquet(f"raw/orders/{day}.parquet", fetch_orders(day))

@dg.asset(partitions_def=daily)
def orders_clean(context, raw_orders) -> None:  # depends on raw_orders
    day = context.partition_key
    transform_and_load(day)

@dg.asset_check(asset=orders_clean)
def no_null_ids(context) -> dg.AssetCheckResult:
    n = count_null_order_ids(context.partition_key)
    return dg.AssetCheckResult(passed=n == 0, metadata={"null_ids": n})
```

**Resource / IO manager** — inject a warehouse client instead of constructing it
inside the asset:

```python
@dg.asset
def orders_summary(context, warehouse: WarehouseResource, orders_clean):
    warehouse.execute("insert into summary select ...")
```

**Schedule** a partitioned job so each run materializes the latest partition;
use a **sensor** to materialize when an upstream file/asset appears.

## Common pitfalls

- **Task thinking** — using bare `@op`/jobs for everything loses lineage,
  observability, and partition-aware backfills that assets give for free.
- **IO inside asset bodies** — hard-coding connections makes assets untestable;
  use resources/IO managers.
- **Non-idempotent partitioned assets** — materializing a partition must overwrite
  that partition, not append (see `writing-idempotent-transformations`).
- **Skipping asset checks** — without them, bad data materializes silently;
  Dagster surfaces check failures in the UI and can block downstream.
- **Mismatched partition definitions** between dependent assets — keep the
  `partitions_def` consistent so mappings resolve.
