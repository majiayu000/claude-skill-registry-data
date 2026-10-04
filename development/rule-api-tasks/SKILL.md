---
name: rule-api-tasks
description: MANDATORY when editing files matching ["api/src/task/**/*.py"]. When working on background tasks in api/src/task/
---

# API Background Tasks Rules

## Task Base Class

ALWAYS inherit from the `Task` base class in `api/src/task/task.py`. NEVER create standalone task functions outside the Task framework. ALWAYS implement the `run_task()` method as the entry point for task logic.

Example from codebase:
```python
# From api/src/task/notifications/closing_date_notification.py
from src.task.task import Task

class ClosingDateNotificationTask(Task):
    class Metrics(StrEnum):
        NOTIFICATIONS_SENT = "notifications_sent"
        OPPORTUNITIES_PROCESSED = "opportunities_processed"

    def run_task(self) -> None:
        # Task logic here
        ...
```

## Metrics Definition

ALWAYS define a `Metrics` class as a `StrEnum` inside the task class. Metrics are auto-initialized to 0. ALWAYS use `self.increment(Metrics.METRIC_NAME)` to update metrics. NEVER use raw counters or external metric tracking.

Example from codebase:
```python
class TransformOracleDataTask(Task):
    class Metrics(StrEnum):
        RECORDS_PROCESSED = "records_processed"
        RECORDS_FAILED = "records_failed"
        BATCHES_COMPLETED = "batches_completed"

    def run_task(self) -> None:
        ...
        self.increment(self.Metrics.RECORDS_PROCESSED)
```

## SubTask Composition

ALWAYS use the `SubTask` base class for batch processing operations. ALWAYS implement `has_more_to_process()` to control the batch loop. NEVER process unbounded data sets in a single pass.

Example from codebase:
```python
# From api/src/task/task.py / subtask pattern
class MySubTask(SubTask):
    def has_more_to_process(self) -> bool:
        return self.current_batch < self.total_batches

    def run_task(self) -> None:
        while self.has_more_to_process():
            batch = self.get_next_batch()
            self.process_batch(batch)
            self.increment(self.Metrics.BATCHES_COMPLETED)
```

## Job Logging

ALWAYS use the `JobLog` database model to track task execution status. Task status transitions: `STARTED` -> `COMPLETED` or `STARTED` -> `FAILED`. ALWAYS update job status in a `finally` block to ensure status is recorded even on failure.

Example from codebase:
```python
def run_task(self) -> None:
    job = JobLog(status=JobStatus.STARTED, task_name=self.__class__.__name__)
    try:
        self._execute_task_logic()
        job.status = JobStatus.COMPLETED
    except Exception:
        job.status = JobStatus.FAILED
        raise
    finally:
        self.db_session.add(job)
```

## Performance Measurement

ALWAYS use `time.perf_counter()` for timing task execution. NEVER use `time.time()` for performance measurement. ALWAYS log task duration in structured logging `extra={}`.

Example from codebase:
```python
import time

def run_task(self) -> None:
    start = time.perf_counter()
    self._process_records()
    duration = time.perf_counter() - start
    logger.info(
        "Task completed",
        extra={"task_name": self.__class__.__name__, "duration_seconds": duration},
    )
```

## Notification Tasks

ALWAYS inherit from `BaseNotificationTask` for email notification tasks. ALWAYS use the Pinpoint adapter for email sending. NEVER call external email services directly from task code.

Example from codebase:
```python
# From api/src/task/notifications/base_notification.py pattern
class ClosingDateNotificationTask(BaseNotificationTask):
    def get_recipients(self) -> list[str]:
        ...

    def build_email_content(self) -> EmailContent:
        ...

    def run_task(self) -> None:
        recipients = self.get_recipients()
        content = self.build_email_content()
        self.send_notification(recipients, content)
```

## ECS Background Task Decorator

ALWAYS use the `ecs_background_task` decorator for tasks that run as ECS containers. This decorator handles NewRelic transaction setup and container lifecycle management.

## Logging

ALWAYS begin every task module with `logger = logging.getLogger(__name__)`. ALWAYS use static log message strings with `extra={}` for dynamic values. NEVER log PII. ALWAYS log task start, completion, and failure events.

Example from codebase:
```python
import logging
logger = logging.getLogger(__name__)

logger.info(
    "Processing SAM extract batch",
    extra={"batch_number": batch_num, "records_in_batch": len(records)},
)
```

## Error Handling

ALWAYS let exceptions propagate to the Task base class — it handles status updates and logging. NEVER swallow exceptions silently. ALWAYS use specific exception types, not bare `except Exception`.

---

## Context Enrichment

When generating significant task code (new task class, complex batch processing, notification logic), enrich your context:
- Call `get_architecture_section("api")` from the `simpler-grants-context` MCP server to understand task architecture
- Call `get_rule_detail("api-services")` for service layer patterns that tasks call
- Call `get_rule_detail("api-database")` for database session management in tasks
- Call `get_rule_detail("cross-domain")` for structured logging conventions
- Consult **Compound Knowledge** for indexed documentation on task patterns

## Related Rules

When working on background tasks, also consult these related rules:
- **`api-services.mdc`** — service functions that tasks orchestrate
- **`api-adapters.mdc`** — external service adapters that tasks use (S3, SQS, Pinpoint)
- **`api-database.mdc`** — database query patterns and session management
- **`api-error-handling.mdc`** — error handling patterns
- **`cross-domain.mdc`** — structured logging, factory patterns

## Specialist Validation

When generating or significantly modifying task code:

**For simple changes (< 20 lines, metrics update, logging change):**
No specialist invocation needed — the directives in this rule file are sufficient.

**For moderate changes (new task class, new SubTask):**
Invoke `codebase-conventions-reviewer` to validate against project conventions.

**For complex changes (new task framework extension, cross-task orchestration, notification pipelines):**
Invoke the following specialists (run in parallel where possible):
- `architecture-strategist` — validate task boundaries and separation of concerns
- `performance-oracle` — check for unbounded processing, missing batch limits
- `kieran-python-reviewer` — Python-specific quality review
