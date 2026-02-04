---
name: td-mcp
description: TD MCP server setup for Claude Code integration. Covers installation, regional configuration (us01, jp01, eu01), available tools (query, list_databases, describe_table), and write mode.
---

# Treasure Data MCP Server

## Setup

```bash
export TD_API_KEY="your_api_key"

claude mcp add td \
  -e TD_API_KEY=$TD_API_KEY \
  -- npx @treasuredata/mcp-server
```

Requires Node.js 18+.

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `TD_API_KEY` | (required) | API key |
| `TD_SITE` | `us01` | Region: us01, jp01, eu01, ap02, ap03 |
| `TD_DATABASE` | - | Default database |
| `TD_ENABLE_UPDATES` | `false` | Enable write operations |

**Regional Setup:**
```bash
# Tokyo
claude mcp add td -e TD_API_KEY=$TD_API_KEY -e TD_SITE=jp01 -- npx @treasuredata/mcp-server

# EU
claude mcp add td -e TD_API_KEY=$TD_API_KEY -e TD_SITE=eu01 -- npx @treasuredata/mcp-server
```

**Enable Write Mode:**
```bash
claude mcp add td -e TD_API_KEY=$TD_API_KEY -e TD_ENABLE_UPDATES=true -- npx @treasuredata/mcp-server
```

## Available Tools

### Data Exploration
- `list_databases` - List all databases
- `list_tables` - List tables in database
- `describe_table` - Show table schema
- `current_database` / `use_database` - Database context

### Query Execution
- `query` - Read-only SQL (default 40 row limit, max 10,000)
- `execute` - Write operations (requires TD_ENABLE_UPDATES=true)

### CDP (Experimental)
- `list_parent_segments`, `get_parent_segment`
- `list_segments`, `get_segment`
- `list_activations`
- `parent_segment_sql`, `segment_sql`

### Workflows (Experimental)
- `list_projects`, `list_workflows`, `list_sessions`

## Usage in Claude Code

```
"List all my TD databases"
"Describe the nasdaq table"
"Query top 10 symbols from nasdaq"
"Show yesterday's events from user_events"
```

## Multiple Environments

```bash
claude mcp add td-prod -e TD_API_KEY=$TD_PROD_KEY -- npx @treasuredata/mcp-server
claude mcp add td-staging -e TD_API_KEY=$TD_STAGING_KEY -e TD_ENABLE_UPDATES=true -- npx @treasuredata/mcp-server
```

## Verify Installation

```bash
claude mcp list   # Should show 'td'
```

## Resources

- https://github.com/treasure-data/td-mcp-server
