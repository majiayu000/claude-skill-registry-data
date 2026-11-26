---
name: seo-performance-audit
description: Audit organic search performance from Search Console and analytics data to explain what rose, dropped or stalled, the likely cause, and what to do next. Use for "why did my traffic drop", "what changed in Search Console", "analyse my GSC data", "which pages are declining".
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/seo-performance-audit
---

# SEO performance audit

Explain what rose, dropped, stalled, or became newly actionable across organic search and analytics. This skill is not a rank-tracker dump. It is a decision filter: identify meaningful movement, suppress noise, diagnose likely cause, and recommend the next action. It hands back a short audit of the movements that matter, each with evidence, a likely cause, a priority and the next skill to run.

> **Romeo's rule:** Most ranking wobbles are weather, not climate; report only the movement that changes what someone should do this week.

## Use this when

- Traffic or clicks dropped or jumped and you want to know why.
- You want a weekly or monthly read of Search Console data that surfaces hidden movement, not the same top terms every time.
- Search Console and analytics disagree and you need to know what that disagreement means.
- A migration, redesign, redirect batch or big content update shipped and you need to separate expected volatility from real damage.
- You want page-2, low-CTR, scaling and new-query opportunities pulled out of existing performance data.

## Don't use this for

- Finding new keywords to target → `seo-opportunity-research`.
- Digging into a suspected crawl, indexing, canonical or redirect problem → `technical-seo-audit`.
- Rewriting weak titles and meta descriptions → `title-meta-ctr`.
- Snapshotting signals before a deploy so you can compare after → `seo-change-monitor`.

## What you need

### Required

- Site domain and canonical URL rules.
- Date range and comparison range.
- Target countries/languages and excluded locales.
- Search performance data: query, page, clicks, impressions, CTR, position, country, device, date.
- Site inventory with page type, target keyword, status, content owner, last updated date.
- Known changes: migrations, redirects, launches, page updates, title/meta edits, outages, campaigns, seasonality.
- Existing tasks and prior audit reports.

### Helpful

- Analytics by URL: sessions, pageviews, users, organic segment, conversions, engagement.
- Rank tracker or SERP snapshots.
- Crawl/indexing data.
- Revenue/lead-quality data by landing page.
- Server logs, AI-bot fetches, internal search, or support demand.

### No tools?

Search Console's Performance report is free and enough for a basic audit. Use its Compare option (last 28 days vs the previous period, or vs the same period last year for seasonal sites), export the Queries and Pages tabs as CSV, and filter by country and device. For any page with a sudden impressions drop, open the Page indexing report and URL Inspection. If there is no analytics export, ask for screenshots of organic landing pages by period from GA4 or whichever analytics tool the site uses. Without a change log, ask the user what shipped in the window and check the Wayback Machine for title or layout changes on pages that dropped. Remember that Search Console data lags by a few days and hides rare queries for privacy, so query rows will not add up to page totals.

## Ground rules

- Lead with hidden movement, not the same known top terms every day.
- Search movement must be interpreted with impressions and CTR, not position alone.
- Analytics and Search Console (GSC) can disagree; that disagreement is often the finding.
- Do not call normal fluctuation a problem.
- Do not recommend risky title/meta edits casually, especially on pages already ranking.
- Ignore configured irrelevant locales, test pages, and suppressed clusters.
- Do not duplicate active tasks.

## Data sources

Normalize data from Google Search Console, GA4, PostHog, Plausible, Amplitude, Fathom, server logs, DataForSEO, Ahrefs, Semrush, SearchAPI, crawlers, or CSV uploads.

Work from compact normalized rows. Never pass raw large API payloads into the reasoning step.

## Default movement rules

Tune thresholds per site size, but start with these defaults:

- Page-2 opportunity: average position 11-30 and meaningful impressions or keyword volume >100.
- Low CTR opportunity: >200 impressions, CTR <1%, and page appears relevant.
- Severe low CTR: >1000 impressions, CTR <1%.
- Scaling opportunity: CTR >3% with <100 impressions/week or low distribution.
- Big mover: average position changes by >=5 positions.
- Core/high-volume terms: only alert on >=10 position movement unless explicitly watched.
- Sharp traffic movement: pageviews/sessions change >=25% with enough baseline volume.
- New query discovery: relevant query appears with impressions/rank that did not exist in prior window.
- Decay candidate: clicks or impressions down for 2+ comparable periods while ranking/intent was previously stable.

## Steps

1. **Normalize and filter.**
   - Align timezones, date windows, and data freshness. Remember GSC is delayed.
   - Normalize URLs and strip parameters.
   - Group by URL, query, country, device, page type, and content cluster.
   - Exclude configured languages/locales, staging/test URLs, branded terms when requested, and known suppressed clusters.
   - Compact external data before analysis.

2. **Load context before judging movement.**
   - Pull site inventory and target keyword mapping.
   - Read recent reports or saved findings for the comparison horizon.
   - Read active tasks/issues so repeated opportunities are marked already tracked.
   - Load known launches, redirects, title/meta changes, deployments, and campaigns.

3. **Detect search movement.**
   - Find rising pages and queries.
   - Find slipping pages and queries.
   - Find page-2 clusters that can be pushed to page 1.
   - Find high-impression/low-click rows.
   - Find high-CTR/low-impression pages worth scaling.
   - Find new queries that reveal language customers use.
   - Find cannibalization candidates where several URLs split one intent.

4. **Cross-check analytics.**
   - Compare organic search movement to pageviews/sessions/conversions.
   - Flag cases where GSC is up but analytics is flat/down, or analytics is up without GSC support.
   - Use conversions to raise priority for pages that affect signups, demos, trials, purchases, or lead quality.
   - Skip top-known pages if the audit goal is hidden opportunities.

5. **Diagnose likely cause.**
   - Content decay: old page slipping, competitor content fresher, weak top section.
   - SERP shift: page type changed, forums/videos/tools now dominate, featured snippet changed, or an AI Overview now answers the query (impressions hold while clicks fall; Search Console's generative AI performance report shows whether the page is cited there).
   - Snippet issue: impressions high, CTR low, title/meta or visible promise weak.
   - Intent mismatch: page ranks for query but does not answer the query quickly.
   - Cannibalization: multiple pages target same intent.
   - Internal-link gap: relevant page exists but lacks authority flow from related content.
   - Indexing/technical issue: sudden impressions drop, URL excluded, canonical/redirect/crawl issue suspected.
   - Tracking issue: analytics changed without search data support.
   - Seasonality: predictable demand shift.
   - Google update or manual action: the drop starts on the dates of a core, spam or other ranking update on Google's Search Status Dashboard, or Search Console's Manual actions or Security issues report is not empty. Check both before blaming a page.
   - Expected volatility: recent redirect/consolidation or major page update. Do not over-alert for 2-4 weeks after redirects.

6. **Prioritize.** Use the library's priority labels.
   - `Fix next` (`Fix now` when the drop hits a conversion page or has a sitewide technical cause):
     - page-2 rank 11-20 with business-fit demand
     - >500 impressions and near-zero clicks
     - conversion page affected
     - sharp sustained drop on important page
     - newly discovered cluster with clear commercial fit
   - `Worth doing`:
     - rank 21-30 with good fit
     - high CTR low impressions
     - internal-link improvements
     - refreshes that do not require design/CMS dependencies
   - `Leave it` (say why):
     - minor rank noise
     - low-fit generic terms
     - duplicate findings
     - known suppressed clusters

7. **Choose action.**
   - Brief for create/refresh/comparison/landing page (`seo-content-brief`).
   - Internal-link task (`internal-linking-plan`).
   - Snippet/title/meta review with risk flag (`title-meta-ctr`).
   - Technical/indexing investigation (`technical-seo-audit`).
   - Consolidation plan (`keyword-cannibalization-check`).
   - Continue watching.
   - Suppress/ignore.

8. **De-duplicate.**
   - Check existing tasks by URL, keyword cluster, and intent.
   - If matched, mark already tracked with task id or reference.
   - Only create a new recommendation when the action, page, or keyword cluster is materially different.
   - Include a duplicate-check note in every audit.

## Required evidence per finding

Each finding needs:

- URL or proposed URL.
- Query/cluster.
- Current metrics and comparison metrics.
- Why it is meaningful.
- Recommended action.
- Confidence.
- Whether it is new, repeated, or already tracked.

## What to hand back

Fill in this template. Write every finding in the finding format shown under Rises; leave a section out only if it has nothing in it, and say so in one line.

```markdown
# SEO performance audit: <site>, <date range> vs <comparison range>

**What I found:** <one plain-English sentence>
**What matters most:** <one sentence>
**What to do first:** <one sentence>

## Executive summary
- <what matters, not a raw data tour>

## Rises
- **<URL or proposed URL>** | <query/cluster>
  - Now vs before: <clicks, impressions, CTR, position, current vs comparison>
  - Why it is meaningful: <interpretation>
  - Recommended action: <...>
  - Confidence: high / medium / low (seen / tool / inferred)
  - Status: new / repeated / already tracked (<task id or reference>)

## Drops
- <finding format, plus likely cause and risk level: high / medium / low>

## Page-2 opportunities
## CTR opportunities
## New query discoveries
## Analytics mismatches
## Cannibalization or duplicate-intent notes

## Already tracked or suppressed
- <item>: <task id, reference or suppression reason>

## Recommended actions
1. <action> | priority: `Fix now` / `Fix next` / `Worth doing` / `Leave it` | page: <URL> | owner or destination: <who or what acts on it> | next skill: `<slug>`

## Duplicate check
- <tasks and prior reports checked; what matched>

## Data gaps or failed sources
- <source, what failed, what it means for confidence>

## What I could not check
- <...>
```

## Stop and flag if

Fail the audit, and say so instead of handing it back as done, if:

- It includes excluded languages/locales.
- It reports raw API dumps.
- It alerts on minor fluctuations without business context.
- It repeats unchanged findings from recent reports without saying already tracked.
- It skips duplicate checks.
- It recommends risky title/meta changes on a ranking page without warning.
- It ignores analytics/conversion data when available.

## Next step

- For each `Fix now` or `Fix next` create, refresh, comparison or landing action, run `seo-content-brief` with the URL, query cluster, metrics and diagnosed cause.
- For suspected indexing or technical causes, run `technical-seo-audit` on the affected URLs before touching content.
- For page-2 clusters and new query discoveries that need fresh demand data, run `seo-opportunity-research`.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
