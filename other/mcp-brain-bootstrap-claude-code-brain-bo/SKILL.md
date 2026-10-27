---
name: mcp
description: Manage MCP (Model Context Protocol) servers — list configured tools, check status, show invocation format, or add a new server to .claude/settings.json.
---

# MCP Skill

Manage Model Context Protocol (MCP) servers for this project.

## Usage

```
/mcp                    # List configured servers + invocation format
/mcp status             # Check which tool binaries are installed
/mcp add <server>       # Add a new MCP server
/mcp format             # Show all tool invocation strings
```

## MCP Tool Invocation Format

```
mcp__SERVER_KEY__TOOL_FUNCTION_NAME
```

Where `SERVER_KEY` is the server key in `.claude/settings.json` under `mcpServers.*`.

## Instructions

### If `list` or empty:
1. Read `.claude/settings.json` — show currently configured `mcpServers` entries
2. Show invocation format for each tool
3. Suggest additional servers based on tech stack in `claude/architecture.md`

### If `status`:
1. Check which MCP binaries are installed:
   ```bash
   command -v uvx &>/dev/null && echo "uvx: ✅" || echo "uvx: ❌ missing — install via: pip install uv"
   command -v npx &>/dev/null && echo "npx: ✅" || echo "npx: ⚠️ missing — install Node.js"
   command -v ccc &>/dev/null && echo "cocoindex CLI (ccc): ✅" || echo "cocoindex CLI: ⚠️ optional — install via: pip install cocoindex"
   # uvx-based tools (codebase-memory, code-review-graph, serena, cocoindex-code) are available when uvx is installed
   ```

### If `add <server-name>`:
1. **Prefer CLI:** `claude mcp add <server-name> -- <command> [args]`
   - Example: `claude mcp add context7 -- npx -y @upstash/context7-mcp`
2. Or manually add to `.claude/settings.json` under `mcpServers.<name>`
3. For HTTP servers requiring OAuth: authenticate after configuration
4. Update `CLAUDE.md` — add to Plugin Ecosystem section

### If `format`:
Show all available MCP tool invocations from `.claude/settings.json`.

## Pre-Configured MCP Stack

| MCP Server Key | Binary | Invocation prefix |
|----------------|--------|-------------------|
| `codebase-memory` | `uvx codebase-memory-mcp@latest` | `mcp__codebase-memory__` |
| `cocoindex-code` | `uvx cocoindex-code-mcp-server@latest` | `mcp__cocoindex-code__` |
| `code-review-graph` | `uvx code-review-graph@latest` | `mcp__code-review-graph__` |
| `serena` | `uvx serena@latest` | `mcp__serena__` |
| `playwright` | `npx @playwright/mcp@latest` | `mcp__playwright__` |

## Adding a New Server — .claude/settings.json Format

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@github/mcp-server"],
      "env": { "GITHUB_TOKEN": "YOUR_GITHUB_TOKEN_HERE" }
    },
    "figma": {
      "url": "https://mcp.figma.com/mcp",
      "headers": { "Authorization": "Bearer YOUR_FIGMA_TOKEN_HERE" }
    }
  }
}
```

## Security Rules

- **NEVER** hardcode API keys — use env var placeholders like `"YOUR_KEY_HERE"`
- For DB tools: prefer **read-only** access unless write is explicitly required
- After any config changes, restart Claude Code for MCP servers to take effect
