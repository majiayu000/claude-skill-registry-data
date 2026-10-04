---
name: proxy-web-search
description: |
  Proxy Web Search Tool - Performs web searches via the OpenClaw Manager proxy.
  
  Use when:
  - Need to search the web for latest information, news, or real-time data
  - Need specific search engines (defaults to Quark, supports Sogou, and more)
  - Need to filter search results by time range or domain
  - Need to control result count and detail level
  
  This skill routes all search requests through the Manager Web Search Proxy
  (configured via `WEB_SEARCH_PROXY_URL` env var, required),
  which handles API key management automatically — no manual configuration needed.
  
  Supported search engines: search_std (basic), search_pro (advanced), search_pro_sogou (Sogou), search_pro_quark (Quark - default)
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["curl"], "envs": ["WEB_SEARCH_PROXY_URL"] },
      },
  }
---

# Proxy Web Search

Web search via the OpenClaw Manager Web Search Proxy. The Manager handles API key injection from encrypted storage automatically — no manual key configuration needed.

The proxy URL is configured via the `WEB_SEARCH_PROXY_URL` environment variable (required). If not set, the skill will not be available.

Defaults to using the `search_pro_quark` engine with 25 results.

## Quick Start

### Basic cURL Usage

```bash
curl --request POST \
  --url "${WEB_SEARCH_PROXY_URL}/" \
  --header 'Content-Type: application/json' \
  --data '{
    "search_query": "OpenClaw framework",
    "search_engine": "search_pro_quark",
    "search_intent": false,
    "count": 25
  }'
```

### Script Usage

A wrapper shell script is provided for convenience.

```bash
# Basic Search (defaults to search_pro_quark and 25 results)
./scripts/proxy_search.sh --query "AI development trends"

# Advanced Search
./scripts/proxy_search.sh \
  --query "latest open source LLMs" \
  --engine "search_pro_sogou" \
  --count 50 \
  --intent \
  --recency "oneWeek"
```

## Authentication

No authentication required — the proxy reads API keys internally from the Manager's encrypted secrets store.

## API Parameter Reference

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `search_query` | string | ✅ | - | Search content, recommended ≤70 chars |
| `search_engine` | enum | - | `search_pro_quark` | `search_std` / `search_pro` / `search_pro_sogou` / `search_pro_quark` |
| `search_intent` | boolean | - | `false` | Enable search intent recognition |
| `count` | integer | - | `25` | Result count, range 1-50 |
| `search_domain_filter` | string | - | - | Whitelist domain filter |
| `search_recency_filter` | enum | - | `noLimit` | `oneDay` / `oneWeek` / `oneMonth` / `oneYear` / `noLimit` |
| `content_size` | enum | - | `medium` | `medium` (summary) / `high` (detailed) |

## Search Engine Selection Guide

| Engine | Use Case |
|--------|----------|
| `search_pro_quark` | Quark search, tailored for specific advanced scenarios (**Default**) |
| `search_std` | Basic search, regular Q&A |
| `search_pro` | Advanced search, need more accurate results |
| `search_pro_sogou` | Sogou search, China domestic content |

## Response Structure

The proxy returns JSON directly.

```json
{
  "id": "task-id",
  "created": 1704067200,
  "request_id": "request-id",
  "search_intent": [
    {
      "query": "original query",
      "intent": "SEARCH_ALL",
      "keywords": "rewritten keywords"
    }
  ],
  "search_result": [
    {
      "title": "title",
      "content": "content summary",
      "link": "result link",
      "media": "site name",
      "icon": "site icon",
      "refer": "reference number",
      "publish_date": "publish date"
    }
  ]
}
```

## Environment Requirements

- OpenClaw Manager must be running with the Web Search Proxy enabled.
- `WEB_SEARCH_PROXY_URL` environment variable must be set to the proxy URL (required, no default).
- `curl` command must be available in your system path.
