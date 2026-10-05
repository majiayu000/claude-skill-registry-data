---
name: gsc
description: "Querying Google Search Console for search performance — top queries and pages, clicks/impressions/CTR/position over a date range, sitemap status, and URL indexing inspection."
homepage: https://developers.google.com/webmaster-tools/v1/searchanalytics/query
metadata:
  {
    "marketingclaw":
      {
        "emoji": "📈",
        "requires":
          {
            "bins": ["curl", "node", "jq"],
            "env": ["GOOGLE_APPLICATION_CREDENTIALS", "GSC_SITE_URL"],
          },
        "primaryEnv": "GOOGLE_APPLICATION_CREDENTIALS",
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "jq",
              "bins": ["jq"],
              "label": "Install jq (brew)",
            },
          ],
      },
  }
---

# Google Search Console Skill

Query the Search Console API (`searchanalytics.query`, sitemaps, URL inspection) using a
service-account access token minted locally — no OAuth consent flow, no third-party library.

## Setup

1. In Google Cloud Console: create (or reuse) a project, enable the **Search Console API**.
2. IAM & Admin → Service Accounts → create a service account → Keys → Add key → JSON. Download it.
3. In Search Console (`search.google.com/search-console`) → Settings → Users and permissions →
   Add user → paste the service account's `client_email` → grant at least **Full** (or Owner for
   sitemap submission) access to the property.
4. Set environment variables:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
   export GSC_SITE_URL="https://example.com/"          # or "sc-domain:example.com" for a domain property
   ```

Every call below first mints an access token, then hits the API:

```bash
TOKEN=$(node {baseDir}/scripts/google-sa-token.mjs)
```

`scripts/google-sa-token.mjs` is a plain Node script (no npm deps) that builds and signs a JWT
with the service account's private key and exchanges it at `oauth2.googleapis.com/token` for an
access token scoped to `webmasters.readonly` by default. It prints only the token to stdout.
Run `node {baseDir}/scripts/google-sa-token.mjs --help` for options (custom scope, alternate
credentials path).

## Search analytics: top queries and pages

```bash
TOKEN=$(node {baseDir}/scripts/google-sa-token.mjs)
SITE_URL_ENC=$(jq -rn --arg u "$GSC_SITE_URL" '$u | @uri')

curl -s -X POST \
  "https://www.googleapis.com/webmasters/v3/sites/${SITE_URL_ENC}/searchAnalytics/query" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "startDate": "2026-06-01",
    "endDate": "2026-06-30",
    "dimensions": ["query"],
    "rowLimit": 25000,
    "dataState": "final"
  }' | jq '.rows[] | {query: .keys[0], clicks, impressions, ctr, position}'
```

Swap `"dimensions": ["query"]` for `["page"]` (top pages), `["query", "page"]` (up to 4
dimensions combinable), `["date"]` (trend over time), or `["device"]`/`["country"]`. Add a
`dimensionFilterGroups` block to filter, e.g. queries containing a phrase:

```json
{
  "dimensionFilterGroups": [
    { "filters": [{ "dimension": "query", "operator": "contains", "expression": "pricing" }] }
  ]
}
```

`rowLimit` caps at 25,000 per request; page with `startRow` if you need more.

## Sitemaps

```bash
TOKEN=$(node {baseDir}/scripts/google-sa-token.mjs)
SITE_URL_ENC=$(jq -rn --arg u "$GSC_SITE_URL" '$u | @uri')

# List submitted sitemaps and their status
curl -s "https://www.googleapis.com/webmasters/v3/sites/${SITE_URL_ENC}/sitemaps" \
  -H "Authorization: Bearer ${TOKEN}" | jq '.sitemap[] | {path, lastSubmitted, isPending, warnings, errors}'

# Submit a new sitemap (write scope — see Notes)
SITEMAP_URL_ENC=$(jq -rn --arg u "${GSC_SITE_URL}sitemap.xml" '$u | @uri')
curl -s -X PUT \
  "https://www.googleapis.com/webmasters/v3/sites/${SITE_URL_ENC}/sitemaps/${SITEMAP_URL_ENC}" \
  -H "Authorization: Bearer ${TOKEN}"
```

## URL inspection

```bash
TOKEN=$(node {baseDir}/scripts/google-sa-token.mjs --scope "https://www.googleapis.com/auth/webmasters.readonly")

curl -s -X POST "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"inspectionUrl\": \"https://example.com/some-page\", \"siteUrl\": \"${GSC_SITE_URL}\"}" | \
  jq '.inspectionResult.indexStatusResult | {verdict, coverageState, robotsTxtState, lastCrawlTime}'
```

## Notes

- Read-only calls (`searchAnalytics.query`, sitemap list, URL inspection) work with the default
  `webmasters.readonly` scope. Sitemap submission (`PUT .../sitemaps/...`) needs the broader
  `https://www.googleapis.com/auth/webmasters` scope — pass
  `node {baseDir}/scripts/google-sa-token.mjs --scope "https://www.googleapis.com/auth/webmasters"`
  for that call.
- `GSC_SITE_URL` must exactly match how the property is registered in Search Console: a full
  URL-prefix property (`https://example.com/`, trailing slash) or a domain property
  (`sc-domain:example.com`, no scheme/slash, no URL-encoding needed for the `sc-domain:` form).
- Data typically has a 2-3 day lag; use `"dataState": "final"` for stable historical numbers.
- Feed this skill's query-mining output into `keyword-research` and its top-query/position data
  into `marketing-report` and `seo-audit`.
- **Verify on first use**: confirm `GSC_SITE_URL` matches the exact registered property string
  before relying on automated reports — a mismatch returns an empty result set, not an error.
