---
name: mvg
description: Munich public transport (MVG) CLI and S-Bahn live tracking. Use for departure times, route planning, nearby stations, service alerts, and real-time S-Bahn positions. Trigger when the user mentions MVG, S-Bahn, U-Bahn, Munich transit, departures, connections, Abfahrten, Verbindungen, or specific line names like S8, U3, etc.
---

# MVG CLI

Munich public transport from the terminal. Uses the unofficial MVG API (`bgw-pt/v3`) — no auth needed.

## Setup

- **CLI**: `python3 <skill_dir>/mvg_cli.py`
- **Dependencies**: Python 3, `urllib` (stdlib only)
- **S-Bahn Live**: Requires `node` + `ws` module for WebSocket connection

## Commands

```bash
# Station search
mvg search "Marienplatz"

# Departures
mvg departures "Marienplatz"
mvg departures "Marienplatz" --type ubahn --limit 20
mvg departures "Daglfing" --offset 5          # +5min walking time

# Route planning (stations or addresses)
mvg route "Marienplatz" "Garching"
mvg route "Hauptstr. 1, München" "Flughafen"  # address support
mvg route "Pasing" "Ostbahnhof" --time "08:30" --mode less-changes

# Nearby stations
mvg nearby                                     # default coords
mvg nearby 48.1351 11.5820

# Service alerts
mvg alerts
mvg alerts --station "Marienplatz"

# Lines
mvg lines --type sbahn

# S-Bahn live tracking (real-time via geOps WebSocket)
mvg live                                       # all S-Bahn lines
mvg live --line S3                             # specific line
```

All commands support `--json` for machine-readable output.

## Transport Type Filters

Use with `--type` or `--exclude`: `ubahn`, `sbahn`, `bus`, `tram`, `bahn` (RE/RB), `regionalbus`, `ruftaxi`

## Route Options

- `--mode`: `fast` (default), `less-changes`, `less-walking`
- `--walk-speed`: `slow`, `normal` (default), `fast`
- `--accessible`: wheelchair-accessible routes only
- `--via "Station"`: route via intermediate stop
- `--arrive`: interpret `--time` as arrival time

## API Notes

- Base URL: `https://www.mvg.de/api/bgw-pt/v3/`
- Endpoints: `/locations`, `/departures`, `/routes`, `/stations/nearby`, `/lines`, `/messages`
- Arrival time in route responses: use `to.plannedDeparture` (not `plannedArrival`)
- S-Bahn live: `wss://api.geops.io/realtime-ws/v1/` with `GET sbm_full` + `SUB sbm_full` + `BBOX`
- Delays from geOps are in milliseconds
