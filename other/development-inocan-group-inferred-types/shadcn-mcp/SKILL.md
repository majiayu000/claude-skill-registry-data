---
name: shadcn-mcp
description: Install and configure the shadcn MCP server for Codex. Use when a user asks to enable shadcn/ui MCP tools, set up the shadcn MCP server in Codex, or troubleshoot shadcn MCP startup.
---

# Shadcn Mcp

## Overview

Install the shadcn MCP server and wire it into Codex so Codex can browse and install shadcn/ui components. This covers running the shadcn MCP init command, updating `~/.codex/config.toml`, and restarting Codex.

## Workflow

### 1. Choose the project context

Run the init command from any project directory where shadcn config makes sense (typically the frontend project where you use shadcn). Confirm the working directory if the user has multiple repos.

### 2. Run the shadcn MCP init command

Use the official command (requires network access):

```bash
npx shadcn@latest mcp init --client codex
```

If `npx` is not found in Codex environments (common with nvm), locate it and use the full path or ensure PATH includes it.

### 3. Add the MCP server to Codex config

Update `~/.codex/config.toml` (create it if missing) with:

```toml
[mcp_servers.shadcn]
command = "npx"
args = ["shadcn@latest", "mcp"]
```

If you must use a full path to `npx`, update `command` accordingly.

### 4. Restart Codex and verify

Restart Codex. On startup, confirm the `shadcn` MCP server initializes successfully (no MCP startup errors).

### 5. Troubleshoot common issues

- If the MCP server fails to start, check that `npx` is available in the Codex environment.
- If the config already contains a `mcp_servers` block, merge the `shadcn` entry without overwriting other servers.
