---
name: log-time
description: 'Log work time on a Plane work item (create a work log entry) Arguments: <project> <item> <duration> [description].'
---

# Log Time

Create a work log entry against a Plane work item. Time is stored as **integer minutes** in the API — convert human input.

## Arguments

Format: `<project> <item> <duration> [description]`

- `project`: project name or identifier
- `item`: work item identifier (e.g. `PROJ-42`) or UUID
- `duration`: human form (`2h`, `2h30m`, `45m`, `1.5h`, `PT2H30M`) — convert to integer minutes
- `description` (optional): free text — what was done

Parse from `"$ARGUMENTS"`.

## Process

1. **Bootstrap connector** — consult `connector-bootstrap`. Probe for the Plane resource tools `work_log`, `project` and `workitem`.
2. **Verify time tracking is enabled** — `project(action=retrieve, project_id)`; if `is_time_tracking_enabled` is false, tell the user how to enable it (project settings → features, or `project(action=update, project_id, is_time_tracking_enabled=true)` with their consent) and stop. A plan without time tracking refuses `work_log` calls with a message naming the feature.
3. **Resolve project** → `project_id`. **Resolve work item** → if identifier like `PROJ-42`, use `workitem(action=retrieve_by_identifier, workitem_identifier="PROJ-42")`; if UUID, skip.
4. **Convert duration to minutes**:
   - `2h` → 120, `2h30m` → 150, `45m` → 45, `1.5h` → 90, `PT2H30M` → 150
   - Reject if result < 1 or > 24h in a single entry (likely a typo); ask user to confirm.
5. **Create the log** — `work_log(action=create, project_id, workitem_id, duration=<minutes>, description)`.
6. **Confirm** — print: total logged today on this item, total logged on this item (`work_log(action=list, project_id, workitem_id)`, follow `next_cursor`; `work_log` lists one work item at a time), and the project totals from `project(action=worklog_summary, project_id)`.

## Subcommands

The base form logs time. Additional verbs (parse `<verb> ...` if first arg is one of these):

- `summary <project>` → `project(action=worklog_summary, project_id)` — total logged per user / per item
- `list <project> <item>` → `work_log(action=list, project_id, workitem_id)` for that item
- `delete <project> <item> <log_id>` → `work_log(action=delete, project_id, workitem_id, work_log_id)` (confirm first)
- `update <project> <item> <log_id> <duration>` → `work_log(action=update, project_id, workitem_id, work_log_id, duration=<minutes>)`

## Examples

```
/log-time "TaskFlow" PROJ-148 2h "Debug Safari login bug + fix"
/log-time "TaskFlow" PROJ-148 45m
/log-time summary "TaskFlow"
/log-time list "TaskFlow" PROJ-148
/log-time delete "TaskFlow" PROJ-148 9f2c-...
```

## Best Practices

- Log time **at the end of each work session**, not in batch at week's end — accuracy drops sharply after 24h.
- One entry per session per item. Don't merge a whole day into one log.
- Use `/log-time summary` before estimation sessions — actual minutes per story point is the most honest velocity input (see `velocity-metrics` skill).