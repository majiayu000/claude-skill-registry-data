---
name: agentstatus-index
description: Search the public AgentStatus MCP Index and call a tool on a listed public server. Use when the user wants an MCP server for a job, a comparison of public servers, or a call to a tool those servers publish.
license: MIT
compatibility: Needs the agentstatus MCP server from this package (Streamable HTTP, no sign-in).
metadata:
  homepage: https://agentstatus.dev/mcp-index
  docs: https://github.com/Carmel-Labs-Inc/agentstatus-mcp-index
---

# AgentStatus Index

The server at https://index.mcp.agentstatus.dev/mcp is a public directory. It does not ask the user to sign in and it does not store third-party credentials.

This connection lists six tools. It does not list the catalog. Search or recommend first, then call.

## How to work

1. Use `search_records` or `recommend_records` for the job. Optional host is `cursor`, `copilot`, or `vscode`.
2. Use `get_record` for one server, `compare_records` for two to five, and `list_sections` for the section names.
3. Call a tool that the match lists with `call_indexed_tool`. Pass the slug, the tool name, and that tool's arguments.
4. Do not invent a server or a tool name. If the Index has no match, say so.
5. Do not call a tool whose name deletes, destroys, drops, wipes, truncates, shuts down, or formats a disk. The Index does not forward those names.

`call_indexed_tool` sends that one call to the public server the user already picked and returns that server's result.
