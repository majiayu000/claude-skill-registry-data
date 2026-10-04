---
name: superpowers-sage:acorn-queues
description: >
  Background job processing in WordPress via Acorn: Laravel queue, dispatch,
  queue:work, ShouldQueue, failed jobs, Action Scheduler, as_schedule_single_action,
  as_schedule_recurring_action, job retries, backoff, job chaining, job batching,
  ShouldBeUnique, Acorn queue, Redis queue driver, database queue driver,
  queue worker, background tasks — using Acorn's Laravel queue stack in Sage/WordPress
user-invocable: false
---

# Queues, Jobs, and Background Tasks

## When to Use What

| Criteria | Action Scheduler | Laravel Queue + Job |
|---|---|---|
| **Best for** | Simple recurring tasks, WP-native workflows | Robust async, retry logic, heavy computation |
| **Infrastructure** | None — runs on WP cron | Needs queue driver (database or Redis) |
| **Retry/backoff** | Manual | Built-in (`$tries`, `$backoff`, exponential) |
| **Monitoring** | WP Admin > Tools > Scheduled Actions | `lando acorn queue:failed`, logs |
| **Examples** | Daily cleanups, content sync, email digests | Image processing, API syncs, bulk imports |
| **Already available** | Bundled with WooCommerce; standalone via `woocommerce/action-scheduler` | Requires Acorn queue config + worker |

**Rule of thumb:** Start with Action Scheduler for simple recurring WordPress tasks. Move to Laravel Queue + Job when you need retries, backoff, chaining, batching, or processing that could take more than a few seconds.

## Quick Start — Laravel Queue

```bash
# 1. Create a job class
bash skills/acorn-queues/scripts/create-job.sh ProcessImage

# 2. Create queue tables (database driver)
lando acorn queue:table
lando acorn queue:failed-table
lando acorn migrate

# 3. Set driver in .env
# QUEUE_CONNECTION=database

# 4. Start a worker
bash skills/acorn-queues/scripts/run-worker.sh
bash skills/acorn-queues/scripts/run-worker.sh emails
```

## Quick Start — Action Scheduler

```bash
# Install (if not using WooCommerce)
lando composer require woocommerce/action-scheduler
```

```php
// Schedule once
as_schedule_single_action(strtotime('+10 minutes'), 'app/sync_content', ['post_id' => 42], 'content-sync');

// Schedule recurring (guard against duplicates)
if (! as_has_scheduled_action('app/cleanup_tokens', [], 'maintenance')) {
    as_schedule_recurring_action(time(), HOUR_IN_SECONDS, 'app/cleanup_tokens', [], 'maintenance');
}
```

Register callbacks in `ThemeServiceProvider::boot()`:

```php
add_action('app/sync_content', function (int $postId): void {
    $this->app->make(\App\Services\ContentSyncService::class)->syncPost($postId);
});
```

## Job Class Anatomy

```php
class ProcessImage implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public int $tries = 3;
    public array $backoff = [10, 60, 300]; // exponential: 10s, 1min, 5min

    public function __construct(protected readonly int $attachmentId) {}

    public function handle(): void
    {
        // If job needs WP user context:
        // wp_set_current_user($this->userId);

        $file = get_attached_file($this->attachmentId);
        if (! $file || ! file_exists($file)) {
            return; // idempotent exit — attachment gone
        }
        // ... process
    }

    public function failed(?\Throwable $exception): void
    {
        Log::error('ProcessImage permanently failed', ['attachment_id' => $this->attachmentId]);
    }
}
```

## Dispatching Jobs

```php
// Basic
ProcessImage::dispatch(attachmentId: $id);

// Delayed (5 minutes)
SyncContent::dispatch(sourceId: $id)->delay(now()->addMinutes(5));

// Specific queue
SendEmail::dispatch(campaignId: $id)->onQueue('emails');

// From a WordPress hook
add_action('add_attachment', function (int $id): void {
    if (wp_attachment_is_image($id)) {
        ProcessImage::dispatch(attachmentId: $id);
    }
});
```

## Scripts

```bash
# Create a job class (validates PascalCase, checks lando on PATH)
bash skills/acorn-queues/scripts/create-job.sh <JobName>

# Run a queue worker (default queue, 3 tries, 60s backoff)
bash skills/acorn-queues/scripts/run-worker.sh
bash skills/acorn-queues/scripts/run-worker.sh emails
```

Script source: [`scripts/create-job.sh`](scripts/create-job.sh) · [`scripts/run-worker.sh`](scripts/run-worker.sh)

## Assets

Boilerplate templates with `{{CLASS_NAME}}` placeholder. Copy and replace.

- **[job-simple.php.tpl](assets/job-simple.php.tpl)** — Simple job with `handle()` + `failed()`, `$tries`, `$backoff`, `wp_set_current_user` stub.
- **[job-batched.php.tpl](assets/job-batched.php.tpl)** — Batched job with `use Batchable`, `$this->batch()->cancelled()` check.

## References

Deep content loaded on demand — zero tokens until needed.

- **[action-scheduler.md](references/action-scheduler.md)** — Action Scheduler setup, `as_schedule_single_action`, `as_schedule_recurring_action`, callbacks, duplicate-schedule prevention, cron-based queue trigger.
- **[laravel-queue.md](references/laravel-queue.md)** — Full `config/queue.php`, all drivers, database setup, dispatching patterns, job chaining, batching, testing with `Bus::fake()`.
- **[redis-driver.md](references/redis-driver.md)** — Redis-backed queue, Lando Redis service config (`REDIS_HOST=cache`), queue isolation, failover to database driver, Supervisor config.
- **[job-patterns.md](references/job-patterns.md)** — Idempotency patterns, chunking large datasets, retry/backoff config, `ShouldBeUnique` + `uniqueId()`, `wp_set_current_user` in jobs, pass IDs not objects.
- **[troubleshooting.md](references/troubleshooting.md)** — Failed jobs table, `queue:work` debug flags, common errors (jobs stuck, Redis refused, class not found, memory exhaustion), escalation paths.

## Verification

- Dispatch a test job and confirm it appears in the queue: check the `jobs` table (database driver) or `lando redis-cli -h cache LLEN queues:default` (Redis driver).
- Run `lando acorn queue:work --once` and confirm the job processes successfully with expected log output.
- After processing, verify the job is removed from the queue and does not appear in `lando acorn queue:failed`.

## Failure modes

### Problem: Jobs dispatched but never processed

- **Cause:** No worker is running, or `QUEUE_CONNECTION` in `.env` does not match a connection in `config/queue.php`.
- **Fix:** Start a worker (`bash skills/acorn-queues/scripts/run-worker.sh`). Verify `QUEUE_CONNECTION` matches a valid connection key. For the database driver, run `lando acorn queue:table && lando acorn migrate`.

### Problem: Jobs fail and the `failed_jobs` table does not exist

- **Cause:** The failed jobs migration was never run.
- **Fix:** `lando acorn queue:failed-table && lando acorn migrate`. Then retry with `lando acorn queue:retry all`.

For all other failure modes see [`references/troubleshooting.md`](references/troubleshooting.md).

## Critical Rules

1. **Action Scheduler vs Laravel Queue:** Use Action Scheduler for simple recurring WP-native tasks. Use Laravel Queue + Job when you need retries, backoff, chaining, batching, or heavy computation.
2. **`wp_set_current_user` in jobs:** If a job calls `current_user_can()` or any WP function that relies on the current user, call `wp_set_current_user($userId)` at the top of `handle()`. Jobs run outside the HTTP lifecycle — WP does not set a current user automatically.
3. **Idempotency:** Every job must be safe to run more than once. Use guard clauses or upsert patterns. See `references/job-patterns.md`.
4. **Pass IDs, not objects:** Pass `$postId` instead of `$post`. Re-fetch in `handle()` to avoid serialization issues and stale data on retry.
5. **Set `$tries` and `$backoff`:** Never let jobs retry infinitely. Use exponential backoff arrays for external API jobs.
6. **Failed jobs table must exist:** Run `lando acorn queue:failed-table && lando acorn migrate` before running workers in production.
7. **`sync` driver is for development only.** It blocks the HTTP request and runs jobs inline. Set `QUEUE_CONNECTION=database` or `redis` in production.
8. **Redis host inside Lando is the service name** (`cache`), not `127.0.0.1`. See `references/redis-driver.md`.
