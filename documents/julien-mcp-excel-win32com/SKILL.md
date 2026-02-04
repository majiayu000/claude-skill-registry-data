---
name: julien-mcp-excel-win32com
description: Install Excel MCP via win32com (Windows). Use when user needs native Excel automation on Windows.
category: mcp
triggers:
  - install excel win32com mcp
  - excel native mcp
  - excel windows mcp
---

# MCP Excel Win32COM Installer

This skill installs the Excel Win32COM MCP server into the current project. Uses native Windows COM automation.

## Installation Procedure

When the user asks to install Excel Win32COM MCP:

1. **Check for existing `.mcp.json`** in the project root
2. **Merge configuration** - Add this server to `mcpServers`:

```json
{
  "excel-win32com": {
    "command": "${ONEDRIVE_MCP_PATH}/excel-mcp-server-win32com/venv/Scripts/python.exe",
    "args": ["${ONEDRIVE_MCP_PATH}/excel-mcp-server-win32com/main.py"]
  }
}
```

3. **If `.mcp.json` doesn't exist**, create it with the full structure:

```json
{
  "mcpServers": {
    "excel-win32com": {
      "command": "${ONEDRIVE_MCP_PATH}/excel-mcp-server-win32com/venv/Scripts/python.exe",
      "args": ["${ONEDRIVE_MCP_PATH}/excel-mcp-server-win32com/main.py"]
    }
  }
}
```

## Environment Variables Required

- `ONEDRIVE_MCP_PATH`: Path to MCP servers folder

## Prerequisites

- Windows with Excel installed
- Python with pywin32

## Usage After Installation

Restart Claude Code to activate the MCP server.

## Skill Chaining

- **Input**: User request to install Excel Win32COM MCP
- **Output**: Configured `.mcp.json` with excel-win32com server
- **Tools Used**: Read, Edit, Write
- **Chains With**: Excel uvx MCP for cross-platform

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Excel not found | Ensure Microsoft Excel is installed |
| pywin32 error | Run `pip install pywin32` in venv |
| Path not found | Verify ONEDRIVE_MCP_PATH environment variable |
| File locked | Close Excel files before editing |
