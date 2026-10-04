---
name: mta
description: NYC MTA transit — real-time subway arrivals, bus predictions, service alerts, and route info for the New York City subway and bus system. Use when the user asks about NYC public transit, subway times, MTA bus arrivals, service alerts, or nearby stops.
homepage: "https://github.com/brianleach/mta-skill"
license: MIT
metadata:
  clawdbot:
    emoji: "🚇"
    tags: [transit, nyc, mta, transportation, subway, bus, train, schedule]
    requires:
      bins: ["node"]
      env: ["MTA_BUS_API_KEY"]
    files: ["scripts/mta.mjs", "proto/gtfs-realtime.proto", "proto/nyct-subway.proto"]
    install:
      - id: npm-deps
        kind: shell
        command: "npm install --prefix $SKILL_DIR"
        label: "Install Node.js dependencies (protobufjs)"
---

# NYC MTA Transit

Real-time New York City MTA transit data — subway arrivals (GTFS-RT protobuf), bus predictions (SIRI JSON API), service alerts, and route information. Subway and alerts work with zero config; bus data requires a free API key.

## When to Use

- User asks about NYC subway, MTA, the train, or specific lines (1/2/3, A/C/E, N/Q/R/W, etc.)
- User asks "when is the next train" in a New York City context
- User mentions specific NYC stations (Times Square, Penn Station, Grand Central, Union Square, etc.)
- User asks about NYC bus routes (M1, B52, Bx12, Q44, S79, etc.)
- User asks about MTA service alerts, delays, planned work, weekend service changes
- User asks about MTA fares, MetroCard, OMNY
- User asks about subway status or weekend service changes
- User asks about nearby subway stops or bus stops in NYC

## Data Sources

NYC MTA is multiple transit agencies with different data formats:

### Subway Real-Time Feeds (GTFS-RT Protobuf, NO key required)

Feeds are grouped by line division. Each returns protobuf binary with NYCT extensions (direction, track info).

| Feed | Lines | URL |
|------|-------|-----|
| 1234567/GS | 1, 2, 3, 4, 5, 6, 7, Grand Central Shuttle | `https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct/gtfs` |
| ACE | A, C, E, Rockaway Shuttle, Franklin Shuttle | `https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct/gtfs-ace` |
| BDFM | B, D, F, M | `https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct/gtfs-bdfm` |
| G | G | `https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct/gtfs-g` |
| JZ | J, Z | `https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct/gtfs-jz` |
| L | L | `https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct/gtfs-l` |
| NQRW | N, Q, R, W | `https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct/gtfs-nqrw` |
| SIR | Staten Island Railway | `https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct/gtfs-si` |

Feeds update every ~30 seconds. No API key required.

### Bus Real-Time (SIRI JSON API, requires `MTA_BUS_API_KEY`)

Get a free key at: https://register.developer.obanyc.com/

| Endpoint | Description |
|----------|-------------|
| SIRI StopMonitoring | Arrivals at a specific bus stop |
| SIRI VehicleMonitoring | All vehicles on a bus route |
| OneBusAway Stop Info | Stop details and nearby stops |
| OneBusAway Routes | Route discovery |

Rate limit: 1 request per 30 seconds.

### Service Alerts (GTFS-RT Protobuf, NO key required)

| Feed | URL |
|------|-----|
| Subway Alerts | `https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys/subway-alerts` |
| Bus Alerts | `https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys/bus-alerts` |
| All Alerts | `https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys/all-alerts` |

### GTFS Static Feed

| Feed | URL |
|------|-----|
| Subway | `http://web.mta.info/developers/data/nyct/subway/google_transit.zip` |

## Implementation

### Script: `scripts/mta.mjs`

Main entry point. Supports these commands:

```bash
# Subway arrivals
node scripts/mta.mjs arrivals --stop-search "times square"
node scripts/mta.mjs arrivals --stop-search "penn station" --line A
node scripts/mta.mjs arrivals --stop 127N
node scripts/mta.mjs arrivals --station "Grand Central"

# Bus arrivals (requires MTA_BUS_API_KEY)
node scripts/mta.mjs bus-arrivals --stop MTA_308209
node scripts/mta.mjs bus-arrivals --stop MTA_308209 --route M1

# Vehicle tracking
node scripts/mta.mjs vehicles --line 1
node scripts/mta.mjs bus-vehicles --route B52

# Service alerts
node scripts/mta.mjs alerts
node scripts/mta.mjs alerts --subway
node scripts/mta.mjs alerts --bus
node scripts/mta.mjs alerts --line A

# Routes and stops
node scripts/mta.mjs routes
node scripts/mta.mjs bus-routes
node scripts/mta.mjs stops --search "grand central"
node scripts/mta.mjs stops --near 40.7484,-73.9856
node scripts/mta.mjs bus-stops --near 40.7484,-73.9856
node scripts/mta.mjs bus-stops --route M1
node scripts/mta.mjs route-info --line A

# Maintenance
node scripts/mta.mjs refresh-gtfs
```

### Setup: Bus API Key

Subway and alert commands work with zero configuration. For bus commands:

1. Get a free key at https://register.developer.obanyc.com/
2. Set environment variable: `MTA_BUS_API_KEY`

### Setup: GTFS Static Data

On first use, run `node scripts/mta.mjs refresh-gtfs` to download subway stop/route data to `~/.mta/gtfs/`. Refresh periodically (data updates hourly).

### NYC Subway Lines Reference

| Line | Color | Route | Terminals |
|------|-------|-------|-----------|
| 1 | Red | 7th Ave Local | Van Cortlandt Park-242 St ↔ South Ferry |
| 2 | Red | 7th Ave Express | Wakefield-241 St ↔ Flatbush Ave-Brooklyn College |
| 3 | Red | 7th Ave Express | Harlem-148 St ↔ New Lots Ave |
| 4 | Green | Lexington Ave Express | Woodlawn ↔ Crown Heights-Utica Ave |
| 5 | Green | Lexington Ave Express | Eastchester-Dyre Ave ↔ Flatbush Ave-Brooklyn College |
| 6 | Green | Lexington Ave Local | Pelham Bay Park ↔ Brooklyn Bridge-City Hall |
| 7 | Purple | Flushing | Flushing-Main St ↔ 34 St-Hudson Yards |
| A | Blue | 8th Ave Express | Inwood-207 St ↔ Far Rockaway / Ozone Park-Lefferts Blvd |
| C | Blue | 8th Ave Local | 168 St ↔ Euclid Ave |
| E | Blue | 8th Ave Local | Jamaica Center ↔ World Trade Center |
| B | Orange | 6th Ave Express | Bedford Park Blvd ↔ Brighton Beach |
| D | Orange | 6th Ave Express | Norwood-205 St ↔ Coney Island-Stillwell Ave |
| F | Orange | 6th Ave Local | Jamaica-179 St ↔ Coney Island-Stillwell Ave |
| M | Orange | 6th Ave Local | Middle Village-Metropolitan Ave ↔ Forest Hills-71 Ave |
| G | Light Green | Brooklyn-Queens Crosstown | Court Sq ↔ Church Ave |
| J | Brown | Nassau St | Jamaica Center ↔ Broad St |
| Z | Brown | Nassau St Express | Jamaica Center ↔ Broad St (Peak only) |
| L | Gray | 14th St-Canarsie | 8 Ave ↔ Canarsie-Rockaway Pkwy |
| N | Yellow | Broadway Express | Astoria-Ditmars Blvd ↔ Coney Island-Stillwell Ave |
| Q | Yellow | Broadway Express | 96 St ↔ Coney Island-Stillwell Ave |
| R | Yellow | Broadway Local | Forest Hills-71 Ave ↔ Bay Ridge-95 St |
| W | Yellow | Broadway Local | Astoria-Ditmars Blvd ↔ Whitehall St-South Ferry |
| S | Gray | 42nd St Shuttle | Times Sq-42 St ↔ Grand Central-42 St |
| S | Gray | Franklin Ave Shuttle | Franklin Ave ↔ Prospect Park |
| S | Gray | Rockaway Park Shuttle | Broad Channel ↔ Rockaway Park-Beach 116 St |
| SIR | Blue | Staten Island Railway | St George ↔ Tottenville |

### Key Bus Routes Reference

| Route | Name | Borough |
|-------|------|---------|
| M1 | 5th Ave / Madison Ave | Manhattan |
| M15 | 1st Ave / 2nd Ave | Manhattan |
| M34 | 34th Street Crosstown | Manhattan |
| M42 | 42nd Street Crosstown | Manhattan |
| M60 | LaGuardia Airport Link | Manhattan/Queens |
| B44 | Nostrand Ave | Brooklyn |
| B52 | Gates Ave/Greene Ave | Brooklyn |
| Bx12 | Fordham Road/Pelham Pkwy | Bronx |
| Q44 | Merrick Blvd/Cross Island | Queens |
| S79 | Hylan Blvd | Staten Island |
| X27 | Bay Ridge-Downtown Manhattan Express | Brooklyn |

### MTA Fares Reference (2025)

| Fare Type | Price |
|-----------|-------|
| Subway/Bus (OMNY tap or MetroCard) | $2.90 |
| Bus-to-bus / subway-to-bus transfer | Free within 2 hours |
| Express Bus | $7.00 |
| 7-Day Unlimited | $34.00 |
| 30-Day Unlimited | $132.00 |
| Single Ride (vending machine only) | $3.25 |
| Reduced Fare | $1.45 |

Payment via OMNY (contactless tap), MetroCard, or Ventra. Free transfers between subway and bus within 2 hours with OMNY.

### Tips for Users

- **Subway stop IDs** end with `N` (northbound/uptown) or `S` (southbound/downtown). Example: `127N` = Times Sq northbound
- **Subway works with zero config** — no API key needed for any subway command
- **Bus requires a free API key** — get one at https://register.developer.obanyc.com/
- **Alerts always work** — no key needed
- Multiple subway feeds exist; the skill automatically fetches the right one(s) for the line requested
- Use `--stop-search` for fuzzy name matching, `--stop` for exact stop IDs

### Error Handling

- If `MTA_BUS_API_KEY` is not set, bus commands print a helpful message with the signup URL; subway commands still work
- Invalid station/stop searches show "No matching station found"
- Network errors and API error responses produce friendly messages
- If a subway feed returns empty data, note that real-time data may be temporarily unavailable

### Response Formatting

When presenting transit info to the user:
- Lead with the most actionable info (next arrival time, active alerts)
- Show line letter/number + direction (e.g., "A train toward Far Rockaway, arriving 3 min")
- For subway: show "Approaching" for trains at the station, minutes for upcoming
- Show track info when available (actual vs scheduled track)
- Always mention active service alerts for the line being queried
- For buses: show route + destination + minutes/stops away
- Times in 12-hour format with AM/PM

## External Endpoints

| Endpoint | Data Sent | Data Received |
|----------|-----------|---------------|
| `api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct/gtfs*` | None (GET only) | Subway positions/arrivals (Protobuf) |
| `api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys/*-alerts` | None (GET only) | Service alerts (Protobuf) |
| `bustime.mta.info/api/siri/*` | API key (query param) | Bus arrivals/positions (JSON) |
| `bustime.mta.info/api/where/*` | API key (query param) | Stop/route discovery (JSON) |
| `web.mta.info/developers/data/nyct/subway/*` | None (GET only) | GTFS static data (ZIP) |

Subway and alert endpoints are open access with no authentication. Bus endpoints require a free API key passed as a query parameter.

## Security & Privacy

- **Subway: No credentials required** — subway and alert feeds are open access, no API keys or tokens
- **Bus: Free API key required** — passed as a URL query parameter to MTA's official BusTime API
- **No user data transmitted** — requests contain only API keys and route/stop identifiers, no personal information
- **Local storage only** — GTFS static data is cached locally at `~/.mta/gtfs/`; no data is written elsewhere
- **No telemetry** — this skill does not phone home or collect usage data
- **Input handling** — stop names and route IDs from user input are used only for local filtering, never interpolated into shell commands

## Trust Statement

This skill reads publicly available transit data from MTA's official feeds and APIs. The bus API key is used only for MTA BusTime API authentication. The skill does not access, store, or transmit any personal information beyond the API key configured by the user.
