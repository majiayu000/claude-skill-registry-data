---
name: async-apex
description: "Use when selecting, designing, or reviewing Queueable, Batch, Future, or Schedulable Apex for callouts, large data processing, retries, or background work. Triggers: 'queueable vs batch', 'future method', 'flex queue', 'async job failed', 'schedule apex'. NOT for Platform Events or a deep-only Batch Apex implementation guide."
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
inputs:
  - "workload size and whether records can exceed one transaction"
  - "need for callouts, chaining, scheduling, or state across chunks"
  - "current entry point such as trigger, UI action, nightly job, or integration"
outputs:
  - "async mechanism recommendation"
  - "review findings for queueable, batch, future, or scheduler usage"
  - "migration guidance from legacy future methods"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-03-13
---

Use this skill when synchronous Apex is the wrong execution model or when an existing async design is brittle. The core job is to choose the smallest async mechanism that fits the workload, preserves observability, and does not create hidden limit or chaining failures.

## Before Starting

- How many records or payloads can this process handle at peak, not just in the happy-path demo?
- Does the work need outbound callouts, a scheduled start time, or multiple transactions with fresh limits?
- Do you need monitoring, retry visibility, or a job ID that operations can inspect later?

## Core Concepts

### Queueable Is The Default Modern Async Tool

For most application-level async work, start with `Queueable`. It supports complex member variables, gives you an `AsyncApexJob` record to monitor, and is usually the right replacement for legacy `@future` code. It is especially strong for "finish DML, then make a callout" patterns when combined with `Database.AllowsCallouts`.

### Batch Exists For Scale And Fresh Limits Per Scope

Use Batch Apex when the workload can exceed normal transaction limits or when you need to process very large data volumes in chunks. Each `execute()` scope gets fresh governor limits. That makes Batch the right tool for record sets that can grow beyond what one Queueable should reasonably hold. It is not the default choice for every background task because it adds more framework overhead and operational complexity.

### Future Is Legacy And Narrow

`@future` still exists, but it is intentionally constrained. Parameters must be primitive types or collections of primitives, and it offers weaker monitoring and composition than Queueable. Keep it for simple legacy code paths only when there is no need for chaining, non-primitive state, or richer operational visibility.

### Schedulable Starts Work; It Should Rarely Do All The Work

`Schedulable` is the timer, not usually the worker. A scheduler should dispatch a Queueable or Batch job instead of performing large business logic inline. This keeps recurring jobs maintainable and avoids turning cron logic into a second processing framework.

## Common Patterns

### Post-Commit Queueable For Callouts

**When to use:** A trigger or synchronous service must perform a callout after data is saved.

**How it works:** Collect record IDs in the original transaction, enqueue one Queueable, re-query inside the job, and implement `Database.AllowsCallouts` when HTTP work is required.

**Why not the alternative:** Doing the callout in-trigger or using `@future` by default makes monitoring, retry design, and composition worse.

### Batch For Large, Query-Driven Workloads

**When to use:** The record count may exceed one transaction or you need controlled chunking with `start`, `execute`, and `finish`.

**How it works:** Use `Database.getQueryLocator()` in `start()`, keep `execute()` idempotent, and summarize outcomes in `finish()`.

### Scheduler As Dispatcher

**When to use:** Work must begin on a cron schedule.

**How it works:** The `Schedulable.execute` method launches a Batch or Queueable and exits quickly, leaving the heavy lifting to the right async mechanism.

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Trigger must perform a callout after DML for tens or hundreds of records | Queueable + `Database.AllowsCallouts` | Clean post-commit boundary with monitoring and chaining support |
| Nightly cleanup or reprocessing may touch thousands to millions of rows | Batch Apex | Fresh limits per scope and native large-volume processing |
| Small legacy fire-and-forget method only needs primitive inputs | `@future` only if there is no reason to modernize | Supported, but weaker than Queueable |
| Work must start on a schedule | Schedulable launching Queueable or Batch | Separates timer concerns from worker concerns |


## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org edition, relevant objects, and current configuration state
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Core Concepts and Common Patterns sections above
4. Validate — run the skill's checker script and verify against the Review Checklist below
5. Document — record any deviations from standard patterns and update the template if needed

---

## Review Checklist

- [ ] The chosen async mechanism matches data volume and operational needs, not team habit.
- [ ] Queueable jobs are not enqueued inside loops.
- [ ] Queueables that make callouts implement `Database.AllowsCallouts`.
- [ ] Batch jobs use an idempotent `execute()` path and summarize failures in `finish()`.
- [ ] Legacy `@future` methods are justified instead of being the default.
- [ ] Schedulers dispatch work rather than containing heavy processing inline.

## Salesforce-Specific Gotchas

1. **`@future` parameters are constrained** — pass IDs or primitives, then re-query inside the async method.
2. **A running Queueable can only chain one child Queueable job** — fan-out designs need a different approach.
3. **Tests do not run async work until `Test.stopTest()`** — asserting before `stopTest()` produces false negatives.
4. **Batch `execute()` gets fresh limits, but that does not excuse non-idempotent logic** — retries or re-runs can still duplicate side effects if the code is not designed carefully.

## Output Artifacts

| Artifact | Description |
|---|---|
| Async decision matrix | Recommended use of Queueable, Batch, Future, or Schedulable for the current workload |
| Async review findings | Findings on callouts, chaining, monitoring, and bulk safety |
| Migration plan | Practical move from `@future` or overloaded schedulers to modern async patterns |

## Related Skills

- `apex/callouts-and-http-integrations` — use when the async question is really about outbound HTTP design, Named Credentials, or callout error handling.
- `apex/governor-limits` — use when the problem is transaction budgeting or loop-driven limit failures, not just async mechanism choice.
- `apex/test-class-standards` — use alongside this skill to validate Queueable, Batch, and scheduler behavior correctly in tests.
