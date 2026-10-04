---
name: weather
description: Get current weather and forecasts with no API key using wttr.in and Open-Meteo.
version: 1.0.0
author: local
license: MIT
metadata:
  hermes:
    tags: [Weather, Forecast, wttr.in, Open-Meteo]
---

# weather

Two free weather services, no API keys required.

## wttr.in (primary)

Quick one-liner:
`curl -s "wttr.in/London?format=3"`

Compact format:
`curl -s "wttr.in/London?format=%l:+%c+%t+%h+%w"`

Full forecast:
`curl -s "wttr.in/London?T"`

Format codes:
- `%c` condition
- `%t` temperature
- `%h` humidity
- `%w` wind
- `%l` location
- `%m` moon

Tips:
- URL-encode spaces: `wttr.in/New+York`
- Airport codes work: `wttr.in/JFK`
- Units: `?m` metric, `?u` USCS
- Today only: `?1`, current only: `?0`
- PNG output: `curl -s "wttr.in/Berlin.png" -o weather.png`

## Open-Meteo (fallback JSON)

Programmatic JSON endpoint:
`curl -s "https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12&current_weather=true"`

Use this when you need structured fields like temperature, windspeed, and weathercode.
Docs: https://open-meteo.com/en/docs
