---
name: ga4
description: "Querying Google Analytics 4 via the Data API runReport — sessions/users/conversions by channel group, landing-page performance, UTM campaign breakdowns, and date-range comparisons."
homepage: https://developers.google.com/analytics/devguides/reporting/data/v1
metadata:
  {
    "marketingclaw":
      {
        "emoji": "📉",
        "requires":
          {
            "bins": ["curl", "node", "jq"],
            "env": ["GOOGLE_APPLICATION_CREDENTIALS", "GA4_PROPERTY_ID"],
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

# Google Analytics 4 Skill

Run report queries against the GA4 Data API (`properties.runReport`) using a service-account
access token minted locally. This skill is standalone — it ships its own copy of
`scripts/google-sa-token.mjs` (same script as the `gsc` skill, scoped to
`analytics.readonly` by default) so it works without the `gsc` skill installed.

## Setup

1. In Google Cloud Console: create (or reuse) a project, enable the **Google Analytics Data API**.
2. IAM & Admin → Service Accounts → create a service account → Keys → Add key → JSON. Download it.
3. In GA4 (analytics.google.com) → Admin → Property Access Management → add the service
   account's `client_email` as a user with **Viewer** access.
4. Find the GA4 property id: Admin → Property Settings → "Property ID" (numeric, no `properties/`
   prefix).
5. Set environment variables:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
   export GA4_PROPERTY_ID="123456789"
   ```

```bash
TOKEN=$(node {baseDir}/scripts/google-sa-token.mjs)
```

Run `node {baseDir}/scripts/google-sa-token.mjs --help` for options.

## Sessions/users/conversions by channel group

```bash
TOKEN=$(node {baseDir}/scripts/google-sa-token.mjs)

curl -s -X POST \
  "https://analyticsdata.googleapis.com/v1beta/properties/${GA4_PROPERTY_ID}:runReport" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "dateRanges": [{"startDate": "2026-06-01", "endDate": "2026-06-30"}],
    "dimensions": [{"name": "sessionDefaultChannelGroup"}],
    "metrics": [
      {"name": "sessions"},
      {"name": "totalUsers"},
      {"name": "conversions"},
      {"name": "engagementRate"}
    ],
    "orderBys": [{"metric": {"metricName": "sessions"}, "desc": true}]
  }' | jq '.rows[] | {channel: .dimensionValues[0].value, sessions: .metricValues[0].value, users: .metricValues[1].value, conversions: .metricValues[2].value, engagementRate: .metricValues[3].value}'
```

## Landing-page performance

```bash
TOKEN=$(node {baseDir}/scripts/google-sa-token.mjs)

curl -s -X POST \
  "https://analyticsdata.googleapis.com/v1beta/properties/${GA4_PROPERTY_ID}:runReport" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "dateRanges": [{"startDate": "2026-06-01", "endDate": "2026-06-30"}],
    "dimensions": [{"name": "landingPagePlusQueryString"}],
    "metrics": [{"name": "sessions"}, {"name": "conversions"}, {"name": "bounceRate"}],
    "orderBys": [{"metric": {"metricName": "sessions"}, "desc": true}],
    "limit": 25
  }' | jq '.rows[] | {page: .dimensionValues[0].value, sessions: .metricValues[0].value, conversions: .metricValues[1].value, bounceRate: .metricValues[2].value}'
```

## UTM campaign breakdown

```bash
TOKEN=$(node {baseDir}/scripts/google-sa-token.mjs)

curl -s -X POST \
  "https://analyticsdata.googleapis.com/v1beta/properties/${GA4_PROPERTY_ID}:runReport" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "dateRanges": [{"startDate": "2026-06-01", "endDate": "2026-06-30"}],
    "dimensions": [{"name": "sessionCampaignName"}, {"name": "sessionSource"}, {"name": "sessionMedium"}],
    "metrics": [{"name": "sessions"}, {"name": "conversions"}],
    "orderBys": [{"metric": {"metricName": "sessions"}, "desc": true}]
  }' | jq '.rows[] | {campaign: .dimensionValues[0].value, source: .dimensionValues[1].value, medium: .dimensionValues[2].value, sessions: .metricValues[0].value, conversions: .metricValues[1].value}'
```

Align UTM parameter conventions with whatever `BRAND.md` documents for the team, so campaigns
roll up consistently here.

## Date-range comparison (this period vs. prior period)

Use two named date ranges in one request instead of two calls:

```bash
TOKEN=$(node {baseDir}/scripts/google-sa-token.mjs)

curl -s -X POST \
  "https://analyticsdata.googleapis.com/v1beta/properties/${GA4_PROPERTY_ID}:runReport" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "dateRanges": [
      {"startDate": "2026-06-01", "endDate": "2026-06-30", "name": "current"},
      {"startDate": "2026-05-01", "endDate": "2026-05-31", "name": "previous"}
    ],
    "metrics": [{"name": "sessions"}, {"name": "totalUsers"}, {"name": "conversions"}]
  }' | jq '.rows[] | {range: .dimensionValues[-1].value, sessions: .metricValues[0].value, users: .metricValues[1].value, conversions: .metricValues[2].value}'
```

Named date ranges add a trailing `dateRange` dimension to each row automatically — no need to
add it to `dimensions` yourself.

## Notes

- `GA4_PROPERTY_ID` is the bare numeric id; the API path needs the `properties/` prefix, which
  the examples above already add.
- Relative date strings work too: `"today"`, `"yesterday"`, `"NdaysAgo"` (e.g. `"30daysAgo"`).
- Metric/dimension name reference: `https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema`.
  Requesting an incompatible dimension+metric pair returns a 400 with a clear message — read it,
  don't guess twice.
- Feed this skill's numbers into `marketing-report`'s traffic section.
- **Verify on first use**: dimension/metric availability can depend on the property's data
  streams and consent settings — confirm the exact names above still resolve for the property
  before automating a report on top of them.
