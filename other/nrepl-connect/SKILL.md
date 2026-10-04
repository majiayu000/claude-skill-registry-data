---
name: nrepl-connect
description: Connect to the project's nREPL server using the nrepl MCP tool
---

# Connect to nREPL

Connect to the running nREPL server using the `mcp__nrepl__connect` tool.

## Steps

1. Try connecting on port **7888** first (the default dev port).
2. If that fails, read the `.nrepl-port` file from the workspace root to get the actual port number, then connect using that port.
3. Host is always `localhost`.
4. After connecting, verify with a simple eval like `(+ 1 1)`.
