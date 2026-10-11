---
name: apex-scheduled-jobs
description: "Scheduling Apex classes using the Schedulable interface: implementing execute(), cron expressions, System.schedule(), monitoring CronTrigger records, job limits, and job chaining patterns. NOT for Batch Apex scheduling (use batch-apex-patterns) or Flow scheduled paths."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Reliability
  - Operational Excellence
triggers:
  - how to run an Apex class on a schedule
  - schedule a daily batch job in Apex using Schedulable
  - cron expression for weekly Apex job
  - how do I abort or reschedule a scheduled Apex job
  - scheduled Apex job not running or failing silently
  - query active scheduled jobs in Salesforce org
tags:
  - schedulable
  - scheduled-apex
  - cron
  - system-schedule
  - async-apex
  - job-management
inputs:
  - "Apex class that needs to run on a time-based schedule (or the business requirement for one)"
  - "Desired schedule frequency, time of day, and day-of-week or day-of-month targeting"
  - "Whether the job will dispatch Batch Apex, Queueable, or perform work inline"
  - "Current org scheduled job count if approaching the 100-job limit"
outputs:
  - "Schedulable Apex class implementation with correct interface and execute() signature"
  - "Valid cron expression for the target schedule"
  - "System.schedule() call for initial deployment or post-deployment manual scheduling"
  - "CronTrigger SOQL query for monitoring and audit"
  - "Guidance on abort-and-reschedule pattern, deployment considerations, and testing approach"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-04
---

# Apex Scheduled Jobs

Use this skill when designing, implementing, reviewing, or troubleshooting Apex classes that run on a time-based schedule using the `Schedulable` interface. The skill covers the full lifecycle: authoring, scheduling via cron expression, monitoring via `CronTrigger`, aborting, rescheduling, testing, and deployment considerations.

---

## Before Starting

Gather this context before working in this domain:

- **What is the scheduling target?** Schedulable should act as the timer and dispatcher, not the data processor. Large-volume work belongs in Batch Apex or a Queueable dispatched from `execute()`.
- **What is the org's current scheduled job count?** The platform limit is 100 scheduled jobs per org (shared across all types). Approaching this limit requires an audit before adding new jobs.
- **Does the job need callouts?** Scheduled Apex cannot make callouts directly. Callouts must be delegated to a `@future(callout=true)` method or a `Queueable` implementing `Database.AllowsCallouts`.
- **Who will own the schedule post-deployment?** Scheduled jobs are not deployed by the Metadata API. They must be created manually or via Anonymous Apex after deployment — plan for this in every release.
- **Is this a sandbox refresh scenario?** Scheduled jobs from production are not copied to a sandbox on refresh. Post-refresh scheduling must be scripted or run manually.

---

## Core Concepts

### The Schedulable Interface

A class becomes schedulable by implementing the `Schedulable` interface and defining a single `global void execute(SchedulableContext SC)` method. The `global` access modifier is required; `public` alone is insufficient.

```apex
global class MyScheduledJob implements Schedulable {
    global void execute(SchedulableContext SC) {
        // Dispatch work here — avoid heavy logic inline
    }
}
```

The `SchedulableContext` object provides `getTriggerId()`, which returns the `CronTrigger` record ID for the active job. This ID can be used inside `execute()` for self-identification or logging, but it cannot be used to modify or abort the job from within the same execution.

### Cron Expressions

Salesforce uses a seven-field cron expression:

```
Seconds  Minutes  Hours  Day_of_month  Month  Day_of_week  [Year]
```

Key rules:
- Day_of_month and Day_of_week are mutually exclusive — one must always be `?`.
- Seconds must be `0` — sub-minute scheduling is not supported.
- Field values are 0-indexed for seconds/minutes/hours; months and days of week use named constants or 1-based integers.

Common patterns:

| Schedule | Cron Expression | Notes |
|---|---|---|
| Daily at 2:00 AM | `'0 0 2 * * ?'` | Runs every day |
| Weekdays at 1:00 PM | `'0 0 13 ? * MON-FRI'` | Day_of_month is `?` |
| First day of each month at midnight | `'0 0 0 1 * ?'` | Day_of_week is `?` |
| Every Sunday at 3:30 AM | `'0 30 3 ? * SUN'` | Day_of_month is `?` |
| Hourly (not recommended) | `'0 0 * * * ?'` | Consumes scheduled job slot continuously |

Always schedule during off-peak hours to reduce contention with user traffic and other async jobs.

### System.schedule() and the CronTrigger Object

A scheduled job is created with:

```apex
String jobId = System.schedule('Job Display Name', cronExpression, new MyScheduledJob());
```

- The first argument is the display name shown in Setup > Scheduled Jobs. It must be unique per org — duplicate names throw a `System.AsyncException` at runtime.
- The method returns a `CronTrigger` record ID (not an `AsyncApexJob` ID).
- Jobs can be scheduled from Anonymous Apex, a trigger, a controller, or another Apex class — but **not** from within a Schedulable's own `execute()` method to reschedule itself (use a separate post-execute mechanism if rescheduling is needed).

Monitor active jobs with:

```soql
SELECT Id, CronJobDetail.Name, CronExpression, State, NextFireTime, PreviousFireTime
FROM CronTrigger
WHERE State = 'WAITING'
ORDER BY NextFireTime ASC
```

`CronTrigger.State` values: `WAITING`, `PAUSED`, `COMPLETE`, `ERROR`, `DELETED`, `BLOCKED`.

Abort a scheduled job with:

```apex
System.abortJob('CronTrigger_Id_Here');
```

### Mode Selection

This skill operates in three modes based on the practitioner's need:

- **Mode 1 — Implement:** Design and create a new scheduled job from scratch. Follow the Schedulable-as-dispatcher pattern and produce both the class and the scheduling call.
- **Mode 2 — Review/Audit:** Evaluate existing scheduled jobs in an org — query `CronTrigger`, check proximity to the 100-job limit, verify off-peak scheduling, and confirm that heavy work is delegated rather than inlined.
- **Mode 3 — Troubleshoot:** Diagnose a job that is not running, stuck in `BLOCKED` or `ERROR` state, or failing silently. Start with `CronTrigger.State`, then check `AsyncApexJob` for the most recent execution record.

---

## Common Patterns

### Schedulable as Dispatcher (Preferred Pattern)

**When to use:** Any case where the scheduled job processes records, performs DML, or does anything beyond trivial computation. This is the default pattern.

**How it works:**
1. The `Schedulable` class holds minimal state — typically a constructor parameter for scoping (e.g., record type, org-specific flag).
2. `execute()` instantiates and dispatches a Batch Apex class or enqueues a Queueable. It does not perform DML or SOQL at scale itself.
3. The Batch or Queueable carries all governor-intensive work within its own transaction limits.

```apex
global class NightlyLeadCleanupScheduler implements Schedulable {
    global void execute(SchedulableContext SC) {
        Database.executeBatch(new LeadCleanupBatch(), 200);
    }
}
```

**Why not the alternative:** Performing large SOQL queries or DML directly in `execute()` burns the Schedulable's governor limits (which are the same full limits as any Apex transaction). If the data volume grows, the job silently fails at governor limit boundaries with no automatic retry.

### Self-Identifying Job for Conditional Logic

**When to use:** A single Schedulable class is reused for multiple schedules with different parameters, and the job needs to know which schedule triggered it.

**How it works:**
1. The `SchedulableContext.getTriggerId()` returns the `CronTrigger.Id`.
2. Query `CronJobDetail` from `CronTrigger` to retrieve the job name and branch logic accordingly.

```apex
global class MultiPurposeScheduler implements Schedulable {
    global void execute(SchedulableContext SC) {
        CronTrigger ct = [
            SELECT CronJobDetail.Name
            FROM CronTrigger
            WHERE Id = :SC.getTriggerId()
        ];
        if (ct.CronJobDetail.Name.contains('Nightly')) {
            Database.executeBatch(new NightlyBatch(), 200);
        } else {
            System.enqueueJob(new WeeklyReportQueueable());
        }
    }
}
```

**Why not the alternative:** Creating one Schedulable class per variation leads to class sprawl. A parameterized or self-identifying class reduces maintenance surface.

### Abort-and-Reschedule for Schedule Changes

**When to use:** The cron schedule for a live job needs to change. There is no in-place modification API.

**How it works:**
1. Query `CronTrigger` to find the job ID by name.
2. Call `System.abortJob(jobId)`.
3. Call `System.schedule(sameName, newCronExpression, new MyScheduledJob())`.

```apex
// Run from Anonymous Apex or a deployment script
List<CronTrigger> jobs = [
    SELECT Id FROM CronTrigger
    WHERE CronJobDetail.Name = 'Nightly Lead Cleanup'
    AND State = 'WAITING'
];
if (!jobs.isEmpty()) {
    System.abortJob(jobs[0].Id);
}
System.schedule('Nightly Lead Cleanup', '0 0 3 * * ?', new NightlyLeadCleanupScheduler());
```

**Why not the alternative:** Attempting to update `CronExpression` directly on the `CronTrigger` record via DML is not supported. The only path to change a schedule is abort and reschedule.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Need to run Apex on a fixed time-based schedule | `Schedulable` + `System.schedule()` | Purpose-built platform feature for time-based Apex |
| Job processes large record volumes | Schedulable dispatches Batch Apex | Batch provides chunked limits and automatic retry |
| Job needs to make outbound callouts | Schedulable enqueues a `Queueable` with `AllowsCallouts` | Direct callouts from Scheduled Apex are not supported |
| Job schedule needs to change post-deployment | Abort existing job, schedule new one with updated cron | No in-place schedule modification API exists |
| Org is near the 100-job limit | Consolidate into a master scheduler class | Single scheduled job dispatches multiple logical tasks |
| Job runs in multiple sandboxes or prod | Plan post-deployment Anonymous Apex script | Scheduled jobs are not Metadata API-deployable |
| Need sub-hourly scheduling | Re-evaluate: consider Platform Events or streaming | Salesforce does not support sub-minute scheduling |
| Job errors silently and stops | Query `CronTrigger.State = 'ERROR'`, check `AsyncApexJob` | State field and job history show failure details |

---


## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org edition, relevant objects, and current configuration state
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Core Concepts and Common Patterns sections above
4. Validate — run the skill's checker script and verify against the Review Checklist below
5. Document — record any deviations from standard patterns and update the template if needed

---

## Review Checklist

Run through these before marking scheduled job work complete:

- [ ] Class declares `global` (not `public`) access and implements `Schedulable`.
- [ ] `execute(SchedulableContext SC)` signature is correct — method is `global void`.
- [ ] Heavy work (SOQL at scale, DML at scale) is delegated to Batch or Queueable, not done inline.
- [ ] Cron expression is valid: seconds field is `0`, Day_of_month and Day_of_week are mutually exclusive (`?`).
- [ ] Job name is unique in the org — duplicate names cause a runtime `AsyncException`.
- [ ] Job is scheduled during off-peak hours.
- [ ] Org is below 100 scheduled jobs — if close, a consolidation plan exists.
- [ ] No direct callouts in `execute()` — callouts are delegated to async contexts.
- [ ] Post-deployment scheduling script (Anonymous Apex) is prepared and documented.
- [ ] Test class uses `Test.startTest()` / `Test.stopTest()` and verifies `CronTrigger` state after scheduling.
- [ ] Sandbox refresh impact is understood and post-refresh scheduling is scripted.

---

## Salesforce-Specific Gotchas

1. **Scheduled jobs are not deployed by the Metadata API** — The Schedulable class deploys, but the active job record in `CronTrigger` does not. Every release that changes or introduces a scheduled job requires a post-deployment step (Anonymous Apex or a post-install script) to create or recreate the schedule.

2. **The 100-job limit is org-wide and shared** — All scheduled Apex jobs, scheduled flows, and scheduled reports count against the same 100-job org limit. Orgs with many automations can exhaust this silently; new `System.schedule()` calls throw a `System.AsyncException` when the limit is reached.

3. **Direct callouts from `execute()` are blocked at runtime** — A Schedulable that attempts an HTTP callout throws `System.CalloutException: Callout from scheduled Apex not supported`. This must be delegated to a `@future(callout=true)` or Queueable with `AllowsCallouts`.

4. **You cannot reschedule a job from within its own `execute()` method** — Calling `System.schedule()` inside `execute()` throws a runtime exception. If a job needs to compute its next run time dynamically, use a Queueable dispatched from `execute()` to do the rescheduling.

5. **Sandbox refreshes clear all scheduled jobs** — Scheduled jobs from production are not carried to a refreshed sandbox. Teams that rely on scheduled jobs in sandboxes for testing or integration must re-create them after each refresh.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Schedulable class implementation | Correctly structured class with `global` modifier and `execute(SchedulableContext SC)` |
| Cron expression | Validated expression matching the target schedule with Day_of_month / Day_of_week handling |
| System.schedule() call | Ready-to-run statement for Anonymous Apex or post-deployment script |
| CronTrigger monitoring query | SOQL to surface active jobs, state, and next fire time |
| Abort-and-reschedule script | Anonymous Apex pattern to change an existing job's schedule |
| Test class scaffold | Unit test with `Test.startTest()` / `Test.stopTest()` and CronTrigger assertion |

---

## Related Skills

- `apex/async-apex` — use when the question is which async mechanism to choose (Schedulable vs Queueable vs Batch vs future).
- `apex/batch-apex-patterns` — use when the scheduled job needs to process large data volumes with chunked limits.
- `apex/apex-queueable-patterns` — use when the scheduled job needs to make callouts or chain async steps.
- `apex/governor-limits` — use when the scheduled job is hitting CPU, SOQL, or DML limits during execution.
- `apex/debug-and-logging` — use when diagnosing why a scheduled job failed or produced unexpected results.
