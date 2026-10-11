---
name: module
description: 'Manage Plane modules — list, get, update, add items, archive (complement to /create-module) Arguments: <action> <project> [args...].'
---

# Module

Operate on modules (feature workstreams) beyond creation. For initial creation use `/create-module`.

## Arguments

Format: `<action> <project> [args...]`

- `action`: `list` | `list-archived` | `get` | `update` | `add-items` | `remove-items` | `archive` | `unarchive` | `delete`
- `project`: project name or identifier
- For `get`/`update`/`add-items`/etc: module name or ID
- For `update`: `--name`, `--description`, `--lead <user>`, `--target <date>`, `--status <planned|in-progress|paused|completed|cancelled>`
- For `add-items`/`remove-items`: item identifiers as remaining args

Parse from `"$ARGUMENTS"`.

## Process

1. **Bootstrap connector** — consult `connector-bootstrap`. Probe for the Plane resource tools `project`, `module` and `workitem` (`mcp__<server>__module` takes every module action below).
2. **Resolve project** → `project_id`. Resolve module by name when given.
3. **Route**:
   - `list` → `module(action=list, project_id)` (follow `next_cursor`; `archived=true` for `list-archived`). Render: name | lead | items | state buckets | target | progress
   - `get` → `module(action=retrieve, project_id, module_id)` + `module(action=list_workitems, project_id, module_id)` grouped by state; state totals in one call: `workitem(action=count, project_id, pql='module = "<module_id>"', group_by=state__group)`
   - `update` → `module(action=update, project_id, module_id, name?, description?, lead?, target_date?, status?)`; if the response looks empty, read it back with `module(action=retrieve)`
   - `add-items` / `remove-items` → resolve item UUIDs, then one call: `module(action=manage_workitems, project_id, module_id, add_ids=[...])` or `remove_ids=[...]` (both take arrays, so no loop; returns nothing, read back with `list_workitems`; a removal asks for confirmation)
   - `archive` / `unarchive` / `delete` → `module(action=archive|unarchive|delete, project_id, module_id)`; confirm before delete; prefer archive. Some deployments reject archiving an active module — set `status` to completed or cancelled first.
4. **Confirm** — re-render the module after mutation.

## Modules vs Cycles

| Cycles | Modules |
|---|---|
| time-boxed (sprints) | scope-boxed (features) |
| 1–2 weeks | weeks–months |
| velocity unit | progress unit |
| every item belongs to one cycle | items can belong to multiple modules |

A single feature usually spans 2–4 cycles. Use both: items live in a cycle for *when* and a module for *what*.

## Examples

```
/module list "TaskFlow"
/module get "TaskFlow" "Checkout v2"
/module update "TaskFlow" "Checkout v2" --status in-progress --target 2026-05-30
/module add-items "TaskFlow" "Checkout v2" PROJ-148 PROJ-149 PROJ-150
/module remove-items "TaskFlow" "Checkout v2" PROJ-148
/module archive "TaskFlow" "Old Workstream"
```