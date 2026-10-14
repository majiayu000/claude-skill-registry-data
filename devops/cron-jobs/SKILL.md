---
name: cron-jobs
description: Scheduled jobs on PaaS and in the cloud — cron syntax, reliability, and observability — vendor-neutral patterns.
category: railway
---

## Overview

Scheduled work — nightly reports, data syncs, cleanup tasks, reminder emails —
runs on cron-like schedulers everywhere: platform cron add-ons, Kubernetes
CronJobs, or managed schedulers. The hard parts aren't the schedule syntax;
they're reliability (exactly-once-ish semantics, failure handling) and
observability (did it run? did it succeed?). This skill covers both.

## When to use

- Setting up recurring jobs (reports, syncs, cleanups, digests)
- Choosing between in-app schedulers and platform cron
- Making jobs idempotent and safe to retry
- Monitoring job execution (success, duration, missed runs)
- Debugging overlapping runs and timezone bugs

## Core concepts

**Cron syntax, precisely.** `* * * * *` = minute hour day-of-month month
day-of-week. `0 9 * * 1-5` = 9am weekdays. Ranges, steps (`*/15`), and lists
(`1,15`) compose freely. The classic traps: day-of-month AND day-of-week
(OR semantics in most crons — `0 0 1 * 1` runs on the 1st AND every Monday),
and everything in UTC unless configured otherwise.

**Idempotency is mandatory.** Jobs get retried, run twice after deploys, and
overlap. Design every job to be safely re-runnable: upsert instead of insert,
dedupe on natural keys, guard with "already processed" markers. A job that
double-charges or double-sends on retry is a bug, not bad luck.

**Overlap protection.** Long jobs + short schedules = concurrent runs
corrupting shared state. Use distributed locks (DB advisory lock, Redis
`SET NX`), or configure the scheduler's concurrency policy (forbid/allow/
replace). Decide per job: skip-if-running is usually right for periodic syncs.

**Timeouts and deadlines.** Every job needs a max runtime; a hung job holding
a lock blocks all future runs. Set timeouts at the scheduler and in code,
and alert on jobs exceeding their p99 duration significantly.

**Observability: the dead man's switch.** A job that fails loudly is fine; a
job that silently stops running is dangerous. Monitor three things: did it
start (schedule drift/missed runs), did it succeed (exit code/result), and
how long did it take (duration anomalies). Heartbeat/dead-man alerts catch
the "cron daemon died" class of failures.

## Practical workflow

1. **Define the job contract:** what it does, its schedule (in UTC, stated
   explicitly), expected duration, and its idempotency mechanism.
2. **Implement defensively:** acquire lock → check preconditions → do work in
   batches with progress → release lock; log start/finish/duration/rows-
   processed as structured events.
3. **Configure the schedule** on the platform (cron add-on, K8s CronJob,
   managed scheduler); set timezone explicitly to UTC and convert in docs.
4. **Add monitoring:** success/failure alerting, duration tracking, and a
   dead-man's-switch check for "hasn't succeeded in N periods".
5. **Test the failure modes:** kill it mid-run (does the next run recover?),
   run it twice concurrently (does the lock hold?), backfill a missed window
   (does it catch up correctly or skip safely?).
6. **Document runbooks:** what the job does, where logs live, how to run it
   manually, and how to disable it in an emergency.

## Common pitfalls

- **Timezone bugs** — "9am" in the developer's timezone vs UTC; daylight
  saving shifts; always schedule in UTC and document the mapping.
- **Non-idempotent jobs** — duplicate emails, double billing, repeated
  side effects on retry; make re-runs safe by construction.
- **Silent death** — scheduler misconfigured, job deleted, credentials
  expired; without dead-man alerting nobody notices for weeks.
- **Overlapping runs** — no locking + variable duration = corruption;
  choose a concurrency policy per job.
- **Jobs as hidden infrastructure** — cron entries living only in one
  person's head or a forgotten server; define jobs as code, in version
  control, with owners.
- **No manual-run path** — when the job needs an ad-hoc run (backfill,
  incident), "just wait for the schedule" isn't acceptable; make manual
  triggers first-class.
