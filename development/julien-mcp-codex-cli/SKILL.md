---
name: julien-mcp-codex-cli
description: Install Codex CLI MCP assistant. Use when user needs Codex CLI capabilities in their project.
category: mcp
triggers:
  - install codex cli mcp
  - codex mcp
  - codex cli
---

# MCP Codex CLI Installer

This skill installs the Codex CLI MCP server into the current project.

## Installation Procedure

When the user asks to install Codex CLI MCP:

1. **Check for existing `.mcp.json`** in the project root
2. **Merge configuration** - Add this server to `mcpServers`:

```json
{
  "codex-cli": {
    "command": "cmd",
    "args": ["/c", "npx", "-y", "codex-mcp-server"]
  }
}
```

3. **If `.mcp.json` doesn't exist**, create it with the full structure:

```json
{
  "mcpServers": {
    "codex-cli": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "codex-mcp-server"]
    }
  }
}
```

## Prerequisites

- Node.js and npm installed

## Usage After Installation

Restart Claude Code to activate the MCP server.

## Skill Chaining

- **Input**: User request to install Codex CLI MCP
- **Output**: Configured `.mcp.json` with codex-cli server
- **Tools Used**: Read, Edit, Write
- **Chains With**: Any code analysis workflow

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `npx` not found | Install Node.js and ensure npm is in PATH |
| Server timeout | Check network connectivity |
| Command failed | Verify codex-mcp-server package exists |
| Permission denied | Run terminal as administrator on Windows |
