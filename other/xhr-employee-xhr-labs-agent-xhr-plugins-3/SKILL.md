---
name: xhr-employee
description: Find xHR employee profiles, organizational information, managers, departments, and employee guidance, and present the People workforce dashboard (workforce structure, headcount trends, movement, offboarding reports).
---

# xHR Employee

1. Call the bundled `xhr-assistant` MCP server's `read` tool with `skills/employee/SKILL.md`.
2. Navigate only through entrypoints declared by the index.
3. Call that same MCP server's `read` tool for the selected leaf and follow it completely.
4. Use that same MCP server's `exec` tool only when that leaf declares an executable script.
5. If `exec` returns `AUTHENTICATION_REQUIRED`, ask for explicit confirmation, call `authenticate` with no arguments, and retry the original `exec` once after success.
6. Never request or accept an access token in chat or tool arguments.
7. Never infer restricted employee data or bypass authorization checks.
8. Obtain explicit confirmation before an action that changes xHR data.
