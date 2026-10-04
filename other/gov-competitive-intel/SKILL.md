---
name: gov-competitive-intel
description: SEC filings, company news, federal contracts, and company profiles. 4 tools for competitive intelligence.
homepage: https://github.com/martc03/gov-mcp-servers
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["mcporter"]}}}
---

# Competitive Intelligence

Company research combining SEC filings, news, federal contracts, and comprehensive profiles.

## Setup

```bash
mcporter add gov-intel --url https://competitive-intel-mcp.apify.actor/mcp --transport streamable-http
```

Or add to your OpenClaw MCP config (`~/.openclaw/mcp.json`):

```json
{
  "servers": {
    "gov-intel": {
      "url": "https://competitive-intel-mcp.apify.actor/mcp",
      "transport": "streamable-http"
    }
  }
}
```

## Available Tools

### `intel_company_filings`
Search SEC EDGAR for a company's regulatory filings (10-K, 10-Q, 8-K, etc).

```
Show Apple's recent SEC filings
Find Tesla 10-K annual reports
```

Parameters: `companyName` (required), `formType`, `dateFrom` (YYYY-MM-DD), `dateTo`, `limit`

### `intel_company_news`
Search recent news articles about a company.

```
Show recent news about Microsoft
What's in the news about Nvidia?
```

Parameters: `query` (required), `limit`

### `intel_company_contracts`
Search USASpending.gov for federal awards to a specific company.

```
Show federal contracts for Palantir
Find government grants to SpaceX
```

Parameters: `companyName` (required), `awardType` ("contracts", "grants", "loans", or "all"), `dateFrom` (YYYY-MM-DD), `dateTo`, `limit`, `page`

### `intel_company_profile`
Get a comprehensive competitive intelligence snapshot combining filings, news, and contract data.

```
Build a competitive profile for CrowdStrike
Get full intel on Booz Allen Hamilton
```

Parameters: `companyName` (required)

## Data Sources

- **SEC EDGAR** — Company regulatory filings
- **Google News** — Recent company news
- **USASpending.gov** — Federal contract awards

## Use Cases

- Competitive analysis and benchmarking
- Vendor and partner due diligence
- Investment research
- Government contractor intelligence

All data from free public APIs. Zero cost. No API keys required.
