---
name: sales-engagement-api
description: "Use when enrolling records in Sales Engagement cadences from Apex, logging call outcomes on cadence steps, customizing cadence step actions via Apex, or consuming cadence lifecycle events through Change Data Capture. Triggers: 'enroll lead in cadence', 'assignTargetToSalesCadence', 'ActionCadenceTracker', 'log call result cadence', 'Sales Engagement Apex'. NOT for building or administering cadence structures (steps, branches, variants) — cadence content must be authored in the Cadence Builder UI and cannot be created or mutated via API."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Reliability
  - Security
  - Scalability
triggers:
  - "how do I enroll a lead or contact in a Sales Engagement cadence from Apex"
  - "ActionCadenceTracker object — how to read or react to cadence state changes in Apex"
  - "log a call disposition or task outcome on a cadence step from code"
  - "Sales Engagement invocable action from Apex — assignTargetToSalesCadence"
  - "CDC on ActionCadence objects — async trigger for cadence events"
tags:
  - sales-engagement
  - high-velocity-sales
  - hvs
  - action-cadence
  - cadence-enrollment
  - invocable-action
  - cdc
inputs:
  - "target record ID (Lead, Contact, or Person Account) for enrollment"
  - "cadence name or ID to enroll the target into"
  - "assigned user ID (Sales Rep) who will work the cadence steps"
  - "whether call logging or step completion customization is needed"
outputs:
  - "Apex service class for cadence enrollment using the invocable action"
  - "CDC-based Async Apex Trigger pattern for reacting to ActionCadenceTracker changes"
  - "review findings on governor limits, duplicate enrollment guards, and error handling"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-06
---

# Sales Engagement API

Use this skill when programmatic Apex code needs to enroll records in Sales Engagement cadences, react to cadence lifecycle events, or log outcomes on cadence steps. The objective is reliable, bulkified enrollment that respects the platform's invocable action model and leverages Change Data Capture for event-driven reactions rather than unsupported triggers.

---

## Before Starting

- Confirm the org has an active Sales Engagement (formerly High Velocity Sales) license and that the Sales Engagement feature is enabled in Setup.
- Identify the target object type — enrollment supports Lead, Contact, and Person Account. Standard Account and custom objects are not supported targets for `assignTargetToSalesCadence` as of Spring '25.
- Determine whether the cadence already exists in the Cadence Builder UI. The cadence structure (steps, branches, email templates, call scripts) is entirely read-only via API. Apex cannot create or modify cadence content — that belongs in the UI.
- Clarify if the requirement is enrollment only, step-completion logging, real-time reaction to cadence state changes, or all three.
- Understand volume expectations. Invocable actions called from Apex count against DML and governor limits. Bulk enrollment via the action supports a list of inputs, which is critical for batch contexts.

---

## Core Concepts

### The `assignTargetToSalesCadence` Invocable Action Is the Only Enrollment API

Salesforce does not expose a direct DML-based way to create enrollment records. Cadence enrollment is performed by calling the `assignTargetToSalesCadence` invocable action using `Invocable.Action` in Apex or by invoking it from Flow. Attempting to insert `ActionCadenceTracker` or related objects directly via DML will result in errors. This pattern is intentional: the platform enforces enrollment rules (duplicate prevention, license checks, step scheduling) inside the action rather than exposing them to raw DML.

### The ActionCadence Object Family Is Read-Only via Apex DML

The `ActionCadence`, `ActionCadenceStep`, `ActionCadenceStepVariant`, and `ActionCadenceTracker` objects represent the cadence structure and enrollment state. They can be queried via SOQL, but DML mutations are restricted or unsupported except through the designated invocable actions. Do not attempt to `insert` or `update` these objects directly. The only mutation surface for enrollment is the invocable action; for step completion and call logging it is the designated `completeActionCadenceStep` action or task record updates.

### Triggers Are Not Supported on ActionCadence Objects — Use CDC

Standard Apex triggers cannot be placed on `ActionCadenceTracker`, `ActionCadenceStepTracker`, or related objects. Reacting to cadence state changes requires Change Data Capture (CDC). Enable CDC on the `ActionCadenceTracker` object in Setup, then author an Async Apex Trigger on the `ActionCadenceTrackerChangeEvent` channel. This is the officially supported pattern for event-driven reactions to enrollment lifecycle changes.

### Enrollment Respects Duplicate Guards at the Platform Level

The invocable action enforces that a target cannot be enrolled in the same cadence twice if an active enrollment already exists. The action returns output fields indicating success or failure. Production code must inspect these outputs per invocation. Swallowing action errors silently leaves the calling code unable to distinguish successful enrollments from duplicates or license errors.

---

## Common Patterns

### Bulk Cadence Enrollment Service

**When to use:** A batch process, trigger, or scheduled job needs to enroll many Leads or Contacts into a cadence at once.

**How it works:** Collect `Invocable.Action.Input` instances for each target, set the `sObjectName`, `targetId`, `cadenceName`, and `userId` parameters, then invoke the `assignTargetToSalesCadence` action as a bulk list. Inspect each `Invocable.Action.Result` for success and log or surface failures per record.

**Why not the alternative:** Calling the action one record at a time in a loop inflates Apex CPU time and may exceed governor limits on large sets. The list-based invocation is the bulk-safe pattern.

### CDC-Based Async Trigger for Enrollment Lifecycle Events

**When to use:** Downstream processes need to react when a target is enrolled, a step is completed, or a cadence run ends.

**How it works:** Enable `ActionCadenceTracker` CDC in Setup. Implement an Async Apex Trigger on `ActionCadenceTrackerChangeEvent`. Inside the trigger, read `EventBus.TriggerContext.currentResumeCheckpoint()` and process the `ChangeEventHeader` to determine the change type (`CREATE`, `UPDATE`, `DELETE`). Enqueue a Queueable for heavier work.

**Why not the alternative:** A synchronous Apex trigger on `ActionCadenceTracker` is not supported. Polling SOQL for state changes is fragile and wastes queries.

### Step Completion and Call Logging

**When to use:** A CTI integration or custom UI needs to record the outcome of a call step and advance the cadence.

**How it works:** Use the `completeActionCadenceStep` invocable action, passing the `ActionCadenceStepTrackerId` and outcome fields (call result, disposition). This advances the tracker to the next step. Alternatively, update the associated `Task` record's call result fields; the cadence engine reads those fields to determine step completion in call-step contexts.

**Why not the alternative:** Directly updating `ActionCadenceStepTracker` status fields via DML is not supported and will fail silently or throw errors.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Enroll leads from a batch job or trigger | `assignTargetToSalesCadence` invocable action, bulk list input | Only supported enrollment surface; list input keeps limits safe |
| React to enrollment or step completion | CDC on `ActionCadenceTrackerChangeEvent` + Async Apex Trigger | Triggers not supported on ActionCadence objects |
| Log call disposition on a cadence step | `completeActionCadenceStep` invocable action or Task update | DML on step tracker is not supported |
| Build or modify cadence structure via API | Not possible — redirect to Cadence Builder UI | Cadence content is read-only via API by design |
| Check whether a target is already enrolled | SOQL on `ActionCadenceTracker` where `State = 'Active'` | Query is supported; use to guard against duplicate enrollment attempts |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Confirm prerequisites — verify that the Sales Engagement license is active, the target cadence exists in the UI, and the target object type is Lead, Contact, or Person Account.
2. Query existing enrollment state — SOQL `ActionCadenceTracker` for active enrollments on the target records to prevent duplicate action calls and interpret likely results.
3. Build the enrollment service — implement a service class that constructs `Invocable.Action.Input` lists, calls `assignTargetToSalesCadence` in bulk, and inspects `Invocable.Action.Result` per record to capture errors.
4. Handle CDC for lifecycle reactions — if downstream automation is needed, enable CDC on `ActionCadenceTracker`, scaffold an Async Apex Trigger on `ActionCadenceTrackerChangeEvent`, and move heavy work to Queueable.
5. Implement step completion logging — if call results must be logged programmatically, use the `completeActionCadenceStep` invocable action or update the Task record associated with the step.
6. Test in a scratch org or sandbox with Sales Engagement enabled — confirm invocable action outputs, governor limit consumption, and CDC event delivery under bulk load.
7. Run the skill checker and validate the full package before committing.

---

## Review Checklist

- [ ] Enrollment is performed via `assignTargetToSalesCadence` invocable action, not DML on ActionCadence objects.
- [ ] Invocable action results are inspected per record and failures are surfaced or logged.
- [ ] A duplicate enrollment guard queries `ActionCadenceTracker` for active enrollments before calling the action.
- [ ] CDC is used for lifecycle reactions, not Apex triggers on ActionCadence objects.
- [ ] Step completion uses `completeActionCadenceStep` or Task field updates — not direct DML on `ActionCadenceStepTracker`.
- [ ] All action calls use list inputs to stay bulkification-safe.
- [ ] Tests use `@isTest` stubs or mock invocable action results since the action cannot fire in test contexts without the managed package.

---

## Salesforce-Specific Gotchas

1. **Invocable actions do not run in unit tests without the Sales Engagement package context** — tests that call `assignTargetToSalesCadence` via `Invocable.Action.invoke()` will return empty results or throw in a standard scratch org without the SE license provisioned. Use a wrapper interface to allow mocking in test context.
2. **ActionCadenceTracker CDC events can arrive out of order** — Async Apex Triggers process events in the order they are delivered by the event bus, which may not match the business order of step completions. Designs that require strict ordering must use the `ChangeEventHeader` sequence or query the tracker state rather than relying on event order.
3. **`assignTargetToSalesCadence` silently no-ops if the target is already in an active enrollment** — the action returns a result with `success = false` and an error code rather than throwing an exception. Callers that only check for exceptions will not detect duplicate enrollment failures.
4. **Cadence structure objects (`ActionCadence`, `ActionCadenceStep`) are accessible via SOQL but reflect the live state** — they do not represent a versioned snapshot. A cadence modified in the UI mid-run changes the SOQL results.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Enrollment service class | Apex service wrapping `assignTargetToSalesCadence` with bulk input construction and result inspection |
| Async Apex Trigger scaffold | CDC-based trigger on `ActionCadenceTrackerChangeEvent` with Queueable handoff |
| Duplicate guard SOQL | Query to detect active `ActionCadenceTracker` records before enrollment |
| Enrollment review findings | Assessment of DML patterns, result handling gaps, and CDC configuration state |

---

## Related Skills

- `apex/change-data-capture-apex` — use for deep CDC pattern design including resume checkpoints, chunking, and replay gaps when the CDC trigger is more complex than a thin enqueue.
- `apex/invocable-methods` — use when building or calling invocable actions for advanced input/output type design.
- `apex/async-apex` — use when the Queueable work spawned from the CDC trigger requires chaining, retry, or batch fallback patterns.
- `apex/governor-limits` — use when enrollment volume is high enough that invocable action call counts and DML governor consumption need modeling.
