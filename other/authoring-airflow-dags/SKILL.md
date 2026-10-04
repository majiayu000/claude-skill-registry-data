---
name: authoring-airflow-dags
description: Write production-grade Apache Airflow DAGs using the TaskFlow API — idempotent tasks, correct scheduling and catchup, retries/SLAs, connections/variables, and avoiding top-level code. Use when creating or reviewing Airflow DAGs, scheduling pipelines, wiring task dependencies, configuring retries/backfills, or fixing non-idempotent tasks.
---

# Authoring Airflow DAGs

## When to use

- Creating or refactoring Airflow DAGs and tasks.
- Configuring schedules, catchup/backfill, retries, and SLAs.
- Passing data between tasks (XCom) or using connections/variables.
- Do NOT use for diagnosing a broken running DAG (use
  `debugging-airflow-pipelines`).

## Workflow

```
- [ ] Make each task idempotent and parameterized by the data interval
- [ ] Keep expensive/import-heavy code inside tasks, not at module top level
- [ ] Set schedule + catchup deliberately
- [ ] Configure retries, retry_delay, and SLAs
- [ ] Wire dependencies via TaskFlow return values or >> operators
```

1. **Idempotent tasks** — a task for the `2026-01-15` interval must produce the
   same result whether it runs once or is re-run. Use the data interval, not
   `datetime.now()`.
2. **No heavy top-level code** — the scheduler parses every DAG file frequently;
   database calls, API calls, or big imports at module level slow scheduling and
   can break parsing. Put them inside tasks.
3. **Schedule + catchup on purpose** — `catchup=True` backfills every missed
   interval from `start_date`; default to `False` unless you want that.
4. **Retries and SLAs** — transient failures are normal; set `retries` and
   `retry_delay`; use SLAs/alerts for lateness.

## Patterns

**TaskFlow DAG, idempotent and cleanly wired:**

```python
from airflow.decorators import dag, task
import pendulum

@dag(
    schedule="@daily",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    catchup=False,
    default_args={"retries": 3, "retry_delay": pendulum.duration(minutes=5)},
    tags=["orders"],
)
def orders_pipeline():

    @task
    def extract(data_interval_start=None):
        # Use the interval, not now(), so re-runs are deterministic.
        return fetch_orders(day=data_interval_start.date())

    @task
    def load(rows):
        # Delete-insert the partition -> idempotent on retry.
        overwrite_partition("fct_orders", rows)

    load(extract())

orders_pipeline()
```

**Pass small data via XCom (return values); pass large data via storage** — write
to S3/GCS/warehouse and pass the path/key, never megabytes through XCom.

**Use connections/variables** for secrets and config (`BaseHook.get_connection`,
`Variable.get`), never hard-coded credentials.

## Common pitfalls

- **Top-level API/DB calls or heavy imports** — slow the scheduler and can fail
  DAG parsing across the whole deployment.
- **`datetime.now()` inside tasks** — breaks idempotency and backfills; use
  `data_interval_start`/`_end`.
- **`catchup=True` unintentionally** — floods the cluster with historical runs on
  first deploy.
- **Large payloads through XCom** — bloats the metadata DB; pass references.
- **Dynamic `start_date`** (e.g. `days_ago`) — makes schedules nondeterministic;
  use a fixed timestamp.
- **One monster task** — split extract/transform/load so retries are granular.

## References

- [Scheduling, catchup, and backfill reference](references/SCHEDULING.md)
