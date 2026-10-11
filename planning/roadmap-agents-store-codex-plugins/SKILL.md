---
name: roadmap
description: 'Generate a Now / Next / Later roadmap view across cycles, modules, epics Arguments: <project> [--horizon <weeks>].'
---

# Roadmap

Produce a Now / Next / Later / Parked roadmap view for a project, aggregating active cycles, modules, epics, and milestones.

## Arguments

Format: `<project> [--horizon <weeks>]`

Parse from `"$ARGUMENTS"`. Default horizon: 12 weeks.

## Process

1. **Bootstrap connector** — consult `connector-bootstrap`. Probe for the Plane resource tools `project`, `cycle`, `module`, `workitem`, `workitem_type`, `milestone` and `release`. There are no epic tools: epics are work items of the type "Epic".
2. **Resolve project** — `project(action=list)` → `project_id`.
3. **Gather horizon data**:
   - `cycle(action=list, project_id, status=current)` and `status=upcoming` — current and next sprint
   - `module(action=list, project_id)` — active modules
   - epics: `workitem_type(action=resolve, project_id, name="Epic")` → `type_id`, then `workitem(action=list, project_id, pql='type = "<epic-type-id>" AND stateGroup IN openStates()')` — active epics
   - `milestone(action=list, project_id)` — upcoming milestones in the horizon
   - optional: `release(action=list)` — releases with status `unreleased` and their `release_date`
4. **Classify each item**:
   - **Now** — in the current sprint or module status `in-progress`
   - **Next** — in the next planned sprint or starting within 2 weeks
   - **Later** — within the horizon but not yet scheduled
   - **Parked** — explicitly deprioritized or blocked indefinitely
5. **Compute progress** for each module/epic — completion percentage, blockers, risk (see `epics-initiatives-milestones`).
6. **Render** as a markdown table grouped by horizon bucket, or offer to publish as a Plane page via `/publish-report roadmap`.

## Example

```
/roadmap "TaskFlow"
/roadmap "TaskFlow" --horizon 8
```

## Output Format

```
### Now
- **Billing v2** (module) — 65%, target Apr 30, 🟢
- **Login fixes** (cycle 14) — in progress

### Next
- **Multi-tenant support** (epic) — starts Sprint 16

### Later
- **Enterprise SSO** (epic) — scoping, target Q3
- **v2.0 Public Beta** (milestone) — Apr 30

### Parked
- **Mobile app** — revisit Q3
```