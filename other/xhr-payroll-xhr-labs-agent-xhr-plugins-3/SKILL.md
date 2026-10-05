---
name: xhr-payroll
description: Handle xHR payroll setup, pay components, earnings, payslips, pay runs, tax, and statutory guidance.
---

# xHR Payroll

1. Call the bundled `xhr-assistant` MCP server's `read` tool with `skills/payroll/SKILL.md`.
2. Follow only index-declared child entrypoints.
3. Call that same MCP server's `read` tool for the selected leaf before responding or executing.
4. Follow the leaf's required lookup and validation sequence.
5. Call that same MCP server's `exec` tool only for a script explicitly declared by the leaf.
6. If `exec` returns `AUTHENTICATION_REQUIRED`, ask for explicit confirmation, call `authenticate` with no arguments, and retry the original `exec` once after success.
7. Never request or accept an access token in chat or tool arguments.
8. Treat payroll data as sensitive and return only authorized information.
9. Obtain explicit confirmation before an action that changes xHR data.
