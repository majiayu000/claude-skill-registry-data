---
name: tokenhop-web-search
description: Web and X search via tokenhop /v1/search using Tavily / Exa / Brave / Serper / SearXNG / Google PSE / Linkup / SearchAPI / You.com / Perplexity / Xquik. Use when the user wants to search the web, find articles, or search public X posts.
---

# tokenhop — Web Search

Requires `TOKENHOP_URL` (and `TOKENHOP_KEY` if auth enabled). See <https://raw.githubusercontent.com/tokenhop/tokenhop/refs/heads/master/skills/tokenhop/SKILL.md> for setup.

If they are unset, use the legacy `NINEROUTER_URL` / `NINEROUTER_KEY` instead. <!-- legacy(9router): remove in v2 -->

## Discover

```bash
curl $TOKENHOP_URL/v1/models/web | jq '.data[] | select(.kind=="webSearch") | .id'
# Per-provider params (searchTypes, maxResults, required options like cx for google-pse)
curl "$TOKENHOP_URL/v1/models/info?id=tavily/search"
```

IDs end in `/search` (e.g. `tavily/search`). Combos (`owned_by:"combo"`) chain providers with auto-fallback.

## Endpoint

`POST $TOKENHOP_URL/v1/search`

| Field                                                | Required | Notes                                            |
| ---------------------------------------------------- | -------- | ------------------------------------------------ |
| `model` (or `provider`)                              | yes      | from `/v1/models/web` (e.g. `tavily` or `brave`) |
| `query`                                              | yes      | search query                                     |
| `max_results`                                        | no       | default 5                                        |
| `search_type`                                        | no       | `web` (default) / `news` / `x` for Xquik         |
| `country`, `language`, `time_range`, `domain_filter` | no       | provider-dependent                               |

## Examples

```bash
curl -X POST $TOKENHOP_URL/v1/search \
  -H "Authorization: Bearer $TOKENHOP_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"tavily","query":"tokenhop open source","max_results":5}'
```

JS:

```js
const r = await fetch(`${process.env.TOKENHOP_URL}/v1/search`, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${process.env.TOKENHOP_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ model: "search-combo", query: "latest LLM benchmarks", max_results: 10 }),
});
console.log(await r.json());
```

X search with Xquik:

```bash
curl -X POST $TOKENHOP_URL/v1/search \
  -H "Authorization: Bearer $TOKENHOP_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"xquik","query":"from:github release","max_results":10,"provider_options":{"queryType":"Latest"}}'
```

Add the Xquik API key in tokenhop's provider settings. Xquik charges 1 credit per returned post. Continue a search by passing `pagination.next_cursor` as `provider_options.cursor`.

Xquik responses include provider pagination and credit usage:

```json
{
  "pagination": { "has_more": true, "next_cursor": "cursor-2" },
  "usage": { "queries_used": 1, "search_cost_usd": null, "provider_credits_used": 10 }
}
```

## Response shape

```json
{
  "provider": "tavily",
  "query": "tokenhop open source",
  "results": [
    {
      "title": "...",
      "url": "https://...",
      "display_url": "github.com/...",
      "snippet": "...",
      "position": 1,
      "score": 0.92,
      "published_at": null,
      "favicon_url": null,
      "content": null,
      "metadata": { "author": null, "language": null, "source_type": null, "image_url": null },
      "citation": { "provider": "tavily", "retrieved_at": "2026-...", "rank": 1 }
    }
  ],
  "answer": null,
  "usage": { "queries_used": 1, "search_cost_usd": 0.008 },
  "metrics": { "response_time_ms": 850, "upstream_latency_ms": 700, "total_results_available": 12 },
  "errors": []
}
```

## Provider quirks

All accept `query` + `max_results`. Optional fields vary:

| Provider       | Supports                                                | Required extras                             |
| -------------- | ------------------------------------------------------- | ------------------------------------------- |
| `tavily`       | country, domain_filter, news topic                      | —                                           |
| `exa`          | domain_filter (incl/excl), news category                | —                                           |
| `brave-search` | country, language                                       | —                                           |
| `serper`       | country, language, news endpoint                        | —                                           |
| `perplexity`   | country, language, domain_filter                        | —                                           |
| `linkup`       | domain_filter, time_range                               | `depth: fast/standard/deep` (option)        |
| `google-pse`   | country, language, time_range, offset                   | **`cx` required** (providerOptions)         |
| `searchapi`    | country, language, pagination                           | —                                           |
| `youcom`       | country, language, time_range, domain_filter, full_page | —                                           |
| `searxng`      | language, time_range                                    | Self-hosted, **noAuth**                     |
| `xquik`        | X/Twitter search operators, language, cursor pagination | `queryType: Latest/Top`, `cursor` (options) |

Provider IS the model — `"provider":"tavily" ≡ "model":"tavily"`.
