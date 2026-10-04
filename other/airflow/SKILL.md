---
name: airflow
description: "Build and troubleshoot Apache Airflow DAGs, operators, sensors, schedules, and retry behavior for data pipelines."
category: devops
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["airflow", "orchestration", "dags", "etl", "scheduling", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Apache Airflow AI Skill Guide

## Overview & Engine Architecture

Airflow schedules DAGs of tasks executed by workers; the scheduler parses DAG files, the metadata DB stores run state, and executors (Local/Celery/Kubernetes) run task instances. Agents write idempotent tasks, set explicit retries/timeouts, avoid top-level heavy I/O in DAG files, and pass data via XCom sparingly (or external storage).

```
DAG file -> scheduler -> executor/workers
                |
           metadata DB (runs, XCom)
                |
           task logs / sensors
```

## When to use this skill

- Time-based or data-aware batch pipelines
- Orchestrating dbt, Spark, warehouse SQL, ML batch jobs
- Backfills with clear logical dates

## Operational directives

1. Keep DAG top-level code fast (imports + structure only).
2. Tasks must be idempotent for a given `data_interval` / logical date.
3. Set `retries`, `retry_delay`, and `execution_timeout` intentionally.
4. Prefer pushing large payloads to object storage over big XComs.
5. Never commit connection passwords; use Airflow Connections / secrets backend.

## Minimal DAG

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="orders_daily",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=5)},
    tags=["orders"],
) as dag:
    extract = BashOperator(
        task_id="extract",
        bash_command="python /opt/airflow/jobs/extract_orders.py --date {{ ds }}",
    )
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /opt/dbt && dbt build --select marts.* --vars '{run_date: {{ ds }}}'",
    )
    extract >> dbt_run
```

## Useful CLI

```bash
airflow dags list
airflow dags test orders_daily 2026-08-26
airflow tasks test orders_daily extract 2026-08-26
```

## Common failures

| Symptom | Cause | Fix |
| --- | --- | --- |
| DAG not appearing | import error / parse fail | check scheduler logs |
| Zombie / stuck tasks | worker death | timeouts; health checks |
| Huge backfill load | catchup=True | limit; clear carefully |
| Sensor hanging | wrong poke / mode | reschedule mode; timeouts |

## Best practices

- One business pipeline per DAG id; stable task ids for clear history.
- Use datasets/data-aware scheduling when producers/consumers share tables.
- Pin provider package versions with Airflow constraints.
- Alert on SLA misses and failed task emails/Slack callbacks.

## Limitations

- Not a streaming engine; pair with Kafka/Flink for continuous event processing.
- Executor/deployment topology (MWAA, Composer, K8s) changes ops details.
- This skill does not replace capacity planning for workers/metadata DB.

## Related skills

- `@prefect` - alternative Python-native orchestration
- `@dbt` - SQL models often invoked from Airflow
- `@spark` - heavy distributed tasks
