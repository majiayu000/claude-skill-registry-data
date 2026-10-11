---
name: link
description: 'Add or list external links (PRs, docs, designs) on a Plane work item Arguments: <action> <project> <item> [url] [title].'
---

# Link

Attach external URLs to a work item — pull requests, design docs, Figma boards, runbooks.

## Arguments

Format: `<action> <project> <item> [url] [title]`

- `action`: `add` (default) | `list` | `remove`
- `project`: project name or identifier
- `item`: work item identifier or UUID
- `url`: full URL (required for `add`)
- `title`: human-readable label (optional; auto-derive from URL host + path tail if omitted)
- `--id <link_id>` for `remove`

Parse from `"$ARGUMENTS"`.

## Process

1. **Bootstrap connector** — consult `connector-bootstrap`. Probe for the Plane resource tools `workitem_link` and `workitem`.
2. **Resolve project** → `project_id`. **Resolve work item** → `workitem_id` (`workitem(action=retrieve_by_identifier, workitem_identifier="PROJ-42")`).
3. **Route**:
   - `add` → if title omitted, derive: `github.com/org/repo/pull/420` → `"PR #420"`, `figma.com/file/...` → `"Figma design"`, `docs.google.com/...` → `"Google Doc"`. Call `workitem_link(action=create, project_id, workitem_id, url, title)` (`url` must be `http://` or `https://`; `title` is the text Plane shows instead of the URL).
   - `list` → `workitem_link(action=list, project_id, workitem_id)`, render as `Title — URL`.
   - `remove` → with `--id`, call `workitem_link(action=delete, project_id, workitem_id, link_id)`. Without, list and ask which to remove. To fix a title or URL use `workitem_link(action=update, ..., link_id, url?, title?)`.
4. **Confirm** — print link title and the item identifier.

## Examples

```
/link add "TaskFlow" PROJ-148 https://github.com/org/repo/pull/420
/link add "TaskFlow" PROJ-148 https://figma.com/file/abc "Login flow design v3"
/link list "TaskFlow" PROJ-148
/link remove "TaskFlow" PROJ-148 --id 9f2c-...
```

## Best Practices

- Always link the **PR** to the work item — this is how reviewers find context and how release-notes generation finds the change.
- Link **design** before implementation, **runbook** before deploy.
- Avoid pasting links into the description body — use proper links so they can be enumerated.