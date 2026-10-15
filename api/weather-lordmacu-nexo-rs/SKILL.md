---
name: Weather
description: Current conditions and 1–16 day forecasts via Open-Meteo (no API key).
requires:
  bins: []
  env: []
---

# Weather

Use this skill when the user asks for current weather or short forecasts for a
specific place. Backed by the `weather` extension (Open-Meteo provider).

## Use when

- "How is the weather in Madrid?"
- "Will it rain tomorrow in Bogota?"
- "Temperature in New York"
- "Weekly forecast for Tokyo"

## Do not use when

- Historical climate analysis (Open-Meteo Archive is a separate API)
- Severe weather emergency guidance
- Aviation or marine forecasting

## Tools

The `weather` extension exposes three tools.

### `status`
No arguments. Returns provider info, endpoints, client version. Use to verify
the extension is loaded.

### `current`
- `location` (string, required) — city or place name (e.g., "Madrid", "New York").
- `units` (string, optional) — `"metric"` (default) or `"imperial"`.

Returns:
```
{
  "location_query": "...",
  "units": "metric",
  "resolved": { "name", "country", "timezone", "lat", "lon" },
  "current": {
    "temperature", "feels_like", "humidity_pct",
    "wind_speed", "wind_dir_deg", "precipitation",
    "weather_code", "weather_desc", "is_day", "observed_at"
  }
}
```

### `forecast`
- `location` (string, required)
- `days` (integer, optional, 1–16, default 3)
- `units` (string, optional)

Returns `forecast: [{ date, min, max, precipitation_sum, wind_max, weather_code, weather_desc }, ...]`.

## Execution guidance

- Ask for a location if the user did not provide one.
- Use `current` for "right now" questions, `forecast` for multi-day windows.
- Prefer concise output first (temperature + condition + wind), expand only if requested.
- If geocoding fails (`-32001 location not found`), suggest a more specific name or country.
- Units default to metric. Switch to imperial only if the user is clearly in an imperial-system region or asks for it.
- Report `resolved.name` + `resolved.country` so the user can verify the right place was matched.
