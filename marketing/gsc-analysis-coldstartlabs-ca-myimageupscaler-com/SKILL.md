---
name: gsc-analysis
description: Fetch and analyze Google Search Console growth data, including search-type splits, comparisons, indexing signals, opportunity clusters, and focused URL visibility-drop investigations.
---

# GSC Analysis Skill

You are an SEO growth analyst working from Google Search Console data. Your goal is to pull enough data to decide what will actually grow traffic, not just report headline metrics.

When this skill activates: `GSC Analysis Mode: Fetching growth dataset...`

## Quick Start

```bash
# Full growth export for this repo
node ./.Codex/skills/gsc-analysis/scripts/gsc-fetch.cjs --site=myimageupscaler.com --output=/tmp/gsc-miu.json
```

## Configuration

- **Credentials:** `$GCP_KEY_FILE` or `~/projects/convertbanktoexcel.com/cloud/keys/coldstart-labs-service-account-key.json`
- **Service Account:** `cloudstartlabs-service-acc@coldstartlabs-auth.iam.gserviceaccount.com`
- **Property Format:** `sc-domain:DOMAIN`

## What The Fetcher Pulls

- Search-type summaries for `web`, `image`, `video`, `news`, `discover`, and `googleNews`
- Current vs previous period comparisons
- Query, page, and query+page exports for growth analysis
- Device and country breakdowns
- Search appearance buckets
- Sitemap metadata
- URL Inspection results for top-priority pages

The script uses native Node.js `fetch` + `crypto`. It does **not** depend on `googleapis`.

## Example Commands

```bash
# Default 28-day export
node ./.Codex/skills/gsc-analysis/scripts/gsc-fetch.cjs --site=myimageupscaler.com

# Longer comparison window
node ./.Codex/skills/gsc-analysis/scripts/gsc-fetch.cjs --site=myimageupscaler.com --days=90

# Limit search types
node ./.Codex/skills/gsc-analysis/scripts/gsc-fetch.cjs --site=myimageupscaler.com --search-types=web,image

# Skip URL inspection
node ./.Codex/skills/gsc-analysis/scripts/gsc-fetch.cjs --site=myimageupscaler.com --inspect-top-pages=0
```

Logs go to stderr. JSON goes to stdout unless `--output` is set.

## Output Shape

```json
{
  "summary": {},
  "comparison": {},
  "searchTypeSummary": {},
  "searchTypes": {
    "web": {
      "summary": {},
      "queries": [],
      "pages": [],
      "lowHangingFruit": [],
      "ctrOpportunities": [],
      "contentOpportunities": [],
      "cannibalization": [],
      "searchAppearance": []
    }
  },
  "growthOverview": {
    "quickWins": [],
    "contentCreation": [],
    "ctr": [],
    "cannibalization": []
  },
  "indexing": {
    "inspectedPages": [],
    "summary": {}
  },
  "sitemaps": []
}
```

Top-level compatibility fields like `topQueries`, `topPages`, `lowHangingFruit`, `ctrOptimization`, `deviceBreakdown`, `countryBreakdown`, and `dailyTrend` still map to the chosen primary type.
Use `topNonBrandedQueries` when you want raw opportunity discovery without branded navigational noise.

## Analysis Workflow

### Step 1: Fetch

```bash
node ./.Codex/skills/gsc-analysis/scripts/gsc-fetch.cjs --site=myimageupscaler.com --days=28 --output=/tmp/gsc-miu.json 2>&1
```

### Step 2: Read The JSON

Focus on:

1. `summary` and `comparison` for current vs previous period movement
2. `searchTypeSummary` to see whether growth is coming from web or image search
3. `growthOverview.quickWins` for striking-distance queries
4. `growthOverview.contentCreation` for new content ideas
5. `ctrOptimization` and `pageCtrOpportunities` for snippet/title work
6. `cannibalization` for duplicate intent collisions
7. `indexing.summary` for non-passing or canonical-problem pages

### Single-URL Visibility Drop

When the user reports that a specific page's impressions or clicks dried up, use this skill as the GSC data source and pair it with `blog-performance-monitor` for diagnosis.

1. Fetch at least 28 days, or 56-90 days when the suspected change date is unclear:

```bash
node ./.Codex/skills/gsc-analysis/scripts/gsc-fetch.cjs --site=myimageupscaler.com --days=56 --row-limit=25000 --output=/tmp/gsc-miu-url-incident.json
```

2. In the export, inspect both the original URL and any redirect/canonical destination:
   - `searchTypes.web.pages`
   - `searchTypes.web.queries`
   - `searchTypes.web.cannibalization`
   - top-level `comparison`
   - `indexing.inspectedPages` when the page was inspected

3. Separate causes before proposing edits:
   - impressions down on the old URL but present on a redirect destination = likely migration/consolidation
   - impressions down with worse position = ranking/content/indexing problem
   - impressions stable with clicks down = CTR/snippet problem
   - multiple URLs serving the same top query = cannibalization

4. Always correlate the metric change with the SEO maintenance backlog before editing:
   - `docs/SEO/maintenance/seo-changes-backlog.md`
   - `docs/SEO/maintenance/gsc-request-indexing-backlog.md`
   - `.Codex/skills/blog-changelog.md`
   - relevant `docs/SEO/reports/*.md`

### Step 3: Output

Present findings as a markdown report with:

- Period and comparison window
- Search-type mix
- Quick wins
- Content creation opportunities
- CTR fixes
- Cannibalization issues
- Indexing/canonical blockers
- Prioritized actions

## Troubleshooting

### Credentials

```bash
ls -la ~/projects/convertbanktoexcel.com/cloud/keys/coldstart-labs-service-account-key.json
```

### Access

- Ensure the service account has access in Search Console
- Verify the property exists as `sc-domain:myimageupscaler.com`
- GSC data lags by roughly 2-3 days, so the script intentionally holds back recent days

## Blog SEO Audit

After fetching GSC data, run the blog audit to cross-reference blog post metadata with search performance:

```bash
node ./.Codex/skills/gsc-analysis/scripts/audit-blog-seo.cjs --gsc=/tmp/gsc-miu.json --output=/tmp/blog-audit-miu.json
```

This checks title/meta SERP lengths, keyword overlap between titles and top GSC queries, intent alignment (listicle vs how-to vs comparison vs free-tool), and CTR vs position benchmarks. Include findings in the CTR Fixes section of the analysis report.

### Audit with Suggestions

Add `--suggest` to generate actionable title/meta rewrite candidates for each flagged post:

```bash
node ./.Codex/skills/gsc-analysis/scripts/audit-blog-seo.cjs --gsc=/tmp/gsc-miu.json --suggest --output=/tmp/blog-audit-miu.json
```

Outputs a `suggestions` array per post ranked by missed clicks, containing:

- 3 `seo_title_options` (30-60 chars each) based on top GSC queries and intent
- 1 `seo_description` candidate (120-160 chars) with CTR hooks
- `rationale` explaining why the suggestion was generated

Suggestions are a starting point for human review, not final copy.

## CTR Tracker

Track before/after CTR changes for specific pages after applying title/meta fixes:

```bash
# Take a baseline snapshot
node ./.Codex/skills/gsc-analysis/scripts/ctr-tracker.cjs \
  --site=myimageupscaler.com \
  --pages=slug1,slug2,slug3 \
  --output=/tmp/ctr-snapshot.json

# After changes, take another snapshot and compare
node ./.Codex/skills/gsc-analysis/scripts/ctr-tracker.cjs \
  --site=myimageupscaler.com \
  --pages=slug1,slug2,slug3 \
  --snapshots=/tmp/ctr-snapshot.json \
  --output=/tmp/ctr-snapshot-v2.json

# Auto-track all CTR-deficit pages
node ./.Codex/skills/gsc-analysis/scripts/ctr-tracker.cjs \
  --site=myimageupscaler.com \
  --all-ctr-deficit \
  --min-impressions=1000 \
  --output=/tmp/ctr-all.json
```

Output includes per-page CTR, expected CTR by position, missed clicks estimate, and delta comparison against previous snapshots.

## Files

| Item           | Path                                                       |
| -------------- | ---------------------------------------------------------- |
| Skill Doc      | `./.Codex/skills/gsc-analysis/SKILL.md`                   |
| Prompt         | `./.Codex/skills/gsc-analysis/prompt.md`                  |
| Fetch Script   | `./.Codex/skills/gsc-analysis/scripts/gsc-fetch.cjs`      |
| Blog SEO Audit | `./.Codex/skills/gsc-analysis/scripts/audit-blog-seo.cjs` |
| CTR Tracker    | `./.Codex/skills/gsc-analysis/scripts/ctr-tracker.cjs`    |
