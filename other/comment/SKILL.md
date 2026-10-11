---
name: comment
description: 'Add or list comments on a Plane work item Arguments: <action> <project> <item> [body].'
---

# Comment

Add or list comments on a Plane work item.

## Arguments

Format: `<action> <project> <item> [body]`

- `action`: `add` (default if omitted) | `list` | `update` | `delete`
- `project`: project name or identifier
- `item`: work item identifier (`PROJ-42`) or UUID
- `body`: comment text (for `add`/`update`) — supports markdown

Parse from `"$ARGUMENTS"`.

## Process

1. **Bootstrap connector** — consult `connector-bootstrap`. Probe for the Plane resource tool `workitem_comment` (and `workitem`, `member` for lookups).
2. **Resolve project** → `project_id`. **Resolve work item** → `workitem_id` (`workitem(action=retrieve_by_identifier, workitem_identifier="PROJ-42")`).
3. **Route**:
   - `add` → convert the markdown body to HTML and call `workitem_comment(action=create, project_id, workitem_id, comment_html="<p>…</p>")` (`access` is `INTERNAL` or `EXTERNAL`). To mention someone write `@[<user uuid>]` inline (resolve the person with `member(action=list_project, project_id)`); a bare `@name` notifies nobody.
   - `list` → `workitem_comment(action=list, project_id, workitem_id)` (follow `next_cursor`), render newest-first with author + timestamp.
   - `update` → resolve `comment_id` (last by current user, or explicit `--id`), `workitem_comment(action=update, project_id, workitem_id, comment_id, comment_html)`.
   - `delete` → confirm before the destructive `workitem_comment(action=delete, project_id, workitem_id, comment_id)` call.
4. **Confirm** — print the comment ID and a one-line preview.

## Examples

```
/comment add "TaskFlow" PROJ-148 "Reproduced on Safari 17.2 — root cause is the cookie SameSite change"
/comment list "TaskFlow" PROJ-148
/comment update "TaskFlow" PROJ-148 --id 9f2c... "Updated: also affects Safari 16"
/comment delete "TaskFlow" PROJ-148 --id 9f2c...
```

## Best Practices

- Comments are for **decisions and findings**, not status pings ("any update?"). Use standup or DM for that.
- When closing a bug, leave a final comment with: root cause, fix summary, test added. This is gold for future debugging.
- Cross-link related items in the body using their identifier (e.g. "see PROJ-150") — Plane auto-links them.