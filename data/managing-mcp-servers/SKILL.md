---
name: managing-mcp-servers
description: Provides comprehensive guidance for managing MCP (Model Context Protocol) servers using the claude mcp CLI. Covers adding servers across scopes (project, local, user), transport types (stdio, sse, http), security best practices, and common patterns. Strongly recommends project scope for team consistency and version control.
---

# Managing MCP Servers

Comprehensive guidance for managing MCP (Model Context Protocol) servers in Claude Code.

## Overview

MCP servers extend Claude Code's capabilities by providing additional tools, resources, and prompts. They can be configured at three scopes:

- **project** (`.mcp.json` in project root) - **PREFERRED**: Project-specific servers (committed to version control)
- **local** (`~/.config/claude/mcp.json`) - Local machine configuration
- **user** (`~/.claude/mcp.json`) - Available globally across all projects

## Default Recommendation

**🎯 Always add MCP servers to project scope (`--scope project`) unless you have a specific reason to use local or user scope.**

Benefits of project scope:
- ✅ Team consistency - everyone uses the same tools
- ✅ Self-documenting - `.mcp.json` shows what tools the project needs
- ✅ Easy onboarding - new team members get tools automatically
- ✅ Version controlled - changes are tracked in git
- ✅ Reproducible - same setup across all environments

Only use `user` scope for truly personal productivity tools unrelated to development (e.g., personal task managers). Development tools, documentation servers, testing frameworks, etc. should all be in project scope.

## Transport Types

MCP servers support three transport mechanisms:

1. **stdio** - Standard input/output (most common, e.g., `npx` commands)
2. **sse** - Server-Sent Events over HTTP
3. **http** - HTTP-based communication

## Commands

### List Servers

```bash
claude mcp list
```

Shows all configured MCP servers with health status:
- ✓ Connected
- ⚠ Needs authentication
- ✗ Failed to connect

### Add Server

#### stdio Transport (Default)

```bash
# Basic stdio server
claude mcp add <name> <command> [args...]

# With environment variables
claude mcp add <name> --env KEY1=value1 --env KEY2=value2 -- <command> [args...]

# Specify scope explicitly
claude mcp add --scope user <name> <command> [args...]
claude mcp add --scope local <name> <command> [args...]
claude mcp add --scope project <name> <command> [args...]
```

**Examples:**

```bash
# Playwright MCP server (project scope - DEFAULT)
claude mcp add --scope project playwright npx @playwright/mcp@latest

# Airtable with API key (project scope with env var)
claude mcp add --transport stdio --scope project airtable \
  --env AIRTABLE_API_KEY="${AIRTABLE_API_KEY}" -- npx -y airtable-mcp-server

# Context7 with API key (project scope - team uses same docs)
claude mcp add --scope project context7 \
  --env UPSTASH_API_KEY="${UPSTASH_API_KEY}" -- npx -y @upstash/context7-mcp
```

**Important:** Use `--` separator before the command when using `--env` or other flags to prevent argument parsing conflicts.

#### SSE Transport

```bash
# Basic SSE server
claude mcp add --transport sse <name> <url>

# With custom headers
claude mcp add --transport sse <name> --header "X-Api-Key: abc123" <url>

# With multiple headers
claude mcp add --transport sse <name> \
  --header "Authorization: Bearer token" \
  --header "X-Custom: value" \
  <url>
```

**Examples:**

```bash
# Asana MCP server
claude mcp add --transport sse asana https://mcp.asana.com/sse

# Atlassian with authentication
claude mcp add --transport sse atlassian \
  --header "Authorization: Bearer YOUR_TOKEN" \
  https://mcp.atlassian.com/v1/sse

# Custom SSE server with headers
claude mcp add --transport sse --scope project myserver \
  --header "X-Api-Key: secret123" \
  https://example.com/mcp/sse
```

#### HTTP Transport

```bash
# Basic HTTP server
claude mcp add --transport http <name> <url>

# With custom headers
claude mcp add --transport http <name> --header "X-Api-Key: abc123" <url>
```

**Examples:**

```bash
# Sentry MCP server
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp

# Custom HTTP server with authentication
claude mcp add --transport http --scope user analytics \
  --header "Authorization: Bearer YOUR_TOKEN" \
  https://analytics.example.com/mcp
```

### Add Server from JSON

For complex configurations, you can add servers using JSON:

```bash
claude mcp add-json <name> '<json-config>'
```

**Examples:**

```bash
# stdio server JSON
claude mcp add-json myserver '{
  "command": "npx",
  "args": ["-y", "@my/mcp-server"],
  "env": {
    "API_KEY": "secret",
    "DEBUG": "true"
  }
}'

# SSE server JSON
claude mcp add-json myserver '{
  "url": "https://example.com/sse",
  "headers": {
    "Authorization": "Bearer token",
    "X-Custom": "value"
  }
}'

# With scope
claude mcp add-json --scope project myserver '{"command": "npx", "args": ["-y", "mcp-server"]}'
```

### Remove Server

```bash
# Remove from any scope (auto-detects)
claude mcp remove <name>

# Remove from specific scope
claude mcp remove --scope user <name>
claude mcp remove --scope local <name>
claude mcp remove --scope project <name>
```

### Get Server Details

```bash
claude mcp get <name>
```

Shows detailed configuration for a specific MCP server.

### Import from Claude Desktop

```bash
# Import all servers from Claude Desktop config
claude mcp add-from-claude-desktop

# Import to specific scope
claude mcp add-from-claude-desktop --scope user
```

**Note:** Only works on Mac and WSL (Windows Subsystem for Linux).

### Reset Project Choices

```bash
claude mcp reset-project-choices
```

Resets all approved and rejected project-scoped (`.mcp.json`) servers within the current project. Useful when you want to re-evaluate which project servers to enable.

### Start MCP Server

```bash
# Start Claude Code MCP server
claude mcp serve

# With debug output
claude mcp serve --debug

# With verbose logging
claude mcp serve --verbose
```

## Scope Selection Guide

**DEFAULT: Always prefer project scope unless there's a specific reason not to.**

### When to use **project** scope (`.mcp.json`) - **PREFERRED**

- **DEFAULT CHOICE**: Most MCP servers should be configured here
- Project-specific integrations and tools
- Servers required by the project team
- Shared configuration committed to version control
- Ensures consistency across team members
- Self-documenting - team can see what tools the project uses
- Makes onboarding easier for new developers

### When to use **local** scope (`~/.config/claude/mcp.json`)

- Machine-specific configurations (paths, local services)
- Servers with machine-specific credentials that shouldn't be shared
- Local development servers running on your machine
- Testing MCP servers before adding to project

### When to use **user** scope (`~/.claude/mcp.json`)

- **ONLY for truly personal tools** that you use across ALL projects
- Personal productivity tools unrelated to any specific project
- Your personal integrations (e.g., your personal task manager)
- **AVOID using for development tools** - these should be in project scope

## Best Practices

### Security

1. **Never commit secrets to `.mcp.json`** - Use environment variables instead:
   ```bash
   claude mcp add --scope project myserver \
     --env API_KEY="${MY_API_KEY}" -- npx mcp-server
   ```

2. **Use headers for authentication** with remote servers:
   ```bash
   claude mcp add --transport sse myserver \
     --header "Authorization: Bearer ${TOKEN}" \
     https://api.example.com/sse
   ```

3. **Store sensitive servers in user/local scope** rather than project scope

### Organization

1. **Use meaningful names** - `github-prod` instead of `gh1`
2. **Document project servers** - Add comments to `.mcp.json` explaining what each server does
3. **Keep scopes clean** - Regularly run `claude mcp list` and remove unused servers

### Debugging

1. **Check health first**: `claude mcp list` shows connection status
2. **Test with debug mode**: `claude mcp serve --debug`
3. **Verify configuration**: `claude mcp get <name>`

## Common Patterns

### Development vs Production

```bash
# Development (project scope - DEFAULT for team)
claude mcp add --scope project myapp-dev \
  --env API_URL=http://localhost:3000 -- npx myapp-mcp

# Production (project scope - team uses same production tools)
claude mcp add --scope project myapp-prod \
  --env API_URL=https://api.myapp.com -- npx myapp-mcp

# Personal testing (local scope - before adding to project)
claude mcp add --scope local myapp-test \
  --env API_URL=http://localhost:4000 -- npx myapp-mcp
```

### Team-Shared Servers

Add to `.mcp.json` (project scope) without secrets:

```bash
# In project, commit this to git
claude mcp add --scope project team-tool \
  --env TOOL_API_KEY=SET_THIS_IN_YOUR_ENV -- npx team-tool-mcp
```

Then team members set their own credentials:
```bash
export TOOL_API_KEY=their_personal_key
```

### Multi-Environment Setup

```bash
# Local development (project scope - team default)
claude mcp add --scope project db-local \
  --env DATABASE_URL=postgresql://localhost:5432/dev -- npx db-mcp

# Staging (project scope - team shares staging)
claude mcp add --scope project db-staging \
  --env DATABASE_URL="${STAGING_DB_URL}" -- npx db-mcp

# Production (project scope - team uses with env vars for credentials)
claude mcp add --scope project db-prod \
  --env DATABASE_URL="${PROD_DB_URL}" -- npx db-mcp
```

## Troubleshooting

### Server won't connect

1. Check if command exists: `which npx` or test the URL
2. Verify environment variables are set: `echo $API_KEY`
3. Test transport independently:
   - stdio: Run the command manually
   - SSE/HTTP: `curl -N <url>` to test connection

### Headers not working

Headers only work with `--transport sse` or `--transport http`, not stdio:

```bash
# ✗ Wrong - headers don't apply to stdio
claude mcp add myserver --header "X-Key: val" npx server

# ✓ Correct - use env vars for stdio
claude mcp add myserver --env API_KEY=val -- npx server

# ✓ Correct - headers work with sse/http
claude mcp add --transport sse myserver --header "X-Key: val" https://url
```

### Scope confusion

If unsure which scope contains a server:

```bash
# List all servers
claude mcp list

# Get specific server details
claude mcp get <name>

# Remove without specifying scope (auto-detects)
claude mcp remove <name>
```

## Examples by Use Case

**Note: All examples default to project scope (`--scope project`) to promote team consistency. Only use user or local scope when there's a specific need.**

### Adding a public MCP server

```bash
# Playwright for browser automation (project scope - team tool)
claude mcp add --scope project playwright npx @playwright/mcp@latest

# Context7 for documentation (project scope - team tool)
claude mcp add --scope project context7 npx -y @upstash/context7-mcp

# Personal productivity tool (user scope exception)
claude mcp add --scope user my-personal-notes npx my-notes-mcp
```

### Adding a private authenticated server

```bash
# SSE with API key header (project scope - team members set their own key)
claude mcp add --transport sse --scope project mycompany \
  --header "X-Api-Key: ${MY_API_KEY}" \
  https://mcp.mycompany.com/sse

# stdio with environment variable (project scope - use env vars for secrets)
claude mcp add --scope project myapp \
  --env API_TOKEN="${MYAPP_TOKEN}" -- npx @myapp/mcp-server

# Local testing (local scope - before adding to project)
claude mcp add --scope local myapp-test \
  --env API_TOKEN="test_token" -- npx @myapp/mcp-server
```

### Adding project-specific server

```bash
# Project database tools (team should set their own DB_URL)
claude mcp add --scope project db-tools \
  --env DATABASE_URL="${DATABASE_URL}" -- npx prisma-mcp

# Project-specific API (committed to .mcp.json)
claude mcp add --scope project project-api \
  --transport sse \
  https://api.thisproject.com/mcp/sse
```

## Quick Reference

| Command | Purpose |
|---------|---------|
| `claude mcp list` | Show all servers and health |
| `claude mcp add` | Add new server |
| `claude mcp remove` | Remove server |
| `claude mcp get` | Show server details |
| `claude mcp add-json` | Add server from JSON |
| `claude mcp serve` | Start Claude Code MCP server |
| `claude mcp reset-project-choices` | Reset project server approvals |

| Scope | Location | Use For |
|-------|----------|---------|
| `project` ⭐ | `.mcp.json` | **DEFAULT**: Project team servers (preferred) |
| `local` | `~/.config/claude/mcp.json` | Machine-specific config, testing |
| `user` | `~/.claude/mcp.json` | Personal tools only (avoid for dev tools) |

| Transport | Flag | Use For |
|-----------|------|---------|
| `stdio` | Default or `--transport stdio` | Local commands (npx, node, python) |
| `sse` | `--transport sse` | Server-Sent Events servers |
| `http` | `--transport http` | HTTP API servers |
