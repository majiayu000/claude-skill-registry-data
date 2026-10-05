---

name: geo-tracker
version: 1.0.0
author: Hermes Agent
license: MIT
description: "Geospatial tracking MCP server — checkpoints, path tracking, phone GPS ingestion, geo-fencing, routing. Uses OpenStreetMap/OSRM (free, no API key)."
metadata:
  hermes:
    tags: [geospatial, gps, tracking, maps, geo-fence, location, checkpoint]
    category: productivity
    triggers: [tracking, gps, location, geo-fence, checkpoint, where-is-my-phone]
    requires_toolsets: [terminal]
    related_skills: [maps]
---
# Geo Tracker (Geospatial MCP Server)

Real-time geospatial tracking for Hermes agents. Combines OpenStreetMap geocoding/routing with checkpoint memory and phone GPS ingestion.

## How Phone GPS Works

The MCP server runs an HTTP endpoint on **port 8484** for OwnTracks GPS data:

1. **Install OwnTracks** (FOSS, Android/iOS) on your phone
2. Configure it to POST to `http://YOUR_VPS_IP:8484/location`
3. Phone's GPS is stored in SQLite and available via MCP tools

Alternatively, just tell me "I'm at the park" and I'll geocode it.

## MCP Tools

### Checkpoints (Memory)
- `checkpoint_set(name, lat, lon)` — "I parked the car here"
- `checkpoint_get(name)` — recall saved location
- `checkpoint_list()` — see all checkpoints
- `checkpoint_delete(name)` — remove one

### Path Tracking
- `track_start(name, lat, lon)` — start recording a path
- `track_point(name, lat, lon)` — add a waypoint
- `track_end(name)` — finish and get distance/duration/speed
- `track_summary(name)` — stats without ending

### Phone Location
- `phone_location_set(lat, lon)` — manual GPS update
- `phone_location_get()` — latest phone position + address
- `phone_location_history(limit)` — recent GPS trail
- `where_is_my_phone(from_checkpoint?)` — phone address + distance from checkpoint

### Distance & Routing
- `distance_between(from, to, mode)` — road distance + time
- `distance_from_checkpoint(checkpoint, to_lat, to_lon)` — how far from saved point
- `geocode(query)` — place name → coordinates
- `reverse_geocode(lat, lon)` — coordinates → address

### Geo-Fencing
- `geo_fence_create(name, center_lat, center_lon, radius_m)` — define a fence
- `geo_fence_check()` — phone inside/outside each fence?
- `geo_fence_list()` — all defined fences

## Server Path
`~/.hermes/skills/productivity/geo-tracker/scripts/geo_tracker_server.py`

## Dependencies
- Python 3.8+ stdlib (no pip installs needed)
- `mcp` package (for MCP protocol)
