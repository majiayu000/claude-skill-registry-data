---
name: fsl-apex-extensions
description: "Use when writing Apex that calls Field Service Lightning scheduling APIs — AppointmentBookingService, ScheduleService, GradeSlotsService, or OAAS — to book, schedule, grade, or optimize service appointments programmatically. Trigger keywords: FSL Apex namespace, GetSlots, schedule service appointment via code, appointment booking API, FSL optimization API. NOT for standard Apex patterns unrelated to FSL, admin-level scheduling policy configuration, or declarative FSL scheduling."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Reliability
  - Performance
  - Security
triggers:
  - "how do I programmatically book a field service appointment from Apex using available time slots"
  - "my Apex code calling FSL scheduling API throws uncommitted work pending exception"
  - "how to trigger FSL optimization or run OAAS from Apex code"
  - "ScheduleService.schedule() fails with missing ServiceTerritory or scheduling policy error"
  - "how to call AppointmentBookingService.GetSlots() and then schedule the appointment in the same transaction"
tags:
  - fsl
  - field-service
  - apex
  - scheduling
  - appointment-booking
  - optimization
  - fsl-namespace
inputs:
  - ServiceAppointment ID (with ServiceTerritory assigned)
  - Scheduling Policy record ID
  - Operating Hours record ID (for GetSlots)
  - ServiceResource ID (for ScheduleService.schedule)
  - Start and end datetime window for the scheduling call
  - Whether Enhanced Scheduling and Optimization add-on is enabled (for OAAS)
outputs:
  - Apex code pattern for booking appointments via GetSlots + schedule in separate transactions
  - Queueable or Batch class wrapping the scheduling API call to avoid callout-DML conflict
  - OAAS invocation pattern for triggering optimization runs
  - Review checklist confirming required fields, governor compliance, and license requirements
dependencies:
  - admin/fsl-scheduling-policies
  - admin/fsl-service-territory-setup
  - admin/fsl-service-resource-setup
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-10
---

# FSL Apex Extensions

This skill activates when a practitioner needs to write Apex that directly calls the `FSL` managed-package namespace to book, schedule, grade, or optimize Field Service Lightning service appointments. It covers the governor constraint that prevents mixing uncommitted DML with FSL scheduling calls, the transaction-splitting patterns required to work around it, and the additional requirements for the OAAS optimization API.

---

## Before Starting

Gather this context before working on anything in this domain:

- Confirm the FSL managed package is installed and the `FSL` namespace is resolvable in the target org. The classes live in the managed package, not the Salesforce core platform.
- Identify whether the ServiceAppointment has a `ServiceTerritory` assigned — `ScheduleService.schedule()` will throw a runtime exception without it.
- Confirm which scheduling policy record will be passed; it must exist as a `FSL__Scheduling_Policy__c` record in the org.
- Determine whether any DML has been executed earlier in the same transaction that will call `GetSlots()` or `schedule()`. If so, a transaction boundary is mandatory.
- For OAAS calls, confirm the org has the Enhanced Scheduling and Optimization add-on license — OAAS is not available on the base FSL license.

---

## Core Concepts

### FSL Apex Namespace Classes

The Field Service managed package exposes four primary Apex classes in the `FSL` namespace:

- **`FSL.AppointmentBookingService`** — provides `GetSlots(serviceAppointmentId, schedulingPolicyId, operatingHoursId)`, which returns `List<FSL.AppointmentBookingSlot>`. Each slot contains a `Interval_Start__c` and `Interval_End__c` datetime and a grade score.
- **`FSL.ScheduleService`** — provides `schedule(serviceAppointmentId, schedulingPolicyId, serviceResourceId, startDateTime, endDateTime)` to commit a specific time slot and resource assignment to the service appointment.
- **`FSL.GradeSlotsService`** — grades a provided list of time slots against the scheduling policy without returning new available windows. Used when the caller already has candidate slots and wants to rank them.
- **`FSL.OAAS`** (Optimization As A Service) — triggers asynchronous optimization runs: global, in-day, resource schedule, or reshuffle. Returns a job ID. Requires the Enhanced Scheduling and Optimization add-on.

### The Callout-DML Transaction Constraint

Both `FSL.AppointmentBookingService.GetSlots()` and `FSL.ScheduleService.schedule()` internally perform HTTP callouts to the FSL routing engine to calculate travel time (SLR — Simple Linear Routing — or P2P routing depending on configuration). Salesforce enforces a platform rule: **a callout cannot be made after uncommitted DML in the same transaction**. This produces the error:

> `System.CalloutException: You have uncommitted work pending. Please commit or rollback before calling out`

This is the most common production failure when integrating FSL scheduling into Apex flows. The trigger, flow-invoked action, or REST handler that inserts or updates records before calling GetSlots/schedule will hit this wall immediately.

### Transaction-Splitting Patterns

Because the callout constraint cannot be bypassed, the solution is always to **separate the DML transaction from the scheduling API transaction**:

1. **Queueable Apex** — insert/update the ServiceAppointment in the synchronous transaction, then enqueue a `Queueable` class that calls `GetSlots()` or `schedule()` in its own fresh transaction. The Queueable receives the record IDs as constructor parameters.
2. **`Database.Batchable` with `batchSize=1`** — a batch job with batch size set to 1 ensures each `execute()` call processes one ServiceAppointment in isolation, with no prior uncommitted DML. The `start()` method queries the appointments to schedule.
3. **`@future` method** — a static `@future(callout=true)` method can be called from a trigger or synchronous context and runs in a fresh transaction. Drawback: `@future` cannot be called from batch context and has tighter limits.

The Queueable pattern is the most flexible for interactive use; the Batch pattern is preferred for bulk scheduling runs.

### OAAS and License Requirements

`FSL.OAAS` methods (`FSL.OAAS.optimizeBySchedulingPolicy()`, `FSL.OAAS.inDay()`, etc.) trigger the FSL optimization engine asynchronously. The return value is a String job ID that can be polled. OAAS requires:

- The **Enhanced Scheduling and Optimization** add-on (a separate SKU from base FSL).
- A valid `FSL__Scheduling_Policy__c` record with optimization settings configured.
- ServiceTerritory in scope for the optimization run.

Calling OAAS without the add-on throws a managed-package exception at runtime — it does not fail gracefully.

---

## Common Patterns

### Pattern 1: Queueable Appointment Booking (GetSlots then Schedule)

**When to use:** A user action (screen flow, LWC, trigger) creates or updates a ServiceAppointment and immediately needs to book it into the first available slot.

**How it works:**

1. The synchronous transaction inserts/updates the `ServiceAppointment` and commits (transaction ends — DML is committed).
2. A Queueable is enqueued, receiving the ServiceAppointment ID, scheduling policy ID, and operating hours ID.
3. In the Queueable's `execute()` method, call `FSL.AppointmentBookingService.GetSlots()` — no prior DML in this transaction, so the internal callout succeeds.
4. Select the desired slot (e.g., highest grade or earliest start).
5. Call `FSL.ScheduleService.schedule()` with the selected slot's resource, start, and end datetimes.

**Why not the alternative:** Calling `GetSlots()` immediately after the `insert ServiceAppointment` statement in the same transaction raises `CalloutException: You have uncommitted work pending`.

### Pattern 2: Bulk Scheduling via Batch with batchSize=1

**When to use:** A nightly or on-demand job must schedule hundreds of unscheduled ServiceAppointments against the FSL engine without manual intervention.

**How it works:**

1. A `Database.Batchable<SObject>` queries all ServiceAppointments with status `None` (or a custom "Pending Scheduling" status).
2. The batch is invoked with `Database.executeBatch(new ScheduleBatch(), 1)` — batch size of 1 is mandatory.
3. Each `execute()` receives a single appointment. The execute scope has no prior uncommitted DML, so calling `FSL.ScheduleService.schedule()` directly is safe.
4. On failure, log the ServiceAppointment ID and error message; do not re-throw so the batch continues.

**Why batch size must be 1:** Each `execute()` call begins a fresh transaction, but if two appointments are in the same batch chunk, the first appointment's `schedule()` call commits travel-calculation state that conflicts with the second. Setting size to 1 guarantees a clean transaction per appointment.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Single appointment booked interactively (trigger, flow-invoked Apex) | Queueable | Clean transaction boundary; supports chaining; works from trigger and invocable contexts |
| Bulk scheduling of 50–500 appointments overnight | Batch with batchSize=1 | Governor-safe for large volumes; built-in retry on chunk failure |
| Need to show available slots to user before booking | GetSlots in Queueable, return via Platform Event or custom object | GetSlots callout cannot run synchronously in same DML transaction |
| Trigger optimization after manual schedule changes | FSL.OAAS | Purpose-built for optimization; returns job ID for monitoring |
| Single appointment, lightweight integration, no chaining needed | @future(callout=true) | Simplest pattern; acceptable when batch/Queueable overhead is undesirable and call is from synchronous non-batch context |
| Grade candidate slots already in hand | FSL.GradeSlotsService | Avoids a full GetSlots call when slot candidates are already known |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner working on this task:

1. **Verify prerequisites** — confirm FSL package is installed, the ServiceAppointment has a ServiceTerritory assigned, and a valid scheduling policy record exists. For OAAS, confirm the Enhanced Scheduling and Optimization add-on is present.
2. **Identify the transaction boundary** — determine where DML occurs relative to the planned FSL API call. If any insert/update/delete/upsert runs before the FSL call in the same transaction, a transaction-splitting pattern is required.
3. **Choose the splitting pattern** — use Queueable for interactive single-record scenarios; use Batch with batchSize=1 for bulk jobs; use `@future(callout=true)` for simple non-batch scenarios without chaining needs.
4. **Implement GetSlots (if booking)** — call `FSL.AppointmentBookingService.GetSlots(saId, policyId, ohId)` in the clean transaction. Null-check the returned list before proceeding — if no slots are available, the list is empty (not null, but may be empty).
5. **Select and confirm slot** — pick the slot based on business rules (grade, earliest time, resource preference). Call `FSL.ScheduleService.schedule()` with the chosen slot's resource ID, start, and end datetimes.
6. **Handle OAAS separately** — if triggering optimization, call the appropriate `FSL.OAAS` method in its own Queueable or invocable action, capture the returned job ID, and store it for monitoring or audit.
7. **Test governor compliance** — run unit tests with `@isTest` that mock the FSL callouts using `HttpCalloutMock` or verify that the Queueable/Batch pattern is invoked rather than the scheduling method being called directly in a DML-preceded transaction.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] ServiceAppointment has ServiceTerritory assigned before any schedule() call
- [ ] No uncommitted DML precedes FSL.AppointmentBookingService.GetSlots() or FSL.ScheduleService.schedule() in the same transaction
- [ ] Queueable, Batch (batchSize=1), or @future pattern is in place if a transaction boundary is needed
- [ ] Batch size is explicitly set to 1 when using Database.Batchable for FSL scheduling
- [ ] OAAS calls are gated on Enhanced Scheduling and Optimization add-on availability (or org type check)
- [ ] Empty slot list from GetSlots() is handled gracefully — no NullPointerException on slot selection
- [ ] Unit tests mock FSL callouts and verify the asynchronous dispatch path is exercised

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **Uncommitted DML before FSL callout** — `GetSlots()` and `schedule()` both make internal HTTP callouts for travel routing. Any uncommitted DML in the same transaction triggers `System.CalloutException: You have uncommitted work pending`. This is the #1 cause of FSL scheduling Apex failures.
2. **Missing ServiceTerritory on ServiceAppointment** — `ScheduleService.schedule()` requires a ServiceTerritory on the appointment. If the territory is null, the call throws a managed-package runtime exception, not a null pointer — the error message is not always obvious about the root cause.
3. **Batch size greater than 1 for FSL scheduling** — setting batchSize > 1 in a batch class that calls FSL APIs causes the second record's callout to fail with the uncommitted work error because the first record's scheduling call leaves uncommitted state in the chunk. Always use batchSize=1.
4. **OAAS requires add-on license** — `FSL.OAAS` throws a managed-package exception if the Enhanced Scheduling and Optimization add-on is not active. This is not a compile-time error; it fails silently or with an opaque exception at runtime in orgs without the add-on.
5. **GetSlots returns empty list, not null** — when no slots are available (e.g., no resources in territory, policy blocks all windows), `GetSlots()` returns an empty `List<FSL.AppointmentBookingSlot>` rather than null. Code that assumes a non-empty list without checking will throw `ListException: List index out of bounds: 0`.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Queueable Apex class | Transaction-safe wrapper for GetSlots + schedule — passes SA ID and policy ID as constructor parameters, calls FSL API in a clean transaction |
| Batch Apex class | Bulk scheduling batch with batchSize=1, queries unscheduled SAs and calls ScheduleService per record |
| OAAS invocation snippet | Apex that calls FSL.OAAS and captures the returned job ID for monitoring |
| Review checklist | Pre-deploy verification list covering transaction boundaries, required fields, and license requirements |

---

## Related Skills

- `admin/fsl-scheduling-policies` — scheduling policy configuration that feeds the policyId parameter into all FSL API calls
- `admin/fsl-service-territory-setup` — ServiceTerritory setup required before ScheduleService.schedule() can succeed
- `admin/fsl-service-resource-setup` — ServiceResource configuration required for the resourceId parameter
