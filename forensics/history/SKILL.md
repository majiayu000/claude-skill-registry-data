---
name: history
description: 'Show the change history (activity log) of a Plane work item Arguments: <project> <item> [--limit n].'
---

# History

Render the activity timeline of a work item — every state change, assignment, label, comment, link, and field edit.

## Arguments

Format: `<project> <item> [--limit n]`

- `project`: project name or identifier
- `item`: work item identifier (`PROJ-42`) or UUID
- `--limit <n>`: max events (default 50, newest-first)
- `--since <date>`: only events after a given date

Parse from `"$ARGUMENTS"`.

## Process

1. **Bootstrap connector** — consult `connector-bootstrap`. Probe for the Plane resource tools `workitem` and `workitem_activity`.
2. **Resolve project** → `project_id`. **Resolve work item** → `workitem_id` (`workitem(action=retrieve_by_identifier, workitem_identifier="PROJ-42")`).
3. **Fetch** — `workitem_activity(action=list, project_id, workitem_id, per_page=<limit>)` (follow `next_cursor`); `workitem_activity(action=retrieve, project_id, workitem_id, activity_id)` for one entry. Apply the `--since` filter client-side (the call has no date parameter) and `--limit`.
4. **Normalize each event** — Plane activities have a `verb` (`created`, `updated`, etc.) and a `field`. Render as one line:
   - `2026-04-08 14:32 alice  state: To Do → In Progress`
   - `2026-04-08 14:35 alice  +label: type/bug`
   - `2026-04-08 14:40 bob    comment: "Reproduced..."`
   - `2026-04-08 15:01 alice  assignees: +charlie`
5. **Render** — newest first. Group consecutive events from the same user within 5 minutes into a single block.
6. **Highlight** — mark state regressions in red (e.g., `In Review → In Progress`) — these are leak indicators worth investigating.

## Examples

```
/history "TaskFlow" PROJ-148
/history "TaskFlow" PROJ-148 --limit 20
/history "TaskFlow" PROJ-148 --since 2026-04-01
```

## Best Practices

- Use during retros to figure out *why* an item slipped — when did it stall, who picked it up, when did the blocker land.
- Use for bug forensics — find when severity was changed, or when a label got removed.
- State regressions are a leak signal. If they happen often, your Definition of Done is too loose (see `agile-fundamentals`).