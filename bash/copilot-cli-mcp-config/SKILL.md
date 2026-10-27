---
name: copilot-cli-mcp-config
description: Manage GitHub Copilot CLI MCP server configuration, including ~/.copilot/mcp-config.json, COPILOT_HOME or --config-dir, project-level .mcp.json/.github/mcp.json/.vscode/mcp.json, /mcp commands, --additional-mcp-config, and VS Code mcp.json migration.
metadata:
  author: arisng
  version: 1.1.0
---

# GitHub Copilot CLI MCP Configuration Management

Configure MCP servers for GitHub Copilot CLI using the `mcp-config.json` file, which uses different syntax from VS Code's `mcp.json`.

## Configuration Location

**Default**: `~/.copilot/mcp-config.json`

**Relocating the config directory** (precedence, highest first):

1. `--config-dir` CLI flag: `copilot --config-dir /path/to/dir`
2. `COPILOT_HOME` environment variable: `export COPILOT_HOME=/path/to/dir`
3. Default `~/.copilot/`

Setting either option redirects the entire config tree (agents, skills, MCP config, logs, sessions).

**Project-level MCP configs**: `.mcp.json`, `.github/mcp.json`, or `.vscode/mcp.json` — these take precedence over user-level definitions when server names conflict and are shared via source control.

**Additional config at runtime**: `--additional-mcp-config` augments `~/.copilot/mcp-config.json` for the current session only. It is repeatable, and accepts either a JSON string or a file path prefixed with `@`:

```bash
copilot --additional-mcp-config '{"mcpServers":{"extra":{"type":"stdio","command":"npx","args":["my-server"],"tools":["*"]}}}' \
        --additional-mcp-config @/path/to/project-mcp.json
```

## CLI Commands

### Management Commands

These are **slash commands entered inside the Copilot CLI interactive session** (not shell commands):

```
/mcp add                  # Interactive form — Tab to navigate fields, Ctrl+S to save
/mcp show                 # List all configured servers
/mcp show SERVER-NAME     # Details for a specific server
/mcp edit SERVER-NAME     # Edit an existing server
/mcp delete SERVER-NAME   # Delete a server
/mcp disable SERVER-NAME  # Disable a server (keeps config, stops loading)
/mcp enable SERVER-NAME   # Re-enable a disabled server
```

> **Note**: `/mcp add` is fully interactive — no server name argument is passed. Start Copilot CLI with `copilot`, then type `/mcp add` at the prompt.

## Configuration Syntax

### Root Structure

GitHub Copilot CLI uses `mcpServers` (VS Code uses `servers`):

```json
{
  "mcpServers": {
    "server-name": { /* config */ }
  }
}
```

### Server Types

GitHub Copilot CLI supports four server types:

#### Types: `stdio` / `local` (Subprocess — standard transport)

`stdio` and `local` are equivalent: both launch a subprocess and communicate via stdin/stdout. **`stdio` is the portable standard name** (aligns with VS Code, the Copilot cloud agent, and the MCP spec); `local` is a CLI-specific alias that also works.

```json
{
  "mcpServers": {
    "azure": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@azure/mcp@latest", "server", "start"],
      "tools": ["*"],
      "env": {}
    },
    "serena": {
      "type": "local",
      "command": "uvx",
      "args": ["--from", "git+https://github.com/oraios/serena", "serena", "start-mcp-server"],
      "tools": ["*"],
      "env": {
        "API_KEY": "${MY_API_KEY}"
      }
    }
  }
}
```

#### Type: `http` (HTTP Server)

Connect to HTTP-based MCP server:

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/readonly",
      "tools": ["*"],
      "headers": {
        "Authorization": "Bearer ${GITHUB_TOKEN}",
        "X-MCP-Toolsets": "repos,issues,pull_requests"
      }
    }
  }
}
```

#### Type: `sse` (Server-Sent Events) — Deprecated

> **Deprecation notice**: SSE transport is deprecated in the MCP specification. Use `http` (streamable HTTP) for new remote server connections. Existing `sse` configurations continue to work but should be migrated.

Connect to SSE-based MCP server:

```json
{
  "mcpServers": {
    "cloudflare": {
      "type": "sse",
      "url": "https://docs.mcp.cloudflare.com/sse",
      "tools": ["*"]
    }
  }
}
```

### Common Configuration Keys

**Required for all types:**
- `type`: Server type (`"local"`, `"stdio"`, `"http"`, `"sse"`)
- `tools`: Array of tool names or `["*"]` for all tools

**Local/stdio specific (required):**
- `command`: Executable command (e.g., `"npx"`, `"uvx"`, `"docker"`)
- `args`: Array of command arguments

**HTTP/sse specific (required):**
- `url`: Server endpoint URL

**Optional for all:**
- `env`: Environment variables object (local/stdio only)
- `headers`: HTTP headers object (http/sse only)

### Environment Variable Expansion

Use `${VAR_NAME}` syntax for variable substitution:

```json
{
  "mcpServers": {
    "sentry": {
      "type": "local",
      "command": "npx",
      "args": ["@sentry/mcp-server@latest", "--host=${SENTRY_HOST}"],
      "tools": ["*"],
      "env": {
        "SENTRY_HOST": "${COPILOT_MCP_SENTRY_HOST}",
        "SENTRY_TOKEN": "${COPILOT_MCP_SENTRY_TOKEN}"
      }
    }
  }
}
```

## VS Code vs GitHub Copilot CLI Syntax Differences

Key differences between `mcp.json` (VS Code) and `mcp-config.json` (GitHub Copilot CLI):

| Feature             | VS Code (mcp.json)                    | GitHub Copilot CLI (mcp-config.json)                                        |
| ------------------- | ------------------------------------- | --------------------------------------------------------------------------- |
| **Root key**        | `"servers"`                           | `"mcpServers"`                                                              |
| **Type values**     | `"stdio"`, `"http"`                   | `"local"`, `"stdio"`, `"http"`, `"sse"`                                     |
| **Env vars**        | Supports `inputs` and `envFile`       | Only `env` object with `${VAR}` syntax                                      |
| **Location**        | `.vscode/mcp.json` or global settings | `~/.copilot/mcp-config.json` (or `$COPILOT_HOME/mcp-config.json`) |
| **Variable syntax** | Can use `inputs` references           | Must use `${VARIABLE}` syntax                                               |

**VS Code example:**

```json
{
  "servers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "env": {
        "MEMORY_FILE_PATH": "${workspaceFolder}/.github/memory.json"
      },
      "type": "stdio"
    }
  }
}
```

**GitHub Copilot CLI equivalent:**

```json
{
  "mcpServers": {
    "memory": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "tools": ["*"],
      "env": {
        "MEMORY_FILE_PATH": "${MEMORY_FILE_PATH}"
      }
    }
  }
}
```

## Per-Agent MCP Servers

CLI agent files can declare remote HTTP MCP servers in `mcp-servers` frontmatter. This is the right surface when an MCP server is specific to one agent and uses the `http` transport:

```yaml
mcp-servers:
  - type: http
    url: https://example.com/mcp
    name: example-server
```

Local `stdio`/`local` MCP servers **cannot** be declared per-agent — they must be configured globally in `~/.copilot/mcp-config.json`.

## Complete Configuration Examples

### Multiple Servers

```json
{
  "mcpServers": {
    "azure": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@azure/mcp@latest", "server", "start"],
      "tools": ["*"]
    },
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/readonly",
      "tools": ["get_issue", "list_repositories"],
      "headers": {
        "Authorization": "Bearer ${GITHUB_PAT}"
      }
    },
    "cloudflare": {
      "type": "sse",
      "url": "https://docs.mcp.cloudflare.com/sse",
      "tools": ["*"]
    }
  }
}
```

### Docker-Based Server

```json
{
  "mcpServers": {
    "notion": {
      "type": "local",
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-e", "OPENAPI_MCP_HEADERS={\"Authorization\": \"Bearer ${NOTION_API_KEY}\"}",
        "mcp/notion"
      ],
      "tools": ["*"],
      "env": {
        "NOTION_API_KEY": "${COPILOT_MCP_NOTION_API_KEY}"
      }
    }
  }
}
```

## Setting Custom Config Location

| Method | Usage |
|--------|-------|
| `COPILOT_HOME` env var | `export COPILOT_HOME=/path/to/dir` — redirects entire config tree |
| `--config-dir` flag | `copilot --config-dir /path/to/dir` — takes precedence over `COPILOT_HOME` |

**Project-level MCP configs** (shareable via source control): `.mcp.json`, `.github/mcp.json`, or `.vscode/mcp.json` — these take precedence over user-level definitions for conflicting server names.

## Troubleshooting

**Configuration not loading:**
- Confirm active config dir: run `/session` inside Copilot CLI to see the config path
- Check `mcp-config.json` exists at that location
- Restart Copilot CLI

**MCP server not starting:**
- Verify command is available (e.g., `which npx`, `which uvx`)
- Check logs in `~/.copilot/logs/` (or `$COPILOT_HOME/logs/` if overridden)
- Test command manually

**Environment variables not expanding:**
- Ensure using `${VAR_NAME}` syntax (not `$VAR_NAME`)
- Verify environment variable is set: `echo $VAR_NAME`
- Check variable is exported: `export VAR_NAME="value"`

**Tools not appearing:**
- Verify `"tools"` field is present (required)
- Use `["*"]` to enable all tools
- Check server initialization logs for errors

## Converting VS Code to CLI Configuration

When migrating from VS Code `mcp.json` to CLI `mcp-config.json`:

1. Change root key: `"servers"` → `"mcpServers"`
2. Add `"tools"` field to each server (required)
3. Replace `inputs` with `env` and use `${VAR}` syntax
4. Convert `envFile` to explicit `env` entries
5. Ensure `type` is valid for CLI: `"local"`, `"stdio"`, `"http"`, or `"sse"`

## Use Cases

**Personal configuration**: Default `~/.copilot/mcp-config.json`

**Session-specific servers**: `--additional-mcp-config` flag (repeatable, JSON string or `@file`)

**Project-level / team sharing**: `.mcp.json`, `.github/mcp.json`, or `.vscode/mcp.json` — commit to source control

**Agent-specific remote servers**: Per-agent `mcp-servers` frontmatter (HTTP only)

**Custom config location**: `COPILOT_HOME` env var or `--config-dir` flag

## References

- [GitHub Docs: CLI configuration directory](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-config-dir-reference)
- [GitHub Docs: Adding MCP servers for GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-mcp-servers)
- [GitHub Docs: Custom agents configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
