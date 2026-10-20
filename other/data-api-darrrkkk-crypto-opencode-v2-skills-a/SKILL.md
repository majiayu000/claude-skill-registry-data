---
name: data-api
description: "Look up external data and generate 3D assets through Manus Data APIs — X/Twitter posts and profiles, LinkedIn people and companies, YouTube videos and captions, TikTok/Instagram/Reddit content, financial market data (prices, technical indicators, company financials), SEC filings and earnings call transcripts, Crunchbase companies and investors, World Bank indicators, Google Trends, App Store rankings, Similarweb website traffic, domain-name availability, and 3D models from text or images. Use when the task needs structured data from these sources instead of scraping web pages, or needs a 3D asset generated programmatically."
compatibility: opencode
---

# Manus Data API

Use the bundled scripts; the API catalog, eligibility rules, pricing, and provider credentials stay on the Manus service.

## Sources

Pick the one `source` key that matches the task:

| source | use when |
|---|---|
| `x-twitter` | Search public posts, look up user profiles, and fetch a user's recent tweets and timelines with engagement metrics. |
| `linkedin` | Fetch a person's profile by username, search people by role or keyword, and get company details for professional background or employment history. |
| `youtube` | Search videos by keyword, fetch video details and view statistics, list a channel's uploads, and extract video captions. Not for understanding what a video actually shows or says — for that, run `manus-analyze-video <youtube_url> "<question>"` instead of this source. |
| `social-media` | Get structured content from TikTok, Instagram, and Reddit — videos, creator info, account statistics, hot subreddit posts, and cross-platform video details with speech-to-text. |
| `financial-market` | Real-time and historical prices for stocks, options, forex and crypto, technical indicators, company financial statements and ratios, SEC EDGAR filings, macro series, and market news. |
| `earnings-research` | Primary sources on public companies — earnings call transcripts, annual and quarterly reports, SEC filings, investor presentations, and corporate event calendars. |
| `crunchbase` | Resolve companies, investors, and people to Crunchbase entities when identifying or disambiguating an organization or person in the startup ecosystem. |
| `world-bank` | World Bank development indicators — GDP, population, inflation, trade, education, health and other macroeconomic time series for every country and region. |
| `google-trends` | Google search interest for any keyword — trends over time, by region, and related queries. |
| `app-store` | Current top free iPhone apps from the US App Store with names, categories, and ranks. |
| `similarweb` | Website traffic and audience metrics — visits, engagement, global and country rank, traffic sources, referrals, keywords, and audience geography. |
| `domain-check` | Real-time domain-name availability when naming a product or preparing to register a domain. |
| `3d-model` | Generate 3D models from text descriptions or images. Generation is asynchronous: submit with text_to_model / image_to_model (upload the image first if needed), then poll get_task until the model is ready. |

## Usage

Use the directory containing this SKILL.md as `<skill-dir>`. `manus-node` is supplied by Manus in both the local computer and Sandbox. It requires no npm install or user Node setup. Authentication is automatic; never read, print, copy or manually pass tokens. If the runtime is unavailable, report that the Manus runtime needs updating.

Discovery and API calls require network access. When using `exec` on a local computer, set `network: true` so Manus can request the normal network permission. Offline data processing does not need this permission.

1. Discover APIs for the concrete task before every call:

```bash
manus-node "<skill-dir>/scripts/discover.mjs" --source <source> --query "<what data is needed>"
```

2. Choose only an `apiName` returned by discovery. Read its `docs`, `useWhen`, examples, defaults, and result limits. Some catalog examples use Python; use their API names and parameter shapes with the bundled JavaScript client.
3. Call it with explicit JSON arguments on the command line so Manus can estimate credits and request confirmation when needed:

```bash
manus-node "<skill-dir>/scripts/call.mjs" --api '<apiName>' --query-json '{"key":"value"}'
```

Use `--body-json`, `--path-params-json`, or `--multipart-form-data-json` when required by the discovered documentation. For single calls, keep the API name and JSON arguments visible in the command for credit estimation. Use an absolute script path (including when it contains spaces), or an explicit execution directory. For batching or data processing, write a `.mjs` script that imports `ApiClient` from `<skill-dir>/lib/data-api.mjs` (use `pathToFileURL` from `node:url` to import an absolute path portably, including Windows drive paths), uses `await client.callApi(apiName, { query, body, pathParams, multipartFormData })`, and runs with `manus-node`. Keep discovered API names and batch bounds explicit in the script so Manus can estimate credits; estimates for dynamic loops are approximate. Do not obscure calls to bypass confirmation. Never guess an API name or parameter. If discovery returns no suitable API, try another relevant `source`, or say the capability is unavailable and use another user-approved source.

## Source notes

- `financial-market` has 70+ APIs, so make `--query` specific — include the asset class (stock / option / forex / crypto / macro), the exact metric (e.g. "RSI", "income statement", "short interest", "treasury yields"), and use English keywords. A vague query like "Tesla" returns weaker matches than "Tesla daily stock price history OHLCV".
- `earnings-research` typical flow: resolve the company first (list_companies by ticker), then list events/reports/transcripts for it, then fetch the specific document by ID.
