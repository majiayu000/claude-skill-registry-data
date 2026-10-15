---
name: xai_generate_text
description: Use when the user asks to generate, draft, answer, rewrite, summarize, or reason with xAI/Grok text generation through the Grok-connected xAI text tool.
---

# xAI Generate Text

Use this skill for text generation with Grok through the Grok-connected xAI Responses text tool.

## Preferred Grok Tool Flow

1. Use `search_tool` to discover the available tool schema first:

```json
{
  "query": "xai generate text"
}
```

2. Call the returned xAI text-generation MCP tool with the schema it reports. A typical payload is:

```json
{
  "prompt": "Write a concise release note for artifact-backed image generation.",
  "reasoning_effort": "medium"
}
```

## Options

- `prompt`: required user request.
- `model`: optional Grok model, only when the user or task requires a specific one.
- `reasoning_effort`: `low`, `medium`, or `high` when supported by the tool schema.

Use `xai_web_search` instead when the user asks for current web information. Use `xai_x_search` instead when the user asks to search X/Twitter.

## Credential Safety

Use existing Grok/xAI credentials exposed by the host or MCP server. Never print, quote, summarize, or store OAuth tokens, refresh tokens, bearer tokens, or API keys.
