---
name: litestar-queues
description: "Use when working with litestar_queues, QueuePlugin, QueueConfig, WorkerConfig, QueueService, @task, QueuedBackgroundTask, QueueEventsConfig, or SQLSpecBackendConfig. Not for litestar-saq, Celery, or Dramatiq."
---

# litestar-queues

`litestar-queues` is the first-party Litestar worker abstraction for task registration, durable queue state, worker lifecycle, schedules, uniqueness, bounded maintenance, execution dispatch, and application-facing task events.

Keep persistence and placement separate:

- A **queue backend** stores task records, identities, maintenance coordination, and optional event history.
- An **execution backend** decides where a claimed task runs.
- **Worker wakeups** are delivery hints. Persisted queue records remain the source of truth.

## Code Style Rules

- Use `QueuePlugin` to wire lifecycle, application state, DI, task discovery, schedules, workers, and CLI commands.
- Put worker settings under `QueueConfig(worker=WorkerConfig(...))`.
- Inject `QueueService` with `NamedDependency[QueueService]`; never use a module-level service from handlers.
- Import public core types from `litestar_queues`. Import optional backend configuration from its backend submodule (`.sqlspec`, `.advanced_alchemy`, `.redis`, `.valkey`) and execution configs from `litestar_queues` or their respective submodules.
- Keep persistent-backend arguments and metadata JSON-serializable. Pass stable object IDs instead of large payloads.
- Use PEP 604 unions (`T | None`) and async I/O. Prefer `msgspec` for event/client DTOs unless the project already uses Pydantic.

## Quick Reference

### Minimal Plugin Setup

```python
from litestar import Litestar, post
from litestar.di import NamedDependency
from litestar_queues import QueueConfig, QueuePlugin, QueueService, WorkerConfig, task


@task("accounts.sync", queue="accounts", retries=3, timeout=300)
async def sync_account(account_id: str) -> dict[str, str]:
    return {"account_id": account_id, "status": "synced"}


@post("/accounts/{account_id:str}/sync")
async def create_sync_job(
    account_id: str,
    queue_service: NamedDependency[QueueService],
) -> dict[str, str]:
    result = await queue_service.enqueue(sync_account, account_id)
    return {"task_id": str(result.id), "status": result.status or "queued"}


app = Litestar(
    route_handlers=[create_sync_job],
    plugins=[
        QueuePlugin(
            QueueConfig(worker=WorkerConfig(placement="server")),
        ),
    ],
)
```

`QueueConfig()` with no arguments defaults to `queue_backend="ephemeral"`, `execution_backend="local"`, and `placement="server"` — a private per-invocation SQLite database plus one CLI-owned worker process, with no broker, port, or extra dependency. Keep that shape for tests, development, and small single-process deployments only.

Process-local `"memory"` storage must be asked for explicitly, together with a placement that shares the process:

```python
from litestar_queues import QueueConfig, WorkerConfig

config = QueueConfig(queue_backend="memory", worker=WorkerConfig(placement="asgi"))
```

Storage, execution, and placement combinations that cannot work are rejected at startup with a message naming the fix, rather than failing at first claim.

### Task Options, Scheduling, and Uniqueness

```python
from datetime import timedelta

from litestar_queues import QueueEventActor, QueueService, RetryBackoff, non_retryable, task


@task(
    "reports.render",
    queue="reports",
    priority=10,
    retries=3,
    retry_backoff=RetryBackoff(initial_delay=2.0, multiplier=2.0, max_delay=60.0),
    timeout=120,
    run_after=30,
    expires_in=timedelta(minutes=30),
    unique_by="arguments",
    unique_until="terminal",
    actor=QueueEventActor(type="service", id="reports-worker", name="Reports Worker"),
)
async def render_report(report_id: str, *, format: str = "pdf") -> str:
    if report_id == "invalid":
        non_retryable("Report ID does not exist")
    return f"{report_id}.{format}"


@task("reports.refresh", interval=timedelta(minutes=15), jitter=30, retries=2)
async def refresh_reports() -> None:
    pass


async def queue_report(queue_service: QueueService, report_id: str) -> str:
    result = await queue_service.enqueue(
        render_report,
        report_id,
        timeout=600,
        metadata={"requested_by": "system"},
    )
    await result.wait(timeout=30)
    return result.status or "unknown"
```

In addition to `await queue_service.enqueue(render_report, ...)` (the primary DI pattern in route handlers), decorated tasks expose `await render_report.enqueue(report_id)` and `await render_report.using(priority=20, run_after=60).enqueue(report_id)`. `Task.enqueue()` uses the active default `QueueService` registered by `QueuePlugin`, or falls back to an inline `"memory"` + `"immediate"` service when called in unit tests with no application wired. `result.record` holds the `QueuedTaskRecord` returned at enqueue time.

When enqueueing against an external execution backend such as Cloud Tasks, catch `QueueDispatchError` (`from litestar_queues.exceptions import QueueDispatchError`) and inspect `exc.committed`: when `True`, the record (`exc.task_id`) is already durably committed in SQL and bounded maintenance will repair the lost delivery.

Identity precedence is strict:

1. Explicit enqueue `key`.
2. Configured task `key`.
3. `unique_by="task"`.
4. `unique_by="arguments"`.
5. No identity.

`unique_until="terminal"` is the default and releases the identity after completion, failure, or cancellation. `unique_until="forever"` stores a permanent reservation until `await queue_service.reset_task_identity(effective_key)` removes it.

Do not combine a configured `key` with `unique_by`. Do not set `unique_until="forever"` without a configured `key` or `unique_by`. Use `QueueConfig.max_argument_identity_bytes` to bound canonical payloads hashed by `unique_by="arguments"`.

Use `interval` or five-field `cron`, never both. Recurring tasks inherit configured `retries` on startup and succession, and persisted occurrences retain their retry budget and backoff until completion. Use `task_modules=("app.domain.reports.jobs",)`, `discover_tasks("app.domain", "jobs")`, or `AutowirePlugin(AutowireConfig(domain_packages=["app.domain"], integrations=["dishka", "queues"]))` before string enqueueing or schedule initialization.

To mark a failure permanent and bypass retries, call `non_retryable("message")` or raise `NonRetryableError`. To cooperatively cancel execution from within a handler, call `job_cancelled("message")` or raise `JobCancelledError`. Calling `await queue_service.cancel_task(task_id, include_running=True)` cancels any active remote provider execution (Cloud Run Jobs or Cloud Tasks) first before writing durable cancellation state.

### Dependency Injection, Error Sanitization, and Role-Aware Worker Factory

- **Attempt-scoped DI (`task_dependency_provider`)**: Enters an `@asynccontextmanager` per attempt `(task, record, context) -> AsyncIterator[Mapping[str, Any]]`, merges the yielded mapping into task keyword arguments, and guarantees clean exit on success, error, timeout, or cancellation. When using **Dishka**, reuse an active in-process request container (`request_container_var.get()`) when running inline or open a fresh `Scope.REQUEST` scope on the worker container.
- **Error sanitization & stale priority**: Set `error_sanitizer=Callable[[BaseException, QueuedTaskRecord], str]` to convert exceptions into persisted error strings, and `stale_requeue_priority` (`"preserve"`, `int`, or `Callable[[int], int]`) for stale task recovery.
- **Worker placement (`WorkerConfig.placement`)**:
  - `"server"` (default): starts one worker in the CLI server lifespan (`litestar run`).
  - `"asgi"`: starts one worker per ASGI worker in the application lifespan (e.g., `target == "local" and role == "web"`).
  - `"external"`: starts nothing automatically; managed processes run `litestar queues run` or `litestar queues run-consumer` (or receive push deliveries on `role == "consumer"`).
- **Role-aware factory (`create_queue_config`)**: Mount `EventStreamConfig` only on the `"web"` role (`None` on `"consumer"` and `"cli"`), and harden `CloudTasksExecutionConfig` by enabling `trust_platform_auth=(role == "consumer")` and attaching a deny guard when `role != "consumer"`. See [Backends, Worker Configuration, Events, and Maintenance](references/backends-and-events.md) for complete factory and Dishka container examples.

```bash
LITESTAR_APP=app:app litestar queues run --queue default --max-concurrency 4 --drain-timeout 60
LITESTAR_APP=app:app litestar queues run-consumer --backend sqs --max-concurrency 4 --drain-timeout 60
LITESTAR_APP=app:app litestar queues status --json
LITESTAR_APP=app:app litestar queues scheduler-health --minutes 5
LITESTAR_APP=app:app litestar queues run-maintenance --json
```

### Backend Selection

Queue backends own persistence:

| Existing stack or need | Queue backend | Import |
| --- | --- | --- |
| Default; dev and single-invocation apps | `"ephemeral"` | Core package (stdlib `sqlite3`) |
| Process-local tests, shared-process placement only | `"memory"` (`InMemoryQueueBackend`) | Core package (`litestar_queues`) |
| SQLSpec-managed SQL persistence | `SQLSpecBackendConfig(...)` | `litestar_queues.backends.sqlspec` |
| Advanced Alchemy / SQLAlchemy models | `SQLAlchemyBackendConfig(...)` | `litestar_queues.backends.advanced_alchemy` |
| Existing Redis infrastructure | `RedisBackendConfig(...)` | `litestar_queues.backends.redis` |
| Existing Valkey infrastructure | `ValkeyBackendConfig(...)` | `litestar_queues.backends.valkey` |

Execution backends decide where a claimed task runs, and never own queue state:

| Need | Execution backend | Import |
| --- | --- | --- |
| Default in-process workers | `"local"` | Core package |
| Inline completion in tests/scripts | `"immediate"` | Core package |
| Isolated Google Cloud Run Jobs | `CloudRunExecutionConfig(...)` | `litestar_queues.execution.cloudrun` |
| Serverless delivery with no worker process | `CloudTasksExecutionConfig(...)` | `litestar_queues.execution.cloudtasks` |
| Apache Kafka continuous consumer fleet | `KafkaExecutionConfig(...)` | `litestar_queues.execution.kafka` |
| GCP Pub/Sub continuous consumer fleet | `PubSubExecutionConfig(...)` | `litestar_queues.execution.pubsub` |
| RabbitMQ continuous consumer fleet (Python 3.11+) | `RabbitMQExecutionConfig(...)` | `litestar_queues.execution.rabbitmq` |
| Amazon SQS continuous consumer fleet | `SqsExecutionConfig(...)` | `litestar_queues.execution.sqs` |

Match the project's existing data stack. Memory cannot coordinate separate processes and has no `MemoryBackendConfig` class — pass `queue_backend="memory"` or an `InMemoryQueueBackend` instance. See [Execution Backends](references/execution-backends.md) and [Backends, Worker Configuration, Events, and Maintenance](references/backends-and-events.md).

### Persistent Backends & Schema

- **SQLSpec (`SQLSpecBackendConfig`)**: When `manage_schema=True` (default), `QueuePlugin` registers the `0001_create_queue_tasks` migration revision. When `manage_schema=False`, register `"litestar_queues"` in `migration_config={"include_extensions": ["events", "litestar_queues"]}` and wire `configure_queue_migration_extension(...)` from `litestar_queues.backends.sqlspec.extension`. `worker_wakeups` defaults to `SQLSpecWorkerWakeupConfig` (`notify_queue` on PostgreSQL, `poll_queue` on DuckDB); set `worker_wakeups=None` with `CloudTasksExecutionConfig`.
- **Advanced Alchemy (`SQLAlchemyBackendConfig`)**: Pass `sqlalchemy_config=alchemy_config` and manage schema via application Alembic migrations (`QueueTaskModelMixin`, `QueueEventHistoryModelMixin`, `QueueMaintenanceModelMixin`, `QueueTaskReservationModelMixin`). Set `worker_wakeups=True` only on PostgreSQL.
- **Redis & Valkey (`RedisBackendConfig` / `ValkeyBackendConfig`)**: Use pub/sub wakeup hints by default with keys namespaced under `key_prefix`.

| Concern | Default table | Override setting (`SQLSpecBackendConfig`) |
| --- | --- | --- |
| Queue records | `queue_task` | `queue_table_name` |
| Distributed maintenance coordination | `queue_maintenance` | `maintenance_table_name` |
| Forever-uniqueness reservations | `queue_task_reservation` | `task_reservation_table_name` |
| Durable event history (when enabled) | `queue_task_event_history` | `event_history_table_name` |

Do not delete the reservation table during ordinary task or event retention. Forever identities are removed only through `QueueService.reset_task_identity()`.

### Events, Progress, Observability, and Bounded Maintenance

- **`QueueEventsConfig`**: Groups live `delivery` (`EventDeliveryConfig`), browser `stream` (`EventStreamConfig(path="/queues/events", transports={"sse", "websocket"})`), and durable `history` (`EventHistoryConfig` with optional `EventHistoryExtraColumn`). Inside `@task` functions, check `context = get_current_task_context()` before calling `await context.progress(...)`, `await context.log(...)`, or `await publish_task_event(...)`, and call `beat("stage")` for heartbeats. Query persisted events via `await queue_service.get_event_log().query_events(QueueEventQuery(...))` and `summarize_stages(...)`.
- **`ObservabilityConfig`**: Configures OpenTelemetry tracing (`enable_otel=True`), Prometheus metrics (`enable_prometheus=True`), and SQLCommenter (`enable_sqlcommenter=True`), plus `scheduler_canary_task` verified by `litestar queues scheduler-health --minutes 5`.
- **Bounded Maintenance (`QueueMaintenanceConfig`)**: Runs four bounded phases in fixed order (`external` reconciliation, `stale` recovery, `terminal` retention, `event` retention) via `litestar queues run-maintenance --json` or `QueueMaintenanceService(service, config).run()`. Retention thresholds (`stale_after`, `terminal_retention`, `event_retention_rules`) default to `None`/empty (disabled); `coordination_timeout` must exceed `time_budget`. Schedule one external invocation every six hours or daily. See [Backends, Worker Configuration, Events, and Maintenance](references/backends-and-events.md) for full configuration snippets.

### External One-Task Execution & Background Responses

- **`litestar queues run-task`**: Claims and executes one existing record for an external executor (such as Cloud Run Jobs), reading `QUEUES_TASK_ID`, `QUEUES_CONFIG_FACTORY`, and `LITESTAR_QUEUES_TASK_MODULES` (or `--task-id`, `--config-factory`, `--task-modules`). It is not a standalone worker loop.
- **`QueuedBackgroundTask`**: Return `Response({"status": "accepted"}, background=QueuedBackgroundTask(process_import, "/tmp/data.csv"))` from a route handler to enqueue a task after the HTTP response is sent.

<workflow>

## Workflow

1. **Identify the work shape.** Use Litestar Queues for durable task state, worker placement, schedules, progress/events, task uniqueness, or bounded maintenance.
2. **Match the queue backend.** Use `"memory"` for same-process tests, `SQLSpecBackendConfig` for SQLSpec apps, `SQLAlchemyBackendConfig` for Advanced Alchemy apps, `RedisBackendConfig` for Redis, or `ValkeyBackendConfig` for Valkey.
3. **Pick execution placement.** Use `"local"` workers by default, `"immediate"` for tests/scripts, broker consumers (Kafka, Pub/Sub, RabbitMQ, SQS) for distributed dispatch, `CloudTasksExecutionConfig` for serverless push delivery, and `CloudRunExecutionConfig` for isolated external jobs.
4. **Configure the worker & storage.** Put worker settings under `WorkerConfig` and provision SQLSpec or Advanced Alchemy schema migrations explicitly.
5. **Define, discover, and enqueue tasks.** Decorate callables with `@task`, import task modules via `task_modules` or `discover_tasks()` before string enqueueing or schedule init, and inject `NamedDependency[QueueService]` in route handlers.
6. **Add optional capabilities & operational commands.** Configure worker wakeups, `QueueEventsConfig`, permanent uniqueness, `ObservabilityConfig`, and `QueueMaintenanceConfig` as needed; run `litestar queues run` / `run-consumer` continuously, `run-task` in one-shot executors, and `run-maintenance` on a six-hour or daily schedule.

</workflow>

<guardrails>

## Guardrails

- **Use `SQLAlchemyBackendConfig` for Advanced Alchemy persistence.** Import it from `litestar_queues.backends.advanced_alchemy` (do not look for `AdvancedAlchemyAsyncBackendConfig` or `AdvancedAlchemySyncBackendConfig`).
- **Use current config and status types.** Use `CloudRunExecutionConfig` (not `CloudRunExecutorConfig`), `TaskStatus` (not `JobStatus`), `RetryBackoff` (not `BackoffStrategy`), `ScheduleConfig` (not `Schedule`), and integer `priority` (not `TaskPriority`); do not look for removed `ConcurrencyLock` or `RateLimit` classes.
- **Use `queue_table_name` on `SQLSpecBackendConfig`.** Do not pass the removed `table_name` parameter.
- **Configure events with `QueueEventsConfig`.** Add `EventDeliveryConfig`, `EventStreamConfig`, and/or `EventHistoryConfig` for the required capabilities.
- **Do not pass flat worker fields to `QueueConfig`.** Use `QueueConfig(worker=WorkerConfig(...))`.
- **Do not use `memory` across processes or look for `MemoryBackendConfig`.** Pass `queue_backend="memory"` or `InMemoryQueueBackend`; it cannot coordinate standalone workers or a separate maintenance command.
- **Do not confuse wakeups with task events.** Wakeups hint that work may exist; task events serve application and operator consumers.
- **Do not rely on wakeups for correctness.** Notifications may be delayed or lost; poll and claim durable state.
- **Do not let the backend open path own migrations.** Run SQLSpec migrations explicitly or manage Advanced Alchemy schema in the application.
- **Do not omit maintenance or reservation storage.** Provision all four SQL concerns used by the deployment.
- **Do not enable retention implicitly.** Leave each destructive threshold at `None` until an explicit policy exists.
- **Do not run maintenance as a minute-level task.** Use one bounded external invocation every six hours or daily.
- **Do not combine `key` and `unique_by`.** Select one identity source.
- **Do not assume `run-task` starts a worker.** It consumes one already-persisted record and exits.
- **Do not import optional configs from `litestar_queues.backends`.** Use the concrete `.sqlspec`, `.advanced_alchemy`, `.redis`, or `.valkey` module.
- **Do not enqueue by string before task discovery.** Import task modules or call `discover_tasks()`.

</guardrails>

<validation>

## Validation Checkpoint

- [ ] The dependency floor is `litestar-queues>=0.14.0`
- [ ] `QueuePlugin` receives one `QueueConfig`
- [ ] Worker options live under `QueueConfig.worker`
- [ ] `WorkerConfig.placement` matches the deployment topology
- [ ] Standalone workers use a shared persistent queue backend
- [ ] The backend matches the project's SQLSpec, Advanced Alchemy, Redis, or Valkey stack
- [ ] SQLSpec uses `sqlspec_config` and the normal migration workflow
- [ ] Advanced Alchemy uses `SQLAlchemyBackendConfig` and application-owned migrations
- [ ] All enabled SQL concerns have queue, event-history, maintenance, and reservation tables
- [ ] Worker wakeups are configured independently from application task events
- [ ] `QueueEventsConfig` enables delivery, stream, or history
- [ ] Task modules are loaded before string enqueueing and schedule initialization
- [ ] Handlers inject `NamedDependency[QueueService]`
- [ ] Uniqueness uses one identity source and the intended lifetime
- [ ] `max_argument_identity_bytes` bounds untrusted argument-derived identity inputs
- [ ] Maintenance thresholds and one external schedule are explicit
- [ ] `run`, `run-consumer`, `run-task`, and `run-maintenance` are used for their distinct lifecycles

</validation>

<example>

## Example

**Task:** Persist report jobs with SQLSpec, run a standalone worker, deduplicate equivalent calls, and perform bounded retention.

```python
from litestar import Litestar, post
from litestar.di import NamedDependency
from sqlspec.adapters.aiosqlite import AiosqliteConfig

from litestar_queues import (
    QueueConfig,
    QueueMaintenanceConfig,
    QueuePlugin,
    QueueService,
    WorkerConfig,
    task,
)
from litestar_queues.backends.sqlspec import SQLSpecBackendConfig


@task(
    "reports.render",
    queue="reports",
    retries=2,
    timeout=300,
    unique_by="arguments",
)
async def render_report(report_id: str) -> dict[str, str]:
    return {"report_id": report_id, "status": "rendered"}


@post("/reports/{report_id:str}/render")
async def enqueue_report(
    report_id: str,
    queue_service: NamedDependency[QueueService],
) -> dict[str, str]:
    result = await queue_service.enqueue(render_report, report_id)
    return {"task_id": str(result.id), "status": result.status or "queued"}


sqlspec_config = AiosqliteConfig(
    connection_config={"database": "queue.db"},
)
queue_config = QueueConfig(
    queue_backend=SQLSpecBackendConfig(sqlspec_config=sqlspec_config),
    execution_backend="local",
    worker=WorkerConfig(
        placement="external",
        max_concurrency=4,
        queues=("reports",),
    ),
    maintenance=QueueMaintenanceConfig(
        time_budget=300,
        coordination_timeout=360,
        stale_after=900,
        terminal_retention=30 * 24 * 60 * 60,
    ),
    task_modules=("app.tasks",),
    max_argument_identity_bytes=64 * 1024,
)

app = Litestar(
    route_handlers=[enqueue_report],
    plugins=[QueuePlugin(queue_config)],
)
```

```bash
LITESTAR_APP=app:app litestar queues run
LITESTAR_APP=app:app litestar queues run-maintenance --json
```

</example>

## References Index

- **[Backends, Worker Configuration, Events, and Maintenance](references/backends-and-events.md)** — `task_dependency_provider`, Dishka worker scope, `create_queue_config`, SQLSpec/Advanced Alchemy/Redis/Valkey backend setups, `QueueEventsConfig`, `ObservabilityConfig`, and `QueueMaintenanceConfig`.
- **[Execution Backends](references/execution-backends.md)** — local, immediate, Cloud Run, Cloud Tasks, Kafka, Pub/Sub, RabbitMQ, SQS, delivery fencing, and lost-delivery repair.
- **[Namespacing and Expiry](references/namespacing.md)** — `namespace=`, not-started deadlines and the `expired` state, event-stream configuration.

## Cross-References

- **[litestar](../litestar/SKILL.md)** — Litestar app setup, plugin lists, DI, and lifespan.
- **[litestar-autowire](../litestar-autowire/SKILL.md)** — Optional task discovery through Autowire integration.
- **[litestar-testing](../litestar-testing/SKILL.md)** — Application and handler tests.
- **[sqlspec](../sqlspec/SKILL.md)** — SQLSpec adapter and migration configuration.
- **[advanced-alchemy](../advanced-alchemy/SKILL.md)** — SQLAlchemy models, services, and Alembic ownership.

## Official References

- <https://github.com/cofin/litestar-queues>
- <https://pypi.org/project/litestar-queues/>

## Shared Styleguide Baseline

- [General Principles](../litestar-styleguide/references/general.md)
- [Python](../litestar-styleguide/references/python.md)
- [Litestar](../litestar-styleguide/references/litestar.md)
