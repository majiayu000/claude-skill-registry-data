---
name: tavily
description: Search the internet for information, news, and research. AI-optimized web search via Tavily API using web_fetch. Returns concise, relevant results.
homepage: https://tavily.com
metadata: {"clawdbot":{"emoji":"🔍","requires":{"env":["TAVILY_API_KEY"]},"primaryEnv":"TAVILY_API_KEY"}}
---

# Tavily Search

AI-optimized web search using Tavily API via `web_fetch`. Designed for AI agents — returns clean, relevant content without HTML parsing.

## Search

```
web_fetch({
  url: "https://api.tavily.com/search",
  method: "POST",
  headers: {"Content-Type":"application/json"},
  body: "{\"api_key\":\"YOUR_TAVILY_API_KEY\",\"query\":\"YOUR_QUERY\",\"max_results\":5}"
})
```

Replace `YOUR_TAVILY_API_KEY` with the value from `config get env.TAVILY_API_KEY`.

## Parameters (in body JSON)

| Parameter | Description |
|-----------|-------------|
| `query` | Search query (required) |
| `max_results` | Number of results, 1-20 (default: 5) |
| `search_depth` | `"basic"` (default, fast) or `"advanced"` (deeper, slower) |
| `topic` | `"general"` (default) or `"news"` |
| `days` | For news topic, limit to last N days |
| `include_answer` | `true` to get an AI-synthesized answer |

## Response

```json
{
  "results": [
    {
      "title": "Page title",
      "url": "https://example.com",
      "content": "Relevant extracted content",
      "score": 0.95
    }
  ],
  "answer": "AI-synthesized answer (if include_answer: true)"
}
```

## Extract content from URL

```
web_fetch({
  url: "https://api.tavily.com/extract",
  method: "POST",
  headers: {"Content-Type":"application/json"},
  body: "{\"api_key\":\"YOUR_TAVILY_API_KEY\",\"urls\":[\"https://example.com/article\"]}"
})
```

## Setup

1. Get API key at https://tavily.com
2. Store it: `config set env.TAVILY_API_KEY your-key-here`

## Notes

- Free tier: 1,000 searches/month
- Uses `web_fetch` — works on all channels (no exec restriction)
- AI-optimized: returns clean snippets, not raw HTML
- `include_answer: true` gives a synthesized answer with citations
