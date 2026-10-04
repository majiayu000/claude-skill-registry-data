---
name: gov-environment
description: EPA air quality data and HUD foreclosure listings. 2 tools for environmental and housing intelligence.
homepage: https://github.com/martc03/gov-mcp-servers
metadata: {"clawdbot":{"emoji":"🌿","requires":{"bins":["mcporter"]}}}
---

# Environmental & Housing Intel

Real-time EPA air quality data and HUD foreclosure listings.

## Setup

```bash
mcporter add gov-env --url https://environmental-compliance-mcp.apify.actor/mcp --transport streamable-http
```

Or add to your OpenClaw MCP config (`~/.openclaw/mcp.json`):

```json
{
  "servers": {
    "gov-env": {
      "url": "https://environmental-compliance-mcp.apify.actor/mcp",
      "transport": "streamable-http"
    }
  }
}
```

## Available Tools

### `env_get_air_quality`
Get EPA AirNow air quality data by state, AQI range, and pollutant type.

```
Show air quality for California
Any unhealthy air quality readings right now?
```

Parameters: `states` (array), `minAqi`, `maxAqi`, `categories` (array), `parameters` (array), `limit`

### `env_search_hud_foreclosures`
Search HUD foreclosure listings by state, zip code, price range, and bedrooms.

```
Show HUD foreclosures in Texas
Find foreclosures under $100,000 in Florida
```

Parameters: `state`, `zipCode`, `minPrice`, `maxPrice`, `bedrooms`, `limit`

## Data Sources

- **EPA AirNow** — Environmental Protection Agency (air quality index)
- **HUD** — Department of Housing and Urban Development (foreclosure listings)

## Use Cases

- Air quality monitoring
- Health and safety planning
- Real estate investment research
- Environmental compliance tracking

All data from free US government APIs. Zero cost. No API keys required.
