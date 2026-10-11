---
name: my-work
description: 'List Plane work items assigned to the current user Arguments: [--project name] [--state name] [--cycle current|next|all] [--limit n].'
---

# My Work

Show open work items assigned to the current user across all projects, or filtered.

## Arguments

Format: `[flags...]`

- `--project <name>`: scope to one project (default: all projects in the workspace)
- `--state <group|name>`: filter (default: anything not in `completed` or `cancelled` group)
- `--cycle current|next|all`: filter by cycle membership (default: all)
- `--priority <p0|p1|p2|...>`
- `--limit <n>`: max items (default 25)
- `--all`: include completed and cancelled

Parse from `"$ARGUMENTS"`.

## Process

1. **Bootstrap connector** — consult `connector-bootstrap`. Probe for the Plane resource tools `member`, `project`, `workitem`, `cycle`, `state` and `get_pql_reference`.
2. **Resolve scope** — if `--project`, resolve that one `project_id` (`project(action=list)`); otherwise leave `project_id` out: `workitem(action=list)` without a project searches the whole workspace, so there is no loop over projects.
3. **Build one PQL filter** — `assignee = currentUser()` resolves the signed-in user server-side (no `member(action=me)` call needed). Add, joined with `AND` (at most 5 conditions; `get_pql_reference` has the syntax):
   - default → `stateGroup IN openStates()`; `--all` drops this condition
   - `--state <group>` → `stateGroup = "started"` etc.; `--state <name>` → `state = "<state uuid>"` (`state(action=list, project_id)` resolves the name)
   - `--priority` → `priority = "urgent"|"high"|"medium"|"low"` (p0 = urgent, p1 = high, p2 = medium, p3 = low)
   - `--cycle current` → `cycle IN activeCycle()`; `--cycle next` → `cycle IN upcomingCycles()`; `all` → no cycle condition
4. **Fetch items** — `workitem(action=list, project_id?, pql=<filter>, per_page=<limit>, fields="id,name,point,estimate_point,priority,state,target_date,updated_at")`; follow `next_cursor` for more than one page.
5. **Totals** — `workitem(action=count, project_id?, pql=<filter>, group_by=state__group)` for the breakdown by state group in one call, and `workitem(action=count, project_id?, pql=<filter> AND isOverdue())` for the overdue count (a `count` with `project_id` adds a `project = ...` condition of its own, so keep the filter within 4 conditions there).
6. **Render** — group by project, sort by priority then state. Columns: `ID | Title | State | Priority | Cycle | Updated`.
7. **Show summary** — total items (`total_count`), total story points (sum of listed `point`), breakdown by state, count of overdue.
8. **Suggest** — `/log-time` for items in progress, `/comment add` for items idle >3 days.

## Examples

```
/my-work
/my-work --cycle current
/my-work --project "TaskFlow" --priority p0
/my-work --state "In Review"
/my-work --all --limit 50
```

## Best Practices

- Run this every morning before standup.
- WIP > 3 in-progress items is a red flag (see `agile-fundamentals` WIP limits).
- If the same item shows up day after day with no movement, it's stuck — comment why or ask for help.