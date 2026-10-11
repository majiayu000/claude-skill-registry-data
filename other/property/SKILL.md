---
name: property
description: 'Manage custom properties on Plane work items (severity, customer impact, etc.) Arguments: <action> <project> [args...].'
---

# Property

Define and manage custom properties on work items. Properties are typed fields beyond the built-ins (state, priority, points). Examples: severity, customer impact, environment, root cause.

## Arguments

Format: `<action> <project> [args...]`

- `action`: `list` | `create` | `update` | `delete` | `get`
- `project`: project name or identifier
- For `create`: `--name`, `--type <text|number|select|multi-select|date|boolean|user|url>` (mapped to Plane's `TEXT`, `DECIMAL`, `OPTION`, `OPTION` + `is_multi`, `DATETIME`, `BOOLEAN`, `RELATION` + `relation_type=USER`, `URL`), `--required`, `--type-id <work_item_type_id>` (the property lives with this work item type), `--options "a,b,c"` (for select)
- For `update`: same flags

Parse from `"$ARGUMENTS"`.

## Process

1. **Bootstrap connector** — consult `connector-bootstrap`. Probe for the Plane resource tools `workitem_property`, `workitem_type` and `workitem` (plan-gated: a plan without work item properties refuses the calls with a message naming the feature).
2. **Resolve project** → `project_id`. If `--type-id` not given, resolve the work item type by name: `workitem_type(action=resolve, project_id, name="Bug")` returns its `id` (the `workitem_type_id`).
3. **Route**:
   - `list` → `workitem_property(action=list, project_id, workitem_type_id?)` (without ids it lists every workspace property in one call; follow `next_cursor`). Render: name | data type | scope (type) | required? | option count
   - `create` → `workitem_property(action=create, project_id, workitem_type_id, display_name, property_type, is_required?, is_multi?, options?)`. For `select`/`multi-select`, parse the options into `options=[{"name": "S0"}, ...]` (a JSON array of `{name, color, is_default}`). `TEXT` and `DATETIME` need a `display_format`; list their allowed values from the tool description.
   - `update` → resolve by name → `workitem_property(action=update, workitem_property_id, project_id?, workitem_type_id?, ...)`. **Changing data type breaks existing values** — warn loudly. Options are managed with `create_option` / `update_option` / `delete_option`.
   - `delete` → confirm, then `workitem_property(action=delete, workitem_property_id, ...)`. Existing values are dropped. (Detaching a property from a type only removes the association: `workitem_property(action=manage_type_properties, workitem_type_id, detach_ids=[...])`.)
   - `get` → `workitem_property(action=retrieve, workitem_property_id, ...)` + a sample of items that have it set: `workitem(action=list, project_id, pql='cf["<property-id>"] IS NOT NULL', per_page=5)`. A single item's value: `workitem_property(action=get_value, project_id, workitem_id, property_id)`; to set it: `set_value`.
4. **Confirm** — re-list.

## Property design rules

- **Use a property when**: data is structured, queryable, and reportable (severity, environment, customer).
- **Use a label when**: data is freeform tagging, optional, no values needed (`needs-design`, `flaky`).
- **Use a work item type when**: the workflow itself differs (Bug vs Spike).

Three buckets, three tools — don't mix. See `labels-states-properties` skill.

## Examples

```
/property list "TaskFlow"
/property create "TaskFlow" --name severity --type select --options "S0,S1,S2,S3" --required
/property create "TaskFlow" --name "customer impact" --type number
/property create "TaskFlow" --name environment --type select --options "prod,staging,dev"
/property update "TaskFlow" severity --required false
/property delete "TaskFlow" "old field"
```