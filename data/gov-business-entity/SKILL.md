---
name: gov-business-entity
description: Search company registrations via OpenCorporates and SEC EDGAR. 3 tools for business entity research.
homepage: https://github.com/martc03/gov-mcp-servers
metadata: {"clawdbot":{"emoji":"🏢","requires":{"bins":["mcporter"]}}}
---

# Business Entity Search

Search company registrations worldwide via OpenCorporates and SEC EDGAR.

## Setup

```bash
mcporter add gov-entities --url https://business-entity-mcp.apify.actor/mcp --transport streamable-http
```

Or add to your OpenClaw MCP config (`~/.openclaw/mcp.json`):

```json
{
  "servers": {
    "gov-entities": {
      "url": "https://business-entity-mcp.apify.actor/mcp",
      "transport": "streamable-http"
    }
  }
}
```

## Available Tools

### `entity_search_companies`
Search OpenCorporates for company registrations worldwide.

```
Search for Acme Corp registrations
Find active companies in Delaware
```

Parameters: `query` (required), `jurisdiction`, `status` ("Active", "Inactive", or "Dissolved"), `limit`, `page`

### `entity_get_company_details`
Get detailed company info from OpenCorporates by jurisdiction and company number.

```
Get details for company us_de/12345678
Look up UK company registration 08209948
```

Parameters: `jurisdiction` (required), `companyNumber` (required)

### `entity_search_sec_companies`
Search SEC EDGAR for US public companies and their filings.

```
Search SEC for Microsoft filings
Find 10-K annual reports for Amazon
```

Parameters: `companyName` (required), `formTypes` (array, e.g. ["10-K","10-Q"]), `dateFrom` (YYYY-MM-DD), `dateTo`, `limit`

## Data Sources

- **OpenCorporates** — Global company registration database
- **SEC EDGAR** — US Securities and Exchange Commission (public company filings)

## Use Cases

- Business due diligence
- Corporate structure research
- KYC/AML compliance
- Competitive analysis

All data from free public APIs. Zero cost. No API keys required.
