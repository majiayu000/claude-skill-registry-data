---
name: debugging-airflow-pipelines
description: Diagnose failing or stuck Apache Airflow pipelines — task failures and retries, scheduler/executor problems, XCom errors, zombie/queued tasks, dependency deadlocks, and pools/concurrency limits. Use when an Airflow task fails or is stuck queued, the scheduler is not running tasks, a DAG will not trigger, or tasks become zombies.
---

# Debugging Airflow Pipelines

## When to use

- A task failed, is stuck in `queued`/`scheduled`, or became a zombie.
- The scheduler isn't launching runs, or a DAG won't trigger.
- XCom pull errors, dependency deadlocks, or pool/concurrency starvation.
- Do NOT use for writing new DAGs (use `authoring-airflow-dags`).

## Workflow

```
- [ ] Read the task log first (Grid view -> task -> Logs)
- [ ] Check task state and why: failed, up_for_retry, queued, or none
- [ ] Localize: task-level bug vs scheduler/executor vs resource limit
- [ ] Fix root cause, then clear the task to re-run
```

1. **Read the task log.** The Grid/Graph view → failed task → Logs shows the real
   exception nearly every time.
2. **Check the state and reason.** `queued` for a long time is usually a
   resource/executor issue, not a code bug.
3. **Localize** using the table below.
4. **Re-run** by clearing the task instance (and downstream if needed) rather than
   re-triggering the whole DAG.

## Patterns

**Task keeps failing** — read the log; fix the exception; confirm `retries` are
set so transient errors self-heal. Use `on_failure_callback` for alerting.

**Task stuck in `queued`/`scheduled`:**

- Worker capacity exhausted, or a `pool` is full → check pool slots and
  `max_active_tasks`/parallelism.
- Celery/Kubernetes executor not picking up → check worker health and the message
  broker/queue.

**Zombie tasks** (process died, heartbeat lost) → often OOM or a killed worker.
Check worker memory/logs; reduce task memory or raise limits; Airflow marks it
failed and retries.

**Scheduler not creating runs:**

- DAG parse error → `airflow dags list-import-errors` (top-level code exceptions).
- DAG paused, or `start_date` in the future, or `catchup=False` with no new
  interval yet.
- `max_active_runs` reached → older runs not completing block new ones.

**Dependency deadlock / "no status"** — an upstream is `skipped` with the default
trigger rule; adjust `trigger_rule` (e.g. `all_done`, `none_failed_min_one_success`)
for branch/cleanup tasks.

**XCom errors** — pulling a key a task never pushed, or a payload too large for the
metadata DB. Push explicitly and pass storage references for big data.

## Common pitfalls

- **Re-triggering the whole DAG** instead of clearing the failed task — reruns
  work already done and can duplicate non-idempotent side effects.
- **Blaming code for `queued` tasks** — check pools, parallelism, and workers first.
- **Ignoring import errors** — one bad DAG file can stall parsing/scheduling.
- **No retries on flaky external calls** — every transient blip pages someone.
- **Clearing a non-idempotent task** — confirm the task is safe to re-run, or you
  duplicate data (see `writing-idempotent-transformations`).
