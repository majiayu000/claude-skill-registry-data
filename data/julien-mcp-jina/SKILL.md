---
name: julien-mcp-jina
description: Install Jina AI MCP for web scraping. Use when user needs Jina Reader for URL content extraction.
category: mcp
triggers:
  - install jina mcp
  - jina reader
  - web scraping mcp
---

# MCP Jina AI Installer

This skill installs the Jina AI MCP server into the current project.

## Installation Procedure

When the user asks to install Jina MCP:

1. **Check for existing `.mcp.json`** in the project root
2. **Merge configuration** - Add this server to `mcpServers`:

```json
{
  "jina": {
    "command": "cmd",
    "args": ["/c", "npx", "-y", "@smithery/cli@latest", "run", "jina-ai-mcp-server", "--key", "${JINA_API_KEY}"],
    "env": {
      "JINA_API_KEY": "${JINA_API_KEY}"
    }
  }
}
```

3. **If `.mcp.json` doesn't exist**, create it with the full structure:

```json
{
  "mcpServers": {
    "jina": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@smithery/cli@latest", "run", "jina-ai-mcp-server", "--key", "${JINA_API_KEY}"],
      "env": {
        "JINA_API_KEY": "${JINA_API_KEY}"
      }
    }
  }
}
```

## Environment Variables Required

- `JINA_API_KEY`: Your Jina AI API key

## Usage After Installation

Restart Claude Code to activate the MCP server.

## Skill Chaining

- **Input**: User request to install Jina MCP
- **Output**: Configured `.mcp.json` with jina server
- **Tools Used**: Read, Edit, Write
- **Chains With**: PureMD MCP for web content extraction

## Troubleshooting

| Problem | Solution |
|---------|----------|
| API key invalid | Get new key at jina.ai |
| `npx` not found | Install Node.js and ensure npm is in PATH |
| Smithery CLI error | Try `npm cache clean --force` |
| Rate limit exceeded | Upgrade Jina plan or add delay |
