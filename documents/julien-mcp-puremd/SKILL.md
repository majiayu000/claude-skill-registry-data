---
name: julien-mcp-puremd
description: Install PureMD MCP for web-to-markdown. Use when user needs to convert web pages to markdown.
category: mcp
triggers:
  - install puremd mcp
  - web to markdown
  - puremd
---

# MCP Pure.md Installer

This skill installs the Pure.md MCP server into the current project.

## Installation Procedure

When the user asks to install Pure.md MCP:

1. **Check for existing `.mcp.json`** in the project root
2. **Merge configuration** - Add this server to `mcpServers`:

```json
{
  "puremd": {
    "command": "cmd",
    "args": ["/c", "npx", "-y", "puremd-mcp"],
    "env": {
      "PUREMD_API_KEY": "${PUREMD_API_KEY}"
    }
  }
}
```

3. **If `.mcp.json` doesn't exist**, create it with the full structure:

```json
{
  "mcpServers": {
    "puremd": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "puremd-mcp"],
      "env": {
        "PUREMD_API_KEY": "${PUREMD_API_KEY}"
      }
    }
  }
}
```

## Environment Variables Required

- `PUREMD_API_KEY`: Your Pure.md API key

## Usage After Installation

Restart Claude Code to activate the MCP server.

## Skill Chaining

- **Input**: User request to install PureMD MCP
- **Output**: Configured `.mcp.json` with puremd server
- **Tools Used**: Read, Edit, Write
- **Chains With**: Jina MCP for web content extraction

## Troubleshooting

| Problem | Solution |
|---------|----------|
| API key invalid | Get new key from pure.md |
| `npx` not found | Install Node.js and ensure npm is in PATH |
| Conversion failed | Check URL is accessible |
| Rate limit exceeded | Upgrade PureMD plan or add delay |
