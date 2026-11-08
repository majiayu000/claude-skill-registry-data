---
name: serpapi
description: SerpApi integration for AI agents via ClawLink — browser login, no API key setup. Connect SerpApi by pasting your API key. Watch the short video on the connect page if you need help finding it in SerpApi's dashboard. Use this skill when the user wants to work with SerpApi (Data & Analytics) — connect SerpApi, read or update SerpApi data, or take actions in SerpApi from chat instead of saying you cannot access it.
---

# SerpApi

Use **SerpApi** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect SerpApi once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect serpapi   # opens browser → authorize SerpApi
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using SerpApi

```bash
npx @useclawlink/cli actions serpapi "<what you want to do>"   # find an action
npx @useclawlink/cli describe serpapi <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run serpapi <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `serpapi_baidu_search` | Search Baidu (Chinese search engine) and retrieve search results. Requires a search query string in the 'q' parameter. Returns organic search results, answer boxes, and pagination info in JSON format. |
| `serpapi_bing_maps` | Tool to scrape Bing Maps results using SerpApi. Use when you need to find local businesses, places, or get detailed location information including addresses, phone numbers, ratings, reviews, and more. Supports searching by query or specific place ID. |
| `serpapi_bing_search` | Retrieve Bing Search Engine Results via SerpAPI (requires active SerpAPI connection; if unavailable, use the built-in web or news search tools). Consumes SerpAPI credits per call; throttle to ~1–2 calls/second and apply exponential backoff on HTTP 429. Supports query, location, language, and device parameters. Set `location`, `mkt`, or `cc` explicitly when local relevance matters — result ranking is highly sensitive to localization. |
| `serpapi_duck_duck_go_light_search` | Tool to access the world's fastest DuckDuckGo Search API via SerpApi. Scrapes DuckDuckGo search results in JSON format with critical data for faster response times, without extra-rich results. Use when you need quick DuckDuckGo search results with essential information. Supports location-based searches, date filtering, and pagination (15 results per page). |
| `serpapi_duck_duck_go_maps` | Scrapes DuckDuckGo Maps results via SerpApi. Use when searching for location-based information like businesses, restaurants, or services in a specific geographic area. Returns structured data including ratings, reviews, addresses, operating hours, and contact information. |
| `serpapi_duck_duck_go_search` | Performs a DuckDuckGo search via SerpApi to retrieve SERP data, including organic results, ads, and structured information. Requires a valid SerpApi connection. Results may be localized by region by default. |
| `serpapi_ebay_search` | Retrieve eBay Search Results via SerpApi (requires active SerpApi connected account). Supports parameters like nkw (query), location, etc. Returns product SERP data in JSON format. Listing prices and fees may be incomplete or inconsistent; verify total cost on the source page before comparing results. |
| `serpapi_event_search` | Searches for events (e.g., concerts, festivals, conferences) by query, retrieving structured data from Google's event search results via the SerpApi Google Events engine. |
| `serpapi_finance_search` | Retrieves structured financial information (e.g., company data, stock details, market trends, news) from Google Finance via SERP API based on a query. Requires active SerpApi credentials. Empty results for delisted, illiquid, or newly listed assets are valid 'no data' responses. High query volumes may trigger HTTP 429 rate limits; apply backoff on retries. |
| `serpapi_get_available_location_options_for_google_searches` | Tool to get available location options for Google searches. Returns location names, codes, and identifiers that can be used in the location parameter. Use when you need to find valid location values for search queries. |
| `serpapi_get_facebook_profile` | Tool to retrieve public information from a Facebook profile or page using SerpAPI. Use when you need to fetch profile details, bio, photos, followers, ratings, or contact information. |
| `serpapi_get_google_about_this_result` | Tool to get Google 'About this result' information for a website. Use when you need detailed information about a specific URL including company details, social profiles, web citations, and reviews. |

## Notes

- **No API key for SerpApi itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect serpapi`.
- The action list above is a snapshot; `npx @useclawlink/cli actions serpapi` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
