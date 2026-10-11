---
name: epic
description: 'Manage Plane epics — list, get, update, delete (complement to /create-epic) Arguments: <action> <project> [args...].'
---

# Epic

Operate on epics beyond creation. For creation use `/create-epic`. For breaking an epic into stories use `/decompose`.

## Arguments

Format: `<action> <project> [args...]`

- `action`: `list` | `get` | `update` | `delete` | `status`
- `project`: project name or identifier
- For `get`/`update`/`status`/`delete`: epic name or ID
- For `update`: `--name`, `--description`, `--lead <user>`, `--target <date>`, `--initiative <name>`

Parse from `"$ARGUMENTS"`.

## Process

1. **Bootstrap connector** — consult `connector-bootstrap`. Probe for the Plane resource tools `workitem_type`, `workitem` and `initiative`. There are no epic tools: an epic is a work item of the type "Epic", and its child items are work items whose `parent` is the epic's id.
2. **Resolve project** → `project_id`, then the epic type: `workitem_type(action=resolve, project_id, name="Epic")` → `type_id`.
3. **Route**:
   - `list` → `workitem(action=list, project_id, pql='type = "<epic-type-id>"')` (follow `next_cursor`). Render: name | lead | child count | state buckets | target | progress %. Child counts per epic: `workitem(action=count, project_id, pql='childOf("<epic identifier>")', group_by=state__group)`.
   - `get` → `workitem(action=retrieve, project_id, workitem_id)` + child items `workitem(action=list, project_id, pql='childOf("<epic identifier>")', fields="id,name,point,estimate_point,state")` grouped by state. Show progress as `(completed_points / total_points)` and as `(completed_count / total_count)`.
   - `status` → same as get but compact and emphasizes RAG (Red/Amber/Green) based on points completed vs time elapsed (see `epics-initiatives-milestones` skill).
   - `update` → `workitem(action=update, project_id, workitem_id, name?, description_html?, assignees?, target_date?)` (`--lead` is the assignee). Linking to an initiative: `--initiative` → `initiative(action=list)` → initiative_id → `initiative(action=manage_workitems, initiative_id, add_ids=[<epic workitem id>])`, read back with `initiative(action=list_workitems, initiative_id)`.
   - `delete` → confirm, then `workitem(action=delete, project_id, workitem_id)` (permanent; the children are separate work items and should be kept — Plane's behaviour, not stated by the tool description: confirm on your instance, and check the children's `parent` afterwards).
4. **Confirm** — re-render after mutation.

## Examples

```
/epic list "TaskFlow"
/epic get "TaskFlow" "Checkout Rewrite"
/epic status "TaskFlow" "Checkout Rewrite"
/epic update "TaskFlow" "Checkout Rewrite" --target 2026-06-30 --lead alice
/epic delete "TaskFlow" "Cancelled Idea"
```

## Best Practices

- Every epic needs an **outcome statement** in its description (not just a feature list). E.g. "Customers can complete checkout in <30s on mobile" — this is the success criterion.
- Epic health check: if an epic has been "in progress" for >3 cycles with <50% completion, rescope or split.
- Pair epics with a tracking page (`/page create project ... --from-template spec`) and link from the epic description.