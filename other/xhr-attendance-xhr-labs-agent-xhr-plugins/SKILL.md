---
name: xhr-attendance
description: Handle xHR attendance, shifts, timesheets, approvals, attendance reports, and overtime policy workflows.
---

# xHR Attendance

1. Call the bundled `xhr-assistant` MCP server's `read` tool with `skills/attendance/SKILL.md`.
2. Follow only child entrypoints declared by that index.
3. Call that same MCP server's `read` tool for the single matching leaf before taking action.
4. Follow the leaf's validation and execution contract exactly.
5. Call that same MCP server's `exec` tool only for a leaf-declared script and never guess paths.
6. If `exec` returns `AUTHENTICATION_REQUIRED`, ask for explicit confirmation, call `authenticate` with no arguments, and retry the original `exec` once after success.
7. Never request or accept an access token in chat or tool arguments.
8. Obtain explicit confirmation before an action that changes xHR data.
