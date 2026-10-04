---
name: governor-limits
description: "Use when writing, reviewing, or troubleshooting Apex that risks hitting Salesforce governor limits. Triggers: 'too many SOQL queries', 'too many DML statements', 'CPU time limit', 'bulkification', 'Queueable vs Batch', 'fix a governor limit exception', 'check limits for a platform event trigger'. NOT for the 100-callout-per-transaction ceiling — use integration/callout-limits-and-async-patterns. NOT for org-level capacity planning — use architect/limits-and-scalability-planning. NOT for runtime Limits class guard clauses — use apex/apex-limits-monitoring."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Scalability
  - Reliability
  - Performance
  - Operational Excellence
tags: ["governor-limits", "bulkification", "queueable", "batch", "cpu-time"]
triggers:
  - "hitting CPU time limit exceeded exception"
  - "too many SOQL queries exception in trigger"
  - "list has no rows for assignment to SObject"
  - "limit exception when processing large data sets"
  - "batch apex failing execute method at scale"
  - "how do I bulkify this trigger"
  - "too many SOQL queries"
  - "bulkify trigger avoid limits"
  - "diagnose maximum trigger depth exceeded error"
  - "resolve too many SOSL queries in transaction"
  - "fix System.LimitException too many SOQL queries 101 in a trigger"
  - "make a platform event trigger safe for 2000 records per batch"
inputs: ["failing transaction", "record volume", "entry point"]
outputs: ["limit triage findings", "bulk-safe design guidance", "async pattern recommendation"]
dependencies: []
version: 1.1.1
author: Pranav Nagrecha
updated: 2026-10-03
---

You are a Salesforce expert in Apex transaction design. Your goal is to keep Apex bulk-safe, limit-aware, and operationally predictable under real production volume. Use this skill when you see too many SOQL queries errors or need to bulkify a trigger to avoid limits.

## Before Starting

Check for `salesforce-context.md` in the project root. If present, read it first.
Only ask for information not already covered there.

Gather if not available:
- Is this trigger, synchronous service, Queueable, Batch, or `@AuraEnabled` Apex?
- What operation is failing: SOQL, DML, CPU, heap, callouts, or async chaining?
- What record volume is realistic in production, not just in the failing example?
- Is the code called by Flow, Process, Platform Events, or integrations in the same transaction?

## Questions to Ask Before Configuring

| Question | Why it matters | What a good answer adds | What proper configuration adds over just doing it |
|---|---|---|---|
| "What starts the transaction: a trigger, a platform event or CDC subscriber, a UI call, an API load, a schedule?" | Trigger batch size is 200, but 2,000 for platform events and Change Data Capture; scheduled Apex runs with synchronous limits | The real batch size and limit tier to design for | Code sized for the worst real input, not the demo record |
| "What else runs in the same transaction: flows, other triggers, managed packages?" | Limits are per transaction, and CPU time includes processes called from the code, such as package code and workflows | A list of every automation layer sharing the budget | A budget that holds when all automation fires together |
| "Which limit failed, and what did the last `LIMIT_USAGE_FOR_NS` block show?" | Each limit has a different fix: SOQL count, query rows, CPU, heap, DML rows, stack depth | The exact limit and where it was consumed | A targeted fix instead of a rewrite |
| "How many records can one run touch at peak?" | 50,000 query rows and 10,000 DML rows are the same in sync and async; only a Batch `QueryLocator` reaches 50 million rows | Synchronous, Queueable, Batch, or cursor choice | No async rewrite that hits the same row limit |
| "Does the transaction make callouts after DML?" | The guide's examples throw "You have uncommitted work pending" for a callout after uncommitted DML | An async boundary for the callout | Callouts that do not roll back saves |
| "Is this an ISV package?" | Certified managed packages get their own per-namespace limits, inside cumulative cross-namespace totals; heap and CPU are shared | The namespace's budget alongside subscriber code | A package that behaves in busy subscriber orgs |

What proper design adds over just bulkifying the obvious loop: the transaction is sized for its real entry point and batch size, every automation layer is counted, and the fix targets the limit that actually failed.

## How This Skill Works

### Mode 1: Build from Scratch

1. Assume 200-record bulk execution unless the entry point proves otherwise, but bump that to 2,000 for platform-event or Change Data Capture subscriber triggers.
2. Design the transaction around the collect -> query once -> map -> process -> DML once pattern.
3. Decide whether the work belongs in synchronous Apex, Queueable, Batch, or Platform Events.
4. Keep callouts, cross-object fan-out, and large data movement out of fragile trigger paths.
5. Add limit checkpoints or test assertions where the volume risk is non-trivial.

### Mode 2: Review Existing

1. Find any SOQL, DML, callout, JSON parsing, or heavy string work inside loops.
2. Check whether trigger logic, Flow-invoked Apex, and helper classes share the same limit budget.
3. Verify async selection: Queueable for controlled background work, Batch for large-scale processing, `@future` only for small legacy patterns.
4. Flag transactions that assume single-record behavior when Salesforce can send 200.
5. Review tests for bulk scenarios, not just happy-path singles.

### Mode 3: Troubleshoot

1. Start from the exact limit exception or debug log checkpoint.
2. Identify the real transaction boundary and every automation layer inside it.
3. Count where queries, DML, CPU, or heap are consumed.
4. Fix the pattern first, then choose async offload if the business flow still exceeds a safe synchronous budget.
5. Re-test with realistic batch size and related automation enabled.

## Governor Limit Control

### Limits That Matter Most

Every value below is quoted with its line reference in `references/limits-table.md` (Apex Developer Guide 262, Execution Governors and Limits).

| Limit | Synchronous | Asynchronous | Why It Matters |
|-------|-------------|--------------|----------------|
| SOQL queries | 100 | 200 | Loop-driven query patterns fail first |
| SOSL queries | 20 | 20 | SOSL has its own count, separate from SOQL; a loop full of `FIND` burns it fast |
| SOSL records per query | 2,000 | 2,000 | A single search caps at 2,000 rows regardless of the SOQL 50,000 ceiling |
| DML statements | 150 | 150 | Repeated `update` or `insert` in loops burns budget quickly |
| DML rows | 10,000 | 10,000 | Large fan-out often needs Batch |
| CPU time | 10,000 ms | 60,000 ms | Complex transforms and nested loops fail here |
| Max transaction execution time | 10 min | 10 min | A hard wall-clock ceiling separate from CPU time; long callout waits or slow processing trip it even when CPU stays low |
| Heap size | 6 MB | 12 MB | Large collections and JSON payloads dominate memory |
| Callouts | 100 | 100 | Integration loops still hit a hard cap |
| Callout cumulative timeout | 120 sec | 120 sec | Total wait across all callouts in a transaction; many small calls with generous timeouts add up |
| `EventBus.publish` (immediate) | 150 | 150 | Publish-immediate platform events have their own cap, distinct from DML statements |
| Trigger recursion stack depth | 16 | 16 | Recursive DML that re-fires triggers throws `Maximum trigger depth exceeded` at 16 |
| Queueable jobs enqueued | 50 | 1 child/job | Matters for fan-out and chaining strategy |
| Apex cursors (`Database.Cursor`) | 10,000/day org-wide | same | Distinct from ordinary SOQL row limits; `Cursor.fetch` still counts against SOQL query and row limits (max 100 fetch calls per transaction) |
| Apex cursor rows per transaction | 50 million | 50 million | Across all cursors in one transaction; the guide gives the same value for sync and async |
| Apex cursor rows per 24h | 100 million cumulative (org-wide) | same | New plus pagination cursor rows combined |

**Apex Cursors.** `Database.getCursor(query)` returns a `Database.Cursor` you can `fetch(position, count)` from any offset and pass between chained Queueable jobs. The cursor fixes its set of record IDs when created. Each `fetch` counts against the SOQL query limit and its rows against the query-row limit, with at most 100 fetch calls per transaction. Monitor with `Limits.getApexCursors()` and `Limits.getApexCursorRows()`. Use cursors for resumable processing of very large result sets, not as a substitute for bulkification in triggers. UNVERIFIED (2026-10-03): the release in which cursors became generally available and whether a `Database.Cursor` can be returned to LWC through `@AuraEnabled`; version 1.1.0 of this skill stated "Spring '26, API 66.0" and LWC serialization without a source.

**Trigger batch size is 200 for standard DML, but 2,000 for platform events and Change Data Capture events.** Code in a platform-event or CDC subscriber trigger must be bulk-safe against 2,000 records per execution, not 200. The same governor budgets apply, so a per-record query or DML that "works" at 200 fails hard at 2,000.

For AppExchange / ISV authors: a certified managed package gets **cumulative cross-namespace limits** on top of the per-namespace values above (for example 1,100 SOQL queries and 1,650 DML statements across all namespaces in a transaction). Your package still lives inside those totals when it runs alongside a subscriber's code and other packages.

### Bulkification Pattern

Use this order every time:

1. Collect IDs or keys from the input records.
2. Query once outside the loop.
3. Build maps or grouped collections for O(1) lookup.
4. Process in memory.
5. Perform DML once per object/action where possible.

If a design cannot follow that pattern, justify why and re-check whether the work should move async.

### Async Decision Matrix

| Mechanism | Use When | Avoid When |
|-----------|----------|------------|
| `Queueable` | Need controlled async work, SObject context, chaining, or callouts | You must process very large data sets |
| `Batch Apex` | More than 10,000 rows, scheduled cleanup, or large reprocessing | The work is really one user transaction and must finish immediately |
| `@future` | Small legacy callout or fire-and-forget pattern | New feature work that needs chaining, tracking, or richer payloads |
| Platform Event | Need decoupling across systems or automation layers | You need immediate same-transaction guarantees |

### Callout and DML Rule

Do not treat callout failures as a last-minute patch.

- If the transaction already performed DML, move the callout to Queueable or another async boundary.
- If the callout result is required before commit, redesign the flow so the transaction order is explicit and safe.
- If the trigger path depends on an external system, document the business fallback before shipping.

## Recommended Workflow

1. **Name the entry point and batch size.** Trigger (200), platform event or CDC subscriber (2,000), UI, API load, scheduled (synchronous limits), Queueable, or Batch.
2. **Read the failing log.** Find the limit exception and the last `LIMIT_USAGE_FOR_NS` block; list every automation layer in the transaction.
3. **Fix the pattern.** Collect keys, query once, map, process in memory, DML once; move SOQL, DML, callouts, and JSON parsing out of loops. Start from `templates/bulk-safe-service.cls`.
4. **Choose the execution model** only after the pattern is fixed: synchronous, Queueable, Batch, or cursors with chained Queueables, sized against `references/limits-table.md`.
5. **Prove it at volume.** Tests with 200 records (2,000 for event triggers), related automation enabled, and `Test.startTest()` for a fresh limit set; run `python3 scripts/check_limit_usage.py force-app/main/default`.

---

## Review Checklist

- [ ] No SOQL inside loops
- [ ] No DML inside loops
- [ ] No repeated JSON parse or string-heavy work inside loops
- [ ] Related automation layers are counted in the same transaction budget
- [ ] Async choice matches volume and recovery needs
- [ ] Bulk tests cover 200 records and realistic related data

## Salesforce-Specific Gotchas

| Gotcha | Why it bites |
|---|---|
| Limits are per transaction, not per method | Trigger code, service classes, Flow-invoked Apex, and utilities all share the same governor budget. |
| Apex is bulk-called even when users work one record at a time | Data loads, list views, integrations, and platform internals can still hand you 200 records. |
| `@future` is a narrow tool | Primitive-only parameters, no chaining, weak observability; a poor default for new work. |
| Callout after DML causes `uncommitted work pending` | If the transaction already changed data, offload the callout or redesign the process. |
| Batch resets limits per execute chunk, not per job | Expensive code can still fail inside one chunk even though the whole job is "async." |
| `Database.getQueryLocator` outside Batch `start` is capped at 10,000 rows | The 50 million figure applies only to a Batch `QueryLocator` (limits table L19548, L19856). |
| Scheduled Apex is async but gets synchronous limits | 100 SOQL and 10,000 ms CPU apply inside `Schedulable.execute` (L19536). |
| Recursion depth has its own limit of 16 | Recursive DML re-firing a trigger throws `Maximum trigger depth exceeded` well before count limits catch it. |
| CPU time is not the only time-based ceiling | A hard 10-minute transaction wall applies even when CPU stays low; long callout waits count against it. |

## Proactive Triggers

Surface these WITHOUT being asked:

| Pattern | Severity | Reason |
|---|---|---|
| SOQL or DML inside loops | Critical | Fastest path to production limit failures. |
| Trigger or service code written for one record only | High | Salesforce can bulk-invoke it with 200 records. |
| CPU-heavy string/JSON logic inside nested loops | High | CPU failures are often harder to diagnose than SOQL overages. |
| Async used as a band-aid over bad synchronous design | Medium | Offloading broken logic still creates broken jobs. |
| No bulk test coverage or no limit assertions in risky code | Medium | The design has not been proven at realistic scale. |

## Output Artifacts

| When you ask for... | You get... |
|---------------------|------------|
| Bulkification review | Findings on SOQL, DML, CPU, heap, and async misuse |
| New Apex scaffold | A bulk-safe pattern with transaction boundaries called out |
| Limit exception triage | Root cause plus the smallest safe design change |

## Related Skills

- **apex/trigger-framework**: Trigger structure decides whether limit-safe patterns are even possible.
- **apex/soql-security**: Query refactors still need CRUD/FLS enforcement, not just lower SOQL counts.
- **flow/fault-handling**: Flow-invoked Apex and record-triggered automation can share the same budget.
