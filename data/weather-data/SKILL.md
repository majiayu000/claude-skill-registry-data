---
name: weather-data
description: Fetch and analyze weather data for specified locations. Use when you need current weather conditions, forecasts, or weather-related analytics for decision-making or integration with Chainlit chat responses.
---

# Weather Data Skill

## Purpose

This skill enables fetching and analyzing real-time weather data from public APIs. It's useful for:
- Getting current weather conditions for any location
- Retrieving weather forecasts
- Integrating weather data into Chainlit chat responses
- Performing weather-based analytics

## How to Use This Skill

### 1. Fetch Current Weather
Use the helper script to get current weather for a location:

```bash
python scripts/fetch_weather.py --location "London" --units metric
```

### 2. Available Parameters
- `--location`: City name or coordinates (required)
- `--units`: metric (Celsius) or imperial (Fahrenheit), default: metric
- `--lang`: Language for response, default: en

### 3. Output Format
Returns JSON with:
- Temperature, feels like temperature
- Weather condition and description
- Humidity and pressure
- Wind speed and direction
- Sunrise/sunset times
- Data collection timestamp

## Example Integration with Chainlit

```python
import subprocess
import json

async def get_weather_response(location: str):
    # Call the weather skill
    result = subprocess.run(
        ["python", "scripts/fetch_weather.py", "--location", location],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        weather_data = json.loads(result.stdout)
        return format_weather_message(weather_data)
    else:
        return f"Could not fetch weather for {location}"

def format_weather_message(data):
    return f"""
    Weather in {data['city']}, {data['country']}:
    - Temperature: {data['temp']}°C (feels like {data['feels_like']}°C)
    - Condition: {data['description']}
    - Humidity: {data['humidity']}%
    - Wind: {data['wind_speed']} m/s
    """
```

## Supported Locations

The skill supports:
- City names (e.g., "London", "New York")
- City, Country format (e.g., "Paris, France")
- Coordinates in latitude,longitude format (e.g., "51.5074,-0.1278")

## Error Handling

The script includes error handling for:
- Invalid locations (returns helpful error message)
- Network connectivity issues
- API rate limiting
- Malformed coordinates

## Testing the Skill

Test with different locations:
```bash
# Major cities
python scripts/fetch_weather.py --location "Tokyo"

# With units specification
python scripts/fetch_weather.py --location "New York" --units imperial

# Using coordinates
python scripts/fetch_weather.py --location "51.5074,-0.1278"
```

## Data Sources

Uses Open-Meteo API (free, no authentication required):
- Real-time weather data
- Global coverage
- Accurate forecasts
- No rate limiting for reasonable use

## Notes

- Data is cached locally for 10 minutes to improve performance
- All temperature data is provided in the requested unit
- Wind speeds are in m/s (metric) or mph (imperial)
- Times are in UTC unless otherwise specified
