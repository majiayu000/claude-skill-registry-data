---
name: tool-installer
description: Registers or imports MCP (Model Context Protocol) servers in LibrAgent or Claude Desktop. Use when users share new MCP connection info (npm/npx package, GitHub URL, config JSON) or want to import, sync, or bring settings from Cursor, VS Code, Windsurf, and similar editors.
---

# MCP Installer

This skill registers MCP servers into the current LibrAgent session or the user's Claude Desktop configuration. It covers both **direct installation** (from packages or URLs) and **import/sync** (from other AI editors).

## 🚀 Workflow

### Step 0: Determine Input Path

| User intent | Path |
| --- | --- |
| "Import from Cursor", "sync my MCP servers", "what's installed elsewhere?" | **Import** → below |
| npm package, GitHub URL, or pasted JSON config | **Direct install** → below |

### Import Workflow

1. **Identify sources** — Consult [app_paths.md](references/app_paths.md) for config locations.
2. **Scan** — Read detected config files. Resolve environment variables (`%APPDATA%`, `%USERPROFILE%`, `~`) before reading. If a project-level config (e.g., `.cursor/mcp.json`) exists in the current workspace, prioritize it.
3. **Compare** — List all found MCP servers. Use `tool__listServers` to compare with LibrAgent's current registrations. Mark servers as new or already registered.
4. **Select** — Present the list to the user. Ask which servers to import (all or specific ones).
5. **Register** — Use `tool__registerServer` for each selected server. Skip duplicates (same name and command).
6. **(Optional)** — Offer to update `claude_desktop_config.json` as well.

**Schema notes:** VS Code Copilot uses `servers` as the root key; Zed uses `context_servers`. Normalize entries before registration.

### Direct Install Workflow

#### 1. Analyze Information

Identify the source and transport details.

- **npx/npm**: Use `npx -y <package>` for registration.
- **GitHub**: Determine if it's TypeScript (needs build) or Python (can use `uvx`).
- **Claude Config**: Extract command, args, and env variables.

#### 2. Register in LibrAgent

Use the `tool__registerServer` tool to add the MCP server.

**Example Task:**
"Register the 'everything' MCP server using npx."

**Execution:**
```json
{
  "name": "everything",
  "description": "MCP server with all capabilities",
  "transport": {
    "type": "stdio",
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-everything"]
  }
}
```

#### 3. Claude Desktop (Optional)

If the user specifically asks to install it in Claude Desktop:

1. Locate `claude_desktop_config.json` (see [app_paths.md](references/app_paths.md)).
2. Read the current configuration.
3. Append the new server entry.
4. Save the file and notify the user to restart Claude Desktop.

## 🛠 Guidelines

- **Duplicate Prevention**: Do not register servers that already exist in LibrAgent with the same name and command.
- **Naming**: Use lowercase slugs (e.g., `github`, `brave-search`).
- **Safety**: Verify the source before execution. If it requires sensitive environment variables, ask the user to provide them or use the `workspace__runInPersistentPowerShell` tool if input is needed.
- **Dependencies**: Use [setup-wizard](../setup-wizard/SKILL.md) if `node`, `npm`, or `uv` are missing.
- **Path Resolution**: Resolve environment variables before reading config files on any platform.

## Reference

- [installation.md](references/installation.md): npm, GitHub, and Python install patterns
- [app_paths.md](references/app_paths.md): Config paths for Cursor, VS Code, Windsurf, and other editors
