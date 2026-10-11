---
name: milestone
description: 'Manage Plane milestones — create, list, add items, update, delete Arguments: <action> <project> [args...].'
---

# Milestone

Create and manage milestones (release markers) on a Plane project. For status/risk reporting on an existing milestone use `/milestone-status`.

## Arguments

Format: `<action> <project> [args...]`

- `action`: `create` | `list` | `get` | `update` | `delete` | `add-items` | `remove-items`
- `project`: project name or identifier
- For `create`: `--name`, `--target <date>`, `--description`
- For `add-items`/`remove-items`: `--milestone <name>`, item IDs as remaining args

Parse from `"$ARGUMENTS"`.

## Process

1. **Bootstrap connector** — consult `connector-bootstrap`. Probe for the Plane resource tools `project`, `milestone` and `workitem`.
2. **Resolve project** → `project_id`.
3. **Route**:
   - `create` → gather name + target date (required). Call `milestone(action=create, project_id, title=<name>, target_date)` (the Plane field is `title`; the milestone has no description field, so put context on a linked page). Reject milestones >6 months out — split into two.
   - `list` → `milestone(action=list, project_id)` (follow `next_cursor`), render with item count and target date.
   - `get` → `milestone(action=retrieve, project_id, milestone_id)` + `milestone(action=list_workitems, project_id, milestone_id)`. Render scope and aggregate state buckets (`workitem(action=count, project_id, pql='milestone = "<milestone_id>"', group_by=state__group)`).
   - `update` → resolve by name → `milestone(action=update, project_id, milestone_id, title?, target_date?)`. Moving the target date is a **trade-off conversation** — reduce scope first, slip date last (see `epics-initiatives-milestones` skill).
   - `delete` → confirm, then `milestone(action=delete, project_id, milestone_id)`. Items are unlinked, not deleted.
   - `add-items` / `remove-items` → resolve item UUIDs → `milestone(action=manage_workitems, project_id, milestone_id, add_ids=[...])` or `remove_ids=[...]` (returns nothing; read back with `milestone(action=list_workitems)`). A removal asks for confirmation.
4. **Confirm** — print milestone ID, target date, and item count.

## Examples

```
/milestone create "TaskFlow" --name "v2.0 Public Beta" --target 2026-06-15
/milestone list "TaskFlow"
/milestone get "TaskFlow" "v2.0 Public Beta"
/milestone add-items "TaskFlow" --milestone "v2.0 Public Beta" PROJ-148 PROJ-150 PROJ-151
/milestone update "TaskFlow" "v2.0 Public Beta" --target 2026-06-22
/milestone remove-items "TaskFlow" --milestone "v2.0 Public Beta" PROJ-160
```

## Best Practices

- Every milestone needs a **single owner** (the release manager).
- Lock the milestone scope at T-2 weeks. Add-items after lock requires removing equivalent points.
- Pair `/milestone create` with a Plane page (`/page create project ... --from-template milestone-update`) and link them in the milestone description.
- Use `/milestone-status` weekly during the run-up to track risk.