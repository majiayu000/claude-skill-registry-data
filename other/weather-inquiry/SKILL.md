---
name: weather-inquiry
description: Query real-time weather, forecasts, historical data, and AI weather summaries via the OpenWeatherMap One Call 3.0 API. Use this skill whenever the user needs current conditions, hourly/daily forecasts, historical weather for a timestamp, daily aggregated statistics, a human-readable weather overview, or wants to start/continue an AI weather assistant conversation.
license: MIT
---

# Weather Inquiry — OpenWeatherMap One Call 3.0

## Capabilities

Access weather data for any coordinate worldwide via the OpenWeatherMap One Call 3.0 API. Six capabilities are supported:

| Capability | Endpoint | API ID |
|------------|----------|--------|
| Current weather + forecast (minutely 1 h / hourly 48 h / daily 8 d) + alerts | `GET https://app-dohnbj5by5mp-api-wL1zlmgJGAlY.gateway.appmedo.com/data/3.0/onecall` | `api-wL1zlmgJGAlY` |
| Historical weather for a timestamp (1979-01-01 to +4 days) | `GET https://app-dohnbj5by5mp-api-Aa2PZmgJq5OL.gateway.appmedo.com/data/3.0/onecall/timemachine` | `api-Aa2PZmgJq5OL` |
| Daily aggregated weather statistics (1979-01-02 to +1.5 years) | `GET https://app-dohnbj5by5mp-api-2Y00zmgJ8lBY.gateway.appmedo.com/data/3.0/onecall/day_summary` | `api-2Y00zmgJ8lBY` |
| AI-generated weather overview (today / tomorrow natural-language summary) | `GET https://app-dohnbj5by5mp-api-oYA6ZxVqenDa.gateway.appmedo.com/data/3.0/onecall/overview` | `api-oYA6ZxVqenDa` |
| AI Weather Assistant — start new session | `POST https://app-dohnbj5by5mp-api-79jKPlpvAJ0L.gateway.appmedo.com/assistant/session` | `api-79jKPlpvAJ0L` |
| AI Weather Assistant — resume existing session | `POST https://app-dohnbj5by5mp-api-oYA6ZxVqyK8a.gateway.appmedo.com/assistant/session/{session_id}` | `api-oYA6ZxVqyK8a` |

- **Authentication**: `platform_managed` — API key is injected by the platform gateway; use `X-Gateway-Authorization: Bearer ${apiKey}` where `apiKey` comes from `process.env["INTEGRATIONS_API_KEY"]`
- **Data refresh**: Updated every 10 minutes (based on OpenWeather proprietary models)
- **Supported languages**: 50+ (specify via the `lang` parameter)
- **Billing**: Standard weather/forecast/history/overview and AI Assistant start-session endpoints are billed (AI Assistant resume-session endpoint is free) |

**Response example (current weather + forecast):**

```json
{
  "lat": 33.44,
  "lon": -94.04,
  "timezone": "America/Chicago",
  "current": {
    "dt": 1684929490,
    "temp": 292.55,
    "feels_like": 292.87,
    "pressure": 1014,
    "humidity": 89,
    "weather": [{"id": 803, "main": "Clouds", "description": "broken clouds"}]
  },
  "hourly": [...],
  "daily": [...]
}
```

> For full parameter documentation and code examples, see `references/onecall-api.md` (weather data endpoints) and `references/assistant-api.md` (AI assistant endpoints).

---

## Generation-time usage (Agent calls directly)

Use the built-in script for generation-time calls. The script reads `INTEGRATIONS_API_KEY` from the environment and sends it via the `X-Gateway-Authorization: Bearer <key>` header.

**The Bash tool timeout MUST be set to 600000ms (600 seconds).**

```bash
# Current weather + forecast
python3 <skill-path>/scripts/call_weather.py --endpoint onecall --lat 40.7128 --lon -74.0060 --units metric

# Historical weather for a timestamp
python3 <skill-path>/scripts/call_weather.py --endpoint timemachine --lat 40.7128 --lon -74.0060 --dt 1684929490

# Daily aggregated statistics
python3 <skill-path>/scripts/call_weather.py --endpoint day_summary --lat 40.7128 --lon -74.0060 --date "2024-06-15"

# AI weather overview
python3 <skill-path>/scripts/call_weather.py --endpoint overview --lat 40.7128 --lon -74.0060

# AI assistant — start a new session
python3 <skill-path>/scripts/call_weather.py --endpoint assistant_create --message "What is the weather like in New York today?"

# AI assistant — continue an existing session
python3 <skill-path>/scripts/call_weather.py --endpoint assistant_continue --session-id "<session_id>" --message "Will it rain tomorrow?"
```

The script prints `{"status":"succeed","result":{...}}` on success. On failure it prints an error to stderr and exits with a non-zero code.

See `references/onecall-api.md` (weather data endpoints) and `references/assistant-api.md` (AI assistant endpoints) for full parameter tables.

---

## Post-generation usage (in-app via Edge Function)

Deploy a separate Edge Function for each endpoint. The Edge Function injects `INTEGRATIONS_API_KEY` server-side, keeping the API key out of the client browser.

> For complete Edge Function code and frontend invocation examples, see the "Post-generation usage" sections in `references/onecall-api.md` and `references/assistant-api.md`.

---

## Notes

- **Key security**: `INTEGRATIONS_API_KEY` must only be read server-side (Edge Function or generation-time agent). Never expose it to the frontend browser.
- **Error handling**: Always handle 429 (quota exceeded) and 402 (insufficient balance).
- **Billing reminder**: Current weather+forecast, historical timestamp, daily aggregation, AI overview, and AI assistant start-session all incur a charge; AI assistant resume-session is free and suitable for follow-up questions at no extra cost.
- **Coordinate precision**: `lat` range −90 to 90, `lon` range −180 to 180, in decimal degrees.
- **Timestamps**: The `timemachine` endpoint's `dt` parameter is a UTC Unix timestamp; only 1979-01-01 to +4 days ahead is supported.
- **Units**: The `units` parameter defaults to `standard` (Kelvin). Use `metric` (Celsius) or `imperial` (Fahrenheit) for most user-facing applications.
