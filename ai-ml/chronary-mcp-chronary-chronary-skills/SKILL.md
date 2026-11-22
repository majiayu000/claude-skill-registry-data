---
name: chronary-mcp
description: Chronary MCP Server — configure and use Chronary calendar tools in Claude Desktop, Cursor, VS Code, and Windsurf.
---

# Chronary MCP Server

The Chronary MCP server exposes calendar management tools via the Model Context Protocol. It lets AI assistants create calendars, schedule events, check availability, and manage webhooks through natural language.

## Quick Start

```bash
npx -y @chronary/mcp --api-key chr_sk_...
```

Or set the environment variable:

```bash
export CHRONARY_API_KEY=chr_sk_...
npx -y @chronary/mcp
```

## Configuration

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "chronary": {
      "command": "npx",
      "args": ["-y", "@chronary/mcp"],
      "env": {
        "CHRONARY_API_KEY": "chr_sk_..."
      }
    }
  }
}
```

### Cursor

Add to `.cursor/mcp.json` in your project root:

```json
{
  "mcpServers": {
    "chronary": {
      "command": "npx",
      "args": ["-y", "@chronary/mcp"],
      "env": {
        "CHRONARY_API_KEY": "chr_sk_..."
      }
    }
  }
}
```

### VS Code Copilot

Add to `.vscode/mcp.json`:

```json
{
  "servers": {
    "chronary": {
      "command": "npx",
      "args": ["-y", "@chronary/mcp"],
      "env": {
        "CHRONARY_API_KEY": "chr_sk_..."
      }
    }
  }
}
```

### Claude Code

Add to `.mcp.json` in your project root:

```json
{
  "mcpServers": {
    "chronary": {
      "command": "npx",
      "args": ["-y", "@chronary/mcp"],
      "env": {
        "CHRONARY_API_KEY": "chr_sk_..."
      }
    }
  }
}
```

### Windsurf

Add to `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "chronary": {
      "command": "npx",
      "args": ["-y", "@chronary/mcp"],
      "env": {
        "CHRONARY_API_KEY": "chr_sk_..."
      }
    }
  }
}
```

## Available Tools

The MCP server exposes all 47 Chronary toolkit tools. Read-only tools (queries, list operations) are auto-approved by most MCP clients. Write and delete operations require confirmation.

**Auto-approved (read-only):** `list_calendars`, `get_calendar`, `list_events`, `list_org_events`, `get_event`, `list_agents`, `get_agent`, `get_availability`, `find_meeting_time`, `get_calendar_context`, `list_proposals`, `get_proposal`, `get_availability_rules`, `list_webhooks`, `get_webhook`, `list_webhook_deliveries`, `list_ical_subscriptions`, `get_ical_subscription`, `list_scoped_keys`, `get_audit_log`, `get_usage`, `get_usage_history`

**Requires confirmation:** `create_calendar`, `update_calendar`, `delete_calendar`, `create_event`, `update_event`, `cancel_event`, `confirm_event`, `release_event`, `create_agent`, `update_agent`, `delete_agent`, `create_proposal`, `respond_to_proposal`, `resolve_proposal`, `cancel_proposal`, `set_availability_rules`, `clear_availability_rules`, `create_webhook`, `update_webhook`, `delete_webhook`, `subscribe_ical`, `update_ical_subscription`, `delete_ical_subscription`, `sync_ical_subscription`, `pause_ical_subscription`, `resume_ical_subscription`, `create_scoped_key`, `revoke_scoped_key`, `accept_terms`

## Selective Tool Loading

Load only specific tools:

```bash
npx -y @chronary/mcp --tools list_calendars,create_event,find_meeting_time
```

## Troubleshooting

**"API key is required"** — Set `CHRONARY_API_KEY` in the `env` block of your MCP config, or pass `--api-key`.

**Tools not appearing** — Restart your IDE after editing MCP config. Check that `npx` is in your PATH.

**Windows: "npx is not recognized"** — Use the full path to npx or use `cmd /c npx` as the command:
```json
{
  "command": "cmd",
  "args": ["/c", "npx", "-y", "@chronary/mcp"],
  "env": { "CHRONARY_API_KEY": "chr_sk_..." }
}
```

**Rate limit errors** — The API allows 10 requests per second per key on Free (25 on Developer, 50 on Pro). If running multiple MCP clients with the same key, consider using separate keys.
