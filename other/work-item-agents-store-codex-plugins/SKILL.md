---
name: work-item
description: 'Create, update, or inspect a work item (issue/task/ticket) in Plane Arguments: <action> <project> [args...].'
---

# Work Item

Create, update, or inspect a single work item in Plane. Delegates all tool resolution to the `connector-bootstrap` skill and all field rules to the `work-items` skill.

## Arguments

Format: `<action> <project> [args...]`

- `action`: one of `create`, `update`, `get`, `search`, `comment`, `link`, `log-time`, `block`
- `project`: project name or identifier
- Remaining args depend on action (see examples)

Parse from `"$ARGUMENTS"`.

## Process

1. **Bootstrap connector** — consult the `connector-bootstrap` skill. Probe `ToolSearch` for the Plane resource tools `project`, `workitem`, `workitem_comment`, `workitem_link`, `work_log` and `workitem_relation` before assuming anything; their names are `mcp__<server>__<resource>`. If multiple Plane instances are connected, ask the user which one.

2. **Resolve project** — `project(action=list)` → pick `project_id` by name or identifier.

3. **Route by action** — follow the matching section of the `work-items` skill:
   - `create` → gather title, description with AC, priority, points, assignees, labels; call `workitem(action=create, project_id, name, description_html, priority, point, state, assignees, labels, type_id?)` (fixed parameter names: `state`, `labels`, `assignees`, `type_id`, `parent`)
   - `update` → resolve work item ID, apply field changes via `workitem(action=update, project_id, workitem_id, ...)`; add or drop one assignee or label with `manage_assignee` / `manage_label`
   - `get` → when the user passes a human identifier like `PROJ-42`, call `workitem(action=retrieve_by_identifier, workitem_identifier="PROJ-42")` (one string). For UUIDs, use `workitem(action=retrieve, project_id, workitem_id)`.
   - `search` → `workitem(action=search, query)` — workspace-scoped (no `project_id`), filter by project client-side if needed; or a server-side filter `workitem(action=list, project_id, pql='text ~ "login bug"')`
   - `comment` → `workitem_comment(action=create, project_id, workitem_id, comment_html)`
   - `link` → `workitem_link(action=create, project_id, workitem_id, url, title?)` (PRs, docs, designs)
   - `log-time` → `work_log(action=create, project_id, workitem_id, duration, description)` with duration as **integer minutes** (convert "2h 30m" → 150); project must have `is_time_tracking_enabled`
   - `block` → `workitem_relation(action=create, project_id, workitem_id, relation_type="blocked_by", workitem_ids=[<uuid>])` (array, plural; the related items go in `workitem_ids`)

4. **Validate** — before creating or committing to a sprint, verify the Definition of Ready from the `agile-fundamentals` skill.

5. **Confirm** — print a short summary of what was created/changed and the item identifier.

## Examples

```
/work-item create "TaskFlow" "Fix login 500 on Safari" --priority high --points 3 --labels bug
/work-item update "TaskFlow" PROJ-148 --state "In Progress" --assignee alice
/work-item get "TaskFlow" PROJ-148
/work-item search "TaskFlow" "login bug"
/work-item comment "TaskFlow" PROJ-148 "Reproduced on Safari 17, investigating"
/work-item link "TaskFlow" PROJ-148 https://github.com/org/repo/pull/420 "PR #420"
/work-item log-time "TaskFlow" PROJ-148 PT2H30M "Debug + fix"
/work-item block "TaskFlow" PROJ-148 PROJ-140
```