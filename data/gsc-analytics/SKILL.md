---
name: gsc-analytics
description: Google Search Console analytics — keyword rankings, indexation status, sitemaps. Uses google_auth tool + web_fetch (no CLI needed).
---

# GSC Analytics

Google Search Console data via service account + web_fetch. No CLI, no exec.

## Auth (ALWAYS do this first)

```
google_auth({ scope: "https://www.googleapis.com/auth/webmasters.readonly" })
```

Returns an access token. Use in all requests:
- Header: `{ "Authorization": "Bearer {token}", "Content-Type": "application/json" }`
- Base URL: `https://searchconsole.googleapis.com/webmasters/v3`

## Search Analytics (keywords, pages, dates)

```
web_fetch({
  url: "https://searchconsole.googleapis.com/webmasters/v3/sites/{siteUrl}/searchAnalytics/query",
  method: "POST",
  headers: { "Authorization": "Bearer {token}", "Content-Type": "application/json" },
  body: '{"startDate":"2026-02-24","endDate":"2026-03-24","dimensions":["query"],"rowLimit":25}'
})
```

Dimensions: `query`, `page`, `date`, `country`, `device`. Combine multiple in array.

Date format: `YYYY-MM-DD`. Max range: 16 months.

## URL Inspection

```
web_fetch({
  url: "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect",
  method: "POST",
  headers: { "Authorization": "Bearer {token}", "Content-Type": "application/json" },
  body: '{"inspectionUrl":"https://example.com/page","siteUrl":"https://example.com/"}'
})
```

Returns: indexing state, crawl info, robots.txt status, last crawl time.

## Sitemaps

### List sitemaps
```
web_fetch({
  url: "https://searchconsole.googleapis.com/webmasters/v3/sites/{siteUrl}/sitemaps",
  headers: { "Authorization": "Bearer {token}" }
})
```

### Submit sitemap
```
web_fetch({
  url: "https://searchconsole.googleapis.com/webmasters/v3/sites/{siteUrl}/sitemaps/{sitemapUrl}",
  method: "PUT",
  headers: { "Authorization": "Bearer {token}" }
})
```

## Sites

### List verified sites
```
web_fetch({
  url: "https://searchconsole.googleapis.com/webmasters/v3/sites",
  headers: { "Authorization": "Bearer {token}" }
})
```

## siteUrl format

- URL-encoded: `https%3A%2F%2Fexample.com%2F` or `sc-domain%3Aexample.com`
- Domain property: `sc-domain:example.com` (covers all protocols + subdomains)
- URL prefix: `https://example.com/`
- Start with listing sites to see available properties

## Workflow

1. `google_auth` with webmasters.readonly scope → get token
2. List sites → discover available properties
3. Query search analytics → keywords, pages, dates
4. Inspect URLs → indexation status
5. Check sitemaps → coverage
