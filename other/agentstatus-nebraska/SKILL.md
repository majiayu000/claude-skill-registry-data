---
name: agentstatus-nebraska
description: Use the public Nebraska DMV MCP hosted by AgentStatus. No sign-in.
license: MIT
compatibility: Needs the agentstatus MCP server from this package (Streamable HTTP, no sign-in).
metadata:
  homepage: https://nebraska.mcp.agentstatus.dev/
---

# Nebraska DMV

The server at https://nebraska.mcp.agentstatus.dev/ is a public MCP. It does not ask for a key.

1. Read the tool list from that server.
2. Call a tool that the list names, with that tool's arguments.
3. Do not invent a tool name.
