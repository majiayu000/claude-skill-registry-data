---
name: julien-mcp-youtube-info
description: Install YouTube Info MCP for video data. Use when user needs YouTube video information extraction.
category: mcp
triggers:
  - install youtube mcp
  - youtube info
  - video info mcp
---

# MCP YouTube Info Installer

This skill installs the YouTube Info MCP server into the current project.

## Installation Procedure

When the user asks to install YouTube Info MCP:

1. **Check for existing `.mcp.json`** in the project root
2. **Merge configuration** - Add this server to `mcpServers`:

```json
{
  "youtube-info": {
    "command": "cmd",
    "args": ["/c", "npx", "-y", "@limecooler/yt-info-mcp"]
  }
}
```

3. **If `.mcp.json` doesn't exist**, create it with the full structure:

```json
{
  "mcpServers": {
    "youtube-info": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@limecooler/yt-info-mcp"]
    }
  }
}
```

## Prerequisites

- Node.js and npm installed

## Usage After Installation

Restart Claude Code to activate the MCP server. Provides YouTube video information extraction.

## Skill Chaining

- **Input**: User request to install YouTube Info MCP
- **Output**: Configured `.mcp.json` with youtube-info server
- **Tools Used**: Read, Edit, Write
- **Chains With**: Any media processing workflow

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `npx` not found | Install Node.js and ensure npm is in PATH |
| Video not found | Check YouTube URL is valid and public |
| Rate limited | YouTube API limits - wait and retry |
| Data incomplete | Some videos may have restricted metadata |
