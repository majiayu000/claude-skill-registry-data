---
name: seo-manager
description: Orchestrate all SEO audit skills in parallel waves and produce a unified health report. Use when asked for "full SEO audit", "SEO health check", "comprehensive SEO report", "SEO manager", "run all SEO checks", or "SEO status".
user_invocable: true
argument_description: "[--competitor=<domain>] [--url=<url>] [--skip=<skill1,skill2>] [--include-strategy] [--days=<28|90>]"
---

# SEO Manager Orchestrator

You are the **SEO Manager** for myimageupscaler.com. Your job: orchestrate all SEO audit skills in parallel waves, collect results, and produce a unified health report grounded in real GSC + GA4 data.

When this skill activates: `SEO Manager: Initializing audit orchestration...`

---

## Principles

1. **GSC + GA4 are ground truth** - All recommendations must reference real search + behavioral data. If GSC fetch fails, STOP.
2. **Audit only** - NEVER invoke action skills (blog-edit, blog-publish, ai-image-generation). Report findings, don't fix them.
3. **Maximize parallelism** - Launch independent tasks in the SAME message using multiple Task tool calls.
4. **Each skill = unique angle** - No redundant re-checks across skills.
5. **Graceful degradation** - If a non-GSC skill fails, mark as "N/A" and continue. Only GSC failure is a hard stop. GA4 failure = warn but continue.

---

## Input / Arguments

Parse optional arguments from user input:

| Argument                | Default                       | Description                                                           |
| ----------------------- | ----------------------------- | --------------------------------------------------------------------- |
| `--competitor=<domain>` | _(not run)_                   | Enable competitor sitemap analysis for this domain                    |
| `--url=<url>`           | `https://myimageupscaler.com` | URL for PageSpeed and SquirrelScan audits                             |
| `--skip=<skills>`       | _(none)_                      | Comma-separated skills to skip (e.g., `blog-audit,backlink-analyzer`) |
| `--include-strategy`    | _(not run)_                   | Include keyword research & content strategy analysis                  |
| `--days=<N>`            | `28`                          | Analysis window in days (28 or 90)                                    |

---

## Execution Pipeline

### Step 1: Initialize

1. Parse arguments
2. Check for prior reports: `ls docs/SEO/reports/seo-report-*.md` - read the most recent one for trend comparison
3. Create the output directory if needed: `mkdir -p docs/SEO/reports`
4. Display the execution plan to the user:

```
SEO Manager: Audit Plan
========================
Target: <url>
Competitor: <domain or "skipped">
Skipping: <skills or "none">
Strategy: <"included" if --include-strategy, otherwise "skipped">
Days window: <days>

Wave 1 (Data Collection):  GSC fetch, GA4 fetch, PageSpeed, SquirrelScan
Wave 1.5 (Synthesis):      GSC + GA4 join via seo-synthesize.cjs
Wave 2 (Analysis):         SEO review, Blog audit, Schema, AI Search, Internal Linking, Backlinks [, Competitor] [, Keyword Strategy]
Wave 3 (Synthesis):        Score, merge, write report

Estimated time: 12-25 minutes (add +5min if --include-strategy)
```

5. Use TaskCreate to create tracking tasks for each wave.

---

### Step 2: Wave 1 - Data Collection

Launch **4 parallel Task tool calls in a single message** (skip any in `--skip` list):

#### Task 1: GSC Data Fetch

```
subagent_type: general-purpose
prompt: |
  Fetch Google Search Console data for myimageupscaler.com.

  Run this command:
  node ./.claude/skills/gsc-analysis/scripts/gsc-fetch.cjs --site=myimageupscaler.com --days=<DAYS> --output=/tmp/gsc-miu.json 2>&1

  Then read /tmp/gsc-miu.json.

  Return a structured summary with EXACTLY these sections:
  - Indexing: submitted count, indexed count, index rate percentage
  - Performance (period): total clicks, total impressions, avg CTR, avg position vs previous period
  - Search type mix: web vs image vs discover (if available)
  - Top 20 queries: query, position, impressions, clicks, CTR (as a table)
  - Low-hanging fruit: keywords with position 4-20 and impressions > 10 (from growthOverview.quickWins)
  - Content gaps: new content opportunities from growthOverview.contentCreation
  - CTR opportunities: pages/queries from growthOverview.ctr
  - Top 10 pages by clicks
  - Device breakdown
  - Country breakdown (top 5)
  - Cannibalization alerts (if any from growthOverview.cannibalization)

  If the script fails, report the exact error message.
```

#### Task 2: GA4 Data Fetch

```
subagent_type: general-purpose
prompt: |
  Fetch Google Analytics 4 organic data for myimageupscaler.com.

  Run this command:
  node ./.claude/skills/ga-analysis/scripts/ga-fetch.cjs --site=myimageupscaler.com --days=<DAYS> --output=/tmp/ga-miu.json 2>&1

  Then read /tmp/ga-miu.json.

  Return a structured summary with EXACTLY these sections:
  - Organic vs total summary: sessions, conversions, organic share %, period deltas
  - Channel mix: top channels by session share (flag any shift ≥10 pts)
  - Top 15 organic landing pages: page, sessions, conversions, conversion rate, engagement rate
  - Conversion opportunities (from opportunities.highTrafficLowConversion): page, sessions, conversion rate
  - Engagement issues (from opportunities.highTrafficLowEngagement): page, sessions, bounce rate
  - Declining pages (from opportunities.decliningLandingPages): page, session delta %
  - Device gaps (from opportunities.underperformingDevices)
  - Country split (top 5 organic countries)
  - GSC/GA cross-check ratio (from summary.crosscheck.gscClicksVsGaSessions.ratio) - flag if outside 0.6–1.6

  If the script fails with an auth error, report: "GA4 FAILED - <error>. Continuing without GA4 data."
  If it fails with a permissions error, note the service account needs Viewer access in GA4 Admin → Property Access Management for property 519826120.
```

#### Task 3: PageSpeed Audit

```
subagent_type: general-purpose
prompt: |
  Run a Lighthouse PageSpeed audit on <URL>.

  Invoke the /pagespeed skill with URL: <URL>

  Return a structured summary with:
  - Scores table: Performance, SEO, Accessibility, Best Practices (mobile + desktop)
  - Lab data: FCP, LCP, TBT, CLS, Speed Index, TTI, TTFB (mobile + desktop)
  - Top 5 performance opportunities with estimated savings
  - Any SEO-specific failures
  - Any accessibility failures

  Save the full report to docs/SEO/audits/pagespeed-report-YYYY-MM-DD.md
```

#### Task 4: SquirrelScan Audit

```
subagent_type: general-purpose
prompt: |
  Run a SquirrelScan website audit on <URL>.

  Execute:
  squirrel audit <URL> --format llm -C surface

  Return a structured summary with:
  - Overall health score (0-100)
  - Issues by severity: critical count, high count, medium count, low count
  - Top issues by category (SEO, technical, content, security, schema, links)
  - Broken links found (if any)
  - Schema markup findings

  If squirrel is not installed, report this and skip.
```

---

### Step 3: Wave 1 Checkpoint + Synthesis

After all Wave 1 tasks return:

1. **Check GSC result** - If GSC failed, STOP and display the error. Help the user troubleshoot:
   - Check credentials: `ls -la ~/projects/convertbanktoexcel.com/cloud/keys/coldstart-labs-service-account-key.json`
   - Check script: `node ./.claude/skills/gsc-analysis/scripts/gsc-fetch.cjs --help`
   - Do NOT proceed without GSC data.

2. **Check GA4 result** - If GA4 failed, mark as "N/A" and continue. Note in report that behavioral data is unavailable.

3. **Run the GSC+GA4 synthesis** (if GA4 succeeded):

```bash
node ./.claude/skills/seo-growth-plan/scripts/seo-synthesize.cjs \
  --gsc=/tmp/gsc-miu.json \
  --ga=/tmp/ga-miu.json \
  --site=myimageupscaler.com \
  --output=/tmp/seo-plan-miu.json 2>&1
```

Read `/tmp/seo-plan-miu.json`. Extract:
- `SEO_SYNTHESIS.crosscheck`: GSC/GA4 click-to-session ratio (flag if abnormal)
- `SEO_SYNTHESIS.priorityActions`: top 15 ranked actions with estimated conversion impact
- `SEO_SYNTHESIS.conversionOpportunities`: high-traffic, low-converting pages
- `SEO_SYNTHESIS.intentMismatch`: pages where users click but leave immediately
- `SEO_SYNTHESIS.strikingDistance`: safe-to-push vs fix-first ranking opportunities
- `SEO_SYNTHESIS.cannibalization`: pages splitting the same query intent

4. **Parse key contexts to inject into Wave 2**:
   - `GSC_SUMMARY`: indexing + performance summary (5-8 lines)
   - `GSC_TOP_QUERIES`: top 20 queries table
   - `GSC_LOW_HANGING_FRUIT`: low-hanging fruit + quick wins
   - `GSC_TOP_PAGES`: top 10 pages by clicks
   - `GA4_SUMMARY`: organic summary, channel mix, top landing pages
   - `GA4_OPPORTUNITIES`: conversion opps, engagement issues, declining pages
   - `SYNTHESIS_ACTIONS`: top 10 priority actions from seo-synthesize.cjs (or "N/A - GA4 unavailable")

5. **Note PageSpeed/SquirrelScan status** - If either failed, mark as "N/A" but continue.

6. Update task statuses.

---

### Step 4: Wave 2 - Domain Analysis

Launch **5-7 parallel Task tool calls in a single message** (skip any in `--skip` list).

Every Wave 2 prompt MUST include the full data context block:

```
## Data Ground Truth (use this to ground your analysis)

### GSC Data
<paste GSC_SUMMARY>
<paste GSC_TOP_QUERIES>
<paste GSC_LOW_HANGING_FRUIT>
<paste GSC_TOP_PAGES>

### GA4 Behavioral Data
<paste GA4_SUMMARY>
<paste GA4_OPPORTUNITIES>

### Priority Actions (GSC+GA4 Synthesis)
<paste SYNTHESIS_ACTIONS or "GA4 unavailable - use GSC only">
```

#### Task A: SEO Expert Review

```
subagent_type: seo-auditor
prompt: |
  You are an SEO expert reviewing myimageupscaler.com (AI-powered image upscaler SaaS).

  <Data context block>

  Your job: Review on-page SEO and content quality for the TOP 10 PAGES from GSC data.
  Focus ONLY on what SquirrelScan does NOT cover:
  - Content depth and search intent match
  - E-E-A-T signals (expertise, experience, authority, trust)
  - Keyword targeting effectiveness (are titles/H1s aligned with GSC queries?)
  - Content gaps (GSC shows impressions but poor CTR - why?)
  - GA4 behavioral confirmation: pages with high bounce per GA4 data are likely intent mismatches
  - User experience signals

  For each page reviewed, reference its GSC metrics (position, impressions, CTR) AND GA4 behavioral data if available (bounce rate, conversion rate).

  Return a structured summary:
  - Pages reviewed (count)
  - Key on-page findings (table: page, issue, severity, GSC context, GA4 context)
  - E-E-A-T assessment (1 paragraph)
  - Content gap opportunities (list with GSC data citations)
  - Intent mismatch candidates confirmed by both GSC low CTR AND GA4 high bounce
  - Score: 0-100 for on-page SEO quality
```

#### Task B: Blog Audit

```
subagent_type: general-purpose
prompt: |
  Audit all published blog posts on myimageupscaler.com for quality and SEO compliance.
  This is REPORT-ONLY mode - do NOT fix anything, do NOT invoke blog-edit.

  <Data context block>

  Step 1: Authenticate
  PASSWORD=$(gcloud secrets versions access latest --secret=myimageupscaler-blog-admin-password --project=coldstartlabs-auth 2>/dev/null || echo "MISSING")
  If PASSWORD is MISSING, try reading from .env.api file.
  TOKEN=$(curl -s -X POST "https://api.myimageupscaler.com/auth/login" \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"motherai@opus.com\",\"password\":\"$PASSWORD\"}" \
    | jq -r '.session.access_token // empty')

  Step 2: Fetch all posts
  ALL_POSTS=$(curl -s "https://myimageupscaler.com/api/blog/admin/posts?limit=200" \
    -H "Authorization: Bearer $TOKEN")

  Step 3: For each post, check:
  - Thin content (< 300 words = CRITICAL)
  - Title length (30-60 chars required)
  - Excerpt length (100-160 chars required)
  - H1 count (exactly 1 required)
  - CTA presence (must have hyperlinked CTAs to https://myimageupscaler.com)
  - AI vocabulary (delve, tapestry, nuanced, multifaceted, pivotal, landscape, testament, myriad)
  - Keyword cannibalization across posts

  Step 4: Cross-reference with GSC low-hanging fruit AND GA4 data:
  - Are blog posts targeting the GSC quick-win keywords?
  - Do high-traffic blog posts have low conversion rates in GA4?

  Return a structured summary:
  - Total posts audited
  - Issues by severity: critical, high, medium, low (counts)
  - Top 10 worst posts (table: slug, word count, issues found, severity)
  - Cannibalization pairs (if any)
  - AI writing detection results
  - Blog posts targeting GSC low-hanging fruit keywords (or gaps)
  - Blog posts with high traffic but low GA4 conversion rate (if data available)
  - Score: 0-100 for blog health

  If authentication fails, report the error and return score as "N/A".
```

#### Task C: Schema Markup Review

```
subagent_type: general-purpose
prompt: |
  Review structured data / schema markup on myimageupscaler.com.

  <Data context block>

  <SquirrelScan schema findings if available>

  Check the following pages for JSON-LD schema:
  1. Homepage (https://myimageupscaler.com) - expect: Organization, SoftwareApplication, WebSite
  2. Pricing page (/pricing) - expect: Product or Offer
  3. Blog posts (check 3 posts) - expect: Article, BreadcrumbList
  4. pSEO pages from top GSC pages (check 2) - expect: FAQPage, BreadcrumbList, SoftwareApplication
  5. Use-case pages (check 2) - expect: HowTo or FAQPage

  For each page, use WebFetch to check the HTML source for JSON-LD scripts.

  Return a structured summary:
  - Pages checked (count)
  - Schema types found (table: page, schemas present, schemas missing)
  - Validation issues (malformed JSON-LD, missing required fields)
  - Rich result eligibility (which pages qualify for which rich results)
  - Priority additions (which schemas would have highest impact)
  - Score: 0-100 for structured data coverage
```

#### Task D: AI Search Optimization Review

```
subagent_type: general-purpose
prompt: |
  Review myimageupscaler.com for AI search engine visibility (AEO/GEO).

  <Data context block>

  Check the following:

  1. robots.txt AI bot access - fetch https://myimageupscaler.com/robots.txt
     - Is GPTBot blocked or allowed?
     - Is ClaudeBot blocked or allowed?
     - Is PerplexityBot blocked or allowed?
     - Is Google-Extended blocked or allowed?

  2. llms.txt presence - check https://myimageupscaler.com/llms.txt and /llms-full.txt
     - Does it exist?
     - Is it well-structured?

  3. Content citability - check 3 key pages from GSC top queries:
     - Does content use inverted pyramid (answer first)?
     - Are there clear definitions/explanations AI can extract?
     - Is content structured with semantic HTML (lists, tables, headings)?
     - Are there FAQ sections?

  4. E-E-A-T signals for AI
     - Author credentials visible?
     - Dates and freshness signals?
     - Authoritative sources cited?

  Return a structured summary:
  - AI bot access status (table: bot, status)
  - llms.txt status
  - Content citability score per page checked
  - AEO readiness checklist (items checked vs passed)
  - Priority recommendations
  - Score: 0-100 for AI search readiness
```

#### Task E: Internal Linking Analysis

```
subagent_type: general-purpose
prompt: |
  Analyze internal linking structure of myimageupscaler.com.

  <Data context block>

  Step 1: Fetch the sitemap
  Use WebFetch to get https://myimageupscaler.com/sitemap.xml
  Parse the URL list.

  Step 2: Categorize pages by type:
  - Homepage, Tool/App pages, pSEO category pages, Blog posts, Static pages

  Step 3: Check 5 high-value pages from GSC top pages (prioritize pages with high impressions or GA4 conversion opportunities):
  - How many internal links point TO this page? (check from homepage, nav, footer, blog posts)
  - How many internal links does this page have going OUT?
  - Is the anchor text descriptive and keyword-relevant?

  Step 4: Check for orphan pages:
  - Are there sitemap URLs that might have zero or minimal internal links?

  Step 5: Topic cluster assessment:
  - Do pSEO pages link to related pages and vice versa?
  - Do blog posts link to relevant tool/pSEO pages?
  - Is there a hub-and-spoke linking pattern?

  For GA4 conversion opportunity pages specifically: do they have enough internal links to maximize PageRank and authority?

  Return a structured summary:
  - Total pages in sitemap
  - Pages checked in detail (count)
  - Internal link distribution (table: page, inbound links, outbound links)
  - Orphan page candidates
  - Topic cluster gaps
  - Anchor text quality assessment
  - Priority linking opportunities (with GSC data: "Link to /upscale-image from blog - it has 450 impressions at position 12" and GA4 data where available)
  - Score: 0-100 for internal linking health
```

#### Task F: Backlink Analysis

```
subagent_type: general-purpose
prompt: |
  Analyze the backlink profile of myimageupscaler.com.

  <Data context block>

  Since we may not have Ahrefs/Semrush API access, use available data:

  1. Check if docs/SEO/ contains any Ahrefs or backlink export files (CSV/JSON)
  2. Use WebFetch to check common backlink checker tools if available
  3. Reference any domain authority metrics from prior reports in docs/SEO/audits/

  Based on available data, assess:
  - Total known backlinks and referring domains
  - Domain authority / Domain Rating
  - Link quality distribution (editorial vs directory vs social vs spam)
  - Anchor text distribution
  - Top referring domains

  Cross-reference with GSC + GA4 synthesis data:
  - Pages in the GA4 conversion opportunities list need backlink authority to convert better
  - Pages with GSC position 4-20 are candidates for link-building to push into top 3

  Return a structured summary:
  - Profile overview (backlinks, referring domains, DR/DA)
  - Link quality assessment
  - Competitor link gap (if prior competitor reports exist in docs/SEO/)
  - High-priority pages needing backlinks (from GSC low-hanging fruit + GA4 conversion opps)
  - Link building opportunity types
  - Score: 0-100 for backlink profile health (or "N/A - Limited data" if no backlink data found)
```

#### Task G: Competitor Sitemap Spy (ONLY if --competitor provided)

```
subagent_type: seo-competitor-analyzer
prompt: |
  Analyze competitor <COMPETITOR_DOMAIN> SEO strategy via their sitemap.

  <Data context block>

  Invoke the /competitor-sitemap-spy skill for domain: <COMPETITOR_DOMAIN>

  Return a structured summary:
  - Total pages found
  - Page categories (table: category, count, percentage)
  - pSEO patterns identified
  - Content gaps (they have, we don't)
  - Our advantages (we have, they don't)
  - Top 5 quick-win opportunities
  - Score: 0-100 for competitive position
```

#### Task H: Keyword Research & Strategy (ONLY if --include-strategy provided)

```
subagent_type: general-purpose
prompt: |
  Generate a keyword research strategy and content roadmap for myimageupscaler.com.

  <Data context block>

  Invoke the /keyword-research-strategy skill with focus on easy wins:
  /keyword-research-strategy --focus=easy-wins --competition=low --limit=15

  The skill will:
  1. Analyze GSC data + Ahrefs snapshots (if available)
  2. Classify search intent for all keywords
  3. Map keywords to existing/proposed pages
  4. Identify content gaps and intent mismatches
  5. Generate prioritized content roadmap

  Augment the strategy with GA4 insights:
  - Which existing pages convert well? → Target similar keywords
  - Which pages have high traffic but low conversion? → Content strategy fix, not just SEO

  Return a structured summary with EXACTLY these sections:
  - Total keywords analyzed
  - Opportunity breakdown by segment:
    - Quick Wins (position 4-20, easy push)
    - Content Gaps (high potential, no page)
    - Long-Tail Clusters (group related keywords)
    - Intent Mismatches (wrong page ranks)
  - Top 5 immediate priorities (keyword, segment, impact, effort)
  - Total potential monthly clicks if roadmap implemented
  - Link to full roadmap file in docs/SEO/keyword-strategy-roadmap-YYYY-MM-DD.md

  Cross-reference with GSC low-hanging fruit to ensure alignment.

  If the skill fails or no Ahrefs data found, note limitation but include GSC-only analysis.
```

---

### Step 5: Wave 2 Checkpoint

After all Wave 2 tasks return:

1. Collect all structured summaries
2. Note which skills succeeded and which returned "N/A"
3. Update task statuses

---

### Step 6: Wave 3 - Synthesis

This runs in the main thread (no subagents).

#### 6a: Compute Health Scores

Extract the score from each skill's summary. Calculate weighted overall score:

| Dimension                | Weight | Source                                                                                    |
| ------------------------ | ------ | ----------------------------------------------------------------------------------------- |
| Technical SEO            | 15%    | SquirrelScan health score                                                                 |
| Core Web Vitals          | 15%    | PageSpeed performance score (mobile 60% + desktop 40%)                                    |
| On-Page SEO              | 15%    | SEO expert review score                                                                   |
| Content / Blog           | 10%    | Blog audit score                                                                          |
| Schema / Structured Data | 5%     | Schema markup review score                                                                |
| Internal Linking         | 10%    | Internal linking analysis score                                                           |
| Backlinks                | 5%     | Backlink analysis score                                                                   |
| AI Search Readiness      | 5%     | AI search optimization score                                                              |
| GSC Performance          | 10%    | Composite: (index_rate × 0.3) + (normalized_position × 0.4) + (normalized_ctr × 0.3)    |
| GA4 Behavioral           | 10%    | Composite: (organic_share × 0.3) + (conversion_rate_norm × 0.4) + (engagement_norm × 0.3) |

For N/A dimensions: redistribute their weight proportionally across available dimensions.

Position normalization: `score = max(0, 100 - (avg_position - 1) * 1.5)`
CTR normalization: `score = min(100, avg_ctr * 1000)`
Conversion rate normalization: `score = min(100, organic_cr_pct * 20)` (5% CR = 100)
Engagement normalization: `score = min(100, engagement_rate_pct)` (already 0–100)

#### 6b: Trend Comparison

If a prior report exists in `docs/SEO/reports/`:

- Compare overall score: up/down/stable
- Compare each dimension score
- Note significant changes (> 5 point swing)

Use arrows: `[+5]` for improvement, `[-3]` for decline, `[=]` for stable

#### 6c: Assemble Report

Write the unified report to `docs/SEO/reports/seo-report-YYYY-MM-DD.md` using this template:

```markdown
# SEO Health Report - myimageupscaler.com

**Date:** YYYY-MM-DD
**Auditor:** SEO Manager Orchestrator
**URL:** <url>
**Period:** Last <days> days
**Skills Used:** <list of skills that ran successfully>
**Skills Skipped/Failed:** <list with reasons>
**Duration:** ~XX minutes

---

## Executive Summary

### Overall SEO Health Score: XX/100 [trend]

| Dimension           | Score  | Weight | Trend   | Key Finding |
| ------------------- | ------ | ------ | ------- | ----------- |
| Technical SEO       | XX/100 | 15%    | [trend] | ...         |
| Core Web Vitals     | XX/100 | 15%    | [trend] | ...         |
| On-Page SEO         | XX/100 | 15%    | [trend] | ...         |
| Content / Blog      | XX/100 | 10%    | [trend] | ...         |
| Schema              | XX/100 | 5%     | [trend] | ...         |
| Internal Linking    | XX/100 | 10%    | [trend] | ...         |
| Backlinks           | XX/100 | 5%     | [trend] | ...         |
| AI Search Readiness | XX/100 | 5%     | [trend] | ...         |
| GSC Performance     | XX/100 | 10%    | [trend] | ...         |
| GA4 Behavioral      | XX/100 | 10%    | [trend] | ...         |

### Top 5 Priority Issues

1. **[CRITICAL]** ... (GSC: ..., GA4: ...)
2. **[HIGH]** ... (GSC: ..., GA4: ...)
3. ...
4. ...
5. ...

### Quick Wins (Impact vs Effort — from GSC+GA4 synthesis)

1. ... (GSC: keyword X at position Y with Z impressions | GA4: N% conversion rate)
2. ...
3. ...

---

## 1. Google Search Console Performance

[Paste GSC summary from Wave 1]

---

## 2. Google Analytics 4 Behavioral Data

[Paste GA4 summary from Wave 1, or "N/A - GA4 fetch failed (see error above)"]

### GSC + GA4 Synthesis — Priority Actions

[Paste top 10 actions from seo-synthesize.cjs output, or "N/A"]

### Tracking Health

GSC/GA4 click-to-session ratio: <ratio> (<"Normal" if 0.6–1.6, otherwise flag as ABNORMAL>)

---

## 3. Core Web Vitals & Performance

[Paste PageSpeed summary from Wave 1, or "N/A - PageSpeed audit was skipped/failed"]

---

## 4. Technical SEO

[Paste SquirrelScan summary from Wave 1, or "N/A"]

---

## 5. On-Page SEO & Content Quality

[Paste SEO expert review from Wave 2]

---

## 6. Blog Content Health

[Paste blog audit summary from Wave 2, or "N/A"]

---

## 7. Structured Data & Schema Markup

[Paste schema review from Wave 2, or "N/A"]

---

## 8. Internal Link Structure

[Paste internal linking analysis from Wave 2, or "N/A"]

---

## 9. Backlink Profile

[Paste backlink analysis from Wave 2, or "N/A"]

---

## 10. AI Search Readiness (AEO/GEO)

[Paste AI search review from Wave 2, or "N/A"]

---

## 11. Competitive Intelligence

[Paste competitor analysis from Wave 2, or "Skipped - run with --competitor=<domain> to include"]

---

## 12. Keyword Research & Content Strategy

[Paste keyword strategy summary from Wave 2, or "Skipped - run with --include-strategy to include"]

**Note:** For full keyword roadmap with detailed action plans, see: `docs/SEO/keyword-strategy-roadmap-YYYY-MM-DD.md`

---

## Prioritized Action Plan

### Critical - This Week

[Items referencing both GSC and GA4 data for each recommendation]

### High Impact - This Month

[Items referencing GSC + GA4 data]

### Medium - This Quarter

[Items]

### Ongoing Maintenance

[Items]

---

## Methodology

- **Data collection:** GSC API (via gsc-fetch.cjs), GA4 API (via ga-fetch.cjs), Lighthouse (local), SquirrelScan CLI
- **Synthesis:** GSC+GA4 joined by landing-page URL via seo-synthesize.cjs; actions ranked by estimated conversion impact
- **Analysis:** Expert review, blog API audit, schema validation, AI search checks, link analysis, backlink assessment
- **Scoring:** Weighted average across 10 dimensions (weights reflect impact on organic growth + revenue)
- **GSC grounding:** All recommendations cite specific keywords, pages, and metrics from Google Search Console
- **GA4 grounding:** Behavioral claims backed by organic session, conversion, and engagement data
```

---

### Step 7: Output Summary

Display to the user:

```
SEO Manager: Audit Complete
============================
Overall Health Score: XX/100 [trend]

Dimension Scores:
  Technical SEO:      XX/100
  Core Web Vitals:    XX/100
  On-Page SEO:        XX/100
  Blog Health:        XX/100
  Schema:             XX/100
  Internal Linking:   XX/100
  Backlinks:          XX/100
  AI Search:          XX/100
  GSC Performance:    XX/100
  GA4 Behavioral:     XX/100

GSC+GA4 Top 3 Priority Actions:
  1. [CRITICAL] ... (~N estimated conversions/mo)
  2. [HIGH] ...
  3. [HIGH] ...

Report saved to: docs/SEO/reports/seo-report-YYYY-MM-DD.md
```

---

## Error Handling

| Error                              | Action                                                              |
| ---------------------------------- | ------------------------------------------------------------------- |
| GSC script fails                   | **HARD STOP** - Display error, help troubleshoot credentials/script |
| GA4 script fails                   | Warn user, mark GA4 dimension as N/A, skip synthesis, continue      |
| Synthesis script fails             | Warn user, use GSC-only context for Wave 2, continue               |
| PageSpeed fails (Chrome not found) | Mark as N/A, note in report, continue                               |
| SquirrelScan not installed         | Mark as N/A, note in report, continue                               |
| Blog audit auth fails              | Mark as N/A, note in report, continue                               |
| Any Wave 2 task fails              | Mark dimension as N/A, redistribute weight, continue                |
| No prior report for trends         | Skip trend comparison, note "First report"                          |
| Competitor domain invalid          | Skip competitor analysis, note in report                            |
| GSC/GA4 ratio outside 0.6–1.6      | Flag tracking issue in report, add "Fix tracking" to Critical items |

## Related Skills

| Skill              | When to use instead                                                        |
| ------------------ | -------------------------------------------------------------------------- |
| `/gsc-analysis`    | Quick GSC-only check, no full audit needed                                 |
| `/ga-analysis`     | Quick GA4 behavioral check, no full audit needed                           |
| `/seo-growth-plan` | Combined GSC+GA4 synthesis only, no full audit — answers "what to do next" |
| `/seo-audit`       | Single-page or targeted SEO review                                         |
| `/pagespeed`       | Performance-only check                                                     |
