---
name: julien-mcp-word-uvx
description: Install Word MCP via uvx. Use when user needs cross-platform Word capabilities.
category: mcp
triggers:
  - install word uvx mcp
  - word uvx
  - docx mcp uvx
---

# MCP Word UVX Installer

This skill installs the Word MCP server via uvx into the current project.

## Installation Procedure

When the user asks to install Word UVX MCP:

1. **Check for existing `.mcp.json`** in the project root
2. **Merge configuration** - Add this server to `mcpServers`:

```json
{
  "word-uvx": {
    "command": "uvx",
    "args": ["--from", "office-word-mcp-server", "word_mcp_server"]
  }
}
```

3. **If `.mcp.json` doesn't exist**, create it with the full structure:

```json
{
  "mcpServers": {
    "word-uvx": {
      "command": "uvx",
      "args": ["--from", "office-word-mcp-server", "word_mcp_server"]
    }
  }
}
```

## Prerequisites

- `uvx` must be installed (comes with `uv`)

## Usage After Installation

Restart Claude Code to activate the MCP server.

## Skill Chaining

- **Input**: User request to install Word UVX MCP
- **Output**: Configured `.mcp.json` with word-uvx server
- **Tools Used**: Read, Edit, Write
- **Chains With**: Word win32com MCP, PowerPoint UVX MCP

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `uvx` not found | Install `uv` from astral.sh |
| Package not found | Run `uv cache clean` |
| Python version error | Ensure Python 3.8+ is installed |
| File not found | Use absolute paths for Word documents |
