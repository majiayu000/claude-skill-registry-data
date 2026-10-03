---
name: content-gap
description: Find high-impression GSC queries your page content doesn't cover, then get Claude-generated integration recommendations. Builds on /gsc-analysis data. Best for refreshing pages already getting impressions but underperforming on CTR.
user_invocable: true
argument_description: '[page URL or "top"] e.g. https://myimageupscaler.com/blog/some-post, or "top" to analyze top 5 pages'
---

# Content Gap Analysis Skill

You are an SEO content strategist. Your job is to identify the delta between what Google already believes a page is relevant for (GSC impressions) and what the page actually says (content coverage), then recommend precise, natural fixes.

When this skill activates: `Content Gap Mode: Analyzing query-to-content delta...`

## Core Method

1. Pull all GSC queries for a specific page (last 90 days)
2. Fetch live page HTML → extract body text
3. Score each query's coverage: **missing** | **partial** | **underrepresented** | **covered**
4. Rank gaps by `impressions × (1 - coverage_score)` — highest-value unrealized impressions first
5. Generate natural integration suggestions for top gaps

## Quick Start

### Single Page Analysis

```bash
node ./.claude/skills/content-gap/scripts/content-gap.cjs \
  --site=myimageupscaler.com \
  --page=https://myimageupscaler.com/blog/your-post-slug \
  --days=90 \
  --output=/tmp/gap-analysis.json
```

### Top N Pages (Requires Existing GSC Data)

```bash
# First fetch GSC data if you don't have it
node ./.claude/skills/gsc-analysis/scripts/gsc-fetch.cjs --site=myimageupscaler.com --output=/tmp/gsc-miu.json

# Then analyze top 5 pages by impression volume
node ./.claude/skills/content-gap/scripts/content-gap.cjs \
  --site=myimageupscaler.com \
  --top-pages=5 \
  --gsc=/tmp/gsc-miu.json \
  --output=/tmp/gap-top5.json
```

## Configuration

- **Credentials:** same service account as `/gsc-analysis` (`$GCP_KEY_FILE` or `~/projects/convertbanktoexcel.com/cloud/keys/coldstart-labs-service-account-key.json`)
- **Default window:** 90 days (recommended — more signal than 28d for content gaps)
- **Min impressions:** 20 (queries below this are noise for content decisions)

## Script Options

| Flag                 | Default  | Description                                         |
| -------------------- | -------- | --------------------------------------------------- |
| `--site=`            | required | Domain (e.g. `myimageupscaler.com`)                 |
| `--page=`            | —        | Full page URL to analyze                            |
| `--top-pages=N`      | —        | Analyze top N pages by impressions (needs `--gsc`)  |
| `--gsc=`             | —        | Pre-fetched GSC JSON path (speeds up `--top-pages`) |
| `--days=`            | 90       | Date window                                         |
| `--min-impressions=` | 20       | Filter threshold                                    |
| `--search-type=`     | web      | GSC search type                                     |
| `--output=`          | stdout   | Output file path                                    |

## Output Shape

```json
{
  "meta": { "site": "...", "dateRange": {}, "pagesAnalyzed": 1 },
  "page": "https://...",
  "pageContentLength": 4200,
  "pageContentSnippet": "...",
  "analysis": {
    "totalImpressions": 48000,
    "gapScore": 0.62,
    "counts": { "missing": 45, "partial": 22, "underrepresented": 31, "covered": 90 },
    "priorityCounts": { "critical": 3, "high": 12, "medium": 28, "low": 55 },
    "totalPotentialClicks": 380,
    "gaps": [
      {
        "query": "free ai image upscaler",
        "impressions": 5200,
        "clicks": 118,
        "ctr": 0.023,
        "position": 6.2,
        "gapType": "missing",
        "score": 0,
        "priority": "critical",
        "potentialClicks": 95,
        "tokenResults": [
          { "token": "free", "count": 0, "found": false },
          { "token": "image", "count": 8, "found": true },
          { "token": "upscaler", "count": 3, "found": true }
        ]
      }
    ]
  }
}
```

### Gap Types

| Type               | Meaning                                           |
| ------------------ | ------------------------------------------------- |
| `missing`          | No meaningful query tokens found in page text     |
| `partial`          | <50% of query tokens found                        |
| `underrepresented` | All tokens found but full phrase absent or sparse |
| `covered`          | Query phrase and tokens well represented          |

### Priority Levels

| Priority   | Threshold                             |
| ---------- | ------------------------------------- |
| `critical` | ≥500 impressions + missing            |
| `high`     | ≥200 impressions + missing or partial |
| `medium`   | ≥50 impressions + any gap type        |
| `low`      | <50 impressions                       |

## Analysis Workflow

### Step 1: Run the Script

```bash
node ./.claude/skills/content-gap/scripts/content-gap.cjs \
  --site=myimageupscaler.com \
  --page=PAGE_URL \
  --days=90 \
  --output=/tmp/gap.json 2>&1
```

### Step 2: Read the Output

Focus on:

1. `analysis.gapScore` — fraction of total impressions currently in gap queries (e.g. 0.62 = 62% of impressions are underserved)
2. `analysis.totalPotentialClicks` — estimated click uplift from closing all gaps
3. `analysis.gaps` filtered by `priority: "critical"` and `priority: "high"` — start here
4. `tokenResults` per gap — reveals exactly which words are missing vs. present
5. `pageContentSnippet` — sanity-check the page structure to understand tone and format

### Step 3: Generate Recommendations

Use `prompt.md` as the LLM analysis prompt. Feed it:

- The top 20-30 gap queries (critical + high priority)
- The `pageContentSnippet`
- The `analysis.counts` summary

The prompt produces per-gap integration suggestions: where (heading, paragraph, FAQ, alt text) and how (exact phrasing options).

### Step 4: Output Report

Present findings as markdown:

```markdown
# Content Gap Report: [Page URL]

**Period:** [start] → [end] ([N] days)
**Gap Score:** [X]% of impressions underserved
**Potential Click Uplift:** ~[N] clicks/period

## Critical Gaps (immediate fixes)

[table: query | impressions | position | gap type | suggested fix]

## High Priority Gaps

[table]

## Integration Recommendations

[per-gap: where to add, exact phrasing, rationale]

## Prioritized Actions

1. ...
```

## Integration With Other Skills

- **Before running**: `/gsc-analysis` gives site-wide picture; use `topPages` output to pick which URLs matter most
- **After running**: Use `/blog-edit` to apply changes to blog posts, or edit page files directly
- **Tracking lift**: Re-run after 4–6 weeks with the same `--page` flag to see gap score change; or use `/gsc-analysis` CTR tracker

## What Makes a Good Gap to Fix

Fix gaps where:

- `priority: "critical"` or `"high"` — high impressions signal Google already associates the query with your page
- `position <= 10` — you're already ranking; content alignment tips you into more clicks
- `gapType: "missing"` with long-tail modifiers (e.g. "free", "without watermark", "for print") — one sentence closes the gap
- The page has good engagement (pair with `/ga-analysis` bounce rate data)

Skip gaps where:

- `position > 30` — ranking problem, not content problem
- The query implies a different intent than the page serves (e.g. transactional query on an informational page)
- Impressions < 50 with no clear intent signal

## Constraints

- GSC lags 2–3 days; `--lag-days=3` is the default
- API returns up to 25k rows per page; pages with >25k query rows will be paginated automatically
- Page fetch uses a simple HTML stripper — JavaScript-rendered content won't be analyzed. If the page relies heavily on client-side rendering, the gap score will be artificially high
- Always prioritize natural integration over stuffing — the goal is to match searcher intent, not mechanically insert keywords

## Files

| Item            | Path                                                   |
| --------------- | ------------------------------------------------------ |
| Skill Doc       | `./.claude/skills/content-gap/SKILL.md`                |
| Analysis Prompt | `./.claude/skills/content-gap/prompt.md`               |
| Gap Script      | `./.claude/skills/content-gap/scripts/content-gap.cjs` |
| GSC Fetcher     | `./.claude/skills/gsc-analysis/scripts/gsc-fetch.cjs`  |
