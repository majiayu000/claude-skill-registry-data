---
name: the-news
description: Access global news from thousands of sources via The News API. Use this skill whenever the user wants to fetch top stories, search all news articles, find similar articles, retrieve a specific article by UUID, or discover available news sources. Trigger on any request involving current events, news search, news filtering, or news data retrieval.
license: MIT
---

# The News

Provide global news from thousands of sources with exceptional response times. This skill wraps the [The News API](https://www.thenewsapi.com) and exposes five endpoints covering top stories, full article search, similar article discovery, single-article lookup, and source listing.

## Capability Overview

| Endpoint | Method | URL |
|----------|--------|-----|
| Top Stories | GET | `https://app-dohnbj5by5mp-api-wL1zlEdVM6DY.gateway.appmedo.com/v1/news/top` |
| All News | GET | `https://app-dohnbj5by5mp-api-W9z3M6eOKQVL.gateway.appmedo.com/v1/news/all` |
| Similar News | GET | `https://app-dohnbj5by5mp-api-m9xKXDbR1oka.gateway.appmedo.com/v1/news/similar/{uuid}` |
| News by UUID | GET | `https://app-dohnbj5by5mp-api-qYGWo8XA7M7Y.gateway.appmedo.com/v1/news/uuid/{uuid}` |
| Sources | GET | `https://app-dohnbj5by5mp-api-oLpZ7eD5jJ5a.gateway.appmedo.com/v1/news/sources` |

Base host: `app-dohnbj5by5mp-api-wL1zlEdVM6DY.gateway.appmedo.com`

**Authentication:** All endpoints are platform-managed. The API key is read from the environment (`INTEGRATIONS_API_KEY`) and sent via the `X-Gateway-Authorization: Bearer <key>` header. Never pass credentials as query parameters.

**Billing:** Each API call is billed. Avoid unnecessary repeated calls.

---

## End-to-End Workflow

Choose the endpoint that matches the user's intent:

1. **Top Stories** — fetching trending/top news globally or by country → `GET /v1/news/top`
2. **All News** — searching the complete article database with filters → `GET /v1/news/all`
3. **Similar News** — finding articles related to a known article UUID → `GET /v1/news/similar/{uuid}`
4. **News by UUID** — fetching a single article by its UUID → `GET /v1/news/uuid/{uuid}`
5. **Sources** — discovering source IDs/domains for use in filtering → `GET /v1/news/sources`

For full parameter tables and code samples, read the relevant reference file:

> Read `references/top-stories-api.md` for Top Stories spec and code.
> Read `references/all-news-api.md` for All News spec and code.
> Read `references/similar-news-api.md` for Similar News spec and code.
> Read `references/news-by-uuid-api.md` for News by UUID spec and code.
> Read `references/sources-api.md` for Sources spec and code.

---

## Generation-time Usage (Agent Direct Call)

The API key is a platform-managed credential. Read it from `process.env["INTEGRATIONS_API_KEY"]` and pass it as the `X-Gateway-Authorization` header.

General pattern:

```typescript
const apiKey = process.env["INTEGRATIONS_API_KEY"] ?? "";

async function callNewsApi(url: string): Promise<unknown> {
  const response = await fetch(url, {
    method: "GET",
    headers: {
      "Accept": "application/json",
      "X-Gateway-Authorization": `Bearer ${apiKey}`,
    },
  });

  if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
  return response.json();
}
```

All endpoints use the `X-Gateway-Authorization` header for authentication. See each `references/<endpoint>-api.md` for the full typed function with all parameters.

---

## Post-generation Usage (Edge Function Call from Application)

Each endpoint requires its own Edge Function to keep the API key off the browser. See each `references/<endpoint>-api.md` for the complete Edge Function boilerplate and frontend fetch helper.

**Security contract:**
- Client sends JSON `{ ...params }` to the Edge Function (no credentials from client).
- Edge Function reads the API key from `Deno.env.get("INTEGRATIONS_API_KEY")` and attaches it as `X-Gateway-Authorization: Bearer <key>`.
- 429 (rate limit) and 402 (insufficient balance) error bodies are forwarded verbatim to the client.

---

## Notes

- **Key security**: `INTEGRATIONS_API_KEY` is a platform-managed credential. In the post-generation (Edge Function) scenario, it must be stored in Deno environment variables and must never be exposed to the frontend.
- **Error handling**: Always handle `429` (rate limit) and `402` (insufficient balance) responses; also handle `401` (invalid token) and `403` (endpoint access restricted).
- **Billing**: Each API call is billed. Avoid unnecessary repeated calls.
- **Pagination limit**: Pagination supports up to 20,000 total results (`page` × `limit` ≤ 20,000).
- **Data freshness**: News data is fetched in real time; `published_at` uses UTC timezone.
