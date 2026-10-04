---
name: gov-disaster-intel
description: FEMA disaster declarations, NOAA weather alerts, and USGS earthquake data. 3 tools for real-time disaster monitoring.
homepage: https://github.com/martc03/gov-mcp-servers
metadata: {"clawdbot":{"emoji":"🌪️","requires":{"bins":["mcporter"]}}}
---

# Natural Disaster Intel

Real-time disaster monitoring from FEMA, NOAA, and USGS.

## Setup

```bash
mcporter add gov-disasters --url https://natural-disaster-intel-mcp.apify.actor/mcp --transport streamable-http
```

Or add to your OpenClaw MCP config (`~/.openclaw/mcp.json`):

```json
{
  "servers": {
    "gov-disasters": {
      "url": "https://natural-disaster-intel-mcp.apify.actor/mcp",
      "transport": "streamable-http"
    }
  }
}
```

## Available Tools

### `disaster_search_fema_declarations`
Search FEMA disaster declarations by state, incident type, and date range. Returns official federal disaster records.

```
Show FEMA disaster declarations for California
Any hurricane declarations in Florida this year?
```

Parameters: `states` (array, e.g. ["CA","NY"]), `incidentTypes` (array, e.g. ["Hurricane","Flood"]), `dateStart`, `dateEnd`, `limit`

### `disaster_get_weather_alerts`
Get active NOAA/NWS weather alerts by state, severity, and event type. Real-time warnings, watches, and advisories.

```
Show severe weather alerts for Texas
Any tornado warnings active right now?
```

Parameters: `states` (array), `severity` (Minor/Moderate/Severe/Extreme), `event`, `limit`

### `disaster_search_earthquakes`
Search USGS earthquake data by magnitude, date range, and alert level. Returns seismic events worldwide.

```
Show earthquakes above magnitude 5 in the last week
Any significant earthquakes near California?
```

Parameters: `minMagnitude` (0-10), `maxMagnitude`, `startDate`, `endDate`, `alertLevel` (green/yellow/orange/red), `limit`

## Data Sources

- **FEMA** — Federal Emergency Management Agency (disaster declarations)
- **NOAA/NWS** — National Weather Service (weather alerts)
- **USGS** — US Geological Survey (earthquake data)

## Use Cases

- Real-time disaster monitoring
- Emergency preparedness
- Insurance risk assessment
- Travel safety checks
- Supply chain disruption tracking

All data from free US government APIs. Zero cost. No API keys required.
