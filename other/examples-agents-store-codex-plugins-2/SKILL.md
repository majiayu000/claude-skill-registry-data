---
name: examples
description: Tool call patterns, end-to-end workflow examples, and scenario references for Plane Agile workflows. Use when needing reference implementations, complete examples, or tool call patterns.
---

# Examples & References

This skill provides reference implementations, tool call patterns, and complete workflow scenarios for Plane Agile workflows.

## Related Skills

For day-to-day operations, route through the dedicated skills rather than this reference:

| Domain | Skill |
|--------|-------|
| Tool discovery across any MCP/connector/instance | **connector-bootstrap** |
| Formulas, DoR/DoD, MoSCoW, WSJF, Fibonacci | **agile-fundamentals** |
| Sprint planning ceremony | **sprint-planning** |
| Work item CRUD, relations, comments, logs | **work-items** |
| Feature/workstream grouping | **modules** |
| Long-horizon planning (epic, initiative, milestone) | **epics-initiatives-milestones** |
| Triage incoming requests | **intake-triage** |
| Publish reports and pages (sprint, retro, ADR, runbook, spec) | **pages-publishing** |
| Labels, states, work item types, custom properties | **labels-states-properties** |
| Backlog grooming, WSJF | **backlog-management** |
| Estimation | **estimation** |
| Task decomposition | **task-decomposition** |
| Velocity and burndown | **velocity-metrics** |
| Daily standup | **daily-standup** |
| Sprint review and retro | **sprint-review-retro** |
| New project setup | **project-setup** |

## Reference Files

| File | Description |
|------|-------------|
| [tool-patterns.md](references/mcp/tool-patterns.md) | Tool call patterns with exact parameter formats |
| [workflow-examples.md](references/mcp/workflow-examples.md) | Multi-step workflow examples combining multiple tools |
| [page-formatting.md](references/page-formatting.md) | HTML formatting rules and templates for Plane pages (`description_html`) |
| [sprint-lifecycle.md](references/scenarios/sprint-lifecycle.md) | End-to-end sprint lifecycle scenario |
| [backlog-grooming.md](references/scenarios/backlog-grooming.md) | Backlog grooming session scenario |
| [everyday-commands.md](references/scenarios/everyday-commands.md) | Common day-to-day flows: page creation, time logging, PR linking, bulk edits, label/state setup |

## Quick Reference: The Resource Tools

Plane MCP (0.3.0 and later) exposes **one tool per resource**; the `action` parameter selects the operation, so a call reads `cycle(action=list, project_id=<id>)`. Every tool's own description lists its actions with their required and optional parameters and is the authoritative reference at call time. Scope: pass `project_id` for a project's own set, omit it for the workspace.

| Tool | Actions |
|------|---------|
| `project` | `list` `retrieve` `create` `update` `delete` `archive` `unarchive` `worklog_summary` `get_features` `update_features` |
| `workspace` | `retrieve` `get_features` `update_features` |
| `member` | `me` `list_workspace` `list_project` `list_roles` `retrieve_role` |
| `workitem` | `list` `list_archived` `retrieve` `retrieve_by_identifier` `search` `count` `create` `update` `delete` `archive` `manage_assignee` `manage_label` |
| `cycle` | `list` `retrieve` `create` `update` `delete` `list_workitems` `manage_workitems` `transfer_workitems` `complete` `archive` `unarchive` |
| `module` | `list` `retrieve` `create` `update` `delete` `list_workitems` `manage_workitems` `archive` `unarchive` |
| `milestone` | `list` `retrieve` `create` `update` `delete` `list_workitems` `manage_workitems` |
| `initiative` | `list` `retrieve` `create` `update` `delete` `list_projects` `add_projects` `remove_projects` `list_workitems` `manage_workitems` |
| `intake` | `list` `retrieve` `create` `update` `delete` |
| `state` | `list` `retrieve` `create` `update` `delete` |
| `label` | `list` `retrieve` `create` `update` `delete` |
| `workitem_type` | `list` `retrieve` `resolve` `create` `update` `delete` `import_to_project` |
| `workitem_property` | `list` `retrieve` `create` `update` `delete` `manage_type_properties` `list_options` `retrieve_option` `create_option` `update_option` `delete_option` `get_value` `set_value` `delete_value` |
| `workitem_comment` | `list` `retrieve` `create` `update` `delete` |
| `workitem_link` | `list` `retrieve` `create` `update` `delete` |
| `workitem_relation` | `list` `create` `delete` `list_definitions` `create_definition` `update_definition` `delete_definition` |
| `workitem_activity` | `list` `retrieve` |
| `workitem_attachment` | `list` `read` `download_url` `upload_from_url` `delete` |
| `work_log` | `list` `create` `update` `delete` |
| `page` | `list` `retrieve` `create` `update` `archive` `delete` `set_collection` `list_workitem_pages` `attach_to_workitem` `detach_from_workitem` |
| `project_estimate` | `retrieve` `create` `update` `delete` `link` `list_points` `create_points` `update_point` `delete_point` |
| `release` | `list` `retrieve` `create` `update` `delete` `get_changelog` `update_changelog` `list_workitems` `manage_workitems` |
| `release_tag` | `list` `retrieve` `create` `update` `delete` |
| `release_label` | `list` `create` `update` `delete` `attach` `detach` |
| `customer`, `customer_property`, `customer_request` | CRM-style records (outside the scope of this plugin) |
| `collection` | page collections: `list` `retrieve` `create` `update` `delete` `list_pages` `search_pages` `add_pages` `remove_page` `list_members` `add_member` `update_member` `remove_member` |
| `template` | `list` `create` `update` `delete` |
| `get_pql_reference` | no `action`: the syntax of the `pql` filter used by `workitem` `list` / `list_archived` / `count` and by `cycle` / `module` `list_workitems` |

There are no epic tools: an epic is a `workitem` whose type is "Epic" (`workitem_type(action=resolve, name="Epic")`, then `workitem(action=create, type_id=...)`).

## Tool Name Resolution

The tool names above are **resource names**. The actual MCP tool name is `mcp__<server>__<resource>` and the server segment depends on how Plane is connected (connector, `.mcp.json` entry, self-hosted, cloud). Never assume a specific prefix in this plugin.

To discover the real tool names for the current environment, follow the `connector-bootstrap` skill. In short: use `ToolSearch` with multiple queries (`plane`, `workitem cycle module`, domain keywords), match the resource tools by name, and handle multiple instances when present. The skill also holds a fallback table for servers older than 0.3.0 that expose one tool per operation.