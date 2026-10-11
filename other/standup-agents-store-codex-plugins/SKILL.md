---
name: standup
description: 'Generate daily standup summary for current sprint Arguments: <project>.'
---

# Standup

Generate a daily standup summary — per-person status, sprint progress, and blockers.

## Arguments
Format: `<project>`
- project: Project name or identifier (required)

Parse from "$ARGUMENTS".

## Process

0. **Bootstrap connector** — consult the `connector-bootstrap` skill. Probe `ToolSearch` for the Plane resource tools referenced below (`project`, `member`, `cycle`, `workitem`, `workitem_relation`); their names are `mcp__<server>__<resource>`, never assume a specific MCP prefix. If multiple Plane instances are connected, ask the user which one to use. All formulas and rules come from the `agile-fundamentals` skill. Calls are written `resource(action=..., ...)`.

1. **Find active sprint:**
   ```
   cycle(action=list, project_id, status=current)
   ```
   The cycle where today is between start_date and end_date.

2. **Get sprint items and team:**
   ```
   cycle(action=list_workitems, project_id, cycle_id)
   member(action=list_project, project_id)
   workitem(action=count, project_id, pql='cycle = "<cycle_id>"', group_by=state__group)
   ```
   The count gives the state-group totals in one call.

3. **Group items by assignee and state:**
   For each team member:
   - Completed: items in "completed" state group
   - In Progress: items in "started" state group
   - Not Started: items in "unstarted" state group

4. **Detect blockers:**
   For in-progress items, check:
   ```
   workitem_relation(action=list, project_id, workitem_id)
   cycle(action=list_workitems, project_id, cycle_id, pql='stateGroup = "started" AND updatedAt < daysAgo(2)')
   ```
   Flag items with "blocked_by" relations, and items in progress that have not changed for 2+ days (stalled candidates).

5. **Calculate sprint progress:**
   - Total/completed/remaining points
   - Days elapsed and remaining
   - Pace vs needed pace
   - WIP count vs limit

6. **Display standup report:**
   Per-person summary (done, doing, blocked) + team-level sprint progress.

## Example Usage
```
/standup "TaskFlow"
/standup "My Project"
```