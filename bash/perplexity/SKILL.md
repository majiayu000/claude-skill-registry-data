---
name: perplexity
description: Search the web with AI-powered answers via Perplexity API. Returns grounded responses with citations. Supports batch queries.
homepage: https://docs.perplexity.ai
metadata: {"clawdbot": {"emoji": "\U0001F52E", "requires": {"bins": ["node"], "env": ["PERPLEXITY_API_KEY"]}, "primaryEnv": "PERPLEXITY_API_KEY"}}
display_name: "perplexity"
display_name_en: "perplexity"
description_zh: "Search the web with AI-powered answers via Perplexity API. Returns grounded responses with citations. Supports batch queries."
description_en: "Search the web with AI-powered answers via Perplexity API. Returns grounded responses with citations. Supports batch queries."
visibility: "public"
icon: "https://codebuddy-platform-1258344699.cos.accelerate.myqcloud.com/public/45edac6b-2078-4678-89f3-6f9800cf5e5f/avatar/skill/au_4f41104d-841.png"
---

# Perplexity Search

AI-powered web search that returns grounded answers with citations.

## Search

Single query:
```bash
node {baseDir}/scripts/search.mjs "what's happening in AI today"
```

Multiple queries (batch):
```bash
node {baseDir}/scripts/search.mjs "What is Perplexity?" "Latest AI news" "Best coffee in NYC"
```

## Options

- `--json`: Output raw JSON response

## Notes

- Requires `PERPLEXITY_API_KEY` environment variable
- Responses include citations when available
- Batch queries are processed in a single API call
