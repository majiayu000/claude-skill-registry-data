---
name: label
description: 'Manage Plane labels — list, create, update, delete, or apply to a work item Arguments: <action> <project> [args...].'
---

# Label

Manage labels in a Plane project. Labels drive triage, grooming, and reporting filters.

## Arguments

Format: `<action> <project> [args...]`

- `action`: `list` | `create` | `update` | `delete` | `apply` | `remove`
- `project`: project name or identifier
- Remaining: label name, `--color #hex`, `--description`, `--item PROJ-42`

Parse from `"$ARGUMENTS"`.

## Process

1. **Bootstrap connector** — consult `connector-bootstrap`. Probe for the Plane resource tools `label` and `workitem` (for `apply` / `remove`).
2. **Resolve project** — `project(action=list)` → `project_id`.
3. **Route**:
   - `list` → `label(action=list, project_id)` (follow `next_cursor`). Group by prefix (`type/`, `area/`, `priority/`) for readability. Usage per label: `workitem(action=count, project_id, group_by=labels__id)`.
   - `create` → `label(action=create, project_id, name, color, description)`. If color omitted, pick from a stable palette by hashing the name.
   - `update` → resolve label by name → `label(action=update, project_id, label_id, ...)`.
   - `delete` → confirm with the user before the destructive `label(action=delete, project_id, label_id)` call (labels in use are unlinked from items).
   - `apply` → resolve the work item with `workitem(action=retrieve_by_identifier, workitem_identifier="PROJ-42")`, then `workitem(action=manage_label, project_id, workitem_id, add_label_id=<label uuid>)`: the label list is merged server-side, no read-first needed.
   - `remove` → `workitem(action=manage_label, project_id, workitem_id, remove_label_id=<label uuid>)`.
4. **Confirm** — print resulting label set or item label list.

## Conventions

Recommend a **prefixed taxonomy** so labels stay searchable:

- `type/bug`, `type/feature`, `type/chore`, `type/spike`, `type/tech-debt`
- `area/api`, `area/web`, `area/mobile`, `area/infra`
- `priority/p0`, `priority/p1`, `priority/p2`
- `status/needs-info`, `status/blocked`, `status/ready-for-review`
- `customer/acme`, `customer/contoso` (only if you track per-customer work)

Avoid creating one-off labels — they become noise. Audit with `/label list` quarterly.

## Examples

```
/label list "TaskFlow"
/label create "TaskFlow" "type/bug" --color #e11d48
/label update "TaskFlow" "type/bug" --description "Defect in shipped behavior"
/label apply "TaskFlow" --item PROJ-148 "type/bug"
/label remove "TaskFlow" --item PROJ-148 "status/needs-info"
/label delete "TaskFlow" "old-label"
```