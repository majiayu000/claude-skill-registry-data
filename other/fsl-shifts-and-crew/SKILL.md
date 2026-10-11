---
name: fsl-shifts-and-crew
description: "Use this skill to configure FSL Shifts, ShiftTemplates, ShiftPatterns, and Crew ServiceResources — covering availability windows layered on Operating Hours, bulk shift generation via ShiftPattern + ShiftPatternEntry, and the two Crew models (Static vs. Shell/Dynamic). NOT for individual resource scheduling, NOT for scheduling policy or work rule configuration, and NOT for FSL mobile app or time-sheet setup."
category: admin
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Operational Excellence
  - Reliability
triggers:
  - "workers not showing up as candidates when I schedule field service appointments by shift"
  - "how do I create repeating shift schedules for a large field workforce in Field Service"
  - "set up crew scheduling in FSL so appointments go to the whole crew not individual members"
  - "ShiftTemplate versus ShiftPattern — which one do I use for bulk shift creation"
  - "field service shift availability not reflecting operating hours correctly"
  - "how to configure static crew versus dynamic shell crew in Field Service Lightning"
  - "get candidates for field service returns no results even though technicians have shifts"
tags:
  - field-service
  - fsl
  - shifts
  - crew
  - shift-pattern
  - shift-template
  - operating-hours
  - scheduling
inputs:
  - "List of service resources (technicians, crews) who need availability windows defined"
  - "Operating Hours records already configured for the relevant service territories"
  - "Shift schedule: days of week, start/end times, rotation pattern, and horizon (how far out to generate)"
  - "Whether crews are Static (fixed membership, skills aggregate) or Shell/Dynamic (membership assigned later, capacity-driven)"
  - "Any ShiftTemplates already in use for individual shift prepopulation"
outputs:
  - "Shift records correctly linked to ServiceResource and Operating Hours"
  - "ShiftTemplate records for common shift definitions"
  - "ShiftPattern + ShiftPatternEntry records for bulk repeating schedule generation"
  - "Crew ServiceResource records with correct crew model (Static vs. Shell) and Crew Size if Shell"
  - "Validation checklist confirming candidate availability and crew appointment routing"
dependencies:
  - fsl-resource-management
  - fsl-service-territory-setup
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-10
---

# FSL Shifts and Crew

This skill activates when a practitioner needs to configure Shift-based availability for Field Service Lightning resources or set up Crew ServiceResources for group appointment scheduling. It covers the Shift data model (Shift, ShiftTemplate, ShiftPattern, ShiftPatternEntry), the relationship between Shifts and Operating Hours, and the two Crew models — Static and Shell/Dynamic — including how service appointments are routed to crews rather than individual technicians.

---

## Before Starting

Gather this context before working on anything in this domain:

- Confirm Field Service is enabled and that Operating Hours records exist for the relevant service territories. Shifts are layered on top of Operating Hours — a Shift outside the Operating Hours window will not make a technician available for scheduling.
- Identify whether the org already uses ShiftTemplates or ShiftPatterns. Creating duplicate patterns causes redundant shift records that bloat the availability calendar and slow the scheduling engine.
- Clarify the crew model required: Static crews aggregate skills from their permanent members; Shell/Dynamic crews use a Crew Size field for capacity and have membership assigned per job. The choice is irreversible on the ServiceResource record — ResourceType cannot be changed after creation.
- Understand that the Shift object governs **availability** (Is this resource available to be scheduled?), not **work assignment** (Has a service appointment been assigned to this resource?). Conflating the two causes the most common FSL configuration errors.
- Note the Salesforce scheduling engine limit of 20 candidates evaluated per search. Shift windows that are too narrow can cause otherwise-qualified resources to fall out of candidate results.

---

## Core Concepts

### Shifts Are Availability Records, Not Work Assignments

A `Shift` record defines a window of time during which a `ServiceResource` is available to be considered for scheduling. It does not mean an appointment has been assigned. The FSL scheduling engine (specifically the **Shift Get Candidates** operation, surfaced in the Dispatcher Console when shifts are enabled) queries Shift records to determine who is available during a time slot — a completely separate process from the **managed-package Get Candidates** operation, which evaluates work rules and scheduling policies against appointments.

Key fields on `Shift`:
- `ServiceResourceId` — the resource whose availability this shift defines
- `StartTime` / `EndTime` — the availability window; must fall within the resource's Operating Hours period
- `Status` — Tentative, Confirmed, or Canceled; only Confirmed shifts are counted as available by the scheduler
- `OperatingHoursId` — the Operating Hours record governing valid working windows for the territory

### ShiftTemplate and ShiftPattern for Bulk Creation

Manually creating individual Shift records for a large workforce is not scalable. Salesforce provides two abstractions:

**ShiftTemplate** — a named preset that prepopulates field values (start time, end time, duration, color label) for an individual shift. Used when a dispatcher manually creates shifts one at a time and wants consistent field defaults. A ShiftTemplate does not generate shifts automatically.

**ShiftPattern + ShiftPatternEntry** — the bulk generation mechanism. A `ShiftPattern` defines the container (name, time zone, pattern length in days). `ShiftPatternEntry` child records define each day's shift definition within the pattern (which day offset, start time, end time, shift type). When you apply a ShiftPattern to a resource or group of resources using the **Generate Shifts** action, FSL creates individual Shift records for the entire specified date horizon in bulk. This is the correct approach for large workforces and recurring schedules.

### Static Crews vs. Shell/Dynamic Crews

A `ServiceResource` with `ResourceType = Crew` represents a group of technicians that can be scheduled as a single unit. There are two models:

**Static Crew** — Members are added as `ServiceCrewMember` records with defined start and end dates. The crew's effective skills are the union of skills held by its active members. The scheduling engine evaluates skills at the crew level. Static crews are appropriate when team composition is fixed (e.g., a dedicated installation team).

**Shell (Dynamic) Crew** — The `ServiceResource` is created as a crew with a `CrewSize` field specifying capacity (number of people expected). Actual `ServiceCrewMember` records are assigned per job, after the service appointment is dispatched. The scheduling engine uses `CrewSize` for capacity evaluation, not individual member skills. Shell crews are appropriate for ad-hoc or pooled workforce models where crew composition varies by job.

**Critical routing behavior:** Service appointments scheduled to a Crew are linked to the `ServiceResource` record that represents the crew — not to individual crew members. Dispatchers see the appointment on the crew's Gantt row, not on individual member rows.

---

## Common Patterns

### Pattern 1: Bulk Shift Generation with ShiftPattern

**When to use:** Org has 20+ technicians with rotating or fixed weekly schedules that repeat over a multi-week horizon. Manual shift creation would take hours and be error-prone.

**How it works:**
1. Create one `ShiftPattern` record: set Name, TimeZone (must match the service territory's time zone), and `PatternLength` (e.g., 7 for a weekly pattern, 14 for a two-week rotation).
2. Create `ShiftPatternEntry` child records: one per unique shift slot in the pattern. Each entry specifies `DayOfPattern` (1–PatternLength), `StartTime`, `EndTime`, and optionally `ShiftType`.
3. Use the **Generate Shifts** action on a ServiceResource record (or via the Shifts tab in Setup), targeting the desired date range and referencing the ShiftPattern. FSL creates individual Shift records in bulk.
4. Confirm generated Shifts have `Status = Confirmed`. Shifts in Tentative status are not evaluated by the scheduling engine.

**Why not the alternative:** Creating shifts individually via ShiftTemplate alone does not automate the generation — ShiftTemplate only defaults field values when a dispatcher opens the new-shift form. For bulk creation, ShiftPattern is required.

### Pattern 2: Static Crew Configuration for Fixed Teams

**When to use:** A dedicated installation or repair crew with fixed members that operates as a unit, where the crew's combined skill set must meet appointment requirements.

**How it works:**
1. Create a `ServiceResource` with `ResourceType = Crew`.
2. Add `ServiceCrewMember` records for each member, linking their individual Technician-type `ServiceResource` records. Set `StartDate` and optionally `EndDate`.
3. Assign `ServiceResourceSkill` records to each member's ServiceResource (not directly to the Crew record). The scheduler aggregates skills from active members.
4. Create Shift records for the Crew `ServiceResource` (not for individual members) — the crew's availability window is what the scheduler queries.
5. Schedule service appointments to the Crew ServiceResource. The appointment appears on the crew's Dispatcher Console row.

**Why not the alternative:** Scheduling appointments to individual crew members instead of the Crew ServiceResource breaks the crew model — members' individual Gantt rows are not the authoritative scheduling surface for crew work. Appointment status and travel time calculations reference the Crew ServiceResource record.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Fixed team of 2–6 technicians always working together, with defined skills | Static Crew with ServiceCrewMember records and skill aggregation | Skills evaluated from members; Crew acts as single schedulable unit |
| Pooled workforce where crew composition varies per job | Shell/Dynamic Crew with CrewSize set to expected headcount | Membership assigned post-dispatch; capacity governed by CrewSize field |
| Recurring weekly shift schedule for many technicians | ShiftPattern + ShiftPatternEntry with Generate Shifts action | Bulk creation; avoids manual effort and ensures consistent Shift records |
| Single shift type used occasionally by dispatchers creating shifts ad hoc | ShiftTemplate for field defaults | Provides consistent prepopulation without automating generation |
| Shift-based scheduling not returning candidates | Verify Shift Status = Confirmed AND Shift falls within Operating Hours window | Only Confirmed shifts within Operating Hours are evaluated by scheduler |
| Scheduling appointments to a crew — members not seeing appointments | Ensure appointments are dispatched to Crew ServiceResource, not to individual members | Crew routing uses the Crew record, not member records |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner working on this task:

1. **Verify prerequisites** — Confirm Field Service is enabled, Operating Hours records exist for the relevant territories, and ServiceResource records are configured for all technicians and crews. The Shift object requires an active FSL license.
2. **Determine the shift generation approach** — For fewer than 10 resources with simple schedules, ShiftTemplates may suffice. For 10+ resources or repeating patterns, create a ShiftPattern + ShiftPatternEntries first before generating any individual Shift records.
3. **Create or identify ShiftPattern(s)** — Set pattern length, time zone (match territory), and one ShiftPatternEntry per shift slot in the cycle. Verify day offsets (1-based) cover all required working days.
4. **Generate Shifts in bulk** — Use the Generate Shifts action on each ServiceResource (or via the Shifts tab) specifying the date range and referencing the ShiftPattern. Confirm all generated shifts have `Status = Confirmed`.
5. **Configure Crew ServiceResource records** — For static crews, add ServiceCrewMember records with date ranges and ensure members have required ServiceResourceSkill records. For shell/dynamic crews, set CrewSize and leave membership to be assigned per job. Create Shift records for the Crew ServiceResource itself.
6. **Validate scheduling candidate results** — Use Shift Get Candidates in the Dispatcher Console to confirm resources surface as expected for a test appointment. Do not use the managed-package Get Candidates (work rule evaluation) to validate shift availability — these are separate operations.
7. **Review before go-live** — Run the skill-local checker script, confirm no Shifts are in Tentative status, confirm Operating Hours windows encompass Shift windows, and confirm Crew appointments route to the Crew ServiceResource record.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] All Shift records targeting production scheduling have `Status = Confirmed` (not Tentative or Canceled)
- [ ] Shift start/end times fall within the associated Operating Hours period — shifts outside Operating Hours are silently ignored
- [ ] ShiftPattern time zone matches the service territory's time zone
- [ ] Static Crew members have active ServiceCrewMember records with correct date ranges and required ServiceResourceSkill records
- [ ] Shell/Dynamic Crew has `CrewSize` populated; individual member assignments are deferred to post-dispatch
- [ ] Service appointments are dispatched to the Crew ServiceResource (crew row), not to individual member records
- [ ] Shift Get Candidates (availability check) validated separately from managed-package Get Candidates (work-rule check)

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **Shift Get Candidates is NOT the same as managed-package Get Candidates** — FSL has two separate "Get Candidates" operations. The Shift Get Candidates checks resource availability based on Shift records (is the resource free during this window?). The managed-package Get Candidates evaluates scheduling policies and work rules (is this resource qualified for this job?). Confusing them leads practitioners to diagnose availability problems using work-rule logs or vice versa — the root causes and resolution paths are entirely different.

2. **Tentative Shifts are silently ignored by the scheduler** — A Shift record with `Status = Tentative` does not make the resource available for scheduling. The scheduler only evaluates `Status = Confirmed` shifts. There is no error — the resource simply does not appear in candidate results. This is the most common cause of "technician missing from candidates" reports in shift-enabled orgs.

3. **Shifts must fall within Operating Hours — mismatches are silent** — If a Shift is created with times outside the Operating Hours window of the associated territory (e.g., Operating Hours ends at 17:00 but the Shift runs until 19:00), the out-of-window portion is silently ignored. The resource will not be available for appointments during the overflow period.

4. **Crew ServiceResource skills come from members (Static) not the Crew record itself** — For Static Crews, `ServiceResourceSkill` records must be attached to individual member ServiceResource records, not to the Crew ServiceResource. Attaching skills to the Crew record directly has no effect on scheduling candidate evaluation. Shell/Dynamic Crews bypass skill aggregation entirely and rely on CrewSize for capacity.

5. **ResourceType cannot be changed after ServiceResource creation** — Once a ServiceResource is saved with `ResourceType = Crew`, it cannot be changed to Technician (or vice versa). If the wrong type is selected, a new ServiceResource record must be created. This also means crew model choice (Static vs. Shell) locks in implicitly at creation time via the presence or absence of CrewSize and ServiceCrewMember strategy.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Shift records | Individual availability windows per ServiceResource; must be Status=Confirmed to be evaluated |
| ShiftTemplate records | Named presets for field-level defaults when creating shifts manually |
| ShiftPattern + ShiftPatternEntry records | Container and day-level definitions for bulk shift generation |
| Crew ServiceResource records | ServiceResource typed as Crew, either Static (with ServiceCrewMember records) or Shell (with CrewSize) |
| ServiceCrewMember records | Junction between Crew ServiceResource and Technician ServiceResource members for Static crews |
| Validation checklist | Confirmation that Shifts are Confirmed, within Operating Hours, and crew routing is correctly configured |

---

## Related Skills

- `fsl-resource-management` — ServiceResource object setup, skill and certification assignment, and capacity-based resource configuration that must exist before Shifts can be created
- `fsl-service-territory-setup` — Service territory and Operating Hours configuration that Shifts are layered on top of
- `fsl-scheduling-policies` — Scheduling policy and work rule configuration evaluated by managed-package Get Candidates (separate from Shift-based availability)
