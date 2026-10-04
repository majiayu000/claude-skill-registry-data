---
name: fault-handling
description: "Use when designing, reviewing, or troubleshooting Salesforce Flow fault handling, error logging, and bulk-safe automation paths. Triggers: 'fault connector', '$Flow.FaultMessage', 'flow failed', 'record-triggered flow rollback', 'screen flow error', 'Custom Error element', 'Roll Back Records', 'faultConnector', 'flow error email recipient', 'FlowTest HasError'. NOT for diagnosing a fault email you already got — use flow/flow-runtime-error-diagnosis. NOT for Apex exception handling — use apex/exception-handling."
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
  - "fault path subflow"
  - "fault path in flow"
  - "fault path connector"
  - "subflow fault handling"
  - "add a fault path to every element in a flow"
  - "block a record save from a flow with a custom error"
  - "log flow errors to a custom object"
  - "roll back records in a screen flow after an error"
  - "test a flow fault path with a flow test"
  - "handle a subflow failure in the parent flow"
  - "stop one bad record from rolling back the whole flow batch"
  - "find out who receives flow error emails"
inputs: ["flow type", "failure points", "user impact"]
outputs: ["fault handling review", "error path recommendations", "bulk safety findings"]
dependencies: []
version: 2.1.0
author: Pranav Nagrecha
updated: 2026-09-05
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
- Who receives this org's flow error emails today? The default recipient is the user who last modified the flow, not a monitored mailbox (`references/gotchas.md` #6).

## Questions to Ask Before Configuring

Ask these before drawing a single connector. Each one decides a design that cannot be
retrofitted cheaply, and each maps to a documented platform behaviour in
`references/gotchas.md`.

| Ask | Why it matters | What a good answer adds |
|---|---|---|
| "Which flow type is this — screen, autolaunched, record-triggered before-save or after-save, or orchestration?" | Decides which fault mechanisms exist at all: Roll Back Records is screen-flow-only, Subflow has no fault connector, an orchestration stage's fault connector is inert (gotchas 1, 2, 3) | The element list you are allowed to use, before you design against one that isn't there |
| "When this element fails, should the triggering save survive or be blocked?" | Separates two opposite designs: a fault path that logs and lets the save stand, against a Custom Error element that rolls the change back (gotcha 9) | Which of the two you are building, decided by the business rather than by whichever element the builder reached for |
| "Where does the diagnostic go, and who reads it tomorrow morning?" | `FlowInterviewLog` covers screen flows only, so background flows leave no platform-side trace at all (gotcha 7) | The log object or event, its retention, and a named owner |
| "Who receives this org's flow error emails right now?" | The default recipient is the user who last modified the flow — usually whoever did the last release (gotcha 6) | Either a Setup change to a distribution list, or a written decision to accept the default |
| "If the notification is the last thing left standing, does it survive the rollback?" | Email is post-commit work; a platform event survives only when its `publishBehavior` is `PublishImmediately`, which is set on the event definition and invisible in the flow (gotcha 5) | The `publishBehavior` value on the alert event, checked rather than assumed |
| "Does anything on the fault path itself write records?" | A fault path is made of the same fallible elements as the happy path, and a governor limit that is already exhausted does not refill for the error handler (gotcha 4) | A nested fault path on the log write, or a platform-event tail behind it |
| "What calls this flow, and what else runs in the same save?" | The 100-SOQL / 150-DML budget is transaction-wide, and an invocable action must return outputs matching its inputs in size and order (gotchas 11, 12) | The per-interview arithmetic times the expected batch size, and the invocable contract in writing |

What a proper fault design adds over "just adding fault connectors": the failure is
attributable to a named element, the diagnostic survives the rollback that caused it, the
person who can fix it is actually told, and the fault branch is covered by a test rather
than by the next production incident.

---

## How This Skill Works

### Mode 1: Build from Scratch

For a new Flow that must fail predictably from day one.

1. **Inventory fallible elements before the happy path.** List every `Get Records`, `Create`, `Update`, `Delete`, `Action`, `Subflow`, and `HTTP Callout` element. Each is a potential fault source; each needs a routing decision.
2. **Classify failure severity per element.** Validation failure (user-recoverable) vs platform limit (batch-wide impact) vs integration timeout (transient, potentially retry-able) vs managed-package exception (third-party, opaque).
3. **Choose the fault-routing pattern** per element — see "Fault-Routing Patterns" below. Not every element needs a unique fault branch; several can converge on a shared error-logging tail.
4. **Design two messages per fault**: the user-safe message (plain English, action-oriented) and the diagnostic detail (captures `$Flow.FaultMessage`, element name, record id, user id).
5. **Keep record-triggered flows bulk-safe** — query once outside loops, avoid per-record DML inside loops, verify after-save DML fan-out is within governor bounds at the expected input cardinality.
6. **Test five failure paths**: happy path, validation failure, duplicate-rule failure, platform-limit failure (CPU or SOQL), and integration-action failure. Unit-test each with a controlled input.
7. **Wire observability**: the error-log object, a notification, and — for background flows — something that outlives a rollback. Do not plan to read `FlowInterviewLog`: it and `FlowInterviewLogEntry` are defined as logs of a *screen flow* interview and carry no fault message (`references/gotchas.md` #7). Whatever your fault path writes is the only trace an autolaunched or record-triggered flow leaves.

### Mode 2: Review Existing

For auditing a Flow that may already be in production.

1. **Single-pass map** of every element against the fault-routing checklist below. Even one missing connector on a fallible element is a P0 finding.
2. **Verify user-facing messages are plain English.** Any message containing `$Flow.FaultMessage` raw, `System.` tokens, or HTML artifacts is a UX failure.
3. **Confirm diagnostic detail is logged separately.** The raw `$Flow.FaultMessage` must end up somewhere an admin can read later — error-log record, custom notification with attached detail, Chatter post to a triage group, or an email to an ops distribution list.
4. **Review after-save flows for DML fan-out.** Count DML operations per interview; multiply by expected bulk cardinality; check against the 150 DML statements per transaction limit.
5. **Confirm subflows and invocable Apex fail observably.** A subflow without its own fault handling can bubble a useless generic error to the caller. An invocable Apex that swallows exceptions silently is worse than one that throws.
6. **Check the flow-error-email recipient at org level.** Process Automation Settings > *Send Process or Flow Error Email to*. Left at its default, error emails go to the user who last modified the flow — after a release, that is whoever did the deploy (`references/gotchas.md` #6).
7. **Flag any Flow that can fail silently.** Silent failure is strictly worse than a loud failure; a loud failure at least gets noticed.

### Mode 3: Troubleshoot

For a Flow that is already failing.

1. **Read the fault message from the flow error email, or from whatever the fault path logged.** That is the ground-truth error; everything else is interpretation. For a screen flow, `FlowInterviewLogEntry` also tells you which element ran last, though not why it failed.
2. **Identify the failing element** (name and type). The error email includes the element name — use it.
3. **Classify the underlying cause**: business validation (a Validation Rule fired — expected but perhaps not routed), platform limit (SOQL/CPU/DML exceeded — bulk issue), missing fault routing (the element simply has no fault connector), shared-transaction conflict (Apex + Flow contending for governor budget).
4. **Check whether the Flow is invoked in a shared transaction.** Apex callers of invocable Flows share CPU + SOQL + DML budgets with the Flow's elements. One element's exhaustion can be another caller's fault.
5. **Add or repair the fault path BEFORE attempting any other optimization.** Without fault routing, every future iteration is blind.
6. **If the failure is at scale**, profile a single successful interview first with a debug log and multiply. Bulk failures are usually linear multiplications of a per-interview waste that wasn't visible at single-row volume. See `flow/flow-debugging` for the log setup and `flow/flow-bulkification` for the arithmetic.

## Fault-Routing Patterns

Four canonical patterns. Combine them — most production Flows use a mix. Each one is the
declarative shape of `templates/flow/FaultPath_Template.md`; `references/metadata-examples.md`
is the same shape as deployable `*.flow-meta.xml`, with the template's four numbered steps
mapping to `Capture_*` → `Log_*` → `Notify_*` / `Show_*` → End.

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
                  ├── Yes → [HTTP Action retry]
                  │           ├── Success → [continue]
                  │           └── Fault   → [log + notify + end]
                  └── No  → [log + notify + end]  // 4xx errors are not retried
```

Retry once, immediately. Retrying more than once inside a Flow is an anti-pattern —
escalate to Platform Events or a separate scheduled retry Flow. UNVERIFIED (2026-09-05):
there is no documented in-transaction delay element for autolaunched flows in
`api_meta.txt`; a `FlowWait` pauses the interview across a transaction boundary rather
than sleeping inside one, so do not design a "wait 30 seconds and retry" step. For a
Flow **local action** (an LWC running client-side) the guide does give a number: requests
time out after 120 seconds by default, and the timeout takes the fault connector
(`lwc_guide.txt` L8863).

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

Caution: this pattern only works if the individual element is INSIDE a loop. Record-triggered
flows without an explicit loop run one interview per record, and all of those interviews
share one save transaction that commits at step 19 of the order of execution
(`apexdev.txt` L15478). UNVERIFIED (2026-09-05): none of the fetched guides state whether
one interview ending on an unhandled fault aborts the sibling interviews in the same
save — treat "the other records will be fine" as an assumption to test in a sandbox with a
partial-success load, not as platform behaviour.

### Pattern D: Explicit termination

For critical-path flows where partial success is worse than total failure.

```text
[DML or Action]
    └── Fault → [Assignment: diagnosticDetail = {!$Flow.FaultMessage}]
                → [Create Records: Application_Log__c (if possible — but this may roll back too)]
                → [Create Records: Error_Event__e]   // publishBehavior = PublishImmediately
                → [End — DO NOT suppress the error]
```

In Pattern D the Flow's fault path ends WITHOUT suppressing the failure, so the transaction
still rolls back. That is the point — this is the right pattern for "order placement
failed", where partial data is worse than none. It is also why the notification is a
platform event rather than an email alert: sending email is post-commit work at step 20 of
the order of execution, after the commit at step 19 (`apexdev.txt` L15478–L15487), so a
rolled-back transaction never sends it. The `Application_Log__c` write is best-effort for
the same reason; the event is the layer that survives, and only when the event definition
declares `PublishImmediately` (`references/gotchas.md` #5).

## Flow Fault Handling Rules

### Elements That Must Be Treated as Fallible

| Element Type | Typical Failure Modes | Required Fault Routing |
|--------------|-----------------------|------------------------|
| Get Records | Query limit, unexpected empty result assumptions, too-many-rows | Pattern A or C; assume zero rows + handle "not found" case explicitly |
| Create/Update/Delete | Validation rule, duplicate rule, required field, record lock, FLS denial | Pattern A (user-initiated) or C (bulk) |
| Subflow | Downstream failure propagates up; managed-package subflows are opaque | **No fault connector exists on `FlowSubflow`** — handle it inside the child and return an outcome variable the parent branches on (`references/gotchas.md` #1) |
| Apex or invocable action | Thrown `AuraHandledException`, unhandled business error, governor exhaustion | Pattern A; the invocable Apex itself should honor `with sharing` and FLS |
| HTTP action / external step | Timeout, auth failure, 4xx/5xx response, rate-limit. The documented 120-second default applies to Flow **local actions** (`lwc_guide.txt` L8863); UNVERIFIED (2026-09-05) for HTTP Callout and External Service actions | Pattern B for 5xx/timeout; Pattern A or D for 4xx |
| Email action | No active recipient, template reference invalid, org-level send-limit exhausted | Pattern A — but NOT Pattern D for notification paths (losing the notification is worse than a partial send) |
| Send Custom Notification | Notification Type not active, recipient reference invalid | Pattern A; fall back to email or log-only |
| Platform-event subscribe | Delivery miss, replay buffer expiry, subscriber session timeout | Requires out-of-band monitoring; not a fault-connector concern at the Flow level |
| Pause (Wait) | Any wait event failing | `FlowWait` does carry a `faultConnector`, and "if any of the wait events fail, the flow takes the fault connector" (`api_meta.txt` L72993) — easy to miss because it is not a DML element |

### Minimum Fault Pattern

Every fallible element must route to:

1. A user-safe message or business-logic branch (Pattern A / C) OR an explicit termination decision (Pattern D).
2. A diagnostic detail capture using `$Flow.FaultMessage` — NEVER discarded.
3. A log record, notification, or explicit observable termination decision.

For screen flows, the user must see a clear next step. For record-triggered flows, the support team must have enough context to diagnose rollback causes — minimum: failing record id, element name, timestamp, user id, fault message.

Two elements that look like fault handling and are not: **Subflow** has no fault connector
in the schema at all, and an **orchestration stage's** fault connector is documented as
"Not used." Both are covered in `references/gotchas.md` #1 and #2; both produce advice that
an admin cannot follow and XML that does not deploy.

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

### Risk 3: Invocable Apex whose outputs do not correspond to its inputs

The old framing of this risk — "the invocable takes a single input, so it fires once per
interview" — describes a method that does not compile. An invocable method's one input
parameter "must be… a list of a primitive data type… a list of an sObject type… a list of
the generic sObject type… a list of a user-defined type" (`apexdev.txt` L5432–L5438).
Lists are mandatory, so Flow always aggregates.

The real hazard is correspondence. "For a correct bulkification implementation, the Inputs
and Outputs must match on both the size and the order… the i-th Output entry must
correspond to the i-th Input entry. Matching entries are required for data correctness
when your action is in bulkified execution, such as when an apex action is used in a
record trigger flow" (`apexdev.txt` L5456–L5459).

**Safer pattern:** an invocable that filters or short-circuits must still return one result
per input, in order, with a per-entry status field. An action that returns a shorter list
hands interview *n* the result belonging to interview *n+k* — silent data corruption that
no fault connector catches, because nothing threw. See `apex/exception-handling` for the
class-side shape.

### Bulk Safety Checklist

- [ ] SOQL count per interview × bulk cardinality < 100
- [ ] DML count per interview × bulk cardinality < 150
- [ ] Invocable Apex returns one result per input, in input order (size and order both)
- [ ] Per-interview `Get Records` checked for cacheability via Platform Cache or Custom Metadata
- [ ] After-save DML fan-out counted and documented
- [ ] Missing fault connector on any DML element — treat as a bulk-safety issue, not just a fault-handling issue: one bad record rolls back the whole batch

## Fault Review Checklist

- [ ] Every fallible element has a fault path
- [ ] `$Flow.FaultMessage` is captured for logging or admin diagnostics
- [ ] End-user messages do not expose raw platform errors
- [ ] Record-triggered paths are reviewed for data-load volume (SOQL + DML math per interview × expected cardinality)
- [ ] Subflows and invocable Apex fail in an intentional, observable way
- [ ] *Send Process or Flow Error Email to* is set deliberately, not left on its default of "whoever last modified the flow"
- [ ] Error-log object exists, and the last hop of the fault path survives a rollback (platform event with `PublishImmediately`, not an email)
- [ ] Every DML element on a fault path has its own fault path or a platform-event tail
- [ ] `$Flow.FaultMessage` is captured in the first element of each fault branch, never read from a merged tail that is also reachable from a success path
- [ ] Each fault branch records which element failed, so a shared log tail stays diagnosable
- [ ] `scripts/check_flow_faults.py --manifest-dir <source tree>` exits 0
- [ ] Retry logic (if present) retries at most once per element
- [ ] WAF pillar tagging complete: Reliability / Scalability / Operational Excellence findings are separated

## Recommended Workflow

1. **Classify the flow, then read the fault-capability table** at the top of
   `references/metadata-examples.md`. It lists, per metadata type, whether a
   `faultConnector` exists at all. Do this before designing anything: Subflow has none,
   Roll Back Records is screen-flow-only, and an orchestration stage's is inert.
2. **Answer the seven questions above** and record the two decisions they force — block the
   save or let it stand, and what the last surviving hop of the fault path is.
3. **Route each fallible element** using Fault-Routing Patterns A–D, or a Custom Error
   element where the answer to question 2 was "block the save". Fill
   `templates/flow/FaultPath_Template.md` once per branch: capture `{!$Flow.FaultMessage}`
   in the branch's first element, set the failing element's name alongside it, write one
   log row, and give that write its own fault path or a platform-event tail.
4. **Write the metadata** against the three worked flows in
   `references/metadata-examples.md` — screen, autolaunched, and record-triggered before-save
   with a Custom Error — plus its `package.xml` and deploy order.
5. **Lint before deploying:**
   `python3 scripts/check_flow_faults.py --manifest-dir <source tree>`. It exits non-zero on
   a missing fault connector, a fault connector pointing at nothing, unguarded DML on a fault
   path, `$Flow.FaultMessage` read outside a fault branch, a rollback element outside a
   screen flow, and a Custom Error outside a record-triggered flow.
6. **Deploy as `Draft`, then force each failure in a sandbox** — a validation rule the update
   will trip, a deleted lookup target, a deactivated user — and confirm the log rows and the
   *Send Process or Flow Error Email to* recipient using § 7 of
   `references/metadata-examples.md`. A fault path that has never fired is a guess.
7. **Pin the fault branch with a `FlowTest`** for record-triggered and autolaunched flows
   (§ 4 of `references/metadata-examples.md`); screen flows are out of scope for `FlowTest`
   and need a scripted manual pass instead. See `flow/flow-testing`.

---

## Salesforce-Specific Gotchas

| Gotcha | Why it bites |
|---|---|
| Missing fault connectors roll back more than one record | In record-triggered automation, one unhandled error can fail the whole batch save. Highest-impact fault-handling gap. |
| `$Flow.FaultMessage` is for diagnostics, not polished UX | Log it or email it — do not dump it raw to business users. |
| Shared transactions still share limits | Apex, Flow, and invocable actions consume the same governor budget. A Flow that works on UI edits may fail under Bulk API load when same-object triggers consumed SOQL budget first. |
| Screen flows and record-triggered flows need different failure design | One is user-guided UX (must have a next step); the other is transaction safety (must not roll back good records). |
| Subflows have no fault connector at all | `FlowSubflow`'s field list contains no `faultConnector`. Handle failure inside the child and return an outcome the parent branches on. |
| Fault connectors on non-DML elements are easy to forget | `Assignment`, `Decision`, and `Loop` elements don't have fault connectors — but the `Action` elements around them do. |
| Screen flow back-button can skip fault paths | A user clicking back AFTER a fault can re-enter with state that doesn't match the fault branch's assumptions. Test explicitly. |
| Flow error emails default to whoever last saved the flow | Not to a monitored mailbox and not to the default workflow user. After a release that is usually the person who deployed. Set *Send Process or Flow Error Email to* deliberately. |
| `FlowInterviewLog` covers screen flows only | Background flows leave no platform-side interview trace, so the fault path's own log row is the only evidence. |
| A platform event only outlives a rollback when it says so | `publishBehavior` lives on the event definition, not the flow. `PublishAfterCommit` makes the alert silent in exactly the case it exists for. |
| Orchestration flows have their own fault semantics | Stage-level faults are handled by stage transitions, NOT fault connectors inside the invoked flows. Don't mix paradigms. |

## Proactive Triggers

Surface these WITHOUT being asked:

- **Any DML or action element with no fault connector** → Flag as Critical. This is an avoidable rollback risk.
- **Generic system error shown to users** → Flag as High. Replace it with a controlled message and a logged diagnostic path.
- **Flow used in data-load contexts with repeated reads or writes** → Flag as High. Bulk behavior must be reviewed before production use.
- **Apex action used with no evidence of list-safe design** → Flag as High. Invocable Apex can still fail at scale.
- **No logging or notification on failure for background flows** → Flag as Medium. Silent failures become support incidents.
- **Flow error email left on the default recipient** → Flag as High. It resolves to the last person who modified the flow, which after a release is the deployer, not an owner.
- **Fault path whose last hop is an email or a record write** → Flag as High. Both die with the transaction; only a `PublishImmediately` platform event survives it.
- **A fault connector on a Subflow element, or advice to add one** → Flag as Critical. The field does not exist; the XML will not deploy and the admin cannot follow the instruction.
- **Retry loop with no termination bound** → Flag as Critical. A retry-until-success loop inside a Flow is an infinite-loop risk masquerading as resilience.
- **Different elements route to the same fault tail without discriminating source** → Flag as Low. Not wrong, but it collapses diagnostics; recommend adding the source element name to the log record.

## Output Artifacts

| When you ask for... | You get... |
|---------------------|------------|
| Fault-handling review | Missing connectors, bulk risks, message design findings, WAF pillar tagging |
| New Flow pattern | Fault-routing structure + logging + user-facing guidance + bulk-safety math |
| Failure triage | Root cause + smallest safe Flow redesign + prevention recommendations |
| Org-level fault posture | *Send Process or Flow Error Email to* check + error-log object inventory + which flow types leave a platform-side trace and which do not |

## Reference Files

| File | Read it when |
|---|---|
| `references/metadata-examples.md` | You are writing or reviewing actual `*.flow-meta.xml`: which elements carry a `faultConnector` and which do not, three complete flows (screen with rollback, autolaunched with a logged and event-backed fault tail, record-triggered before-save with Custom Error), a `FlowTest` asserting the fault branch, `package.xml`, deploy order, and the log query plus Setup check that prove it fired |
| `references/gotchas.md` | The fault path exists and the error still vanished — rollback scope, notification survival, error-email recipients, `$Flow.FaultMessage` scope, elements that only look fault-capable |
| `references/examples.md` | You want the narrative: the routing patterns as diagrams, and the review that turned a flow with fault connectors on everything into a flow that actually keeps its errors |
| `references/llm-anti-patterns.md` | You are reviewing fault-handling advice or generated Flow XML produced by an AI assistant, or self-checking your own output |
| `references/well-architected.md` | You need the pillar framing, or the source and line behind any platform claim in this skill |
| `templates/flow-fault-design-template.md` | You are recording the design — fallible element inventory, failure outcome per element, diagnostic sink, release decision — for review |
| `templates/flow/FaultPath_Template.md` (repo-level) | You want the canonical four-step fault-path shape every pattern here fills in |
| `scripts/check_flow_faults.py` | Before every deploy. `--manifest-dir <source tree>`; exits non-zero on any finding |

---

## Related Skills

- **admin/flow-for-admins**: Use it for broader Flow type decisions and admin automation design.
- **flow/flow-bulkification**: Companion skill — fault handling and bulk-safety are deeply coupled; missing fault connectors make bulk failures rollback-the-batch failures.
- **flow/record-triggered-flow-patterns**: Record-triggered fault semantics differ from screen flows — read that skill for save-order, entry-criteria and run-order concerns, and for its metadata examples.
- **flow/subflows-and-reusability**: Where the failure has to be handled when a subflow is involved, since the calling element has no fault connector.
- **flow/flow-debugging**: For reading a failure that has already happened — debug logs, the interview view, and what the error email actually contains.
- **flow/flow-testing**: For `FlowTest` coverage beyond the single fault-branch assertion shown here.
- **flow/flow-runtime-error-diagnosis**: When you already have a fault email in hand and need the root cause rather than a design.
- **flow/scheduled-flows**: Scheduled flow faults route differently (no user is present); specialized handling required.
- **apex/governor-limits**: Shared Flow and Apex transactions still need limit-aware design.
- **apex/exception-handling**: For Apex invoked from Flows — failures in invocable Apex are where many Flow faults actually originate.
- **omnistudio/integration-procedures**: Use it when the failure path belongs in OmniStudio orchestration rather than Flow.
