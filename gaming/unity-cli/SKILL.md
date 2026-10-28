---
name: unity-cli
description: "Install and use unity-mcp-cli: Node.js requirements, npm installation, npx, tool calls, JSON input files and troubleshooting."
metadata:
  generated-by: unity-mcp
  ai-game-dev: exclude
---
# Unity CLI

Install and use `unity-mcp-cli` to call the engine's MCP tools from a terminal.

## Prerequisites

Node.js ^20.19.0 or >=22.12.0 and npm are required. Node.js 21 is unsupported.
Check existing installations first:

```powershell
node --version
npm.cmd --version
```

If needed, install a supported Node.js LTS release from https://nodejs.org/ and reopen the terminal.
Use the Windows installer and reopen PowerShell. The examples use .cmd launchers to avoid npm PowerShell execution-policy restrictions.

## Install and verify

```powershell
npm.cmd install -g unity-mcp-cli
unity-mcp-cli.cmd --version
unity-mcp-cli.cmd --help
```

Alternatively, use npm's temporary runner without a global installation:

```powershell
npx.cmd unity-mcp-cli --help
```

Replace the leading `unity-mcp-cli.cmd` with `npx.cmd unity-mcp-cli` in subsequent examples when using this option.

## Call tools

Run commands from the game project's root directory. The target editor or game must be running with its MCP plugin connected.
The following read-only example lists the available RQL sources and types in the editor:

```powershell
unity-mcp-cli.cmd status
unity-mcp-cli.cmd run-tool rql-schema --input '{}'
```

For input files, create a UTF-8 JSON file and pass its path. This example makes the same read-only call:

```powershell
[System.IO.File]::WriteAllText((Join-Path $PWD 'args.json'), '{}')
unity-mcp-cli.cmd run-tool rql-schema --input-file args.json
```

Replace `rql-schema` and the JSON with the tool name and arguments from its individual skill.
Use command-specific `--help` for options. RQL tools require an editor; a game exposes only its registered runtime tools.

## Troubleshooting

- `node` or `npm.cmd` not found: finish installing Node.js, check PATH, and reopen the terminal.
- `unity-mcp-cli.cmd` not found: reopen the terminal, check the npm global executable directory in PATH, or use `npx.cmd unity-mcp-cli`.
- Global npm installation denied: use a user-owned Node.js installation or the npx alternative.
- Connection unavailable: check the project directory and ensure its editor or game and MCP plugin are running and connected.

For optional asset-generation and Blender workflows, consult the `ai-game-dev-app` skill.
