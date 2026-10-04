---
name: gov-public-health
description: CDC open data and WHO global health indicators. 3 tools for public health intelligence.
homepage: https://github.com/martc03/gov-mcp-servers
metadata: {"clawdbot":{"emoji":"🏥","requires":{"bins":["mcporter"]}}}
---

# Public Health Intel

Access CDC open data and WHO Global Health Observatory indicators.

## Setup

```bash
mcporter add gov-health --url https://public-health-mcp.apify.actor/mcp --transport streamable-http
```

Or add to your OpenClaw MCP config (`~/.openclaw/mcp.json`):

```json
{
  "servers": {
    "gov-health": {
      "url": "https://public-health-mcp.apify.actor/mcp",
      "transport": "streamable-http"
    }
  }
}
```

## Available Tools

### `health_get_cdc_data`
Query CDC Open Data using the Socrata SODA API. Access datasets on disease surveillance, vaccinations, mortality, and more.

```
Get CDC COVID-19 surveillance data
Query CDC dataset for vaccination rates
```

Parameters: `datasetId` (default "g4ie-h725"), `query` (SoQL where clause), `limit`, `offset`, `orderBy`

### `health_get_who_indicator`
Query WHO Global Health Observatory indicators by country and year.

```
Get life expectancy data for Japan
Show WHO malaria incidence for Nigeria
```

Parameters: `indicatorCode` (default "WHOSIS_000001"), `country` (3-letter ISO code), `year`, `limit`

### `health_list_who_indicators`
List available WHO GHO indicators. Search by keyword to find the right indicator code.

```
Search WHO indicators for tuberculosis
List available WHO health indicators
```

Parameters: `search`, `limit`

## Data Sources

- **CDC** — Centers for Disease Control and Prevention (open data via Socrata)
- **WHO GHO** — World Health Organization Global Health Observatory

## Use Cases

- Disease surveillance monitoring
- Global health research
- Public health policy analysis
- Epidemiological data access

All data from free government APIs. Zero cost. No API keys required.
