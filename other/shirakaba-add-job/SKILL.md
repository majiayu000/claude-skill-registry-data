---
name: shirakaba-add-job
description: Add a background job or a scheduled task to a Shirakaba application - the job DTO, an idempotent handler, pushing it in the writing transaction, workers, the schedule and tests. Use when asked to move work out of a request, send mail or webhooks, or run something periodically in a project that uses shirakaba/queue.
---

# Add a background job to a Shirakaba application

Read `vendor/shirakaba/docs/guide/14-background-jobs.md` and `vendor/shirakaba/docs/design/10-background-work.md` first.

1. **Job DTO.** A `#[JsonDto]` `final readonly` class holding IDs and small values, not
   entities or services: it is stored as JSON.
2. **Handler.** Register it with a stable name, so renaming the class does not orphan
   waiting jobs: `$jobs->handle(SendWelcome::class, $handler, name: 'mail.welcome')`. The
   handler receives the job and a `RequestScope`; lease database access from that scope.
3. **Make it idempotent.** Delivery is at least once: record a unique key of the work done
   (an insert with `onConflict`) and return early when it exists.
4. **Push it in the transaction** that writes the data it depends on:
   `$db->transaction(fn (Writer $db) => ... $jobs->push(new SendWelcome($user->id), $db))`.
   Use `PushOptions` for the queue, a delay or a unique key.
5. **Recurring work.** Add a task to the `Schedule` with a cron expression and a stable name;
   make sure `CreateScheduleTable` is migrated and cron runs `app schedule:run` every minute.
6. **Test.** With `InMemoryQueue`, assert `pendingTypes()` after the request; run jobs with
   `JobRunner::runPending()` and assert their effect, including running one twice. For a
   schedule, call `$schedule->run($writer, $frozenClock)` and advance the clock.

## Verify

- `vendor/bin/phpstan analyse`
- the test suite, including the twice-run (idempotency) test
- `app queue:work --stop-when-empty` processes a pushed job locally; `app schedule:list`
  shows the next run of a scheduled task
