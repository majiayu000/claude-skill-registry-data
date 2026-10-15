---
name: xai_web_search
description: Use when the user asks xAI/Grok to search the web, find current information, answer with citations, or use server-side web_search from a Grok-connected xAI tool.
---

# xAI Web Search

Use this skill for web-backed answers through the Grok-connected xAI Responses `web_search` tool.

## Preferred Grok Tool Flow

1. Use `search_tool` to discover the available tool schema first:

```json
{
  "query": "xai web search"
}
```

2. Call the returned xAI web-search MCP tool with the schema it reports. A typical payload is:

```json
{
  "prompt": "Find the latest xAI model announcement and summarize it with citations."
}
```

## Options

- `prompt`: required search question.
- `model`: optional Grok model, only when supported and needed.

Return a concise answer and include citations from the tool output when available. If the tool is unavailable, say so and use the host's normal web/search tools only if the user still wants a fallback.

## Credential Safety

Use existing Grok/xAI credentials exposed by the host or MCP server. Never print, quote, summarize, or store OAuth tokens, refresh tokens, bearer tokens, or API keys.
