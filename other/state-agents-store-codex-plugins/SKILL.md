---
name: state
description: 'Manage Plane workflow states — list, create, update, delete, reorder Arguments: <action> <project> [args...].'
---

# State

Manage workflow states (the columns on a board) for a Plane project.

## Arguments

Format: `<action> <project> [args...]`

- `action`: `list` | `create` | `update` | `delete`
- `project`: project name or identifier
- For `create`/`update`: `--name`, `--group <backlog|unstarted|started|completed|cancelled>`, `--color #hex`, `--sequence <int>`, `--default`

Parse from `"$ARGUMENTS"`.

## Process

1. **Bootstrap connector** — consult `connector-bootstrap`. Probe for the Plane resource tools `project`, `state` and `workitem`.
2. **Resolve project** → `project_id`.
3. **Route**:
   - `list` → `state(action=list, project_id)` (follow `next_cursor`). Render grouped by `group`, sorted by `sequence`. Mark the default state. Plane keeps its own triage state per project; it is not listed and cannot be created, and `Triage` is a reserved name.
   - `create` → require `--name` and `--group`. Color defaults from a stable palette per group. Call `state(action=create, project_id, name, color, group, sequence?, default?)` (`color` is required, a hex code).
   - `update` → resolve state by name → `state(action=update, state_id, project_id, name?, color?, group?, sequence?, default?)`. Renaming a state does NOT migrate items — they keep the same `state_id`.
   - `delete` → confirm. **Block deletion** if any items currently sit in this state (`workitem(action=count, project_id, pql='state = "<state uuid>"')` → `total_count`) — instruct the user to migrate them first via `/bulk-update --state <new>`. Then `state(action=delete, state_id, project_id)`.
4. **Confirm** — re-list states after mutation.

## State group semantics

Plane groups are fixed: `backlog`, `unstarted`, `started`, `completed`, `cancelled`. Velocity counts only items moved into a `completed` group state during the cycle. Reports separate `cancelled` from `completed`. **Don't put "Done" in the `started` group** — it breaks burndown.

## Recommended state set (Scrum)

| Group | States |
|---|---|
| backlog | Backlog |
| unstarted | Ready, To Do |
| started | In Progress, In Review |
| completed | Done |
| cancelled | Cancelled, Won't Fix |

See `labels-states-properties` skill for variant sets (Kanban, support, research).

## Examples

```
/state list "TaskFlow"
/state create "TaskFlow" --name "In Review" --group started --color #f59e0b
/state update "TaskFlow" "In Review" --sequence 35
/state delete "TaskFlow" "Old Column"
```