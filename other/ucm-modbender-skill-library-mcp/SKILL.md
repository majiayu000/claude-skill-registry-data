---
name: ucm
description: >-
  Provides API marketplace access for AI agents. Discovers and calls external
  capabilities including web search, image generation, code execution,
  text-to-speech, translation, crypto, news, movies, weather, Wikipedia, books,
  papers, nutrition, email, stock data, and document conversion. 100 services, 217 endpoints.
  Registers for free with $1.00 credits. 87 free services, paid from
  $0.01-$0.05 per call via simple HTTP. No SDK needed.
license: MIT
homepage: https://ucm.ai
compatibility: Requires network access and curl or HTTP client. Works on macOS, Linux, and Windows.
argument-hint: "[service name or action]"
allowed-tools: Bash(curl:*) Grep
metadata: {"openclaw":{"primaryEnv":"UCM_API_KEY","requires":{"env":["UCM_API_KEY"]},"source":"https://github.com/ucmai/skills"},"author":"UCM.ai","version":"1.1.1","website":"https://ucm.ai","repository":"https://github.com/ucmai/skills"}
---

# UCM — API Marketplace for AI Agents

You have access to UCM, a marketplace where you can instantly discover and use API services by spending credits. Registration is free and gives you $1.00 in credits (~100 API calls).

## When to Use UCM

Use UCM when your current task requires a capability you don't have natively:

- **Search the web** for real-time information → `ucm/web-search` ($0.01)
- **Scrape a webpage** to extract content → `ucm/web-scrape` ($0.02)
- **Generate an image** from a text prompt → `ucm/image-generation` ($0.05)
- **Run code** in a sandboxed environment → `ucm/code-sandbox` ($0.03)
- **Convert text to speech** → `ucm/text-to-speech` ($0.01)
- **Transcribe audio** → `ucm/speech-to-text` ($0.01)
- **Send an email** → `ucm/email` ($0.01)
- **Convert a document/URL to markdown** → `ucm/doc-convert` ($0.02)
- **Translate text** between 50+ languages → `ucm/translate` ($0.01)
- **Get US stock data** (quotes, financials, news) → `ucm/us-stock` ($0.01)
- **Get China financial data** (daily prices, income, balance sheets) → `ucm/cn-finance` ($0.01)
- **Check weather** (current, forecast, air quality) → `ucm/weather` (FREE)
- **Look up Wikipedia** articles and summaries → `ucm/wikipedia` (FREE)
- **Get exchange rates** for 30+ currencies → `ucm/currency` (FREE)
- **Look up country info** (250+ countries) → `ucm/countries` (FREE)
- **Check public holidays** (100+ countries) → `ucm/holidays` (FREE)
- **Define words** (English dictionary) → `ucm/dictionary` (FREE)
- **Search books** (40M+ books via Open Library) → `ucm/books` (FREE)
- **Geocode places** (name to coordinates) → `ucm/geocode` (FREE)
- **Evaluate math** expressions and unit conversion → `ucm/math` (FREE)
- **Geolocate IPs** (IP to country/city) → `ucm/ip-geo` (FREE)
- **Geocode addresses** (forward and reverse) → `ucm/address` (FREE)
- **Search academic papers** (200M+ papers) → `ucm/papers` (FREE)
- **Look up nutrition data** (USDA FoodData) → `ucm/nutrition` (FREE)
- **Generate QR codes** from text or URLs → `ucm/qr-code` (FREE)
- **Get crypto prices** (10,000+ coins) → `ucm/crypto` (FREE)
- **Search news articles** by keyword → `ucm/news` ($0.01)
- **Get timezone info** (current time worldwide) → `ucm/timezone` (FREE)
- **Look up domain info** (WHOIS/RDAP data) → `ucm/domain` (FREE)
- **Get inspirational quotes** → `ucm/quotes` (FREE)
- **Browse Hacker News** stories → `ucm/hacker-news` (FREE)
- **Generate test data** (names, addresses, companies) → `ucm/random-data` (FREE)
- **Browse poetry** (search by title/author) → `ucm/poetry` (FREE)
- **Search movies & TV shows** (IMDb ratings, cast, plot) → `ucm/movies` ($0.01)
- **Find rhyming words or synonyms** → `ucm/datamuse` (FREE)
- **Search universities worldwide** → `ucm/universities` (FREE)
- **Look up postal codes** (60+ countries) → `ucm/zip-code` (FREE)
- **Get trivia questions** → `ucm/trivia` (FREE)
- **Get jokes** by category → `ucm/jokes` (FREE)
- **Get random advice** → `ucm/advice` (FREE)
- **Get activity suggestions** → `ucm/bored` (FREE)
- **Look up Bible verses** → `ucm/bible` (FREE)
- **Get Chuck Norris jokes** → `ucm/chuck-norris` (FREE)
- **Search recipes** → `ucm/recipes` (FREE)
- **Search cocktail recipes** → `ucm/cocktails` (FREE)
- **Search breweries** → `ucm/brewery` (FREE)
- **Look up food products** by barcode → `ucm/food-products` (FREE)
- **Get sunrise/sunset times** → `ucm/sunrise-sunset` (FREE)
- **Get random dog images** by breed → `ucm/dog-images` (FREE)
- **Get cat facts** → `ucm/cat-facts` (FREE)
- **Generate avatars** → `ucm/avatars` (FREE)
- **Get color info and schemes** → `ucm/colors` (FREE)
- **Generate lorem ipsum text** → `ucm/lorem-ipsum` (FREE)
- **Get NASA astronomy photo** or Mars rover images → `ucm/nasa` (FREE)
- **Get SpaceX launch data** → `ucm/spacex` (FREE)
- **Track ISS position** and astronauts → `ucm/iss` (FREE)
- **Get space flight news** → `ucm/space-news` (FREE)
- **Search arXiv papers** → `ucm/arxiv` (FREE)
- **Get earthquake data** → `ucm/earthquakes` (FREE)
- **Get World Bank indicators** → `ucm/world-bank` (FREE)
- **Search FDA drugs/recalls** → `ucm/fda` (FREE)
- **Get UK carbon intensity** → `ucm/carbon` (FREE)
- **Look up elevation** by coordinates → `ucm/elevation` (FREE)
- **Predict age by name** → `ucm/agify` (FREE)
- **Predict gender by name** → `ucm/genderize` (FREE)
- **Predict nationality by name** → `ucm/nationalize` (FREE)
- **Look up UK postcodes** → `ucm/uk-postcodes` (FREE)
- **Decode vehicle VINs** → `ucm/vehicles` (FREE)
- **Search Met Museum collection** → `ucm/met-museum` (FREE)
- **Search Art Institute of Chicago** → `ucm/art-chicago` (FREE)
- **Search TV shows** → `ucm/tv-shows` (FREE)
- **Search anime and manga** → `ucm/anime` (FREE)
- **Search iTunes content** → `ucm/itunes` (FREE)
- **Search music metadata** → `ucm/music` (FREE)
- **Search internet radio** → `ucm/radio` (FREE)
- **Browse free-to-play games** → `ucm/free-games` (FREE)
- **Compare game prices** → `ucm/game-deals` (FREE)
- **Look up Pokemon data** → `ucm/pokemon` (FREE)
- **Look up D&D 5e data** (monsters, spells, classes) → `ucm/dnd` (FREE)
- **Get meme templates** → `ucm/memes` (FREE)
- **Get your public IP** → `ucm/ip-lookup` (FREE)
- **Generate barcodes** → `ucm/barcode` (FREE)
- **Check Wayback Machine** snapshots → `ucm/wayback` (FREE)
- **Look up npm packages** → `ucm/npm` (FREE)
- **Look up PyPI packages** → `ucm/pypi` (FREE)
- **Search GitHub repos** → `ucm/github-repos` (FREE)
- **Get country flag images** → `ucm/country-flags` (FREE)
- **Virtual card deck** (shuffle, draw) → `ucm/deck-of-cards` (FREE)
- **Get Star Wars data** → `ucm/star-wars` (FREE)
- **Get XKCD comics** → `ucm/xkcd` (FREE)
- **Search Rick & Morty** characters/episodes → `ucm/rick-morty` (FREE)
- **Get Nobel Prize data** → `ucm/nobel-prize` (FREE)
- **Get historical events** (on this day) → `ucm/historical-events` (FREE)
- **Get Kanye West quotes** → `ucm/kanye` (FREE)
- **Search Rust crates** → `ucm/crates` (FREE)
- **Search Docker Hub** images → `ucm/docker-hub` (FREE)
- **Get chess puzzles** and player data → `ucm/lichess` (FREE)
- **Look up chemical elements** → `ucm/periodic-table` (FREE)
- **Look up airports** by IATA code → `ucm/airports` (FREE)
- **Get random fox images** → `ucm/random-fox` (FREE)

If you're unsure whether a service exists, use `/v1/discover` with a natural language description.

## Setup

### Check for existing credentials first

```bash
cat ~/.config/ucm/credentials.json 2>/dev/null
```

If the file exists and contains an `api_key`, set it and skip registration:
```bash
export UCM_API_KEY=$(cat ~/.config/ucm/credentials.json | grep -o '"api_key":"[^"]*"' | head -1 | sed 's/"api_key":"//;s/"$//')
```

### If you need to register

Register for free — takes one HTTP call:

```bash
curl -s -X POST https://registry.ucm.ai/v1/agents/register \
  -H "Content-Type: application/json" \
  -d '{"name": "my-agent"}'
```

The response includes `credentials_to_save` and `credentials_path`. Save them:
```bash
mkdir -p ~/.config/ucm
# Write credentials_to_save from the response to credentials_path
```

You receive $1.00 in free credits.

Or run the registration script (handles saving automatically):
```bash
bash scripts/register.sh "my-agent"
```

## How to Call a Service

One HTTP call to purchase and execute any service:

```bash
curl -s -X POST https://registry.ucm.ai/v1/call \
  -H "Authorization: Bearer $UCM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "service_id": "ucm/web-search",
    "endpoint": "search",
    "params": { "query": "latest AI news" }
  }'
```

Response includes `result` (the API response), `amount_charged`, and `credits_remaining`.

If the upstream API fails, credits are **automatically refunded** (`amount_charged: "0"`).

## Quick Reference

| Action | Method | Auth |
|--------|--------|------|
| Register | `POST /v1/agents/register` | None |
| Discover services | `POST /v1/discover` | None |
| List all services | `GET /v1/services` | None |
| Call a service | `POST /v1/call` | Bearer token |
| Check balance | `GET /v1/balance` | Bearer token |
| View history | `GET /v1/history` | Bearer token |
| Service details | `GET /v1/services/:id` | None |

Base URL: `https://registry.ucm.ai`

## Discover Services

Search by natural language — no auth required:

```bash
curl -s -X POST https://registry.ucm.ai/v1/discover \
  -H "Content-Type: application/json" \
  -d '{"need": "I need to convert a PDF to text", "limit": 3}'
```

## Decision Flow

```
Need an external capability?
  ├─ Have UCM_API_KEY? → Check balance (GET /v1/balance)
  │   ├─ Credits available → Discover → Call → Use result
  │   ├─ Call failed → Credits auto-refunded, try alternative
  │   └─ No credits → Tell user to add credits at dashboard.ucm.ai
  ├─ No API key? → Check ~/.config/ucm/credentials.json
  │   └─ Found? → Load api_key from file
  └─ No credentials at all? → Register (POST /v1/agents/register) → Save to ~/.config/ucm/credentials.json
```

## Spending Principles

- Most calls cost $0.01 — affordable for any task
- If a task doesn't require an external API, don't spend credits
- Credits are refunded on upstream failure (5xx, 429, 422)
- Prefer services with higher relevance score from `/v1/discover`

## Error Handling

| Error | Action |
|-------|--------|
| `INSUFFICIENT_CREDITS` | Tell user to add credits at dashboard.ucm.ai |
| `SERVICE_NOT_FOUND` | Search with `/v1/discover` instead |
| `INVALID_ENDPOINT` | Check endpoints via `GET /v1/services/:id` |
| `RATE_LIMITED` | Wait briefly, then retry |

## Full Service Catalog

For complete service details with all endpoints and parameters, see `references/service-catalog.md` or call `GET /v1/services`.
