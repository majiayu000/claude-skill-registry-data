---
name: julien-mcp-gmail
description: Install Gmail MCP for email operations. Use when user needs Gmail read/send capabilities.
category: mcp
triggers:
  - install gmail mcp
  - gmail integration
  - email mcp gmail
---

# MCP Gmail Installer

This skill installs the Gmail MCP server into the current project.

## Installation Procedure

When the user asks to install Gmail MCP:

1. **Check for existing `.mcp.json`** in the project root
2. **Merge configuration** - Add this server to `mcpServers`:

```json
{
  "gmail": {
    "command": "node",
    "args": ["${ONEDRIVE_MCP_PATH}/Gmail-MCP-Server/dist/index.js"]
  }
}
```

3. **If `.mcp.json` doesn't exist**, create it with the full structure:

```json
{
  "mcpServers": {
    "gmail": {
      "command": "node",
      "args": ["${ONEDRIVE_MCP_PATH}/Gmail-MCP-Server/dist/index.js"]
    }
  }
}
```

## Environment Variables Required

- `ONEDRIVE_MCP_PATH`: Path to MCP servers folder

## Prerequisites

- Node.js installed
- Gmail OAuth credentials configured

## Usage After Installation

Restart Claude Code to activate the MCP server.

## Example Usage

After installation, use in Claude Code:
```
"Read my latest 5 emails"
"Send an email to user@example.com"
```

## Skill Chaining

- **Input**: User request to install Gmail MCP
- **Output**: Configured `.mcp.json` with gmail server
- **Tools Used**: Read, Edit, Write
- **Chains With**: Outlook MCP for multi-provider email

## Troubleshooting

| Problem | Solution |
|---------|----------|
| OAuth error | Re-run Gmail OAuth setup, check credentials.json |
| Path not found | Verify ONEDRIVE_MCP_PATH environment variable |
| Server crash | Check dist/index.js exists, rebuild if needed |
| Permission denied | Ensure OAuth scopes include required permissions |
