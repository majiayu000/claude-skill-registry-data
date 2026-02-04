---
name: julien-mcp-github-http
description: Install GitHub MCP via HTTP/Copilot API. Use when user needs GitHub Copilot MCP endpoint.
category: mcp
triggers:
  - install github http mcp
  - github copilot mcp
  - copilot api
---

# MCP GitHub HTTP Installer

This skill installs the GitHub HTTP MCP server into the current project (uses Copilot API).

## Installation Procedure

When the user asks to install GitHub HTTP MCP:

1. **Check for existing `.mcp.json`** in the project root
2. **Merge configuration** - Add this server to `mcpServers`:

```json
{
  "github-http": {
    "type": "http",
    "url": "https://api.githubcopilot.com/mcp/",
    "headers": {
      "Authorization": "Bearer ${GITHUB_PERSONAL_ACCESS_TOKEN2}"
    }
  }
}
```

3. **If `.mcp.json` doesn't exist**, create it with the full structure:

```json
{
  "mcpServers": {
    "github-http": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer ${GITHUB_PERSONAL_ACCESS_TOKEN2}"
      }
    }
  }
}
```

## Environment Variables Required

- `GITHUB_PERSONAL_ACCESS_TOKEN2`: Your GitHub Copilot token

## Usage After Installation

Restart Claude Code to activate the MCP server.

## Skill Chaining

- **Input**: User request to install GitHub HTTP MCP
- **Output**: Configured `.mcp.json` with github-http server
- **Tools Used**: Read, Edit, Write
- **Chains With**: GitHub Docker MCP as alternative

## Troubleshooting

| Problem | Solution |
|---------|----------|
| 401 Unauthorized | Check GITHUB_PERSONAL_ACCESS_TOKEN2 is valid |
| Copilot not enabled | Ensure GitHub Copilot subscription is active |
| Rate limit exceeded | Wait or use a different token |
| Connection refused | Check network and GitHub API status |
