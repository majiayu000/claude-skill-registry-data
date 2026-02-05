---
name: julien-mcp-chrome-devtools
description: Install Chrome DevTools MCP for browser debugging. Use when user needs Chrome DevTools Protocol integration.
category: mcp
triggers:
  - install chrome devtools mcp
  - chrome debugging
  - devtools mcp
---

# MCP Chrome DevTools Installer

This skill installs the Chrome DevTools MCP server into the current project.

## Installation Procedure

When the user asks to install Chrome DevTools MCP:

1. **Check for existing `.mcp.json`** in the project root
2. **Merge configuration** - Add this server to `mcpServers`:

```json
{
  "chrome-devtools": {
    "command": "cmd",
    "args": ["/c", "npx", "-y", "chrome-devtools-mcp@latest"]
  }
}
```

3. **If `.mcp.json` doesn't exist**, create it with the full structure:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

## Prerequisites

- Chrome browser must be running with remote debugging enabled
- Node.js and npm installed

## Usage After Installation

Restart Claude Code to activate the MCP server.

## Skill Chaining

- **Input**: User request to install Chrome DevTools MCP
- **Output**: Configured `.mcp.json` with chrome-devtools server
- **Tools Used**: Read, Edit, Write
- **Chains With**: Playwright MCP for automation

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Chrome not running | Start Chrome with `--remote-debugging-port=9222` |
| `npx` not found | Install Node.js and ensure npm is in PATH |
| Connection refused | Check debugging port is correct (default 9222) |
| Tab not found | Ensure target page is open in Chrome |
