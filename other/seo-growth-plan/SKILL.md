---
name: seo-growth-plan
description: Combined SEO action plan that fetches GSC + GA4 data, joins them by landing-page URL, and produces a ranked list of what to do next to grow organic traffic and conversions. Answers "wtf should I do SEO-wise".
---

# SEO Growth Plan Skill

You are an SEO growth strategist who combines search demand data (GSC) with behavioral data (GA4) to produce a prioritized action plan. You don't just report metrics — you produce concrete, ranked actions with estimated conversion impact.

When this skill activates: `SEO Growth Plan: Fetching and synthesizing data...`

## Quick Start

```bash
# Step 1: fetch both datasets in parallel
node ./.Codex/skills/gsc-analysis/scripts/gsc-fetch.cjs --site=myimageupscaler.com --output=/tmp/gsc-miu.json &
node ./.Codex/skills/ga-analysis/scripts/ga-fetch.cjs  --site=myimageupscaler.com --output=/tmp/ga-miu.json  &
wait

# Step 2: synthesize
node ./.Codex/skills/seo-growth-plan/scripts/seo-synthesize.cjs \
  --gsc=/tmp/gsc-miu.json \
  --ga=/tmp/ga-miu.json \
  --site=myimageupscaler.com \
  --output=/tmp/seo-plan-miu.json
```

## What Each Script Does

| Script               | Purpose                                                                              |
| -------------------- | ------------------------------------------------------------------------------------ |
| `gsc-fetch.cjs`      | Pulls GSC search analytics: queries, pages, CTR, rankings, cannibalization, indexing |
| `ga-fetch.cjs`       | Pulls GA4 organic sessions, landing page conversions, engagement, device/country     |
| `seo-synthesize.cjs` | Joins both datasets by URL and ranks actions by estimated conversion impact          |

## Configuration

Same service account for both APIs (`$GCP_KEY_FILE` or `~/projects/convertbanktoexcel.com/cloud/keys/coldstart-labs-service-account-key.json`).

The service account needs:

- GSC: **Full user** (or Owner) on the property in Search Console
- GA4: **Viewer** in GA4 Admin → Property Access Management → property `519826120`

## What The Synthesis Produces

### Priority Actions (top 15, ranked by estimated conversions recovered)

Each action includes:

- `type`: `conversion` | `engagement` | `ranking` | `content` | `consolidation` | `technical`
- `priority`: `high` | `medium` | `low`
- `page`: the exact URL to act on
- `topQueries`: GSC queries driving traffic there
- `evidence`: GSC + GA metrics side by side
- `estimatedImpact.conversions`: rough conversions unlocked if fixed
- `suggestedFix`: what to actually do

### Opportunity Clusters

| Cluster                                  | Meaning                                                         |
| ---------------------------------------- | --------------------------------------------------------------- |
| `conversionOpportunities`                | Organic sessions ≥100 + conversion rate < 2%                    |
| `intentMismatch`                         | GSC CTR ≥ 2.5% + GA bounce ≥ 65% (users click but leave)        |
| `strikingDistance.rankingOpportunities`  | Position 8–25 + bounce ≤ 55% (safe to push rankings)            |
| `strikingDistance.fixFirstOpportunities` | Position 8–25 + bounce ≥ 68% (fix page before pushing)          |
| `correlatedDeclines`                     | GA sessions down ≥20% — with correlated GSC signal if available |
| `cannibalization`                        | Multiple GSC pages splitting same query intent                  |
| `trackingGaps.gscGhosts`                 | GSC shows clicks but GA shows zero sessions                     |
| `trackingGaps.gaGhosts`                  | GA shows organic sessions but GSC shows no impressions          |

### Summary Cross-Check

`summary.crosscheck.gscClicksVsGaSessions.ratio` should be between 0.6–1.6. Outside that range indicates a tracking issue worth investigating before trusting the data.

## Output Shape

```json
{
  "meta": { "site": "...", "gscPeriod": {...}, "gaPeriod": {...}, "pagesWithBoth": 0 },
  "summary": {
    "gsc": { "clicks": 0, "impressions": 0, "avgCtr": 0, "avgPosition": 0 },
    "ga":  { "organicSessions": 0, "organicConversions": 0, "organicShare": {...} },
    "crosscheck": { "gscClicksVsGaSessions": { "ratio": 1.0, "looksNormal": true } }
  },
  "priorityActions": [],
  "opportunities": {
    "conversionOpportunities": [],
    "intentMismatch": [],
    "strikingDistance": { "rankingOpportunities": [], "fixFirstOpportunities": [] },
    "correlatedDeclines": [],
    "cannibalization": [],
    "trackingGaps": { "gscGhosts": [], "gaGhosts": [] }
  },
  "joinedPagesTop": []
}
```

## Analysis Workflow

### Step 1: Run All Three Scripts

```bash
node ./.Codex/skills/gsc-analysis/scripts/gsc-fetch.cjs  --site=myimageupscaler.com --days=28 --output=/tmp/gsc-miu.json 2>&1
node ./.Codex/skills/ga-analysis/scripts/ga-fetch.cjs    --site=myimageupscaler.com --days=28 --output=/tmp/ga-miu.json  2>&1
node ./.Codex/skills/seo-growth-plan/scripts/seo-synthesize.cjs \
  --gsc=/tmp/gsc-miu.json --ga=/tmp/ga-miu.json \
  --site=myimageupscaler.com --output=/tmp/seo-plan-miu.json 2>&1
```

### Step 2: Read The Plan JSON

Work through in this order:

1. `summary.crosscheck` — verify tracking is sane before reading anything else
2. `summary.gsc` + `summary.ga` — headline performance and organic share
3. `priorityActions` — top 15 ranked actions; these are the output
4. `opportunities.conversionOpportunities` — biggest revenue lever
5. `opportunities.intentMismatch` — quick CX fixes
6. `opportunities.strikingDistance.rankingOpportunities` — safe SEO work
7. `opportunities.correlatedDeclines` — fire-fighting
8. `opportunities.cannibalization` — consolidation work
9. `opportunities.trackingGaps` — data quality issues to fix first

### Step 3: Produce The Report

See the prompt.md output format.

## Troubleshooting

### Low `pagesWithBoth`

If fewer than 30% of pages have both GSC + GA data, check:

- URL normalization: GSC uses full URLs, GA uses paths. The synthesizer strips protocol+host automatically.
- Locale prefixes: `/en/page` vs `/page` are different keys. Don't collapse them.
- Query strings: synthesizer strips them. If pages differ only by `?utm=X` they'll merge.

### GSC/GA click ratio way off

`ratio < 0.6`: GA is under-counting organic sessions. Check consent mode blocking GA, missing tag on some pages, or redirect chains breaking session attribution.

`ratio > 1.6`: GSC over-counting, or GA is inflating organic sessions. Check if GA4 channel grouping rule for "Organic Search" captures more than just web search.

## Files

| Item             | Path                                                          |
| ---------------- | ------------------------------------------------------------- |
| Skill Doc        | `./.Codex/skills/seo-growth-plan/SKILL.md`                   |
| Prompt           | `./.Codex/skills/seo-growth-plan/prompt.md`                  |
| Synthesis Script | `./.Codex/skills/seo-growth-plan/scripts/seo-synthesize.cjs` |
| GSC Fetch Script | `./.Codex/skills/gsc-analysis/scripts/gsc-fetch.cjs`         |
| GA Fetch Script  | `./.Codex/skills/ga-analysis/scripts/ga-fetch.cjs`           |
