---
name: julien-mcp-word
description: Install Word MCP via win32com/uv. Use when user needs Word document automation on Windows.
category: mcp
triggers:
  - install word mcp
  - word automation
  - docx mcp
---

# MCP Word Installer

This skill installs the Word MCP server into the current project.

## Installation Procedure

When the user asks to install Word MCP:

1. **Check for existing `.mcp.json`** in the project root
2. **Merge configuration** - Add this server to `mcpServers`:

```json
{
  "word": {
    "command": "uv",
    "args": ["run", "--with", "pywin32", "--with", "fastmcp", "fastmcp", "run", "${ONEDRIVE_MCP_PATH}/word-mcp-server-win32com-2/main.py"]
  }
}
```

3. **If `.mcp.json` doesn't exist**, create it with the full structure:

```json
{
  "mcpServers": {
    "word": {
      "command": "uv",
      "args": ["run", "--with", "pywin32", "--with", "fastmcp", "fastmcp", "run", "${ONEDRIVE_MCP_PATH}/word-mcp-server-win32com-2/main.py"]
    }
  }
}
```

## Environment Variables Required

- `ONEDRIVE_MCP_PATH`: Path to MCP servers folder

## Prerequisites

- Windows with Word installed
- uv package manager

## Usage After Installation

Restart Claude Code to activate the MCP server.

## Skill Chaining

- **Input**: User request to install Word MCP
- **Output**: Configured `.mcp.json` with word server
- **Tools Used**: Read, Edit, Write
- **Chains With**: Word UVX MCP, PDF Reader MCP

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Word not found | Ensure Microsoft Word is installed |
| pywin32 error | Run `uv pip install pywin32` |
| Path not found | Verify ONEDRIVE_MCP_PATH environment variable |
| Permission denied | Close Word documents before editing |
