---
name: synapse.weather
description: "Fetch real-time weather data for any city and report current conditions, temperature, and wind speed."
version: "1.0.0"
author: "synapse-core"
triggers: ["weather in", "what's the weather", "how's the weather", "temperature in", "forecast for"]
model_hint: "casual"
permissions: ["network:fetch"]
cloud_safe: false
enabled: true
entry_point: "scripts/weather.py:get_weather_context"
---

# Weather Skill

You have been provided live weather data from the Open-Meteo API. Use it to give a friendly,
concise weather report.

## When invoked

A user has asked about the weather. The `context_block` in your context contains current
conditions fetched from Open-Meteo. Use this data to answer.

## How to respond

1. **Lead with the current temperature** — state it in both Celsius and Fahrenheit.
2. **Describe the conditions** — use the WMO weather code to describe sky/rain/snow.
3. **Mention wind speed** briefly.
4. **Keep it conversational** — one short paragraph is ideal.
5. **If no data is available** (context_block is empty or shows an error), apologise and
   suggest the user check a weather app directly.

## WMO weather code guide (partial)

| Code | Condition |
|------|-----------|
| 0 | Clear sky |
| 1-3 | Mainly clear / partly cloudy / overcast |
| 45-48 | Fog |
| 51-57 | Drizzle |
| 61-67 | Rain |
| 71-77 | Snow |
| 80-82 | Rain showers |
| 95 | Thunderstorm |
| 96-99 | Thunderstorm with hail |

Use plain language — avoid technical jargon.
