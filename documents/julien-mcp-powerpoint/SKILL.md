---
name: julien-mcp-powerpoint
description: Install PowerPoint MCP via win32com. Use when user needs PowerPoint automation on Windows.
category: mcp
triggers:
  - install powerpoint mcp
  - powerpoint automation
  - pptx mcp
---

# MCP PowerPoint Installer

This skill installs the PowerPoint MCP server into the current project.

## Installation Procedure

When the user asks to install PowerPoint MCP:

1. **Check for existing `.mcp.json`** in the project root
2. **Merge configuration** - Add this server to `mcpServers`:

```json
{
  "powerpoint": {
    "command": "${ONEDRIVE_MCP_PATH}/Office-PowerPoint-MCP-Server/.venv/Scripts/python.exe",
    "args": ["${ONEDRIVE_MCP_PATH}/Office-PowerPoint-MCP-Server/ppt_mcp_server.py"],
    "env": {
      "PYTHONPATH": "${PYTHONPATH_PPT}"
    }
  }
}
```

3. **If `.mcp.json` doesn't exist**, create it with the full structure:

```json
{
  "mcpServers": {
    "powerpoint": {
      "command": "${ONEDRIVE_MCP_PATH}/Office-PowerPoint-MCP-Server/.venv/Scripts/python.exe",
      "args": ["${ONEDRIVE_MCP_PATH}/Office-PowerPoint-MCP-Server/ppt_mcp_server.py"],
      "env": {
        "PYTHONPATH": "${PYTHONPATH_PPT}"
      }
    }
  }
}
```

## Environment Variables Required

- `ONEDRIVE_MCP_PATH`: Path to MCP servers folder
- `PYTHONPATH_PPT`: Python path for PowerPoint server

## Usage After Installation

Restart Claude Code to activate the MCP server.

## Skill Chaining

- **Input**: User request to install PowerPoint MCP
- **Output**: Configured `.mcp.json` with powerpoint server
- **Tools Used**: Read, Edit, Write
- **Chains With**: PowerPoint UVX MCP, Excel win32com MCP

## Troubleshooting

| Problem | Solution |
|---------|----------|
| PowerPoint not found | Ensure Microsoft PowerPoint is installed |
| Python path error | Verify PYTHONPATH_PPT environment variable |
| venv not found | Create venv with `python -m venv .venv` |
| Permission denied | Run terminal as administrator on Windows |
