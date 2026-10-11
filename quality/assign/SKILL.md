---
name: assign
description: 'Assign or unassign a Plane work item to one or more users Arguments: <project> <item> <assignee> [more...].'
---

# Assign

Assign a work item in Plane to one or more users. Replaces or appends depending on flags.

## Arguments

Format: `<project> <item> <assignee> [more...]`

- `project`: project name or identifier
- `item`: work item identifier (`PROJ-42`) or UUID
- `assignee`: username, email, display name, or `me`
- Additional assignees space-separated for multi-assign
- Flags: `--replace` (default: append), `--unassign <user>`, `--clear` (remove all)

Parse from `"$ARGUMENTS"`.

## Process

1. **Bootstrap connector** — consult `connector-bootstrap`. Probe for the Plane resource tools `workitem` and `member` (`mcp__<server>__workitem`, `mcp__<server>__member`).
2. **Resolve project** → `project_id`. **Resolve work item** → `workitem_id` (`workitem(action=retrieve_by_identifier, workitem_identifier="PROJ-42")`; the result carries the current `assignees`).
3. **Resolve users**:
   - `me` → `member(action=me)` → user_id
   - else → `member(action=list_project, project_id)` and match by `display_name`, `email`, or `username` (case-insensitive). If no project member matches, fall back to `member(action=list_workspace, display_name=...)` (name and email filters match case-insensitively). If still ambiguous, ask the user to choose.
4. **Choose the call**:
   - default (append) → `workitem(action=manage_assignee, project_id, workitem_id, add_user_id=<id or several>)`: the list is merged, nothing is replaced
   - `--unassign <user>` → `workitem(action=manage_assignee, project_id, workitem_id, remove_user_id=<id>)`
   - `--replace` → `workitem(action=update, project_id, workitem_id, assignees=[<new ids>])`
   - `--clear` → `workitem(action=update, project_id, workitem_id, assignees=[])`
5. **Update** — run the call from step 4. The assignees parameter is `assignees` on `update` and `add_user_id` / `remove_user_id` on `manage_assignee` (the tool validates against the declared set)
6. **Confirm** — print final assignee list and item identifier.

## Examples

```
/assign "TaskFlow" PROJ-148 alice
/assign "TaskFlow" PROJ-148 me
/assign "TaskFlow" PROJ-148 alice bob --replace
/assign "TaskFlow" PROJ-148 --unassign bob
/assign "TaskFlow" PROJ-148 --clear
```

## Best Practices

- Prefer **single assignee** for accountability. Multi-assign blurs ownership — use it only for pairing or review handoff.
- Don't assign before the item meets Definition of Ready (see `agile-fundamentals` skill).
- When unassigning yourself, leave a comment with handoff context (`/comment add ...`).