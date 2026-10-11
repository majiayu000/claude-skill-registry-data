---
name: scheduled-flows
description: "Use when designing or reviewing schedule-triggered flows for recurring automation, replacement of time-based workflow patterns, bounded record selection, idempotent processing, and escalation to Apex when volume is too high. Triggers: 'scheduled flow design', 'nightly flow job', 'time based workflow replacement', 'schedule triggered flow limits'. NOT for record-triggered scheduled paths or large-scale batch processing that should be built directly in Batch Apex."
category: flow
salesforce-version: "Spring '25+'"
well-architected-pillars:
  - Scalability
  - Reliability
  - Operational Excellence
tags:
  - scheduled-flows
  - schedule-triggered
  - recurring-automation
  - idempotency
  - batch-apex-boundary
triggers:
  - "when should i use a scheduled flow"
  - "nightly automation with schedule triggered flow"
  - "scheduled flow versus batch apex"
  - "time based workflow replacement with flow"
  - "scheduled flow volume and retry design"
inputs:
  - "what recurrence is needed and whether the record set can be bounded tightly"
  - "how much data the flow will inspect or mutate on each run"
  - "what should happen on rerun, partial failure, or duplicate processing"
outputs:
  - "scheduled-flow design for record selection, processing, and escalation boundaries"
  - "review findings for unbounded scope, weak retry behavior, and volume risk"
  - "guidance on when to stay in Flow versus move heavy work to Apex"
dependencies: []
version: 2.0.0
author: Pranav Nagrecha
updated: 2026-04-17
---

Use this skill when automation needs to run on a recurring cadence rather than directly from a record event. Schedule-triggered flows work well for bounded recurring tasks such as reminders, renewals, or cleanup logic. They become risky when teams treat them like a general-purpose batch engine and let the record scope or side effects grow without discipline.

The three most common failure modes of scheduled flows in production: (1) unbounded start filter that touches half the org's records on every run, (2) missing idempotency so the same records get "reminded" on every nightly run, (3) silent failure because nobody is monitoring the schedule-trigger error queue. This skill exists to prevent all three — and to know when to stop and use Batch Apex instead.

## Before Starting

Check for `salesforce-context.md` in the project root. If present, read it first.

Gather if not available:
- What recurrence is required, and is the automation tied to a business calendar or to a record event that might fit a scheduled path better?
- How many records could match the criteria on a normal day, and what is the worst-case volume during seasonal or data-load spikes?
- How will the flow avoid duplicate work if it runs again, partially fails, or overlaps with another automation?
- What is the expected runtime budget (each scheduled-flow invocation must finish within async limits)?
- Who owns the error-email recipient for this schedule? What's the SLA on response?

## Core Concepts

The core design problem in scheduled flows is not the schedule itself. It is **bounded scope** plus **repeat-safe behavior**. A recurring automation that cannot explain which records it will touch, why it will touch them only once when appropriate, and when it should escalate out of Flow is not ready for production.

### Choose The Right Time Primitive

Three options; only one is a schedule-triggered flow:

| Primitive | When to use | When NOT |
|---|---|---|
| **Schedule-triggered flow** | Periodic scan of records matching time-based criteria independently of save events (nightly lease-renewal reminders, quarterly data cleanup) | When triggered from a record event — use scheduled path instead |
| **Scheduled Path on record-triggered flow** | Record event → wait N days → do work (send follow-up email 14d after Case created) | When there's no triggering record — schedule-triggered is the answer |
| **Batch Apex scheduled via System.schedule** | High-volume periodic processing, complex joins, large record sets | When the workload truly fits Flow's model (small set, simple operations, admin-maintainable) |

A wrong primitive choice is the most common scheduled-flow design error. If the requirement starts "when a record is X and Y days old", it's likely a scheduled path, not a schedule-triggered flow.

### Bounded Selection Comes First

The start criteria should narrow the job to a realistic set of records. Wide-open scans with complex branching downstream create both performance risk and support ambiguity. Good scheduled flows have clear filters, explicit stop conditions, and a manageable result set per run (< 250 records per run is a good rule of thumb for pure-Flow execution).

Concrete selection criteria should combine:
- **Type/status filter** — `Status = 'Open' AND RecordType = 'Support'`.
- **Time-window filter** — `LastModifiedDate < TODAY - 30` or `CreatedDate = THIS_MONTH`.
- **Processing marker** — `Last_Reminded_Date__c != TODAY` (see idempotency below).

Filters that rely on computed fields or formula predicates WILL slow the scheduled query. Prefer indexed fields + date ranges + processing flags.

### Idempotency Matters In Recurring Automation

A recurring flow should be able to answer: "has this record already been processed for this job window?" Without idempotency, the same records get reminded, updated, or emailed every run — a frequent source of "the system spammed our customers" incidents.

Idempotency patterns:

| Pattern | Implementation | Tradeoff |
|---|---|---|
| Processing flag | `Processed_Today__c = true` set at end of processing; reset nightly | Simple; requires a reset job |
| Last-processed date | `Last_Processed_At__c = <timestamp>`; filter on `Last_Processed_At__c < TODAY` | No reset needed; field can stale |
| Status transition | Move record to a terminal status that the filter excludes | Cleanest; requires business-meaningful status |
| External lock | Write to a custom "job log" object; check before processing | Most robust; highest overhead |

### Flow Is Not Always The Final Execution Engine

When the recurring job becomes large (> 500 records per run), computationally heavy (complex joins or multi-step transformations), or deeply iterative (nested loops with DML), the right answer may be to use the scheduled flow only as a lightweight orchestration layer or move the workload into Batch Apex entirely. The schedule does not justify using the wrong execution model.

**Signals Flow is no longer the right engine:**
- Record count per run > 500.
- CPU time approaches the async limit (60s sync / still constrained async).
- The Flow has > 5 DML operations in a loop.
- The job needs to run more than daily to stay current.
- Apex invocables are doing most of the real work (then just make it Batch Apex).

## Common Patterns

### Pattern 1: Narrow Nightly Follow-Up Flow

**When to use:** Recurring reminder or status update on a bounded slice of records.

**Structure:**
```text
Schedule: Daily at 2am
Entry criteria: Status = 'Pending' AND CreatedDate < TODAY - 7 AND Last_Reminded_Date__c != TODAY
Plan:
  └── [Get Records matching entry criteria, LIMIT 200]
  └── [Loop]:
       └── [Send Custom Notification OR Email Alert]
       └── [Assignment: Last_Reminded_Date__c = TODAY]
  └── [Update Records] (bulk update after loop)
  └── [Fault path: log + notify admin]
```

**Why not the alternative:** A broad nightly sweep without clear selection becomes unpredictable and expensive.

### Pattern 2: Scheduled Flow As Lightweight Orchestrator

**When to use:** The timing belongs in Flow, but the heavy work belongs elsewhere.

**Structure:**
```text
Schedule: Weekly on Monday 3am
Plan:
  └── [Get Records: this week's candidates (narrow filter)]
  └── [Decision: record_count > threshold?]
       └── Yes → [Invocable Apex: kick off Batch Apex job with candidate IDs]
       └── No  → [Process inline via Loop + subflow]
```

Flow owns the timing and the "is this worth running today" check. Apex owns the work.

### Pattern 3: Replace Time-Based Workflow With Explicit Criteria

**When to use:** Legacy time-based Workflow Rule being migrated to Flow.

**Structure:** The Workflow Rule's "Evaluate every time a record is created or edited" + time-based action becomes a record-triggered flow's Scheduled Path (NOT a schedule-triggered flow) — because the behavior is record-event-driven, not portfolio-scan-driven.

For ACTUAL portfolio-scan automation being migrated from custom Apex scheduled jobs: evaluate whether it's really Flow-shaped first. Many scheduled Apex jobs exist because there was no good Flow primitive; now that scheduled flows + scheduled paths exist, some can migrate, but not all.

### Pattern 4: Run Log + Monitoring

**When to use:** Any production scheduled flow — this is not optional.

**Structure:**
```text
Start of run → [Create Records: Scheduled_Flow_Run__c with start_time + run_id]
... main work ...
End of run → [Update Records: the same log record with end_time + record_count + status]
Fault path → [Update Records: log record with status='failed' + fault_message]
```

A Scheduled_Flow_Run__c object (or equivalent) gives operations:
- **Run history** — did the 3am job actually run last night?
- **Duration trends** — is the nightly job taking longer over time?
- **Failure visibility** — alert when `status='failed'` appears without alerting on every successful run.

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Recurring job scans a bounded set of records daily or weekly | Schedule-triggered flow (Pattern 1) | Good fit for predictable recurring automation |
| Follow-up tied to a specific record save event | Scheduled path on record-triggered flow | Event-based, not portfolio-wide |
| Job volume or processing complexity high | Batch Apex or async code boundary | Flow is not the best execution engine for heavy batch work |
| Repeated reminders need duplicate prevention | Add idempotent markers or date fields | Recurring runs must know what's already processed |
| Selection criteria vague or unbounded | Redesign before scheduling | Schedule will amplify poor scope decisions |
| Job needs to run multiple times per day | Consider sub-hourly schedule (flow limits) or move to Batch Apex | Flow scheduling granularity may not fit |
| Requires external callout per record | HTTP Action inline for small sets; async via Platform Events for large | Per-record callouts exhaust callout limits |

## Well-Architected Pillar Mapping

- **Scalability** — findings about unbounded scope, linear-in-records DML, cross-transaction budget contention land here. Bad scheduled flows scale linearly into incidents.
- **Reliability** — missing idempotency and missing fault handling produce "we didn't know it failed" and "it ran twice and double-processed" — both reliability failures.
- **Operational Excellence** — run-log observability, error-email monitoring, and "did last night's job finish" dashboards.

## Review Checklist

- [ ] Schedule primitive is correct (scheduled flow vs scheduled path vs Batch Apex).
- [ ] Start criteria narrow the candidate record set intentionally (no bare `Active=true`).
- [ ] Idempotent markers prevent duplicate tasks, emails, or updates across runs.
- [ ] Failure handling exists for every DML element (Pattern A from `flow/fault-handling`).
- [ ] Volume expectations were reviewed for normal and worst-case runs.
- [ ] Heavy work was escalated out of Flow when appropriate.
- [ ] Run log exists (custom object or equivalent) for operational monitoring.
- [ ] Error-email recipient is a monitored mailbox, not a single inactive admin.


## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org edition, relevant objects, and current configuration state
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Common Patterns above
4. Validate — run the skill's checker script and verify against the Review Checklist above
5. Document — record any deviations from standard patterns and update the template if needed

---

## Salesforce-Specific Gotchas

1. **A recurring schedule amplifies weak selection logic** — broad filters turn into repeated large jobs quickly.
2. **Recurring automation needs duplicate prevention explicitly** — without markers, the same records can be processed on every run.
3. **Scheduled flows are not a substitute for true batch architecture** — the timing may fit, while the execution model does not.
4. **A record-event requirement may fit scheduled paths better** — choosing the wrong time primitive creates unnecessary complexity.
5. **Scheduled-flow errors email the Process Automation user**, same as record-triggered flows. Verify the recipient is monitored annually.
6. **Scheduled flows DO NOT retry automatically on failure** — a failed run just... doesn't run. The next scheduled run tries fresh. Build retry logic into the flow if the business needs it.
7. **Two schedules overlapping can compete for records** — if two scheduled flows both filter "Status = Open", run one, the records transition, then the second flow sees different results than the first. Design mutually-exclusive filters or serialize schedules.
8. **Salesforce limits the number of scheduled jobs per org** — check `AsyncApexJob` + scheduled-flow limits before adding the Nth schedule.
9. **Daily-at-2am is everyone's default** — so everyone's org hits Salesforce's scheduler peak load at 2am. Spread actual scheduled times to avoid platform contention.
10. **Scheduled flows can't be paused mid-run** — once started, they run to completion or failure. Design the scope accordingly.

## Proactive Triggers

Surface these WITHOUT being asked:

- **Scheduled flow with no idempotency marker** → Flag as Critical. Will double-process on retry or next run.
- **Scheduled flow with unbounded start criteria (e.g. "Active = true" alone)** → Flag as Critical. Volume bomb waiting to happen.
- **Record-event requirement being built as scheduled flow instead of scheduled path** → Flag as High. Wrong primitive.
- **Scheduled flow > 500 records per run with no escalation plan** → Flag as High. Probably needs Batch Apex.
- **No run log / monitoring surface for production scheduled flow** → Flag as High. Silent failure invitation.
- **Multiple scheduled flows on same object with overlapping filters** → Flag as Medium. Coordination risk.
- **Scheduled flow error email recipient is inactive** → Flag as Critical. Unseen failure pattern.
- **All scheduled flows set for 2am** → Flag as Low. Platform-peer peak-load contention; spread schedules.

## Output Artifacts

| Artifact | Description |
|---|---|
| Scheduling design | Recommendation for schedule-triggered flow, scheduled path, or Apex |
| Scope and idempotency plan | Rules for bounded selection and duplicate prevention |
| Volume review findings | Risks around record set size, side effects, execution model choice |
| Run-log specification | Scheduled_Flow_Run__c schema + dashboard guidance |

## Related Skills

- **flow/flow-bulkification** — use when the recurring job may still break under shared limit pressure.
- **flow/fault-handling** — use when the main challenge is how background failures should be surfaced.
- **flow/record-triggered-flow-patterns** — use when a scheduled path on a record-triggered flow is the right primitive instead.
- **apex/batch-apex-patterns** — use when the workload has clearly crossed into true batch-processing territory.
- **standards/decision-trees/async-selection.md** — upstream decision tree for scheduled flow vs Batch Apex vs Queueable.
