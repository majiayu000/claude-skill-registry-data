---
name: gov-financial-intel
description: SEC EDGAR filings, BLS employment stats, and USDA crop prices. 3 tools for federal financial intelligence.
homepage: https://github.com/martc03/gov-mcp-servers
metadata: {"clawdbot":{"emoji":"💰","requires":{"bins":["mcporter"]}}}
---

# Federal Financial Intel

Real-time access to SEC filings, BLS employment statistics, and USDA commodity prices.

## Setup

```bash
mcporter add gov-finance --url https://federal-financial-intel-mcp.apify.actor/mcp --transport streamable-http
```

Or add to your OpenClaw MCP config (`~/.openclaw/mcp.json`):

```json
{
  "servers": {
    "gov-finance": {
      "url": "https://federal-financial-intel-mcp.apify.actor/mcp",
      "transport": "streamable-http"
    }
  }
}
```

## Available Tools

### `finance_search_sec_filings`
Search SEC EDGAR for company filings (10-K, 10-Q, 8-K, etc).

```
Search SEC filings for Apple
Show 10-K annual reports for Tesla
```

Parameters: `searchText`, `formTypes` (array, e.g. ["10-K","10-Q","8-K"]), `dateFrom`, `dateTo`, `limit`

### `finance_get_employment_stats`
Get BLS employment statistics: unemployment rate, nonfarm payrolls, CPI, hourly earnings.

```
Show current unemployment rate
Get BLS employment data for 2024-2025
```

Parameters: `seriesIds` (array, e.g. ["LNS14000000","CES0000000001"]), `startYear`, `endYear`

### `finance_get_crop_prices`
Get USDA crop and commodity prices (corn, soybeans, wheat, etc).

```
Show corn prices for 2024
Get USDA soybean prices by state
```

Parameters: `commodities` (array, e.g. ["CORN","SOYBEANS","WHEAT"]), `states` (array), `years` (array), `statisticCategory`, `limit`

## Data Sources

- **SEC EDGAR** — Securities and Exchange Commission (company filings)
- **BLS** — Bureau of Labor Statistics (employment, CPI)
- **USDA NASS** — National Agricultural Statistics Service (crop prices)

## Use Cases

- Company financial research
- Economic indicator tracking
- Agricultural market analysis
- Investment due diligence

All data from free US government APIs. Zero cost. No API keys required.
