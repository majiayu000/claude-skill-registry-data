---
name: projects
description: 'List, inspect, update, or delete Plane projects (complement to /setup-project) Arguments: <action> [args...].'
---

# Projects

Operate on Plane projects. For initial creation with Agile defaults use `/setup-project`.

## Arguments

Format: `<action> [args...]`

- `action`: `list` | `get` | `update` | `archive` | `unarchive` | `delete` | `features`
- For `get`/`update`/`delete`/`features`: project name or identifier
- For `update`: `--name`, `--identifier <SLUG>`, `--description`, `--icon` (the `emoji` field), `--lead <user>` (`project_lead`), `--default-assignee <user>`, `--time-tracking on|off`
- For `features`: `--enable cycles,modules,epics,intakes,pages,views,workitem_types` or `--disable ...` (also `parallel_cycles`, `project_updates`, `workflows`)

Parse from `"$ARGUMENTS"`.

## Process

1. **Bootstrap connector** — consult `connector-bootstrap`. Probe for the Plane resource tools `project` and `member`.
2. **Route**:
   - `list` → `project(action=list)` (paginated: follow `next_cursor`; the list is trimmed, use `retrieve` for full detail). Render: identifier | name | lead | members | cycles? | modules? | last activity. Highlight archived.
   - `get` → `project(action=retrieve, project_id)` + `member(action=list_project, project_id)` member count + `project(action=get_features, project_id)` + active cycle count (`cycle(action=list, project_id, status=current)`).
   - `update` → `project(action=update, project_id, ...)`. Changing `identifier` rewrites all work item IDs (`OLD-42` → `NEW-42`) — warn loudly before doing this. `--time-tracking` sets `is_time_tracking_enabled`.
   - `archive` / `unarchive` → `project(action=archive|unarchive, project_id)`: the safer alternative to delete.
   - `delete` → **destructive** (the whole project with its work items, cycles, modules and pages). Confirm with project name typed back. Suggest `archive` as the safer alternative. `project(action=delete, project_id)`.
   - `features` → `project(action=get_features, project_id)` first, show current state, then `project(action=update_features, project_id, <flag>=true|false, ...)`; omitted flags are left as they are. Flags: cycles, modules, views, pages, intakes (the triage inbox), workitem_types, epics, parallel_cycles, project_updates, workflows. Time tracking is not a feature flag: it is `project(action=update, is_time_tracking_enabled=...)`. A plan without a feature refuses the call with a message naming it.
3. **Confirm** — print result.

## Examples

```
/projects list
/projects get "TaskFlow"
/projects update "TaskFlow" --lead alice --description "Customer-facing checkout app"
/projects features "TaskFlow" --enable intakes,pages,modules
/projects delete "Old Sandbox"
```

## Best Practices

- Don't rename project `identifier` after launch — every existing reference (commits, PR titles, Slack threads) breaks.
- Disable unused features — clutter in the sidebar slows everyone down. Most teams need: cycles, modules, pages, views.
- Use `/projects features` to enable `intakes` before running `/triage-intake`.