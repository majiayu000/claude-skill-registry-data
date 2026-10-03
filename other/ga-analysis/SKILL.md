---
name: ga-analysis
description: Fetch and analyze Google Analytics 4 organic-search data for SEO decisions — landing page conversions, engagement, source/medium mix, country/device splits, and opportunity clusters. Pairs with /gsc-analysis.
---

# GA Analysis Skill

You are an SEO growth analyst using Google Analytics 4 behavioral data to decide what to change on landing pages. Your job is to pair GA4 behavior metrics (engagement, conversions) with GSC search-demand data to find high-leverage fixes.

When this skill activates: `GA Analysis Mode: Fetching organic dataset...`

## Quick Start

```bash
node ./.Codex/skills/ga-analysis/scripts/ga-fetch.cjs --site=myimageupscaler.com --output=/tmp/ga-miu.json
```

## Configuration

- **Credentials:** same service account key as `/gsc-analysis` (`$GCP_KEY_FILE` or `~/projects/convertbanktoexcel.com/cloud/keys/coldstart-labs-service-account-key.json`)
- **Service Account:** `cloudstartlabs-service-acc@coldstartlabs-auth.iam.gserviceaccount.com`
- **Default GA4 Property ID:** `519826120` (myimageupscaler.com)
- **Organic filter:** `sessionDefaultChannelGroup = "Organic Search"` (override with `--organic-channel=`)

The service account must be granted **Viewer** access inside GA4 (Admin → Property Access Management). GA4 Data API access is property-scoped and completely separate from GSC access even when the same service account is used.

## What The Fetcher Pulls

- Organic vs total summary with previous-period comparison
- Channel mix (all channels, with session share and deltas)
- Organic landing pages with engagement + conversions (28-day comparison). Uses `pagePath` dimension with automatic fallback from `landingPagePlusQueryString` to avoid `(not set)` rows.
- Source/medium breakdown
- Page engagement (views, engagement duration, bounce rate, views/session) filtered to organic
- Country + device splits for organic traffic
- Daily trend (organic sessions)
- Opportunity clusters: high-traffic low-conversion, high-traffic low-engagement, declining pages, underperforming devices

Native Node.js `fetch` + `crypto`. No `googleapis` dependency.

## Example Commands

```bash
# Default 28-day window, default property
node ./.Codex/skills/ga-analysis/scripts/ga-fetch.cjs --site=myimageupscaler.com --output=/tmp/ga-miu.json

# Override property + window
node ./.Codex/skills/ga-analysis/scripts/ga-fetch.cjs --site=example.com --property-id=123456789 --days=90 --output=/tmp/ga-example.json

# Broader "organic" definition (include organic shopping, organic video)
node ./.Codex/skills/ga-analysis/scripts/ga-fetch.cjs --organic-channel="Organic Search" --output=/tmp/ga-miu.json

# Larger landing-page sample
node ./.Codex/skills/ga-analysis/scripts/ga-fetch.cjs --landing-page-limit=2000 --output=/tmp/ga-miu.json

# Check GA4 key-event setup for the SEO funnel
node ./.Codex/skills/ga-analysis/scripts/ga4-key-events.cjs

# Create missing key events when the service account has GA4 Editor access
node ./.Codex/skills/ga-analysis/scripts/ga4-key-events.cjs --create
```

Logs go to stderr. JSON goes to stdout unless `--output` is set.

## Output Shape

```json
{
  "meta": {},
  "summary": {
    "all":     { "current": {...}, "previous": {...}, "delta": {...}, "deltaPct": {...} },
    "organic": { "current": {...}, "previous": {...}, "delta": {...}, "deltaPct": {...} },
    "organicShare": { "sessions": 62.4, "conversions": 47.9 }
  },
  "channelMix": [
    { "channel": "Organic Search", "sessions": 0, "sessionsShare": 0, "sessionDeltaPct": 0 }
  ],
  "organic": {
    "landingPages": [],
    "countries": [],
    "devices": [],
    "dailyTrend": []
  },
  "sourceMedium": [],
  "pageEngagement": [],
  "opportunities": {
    "highTrafficLowConversion": [],
    "highTrafficLowEngagement": [],
    "decliningLandingPages": [],
    "underperformingDevices": []
  }
}
```

## Analysis Workflow

### Step 1: Fetch

```bash
node ./.Codex/skills/ga-analysis/scripts/ga-fetch.cjs --site=myimageupscaler.com --days=28 --output=/tmp/ga-miu.json 2>&1
```

### Step 2: Pair With GSC

Run `/gsc-analysis` in the same session. The two datasets are complementary:

- **GSC** tells you what users searched and clicked (demand, rankings, CTR)
- **GA4** tells you what happened after they clicked (engagement, conversions)

Join by landing-page URL. Use `/seo-growth-plan` if you want both fetched + joined automatically.

### Step 3: Read The JSON

Focus on:

1. `summary.organic` vs `summary.all` — is organic growing/shrinking versus total?
2. `summary.organicShare` — how dependent is the business on SEO right now?
3. `channelMix` — where growth is actually coming from (context for SEO conclusions)
4. `organic.landingPages` — top entry points, cross-reference with GSC pages
5. `opportunities.highTrafficLowConversion` — search demand exists, page fails to convert
6. `opportunities.highTrafficLowEngagement` — intent/UX mismatch
7. `opportunities.decliningLandingPages` — pages shedding organic traffic
8. `organic.devices` + `opportunities.underperformingDevices` — mobile/desktop gaps
9. `organic.countries` — geographic concentration, localization signal

### Step 4: Output

Present findings as markdown with:

- Period and comparison window
- Organic vs total summary with organic share
- Channel mix (only flag shifts ≥10 pts)
- Top landing pages (paired with GSC queries if available)
- Conversion opportunities (high-traffic, low CR)
- Engagement opportunities (high bounce)
- Declining pages
- Device/country gaps
- Prioritized actions

## Troubleshooting

### Credentials

```bash
ls -la ~/projects/convertbanktoexcel.com/cloud/keys/coldstart-labs-service-account-key.json
```

### Access Denied (403)

- Add the service account email as **Viewer** in GA4 Admin → Property Access Management
- Confirm property ID is the numeric one (e.g., `519826120`) — NOT the `G-XXXX` measurement ID
- Account-level access is not enough; access must be granted at the property

### Metric name errors

- If `conversions` returns a deprecation error, swap to `keyEvents` in `ga-fetch.cjs` (GA4 renamed the metric in 2024 and some properties enforce the new name)

### Data lag

- GA4 processing lag is typically 4–24 hours (much shorter than GSC's 2–3 day lag)
- Default `--lag-days=1` is conservative; drop to `0` for last-day data but numbers may still shift

### Organic scope

- `sessionDefaultChannelGroup = "Organic Search"` excludes Organic Shopping, Organic Video (YouTube), Organic Social
- Override with `--organic-channel=` if you want a different scope

## Cross-Reference With GSC

After running `/gsc-analysis` and `/ga-analysis`, look for:

1. **GSC-heavy, GA-light pages** — impressions but few sessions → tracking issue or URL mismatch
2. **High-CTR GSC pages with high GA bounce** — snippet matches intent but page doesn't
3. **GSC impression growth + GA session drop** — ranking up but clicks collapsed
4. **GSC cannibalization + GA split sessions** — consolidation candidates
5. **GSC position ≤10 + GA conversion rate <1%** — traffic exists, page isn't doing the job

For the automated join + synthesis, use `/seo-growth-plan`.

## Files

| Item         | Path                                                |
| ------------ | --------------------------------------------------- |
| Skill Doc    | `./.Codex/skills/ga-analysis/SKILL.md`             |
| Prompt       | `./.Codex/skills/ga-analysis/prompt.md`            |
| Fetch Script | `./.Codex/skills/ga-analysis/scripts/ga-fetch.cjs` |
