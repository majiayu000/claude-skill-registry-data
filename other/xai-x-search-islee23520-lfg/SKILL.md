---
name: xai_x_search
description: Use when the user asks to search X, Twitter, posts, handles, tweets, or real-time social signal through Grok-connected xAI server-side x_search.
---

# xAI X Search

Use this skill for X/Twitter search through the Grok-connected xAI Responses server-side `x_search` tool.

## Preferred Grok Tool Flow

1. Use `search_tool` to discover the available tool schema first:

```json
{
  "query": "xai x search"
}
```

2. Call the returned xAI X-search MCP tool with the schema it reports. A typical payload is:

```json
{
  "prompt": "Summarize recent posts from @xai about Grok releases.",
  "allowed_x_handles": ["xai"]
}
```

## Options

- `prompt`: required X search request.
- `allowed_x_handles`: optional handles to include.
- `excluded_x_handles`: optional handles to exclude.

Do not pass both `allowed_x_handles` and `excluded_x_handles` in the same call.

## Evidence Discipline

Treat X posts as leads or primary-source statements only when the account identity matters. Corroborate factual claims with independent web/docs/repo evidence before presenting them as settled facts.

## Credential Safety

Use existing Grok/xAI credentials exposed by the host or MCP server. Never print, quote, summarize, or store OAuth tokens, refresh tokens, bearer tokens, or API keys.
