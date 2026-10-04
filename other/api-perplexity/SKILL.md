---
name: api-perplexity
description: "Search the live web via Perplexity Search API. Use when you need current documentation, release notes, vendor pages, news, domain-constrained web search, or date/recency filtering. Not for local codebase search or stable docs already in context."
---

# Perplexity Search API

Thin retrieval tool for live web search. The agent plans queries and interprets
results; this skill handles raw retrieval only.

**Endpoint:** `POST https://api.perplexity.ai/search`
**Auth:** `Authorization: Bearer $PERPLEXITY_API_KEY`
**Pricing:** $5.00 per 1K requests. No token-based charges.

## When to Use

- Current docs, changelogs, release notes
- Vendor/library documentation lookup
- News and time-sensitive information
- Domain-constrained retrieval (e.g. only official docs sites)
- Date-filtered search (published/updated before or after a date)

## When Not to Use

- Local codebase search (use Grep/finder)
- Stable docs already in context
- Page interaction or scraping (use browser tools)
- LLM-generated summaries (use Sonar API instead)

## Request Schema

All fields except `query` are optional.

| Field | Type | Default | Notes |
|---|---|---|---|
| `query` | `string \| string[]` | — | **Required.** Up to 5 queries for batch. |
| `max_results` | `integer` | `10` | Range: 1–20 |
| `max_tokens` | `integer` | `10000` | Total content budget across all results |
| `max_tokens_per_page` | `integer` | `4096` | Per-page content extraction limit |
| `country` | `string` | — | ISO 3166-1 alpha-2 (e.g. `"US"`, `"DE"`) |
| `search_language_filter` | `string[]` | — | ISO 639-1 codes, max 20 (e.g. `["en"]`) |
| `search_domain_filter` | `string[]` | — | Max 20. Prefix `"-"` to deny (see below) |
| `search_recency_filter` | `string` | — | `"hour"` `"day"` `"week"` `"month"` `"year"` |
| `search_after_date_filter` | `string` | — | `MM/DD/YYYY` — results published after |
| `search_before_date_filter` | `string` | — | `MM/DD/YYYY` — results published before |
| `last_updated_after_filter` | `string` | — | `MM/DD/YYYY` — results updated after |
| `last_updated_before_filter` | `string` | — | `MM/DD/YYYY` — results updated before |

### Domain Filter Rules

One array, two modes. **Cannot mix allow and deny in the same request.**

```json
// Allowlist — only these domains
"search_domain_filter": ["docs.stripe.com", "stripe.com"]

// Denylist — exclude these domains (prefix with "-")
"search_domain_filter": ["-pinterest.com", "-reddit.com", "-quora.com"]
```

## Response Schema

```ts
{
  id: string
  server_time: string | null
  results: Array<{
    title: string       // page title
    url: string         // page URL
    snippet: string     // extracted content
    date: string | null // publication date
    last_updated: string | null
  }>
}
```

**There is no `score` field.** Results are ranked by relevance — use list order
as rank. For single queries, `results` is a flat list. For multi-query batch,
results are grouped per query in submission order.

## Query Strategy

1. **Start narrow.** One precise query beats a broad one.
2. **Use domain filters before broadening query text.** Constrain sources first.
3. **Apply recency only when freshness matters.** Suppresses good evergreen content.
4. **Use low token budgets for quick lookups.** `max_tokens_per_page: 512` for headlines.
5. **Batch only for parallel angles.** Not for rephrasing the same question.
6. **Prefer 3–5 results** unless broad recall is needed.

## Examples

### Basic search

```bash
curl -X POST https://api.perplexity.ai/search \
  -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "drizzle orm sqlite migration guide",
    "max_results": 5
  }'
```

### Domain-constrained with recency

```bash
curl -X POST https://api.perplexity.ai/search \
  -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "breaking changes v5",
    "max_results": 5,
    "search_domain_filter": ["docs.stripe.com"],
    "search_recency_filter": "month"
  }'
```

### Date-filtered search

```bash
curl -X POST https://api.perplexity.ai/search \
  -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "vite 7 release",
    "max_results": 5,
    "search_after_date_filter": "01/01/2026"
  }'
```

### Lightweight extraction

```bash
curl -X POST https://api.perplexity.ai/search \
  -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "latest AI developments",
    "max_results": 3,
    "max_tokens": 3000,
    "max_tokens_per_page": 512
  }'
```

### Multi-query batch

```bash
curl -X POST https://api.perplexity.ai/search \
  -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": [
      "temporal workflow determinism typescript",
      "temporal activity heartbeat pattern"
    ],
    "max_results": 5,
    "search_domain_filter": ["docs.temporal.io"]
  }'
```

### Denylist with language filter

```bash
curl -X POST https://api.perplexity.ai/search \
  -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "react server components best practices",
    "max_results": 5,
    "search_domain_filter": ["-pinterest.com", "-w3schools.com"],
    "search_language_filter": ["en"]
  }'
```

## Guardrails

- **Date format is `MM/DD/YYYY`** — not ISO 8601.
- **Domain filter is one array** — allow or deny, not both simultaneously.
- **No score field** — trust result order; do not threshold on numeric scores.
- **`max_tokens` is content budget, not pricing** — controls how much text is extracted, not cost.
- **Batch limit is 5 queries** per request.
- **Deduplicate by URL** when combining results from multiple searches.
- **Cite sources** — include URLs in any answer derived from search results.

## Suggested Workflow

1. Decide if the task needs live web retrieval (current info, external docs).
2. Formulate 1–3 focused queries. Prefer domain filters over broad text.
3. Run search with appropriate `max_results` and token budgets.
4. Inspect top results — check URL relevance and snippet quality.
5. If results are thin, refine: adjust query, broaden domains, relax recency.
6. Synthesize answer from retained evidence. Cite URLs. Flag uncertainty when
   only one source supports a claim.
