---
name: Brave Search
description: Web search via Brave Search API with clean JSON results and minimal SEO noise.
requires:
  bins: []
  env: [BRAVE_SEARCH_API_KEY]
---

# Brave Search

Use this skill when the user asks for web search:
"find news about X", "what happened to Y", "find an article about Z".
It pairs well with `fetch-url` + `summarize`.

## Tools
- `status`
- `brave_search(query, count?, freshness?, country?, safesearch?)` —
  `freshness` accepts `pd|pw|pm|py` (past day/week/month/year)

Returns `{results: [{title, url, description, page_age, language}]}`.

## Setup
Get an API key at [brave.com/search/api](https://brave.com/search/api)
(free tier: ~2k queries/day).
