---
name: gov-grants
description: Search Grants.gov for federal funding opportunities by agency, category, and eligibility. 4 tools.
homepage: https://github.com/martc03/gov-mcp-servers
metadata: {"clawdbot":{"emoji":"💵","requires":{"bins":["mcporter"]}}}
---

# Federal Grant Finder

Search Grants.gov for federal funding opportunities, detailed grant info, and filter options.

## Setup

```bash
mcporter add gov-grants --url https://grant-finder-mcp.apify.actor/mcp --transport streamable-http
```

Or add to your OpenClaw MCP config (`~/.openclaw/mcp.json`):

```json
{
  "servers": {
    "gov-grants": {
      "url": "https://grant-finder-mcp.apify.actor/mcp",
      "transport": "streamable-http"
    }
  }
}
```

## Available Tools

### `grants_search_opportunities`
Search Grants.gov for federal funding opportunities by keyword, agency, category, and eligibility.

```
Search for cybersecurity research grants
Find education grants for nonprofits
```

Parameters: `keyword`, `status` ("forecasted", "posted", "closed", or "archived"), `agency`, `fundingCategory`, `fundingInstrument`, `eligibility`, `limit`, `offset`

### `grants_get_opportunity`
Get detailed info for a specific grant opportunity by its opportunity number.

```
Get details for grant HHS-2024-ACF-001
```

Parameters: `opportunityNumber` (required)

### `grants_search_by_agency`
Search grants from a specific federal agency.

```
Show NIH grants for biomedical research
Find NSF grants for AI and machine learning
```

Parameters: `agency` (required), `keyword`, `status` ("forecasted", "posted", "closed", or "archived"), `limit`

### `grants_get_filter_options`
Get available filter options for Grants.gov searches (agencies, categories, instruments, eligibilities).

```
What grant categories are available?
Show filter options for education grants
```

Parameters: `keyword`

## Data Sources

- **Grants.gov** — Federal grant opportunities clearinghouse

## Use Cases

- Grant prospecting for nonprofits
- Research funding discovery
- Small business grant search
- Government funding analysis

All data from free US government APIs. Zero cost. No API keys required.
