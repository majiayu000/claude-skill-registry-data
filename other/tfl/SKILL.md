---
name: tfl
description: London TfL transit — real-time Tube arrivals, bus predictions, line status, service disruptions, journey planning, and route info for the London Underground, DLR, Overground, Elizabeth line, and buses. Use when the user asks about London public transport, Tube times, bus arrivals, or TfL service status.
homepage: "https://github.com/brianleach/tfl-skill"
license: MIT
metadata:
  openclaw:
    emoji: "\U0001F1EC\U0001F1E7"
    tags: [transit, london, tfl, transportation, tube, underground, bus, train, schedule]
    primaryEnv: TFL_API_KEY
    requires:
      bins: ["node"]
    files: ["scripts/tfl.mjs"]
  minis:
    originalSource: "https://clawskills.sh/skills/brianleach-tfl"
    convertedAt: "2026-10-31T22:14:33.510Z"
    license: "MIT"
---

# TfL London Transit

Real-time London TfL transit data — Tube arrivals, bus predictions, line status, disruptions, journey planning, and route information. Uses TfL's single unified REST API for all modes. API key optional (free, recommended for higher rate limits).

## When to Use

- User asks about the Tube, London Underground, TfL, or London public transport
- User mentions specific Tube lines (Bakerloo, Central, Circle, District, Hammersmith & City, Jubilee, Metropolitan, Northern, Piccadilly, Victoria, Waterloo & City)
- User asks "is the Northern line running" or "when's the next Tube"
- User mentions London stations (King's Cross, Oxford Circus, Waterloo, Victoria, Paddington, etc.)
- User asks about London buses, DLR, Overground, Elizabeth line, or trams
- User asks about TfL service status, delays, disruptions, or planned closures
- User asks about Oyster, contactless, or TfL fares
- User asks about journey planning in London

## Data Sources

TfL has a **single unified REST API** (`api.tfl.gov.uk`) that returns JSON for ALL modes — Tube, bus, DLR, Overground, Elizabeth line, trams, river bus, cable car. No protobuf, no SIRI, no multiple feed formats. Just one clean REST API with consistent JSON responses.

**API key:** Register for a free `app_key` at https://api-portal.tfl.gov.uk/ — append `?app_key={KEY}` to requests. The API works without a key for basic usage but is rate-limited; with a key you get 500 requests per minute.

### Key Endpoints

| Endpoint | Description |
|----------|-------------|
| `/Line/Mode/tube/Status` | All Tube line statuses |
| `/Line/{lineId}/Status` | Specific line status |
| `/StopPoint/{naptanId}/Arrivals` | Arrivals at a stop |
| `/Line/{lineId}/Arrivals/{stopPointId}` | Arrivals filtered by line |
| `/StopPoint/Search/{query}` | Search stops by name |
| `/StopPoint?lat=&lon=&radius=` | Stops near location |
| `/Line/{lineId}/StopPoints` | Stops on a line |
| `/Line/{lineId}/Route/Sequence/{dir}` | Route stop sequence |
| `/Line/{lineId}/Disruption` | Disruptions on a line |
| `/Journey/JourneyResults/{from}/to/{to}` | Journey planning |
| `/Line/Mode/bus` | All bus routes |

All endpoints return JSON. Append `?app_key={KEY}` for authenticated requests.

## Implementation

### Quick Start: Use the helper scripts

The scripts in this skill's `scripts/` directory handle fetching, parsing, and presenting TfL data.

### Script: `scripts/tfl.mjs`

Main entry point. Supports these commands:

```bash
# Tube line status
node scripts/tfl.mjs status
node scripts/tfl.mjs status --all
node scripts/tfl.mjs status --line victoria

# Arrivals at a station
node scripts/tfl.mjs arrivals --station "Oxford Circus"
node scripts/tfl.mjs arrivals --stop 940GZZLUOXC
node scripts/tfl.mjs arrivals --stop-search "kings cross"
node scripts/tfl.mjs arrivals --stop-search "kings cross" --line piccadilly

# Bus arrivals
node scripts/tfl.mjs bus-arrivals --stop 490005183E
node scripts/tfl.mjs bus-arrivals --stop-search "oxford circus"
node scripts/tfl.mjs bus-arrivals --stop-search "oxford circus" --route 24

# Disruptions
node scripts/tfl.mjs disruptions
node scripts/tfl.mjs disruptions --line northern

# Routes and stops
node scripts/tfl.mjs routes
node scripts/tfl.mjs routes --all
node scripts/tfl.mjs bus-routes
node scripts/tfl.mjs stops --search "waterloo"
node scripts/tfl.mjs stops --near 51.5074,-0.1278 --radius 500
node scripts/tfl.mjs stops --line victoria
node scripts/tfl.mjs route-info --line bakerloo
node scripts/tfl.mjs route-info --route 24

# Journey planning
node scripts/tfl.mjs journey --from "waterloo" --to "kings cross"
node scripts/tfl.mjs journey --from "51.5031,-0.1132" --to "51.5308,-0.1238"
```

### Setup: API Key (Optional, Recommended)

Basic functionality works without a key (rate-limited). For 500 requests/minute:

1. Register at https://api-portal.tfl.gov.uk/
2. Set environment variable: `TFL_API_KEY`

### Tube Lines Reference

| Line ID | Line Name | Emoji | Terminals |
|---------|-----------|-------|-----------|
| bakerloo | Bakerloo | brown | Harrow & Wealdstone <-> Elephant & Castle |
| central | Central | red | Epping / Ealing Broadway <-> West Ruislip |
| circle | Circle | yellow | Hammersmith (loop via Liverpool Street) |
| district | District | green | Richmond / Ealing Broadway <-> Upminster |
| hammersmith-city | Hammersmith & City | pink | Hammersmith <-> Barking |
| jubilee | Jubilee | silver | Stanmore <-> Stratford |
| metropolitan | Metropolitan | magenta | Chesham / Amersham / Uxbridge <-> Aldgate |
| northern | Northern | black | Edgware / High Barnet <-> Morden / Battersea |
| piccadilly | Piccadilly | dark blue | Heathrow T5 / Uxbridge <-> Cockfosters |
| victoria | Victoria | light blue | Walthamstow Central <-> Brixton |
| waterloo-city | Waterloo & City | teal | Waterloo <-> Bank |

### Other TfL Rail Modes

| Line ID | Name | Type |
|---------|------|------|
| dlr | DLR | Docklands Light Railway |
| liberty | Liberty | Overground (Romford — Upminster) |
| lioness | Lioness | Overground (Watford — Euston) |
| mildmay | Mildmay | Overground (Stratford — Richmond/Clapham) |
| suffragette | Suffragette | Overground (Gospel Oak — Barking) |
| weaver | Weaver | Overground (Liverpool St — Enfield/Cheshunt/Chingford) |
| windrush | Windrush | Overground (Highbury — Crystal Palace/Clapham/W Croydon) |
| elizabeth | Elizabeth line | Crossrail |
| tram | London Trams | Croydon Tramlink |

### TfL Fares Reference (from March 2025)

| Fare Type | Price |
|-----------|-------|
| Tube Zone 1 (Oyster/contactless, peak) | £2.80 |
| Tube Zone 1 (Oyster/contactless, off-peak) | £2.70 |
| Tube Zones 1-2 (peak) | £2.80 |
| Tube Zones 1-2 (off-peak) | £2.70 |
| Tube Zones 1-3 (peak) | £3.50 |
| Tube Zones 1-3 (off-peak) | £2.80 |
| Bus & Tram (any journey) | £1.75 |
| Hopper fare (unlimited bus/tram within 1 hour) | £1.75 total |
| Daily cap Zones 1-2 | £8.90 |
| Weekly cap Zones 1-2 | £44.70 |
| Cash single (ticket machine) | £6.70 (Zone 1) |

Peak: Mon-Fri 6:30-9:30am and 4:00-7:00pm (except public holidays).

### Tips for Users

- **NaPTAN IDs** are the station identifiers — Tube stations use `940GZZLU{code}` format
- Use `--station` or `--stop-search` for name-based lookups; use `--stop` for exact NaPTAN IDs
- Times are shown in 24-hour format (London convention)
- The `arrivals` command uses `timeToStation` (seconds) from the TfL API for ETA
- Bus stops have their own NaPTAN IDs in `490{code}` format
- Journey planning returns fare estimates when available

### Error Handling

- If `TFL_API_KEY` is not set, requests still work but are rate-limited — a note is printed
- 429 rate limit responses print a helpful message with the key signup URL
- Invalid station/stop searches show "No matching station found" with suggestions
- Network errors and API error responses produce friendly messages
- Station closed or no service shows an appropriate message

### Response Formatting

When presenting transit info to the user:
- Lead with the most actionable info (next arrival time, line status)
- Show line name with color emoji (e.g., "🔴 Central: Good Service")
- Show times in 24-hour format (London convention)
- For arrivals: show line + destination + minutes (from `timeToStation / 60`)
- Show platform name when available
- For journey planning: show step-by-step with mode, line, duration, and fare
- Always mention disruptions for queried lines

## External Endpoints

| Endpoint | Data Sent | Data Received |
|----------|-----------|---------------|
| `api.tfl.gov.uk/Line/*/Status` | API key (query param, optional) | Line status (JSON) |
| `api.tfl.gov.uk/StopPoint/*/Arrivals` | API key (query param, optional) | Arrivals (JSON) |
| `api.tfl.gov.uk/StopPoint/Search/*` | API key (query param, optional) | Stop search results (JSON) |
| `api.tfl.gov.uk/StopPoint?lat=&lon=` | API key (query param, optional) | Nearby stops (JSON) |
| `api.tfl.gov.uk/Line/*/StopPoints` | API key (query param, optional) | Stops on line (JSON) |
| `api.tfl.gov.uk/Line/*/Route/Sequence/*` | API key (query param, optional) | Route sequence (JSON) |
| `api.tfl.gov.uk/Line/*/Disruption` | API key (query param, optional) | Disruptions (JSON) |
| `api.tfl.gov.uk/Journey/JourneyResults/*` | API key (query param, optional) | Journey results (JSON) |
| `api.tfl.gov.uk/Line/Mode/bus` | API key (query param, optional) | Bus routes (JSON) |

API key is passed as a query parameter to TfL's official API. No other user data is transmitted.

## Security & Privacy

- **API key optional** — TfL Unified API works without a key (rate-limited); with a free key you get 500 req/min
- **No user data transmitted** — requests contain only the optional API key and route/stop identifiers, no personal information
- **No local storage** — this skill does not write any files to disk (no GTFS cache needed — TfL is all live API)
- **No telemetry** — this skill does not phone home or collect usage data
- **Input handling** — stop names and route IDs from user input are URL-encoded in API queries, never interpolated into shell commands

## Trust Statement

This skill reads publicly available transit data from TfL's official Unified API. The optional API key is used only for TfL API rate-limit authentication. The skill does not access, store, or transmit any personal information beyond the API key configured by the user.
