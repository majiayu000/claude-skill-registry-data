---
name: burndown
description: 'Show sprint burndown and projected completion for the active cycle Arguments: <project> [--cycle <current|name>].'
---

# Burndown

Compute a burndown view for a sprint: ideal line, actual points remaining, and projected end state.

## Arguments

Format: `<project> [--cycle <current|name>]`

Parse from `"$ARGUMENTS"`. Default: current cycle.

## Process

1. **Bootstrap connector** — consult `connector-bootstrap`. Probe for the Plane resource tools `project`, `cycle`, `workitem`, `workitem_activity`.
2. **Resolve project and cycle** — `project(action=list)` → `cycle(action=list, project_id, status=current)` → active cycle (or the named one; `status=completed` for a finished sprint).
3. **Load cycle items** — `cycle(action=list_workitems, project_id, cycle_id, fields="id,name,point,estimate_point,state")`; for the item totals per state group in one call: `workitem(action=count, project_id, pql='cycle = "<cycle_id>"', group_by=state__group)`.
4. **Reconstruct daily points remaining** — for each day from `start_date` to today, sum points of items not in a completed state group as of that day. Use `workitem_activity(action=list, project_id, workitem_id)` (one call per completed item) to find the day each item moved to a completed state, or fall back to the current snapshot if activity data is unavailable. PQL cannot query history (no `wasEver` / `changedTo`), so the history needs the activity log.
   Points are `point`; if `point` is empty and the project has an estimate system (`project_estimate(action=retrieve, project_id)`), sum the `value` of each item's `estimate_point` instead (`project_estimate(action=list_points, project_id, estimate_id)` maps ids to values).
5. **Compute**:
   - `total_points` = sum of all cycle item points
   - `completed_points` = sum of items in completed state group
   - `remaining_points` = `total_points − completed_points`
   - `ideal_remaining(day)` = `total_points × (1 − day / total_days)`
   - `projected_end_points` = linear extrapolation from the last 3 days of actual burn
   - `on_track` = `projected_end_points ≤ 0`
6. **Present** — ASCII or markdown table with day, ideal, actual, delta. Highlight if the team is ahead/behind and by how much.
7. **Recommend** — if off track by > 20%, suggest scope reduction (see `sprint-planning` on transferring items).

## Example

```
/burndown "TaskFlow"
/burndown "TaskFlow" --cycle "Sprint 15"
```

## Output Format

```
Sprint 14 — Billing v2 (day 6 of 10)
Total: 40 pts · Completed: 22 · Remaining: 18 · Ideal: 16
Status: 🟡 2 pts behind ideal · Projected end: 30/40 (75%)

Day | Ideal | Actual | Delta
  0 |   40  |   40   |   0
  1 |   36  |   38   |  +2
  …
```