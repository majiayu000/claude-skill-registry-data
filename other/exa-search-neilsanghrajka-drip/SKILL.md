---
name: exa-search
description: Use for generic Exa Search API research. Provides auth, request-shape, date-filter, batching, highlights, error-handling, and compact JSON evidence guidance for arbitrary caller-supplied queries. Query-agnostic; does not decide what to search for.
---

# Exa Search

Use Exa as a source-backed web search adapter. The caller decides the research question and query text. This skill explains how to execute Exa Search API calls and return compact evidence.

Do not use Exa MCP. Do not require an Exa CLI.

## Auth

Use `EXA_API_KEY` and never print its value.

```bash
curl -fsS "https://api.exa.ai/search" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $EXA_API_KEY" \
  -d '{"query":"<caller supplied query>","type":"fast","numResults":8,"contents":{"highlights":{"maxCharacters":500}}}'
```

## Request Guidance

- Use caller-provided queries. Do not invent a domain playbook inside this skill.
- Prefer `type: "fast"` for first-pass research.
- Use `numResults` between `5` and `10` unless the caller asks otherwise.
- Use `contents.highlights` for token-efficient evidence.
- Use published-date filters when the caller provides a time window.
- Use `category: "news"` only when the caller explicitly wants news-like recency.
- Avoid `category: "company"` unless the caller asks for company research.
- Use `moderation: true` when the caller needs safer public web results.
- Do not pull full page text unless a source is ambiguous and the caller needs deeper context.

Example request body:

```json
{
  "query": "<caller supplied query>",
  "type": "fast",
  "numResults": 8,
  "moderation": true,
  "startPublishedDate": "2026-06-03T00:00:00.000Z",
  "endPublishedDate": "2026-06-04T23:59:59.999Z",
  "contents": {
    "highlights": {
      "maxCharacters": 500
    },
    "livecrawlTimeout": 5000
  }
}
```

## Parallel Calls

When the caller supplies multiple query angles or topics, run independent Exa calls in parallel when practical. Keep the merged return compact; do not dump raw result sets into the parent context.

Parallelism is API-level. Do not spawn additional Codex subagents from this skill.

## Merge Rules

- Return title, URL, published date when available, and a short relevant highlight or summary.
- Deduplicate near-identical articles by normalized URL, title, and source domain.
- Prefer primary or source-rich pages over generic SEO pages.
- Preserve uncertainty instead of over-explaining weak evidence.
- Do not convert sources into product ideas. The caller owns interpretation.

## Return Shape

Return compact JSON-like evidence:

```json
{
  "source": "exa",
  "queriesRun": 2,
  "evidence": [
    {
      "query": "<query that found this>",
      "title": "Source title",
      "url": "https://example.com/story",
      "publishedDate": "2026-06-04T00:00:00.000Z",
      "highlight": "Short relevant excerpt or summary",
      "sourceDomain": "example.com"
    }
  ],
  "errors": []
}
```
