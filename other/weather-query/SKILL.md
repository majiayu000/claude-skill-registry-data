---
name: weather-query
description: Query current weather information for any location
version: 1.0.0
author: PonyBunny Team
tags: [weather, information, query]
phases: [conversation, execution]
user-invocable: true
requires-approval: false
primary-env: host
---

# Weather Query Skill

This skill helps you query current weather information for any location worldwide.

## When to Use This Skill

Use this skill when the user asks about:
- Current weather conditions
- Temperature in a specific location
- Weather forecasts
- Climate information

**Examples**:
- "What's the weather in London?"
- "Tell me the temperature in Tokyo"
- "Is it raining in New York?"
- "伦敦的气温是多少？"

## How to Use

### Step 1: Identify the Location

Extract the location from the user's query. Common patterns:
- "weather in [LOCATION]"
- "temperature in [LOCATION]"
- "[LOCATION] weather"
- "[LOCATION]的气温"

### Step 2: Use Web Search Tool

Use the `web_search` tool to query current weather:

```json
{
  "tool": "web_search",
  "parameters": {
    "query": "current weather in [LOCATION]"
  }
}
```

**Important**: Always include "current" in the query to get real-time data.

### Step 3: Extract Weather Information

From the search results, extract:
- Temperature (in Celsius and Fahrenheit if available)
- Weather condition (sunny, cloudy, rainy, etc.)
- Additional info (humidity, wind speed, etc.)

### Step 4: Format the Response

Provide a concise, natural response:

**Good response**:
```
London is currently 12°C (54°F), partly cloudy with light winds.
```

**Bad response** (too verbose):
```
I have searched for the weather information and found that according to 
multiple sources, the current temperature in London, United Kingdom is 
approximately 12 degrees Celsius, which converts to about 54 degrees 
Fahrenheit. The weather conditions show partly cloudy skies...
```

## Example Execution

**User**: "What's the weather in London?"

**Your thought process**:
1. Detect weather query → Use weather-query skill
2. Extract location: "London"
3. Call web_search with "current weather in London UK"
4. Extract: 12°C, partly cloudy
5. Respond concisely

**Your response**:
```
London is currently 12°C (54°F), partly cloudy with light winds.
```

## Error Handling

If the location is ambiguous:
- Ask for clarification: "Which London do you mean? London, UK or London, Ontario?"

If web_search fails:
- Apologize and suggest alternatives: "I'm unable to fetch weather data right now. You can check weather.com or bbc.com/weather for current conditions."

## Tips

- Always be concise (1-2 sentences max)
- Include both Celsius and Fahrenheit when possible
- Don't narrate the search process
- Don't apologize for using tools
- Just provide the answer directly
