---
name: xhr-documents
description: List, search, and explain authorized company documents and xHR document-management guidance.
---

# xHR Documents

1. Call the bundled `xhr-assistant` MCP server's `read` tool with `skills/documents/SKILL.md`.
2. Follow only child entrypoints declared by that index.
3. Call that same MCP server's `read` tool for the selected leaf and follow its complete instructions.
4. Call that same MCP server's `exec` tool only when the leaf explicitly declares a script.
5. If `exec` returns `AUTHENTICATION_REQUIRED`, ask for explicit confirmation, call `authenticate` with no arguments, and retry the original `exec` once after success.
6. Never request or accept an access token in chat or tool arguments.
7. Respect document access controls and do not infer inaccessible content.
8. Obtain explicit confirmation before an action that changes xHR data.
