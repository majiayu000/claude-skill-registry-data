---
name: notion-constraint-memory
description: Use the constraint-memory MCP tools to query/upsert timeboxing constraints stored in Notion.
compatibility: network
metadata:
  owner: fateforger
  version: "0.1.0"
---

Use this skill when working with the timeboxing preference memory stored in Notion.
Do NOT call Notion APIs directly; use the MCP tools from the constraint-memory server.

Tools
- `constraint_get_store_info()`
- `constraint_get_constraint(uid)`
- `constraint_query_types(stage, event_types)`
- `constraint_query_constraints(filters, type_ids, tags, sort, limit)`
- `constraint_upsert_constraint(record, event)`
- `constraint_log_event(event)`
- `constraint_seed_types()`

Server
- Script: `scripts/constraint_mcp_server.py`
- Transport: stdio (recommended)

Environment
- `NOTION_TOKEN`: Notion integration token.
- `NOTION_TIMEBOXING_PARENT_PAGE_ID`: parent page where the DBs live.

Usage notes
- Always call `constraint_query_types` before expanding to constraint queries.
- Use `constraint_upsert_constraint` with an event payload for audit logging when possible.
