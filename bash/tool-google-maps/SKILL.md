---
name: tool-google-maps
description: Query Google Maps APIs — distances (walking/driving/transit), nearby places by type, and geocoding — with built-in usage tracking to stay inside the $200/month free credit. Use when the user says "how far is X" / "多远", "distance from A to B", "nearby supermarkets/cafes", "geocode <address>", or "maps usage". NOT for in-EmptyOS geo features (use the geocode/routing apps).
---

# Google Maps Skill

> Verify distances, find nearby places, and geocode addresses using Google Maps APIs. Tracks usage to stay within $200/month free credit.

## Quick Start

```bash
# Walking distance (default)
python _claude/skills/google-maps/google_maps.py distance "6-8 Nile Close, Marsfield" "Macquarie Centre"

# Multiple destinations
python _claude/skills/google-maps/google_maps.py distance "origin" "dest1" "dest2" "dest3"

# Driving/transit
python _claude/skills/google-maps/google_maps.py distance --mode driving "origin" "dest"

# Find nearby places
python _claude/skills/google-maps/google_maps.py nearby "6-8 Nile Close, Marsfield" --type supermarket --radius 1000

# Geocode an address
python _claude/skills/google-maps/google_maps.py geocode "Macquarie University"

# Check usage
python _claude/skills/google-maps/google_maps.py usage
```

## Modes

### 1. Distance (`distance`)

Calculate distance and duration between origin and one or more destinations.

**Arguments:**
- Positional: `origin dest1 [dest2 ...]`
- `--mode`: walking (default), driving, transit, bicycling
- `--origin` / `--to`: named argument alternatives

**Output:** Distance (km), duration (min), travel mode for each destination.

**API cost:** $5 per 1,000 elements (1 element = 1 origin×destination pair)

### 2. Nearby (`nearby`)

Find places near an address.

**Arguments:**
- Positional: `address`
- `--type`: Place type (supermarket, pharmacy, gym, restaurant, etc.)
- `--radius`: Search radius in meters (default: 1000)

**Output:** Up to 10 results with name, address, distance, rating.

**API cost:** $32 per 1,000 requests — use sparingly!

### 3. Geocode (`geocode`)

Get coordinates for an address.

**Arguments:**
- Positional: `address`

**Output:** Latitude, longitude, formatted address.

**API cost:** $5 per 1,000 requests

### 4. Usage (`usage`)

Show current month's API usage and budget status.

**Output:** Call count, element count, estimated cost, budget remaining.

## Budget Management

Google Maps Platform gives **$200/month free credit**.

| Threshold | Action |
|-----------|--------|
| < 75% ($150) | Normal operation |
| 75-90% ($150-180) | Warning printed before each call |
| > 90% ($180) | **Hard stop** — refuses to make API calls |

Budget is tracked per calendar month in `usage.json`.

## Caching

Results are cached in `cache.json` with a **30-day TTL**:
- Cache key: `{mode}|{origin}|{destination}` (normalized)
- Cached results are returned instantly without API calls
- Run with `--no-cache` to bypass

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | This file |
| `google_maps.py` | Main script |
| `.env` | API key (`GOOGLE_MAPS_API_KEY=...`) |
| `usage.json` | Auto-created usage tracking |
| `cache.json` | Auto-created result cache |

## Trigger Words

| User Says | Action |
|-----------|--------|
| "多远" / "how far" / "walking distance" | Distance mode |
| "附近有什么" / "nearby" / "find places" | Nearby mode |
| "地址坐标" / "geocode" | Geocode mode |
| "API用量" / "maps usage" | Usage check |

## Important Notes

- **Never guess distances** — always use this skill (see MEMORY.md)
- Default origin for apartment queries: `6-8 Nile Close, Marsfield NSW 2122`
- Nearby search is expensive ($32/1k) — prefer Distance Matrix for known destinations
- Cache persists across sessions — no cost for repeated queries
