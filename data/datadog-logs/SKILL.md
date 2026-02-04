---
name: datadog-logs
description: Search Datadog logs via API - query syntax, storage tiers (indexes, flex, online-archives), pagination. Use when searching logs or using the dd search-logs command.
---

# Datadog Logs API

## CLI Command

```bash
# Basic search (last 15 minutes)
dd search-logs 'env:prod service:my-service error'

# Custom time range
dd search-logs 'env:prod error' --from now-1h --to now

# Search Flex Logs tier (for archived/long-retention logs)
dd search-logs 'env:prod' --storage-tier flex --from now-30d

# Multi-service search with OR
dd search-logs 'env:prod service:(service-a OR service-b) order-12345' --storage-tier flex

# Fetch all pages
dd search-logs 'env:prod' --all-pages --limit 100
```

## Query Syntax

The query syntax matches Datadog's Log Explorer. Pass it directly to `--query`:

```bash
# Attribute search
env:prod status:error

# Boolean operators
service:(api OR web) AND status:error

# Free text search
"connection timeout"

# Full-text search across all fields
*:order-12345

# Exclusions
env:prod -status:info
```

## Storage Tiers

| Tier | Flag | Use case |
| --- | --- | --- |
| `indexes` | (default) | Recent, indexed logs |
| `flex` | `--storage-tier flex` | Long-retention logs (30d+) |
| `online-archives` | `--storage-tier online-archives` | Archived logs |

**Important**: If you don't see results, check if logs are in Flex tier. The Datadog UI has a toggle "Include Flex Logs" - this CLI flag is the equivalent.

## Options

| Option | Default | Description |
| --- | --- | --- |
| `--from` | `now-15m` | Start time (e.g., `now-1h`, `now-7d`) |
| `--to` | `now` | End time |
| `--limit` | `100` | Max logs per page |
| `--storage-tier` | indexes | Storage tier to search |
| `--all-pages` | false | Fetch up to 50 pages |

## Common Patterns

```bash
# Search for UUID across services
dd search-logs 'env:prod service:(svc-a OR svc-b) fb13dc8c-8552-429b-b2d9-8897bfdcfb0e' \
  --storage-tier flex --from now-30d

# Find errors in last hour
dd search-logs 'env:prod status:error' --from now-1h

# Search specific host
dd search-logs 'env:prod host:web-01 status:error'
```

## API Details

- **Endpoint**: `POST /api/v2/logs/events/search`
- **Pagination**: Cursor-based (`--all-pages` handles this)
- **Permission**: Requires `logs_read_data` on the app key

## curl Example

```bash
curl -X POST "https://api.$DD_SITE/api/v2/logs/events/search" \
  -H "DD-API-KEY: $DD_API_KEY" \
  -H "DD-APPLICATION-KEY: $DD_APP_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "query": "env:prod status:error",
      "from": "now-1h",
      "to": "now",
      "storage_tier": "flex"
    },
    "sort": "-timestamp",
    "page": {"limit": 100}
  }'
```
