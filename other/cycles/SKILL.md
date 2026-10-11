---
name: cycles
description: 'Manage Plane cycles beyond planning — list, complete, archive, transfer, delete Arguments: <action> <project> [args...].'
---

# Cycles

Operate on cycles (sprints) beyond create/plan/close. For sprint planning use `/plan-sprint` and `/create-sprint`; for status use `/sprint-status`; for closing use `/close-sprint`.

## Arguments

Format: `<action> <project> [args...]`

- `action`: `list` | `list-archived` | `get` | `complete` | `archive` | `unarchive` | `transfer` | `delete` | `update`
- `project`: project name or identifier
- For `get`/`complete`/`archive`/`unarchive`/`delete`: cycle name or ID
- For `transfer`: `--from <cycle>` `--to <cycle>` (moves the unfinished items only)
- For `update`: `--name`, `--description`, `--start <date>`, `--end <date>`

Parse from `"$ARGUMENTS"`.

## Process

1. **Bootstrap connector** — consult `connector-bootstrap`. Probe for the Plane resource tools `project` and `cycle` (`mcp__<server>__cycle` takes every action used below).
2. **Resolve project** → `project_id`.
3. **Route**:
   - `list` → `cycle(action=list, project_id)` (optionally `status=current|upcoming|completed|draft|incomplete`; follow `next_cursor`). Render with: name | state (upcoming/current/completed) | dates | items | progress.
   - `list-archived` → `cycle(action=list, project_id, archived=true)`.
   - `get` → `cycle(action=retrieve, project_id, cycle_id)` + `cycle(action=list_workitems, project_id, cycle_id)`; item totals per state group: `workitem(action=count, project_id, pql='cycle = "<cycle_id>"', group_by=state__group)`. Show metrics.
   - `complete` → `cycle(action=complete, project_id, cycle_id)`: ends the sprint today (sets `end_date`). Skip when `end_date` is already past.
   - `archive` → confirm. `cycle(action=archive, project_id, cycle_id)` **ends a still-running cycle first**, so warn when the cycle is still current and offer `complete` + `transfer` before archiving. Archived cycles disappear from default views but remain queryable.
   - `unarchive` → `cycle(action=unarchive, project_id, cycle_id)` restores it.
   - `transfer` → resolve both cycles. The source cycle must already have ended: if it has not, offer `cycle(action=complete)` first (the server rejects the transfer otherwise). Call `cycle(action=transfer_workitems, project_id, cycle_id=<from>, new_cycle_id=<to>)`; it moves only the unfinished work items, finished ones stay in the sprint they were completed in. Print the count moved (compare `workitem(action=count, pql='cycle = "<to>"')` before and after). To carry specific items elsewhere, use `cycle(action=manage_workitems, ..., add_ids=[...])` on the target.
   - `delete` → **destructive**, confirm twice. Items lose cycle assignment but are not deleted. Prefer `archive` over `delete`. `cycle(action=delete, project_id, cycle_id)`.
   - `update` → resolve cycle → `cycle(action=update, project_id, cycle_id, name?, description?, start_date?, end_date?)`. Changing dates of an active cycle distorts velocity history — warn the user.
4. **Confirm** — re-list after mutation.

## Examples

```
/cycles list "TaskFlow"
/cycles list-archived "TaskFlow"
/cycles get "TaskFlow" "Sprint 14"
/cycles transfer "TaskFlow" --from "Sprint 14" --to "Sprint 15"
/cycles archive "TaskFlow" "Sprint 10"
/cycles update "TaskFlow" "Sprint 15" --end 2026-04-25
/cycles delete "TaskFlow" "Sprint 09"
```

## Best Practices

- **Archive completed cycles after retro** — keeps the active list clean while preserving velocity data.
- Don't use `delete` to "redo" a sprint — historical data is gold for velocity. Archive instead.
- `transfer` should be the LAST step of a sprint close, after retro, not the first.