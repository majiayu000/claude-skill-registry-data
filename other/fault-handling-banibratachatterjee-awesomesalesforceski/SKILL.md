---
name: fault-handling
description: "Use when designing, reviewing, or troubleshooting Salesforce Flow fault handling, error logging, and bulk-safe automation paths. Triggers: 'fault connector', '$Flow.FaultMessage', 'flow failed', 'record-triggered flow rollback', 'screen flow error'. NOT for generic Flow type selection unless the main risk is failure handling; NOT for Apex exception handling (see apex/exception-handling-patterns)."
category: flow
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Reliability
  - Scalability
  - Operational Excellence
tags: ["flow-faults", "fault-connectors", "error-logging", "record-triggered-flow", "screen-flow"]
triggers:
  - "flow fails and rolls back the entire transaction"
  - "unhandled fault in record triggered flow"
  - "how do I catch errors in a flow"
  - "how do I send flow error notification to admin"
  - "bulk data load causing flow to fail on one record and roll back all"
  - "flow error email message is confusing to users"
  - "what happens when flow fails"
  - "flow fails fault path"
inputs: ["flow type", "failure points", "user impact"]
outputs: ["fault handling review", "error path recommendations", "bulk safety findings"]
dependencies: []
version: 2.0.0
author: Pranav Nagrecha
updated: 2026-04-17
---

You are a Salesforce expert in Flow failure design. Your goal is to make Flows fail predictably, surface useful errors, and avoid silent rollback or bulk-data surprises. Flow failures are not just bugs — they are an architectural concern. A Flow without fault handling is a Flow that rolls back transactions, hides root causes, and turns one bad record into a batch-wide outage. The job of fault handling is to convert failures from "mystery at 3 AM" to "row 47 failed this validation, here's the log entry, here's the remediation."

This skill covers the full fault-handling design space: when to add connectors, how to shape the user message vs the diagnostic log, how to keep record-triggered flows bulk-safe when one record trips, and how to align the Flow's failure posture with the Well-Architected pillars (Reliability, Scalability, Operational Excellence). Use it for new-design, review, and troubleshooting work.

## Before Starting

Check for `salesforce-context.md` in the project root. If present, read it first. Only ask for information not already covered there.

Gather if not available:
- Is the Flow record-triggered, screen, scheduled, auto-launched, or orchestration?
- Which elements can fail: DML, subflow, Apex action, email action, HTTP action, or managed-package invocable?
- What should happen on failure: user message, admin notification, error log, explicit termination, or transaction rollback?
- Is the Flow invoked in bulk through data load, integration (REST/SOAP/Bulk API), or upstream Apex?
- Is there an existing error-log object (`Application_Log__c`, `Flow_Error_Log__c`, custom) or should one be proposed?
- Does the org have a fault-email recipient configured under Process Automation Settings?

## How This Skill Works

### Mode 1: Build from Scratch

For a new Flow that must fail predictably from day one.

1. **Inventory fallible elements before the happy path.** List every `Get Records`, `Create`, `Update`, `Delete`, `Action`, `Subflow`, and `HTTP Callout` element. Each is a potential fault source; each needs a routing decision.
2. **Classify failure severity per element.** Validation failure (user-recoverable) vs platform limit (batch-wide impact) vs integration timeout (transient, potentially retry-able) vs managed-package exception (third-party, opaque).
3. **Choose the fault-routing pattern** per element — see "Fault-Routing Patterns" below. Not every element needs a unique fault branch; several can converge on a shared error-logging tail.
4. **Design two messages per fault**: the user-safe message (plain English, action-oriented) and the diagnostic detail (captures `$Flow.FaultMessage`, element name, record id, user id).
5. **Keep record-triggered flows bulk-safe** — query once outside loops, avoid per-record DML inside loops, verify after-save DML fan-out is within governor bounds at the expected input cardinality.
6. **Test five failure paths**: happy path, validation failure, duplicate-rule failure, platform-limit failure (CPU or SOQL), and integration-action failure. Unit-test each with a controlled input.
7. **Wire observability**: the error-log object, a notification (custom notification > email > push-to-chat), and a run-summary metric if the Flow runs in background (`FlowInterviewLog` is the Salesforce-native place to watch).

### Mode 2: Review Existing

For auditing a Flow that may already be in production.

1. **Single-pass map** of every element against the fault-routing checklist below. Even one missing connector on a fallible element is a P0 finding.
2. **Verify user-facing messages are plain English.** Any message containing `$Flow.FaultMessage` raw, `System.` tokens, or HTML artifacts is a UX failure.
3. **Confirm diagnostic detail is logged separately.** The raw `$Flow.FaultMessage` must end up somewhere an admin can read later — error-log record, custom notification with attached detail, Chatter post to a triage group, or an email to an ops distribution list.
4. **Review after-save flows for DML fan-out.** Count DML operations per interview; multiply by expected bulk cardinality; check against the 150 DML statements per transaction limit.
5. **Confirm subflows and invocable Apex fail observably.** A subflow without its own fault handling can bubble a useless generic error to the caller. An invocable Apex that swallows exceptions silently is worse than one that throws.
6. **Check for fault-email recipient config at org level.** If Process Automation Settings has no default workflow user, unhandled faults go to the org's automated workflow email — often a mailbox nobody reads.
7. **Flag any Flow that can fail silently.** Silent failure is strictly worse than a loud failure; a loud failure at least gets noticed.

### Mode 3: Troubleshoot

For a Flow that is already failing.

1. **Read `$Flow.FaultMessage` from the Flow error email or FlowInterviewLog.** This is the ground-truth error; everything else is interpretation.
2. **Identify the failing element** (name and type). The error email includes the element name — use it.
3. **Classify the underlying cause**: business validation (a Validation Rule fired — expected but perhaps not routed), platform limit (SOQL/CPU/DML exceeded — bulk issue), missing fault routing (the element simply has no fault connector), shared-transaction conflict (Apex + Flow contending for governor budget).
4. **Check whether the Flow is invoked in a shared transaction.** Apex callers of invocable Flows share CPU + SOQL + DML budgets with the Flow's elements. One element's exhaustion can be another caller's fault.
5. **Add or repair the fault path BEFORE attempting any other optimization.** Without fault routing, every future iteration is blind.
6. **If the failure is at scale**, profile a single successful interview first (`FlowInterviewLog` with debug logging) and multiply. Bulk failures are usually linear multiplications of a per-interview waste that wasn't visible at single-row volume.

## Fault-Routing Patterns

Four canonical patterns. Combine them — most production Flows use a mix.

### Pattern A: User-safe branch + diagnostic log

For user-facing screen flows and user-initiated quick actions.

```text
[DML or Action]
    ├── Success → [Next business step]
    └── Fault   → [Assignment: userMessage = "We could not complete your request right now. Please try again or contact support."]
                → [Assignment: diagnosticDetail = {!$Flow.FaultMessage}]
                → [Create Records: Application_Log__c with diagnosticDetail + recordId + userId + elementName]
                → [Screen: show userMessage + link to support]
                → [End]
```

The user sees a message they can act on. The admin sees the raw fault detail in the log object.

### Pattern B: Retry-once for transient failures

For HTTP callouts, integration actions, and other elements where the first failure may be transient.

```text
[HTTP Action]
    └── Fault → [Decision: is error code 5xx or timeout?]
                  ├── Yes → [Wait 30s via Platform Event delay] → [HTTP Action retry]
                  │           ├── Success → [continue]
                  │           └── Fault   → [log + notify + end]
                  └── No  → [log + notify + end]  // 4xx errors are not retried
```

Retry once. Retrying more than once inside a Flow is an anti-pattern — escalate to Platform Events or a separate scheduled retry Flow.

### Pattern C: Continue-on-error for bulk safety

For record-triggered flows that need to survive one record failing out of many.

```text
Per-record element in a loop
    └── Fault → [Assignment: add record to failed_records collection with reason]
                → [continue to next iteration]

After loop:
    → [Decision: failed_records.size > 0]
         ├── Yes → [Create Records: Flow_Error_Log__c for each entry]
         │        → [Send notification to admin]
         │        → [End — successful records are committed]
         └── No  → [End]
```

Caution: this pattern only works if the individual element is INSIDE a loop. Record-triggered flows without an explicit loop process each record in a separate interview; Salesforce already handles the "one record fails, continue others" case at the interview boundary — but only if the per-interview Flow has a fault connector that ends cleanly.

### Pattern D: Explicit termination

For critical-path flows where partial success is worse than total failure.

```text
[DML or Action]
    └── Fault → [Assignment: diagnosticDetail = {!$Flow.FaultMessage}]
                → [Create Records: Application_Log__c (if possible — but this may roll back too)]
                → [Send Email Alert via Email Alert action]  // Decoupled from the transaction
                → [End — DO NOT suppress the error]
```

In Pattern D, the Flow's fault path ends WITHOUT suppressing the failure, so the transaction still rolls back. The log and the email alert are best-effort notifications. This is the right pattern for "order placement failed" — you don't want partial data committed.

## Flow Fault Handling Rules

### Elements That Must Be Treated as Fallible

| Element Type | Typical Failure Modes | Required Fault Routing |
|--------------|-----------------------|------------------------|
| Get Records | Query limit, unexpected empty result assumptions, too-many-rows | Pattern A or C; assume zero rows + handle "not found" case explicitly |
| Create/Update/Delete | Validation rule, duplicate rule, required field, record lock, FLS denial | Pattern A (user-initiated) or C (bulk) |
| Subflow | Downstream failure propagates up; managed-package subflows are opaque | Parent calls with Pattern A; inner subflow should fault-handle its own elements |
| Apex or invocable action | Thrown `AuraHandledException`, unhandled business error, governor exhaustion | Pattern A; the invocable Apex itself should honor `with sharing` and FLS |
| HTTP action / external step | Timeout (default 120s), auth failure, 4xx/5xx response, rate-limit | Pattern B for 5xx/timeout; Pattern A or D for 4xx |
| Email action | No active recipient, template reference invalid, org-level send-limit exhausted | Pattern A — but NOT Pattern D for notification paths (losing the notification is worse than a partial send) |
| Send Custom Notification | Notification Type not active, recipient reference invalid | Pattern A; fall back to email or log-only |
| Platform-event subscribe | Delivery miss, replay buffer expiry, subscriber session timeout | Requires out-of-band monitoring; not a fault-connector concern at the Flow level |

### Minimum Fault Pattern

Every fallible element must route to:

1. A user-safe message or business-logic branch (Pattern A / C) OR an explicit termination decision (Pattern D).
2. A diagnostic detail capture using `$Flow.FaultMessage` — NEVER discarded.
3. A log record, notification, or explicit observable termination decision.

For screen flows, the user must see a clear next step. For record-triggered flows, the support team must have enough context to diagnose rollback causes — minimum: failing record id, element name, timestamp, user id, fault message.

### Error-Message Design

The UX cost of a raw fault message is real. Design two messages per fault:

| Audience | Message content | Example |
|---|---|---|
| User (screen flow) | Plain English, action-oriented, no technical jargon | "We couldn't save your changes. Please check the required fields and try again." |
| Admin (log + email) | Full diagnostic detail preserved | `Element: Update_Case. Error: FIELD_CUSTOM_VALIDATION_EXCEPTION, Priority cannot be set to Urgent without a justification. Record: 500xx00000ABCD` |
| Integration (caller) | Machine-parseable where the calling system needs to branch | HTTP status + JSON body including fault code (`FLOW_FAULT_VALIDATION_RULE`, `FLOW_FAULT_LIMIT_EXCEEDED`, etc.) |

Raw `$Flow.FaultMessage` belongs in the admin audience only.

## Bulk-Safety Deep Dive

Record-triggered flows fire once per interview; bulk DML (data load, integration, upstream Apex) triggers many interviews in a single transaction. Three bulk-safety risks dominate:

### Risk 1: Repeated `Get Records` per interview

Every interview's `Get Records` counts against the transaction's 100-SOQL limit. For a 200-record load, 2 `Get Records` per interview = 400 SOQL calls — over the limit, every record in the batch rolls back.

**Safer patterns:**
- Query once outside the loop if possible (auto-launched flow called by a single `Get Records` in a parent Flow).
- Use before-save logic for same-record reads (`$Record` and `$Record__Prior` are free — no SOQL).
- Cache lookups via Custom Metadata or Platform Cache for reference data.

### Risk 2: After-save DML fan-out

Each interview's DML elements count against the 150-statement limit. An after-save flow that creates 3 related records per source record hits the limit at 50 source records — far below typical data-load batch sizes.

**Safer patterns:**
- Aggregate the source records into one DML call via a Get-then-Update loop outside individual interviews (usually requires an invocable Apex to bulk).
- Move fan-out to async: Platform Event fire-and-forget, or schedule a Platform Event Flow for deferred creation.
- Reduce the fan-out — is every related record actually needed?

### Risk 3: Invocable Apex not list-safe

An invocable Apex with a method signature `void doWork(MyInputType input)` and an `@InvocableVariable` on the INSTANCE level receives one call per interview. A method signature `void doWork(List<MyInputType> inputs)` receives ONE call per batch. The former fires 200 times in a 200-record load; the latter fires once.

**Safer pattern:** every invocable method used from a Flow should accept a `List<T>` of inputs and return `List<Result>`. Flow automatically aggregates and de-aggregates.

### Bulk Safety Checklist

- [ ] SOQL count per interview × bulk cardinality < 100
- [ ] DML count per interview × bulk cardinality < 150
- [ ] Invocable Apex signatures accept `List<T>` not single instances
- [ ] Per-interview `Get Records` checked for cacheability via Platform Cache or Custom Metadata
- [ ] After-save DML fan-out counted and documented
- [ ] Missing fault connector on any DML element — treat as a bulk-safety issue, not just a fault-handling issue: one bad record rolls back the whole batch

## Well-Architected Pillar Mapping

This skill's findings map to three pillars — surface the pillar in every review.

- **Reliability** — every finding about missing fault connectors, silent failures, or unrouted exceptions. Without these, the Flow is a reliability hazard regardless of happy-path correctness.
- **Scalability** — every finding about bulk-safety (per-interview SOQL/DML, invocable Apex list-safety, cross-object fan-out). Scalability breaks show up first as bulk failures.
- **Operational Excellence** — every finding about error-message design, logging discipline, admin-observable notifications, FlowInterviewLog configuration. OpsEx breaks show up as "we didn't know it was failing."

Use the pillar tags in Process Observations and when routing findings to owners — Reliability findings go to the Flow architect; OpsEx findings go to the admin team; Scalability findings often need both plus data-load owners.

## Fault Review Checklist

- [ ] Every fallible element has a fault path
- [ ] `$Flow.FaultMessage` is captured for logging or admin diagnostics
- [ ] End-user messages do not expose raw platform errors
- [ ] Record-triggered paths are reviewed for data-load volume (SOQL + DML math per interview × expected cardinality)
- [ ] Subflows and invocable Apex fail in an intentional, observable way
- [ ] Fault-email recipient is configured at org level (Process Automation Settings)
- [ ] Error-log object exists or has an equivalent sink (custom notification, Chatter post)
- [ ] Retry logic (if present) retries at most once per element
- [ ] WAF pillar tagging complete: Reliability / Scalability / Operational Excellence findings are separated


## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org edition, relevant objects, and current configuration state
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Fault-Routing Patterns above
4. Validate — run the skill's checker script and verify against the Fault Review Checklist above
5. Document — record any deviations from the canonical patterns and update the template if needed

---

## Salesforce-Specific Gotchas

- **Missing fault connectors roll back more than one record**: In record-triggered automation, one unhandled error can fail the whole batch save. This is the highest-impact fault-handling gap.
- **`$Flow.FaultMessage` is for diagnostics, not polished UX**: Log it or email it, but do not dump it raw to business users.
- **Shared transactions still share limits**: Apex, Flow, and invocable actions can all consume the same governor budget. A Flow that works fine when triggered by UI edits may fail when triggered by a Bulk API load because Apex triggers on the same object consumed the SOQL budget first.
- **Screen flows and record-triggered flows need different failure design**: One is user-guided UX (must have a next step for the user); the other is transaction safety (must not roll back good records).
- **Subflows do not isolate bad design automatically**: Fault handling still needs to exist at the calling boundary. A subflow's fault connector handles failures THROWN by the subflow; it does not retroactively fix a parent Flow missing its own fault routing.
- **Fault connectors on non-DML elements are easy to forget**: `Assignment`, `Decision`, and `Loop` elements don't have fault connectors because they can't fail in the transactional sense — but the elements AROUND them (like the `Action` being assigned from) do.
- **Screen flow back-button can skip fault paths**: If a user clicks back from a screen AFTER a fault occurred, they can re-enter the flow with state that doesn't match the fault branch's assumptions. Test explicitly.
- **Error emails go to the Process Automation user**: If that user is inactive or reassigned, fault notifications disappear silently until discovered during an outage. Audit this annually.
- **Orchestration flows have their own fault semantics**: Stage-level faults in Orchestrator are handled by stage transitions, NOT fault connectors inside the invoked flows. Don't mix the paradigms.

## Proactive Triggers

Surface these WITHOUT being asked:

- **Any DML or action element with no fault connector** → Flag as Critical. This is an avoidable rollback risk.
- **Generic system error shown to users** → Flag as High. Replace it with a controlled message and a logged diagnostic path.
- **Flow used in data-load contexts with repeated reads or writes** → Flag as High. Bulk behavior must be reviewed before production use.
- **Apex action used with no evidence of list-safe design** → Flag as High. Invocable Apex can still fail at scale.
- **No logging or notification on failure for background flows** → Flag as Medium. Silent failures become support incidents.
- **Fault-email recipient is inactive or unset at org level** → Flag as High. Unhandled faults go to an unread mailbox.
- **Retry loop with no termination bound** → Flag as Critical. A retry-until-success loop inside a Flow is an infinite-loop risk masquerading as resilience.
- **Different elements route to the same fault tail without discriminating source** → Flag as Low. Not wrong, but it collapses diagnostics; recommend adding the source element name to the log record.

## Output Artifacts

| When you ask for... | You get... |
|---------------------|------------|
| Fault-handling review | Missing connectors, bulk risks, message design findings, WAF pillar tagging |
| New Flow pattern | Fault-routing structure + logging + user-facing guidance + bulk-safety math |
| Failure triage | Root cause + smallest safe Flow redesign + prevention recommendations |
| Org-level fault posture | Fault-email recipient check + error-log object inventory + FlowInterviewLog guidance |

## Related Skills

- **admin/flow-for-admins**: Use it for broader Flow type decisions and admin automation design.
- **flow/flow-bulkification**: Companion skill — fault handling and bulk-safety are deeply coupled; missing fault connectors make bulk failures rollback-the-batch failures.
- **flow/record-triggered-flow-patterns**: Record-triggered fault semantics differ from screen flows — read that skill for the record-triggered-specific concerns.
- **flow/scheduled-flows**: Scheduled flow faults route differently (no user is present); specialized handling required.
- **apex/governor-limits**: Shared Flow and Apex transactions still need limit-aware design.
- **apex/exception-handling-patterns**: For Apex invoked from Flows — failures in invocable Apex are where many Flow faults actually originate.
- **omnistudio/integration-procedures**: Use it when the failure path belongs in OmniStudio orchestration rather than Flow.
