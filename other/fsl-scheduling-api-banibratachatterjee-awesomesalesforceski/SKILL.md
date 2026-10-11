---
name: fsl-scheduling-api
description: "Use this skill when implementing Apex code that calls the FSL scheduling Apex API: GetSlots, schedule(), GradeSlotsService, or OAAS optimization classes. Trigger keywords: AppointmentBookingService, ScheduleService.schedule, GetSlots, GradeSlotsService, OAAS, bulk scheduling, FSL optimization callout. NOT for admin-level scheduling policy configuration, scheduling rules UI setup, or the standard Book Appointment quick action without custom Apex."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Performance
  - Reliability
  - Security
triggers:
  - "How do I call FSL scheduling API from Apex to book appointments programmatically"
  - "GetSlots returns available time windows but I need to split across two transactions"
  - "FSL.ScheduleService.schedule bulk processing hitting callout limits in Apex"
  - "OAAS optimization not running after Enhanced Scheduling add-on enabled"
  - "GradeSlotsService ranking slots for custom booking UI in Apex"
tags:
  - fsl
  - field-service
  - scheduling
  - apex
  - fsl-scheduling-api
  - appointment-booking
inputs:
  - "ServiceAppointment Id(s) to schedule or get slots for"
  - "ServiceTerritory and resource availability context"
  - "Whether Enhanced Scheduling and Optimization (ESO) add-on is licensed"
  - "Apex transaction context (sync vs async, whether a prior callout was made)"
outputs:
  - "Apex implementation of FSL scheduling API calls with correct transaction boundaries"
  - "Pattern for splitting GetSlots + ArrivalWindow DML + schedule() across two transactions"
  - "Batch class implementation for bulk ServiceAppointment scheduling"
  - "OAAS configuration guidance and operation-type selection"
dependencies:
  - apex/fsl-apex-extensions
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-10
---

# FSL Scheduling API

This skill activates when an Apex developer needs to programmatically call the FSL scheduling Apex namespace — specifically `FSL.AppointmentBookingService.GetSlots()`, `FSL.ScheduleService.schedule()`, `FSL.GradeSlotsService`, or `FSL.OAAS` — to book, rank, or optimize service appointments. It handles the transaction boundary constraints, bulk patterns, and add-on licensing requirements that the standard documentation buries or omits.

---

## Before Starting

Gather this context before working on anything in this domain:

- Confirm whether the org has the Enhanced Scheduling and Optimization (ESO) add-on license. OAAS operations that use ESO require it. Without ESO, the legacy optimization engine is used and operation limits differ.
- Determine the Apex execution context. `FSL.AppointmentBookingService.GetSlots()` and `FSL.ScheduleService.schedule()` are callout-backed; they cannot be called in the same transaction as a DML statement that precedes them unless the DML comes first and the transaction is committed before the callout.
- Know whether you are scheduling one appointment (sync) or many (bulk). Bulk requires a Batch Apex class with `Database.executeBatch(job, 1)` — batch size 1 is mandatory because each FSL scheduling call is itself a callout.
- Identify what "scheduling" means in your context: slot retrieval only (GetSlots), hard assignment (schedule()), slot ranking for a custom UI (GradeSlotsService), or background optimization (OAAS).

---

## Core Concepts

### AppointmentBookingService — Slot Retrieval

`FSL.AppointmentBookingService.GetSlots(saId, policyId, schedulingPolicyId)` returns a `List<FSL.Scheduling.TimeSlot>` representing available booking windows for a ServiceAppointment. Each TimeSlot includes start/end times and a list of candidate resources.

**Critical constraint:** GetSlots is a callout. After calling GetSlots, you cannot perform DML in the same transaction. The common pattern — call GetSlots, pick a slot, update `ArrivalWindowStart`/`ArrivalWindowEnd` on the SA, then call `schedule()` — requires two separate transactions:
- **Transaction 1:** Call GetSlots, return slot data to the caller (LWC, Flow, or async context)
- **Transaction 2:** Update the SA's ArrivalWindow fields (DML), then call schedule()

Attempting to do all three in one transaction throws a `System.CalloutException: You have uncommitted work pending`.

### ScheduleService — Hard Assignment

`FSL.ScheduleService.schedule(saId, schedulingPolicyId)` assigns a ServiceResource to the ServiceAppointment based on the scheduling policy. It returns an `FSL.ScheduleResult` containing the assigned resource, territory, and scheduled start/end time.

Unlike GetSlots, schedule() both calls out and commits scheduling data — it does not require a separate DML commit after it runs. However, it must be called after any preceding DML is committed (i.e., in a fresh transaction with no prior DML in scope).

### GradeSlotsService — Slot Ranking

`FSL.GradeSlotsService.GradeSlots(saId, slots, schedulingPolicyId)` accepts a list of TimeSlots (from GetSlots) and returns them scored by the scheduling policy's optimization criteria. Use this when building a custom booking UI where customers or dispatchers choose from ranked options rather than having the system auto-assign.

### OAAS — Optimization as a Service

`FSL.OAAS` exposes four optimization operations:
- **Global:** Batch optimization over a 1–7 day horizon. Hard timeout of 2 hours.
- **In-Day:** Re-optimizes same-day disruptions.
- **Resource Schedule:** Optimizes a single resource's schedule.
- **Reshuffle:** Reassigns pinned appointments to fill gaps.

OAAS operations are asynchronous — they submit an optimization job and return immediately. ESO (Enhanced Scheduling and Optimization) is a newer Hyperforce-backed engine with higher throughput and work chain support. When ESO is enabled for a territory, that territory uses ESO; there is no automatic fallback to the legacy engine if ESO encounters an error.

---

## Common Patterns

### Two-Transaction Booking Flow

**When to use:** Any time you need to get slots, let a user or automated logic pick one, then hard-assign the resource.

**How it works:**
1. In a first Apex transaction (e.g., an `@AuraEnabled` method or Queueable), call `FSL.AppointmentBookingService.GetSlots(saId, ...)`. Return the slot list to the caller.
2. Store the chosen slot data (start/end, resourceId, territoryId) in a temporary custom object or pass back to the next Apex call.
3. In a second transaction, update `ServiceAppointment.ArrivalWindowStart`/`ArrivalWindowEnd` with DML, then call `FSL.ScheduleService.schedule(saId, ...)`.

**Why not one transaction:** FSL scheduling calls are HTTP callouts to the optimization microservice. Uncommitted DML before a callout throws a `CalloutException`.

```apex
// Transaction 1 — slot retrieval (Queueable or @AuraEnabled)
List<FSL.Scheduling.TimeSlot> slots = 
    FSL.AppointmentBookingService.GetSlots(saId, null, schedulingPolicyId);
// Return to LWC or store in intermediate object

// Transaction 2 — assignment (separate @AuraEnabled or Queueable)
ServiceAppointment sa = [SELECT Id FROM ServiceAppointment WHERE Id = :saId];
sa.ArrivalWindowStart = chosenSlot.startTime;
sa.ArrivalWindowEnd = chosenSlot.endTime;
update sa; // DML first, no prior callout in this transaction
FSL.ScheduleService.schedule(saId, schedulingPolicyId);
```

### Bulk Scheduling via Batch Apex

**When to use:** Scheduling more than one ServiceAppointment at a time from Apex (e.g., post-migration bulk assignment, nightly scheduling run).

**How it works:** Implement `Database.Batchable<SObject>` and set batch size to exactly 1. Each execute() call handles one SA and makes one FSL scheduling callout.

```apex
global class BulkFslScheduler implements Database.Batchable<SObject>, Database.AllowsCallouts {
    global Database.QueryLocator start(Database.BatchableContext bc) {
        return Database.getQueryLocator(
            'SELECT Id FROM ServiceAppointment WHERE Status = \'None\''
        );
    }
    global void execute(Database.BatchableContext bc, List<SObject> scope) {
        ServiceAppointment sa = (ServiceAppointment)scope[0];
        try {
            FSL.ScheduleService.schedule(sa.Id, SCHEDULING_POLICY_ID);
        } catch (Exception e) {
            // log and continue
        }
    }
    global void finish(Database.BatchableContext bc) {}
}
// Call with: Database.executeBatch(new BulkFslScheduler(), 1);
```

**Why batch size 1:** The Apex callout limit is 100 callouts per transaction. More importantly, FSL scheduling calls are long-running HTTP requests — running more than one per execute() risks timeouts and partial failures with no rollback.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| User picks from a list of time windows | GetSlots → GradeSlots → display → schedule() in two transactions | GradeSlots ranks windows by policy score; user sees best options first |
| Fully automated assignment, one SA | FSL.ScheduleService.schedule() in a Queueable with no prior DML | Cleanest async path, avoids callout constraint |
| Fully automated assignment, many SAs | Batch Apex, size 1, AllowsCallouts | Only supported bulk pattern for FSL scheduling callouts |
| Background re-optimization of a territory | FSL.OAAS with Global or In-Day operation | OAAS runs asynchronously and handles constraint-solving at scale |
| Custom booking UI with ranked slots | GetSlots → GradeSlots → return to LWC | GradeSlots assigns scores; LWC displays ranked options |
| ESO licensed, territory enrolled | Use standard schedule() or OAAS; ESO is transparent to API caller | No API change needed — ESO activates per-territory in Setup |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner working on this task:

1. **Confirm licensing and ESO status** — Verify whether the org has the Field Service Scheduling optimization add-on and whether ESO is enabled per territory in Setup > Field Service > Enhanced Scheduling. Mismatched assumptions cause silent OAAS failures.
2. **Identify transaction context** — Determine whether the call originates from a trigger (avoid — no callouts in triggers), a synchronous Apex controller (@AuraEnabled), a Queueable, or a Batch class. Plan transaction boundaries before writing any code.
3. **Split GetSlots and schedule() across two transactions** — If the flow requires slot retrieval followed by user selection followed by assignment, implement the split explicitly. Pass slot data via a custom object or back through the LWC component.
4. **Implement bulk patterns with Batch Apex, size 1** — If scheduling more than one SA, use `Database.executeBatch(new BulkFslScheduler(), 1)`. Never loop `schedule()` inside a single transaction or standard batch execute() with size > 1.
5. **Handle OAAS operations asynchronously** — Call `FSL.OAAS` methods from a Queueable or scheduled job. Confirm the operation type (Global/In-Day/Resource/Reshuffle) matches the optimization window and scope.
6. **Add error handling for scheduling failures** — `schedule()` can return null or throw if no resource is available. Always check the return value and log failures without rethrowing to avoid blocking the batch.
7. **Validate in a sandbox with real scheduling policy data** — FSL scheduling calls depend on scheduling policies, resources, territories, and operating hours being correctly configured. Unit tests with mocked return values will pass but integration tests against real FSL config are mandatory.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] No DML statements precede FSL scheduling callouts in the same transaction
- [ ] Bulk scheduling uses Batch Apex with `executeBatch(job, 1)`
- [ ] OAAS calls originate from async context (Queueable or Scheduled)
- [ ] ESO licensing and per-territory enrollment confirmed before OAAS design
- [ ] Error handling checks `ScheduleResult` for null and logs FSL failures without rethrowing
- [ ] Transaction 2 in two-transaction flow performs DML before calling schedule()
- [ ] Integration tested against real scheduling policy and territory setup in sandbox

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **GetSlots → ArrivalWindow DML → schedule() must span two transactions** — Attempting this in one transaction throws `System.CalloutException: You have uncommitted work pending`. This is the most common FSL scheduling Apex bug and the official docs do not call it out explicitly.
2. **Batch size must be exactly 1 for bulk scheduling** — Using a batch size > 1 with FSL callouts risks `System.LimitException: Too many callouts` and partial failure with no automatic rollback. Always `executeBatch(job, 1)`.
3. **OAAS has a 2-hour hard timeout for Global optimization** — Jobs submitted past the 2-hour window are cancelled silently. Monitor FSL optimization job records to detect incomplete runs.
4. **ESO has no automatic fallback to legacy engine** — If ESO is enabled for a territory and the ESO service is unavailable, optimization fails for that territory. There is no automatic downgrade to the classic scheduling engine.
5. **schedule() returns null when no resource is available** — Do not assume a non-null return. Null means the SA was not scheduled. Log and handle gracefully.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Two-transaction booking Apex pattern | Apex classes implementing slot retrieval and hard assignment across two separate transactions |
| BulkFslScheduler batch class | Batch Apex implementation for scheduling multiple SAs with callout isolation |
| OAAS operation invocation snippet | Queueable-based OAAS call with correct operation type selection |

---

## Related Skills

- apex/fsl-apex-extensions — Broader FSL Apex namespace coverage including trigger disabling, custom actions, and FSL SDK patterns
- architect/fsl-optimization-architecture — Architecture-level decisions on optimization mode selection, territory sizing, and ESO adoption
