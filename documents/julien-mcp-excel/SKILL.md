---
name: julien-mcp-excel
description: Install Excel MCP server via uvx. Use when user needs Excel file manipulation capabilities.
category: mcp
triggers:
  - install excel mcp
  - excel automation
  - xlsx mcp
---

# MCP Excel Installer

This skill installs the Excel MCP server into the current project.

## Installation Procedure

When the user asks to install Excel MCP:

1. **Check for existing `.mcp.json`** in the project root
2. **Merge configuration** - Add this server to `mcpServers`:

```json
{
  "excel": {
    "command": "uvx",
    "args": ["excel-mcp-server", "stdio"]
  }
}
```

3. **If `.mcp.json` doesn't exist**, create it with the full structure:

```json
{
  "mcpServers": {
    "excel": {
      "command": "uvx",
      "args": ["excel-mcp-server", "stdio"]
    }
  }
}
```

## Prerequisites

- `uvx` must be installed (comes with `uv`)

## Usage After Installation

Restart Claude Code to activate the MCP server. Provides Excel file manipulation capabilities.

## Example Usage

After installation, use in Claude Code:
```
"Read data from sheet1 of report.xlsx"
"Create a new Excel file with sales data"
```

## Skill Chaining

- **Input**: User request to install Excel MCP
- **Output**: Configured `.mcp.json` with excel server
- **Tools Used**: Read, Edit, Write
- **Chains With**: Excel win32com MCP for Windows-native features

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `uvx` not found | Install `uv` from astral.sh |
| Package not found | Run `uv cache clean` |
| File not found | Use absolute paths for Excel files |
| Permission denied | Check write permissions on output directory |
