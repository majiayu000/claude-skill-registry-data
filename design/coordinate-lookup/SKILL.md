---
name: Coordinate Lookup
description: This skill should be used when accurate GPS coordinates are needed for a location, when geocoding an address, or when coordinate lookup fails and manual intervention is required. Provides OpenStreetMap Nominatim API expertise and geocoding utilities.
version: 0.1.0
---

# Coordinate Lookup

## Overview

Find accurate GPS coordinates for locations using OpenStreetMap's Nominatim geocoding service. This skill provides knowledge for querying Nominatim API, handling multiple search strategies, and selecting the most relevant results.

## When to Use This Skill

Load this skill when:
- Finding GPS coordinates for a location name
- Geocoding addresses or place names
- Resolving ambiguous location queries
- Validating coordinate accuracy
- Troubleshooting failed coordinate lookups

## Core Concepts

### Nominatim API

Nominatim is OpenStreetMap's free geocoding service that converts place names and addresses into geographic coordinates.

**Key features:**
- Free to use (no API key required)
- Global coverage from OpenStreetMap data
- Multiple search strategies (place name, address, structured)
- Returns multiple results ranked by relevance
- Includes bounding boxes and administrative boundaries

**Base URL:** `https://nominatim.openstreetmap.org`

**Rate limit:** 1 request per second (enforced)

### Search Endpoint

**Basic search:**
```bash
GET /search?q={query}&format=json&limit=5
```

**Parameters:**
- `q` - Search query (location name, address, etc.)
- `format` - Response format (`json`, `jsonv2`, `xml`)
- `limit` - Maximum results (default 10, max 50)
- `countrycodes` - Restrict to countries (ISO 3166-1 alpha-2, comma-separated)
- `addressdetails` - Include address breakdown (`0` or `1`)

**Example:**
```bash
curl "https://nominatim.openstreetmap.org/search?q=Old+Man+of+Storr&format=json&limit=5"
```

### Response Format

```json
[
  {
    "place_id": 12345,
    "lat": "57.5062935",
    "lon": "-6.180885",
    "display_name": "Old Man of Storr, Isle of Skye, Highland, Scotland, UK",
    "type": "peak",
    "importance": 0.62,
    "boundingbox": ["57.5062935", "57.5062935", "-6.180885", "-6.180885"]
  }
]
```

**Key fields:**
- `lat` - Latitude (string, convert to number)
- `lon` - Longitude (string, convert to number)
- `display_name` - Full location description
- `type` - OSM feature type (peak, city, restaurant, etc.)
- `importance` - Relevance score (0-1, higher = more important)
- `boundingbox` - [min_lat, max_lat, min_lon, max_lon]

## Search Strategies

To find the most accurate coordinates, try multiple search strategies in order:

### 1. Exact Name Search

Start with the exact location name provided.

```bash
curl "https://nominatim.openstreetmap.org/search?q=University+of+Bristol+Botanic+Gardens&format=json&limit=3"
```

**Best for:** Well-known landmarks, specific venues

### 2. Name + Country/Region

Add geographic context if exact search fails or returns too many results.

```bash
curl "https://nominatim.openstreetmap.org/search?q=Dishoom+Edinburgh&countrycodes=gb&format=json&limit=3"
```

**Best for:** Common names, chain locations

### 3. Structured Search

Use structured query parameters for addresses.

```bash
GET /search?street={street}&city={city}&country={country}&format=json
```

**Best for:** Full addresses, specific properties

### 4. Reverse Search Variations

Try alternative name formats or common misspellings.

```bash
# Try without special characters
curl "https://nominatim.openstreetmap.org/search?q=Old+Man+Storr&format=json"

# Try alternative names
curl "https://nominatim.openstreetmap.org/search?q=The+Old+Man+of+Storr&format=json"
```

## Selecting Best Result

When multiple results returned, select based on:

1. **Type relevance:** Match expected type (restaurant, peak, park, etc.)
2. **Importance score:** Higher is generally more relevant
3. **Display name:** Should match expected location/region
4. **Bounding box:** Smaller box = more specific location

**Example logic:**
```python
# Sort by importance (descending)
results.sort(key=lambda x: float(x['importance']), reverse=True)

# Filter by expected type if known
if location_type == "restaurant":
    results = [r for r in results if r['type'] in ['restaurant', 'cafe', 'bar']]

# Take first (most relevant)
best_result = results[0]
coordinates = [float(best_result['lat']), float(best_result['lon'])]
```

## Error Handling

### No Results Found

**Causes:**
- Misspelled location name
- Very obscure or new location
- Location not in OpenStreetMap database

**Solutions:**
1. Try alternative name formats
2. Add geographic context (country, region)
3. Search for nearby landmark instead
4. Leave coordinates empty (graceful degradation)

### Rate Limit Exceeded

**Error:** HTTP 429 or "Too Many Requests"

**Solution:**
- Wait 1 second between requests
- Use `time.sleep(1)` in scripts
- Respect Nominatim usage policy

### Ambiguous Results

**Issue:** Multiple equally relevant results

**Solutions:**
1. Check `display_name` for region match
2. Use `countrycodes` parameter to filter
3. Compare `importance` scores
4. Ask user to confirm if uncertain

## Best Practices

### API Usage

1. **Add User-Agent header:**
   ```bash
   -H "User-Agent: ObsidianLocationNotes/0.1.0"
   ```
   Required by Nominatim usage policy

2. **Respect rate limit:** 1 request/second maximum

3. **Cache results:** Don't re-query same location

4. **Use countrycodes:** Filter results when country known
   ```bash
   &countrycodes=gb,ie  # UK and Ireland only
   ```

### Search Quality

1. **Remove special characters:** Convert "Old Man of Storr" → "Old Man Storr" if needed

2. **Try variations:** "Botanic Garden" vs "Botanical Gardens"

3. **Include city for businesses:** "Dishoom Edinburgh" not just "Dishoom"

4. **Check display_name:** Verify result matches expected region

### Coordinate Format

Convert API strings to numbers:

```python
lat = float(result['lat'])  # "57.5062935" → 57.5062935
lon = float(result['lon'])  # "-6.180885" → -6.180885
```

Store as array for Obsidian:
```yaml
location:
  - 57.5062935   # Latitude
  - -6.180885    # Longitude
```

## Common Use Cases

### Case 1: Find Coordinates for Landmark

```bash
# Query
curl -H "User-Agent: ObsidianLocationNotes/0.1.0" \
  "https://nominatim.openstreetmap.org/search?q=Eiffel+Tower&format=json&limit=1"

# Response
[{
  "lat": "48.8583701",
  "lon": "2.2944813",
  "display_name": "Eiffel Tower, Avenue Anatole France, Paris, France"
}]

# Result
[48.8583701, 2.2944813]
```

### Case 2: Geocode Restaurant with City

```bash
# Query with country filter
curl -H "User-Agent: ObsidianLocationNotes/0.1.0" \
  "https://nominatim.openstreetmap.org/search?q=Dishoom+Edinburgh&countrycodes=gb&format=json&limit=3"

# Select best result based on type=restaurant
# Result
[55.9533, -3.1883]
```

### Case 3: Handle Failed Lookup

```bash
# Query returns empty array
[]

# Fallback: Leave location empty
location: null  # or omit field entirely
```

## Utility Script

A bash script for coordinate lookup is provided:

### scripts/geocode.sh

```bash
#!/bin/bash
# Geocode a location using Nominatim API
# Usage: ./geocode.sh "Location Name" [country_code]

LOCATION="$1"
COUNTRY="${2:-}"

# Build query
QUERY="https://nominatim.openstreetmap.org/search"
QUERY+="?q=$(echo "$LOCATION" | sed 's/ /+/g')"
QUERY+="&format=json&limit=5"

if [ -n "$COUNTRY" ]; then
    QUERY+="&countrycodes=$COUNTRY"
fi

# Query API (with rate limit)
sleep 1  # Respect rate limit
RESPONSE=$(curl -s -H "User-Agent: ObsidianLocationNotes/0.1.0" "$QUERY")

# Parse first result
echo "$RESPONSE" | jq -r '.[0] | "\(.lat)\n\(.lon)\n\(.display_name)"'
```

**Usage:**
```bash
./geocode.sh "Old Man of Storr"
./geocode.sh "Dishoom" "gb"
```

## Validation

Check coordinates are valid:
- ✅ Latitude: -90 to 90
- ✅ Longitude: -180 to 180
- ✅ Minimum 6 decimal places for accuracy
- ✅ Matches expected region (check display_name)

**Example validation:**
```python
def validate_coordinates(lat, lon):
    if not (-90 <= lat <= 90):
        return False
    if not (-180 <= lon <= 180):
        return False
    return True
```

## Troubleshooting

**Issue:** Empty results
**Cause:** Location not in OSM or misspelled
**Fix:** Try alternative names, add geographic context, or leave empty

**Issue:** Wrong location returned
**Cause:** Ambiguous name (e.g., "Springfield" exists in many countries)
**Fix:** Add country/region to query, check display_name

**Issue:** Rate limit error
**Cause:** Requests too frequent
**Fix:** Add sleep(1) between requests, respect 1 req/second limit

**Issue:** Coordinates seem inaccurate
**Cause:** OSM data quality or location ambiguity
**Fix:** Verify display_name matches expected location, try structured search

## Additional Resources

For detailed API documentation and advanced features:
- **`references/nominatim-api.md`** - Complete API reference
- **`examples/geocode-examples.sh`** - Working search examples
- **`scripts/geocode.sh`** - Utility script for coordinate lookup

Use these resources when working with complex queries or troubleshooting coordinate issues.
