---
name: seo-opportunity-research
description: Find and score SEO opportunities from your own rankings, keyword data, SERPs, competitors and site inventory, then decide create, refresh, consolidate, link or skip. Use for "what should I write next", "keyword research for my site", "find page 2 keywords", "which keywords are worth targeting".
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/seo-opportunity-research
---

# SEO opportunity research

Decide what SEO work should happen next: create new content, refresh a page, consolidate overlapping pages, improve internal links, adjust snippets, build a landing page, or ignore a tempting but weak keyword. This is not a generic keyword research skill. It is an evidence-weighted opportunity engine. Keyword volume alone is never enough. It hands back a ranked, de-duplicated list of opportunities, each with a type, evidence, a score, a recommended action and the next skill to run.

> **Romeo's rule:** The keyword with the biggest number is usually the one you can't have; the one you already rank 14th for is the one you can.

## Use this when

- You need to decide what SEO work to do next on a site, ranked by evidence rather than volume.
- You have Search Console data or a keyword export and want the page-2, low-CTR and long-tail wins pulled out of it.
- You have a pile of keyword ideas and need to know which deserve a new page, which belong on an existing page, and which to ignore.
- A commercial, platform or competitor query might deserve a landing or comparison page instead of a blog post.
- You are researching a non-English market and need native keyword behavior, not translations.

## Don't use this for

- Explaining why traffic rose or dropped → `seo-performance-audit`.
- Grouping a large keyword set into hub-and-spoke clusters → `topic-cluster-map`.
- Turning a chosen opportunity into a writer-ready plan → `seo-content-brief`.
- Deciding merge vs differentiate for pages already competing → `keyword-cannibalization-check`.

## What you need

### Required

- Site domain and canonical URL rules.
- Target market: countries, languages, regions, excluded locales.
- Business profile: product category, ideal customers, use cases, pricing model, conversion path.
- Product facts and prohibited claims.
- Existing site inventory, crawl, sitemap, CMS export, or uploaded URL list.
- Search performance data when available: query, page, clicks, impressions, CTR, average position, country, device, date.
- Keyword provider data when available: volume, difficulty/competition, trend, SERP URLs, related terms.
- Competitor domains and comparison targets.
- Topics to prioritize, avoid, or suppress.
- Known active tasks and recent SEO work, so you do not repeat yesterday's work.

### Helpful

- Analytics traffic/conversion by URL.
- Revenue or lead-quality events.
- Prior SEO reports.
- Editorial calendar.
- Support tickets, sales-call notes, product usage, internal search, or AI-bot/server-log demand.
- Localization glossary and country-specific keyword rules.

### No tools?

You can still run this at a basic level. A Search Console Performance export (Queries and Pages, last 3 months compared with the previous 3, as CSV) covers the existing-ranking step on its own: page-2 positions, high-impression low-click rows and long-tail wins. Build site coverage from `/sitemap.xml` opened in a browser, or a URL list the user pastes. For demand, use Google Keyword Planner (free with a Google Ads account; it shows ranges), Google Trends for direction and seasonality, and autocomplete and "People also ask" for phrasing. Inspect the SERP yourself in a private window set to the target country, or ask the user for screenshots. Any volume or difficulty you could not measure is "not checked"; never estimate it.

## Ground rules

- First-party data wins over generic keyword suggestions.
- Existing ranking pages are often more valuable than new articles.
- Page-2 rankings with business fit are the fastest wins.
- Long-tail opportunities beat broad vanity terms for small and mid-sized sites.
- Do not create content that competes with a stronger existing page unless the recommendation is consolidation or refresh.
- Do not report the same unchanged opportunity repeatedly. Preserve suppression windows and already-tracked issue checks.
- For localized SEO, research native keyword behavior. Never translate slugs or keywords literally.

## Data sources

Accept normalized data from whatever sources are available. Examples:

- Google Search Console for existing query/page performance.
- DataForSEO, Ahrefs, Semrush, Moz, Keyword Planner, or CSV for keyword/competitor data.
- Browser automation, SearchAPI, SerpAPI, or cached SERP snapshots for live SERP inspection.
- CMS, crawler, or sitemap export for inventory.
- Analytics export for traffic/conversion weighting.

Keep each source's quirks out of the analysis. Normalize everything into compact records first, then reason over those records.

## Opportunity types

Classify every finding as exactly one primary type:

- Page-2 push: ranking positions 11-30 with relevant demand.
- CTR lift: high impressions, weak CTR, page already matches intent.
- Content refresh: page matches intent but is stale, thin, badly structured, or missing answer-first sections.
- Internal-link lift: relevant page ranks or converts but lacks links from supporting pages.
- New content: no existing page matches the intent.
- Landing page: commercial/platform/tool intent deserves a conversion page rather than a blog post.
- Comparison page: competitor or alternative intent deserves a decision page.
- Consolidation: duplicate intent or cannibalization exists.
- Localization opportunity: local-language demand differs from English targeting.
- Do not pursue: poor business fit, wrong SERP intent, too broad, too competitive, or already sufficiently covered.

## Steps

1. **Build the business/search context.**
   - Summarize the product, buyer, main use cases, and conversion goals.
   - Identify branded terms, non-branded priority themes, comparison terms, platform terms, pain-point terms, and forbidden topics.
   - Load locales and exclusions. For example, a site owner may want English-only reporting, or may want German research to use native German terms.
   - Identify conversion URLs and pages that should receive internal links.

2. **Build or load site coverage.**
   - Normalize URLs and remove tracking parameters.
   - Group pages by section: blog, landing page, comparison, docs, help, product, pricing, templates, glossary.
   - Attach known target keywords and current page purpose.
   - Mark thin pages, stale pages, uncategorized pages, and pages with no conversion path.

3. **Mine existing ranking opportunities.**
   - Pull recent search performance with a comparison period when available.
   - Exclude configured noise: irrelevant locales, test URLs, suppressed clusters, branded terms when non-branded research is requested.
   - Find high-impression low-click records. Default signal: >200 impressions, <5 clicks, CTR <1%, adjusted for site size.
   - Find page-2 opportunities. Default signal: average position 11-30, >100 monthly volume when volume exists, or meaningful impressions when volume is absent.
   - Find long-tail hidden wins. Default signal: 3-4+ words, relevant, already ranking or generating impressions.
   - Find scaling pages. Default signal: CTR >3% with low impressions, or high engagement/traffic with low search visibility.
   - Detect cannibalization by grouping queries/pages by intent, not just exact keyword.

4. **Mine new keyword opportunities.**
   - Start from business themes, product use cases, customer roles, platforms, competitors, and pain points.
   - Prefer long-tail 100-1000 volume for realistic small-site wins unless the site has authority for larger terms.
   - Check whether the site already ranks. If rank is 1-10, classify as defend/scale, not new content. If 11-30, classify as page-2 push. If >30 or absent, consider new/refresh.
   - Filter out one-word/generic terms, wrong-language terms, polluted intent, and topics that require claims the site cannot support.

5. **Inspect the SERP before recommending content.**
   - Review top 3-5 ranking pages or SERP records.
   - Capture page type: blog, listicle, landing page, product page, support doc, template, tool, forum, marketplace, video.
   - Note answer pattern: quick answer, steps, table, feature grid, calculator, FAQ, comparison, local pack, forum-heavy, UGC-heavy.
   - Identify what ranking pages do well: title angle, headings, depth, examples, tools covered, media, schema.
   - Identify gaps the site can credibly fill.
   - If SERP intent is polluted or mismatched, downgrade or mark do not pursue.

6. **Score each candidate.**
   - Business fit: 0-5. Does this attract people who can become customers?
   - Evidence strength: 0-5. First-party ranking/impression/conversion evidence beats external keyword guesses.
   - Search demand: 0-5. Use volume, impressions, trend, and seasonality.
   - Rankability: 0-5. Consider current rank, domain strength, SERP type, competitor quality, page type match.
   - Conversion path: 0-5. Can the page naturally link to or become a conversion page?
   - Freshness/urgency: 0-5. Rising demand, content decay, recent drop, or urgent commercial opportunity.
   - Effort: 0-5 reversed. Refresh/internal link is easier than a full new page; technical/design dependencies reduce score.
   - Risk: 0-5 reversed. Existing ranked title/meta changes, legal/medical claims, or SERP mismatch reduce score.

7. **Decide the action.**
   - Create only when no existing page satisfies intent.
   - Refresh when a page is already close but weak.
   - Consolidate when multiple pages split the same intent.
   - Internally link when the content is good but unsupported.
   - Update snippet only when the current title/meta is clearly weak and the page is not a sensitive ranked page. Protect pages already ranking well.
   - Build landing page when the query is commercial or platform/tool-specific and conversion intent is clear.
   - Build comparison page when the query implies alternatives, vs, competitor, pricing, or selection criteria.
   - Ignore when the keyword is tempting but strategically weak.

8. **De-duplicate and suppress repeats.**
   - Check site inventory, active tasks, recent reports, and completed work.
   - Compare by URL, keyword cluster, and intent, not exact title.
   - If already tracked, return the existing item and do not create a duplicate recommendation.
   - Suppress repeated clusters unless there is a material new event: large movement, new keyword outside the cluster, technical issue, or explicit user request.

## Quality bar

A good recommendation should answer:

- Why this opportunity matters now.
- Whether to create or improve an existing page.
- Which intent the page must satisfy.
- What proof supports the recommendation.
- What not to do.

## What to hand back

Fill in this template. Rank recommendations by score, highest first.

```markdown
# SEO opportunities: <site> (<market>, <data date range>)

**What I found:** <one plain-English sentence>
**What matters most:** <one sentence>
**What to do first:** <one sentence>

## Executive summary
- <3-6 bullets with the highest-signal findings>

## Ranked recommendations

### 1. <keyword cluster>
- Opportunity type: <exactly one primary type>
- Keyword cluster: <primary query + close variants>
- Current/proposed URL: <URL>
- Target country/language: <...>
- Evidence: <search / keyword / SERP / inventory facts, each marked seen, tool or inferred>
- Score: <total>/40 (business fit x, evidence x, demand x, rankability x, conversion path x, freshness x, effort x, risk x)
- Confidence: high / medium / low
- Priority: `Fix now` / `Fix next` / `Worth doing` / `Leave it`
- Recommended action: <create / refresh / consolidate / internal link / snippet update + risk note / landing page / comparison page / ignore>
- Why this matters for the business: <...>
- What not to do: <...>
- Next skill to call: <`seo-performance-audit` / `seo-content-brief` / `seo-blog-writer` / `seo-content-qa` / `site-content-inventory` / `cms-publishing-adapter` / `comparison-page-writer` / `internal-linking-plan` / `title-meta-ctr` / `keyword-cannibalization-check`>

### 2. ...

## Already covered or suppressed
- <cluster>: <existing URL or tracked item>, <why it is not a new recommendation>

## Do not pursue
- <keyword or cluster>: <reason>

## Data gaps that would improve confidence
- <missing source and what it would change>

## What I could not check
- <e.g. search volume not checked: no keyword data provided>
```

## Stop and flag if

Fail the research, and say so instead of handing it back as done, if:

- It proposes topics from volume alone.
- It ignores existing pages and creates duplicate content.
- It misses obvious first-party page-2 or low-CTR opportunities.
- It reports excluded languages/markets.
- It repeats unchanged findings without checking prior work.
- It recommends title/meta changes for already-ranking pages without a risk note.
- It treats translated keywords as valid without local keyword research.

## Next step

- Run `seo-content-brief` on the top create, refresh, landing or comparison recommendation, passing its evidence, score, intent and SERP notes.
- Route other types to their specialist: internal-link lifts to `internal-linking-plan`, CTR lifts to `title-meta-ctr`, consolidation to `keyword-cannibalization-check`.
- If site coverage was thin or missing, run `site-content-inventory` first, then re-run this skill.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
