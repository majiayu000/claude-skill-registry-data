---
name: query-weather
description: Retrieve current weather and forecast for a specific location. Use this skill when the user asks for weather information.
compatibility: opencode
---

# Query Weather

This skill allows you to fetch weather information for a given city or location.

## Instructions

1. **Identify the Location**: Extract the location/city name from the user's request. If no location is specified, default to "Beijing".
2. **Execute Weather Query**: Run the provided weather script.
   ```bash
   ~/.claude/skills/query-weather/weather.sh "<LOCATION>"
   ```
   *Replace `<LOCATION>` with the actual city name.*
3. **Present Results**: The script returns a formatted weather report. Present this information clearly to the user.
