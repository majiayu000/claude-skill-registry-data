---
name: xhr-workbench
description: Handle xHR Workbench projects, tasks, sprints, task comments and linked tasks, time logging, custom fields, project members, wiki pages, statuses, priorities, and project progress reports.
---

# xHR Workbench

1. Call the bundled `xhr-assistant` MCP server's `read` tool with `skills/workbench/SKILL.md`.
2. Follow only child entrypoints declared by that index.
3. Call that same MCP server's `read` tool for the single leaf matching the requested outcome.
4. Follow the leaf's filters, identifiers, and execution contract exactly.
5. Call that same MCP server's `exec` tool only for a leaf-declared script and never probe paths.
6. If `exec` returns `AUTHENTICATION_REQUIRED`, ask for explicit confirmation, call `authenticate` with no arguments, and retry the original `exec` once after success.
7. Never request or accept an access token in chat or tool arguments.
8. Obtain explicit confirmation before creating or changing xHR data.
