---
name: dataforseo
description: Query live SERP data from Google, Bing, and YouTube via DataForSEO. See exactly what search results look like right now — organic results, featured snippets, knowledge graphs, AI overviews, local packs, and more.
allowed-tools: Bash, Read, Write, WebSearch
env:
  - DATAFORSEO_LOGIN
  - DATAFORSEO_PASSWORD
---

# DataForSEO SERP Analysis Skill

Query live search engine results pages via MCP tools. See real-time rankings, SERP features, and competitive positions across Google, Bing, and YouTube.

## Quick Start

```bash
# Full Google SERP (all elements)
mcp__dataforseo-serp__google_serp_live(keyword="your keyword", location_code=2840)

# Quick organic-only results (cheaper)
mcp__dataforseo-serp__google_serp_regular(keyword="your keyword", location_code=2840)

# Find location codes
mcp__dataforseo-serp__google_locations(query="London")

# YouTube rankings
mcp__dataforseo-serp__youtube_serp_live(keyword="your keyword")

# Bing comparison
mcp__dataforseo-serp__bing_serp_live(keyword="your keyword", location_code=2840)
```

## Tool Reference

### google_serp_live — Full SERP

All SERP elements: organic, paid, featured snippets, knowledge graph, AI overview, local pack, people also ask, images, videos.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `keyword` | string | Yes | — | Search query |
| `location_code` | number | No | — | Location code (use google_locations to find) |
| `location_name` | string | No | — | Alt: location name (e.g. "United States") |
| `language_code` | string | No | "en" | Language code |
| `device` | string | No | "desktop" | "desktop" or "mobile" |
| `depth` | number | No | 10 | Results count (10-100) |

### google_serp_regular — Quick Organic

Organic + paid results only. ~60% cheaper than advanced.

Same parameters as `google_serp_live`.

### google_locations — Location Lookup

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | string | No | Location name to search |
| `country` | string | No | Filter by country ISO code |

### google_languages — Language Codes

No parameters. Returns all available language codes.

### bing_serp_live — Bing SERP

Same parameters as `google_serp_live` (except no `device`).

### youtube_serp_live — YouTube Rankings

Same parameters as `google_serp_live` (except no `device`, default depth 20).

## Common Location Codes

| Code | Location |
|------|----------|
| 2840 | United States |
| 2826 | United Kingdom |
| 2276 | Germany |
| 2250 | France |
| 2392 | Japan |
| 2036 | Australia |
| 2124 | Canada |
| 2356 | India |
| 2076 | Brazil |
| 2724 | Spain |

## Workflows

### 1. Competitive SERP Analysis

```bash
mcp__dataforseo-serp__google_serp_live(keyword="your target keyword", location_code=2840, depth=20)
```

### 2. Cross-Engine Comparison

```bash
mcp__dataforseo-serp__google_serp_live(keyword="your keyword", location_code=2840)
mcp__dataforseo-serp__bing_serp_live(keyword="your keyword", location_code=2840)
```

### 3. Mobile vs Desktop

```bash
mcp__dataforseo-serp__google_serp_live(keyword="your keyword", location_code=2840, device="desktop")
mcp__dataforseo-serp__google_serp_live(keyword="your keyword", location_code=2840, device="mobile")
```

### 4. Local SERP Check

```bash
mcp__dataforseo-serp__google_locations(query="San Francisco")
mcp__dataforseo-serp__google_serp_live(keyword="coffee shops", location_code=1014221)
```

### 5. YouTube Video Research

```bash
mcp__dataforseo-serp__youtube_serp_live(keyword="your topic", depth=20)
```

## Integration with Other SEO Tools

Combine DataForSEO SERP data with:

- **Ahrefs**: Backlinks, DR, keyword difficulty
- **SE Ranking**: Keyword tracking over time
- **Search Console**: Your actual click/impression data

## Pricing

| Endpoint | Cost per Request |
|----------|-----------------|
| Google SERP Advanced | ~$0.0025 |
| Google SERP Regular | ~$0.001 |
| Bing SERP | ~$0.002 |
| YouTube SERP | ~$0.002 |
| Locations/Languages | Free |

New accounts get **$1 free credit** at [dataforseo.com](https://dataforseo.com/).
