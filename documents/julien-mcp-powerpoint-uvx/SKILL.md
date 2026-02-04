---
name: julien-mcp-powerpoint-uvx
description: Install PowerPoint MCP via uvx. Use when user needs cross-platform PowerPoint capabilities.
category: mcp
triggers:
  - install powerpoint uvx
  - pptx mcp uvx
  - powerpoint uvx
---

# MCP PowerPoint UVX Installer

This skill installs the PowerPoint MCP server via uvx into the current project.

## Installation Procedure

When the user asks to install PowerPoint UVX MCP:

1. **Check for existing `.mcp.json`** in the project root
2. **Merge configuration** - Add this server to `mcpServers`:

```json
{
  "powerpoint-uvx": {
    "command": "uvx",
    "args": ["--from", "office-powerpoint-mcp-server", "ppt_mcp_server"]
  }
}
```

3. **If `.mcp.json` doesn't exist**, create it with the full structure:

```json
{
  "mcpServers": {
    "powerpoint-uvx": {
      "command": "uvx",
      "args": ["--from", "office-powerpoint-mcp-server", "ppt_mcp_server"]
    }
  }
}
```

## Prerequisites

- `uvx` must be installed (comes with `uv`)

## Usage After Installation

Restart Claude Code to activate the MCP server.

## Skill Chaining

- **Input**: User request to install PowerPoint UVX MCP
- **Output**: Configured `.mcp.json` with powerpoint-uvx server
- **Tools Used**: Read, Edit, Write
- **Chains With**: PowerPoint win32com MCP, Word UVX MCP

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `uvx` not found | Install `uv` from astral.sh |
| Package not found | Run `uv cache clean` |
| Python version error | Ensure Python 3.8+ is installed |
| Permission denied | Check write permissions on output directory |
