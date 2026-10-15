---
name: GoPlaces
description: Rich POI lookup via Google Places API (requires paid API key).
requires:
  bins: []
  env:
    - GOOGLE_PLACES_API_KEY
---

# GoPlaces

Use this skill for place lookup when the user asks for restaurants, stores,
addresses, maps links, or place details.

## Provider routing rule

- Default to `provider: "auto"`.
- In `auto`: use Google if `GOOGLE_PLACES_API_KEY` is available.
- If Google key is missing, fallback automatically to OpenStreetMap.
- If user explicitly requests one source, set `provider` explicitly:
  - `provider: "google"`
  - `provider: "openstreetmap"`

## Execution guidance

- Use `ext_goplaces_search_text` for query search.
- Use `ext_goplaces_place_details` when you already have a place id.
- For OpenStreetMap details, prefer `lookup_id` returned by `search_text`.
- You can also pass `osm_type` + `osm_id` explicitly (`node|way|relation`).
