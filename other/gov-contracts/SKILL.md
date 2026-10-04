---
name: gov-contracts
description: SAM.gov contract opportunities, USAspending awards, and entity lookup. 3 tools for government contracting.
homepage: https://github.com/martc03/gov-mcp-servers
metadata: {"clawdbot":{"emoji":"📋","requires":{"bins":["mcporter"]}}}
---

# Government Contracts

Search SAM.gov contract opportunities, federal spending awards, and registered entities.

## Setup

```bash
mcporter add gov-contracts --url https://gov-contracts-mcp.apify.actor/mcp --transport streamable-http
```

Or add to your OpenClaw MCP config (`~/.openclaw/mcp.json`):

```json
{
  "servers": {
    "gov-contracts": {
      "url": "https://gov-contracts-mcp.apify.actor/mcp",
      "transport": "streamable-http"
    }
  }
}
```

## Available Tools

### `contracts_search_opportunities`
Search SAM.gov for contract opportunities (RFPs, RFQs, solicitations).

```
Search for cybersecurity contract opportunities
Find IT contracts posted this month
```

Parameters: `keyword`, `naicsCode`, `postedFrom` (MM/dd/yyyy), `postedTo`, `limit`, `offset`

### `contracts_search_spending`
Search USASpending.gov for federal awards data (contracts, grants, loans).

```
Show federal contracts for Lockheed Martin
Search USAspending for defense grants
```

Parameters: `keyword`, `awardType` ("contracts", "grants", "loans", "direct_payments", "other"), `dateFrom` (YYYY-MM-DD), `dateTo`, `agency`, `limit`, `page`

### `contracts_lookup_entity`
Search SAM.gov for registered entities (contractors, grantees) by name, UEI, or CAGE code.

```
Look up Raytheon in SAM.gov
Search for contractors in California
```

Parameters: `legalBusinessName`, `ueiSAM`, `cageCode`, `state`, `limit`

## Data Sources

- **SAM.gov** — System for Award Management (opportunities + entity registration)
- **USASpending.gov** — Federal spending transparency

## Use Cases

- Government contract bidding
- Competitive intelligence for GovCon
- Federal spending analysis
- Vendor due diligence

All data from free US government APIs. Zero cost. No API keys required.
