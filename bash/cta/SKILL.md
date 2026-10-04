---
name: cta
description: Chicago CTA transit — real-time L train arrivals, bus predictions, service alerts, and route info. Use when the user asks about Chicago public transit, L train schedules, CTA bus times, service alerts, or nearby stops.
homepage: "https://github.com/brianleach/cta-skill"
license: MIT
metadata:
  clawhub:
    emoji: "🚇"
    tags: [transit, chicago, cta, transportation, bus, train, l-train, schedule]
    requires:
      bins: ["node", "unzip"]
      env: ["CTA_TRAIN_API_KEY", "CTA_BUS_API_KEY"]
    files: ["scripts/cta.mjs"]
    install:
      - id: npm-deps
        kind: shell
        command: "npm install --prefix $SKILL_DIR"
        label: "Install Node.js dependencies"
---

# CTA Chicago Transit

Real-time Chicago CTA transit data — L train arrivals, bus predictions, service alerts, and route information. Requires free API keys for train and bus data; alerts work without any keys.

## When to Use

- User asks about CTA, L train, Blue Line, Red Line, Brown Line, or any Chicago rail line
- User asks about Chicago bus routes, bus tracker, or train tracker
- User asks "when is the next train" or "is the Red Line running" in a Chicago context
- User mentions specific CTA stations (O'Hare, Midway, Clark/Lake, Belmont, etc.)
- User asks about CTA fares, Ventra, or how to ride Chicago transit
- User asks about CTA service alerts, delays, or detours
- User asks about nearby stops or route information in Chicago

## Data Sources

CTA uses 3 proprietary REST APIs. Train Tracker and Bus Tracker require free API keys. Customer Alerts is open access.

### Train Tracker API (requires `CTA_TRAIN_API_KEY`)

Get a free key at: https://www.transitchicago.com/developers/traintrackerapply/

| Endpoint | Description |
|----------|-------------|
| Arrivals by station (`mapid`) | Train arrivals at a parent station |
| Arrivals by stop (`stpid`) | Train arrivals at a directional stop |
| Train positions (`rt`) | Live positions of all trains on a line |
| Follow a run (`runnumber`) | Track a specific train run |

Data refreshes approximately once per minute. Daily limit: 50,000 requests per key.

### Bus Tracker API v2 (requires `CTA_BUS_API_KEY`)

Get a free key at: https://www.transitchicago.com/developers/bustracker/

| Endpoint | Description |
|----------|-------------|
| Predictions by stop | Bus arrival predictions at a stop |
| Predictions by vehicle | Predictions for a specific bus |
| Vehicle locations | Live bus positions on a route |
| Routes list | All active bus routes |
| Route directions | Available directions for a route |
| Stops for route/direction | All stops along a route |

Bus data updates approximately every 30 seconds.

### Customer Alerts API (NO key required)

| Endpoint | Description |
|----------|-------------|
| Route statuses | Current status of all routes |
| All alerts | All active service alerts |
| Alerts by route | Alerts filtered by route |
| Alerts by station | Alerts filtered by station |

### GTFS Static Feed

| Feed | Format | URL |
|------|--------|-----|
| GTFS Static (zip) | ZIP | `https://www.transitchicago.com/downloads/sch_data/google_transit.zip` |

Used for stop names, route info, and schedule lookups. Same stop IDs used across all APIs.

## Implementation

### Quick Start: Use the helper scripts

The scripts in this skill's `scripts/` directory handle fetching, parsing, and presenting CTA data.

### Script: `scripts/cta.mjs`

Main entry point. Supports these commands:

```bash
# L train arrivals
node scripts/cta.mjs arrivals --station "Clark/Lake"
node scripts/cta.mjs arrivals --mapid 40380
node scripts/cta.mjs arrivals --stop 30070
node scripts/cta.mjs arrivals --stop-search "ohare"
node scripts/cta.mjs arrivals --stop-search "belmont" --route Red

# Bus predictions
node scripts/cta.mjs bus-arrivals --stop 456
node scripts/cta.mjs bus-arrivals --stop 456 --route 22
node scripts/cta.mjs bus-arrivals --stop-search "michigan"

# Vehicle tracking
node scripts/cta.mjs vehicles --route Red
node scripts/cta.mjs bus-vehicles --route 22

# Service alerts
node scripts/cta.mjs alerts
node scripts/cta.mjs alerts --route Red

# Routes and stops
node scripts/cta.mjs routes
node scripts/cta.mjs bus-routes
node scripts/cta.mjs stops --search "belmont"
node scripts/cta.mjs stops --near 41.8781,-87.6298 --radius 0.3
node scripts/cta.mjs route-info --route Red
node scripts/cta.mjs route-info --route 22

# Maintenance
node scripts/cta.mjs refresh-gtfs
```

### Setup: API Keys

Train and bus commands require free API keys:

1. **Train Tracker key:** Apply at https://www.transitchicago.com/developers/traintrackerapply/
2. **Bus Tracker key:** Apply at https://www.transitchicago.com/developers/bustracker/
3. Set environment variables: `CTA_TRAIN_API_KEY` and `CTA_BUS_API_KEY`

Alert commands work without any keys.

### Setup: GTFS Static Data

On first use, run `node scripts/cta.mjs refresh-gtfs` to download and extract the static GTFS data (routes, stops, schedules) to `~/.cta/gtfs/`. This only needs to be refreshed when CTA updates their schedule.

### L Train Lines Reference

| Route Code | Line | Terminals |
|-----------|------|-----------|
| Red | Red Line | Howard ↔ 95th/Dan Ryan |
| Blue | Blue Line | O'Hare ↔ Forest Park |
| Brn | Brown Line | Kimball ↔ Loop |
| G | Green Line | Harlem/Lake ↔ Ashland/63rd or Cottage Grove |
| Org | Orange Line | Midway ↔ Loop |
| P | Purple Line | Linden ↔ Howard (Express to Loop weekdays) |
| Pink | Pink Line | 54th/Cermak ↔ Loop |
| Y | Yellow Line | Dempster-Skokie ↔ Howard |

### Key Bus Routes Reference

| Route | Name | Notes |
|-------|------|-------|
| 22 | Clark | Major north-south corridor |
| 36 | Broadway | North Side lakefront |
| 77 | Belmont | Major east-west crosstown |
| 151 | Sheridan | Lakefront express |
| 146 | Inner Drive/Michigan Express | Loop to north lakefront |
| 8 | Halsted | Long north-south route |
| 9 | Ashland | Major north-south corridor |
| 49 | Western | Longest route in system |
| 66 | Chicago | Major east-west route |
| 79 | 79th | Major south side east-west |

### CTA Fares Reference (2026)

| Fare Type | Price |
|-----------|-------|
| Regular (Ventra/contactless) | $2.50 |
| Bus transfer | $0.25 |
| Rail-to-rail transfer | Free within 2 hours |
| Reduced fare | $1.25 |
| 1-Day Pass | $5.00 |
| 3-Day Pass | $15.00 |
| 7-Day Pass | $20.00 |
| 30-Day Pass | $75.00 |

Payment via Ventra card, Ventra app, or contactless bank card. Transfers valid for 2 hours.

### Tips for Users

- **Station IDs** are in the 4xxxx range (parent stations); stop IDs in the 3xxxx range (directional)
- Use `--station` or `--stop-search` for name-based lookups; use `--mapid` for exact station IDs
- **Alerts** always work — no API key needed — so check alerts first if something seems wrong
- Train data refreshes ~1 minute; bus data refreshes ~30 seconds
- For the Loop, trains may show as arriving from different directions depending on the line

### Error Handling

- If `CTA_TRAIN_API_KEY` is not set, train commands print a helpful message with the signup URL
- If `CTA_BUS_API_KEY` is not set, bus commands print a helpful message with the signup URL
- Alert commands always work (no key required)
- Invalid station/stop searches show "No matching station found" with suggestions
- Network errors and API error responses produce friendly messages

### Response Formatting

When presenting transit info to the user:
- Lead with the most actionable info (next arrival time, active alerts)
- Show times in 12-hour format with AM/PM
- Include line color AND destination (e.g., "Red Line toward 95th/Dan Ryan")
- For trains: show "Due" for imminent arrivals, minutes for upcoming
- For bus predictions, show estimated minutes until arrival
- If there are active service alerts for the route being queried, always mention them

## External Endpoints

| Endpoint | Data Sent | Data Received |
|----------|-----------|---------------|
| `https://lapi.transitchicago.com/api/1.0/ttarrivals.aspx` | API key (query param, HTTPS) | Train arrivals (JSON) |
| `https://lapi.transitchicago.com/api/1.0/ttpositions.aspx` | API key (query param, HTTPS) | Train positions (JSON) |
| `https://lapi.transitchicago.com/api/1.0/ttfollow.aspx` | API key (query param, HTTPS) | Train run details (JSON) |
| `https://www.ctabustracker.com/bustime/api/v2/*` | API key (query param, HTTPS) | Bus predictions/positions (JSON) |
| `https://www.transitchicago.com/api/1.0/routes.aspx` | None (GET only) | Route statuses (JSON) |
| `https://www.transitchicago.com/api/1.0/alerts.aspx` | None (GET only) | Service alerts (JSON) |
| `https://www.transitchicago.com/downloads/sch_data/google_transit.zip` | None (GET only) | GTFS static data (ZIP) |

All API calls use HTTPS. API keys are passed as query parameters to CTA's official APIs. No other user data is transmitted.

## Security & Privacy

- **API keys required** — Train and Bus Tracker APIs require free developer keys passed as URL query parameters
- **No user data transmitted** — requests contain only API keys and route/stop identifiers, no personal information
- **Local storage only** — GTFS static data is cached locally at `~/.cta/gtfs/`; no data is written elsewhere
- **No telemetry** — this skill does not phone home or collect usage data
- **Input handling** — stop names and route IDs from user input are used only for local filtering, never interpolated into shell commands

## Trust Statement

This skill reads publicly available transit data from CTA's official APIs. API keys are used only for CTA API authentication. The skill does not access, store, or transmit any personal information beyond the API keys configured by the user.
