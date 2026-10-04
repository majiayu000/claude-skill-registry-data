---
name: gov-travel
description: US visa wait times, border crossing delays, and FAA airport status. 3 tools for travel intelligence.
homepage: https://github.com/martc03/gov-mcp-servers
metadata: {"clawdbot":{"emoji":"✈️","requires":{"bins":["mcporter"]}}}
---

# Immigration & Travel Intel

Real-time visa wait times, border crossing delays, and FAA airport status.

## Setup

```bash
mcporter add gov-travel --url https://immigration-travel-mcp.apify.actor/mcp --transport streamable-http
```

Or add to your OpenClaw MCP config (`~/.openclaw/mcp.json`):

```json
{
  "servers": {
    "gov-travel": {
      "url": "https://immigration-travel-mcp.apify.actor/mcp",
      "transport": "streamable-http"
    }
  }
}
```

## Available Tools

### `travel_get_visa_wait_times`
Get US visa wait times by embassy city.

```
Show visa wait times for London
What are current visa processing times?
```

Parameters: `city`, `visaCategory`

### `travel_get_border_wait_times`
Get US border crossing wait times from CBP.

```
Show Mexican border wait times
What's the wait at the Canadian border for pedestrians?
```

Parameters: `border` ("Canadian Border" or "Mexican Border"), `portName`, `laneType` ("commercial", "passenger", or "pedestrian")

### `travel_get_airport_delays`
Get FAA airport delays and event information.

```
Any delays at JFK right now?
Show FAA airport status for LAX and SFO
```

Parameters: `airports` (array, e.g. ["JFK","LAX"]), `delayTypes` (array)

## Data Sources

- **State Department** — Visa appointment wait times
- **CBP** — Customs and Border Protection (border wait times)
- **FAA** — Federal Aviation Administration (airport delays)

## Use Cases

- Travel planning and timing
- Border crossing optimization
- Flight delay monitoring
- Immigration processing estimates

All data from free US government APIs. Zero cost. No API keys required.
