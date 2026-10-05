---
name: prefect-flows
description: Use when prefect workflow orchestration — flows, tasks, deployments,
  work pools, schedules, retries. Use when working with prefect flows.
domain: data
author: oyi77
license: Apache-2.0
subdomain: data-engineering
tags:
- analytics
- data-analysis
- flows
- prefect
- visualization
- workflow
version: 1.0.0
category: data
---



## Overview

Prefect is a modern workflow orchestration framework for Python. It uses decorators to define flows and tasks with built-in retries, caching, concurrency, and deployment management. Prefect Cloud/Server provides a UI for monitoring and managing workflows.

## Capabilities

- Define workflows with @flow and @task decorators
- Configure retries, timeouts, and caching per task
- Deploy flows to work pools for scheduled/triggered execution
- Use task runners for parallel/concurrent execution
- Manage secrets and configuration via Prefect blocks
- Monitor runs via Prefect Cloud UI

## When to Use

**Trigger phrases:**
- "prefect flows"
- "Building Python-based data pipelines"
- "Needing local development with cloud deployment"
- "Wanting simple decorator-based workflow definition"


- Building Python-based data pipelines
- Needing local development with cloud deployment
- Wanting simple decorator-based workflow definition
- Managing retries and error handling for unreliable tasks
- Scheduling and triggering workflows remotely

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code

The prefect-flows workflow follows a standard pipeline pattern.

Core flow:
```
# prefect-flows primary flow
input = prepare(raw_data)
result = process(input, config={deployments, flows, orchestration, pools, prefect})
validate(result)
deliver(result)
```

Error handling:
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Flow and Task Definition

```python
from prefect import flow, task
import httpx
import pandas as pd

@task(retries=3, retry_delay_seconds=30)
def fetch_data(url: str) -> dict:
    response = httpx.get(url, timeout=30)
    response.raise_for_status()
    return response.json()

@task
def transform(data: dict) -> pd.DataFrame:
    df = pd.DataFrame(data['results'])
    df['processed_at'] = pd.Timestamp.now()
    return df

@task
def load(df: pd.DataFrame, table: str):
    df.to_sql(table, con=engine, if_exists='append')

@flow(name="ETL Pipeline")
def etl_pipeline(url: str, table: str):
    data = fetch_data(url)
    df = transform(data)
    load(df, table)
```

### Task Caching

```python
from prefect import task
from prefect.tasks import task_input_hash
from datetime import timedelta

@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1))
def expensive_query(date: str) -> pd.DataFrame:
    return pd.read_sql(f"SELECT * FROM events WHERE date='{date}'", con=engine)
```

### Parallel Execution

```python
from prefect import flow, task
from prefect.futures import submit

@task
def process_file(filename: str) -> int:
    df = pd.read_csv(filename)
    return len(df)

@flow
def parallel_pipeline(files: list[str]):
    # Submit tasks in parallel
    futures = [submit(process_file, f) for f in files]
    results = [f.result() for f in futures]
    print(f"Processed {sum(results)} total rows")
```

### Deployment

```python
from prefect import flow

@flow
def my_flow(name: str):
    print(f"Hello {name}")

# Deploy via CLI:
# prefect deploy my_flow.py:my_flow -n daily-greeting --cron "0 9 * * *"

# Or programmatic deployment
if __name__ == "__main__":
    my_flow.serve(
        name="daily-greeting",
        cron="0 9 * * *",
        parameters={"name": "World"},
    )
```

### Work Pool

```bash
# Create work pool
prefect work-pool create my-pool --type process

# Start worker
prefect worker start --pool my-pool

# Deploy to pool
prefect deploy --pool my-pool --work-queue default
```

### Retries with Backoff

```python
import random

@task(retries=5, retry_delay_seconds=exponential_backoff(backoff_factor=10))
def flaky_api_call():
    if random.random() < 0.7:
        raise Exception("Transient failure")
    return {"status": "ok"}
```

### Subflows

```python
@flow
def sub_flow(data: dict) -> dict:
    return {"processed": len(data)}

@flow
def parent_flow():
    data = fetch_data()
    result = sub_flow(data)  # Nested flow run
    print(result)
```

## Common Patterns

| Pattern | When to Use |
|---------|------------|
| `@task(retries=N)` | Retry on transient failures |
| `cache_key_fn=task_input_hash` | Skip recomputation for same inputs |
| `submit()` | Parallel task execution |
| `serve()` | Long-running deployment with schedule |
| `prefect deploy` | Deploy to work pool |
| Subflows | Logical grouping of related tasks |
| `exponential_backoff` | Avoid hammering failing services |

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `FlowRunFailed` | Unhandled exception in flow | Check traceback in Prefect UI |
| Task stuck in `Pending` | No worker available | Start worker for the work pool |
| `TimeoutError` | Task exceeded `timeout_seconds` | Increase timeout or optimize task |
| Deployment not running | Missing schedule or worker | Check `prefect deployment ls` and worker status |

## How to Use

1. Define data sources, sinks, and transformation requirements
2. Implement extraction with error handling and schema validation
3. Add transformation logic with idempotency guarantees
4. Configure loading with conflict resolution (upsert/append)
5. Set up monitoring for pipeline health and data freshness
6. Test with representative sample data before production

## Red Flags

- **Data pipeline has no error handling**: Silent failures corrupt downstream datasets
- **No data validation at boundaries**: Bad input propagates through entire pipeline
- **Missing monitoring for data freshness**: Stale data causes wrong business decisions
- **No rollback on failed transforms**: Failed transforms without rollback require manual recovery
- **Hardcoded connection strings**: Credentials in code get committed to version control

## Verification

- [ ] Skill output matches expected behavior

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "CSV is fine for everything" | Structured databases enable queries, integrity, and scale. |
| "I will add data validation later" | Bad data propagates silently. Validate at ingestion. |
| "Small datasets do not need optimization" | Even small datasets benefit from proper indexing and schema design. |