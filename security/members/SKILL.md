---
name: members
description: 'List Plane workspace or project members and their roles Arguments: [scope] [project].'
---

# Members

List members of the workspace or a specific project.

## Arguments

Format: `[scope] [project]`

- `scope`: `workspace` (default) | `project`
- `project`: required when `scope=project` — project name or identifier
- `--role <slug>`: filter by role slug (workspace roles: Owner / Admin / Member / Guest; project roles: Admin / Contributor / Commenter / Guest; `member(action=list_roles)` lists the slugs)
- `--active`: only active members

Parse from `"$ARGUMENTS"`.

## Process

1. **Bootstrap connector** — consult `connector-bootstrap`. Probe for the Plane resource tools `member` and `project`.
2. **Route**:
   - `workspace` → `member(action=list_workspace, per_page=100)` (follow `next_cursor`). Render: name | email | role | joined | last active.
   - `project` → resolve `project_id` → `member(action=list_project, project_id)`. Add a column showing the workspace role for context.
3. **Apply filters** — server-side where possible: `member(action=list_workspace, role_slug=<slug>, is_active=true, first_name=…, last_name=…, email=…, display_name=…)`; the name filters match case-insensitively and combine with AND. `member(action=list_project)` has no filters: filter client-side.
4. **Highlight current user** (from `member(action=me)`).
5. **Footer** — total count, count by role.

## Examples

```
/members
/members workspace --role admin
/members project "TaskFlow"
/members project "TaskFlow" --role member
```

## Best Practices

- Audit workspace admins quarterly — too many admins is a security risk.
- Project membership should be the minimum needed; use viewer for stakeholders.
- Pair with `/assign` to find the right user when names are ambiguous.