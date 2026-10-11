---
name: whoami
description: 'Show the current Plane user, workspace, and connector status Arguments: (no arguments).'
---

# Who Am I

Print the identity and context Plane is currently operating with. Useful for verifying the right account/instance is connected before destructive operations.

## Process

1. **Bootstrap connector** — consult `connector-bootstrap`. Probe for the Plane resource tools `member`, `workspace` and `project`.
2. **Identity** — `member(action=me)`. Print: display name, email, user_id, role, avatar URL.
3. **Workspace** — `workspace(action=retrieve)`: the workspace this connection is bound to (slug, and id and name on an OAuth connection; null otherwise, along with how it connected). Then `workspace(action=get_features)` and print the enabled features.
4. **Projects** — `project(action=list)` (follow `next_cursor`), count by archived/active. Print top 5 by recent activity.
5. **Connector** — print which MCP server / instance the tools were resolved against (from `connector-bootstrap` result). If multiple Plane instances are connected, list them and indicate the active one.
6. **Suggest** — if no projects, suggest `/setup-project`. If multiple instances, show how to switch.

## Examples

```
/whoami
```

## Why this exists

Before running anything destructive (`/cycles delete`, `/projects delete`, `/state delete`), run `/whoami` to make sure you are not accidentally connected to a production workspace when you meant the staging one. Cheap insurance.