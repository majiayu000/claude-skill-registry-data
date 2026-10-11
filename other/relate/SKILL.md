---
name: relate
description: 'Create a relation between two Plane work items (block, duplicate, relates-to) Arguments: <relation> <project> <from-item> <to-item>.'
---

# Relate

Create or remove a typed relation between two work items.

## Arguments

Format: `<relation> <project> <from-item> <to-item>`

- `relation`: `blocks` | `blocked-by` | `duplicate` | `duplicate-of` | `relates-to` | `remove`
- `project`: project name or identifier
- `from-item`: source work item identifier (`PROJ-42`)
- `to-item`: target work item identifier (`PROJ-43`)

Parse from `"$ARGUMENTS"`.

## Process

1. **Bootstrap connector** — consult `connector-bootstrap`. Probe for the Plane resource tools `workitem_relation` and `workitem`.
2. **Resolve project** → `project_id`. **Resolve both work items** → UUIDs (`workitem(action=retrieve_by_identifier, workitem_identifier="PROJ-42")`).
3. **Map relation type** to API value. The built-in dependency types are `blocking`, `blocked_by`, `start_before`, `start_after`, `finish_before`, `finish_after` (they go in `relation_type`). Duplicate, relates-to and any custom relation are *definitions*: call `workitem_relation(action=list_definitions)`, match the user's wording to an entry, and pass `relation_definition_id` plus `relation_definition_label` (the matched outward or inward label, which sets the direction) instead of `relation_type`. The related items go in `workitem_ids` (an array of UUIDs).
4. **Route**:
   - `blocks` → `workitem_relation(action=create, project_id, workitem_id=<from>, workitem_ids=[<to>], relation_type="blocking")` (the inverse `blocked_by` shows on the target)
   - `blocked-by` → `workitem_relation(action=create, ..., relation_type="blocked_by")`
   - `duplicate` / `duplicate-of` → the duplicate definition (`list_definitions`), with `relation_definition_id` and the label for the requested direction
   - `relates-to` → the relates-to definition, the same way
   - `remove` → `workitem_relation(action=list, project_id, workitem_id)`, find the matching one, then `workitem_relation(action=delete, project_id, workitem_id, related_workitem_id, is_dependency)`; `is_dependency` must match the kind that was created (true for the six built-in types, default false for definitions)
5. **Confirm** — print both items and the relation direction.

## Examples

```
/relate blocks "TaskFlow" PROJ-148 PROJ-150
/relate blocked-by "TaskFlow" PROJ-150 PROJ-148
/relate duplicate "TaskFlow" PROJ-160 PROJ-148
/relate relates-to "TaskFlow" PROJ-148 PROJ-200
/relate remove "TaskFlow" PROJ-148 PROJ-150
```

## Best Practices

- Set blockers **as soon as you discover them**, not in retro. Blockers visible early let the team unblock themselves.
- Mark duplicates with `duplicate-of`, then close the duplicate with a comment linking to the canonical item.
- Use `/dependencies` after blocking to see the full graph and detect chains/cycles.