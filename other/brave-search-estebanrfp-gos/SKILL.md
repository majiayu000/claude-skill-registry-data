---
name: brave-search
description: Search the internet for information, news, and research. Web search via Brave Search API using web_fetch. Fast, structured results — no exec needed.
homepage: https://brave.com/search/api/
metadata: {"clawdbot":{"emoji":"🔍","requires":{"env":["BRAVE_API_KEY"]},"primaryEnv":"BRAVE_API_KEY"}}
---

# Brave Search

Web search using Brave Search API. Returns structured results (title, URL, description) via `web_fetch` — no shell execution needed.

## Search

```
web_fetch({
  url: "https://api.search.brave.com/res/v1/web/search?q=YOUR_QUERY&count=5",
  headers: {"Accept":"application/json","X-Subscription-Token":"YOUR_BRAVE_API_KEY"}
})
```

Replace `YOUR_BRAVE_API_KEY` with the value from `config get env.BRAVE_API_KEY`.

## Parameters

| Parameter | Description |
|-----------|-------------|
| `q` | Search query (required) |
| `count` | Number of results, 1-20 (default: 10) |
| `country` | 2-letter country code (e.g. `ES`, `US`) |
| `search_lang` | Language code (e.g. `es`, `en`) |
| `freshness` | Time filter: `pd` (day), `pw` (week), `pm` (month), `py` (year) |

## Response

Results are in `web.results[]`:

```json
{
  "web": {
    "results": [
      {
        "title": "Page title",
        "url": "https://example.com",
        "description": "Snippet text",
        "age": "2 hours ago"
      }
    ]
  }
}
```

## Setup

1. Get a free API key at https://brave.com/search/api/
2. Store it: `config set env.BRAVE_API_KEY your-key-here`

## Notes

- Free tier: 2,000 queries/month
- Uses `web_fetch` — works on all channels (no exec restriction)
- Structured JSON output — no HTML parsing needed
