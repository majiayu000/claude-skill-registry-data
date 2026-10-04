---
name: async-apex
description: "Use when selecting, designing, or reviewing Queueable, Batch, Future, or Schedulable Apex for callouts, large data processing, retries, or background work. Triggers: 'queueable vs batch', 'future method', 'flex queue', 'async job failed', 'schedule apex', 'move a callout out of a trigger', 'run Apex in the background'. NOT for Batchable structure or scope sizing — use apex/batch-apex-patterns. NOT for Queueable chaining — use apex/apex-queueable-patterns."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Scalability
  - Performance
  - Reliability
tags:
  - async-apex
  - queueable
  - batch-apex
  - future-method
  - schedulable
triggers:
  - "should this be queueable or batch apex"
  - "future method needs to do a callout after trigger"
  - "async job failed and I need to debug it"
  - "how do I chain queueable jobs safely"
  - "when should I use schedulable apex"
  - "move an HTTP callout out of a trigger into a background job"
  - "replace our future methods with queueable apex"
inputs:
  - "workload size and whether records can exceed one transaction"
  - "need for callouts, chaining, scheduling, or state across chunks"
  - "current entry point such as trigger, UI action, nightly job, or integration"
outputs:
  - "async mechanism recommendation"
  - "review findings for queueable, batch, future, or scheduler usage"
  - "migration guidance from legacy future methods"
dependencies: []
version: 1.0.1
author: Pranav Nagrecha
updated: 2026-10-03
---

Use this skill when synchronous Apex is the wrong execution model or when an existing async design is brittle. The job is to choose the smallest async mechanism that fits the workload, keeps it observable, and stays inside the per-transaction and org-wide async limits.

## Before Starting

- How many records or payloads can this process handle at peak, not just in the happy-path demo?
- Does the work need outbound callouts, a scheduled start time, or many transactions with fresh limits?
- Do operations need a job ID to monitor (`AsyncApexJob`) and a recovery path when a job fails?
- What else in the org consumes async executions? The daily limit is shared by Batch, Queueable, scheduled Apex, and future methods.

## Questions to Ask Before Configuring

| Question | Why it matters | What a good answer adds | What proper configuration adds over just doing it |
|---|---|---|---|
| "How many records at peak, and does one transaction's 50,000-row query limit cover them?" | Queueable and future jobs share the 50,000-row SOQL limit; Batch `QueryLocator` returns up to 50 million rows | Queueable for bounded work, Batch (or Cursors with chained Queueables) for unbounded work | A job sized for the real volume, not the demo |
| "What starts the work: a trigger, a UI action, a schedule, or another job?" | You can enqueue 50 Queueables in a synchronous transaction but only 1 from an async one, and future methods are not allowed from Batch or future contexts | The entry point and the matching enqueue pattern | No `LimitException` the first time the job is called from a batch |
| "Does the work make callouts?" | Queueables need `Database.AllowsCallouts`; synchronous callouts aren't supported from scheduled Apex | The callout-capable worker class the scheduler or trigger hands off to | Callouts that run where the platform allows them |
| "What happens if the job fails halfway?" | A rolled-back transaction discards the Queueables it enqueued, and Batch scopes are separate transactions | A Transaction Finalizer, idempotent `execute`, or a retry design | Failures that are visible and recoverable |
| "How many jobs will run at once?" | Only 5 batch jobs are active; the flex queue holds 100, and `Database.executeBatch` throws `LimitException` when it is full | A cap or a single dispatcher instead of one batch per event | No dropped jobs during busy periods |
| "Who owns the schedule after a sandbox refresh or deployment?" | Scheduled jobs aren't copied on refresh, and deploying a scheduled class fails while jobs are pending | A runbook to delete, deploy, and reschedule | Releases that do not stall on CronTrigger errors |

What a proper design adds over "just make it async": the job runs in the right mechanism for its volume and entry point, its failures are observable, and it does not starve the rest of the org's async capacity.

## Core Concepts

### Choosing the mechanism

| Mechanism | Use it for | Key limits (Apex Developer Guide 262) |
|---|---|---|
| Queueable | Default background work, callouts after DML, non-primitive state, chaining | 50 enqueues per synchronous transaction, 1 per async transaction; one child per executing job; chain depth unlimited except 5 in Developer and Trial orgs |
| Batch Apex | Large, query-driven volumes with fresh limits per scope | `QueryLocator` up to 50 million rows; scope up to 2,000 with a `QueryLocator` (default 200); 5 active jobs; flex queue of 100; one `start` at a time |
| Scheduled Apex | A timer that dispatches a Queueable or Batch | 100 scheduled jobs; synchronous limits apply; no synchronous callouts |
| Future method | Narrow legacy use, mixed-DML isolation | Static, void, primitive parameters only; 50 per synchronous invocation, 0 in batch and future contexts, 50 in queueable context; no guaranteed order |
| Apex Cursors with chained Queueables | Large volumes without competing for the 5 batch slots | 50 million cursor rows per transaction; 10,000 cursors per day |

Salesforce recommends Queueable over future methods: same use cases plus job IDs, non-primitive types, and chaining.

### Org-wide async capacity

Asynchronous Apex method executions are limited to 250,000 per 24 hours or 200 per applicable user license, whichever is greater, shared across Batch, Queueable, scheduled Apex, and future methods. Batch checks the required capacity when `Database.executeBatch` is called and the `start` method has returned its workload, and won't start without enough capacity.

### Testing

Async work queued after `Test.startTest()` runs synchronously at `Test.stopTest()`. A batch test can exercise only one `execute`, so size test data to one scope.

## Common Patterns

### Post-commit Queueable for callouts

Collect IDs in the trigger, enqueue one Queueable that implements `Database.AllowsCallouts`, re-query inside `execute`, and throw on a failed response so the `AsyncApexJob` records it; add a Transaction Finalizer (`apex/apex-transaction-finalizers`) when the job needs automatic recovery. Full class and tests in `references/code-examples.md`.

### Batch for large, query-driven work

`Database.getQueryLocator()` in `start`, an idempotent `execute` with partial-success DML, and a summary in `finish`. Use `Database.Stateful` only for instance variables you need across scopes.

### Scheduler as dispatcher

`Schedulable.execute` calls `Database.executeBatch` or `System.enqueueJob` and returns. Mark member variables `transient` if they must not persist between runs.

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Trigger must call out after DML for a few hundred records | One Queueable with `Database.AllowsCallouts` | Post-commit, monitorable, callout-capable |
| Nightly work over millions of rows | Batch Apex dispatched by a scheduler | Fresh limits per scope, 50 million row locator |
| Many independent large jobs competing for batch slots | Apex Cursors with chained Queueables | Avoids the 5-active and 100-flex-queue limits |
| Callout needed from a schedule | Scheduler enqueues a Queueable or a callout-enabled batch | Synchronous callouts aren't supported from scheduled Apex |
| Need to fan out from a Batch `execute` | Enqueue one Queueable per execute | Async contexts allow one enqueue and zero future calls |
| Legacy future method needs sObject input | Convert to Queueable | Future parameters must be primitives |
| Prevent duplicate jobs for the same record | `AsyncOptions` with a `QueueableDuplicateSignature` | Duplicate enqueue throws `DuplicateMessageException` |

## Recommended Workflow

1. **Size and source the work.** Peak records, entry point (trigger, UI, schedule, job), callouts, and failure tolerance.
2. **Pick the mechanism** from the table above; check the entry point's enqueue and future limits.
3. **Build the worker.** Queueable or Batch with IDs re-queried inside, partial-success DML, and callout support where needed; start from `references/code-examples.md`.
4. **Add recovery.** A Transaction Finalizer for Queueables, idempotent Batch scopes, and a logged summary in `finish`.
5. **Test with `Test.startTest()` and `Test.stopTest()`.** One batch scope's worth of data; `HttpCalloutMock` for callouts (`templates/apex/tests/MockHttpResponseGenerator.cls`).
6. **Scan and deploy.** Run `python3 scripts/check_async_apex.py --manifest-dir force-app/main/default`; delete pending scheduled jobs before deploying a scheduled class, then reschedule.

## Review Checklist

- [ ] Mechanism matches peak volume and entry point
- [ ] No `System.enqueueJob` or `Database.executeBatch` inside a loop
- [ ] Queueables that call out implement `Database.AllowsCallouts`
- [ ] No future calls from Batch or future contexts
- [ ] Schedulers dispatch work and make no synchronous callouts
- [ ] Batch `execute` is idempotent; `finish` records the outcome
- [ ] Failure handling exists (Finalizer, retry, or alert)
- [ ] Tests wrap async calls in `Test.startTest()` and `Test.stopTest()`

## Salesforce-Specific Gotchas

See `references/gotchas.md`. The two that surprise teams most: scheduled Apex runs with synchronous limits, and a rolled-back transaction silently discards the Queueables it enqueued.

## Output Artifacts

| Artifact | Description |
|---|---|
| Async decision matrix | Queueable, Batch, Future, Scheduled, or Cursors for the workload |
| Worker classes and tests | Deployable Queueable or Batch with tests and package.xml |
| Async review findings | Callouts, chaining, limits, monitoring, and bulk safety |
| Migration plan | Moving future methods and heavy schedulers to Queueable or Batch |

## Related Skills

- `apex/batch-apex-patterns`: Batchable structure and scope sizing
- `apex/apex-queueable-patterns`: Queueable chaining in depth
- `apex/apex-transaction-finalizers`: Finalizer-based recovery for Queueables
- `apex/apex-scheduled-jobs`: cron expressions and scheduled job management
- `apex/callouts-and-http-integrations`: outbound HTTP design, Named Credentials, callout errors
- `apex/governor-limits`: transaction budgeting and loop-driven limit failures
- `apex/test-class-standards`: testing Queueable, Batch, and scheduler behavior
