---
name: batch-apex-patterns
description: "Use when designing, reviewing, or debugging Batch Apex contracts, scope sizing, stateful behavior, chaining, and AsyncApexJob monitoring. Triggers: 'Database.Batchable', 'Database.Stateful', 'executeBatch', 'batch scope', 'AsyncApexJob'. NOT for generic async choice discussions where Queueable or Future might still be the better tool."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Scalability
  - Performance
  - Reliability
tags:
  - batch-apex
  - database-batchable
  - stateful
  - asyncapexjob
  - batch-scope
triggers:
  - "when should I use Batch Apex"
  - "Database.Stateful pattern for batch"
  - "batch scope size and performance"
  - "AsyncApexJob monitoring for batch"
  - "chaining batch jobs safely"
inputs:
  - "expected record volume and whether query locator is needed"
  - "whether callouts, state accumulation, or chaining are required"
  - "operational monitoring and retry expectations"
outputs:
  - "Batch Apex design recommendation"
  - "review findings for scope, lifecycle, and state risks"
  - "batch scaffold with monitoring and error accumulation guidance"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-03-13
---

Use this skill when Queueable is no longer enough and the workload genuinely needs chunked processing across many transactions. Batch Apex is powerful because each `execute()` scope receives fresh limits, but that same power introduces lifecycle, state, chaining, and monitoring choices that teams routinely under-design.

## Before Starting

- Will the record volume exceed what one Queueable or synchronous transaction should safely handle?
- Does the job need `Database.getQueryLocator()`, custom iterable input, callouts, or cross-scope state?
- How will operations know the batch succeeded, partially failed, or should be retried?

## Core Concepts

### `start`, `execute`, And `finish` Are Separate Responsibilities

`start` defines the workload, `execute` processes each scope, and `finish` handles summary or follow-up actions. Treating them as one blurred method creates monitoring and retry pain. Keep `start` lightweight, `execute` idempotent, and `finish` focused on reporting or safe handoff.

### Scope Size Is A Throughput Tradeoff

The default batch size is commonly 200, but that is not always optimal. Large scopes can increase throughput for simple DML work. Smaller scopes may be safer for heavy processing or callouts. Scope sizing is a performance choice tied to payload weight, lock contention, and external system tolerance.

### `Database.Stateful` Is Useful But Not Free

Stateful batch classes retain instance state between `execute()` calls. That is useful for counters, failed IDs, and summary metrics, but it also means more serialization overhead. Use it when the accumulated state changes the outcome or the reporting story, not by default.

### `AsyncApexJob` Is Part Of The Pattern

Operationally, a batch job is not complete just because `Database.executeBatch()` returned an ID. Job status, processed counts, and error counts live in `AsyncApexJob`, and serious batch designs account for that from the start.

## Common Patterns

### QueryLocator Batch For Large Record Sets

**When to use:** Salesforce data volume is large and query-driven.

**How it works:** Use `Database.getQueryLocator()` in `start()`, process a scope at a time in `execute()`, and monitor the resulting job.

**Why not the alternative:** Direct list loading in one transaction defeats the point of Batch Apex.

### Stateful Error Accumulation

**When to use:** The team needs final counts, failed IDs, or summary reporting after all scopes finish.

**How it works:** Add `Database.Stateful` and store lightweight counters or IDs only.

### Dispatch Follow-Up Work In `finish()`

**When to use:** Another batch, Queueable, or notification should happen only after the batch completes.

**How it works:** Query `AsyncApexJob` or accumulated counters in `finish()`, then launch the next safe step.

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Very large Salesforce record set must be processed safely | QueryLocator Batch | Fresh limits per scope and large-volume support |
| Need only simple after-save async work for a modest set of records | Not Batch; prefer Queueable | Lower framework overhead |
| Need summary counters across all scopes | `Database.Stateful` | Keeps lightweight cross-scope state |
| Need post-completion reporting or next-stage dispatch | `finish()` + `AsyncApexJob` data | Clear completion boundary |


## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org edition, relevant objects, and current configuration state
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Core Concepts and Common Patterns sections above
4. Validate — run the skill's checker script and verify against the Review Checklist below
5. Document — record any deviations from standard patterns and update the template if needed

---

## Review Checklist

- [ ] Batch is used because scale or chunking is truly required.
- [ ] `start()` is lightweight and suitable for the expected record volume.
- [ ] `execute()` is idempotent and safe to retry in part.
- [ ] Scope size is a deliberate choice, not a default carried forward blindly.
- [ ] `Database.Stateful` is used only when cross-scope state is genuinely needed.
- [ ] Monitoring or summary behavior uses `AsyncApexJob` or equivalent visibility.

## Salesforce-Specific Gotchas

1. **Each `execute()` scope gets fresh limits, but `Database.Stateful` still carries serialization cost** — do not store large collections casually.
2. **Callout-enabled batches still need `Database.AllowsCallouts`** — forgetting it breaks valid designs.
3. **A batch job ID is not observability by itself** — you still need job status and error interpretation.
4. **Tests need `Test.stopTest()` for batch completion** — otherwise assertions can run before the batch executes.

## Output Artifacts

| Artifact | Description |
|---|---|
| Batch design review | Findings on lifecycle, state, scope size, and monitoring |
| Batch decision guide | Recommendation for when Batch is justified and how to size and monitor it |
| Batch scaffold | Pattern for `start`, `execute`, `finish`, optional state, and summary behavior |

## Related Skills

- `apex/async-apex` — use when the real design question is whether Batch is needed at all.
- `apex/debug-and-logging` — use when Batch supportability and job diagnostics are the main pain.
- `apex/apex-cpu-and-heap-optimization` — use when the batch already exists and the bottleneck is CPU or heap within `execute()`.
