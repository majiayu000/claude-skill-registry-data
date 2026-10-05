---
name: queues-and-jobs
description: Design and operate Laravel queues, jobs, workers, and Horizon with retry safety, idempotency, failure handling, tests, and production visibility.
tags:
  - laravel
  - php
---

# Queues And Jobs

Use queues for work that can happen outside the request cycle: notifications, imports, exports, media processing, integration callbacks, long-running calculations, and retryable external operations.

This is the canonical queue skill. It consolidates the former `queues-and-horizon` topic while keeping `horizon-metrics-and-dashboards` for focused observability work.

## Detect The Queue Stack

Confirm the queue connection, worker manager, Horizon installation, failed-job storage, deployment process, and local runner before changing configuration or issuing operational commands. Do not assume Horizon is installed merely because Redis is used.

## Job Design

Queued jobs should be safe to retry.

Prefer:

- passing IDs or small scalar payloads;
- reloading models in `handle()`;
- explicit `tries`, backoff, timeout, and failure behavior when the job is important;
- idempotency keys or state checks for external side effects;
- after-commit dispatch when jobs depend on committed records.

```php
final class ProcessRecord implements ShouldQueue
{
    public function __construct(public int $recordId)
    {
    }

    public function handle(): void
    {
        $record = Record::query()->findOrFail($this->recordId);

        if ($record->processed_at !== null) {
            return;
        }

        // Perform idempotent work.
    }
}
```

## Dispatching

Dispatch after commit when a queued job needs database writes to be visible.

```php
ProcessRecord::dispatch($record->id)->afterCommit();
```

## Failure Handling

Separate transient failures from permanent failures. Retry network and temporary provider issues; fail fast for invalid state or bad input.

Log failures with redacted context. Do not log secrets, tokens, signatures, full payloads, or unnecessary personal data.

## Horizon And Workers

Do not force Horizon on every project. Use Horizon or equivalent visibility when queue volume, failed jobs, throughput, or production support justifies it.

Worker configuration should account for:

- queue priorities;
- memory limits;
- timeouts;
- retry/backoff;
- graceful restarts;
- failed job storage.

When Horizon is installed:

- align supervisors with real queue names and priorities;
- keep worker timeout below the queue driver's retry-after window;
- balance processes based on workload behavior rather than one global queue;
- tag jobs with low-cardinality identifiers that help operators diagnose failures;
- protect the dashboard with production authorization;
- terminate or restart workers through the deployment lifecycle so new code is loaded safely.

Without Horizon, apply the same timeout, memory, retry, graceful-restart, and failed-job expectations to the selected process manager.

## Scheduling

Scheduled tasks should use overlap protection for long-running or non-reentrant work.

```php
Schedule::command('records:process')
    ->everyFiveMinutes()
    ->withoutOverlapping()
    ->onOneServer();
```

Keep scheduled commands testable independently from cron.

## Testing

Use `Queue::fake()` or `Bus::fake()` to assert dispatching. Test job behavior directly when the job contains meaningful logic.

Also verify retry/idempotency behavior, failure callbacks, batch or chain behavior when used, and after-commit dispatch for jobs that depend on newly written data. For operational changes, inspect the effective worker/Horizon configuration and perform a safe local smoke test when the required services are available.
