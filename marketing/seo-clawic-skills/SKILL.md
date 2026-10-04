---
name: SEO (Site Audit + Content Writer + Competitor Analysis)
slug: seo
version: 1.0.6
description: 'Improves Google rankings with search engine optimization (SEO): audits, keyword research, content optimization, technical fixes, schema, and links. Not for paid search ads (PPC/SEM) or app store optimization. Use when organic traffic or rankings drop, pages are not indexed or get deindexed, crawl errors appear in Search Console, or a migration, redesign, or domain change is planned. Also for writing or refreshing content to rank, picking target keywords, fixing titles, canonicals, sitemaps, robots.txt, redirects, hreflang, duplicate content, or Core Web Vitals, and adding schema markup. And for chasing featured snippets or AI Overview citations, recovering from a Google penalty, core update, or manual action, optimizing local, ecommerce, SaaS, or publisher sites, or setting up Bing Webmaster Tools and IndexNow.'
homepage: https://clawic.com/skills/seo
changelog: 'Full coverage pass: deeper guides, situation-named files, and per-user configuration'
metadata:
  clawdbot:
    emoji: 🔍
    os:
    - linux
    - darwin
    - win32
    displayName: SEO (Site Audit + Content Writer + Competitor Analysis)
    configPaths:
    - ~/Clawic/data/seo/
    - ~/seo/
    - ~/clawic/seo/
  openclaw:
    requires:
      config:
      - ~/Clawic/data/seo/
      - ~/seo/
      - ~/clawic/seo/
---

All persistent data (site profiles, config, audit history, keyword tracking) lives in `~/Clawic/data/seo/`. If you have data at an old location (`~/seo/` or `~/clawic/seo/`), move it to `~/Clawic/data/seo/`, and say in one line that you moved it and from where. Read `setup.md` on first use; `memory-template.md` holds the file format.

## When To Use

- Auditing a site: indexing, technical health, on-page, content, links, structure
- Diagnosing a ranking or organic traffic drop, a deindexed page, or a core-update hit
- Writing, refreshing, or consolidating content to rank for a target query
- Keyword research, opportunity sizing, competitor gap analysis, cannibalization
- Shipping structural changes safely: migrations, redesigns, hreflang, faceted navigation, programmatic pages
- Earning visibility in the surfaces above the ten blue links: snippets, packs, AI Overviews
- Not for paid search ads (PPC, Google Ads bidding, quality score) or for content planning with no search target — route to `content-marketing`

## Quick Reference

| Situation | Read |
|-----------|------|
| Ranking or organic traffic dropped | Triage below first, then `recovery.md` |
| Core update hit, manual action, hacked or spammy pages, reconsideration request | `recovery.md` |
| First pass on a new site, scoping an audit, writing the deliverable | `audits.md` |
| Picking keywords, sizing opportunity, competitor gaps, cannibalization | `keywords.md` |
| Deciding what to write, intent, E-E-A-T, thin content, AI-written drafts | `content.md` |
| Bottom-funnel pages: alternatives, "vs", best-X, pricing, integrations, glossary | `commercial-pages.md` |
| Titles, meta descriptions, headings, URLs, image alt text | `on-page.md` |
| Site structure, click depth, topic clusters, subdomain vs subfolder, index bloat, new site from zero | `architecture.md` |
| Pages not indexed, robots.txt, canonicals, sitemaps, status codes, duplicates, log files | `technical.md` |
| Slow pages, LCP / INP / CLS failing, PageSpeed vs field data | `performance.md` |
| React/Vue/Angular site, content missing from view-source, SPA routing, soft 404s | `javascript.md` |
| JSON-LD, rich results, review stars, breadcrumbs, product feeds | `schema.md` |
| Internal links, backlinks, anchor text, outreach, disavow | `links.md` |
| Physical location or service area, Google Business Profile, reviews, map pack | `local.md` |
| Product and category pages, faceted navigation, variants, out-of-stock, pagination | `ecommerce.md` |
| Multiple languages or countries, hreflang, geotargeting, translated duplicates | `international.md` |
| Domain change, replatform, redesign, URL restructure, HTTP to HTTPS | `migrations.md` |
| Featured snippets, People Also Ask, sitelinks, image and video results, pixel position | `serp-features.md` |
| AI Overviews, AI Mode, ChatGPT and Perplexity citations, AI crawlers, llms.txt | `ai-search.md` |
| Search Console data, exports, regex filters, proving a change worked, forecasting, reporting | `search-console.md` |
| Bing, IndexNow, Applebot, Yandex, Naver, Baidu, privacy engines | `other-engines.md` |
| Publisher work: Top Stories, Google News, Discover traffic, paywalls | `news-discover.md` |
| Generating hundreds or thousands of templated pages | `programmatic.md` |
| WordPress, Shopify, Webflow, Wix, Next.js platform quirks | `cms-platforms.md` |
| Anything else SEO | Run the audit checklist below, then route from the area that fails |

## Core Rules

1. **Audit before prescribing.** Fixed order: manual actions → indexing → intent match → technical → content → links. Diagnosing content quality on a page Google never indexed wastes the engagement; every layer above depends on the one before it.
2. **The SERP is the spec.** Before writing or prescribing format, search the exact query in the target market. Page 1 defines format, depth, and freshness. If page 1 is all product grids, a 3,000-word guide will not rank there at any quality level.
3. **Improve before you create.** Pages at position 4-15 in Search Console with impressions at or above `min_impressions` (Configuration; default 100/month) are the highest-ROI work: better snippet, filled content gaps, internal links. Write a new page only when no existing URL targets the intent. Example: a page at position 8 with 1,000 monthly impressions needs a title rewrite and two internal links — not a competing new article, which triggers rule 4.
4. **One intent per page.** Two URLs alternating in Search Console for the same query = cannibalization: Google splits signals and both underperform. Fix: 301 the weaker into the stronger, merge unique content. Map keywords by intent, not by string — Google clusters variants onto one page.
5. **Technical floor.** Core Web Vitals "good" thresholds (Google, field data at p75): LCP < 2.5s, INP < 200ms, CLS < 0.1. HTTPS, mobile-first, self-referencing canonicals, clean sitemap. Technical debt caps everything content can earn.
6. **E-E-A-T is signals, not a score.** No E-E-A-T meter exists — demonstrate it: author bios with verifiable credentials, first-hand evidence (photos, data, tests), citations, contact and about pages. Decisive for YMYL topics (health, finance, legal, safety).
7. **Links: earn, never buy.** Bought links risk manual actions that take months to recover from after cleanup. Internal links are the lever you fully control — spend them before any outreach.
8. **Iterate from Search Console, not assumptions.** Each symptom has a different fix: CTR far below the position curve → rewrite the snippet. Impressions but no clicks → intent or SERP-feature problem. No impressions → indexing or relevance problem. GSC tells you which; guessing does not.
9. **Size the prize before doing the work.** `expected monthly clicks = volume × CTR at the realistic position × (1 − feature discount)`. Worked: 2,000 searches/mo, realistic landing spot position 5 (~5-10% CTR), an AI Overview and an ads block above → 2,000 × 0.07 × 0.6 ≈ 84 clicks/mo. If that number does not justify the build, say so before writing.

## Ranking Drop Triage

In order — stop at the first confirmed cause:

1. GSC → Manual Actions + Security Issues. If flagged, that IS the diagnosis (`recovery.md`).
2. URL Inspection on hit pages: still indexed? Google-selected canonical changed to another URL?
3. Recent deploys: robots.txt edits, stray noindex, redirect changes, template changes shipped near the drop date.
4. Drop date vs Google's announced update dates. Aligned = sitewide quality reassessment, not a page bug — fix the weakest content across the site.
5. Search the lost queries: did the SERP change format or gain features (AI Overview, more ads, a pack) that push you down visually at the same rank?
6. Backlinks: links lost on your side, or a competitor gained them.
7. Seasonality and tracking: compare year-over-year, and confirm the drop is not analytics (broken tag, bot filter, property change) before treating it as SEO.
8. None conclusive → gap-compare the pages that replaced you (`keywords.md`).

## SEO Audit Checklist

**Indexing:**
- [ ] Important pages indexed — verify with URL Inspection and the Page indexing report, not the `site:` operator
- [ ] No important pages blocked in robots.txt
- [ ] XML sitemap submitted to Search Console, only canonical 200-status URLs in it
- [ ] No stray noindex on pages that should rank
- [ ] No page both robots.txt-blocked AND noindexed — blocked crawl means Google never sees the noindex, so the page can stay indexed

**Technical:**
- [ ] Core Web Vitals passing (thresholds in rule 5)
- [ ] Mobile-friendly, HTTPS with no mixed content
- [ ] No crawl errors, no soft 404s, no server errors in Search Console
- [ ] Redirect chains ≤3 hops
- [ ] Rendered HTML contains the main content (JavaScript sites)

**On-Page:**
- [ ] Unique title tags (50-60 chars), meta descriptions (150-160 chars)
- [ ] One H1 per page with the target term; proper heading hierarchy
- [ ] Images with alt text; internal links to and from the page

**Content:**
- [ ] Search intent matched (rule 2)
- [ ] No cannibalization (rule 4)
- [ ] No thin or duplicate content; dead pages improved, consolidated, or removed

**Off-Page and Entity:**
- [ ] Google Business Profile complete (local businesses)
- [ ] Backlink profile checked for toxic patterns
- [ ] Brand queries return the right result, sitelinks, and knowledge panel where applicable

## Content Writing Process

1. **Keyword research** — target keyword, volume, SERP reality check (`keywords.md`)
2. **Intent analysis** — search the query in the target market; page 1 is the format spec
3. **Gap + gain** — cover what ranking pages cover, then add what none of them have
4. **Write** — answer the query in the first ~100 words, then structure per `content.md`
5. **Optimize** — title, meta, headers, internal links from strong pages, schema
6. **Publish** — request indexing once, log in `~/Clawic/data/seo/memory.md`, review GSC after a few weeks

## What Takes How Long

Honest ranges beat invented dates; every one of these is mechanism, not promise.

| Change | Time to effect | Mechanism |
|---|---|---|
| Title or meta rewrite | Days to appear, 2-4 weeks to judge | Needs a recrawl, then enough impressions for CTR to be readable |
| New page, established site | Indexed in days; competitive movement 3-6 months | Discovery is fast; earning position takes links and engagement history |
| New domain | Months before competitive queries move | No confirmed sandbox — the delay is missing links, history, and coverage |
| Core Web Vitals fix | ~4 weeks before field data reflects it | CrUX field data is a 28-day rolling window; lab scores change instantly |
| 301 migration | 2-8 weeks of turbulence, longer on large sites | Google must recrawl every redirected URL to transfer signals |
| Manual action revoked | Days to weeks after reconsideration | Human review queue; recovery of position is separate and slower |
| Core update recovery | Usually at the next update, not between them | Sitewide reassessments are recomputed on update cycles |
| Disavow file | Weeks to months | Applied as links are recrawled, not on upload |

## Output Gates

Before delivering recommendations or content:

- Did I search the actual query in the target market, or am I prescribing format from memory?
- Did I check for an existing page targeting this intent before recommending a new one?
- Is every number I cite from this skill's files or the user's own data, not improvised?
- Does each recommendation name the exact URL and the exact change ("rewrite /pricing title to lead with X"), not "improve content"?
- Did I size the prize (rule 9) so the user can refuse the work?
- Am I promising a date? State the mechanism and a range from What Takes How Long, never a deadline.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/seo/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| site_type | blog \| ecommerce \| saas \| local \| news \| directory \| auto | auto | Weights the audit checklist and decides which guide the router opens first; `auto` infers from URL patterns and page templates on first look |
| target_market | text (locale, e.g. en-US) | en-US | Which SERP to check, which spelling variant to write, and whether hreflang and local guidance apply |
| tool_access | gsc-only \| paid-suite | gsc-only | `gsc-only` keeps every workflow on free data (GSC, Trends, SERPs); `paid-suite` unlocks backlink-index and difficulty-score steps |
| risk_posture | conservative \| standard \| aggressive | conservative | Gates link tactics, external anchor ratios, and how much templated page generation to recommend |
| cms | wordpress \| shopify \| webflow \| wix \| headless \| other \| auto | auto | Picks the implementation path for every fix (where redirects, robots, and metadata actually live) |
| min_impressions | number (impressions/month) | 100 | Floor for every opportunity list: striking distance (rule 3, `keywords.md`, `search-console.md`) and the traffic-at-stake cutoff for the audit Top 5. Below it, a page cannot produce a readable CTR or click change — raise it on large sites |
| voice_file | path | none | Brand voice guide at `~/Clawic/data/seo/<file>`; governs drafted copy, never the SEO structure |

Preference areas — customizable dimensions; a stated preference gets recorded in config.yaml and applied:

- **Reporting**: audit depth (one-page priorities vs full report), technical vs business language, which KPI leads (clicks, conversions, revenue)
- **Conventions**: URL and slug style, title formula (brand position and separator), heading patterns, internal anchor style
- **Scope boundaries**: sections that are off-limits (legal, careers, docs), staging hosts, URLs never to touch
- **Implementation**: whether the agent edits files and writes patches or hands over specs and tickets
- **Measurement**: reporting property, comparison window, whether branded queries are excluded from "SEO traffic"
- **Thresholds**: floors that gate what gets worked on — impressions (`min_impressions`), traffic at stake for a finding to make the Top 5, minimum sample before a test is called
- **Cadence**: rank and GSC review frequency, content refresh schedule, reporting date

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Writing before checking the SERP | Format mismatch = no ranking at any quality | Rule 2: the SERP is the spec |
| New article for a query an existing page ranks 4-15 for | Cannibalization splits signals | Improve the existing page (rule 3) |
| Chasing keyword density | No density threshold exists; stuffing detection is pattern-based | Cover the topic, use variants naturally |
| noindex on a robots.txt-blocked page | Google never crawls it, never sees the noindex | Allow crawl until deindexed, then block |
| Changing URLs without 301s | Links and authority now point at 404s | Map every old URL to its closest new match |
| Buying links or PBNs | Payment and network footprints → manual action | Earn links via assets and digital PR |
| Reporting rank without checking the rendered SERP | #1 under an AI Overview and four ads earns a fraction of historical #1 clicks | Check pixel position, not just rank |
| Judging index coverage with `site:domain.com` | The operator is an estimate and excludes results Google chooses to hide | Page indexing report + URL Inspection |
| Re-requesting indexing for the same URL repeatedly | The queue is not a priority auction; nothing accelerates | Fix the reason it was not indexed (quality, duplicate, discovery) |
| Fixing every warning a crawler emits | Crawl tools flag non-signals (meta keywords, long titles on pages with no impressions) | Rank issues by the traffic at stake, then fix |
| Optimizing a page whose Google-selected canonical is another URL | Every signal you add credits the other URL | Resolve the canonical conflict first |
| Reporting "average position improved" as a win | Average position moves when the query mix changes; new long-tail impressions drag it down while traffic grows | Report clicks and conversions, positions per query |

## Where Experts Disagree

- **Word count.** Studies show correlation between length and ranking; nobody serious claims causation. Cover the intent fully, then stop — padding is a negative.
- **Disavow.** Google says it is unnecessary without a manual action; some practitioners still disavow after obvious spam attacks. Default: don't, unless a manual action names links.
- **Exact-match anchors.** They move rankings in tests AND they are the first pattern link-spam systems check. The disagreement is the safe ratio, not the risk — keep exact match a small minority of external anchors.
- **Subdomain vs subfolder.** Google states both can rank; migration case studies keep showing subfolder gains. Unresolved: whether the gains come from the structure or from the consolidation and relaunch links that accompany the move. Default subfolder for new builds; do not migrate a working subdomain for this reason alone.
- **Optimizing for AI Overviews.** One camp treats citation as the new goal; the other says citations that suppress clicks are a bad trade and defends click-worthy queries instead. Both are right per query type — decide per page with the click data, not sitewide.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/seo (install if the user confirms):

- `content-marketing` — Content strategy
- `analytics` — Traffic analysis
- `market-research` — Competitive analysis
- `html` — HTML optimization
- `web` — Web development

## Feedback

- If useful, star it: https://clawic.com/skills/seo
- Latest version: https://clawic.com/skills/seo

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/seo.
