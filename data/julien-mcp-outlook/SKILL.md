---
name: julien-mcp-outlook
description: Install Outlook MCP via win32com. Use when user needs Outlook email automation on Windows.
category: mcp
triggers:
  - install outlook mcp
  - outlook automation
  - email mcp
---

# MCP Outlook Installer

This skill installs the Outlook MCP server into the current project.

## Installation Procedure

When the user asks to install Outlook MCP:

1. **Check for existing `.mcp.json`** in the project root
2. **Merge configuration** - Add this server to `mcpServers`:

```json
{
  "outlook": {
    "command": "${ONEDRIVE_MCP_PATH}/outlook-mcp-server/venv/Scripts/python.exe",
    "args": ["${ONEDRIVE_MCP_PATH}/outlook-mcp-server/main.py"]
  }
}
```

3. **If `.mcp.json` doesn't exist**, create it with the full structure:

```json
{
  "mcpServers": {
    "outlook": {
      "command": "${ONEDRIVE_MCP_PATH}/outlook-mcp-server/venv/Scripts/python.exe",
      "args": ["${ONEDRIVE_MCP_PATH}/outlook-mcp-server/main.py"]
    }
  }
}
```

## Environment Variables Required

- `ONEDRIVE_MCP_PATH`: Path to MCP servers folder

## Prerequisites

- Windows with Outlook installed
- Python with pywin32

## Usage After Installation

Restart Claude Code to activate the MCP server.

## Skill Chaining

- **Input**: User request to install Outlook MCP
- **Output**: Configured `.mcp.json` with outlook server
- **Tools Used**: Read, Edit, Write
- **Chains With**: Gmail MCP for multi-provider email

## Troubleshooting

| Problem | Solution |
|---------|----------|
| pywin32 error | Run `pip install pywin32` in venv |
| Outlook not found | Ensure Outlook desktop app is installed |
| Path not found | Verify ONEDRIVE_MCP_PATH environment variable |
| Permission denied | Grant Outlook access when prompted |
