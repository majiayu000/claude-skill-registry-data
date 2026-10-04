---
name: orchestrating-prefect-flows
description: Build Prefect workflows — flows and tasks, retries and caching, parameters, concurrency limits, deployments and schedules, blocks for connections/secrets, and idempotent task design. Use when writing or debugging Prefect flows, scheduling runs, configuring retries/caching, or migrating scripts to Prefect orchestration.
---

# Orchestrating Prefect Flows

## When to use

- Writing or refactoring Prefect flows and tasks.
- Configuring retries, caching, parameters, concurrency, or deployments/schedules.
- Migrating standalone Python scripts into managed orchestration.
- Do NOT use for Airflow (use the Airflow skills) or Dagster assets.

## Workflow

```
- [ ] Wrap the pipeline in a @flow; decompose steps into @task
- [ ] Parameterize by run window, not now(); keep tasks idempotent
- [ ] Add retries + retry_delay on flaky/external tasks
- [ ] Cache pure tasks by input to skip redundant work
- [ ] Create a deployment with a schedule; store secrets in blocks
```

1. **Flows and tasks.** A `@flow` is the orchestrated unit; `@task` functions are
   the retryable, observable steps. Return values pass data between tasks.
2. **Idempotency + parameters.** Pass the processing window as a parameter and make
   writes upsert/overwrite so retries and reruns are safe.
3. **Retries** on tasks that call networks/warehouses; transient failures self-heal.
4. **Caching** — cache deterministic tasks keyed on inputs to avoid recomputation.
5. **Deployments** attach a schedule and infrastructure; **blocks** hold
   connections/secrets instead of hard-coding them.

## Patterns

**Flow with retries and idempotent load:**

```python
from prefect import flow, task
from datetime import timedelta

@task(retries=3, retry_delay_seconds=30)
def extract(run_date):
    return fetch_orders(run_date)          # window is a parameter, not now()

@task
def load(rows, run_date):
    overwrite_partition("fct_orders", run_date, rows)   # idempotent

@flow(name="orders")
def orders(run_date: str):
    load(extract(run_date), run_date)
```

**Caching a pure task:**

```python
from prefect.tasks import task_input_hash
@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1))
def transform(rows): ...
```

**Deployment + schedule** — `flow.serve(name="daily", cron="0 6 * * *")` or a
`prefect.yaml` deployment; set concurrency limits to protect the warehouse.

## Common pitfalls

- **`datetime.now()` inside tasks** — breaks idempotency and backfills; pass the
  run window as a parameter.
- **No retries on external calls** — every transient blip fails the flow.
- **Caching non-deterministic tasks** — returns stale/wrong results; only cache
  pure functions.
- **Secrets in code** — use blocks (`Secret`, connection blocks), not literals.
- **One giant task** — retries reprocess everything; split into granular tasks.
- **Unbounded concurrency** — parallel tasks overwhelm the source/warehouse; set
  concurrency limits.
