---
name: fetch-stores
description: Fetch store leads from Google Maps using Dumpling AI API. Use this skill when the user wants to search for businesses, stores, restaurants, or any places on Google Maps.
---

# Fetch Stores from Google Maps

This skill allows you to search for businesses and places using the Dumpling AI API, which queries Google Maps data.

## When to Use

Use this skill when the user:
- Wants to find stores, restaurants, or businesses in a specific area
- Asks for "best [type of business] in [location]"
- Needs to collect business leads or listings
- Wants to search Google Maps for places

## How to Use

Execute the script located at `scripts/fetch-stores.sh`:

```bash
fetch-stores.sh "search query" ["optional location"]
```

### Examples

```bash
# Search for restaurants in New York
fetch-stores.sh "best restaurants in New York"

# Search with separate location parameter
fetch-stores.sh "coffee shops" "San Francisco, CA"
```

## Prerequisites

The `DUMPLING_AI_API_KEY` environment variable must be set:

```bash
export DUMPLING_AI_API_KEY=your_api_key
```

## Output

- Results are saved to `/tmp/data/stores_[timestamp].json`
- The script displays:
  - Number of places found
  - Top 10 rated places with ratings and addresses
  - The best rated place with full details

## Response Format

The API returns places with the following information:
- `title`: Business name
- `rating`: Star rating (1-5)
- `ratingCount`: Number of reviews
- `address`: Full address
- `phoneNumber`: Contact phone
- `website`: Business website URL

## Guidelines

1. Always ask the user for their search query if not provided
2. Suggest adding a location for more relevant results
3. After fetching, summarize the top results for the user
4. If the API key is not set, guide the user to set it up
