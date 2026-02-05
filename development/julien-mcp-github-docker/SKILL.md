---
name: julien-mcp-github-docker
description: Install GitHub MCP via Docker. Use when user needs GitHub integration through Docker container.
category: mcp
triggers:
  - install github docker mcp
  - github mcp docker
  - github integration docker
---

# MCP GitHub (Docker) Installer

This skill installs the GitHub MCP server via Docker into the current project.

## Installation Procedure

When the user asks to install GitHub Docker MCP:

1. **Check for existing `.mcp.json`** in the project root
2. **Merge configuration** - Add this server to `mcpServers`:

```json
{
  "github-docker": {
    "command": "docker",
    "args": ["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghcr.io/github/github-mcp-server"],
    "env": {
      "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
    }
  }
}
```

3. **If `.mcp.json` doesn't exist**, create it with the full structure:

```json
{
  "mcpServers": {
    "github-docker": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghcr.io/github/github-mcp-server"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    }
  }
}
```

## Environment Variables Required

- `GITHUB_PERSONAL_ACCESS_TOKEN`: Your GitHub Personal Access Token

## Prerequisites

- Docker installed and running

## Usage After Installation

Restart Claude Code to activate the MCP server.

## Skill Chaining

- **Input**: User request to install GitHub Docker MCP
- **Output**: Configured `.mcp.json` with github-docker server
- **Tools Used**: Read, Edit, Write
- **Chains With**: GitHub HTTP MCP as alternative

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Docker not running | Start Docker Desktop |
| Image pull failed | Check network and Docker Hub access |
| Token invalid | Generate new PAT at github.com/settings/tokens |
| Permission denied | Run Docker with appropriate permissions |
