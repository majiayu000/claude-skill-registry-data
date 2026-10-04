---
name: gov-court-records
description: Search US court opinions, dockets, and judges. 3 tools for federal court records research.
homepage: https://github.com/martc03/gov-mcp-servers
metadata: {"clawdbot":{"emoji":"⚖️","requires":{"bins":["mcporter"]}}}
---

# US Court Records

Search federal court opinions, dockets, and judges from CourtListener.

## Setup

```bash
mcporter add gov-courts --url https://court-records-mcp.apify.actor/mcp --transport streamable-http
```

Or add to your OpenClaw MCP config (`~/.openclaw/mcp.json`):

```json
{
  "servers": {
    "gov-courts": {
      "url": "https://court-records-mcp.apify.actor/mcp",
      "transport": "streamable-http"
    }
  }
}
```

## Available Tools

### `court_search_opinions`
Search US court opinions and case law by keyword, court, and date range.

```
Search for Supreme Court opinions on patent law
Find recent appellate decisions on data privacy
```

Parameters: `query` (required), `court`, `dateAfter` (YYYY-MM-DD), `dateBefore`, `limit`

### `court_search_dockets`
Search court dockets and case filings.

```
Search dockets for Google antitrust case
Find recent patent infringement filings
```

Parameters: `query` (required), `court`, `dateAfter` (YYYY-MM-DD), `dateBefore`, `limit`

### `court_search_judges`
Search judges in the US court system.

```
Search for judges in the 9th Circuit
Look up Judge Smith
```

Parameters: `query` (required), `court`, `limit`

## Data Sources

- **CourtListener** — Free Law Project (court opinions, dockets, judges)
- **PACER** — Public Access to Court Electronic Records

## Use Cases

- Legal research and case law analysis
- Litigation tracking
- Judicial background research
- Regulatory compliance research

All data from free public APIs. Zero cost. No API keys required.
