---
name: prefect
description: "Build Prefect flows and tasks, configure deployments and work pools, and troubleshoot retries or pipeline observability."
category: devops
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["prefect", "orchestration", "flows", "etl", "python", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Prefect Flow Orchestration AI Skill Guide

## Overview & Engine Architecture

Prefect 2/3 wraps Python functions as `@task` / `@flow` with state tracking in Prefect API/Cloud. Deployments schedule flows onto work pools/workers. Agents keep tasks pure and idempotent, configure retries/caching deliberately, and pass artifact URIs instead of giant in-memory payloads between tasks.

```
@flow / @task code
      -> Prefect API (runs, states)
          -> work pool / worker
              -> infrastructure (process, Docker, K8s)
```

## When to use this skill

- Python-first pipelines with lighter DAG boilerplate than Airflow
- Deploying the same flow to local, Docker, or Kubernetes workers
- Retries, caching, and run observability for ETL/ML batch jobs

## Operational directives

1. Put side effects inside tasks; keep flow functions as wiring.
2. Set `retries` and `retry_delay_seconds` on flaky I/O tasks.
3. Use `cache_key_fn` / cache policies only when inputs are stable and outputs cheap to reuse.
4. Persist large data to storage; return paths/IDs from tasks.
5. Store blocks/secrets in Prefect - do not hardcode credentials in flow code.

## Flow example

```python
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta
from pathlib import Path

@task(retries=3, retry_delay_seconds=30)
def extract(run_date: str) -> Path:
    out = Path(f"/data/raw/orders_{run_date}.parquet")
    # ... write parquet ...
    return out

@task
def transform(path: Path) -> Path:
    out = path.with_name(path.name.replace("raw", "curated"))
    # ... polars/duckdb transform ...
    return out

@flow(name="orders-daily")
def orders_daily(run_date: str = "2026-08-26"):
    raw = extract(run_date)
    return transform(raw)

if __name__ == "__main__":
    orders_daily()
```

## Deploy / run CLI

```bash
prefect flow serve flows/orders.py:orders_daily --name orders-daily-local
prefect deployment run 'orders-daily/orders-daily-local' --param run_date=2026-08-26
prefect worker start --pool default-agent-pool
```

## Common failures

| Symptom | Cause | Fix |
| --- | --- | --- |
| Late runs | worker offline / wrong pool | check worker logs; pool binding |
| Retry storm | non-idempotent task | make upserts; fix side effects |
| Crashed after success | client timeout vs long task | heartbeats; infra timeouts |
| Param mismatch | schema drift | type the flow signature; validate |

## Best practices

- Name flows/deployments stably for dashboard history.
- Use artifacts (`create_markdown_artifact`) for run summaries.
- Separate scheduling (deployment) from business logic (flow module).
- Pin `prefect` major version; APIs differ between 2.x lineages and Cloud features.

## Limitations

- Exact CLI/deployment UX varies by Prefect version and Cloud vs OSS.
- Not a replacement for warehouse-native schedulers when only SQL needs to run.
- Infra provisioning (K8s jobs, IAM) remains environment-specific.

## Related skills

- `@airflow` - DAG-centric alternative common in enterprises
- `@dbt` / `@spark` - systems often invoked from Prefect tasks
- `@pandas` / `@polars` - in-task compute
