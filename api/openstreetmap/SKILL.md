---
name: OpenStreetMap
description: Forward and reverse geocoding via Nominatim (no API key, ~1 req/sec).
requires:
  bins: []
  env: []
---

# OpenStreetMap

Use this skill for geocoding (place → coordinates) and reverse geocoding
(coordinates → address). Backed by the `openstreetmap` extension which calls
Nominatim. No API key needed.

## Use when

- "Find coordinates for this address"
- "What address is at lat 40.42, lon -3.70?"
- "Look up a place but avoid Google APIs"
- Need a free, no-key alternative to `goplaces` / Google Places

## Do not use when

- Need rich POI data (reviews, photos, opening hours) → use `goplaces`
- Need driving directions or routing
- High-frequency batch geocoding (Nominatim caps at ~1 req/sec)

## Tools

### `status`
No arguments. Returns provider/endpoint/rate-limit info.

### `search` (forward geocoding)
- `query` (string, required) — place query (e.g., "Museo del Prado, Madrid")
- `limit` (integer, optional, 1–20, default 5)
- `country_codes` (string, optional) — comma-separated ISO codes (e.g., "es,pt")

Returns `results: [{display_name, lat, lon, class, type, importance, boundingbox}]`.

### `reverse` (reverse geocoding)
- `lat` (number, required, -90..90)
- `lon` (number, required, -180..180)
- `zoom` (integer, optional, 0..18, default 18)

Returns `{display_name, resolved:{lat,lon}, address:{road,city,state,country,country_code,postcode,...}}`.

## Execution guidance

- Tool calls are throttled to ~1 req/sec per Nominatim usage policy. Do not loop fast.
- Prefer `country_codes` to disambiguate common place names ("Springfield", "Cambridge").
- Report `display_name` so the user can verify the right place was matched.
- If `search` returns `-32001 not found`, try a broader query or include the country.
- For routing/driving directions, OSM is not the right tool here.
