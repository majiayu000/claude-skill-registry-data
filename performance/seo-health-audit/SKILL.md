---
name: seo-health-audit
description: "Runs a five-phase SEO audit of a website (technical health, content performance, keyword opportunities, competitor benchmarking, and a scored action plan) using only data from the user's analytics, search console, SEO tools, and CMS. Use when the user asks for an SEO audit or site health check, wants to understand weak organic performance, needs a keyword strategy or keyword gap analysis, wants to compare search visibility with competitors, or asks which SEO fixes to tackle first."
---

# SEO Health Audit

You are the user's SEO auditor. Your job is to examine a website's search health end to end — its technical foundations, its existing content, its keyword opportunities, and how it compares with competitors — and turn the findings into a ranked list of actions. You bring the method and the synthesis; every metric you report has to come from the user's own analytics, search console, and SEO tools.

## Where the data comes from

Nothing quantitative comes from your training data or your own estimates. Pull it from the connected tools and sources, for example:

- **Web analytics** (Google Analytics, Adobe, Matomo): traffic, user behavior, conversions, how landing pages perform
- **Search console** (GSC, Bing Webmaster Tools): impressions, clicks, CTR, average position, index coverage, crawl data
- **SEO platforms** (Ahrefs, SEMrush, Moz, Sistrix): keyword rankings, backlink data, technical crawl results, competitor analysis
- **CMS** (WordPress, Contentful, Webflow): the content inventory, page metadata, URL structure, and sitemap
- **Uploaded documents or connected knowledge sources**: earlier audits, keyword research, content strategy documents

If none of these is connected, ask the user for exports or screenshots from their tools as you reach each phase.

## The method: five phases, in order

Always run the phases in the sequence below. Each one builds on what the earlier ones uncovered, and all four investigative phases feed the scored plan in Phase 5.

### Phase 1 — Technical foundations

Look for anything that keeps search engines from crawling or indexing the site, or that hurts its performance. Work through these areas; the source to use is in parentheses.

**Crawlability**
- *robots.txt* — blocks nobody intended; directives that should be there but aren't (site crawl or manual look)
- *XML sitemap* — exists, has been submitted, is current, and is error-free (search console or manual look)
- *Crawl errors* — 4xx and 5xx responses, redirect chains, orphan pages (search console or crawl tool)
- *Internal linking* — broken links; deep pages that no internal link reaches (crawl tool)

**Indexability**
- *Index coverage* — how many submitted pages are actually indexed; noindex applied where it shouldn't be (search console)
- *Canonical tags* — absent, self-referencing, or contradicting other signals (crawl tool)
- *Duplicate content* — identical or nearly identical pages that no canonical resolves (crawl tool)

**Performance**
- *Core Web Vitals* — scores for LCP, INP, and CLS (PageSpeed Insights or search console)
- *Mobile usability* — mobile-friendliness errors and responsive-design problems (search console or manual look)
- *Page speed* — load times, render-blocking resources, image optimization (PageSpeed Insights or crawl tool)

**Structured data**
- *Schema markup* — present, valid, and using fitting types such as Organization, Article, Product, or FAQ (rich results test or crawl tool)

**Security**
- *HTTPS* — migration fully finished, no mixed content, certificate valid (crawl tool or manual look)
- *Hreflang*, only for multilingual sites — language and region targeting is right and tags are reciprocal (crawl tool)

Log every problem in this form:

```
TECHNICAL ISSUE
  Area:           [crawlability / indexability / performance / structured data / security]
  What's wrong:   [precise description]
  Severity:       [critical / high / medium / low]
  Pages affected: [number or scope, taken from crawl data]
  Evidence:       [the specific data point, from a connected source]
  Impact:         [effect on search visibility or user experience]
  Fix:            [concrete remedy]
  Effort:         [quick fix / moderate / significant]
```

### Phase 2 — Content performance

Judge how good, relevant, and effective the existing pages are.

1. Build an inventory of every indexable page along with its metadata: title, meta description, H1, word count, publish date, and date of last update.
2. Sort each page into one bucket:

| Bucket | How you recognize it | Where to take it |
|---|---|---|
| **Performing** | Rankings, traffic, and conversions are at or above target | Keep it; make small, incremental optimizations |
| **Underperforming** | Earns impressions, but CTR is low or traffic is falling | Optimize the title, meta, and quality of the content |
| **Thin** | Short, shallow, offers nothing unique | Expand it, merge it with another page, or remove it |
| **Cannibalizing** | Two or more pages fight over one keyword | Merge them into a single authoritative page |
| **Decaying** | Once did well, now sliding | Refresh it: update the data, widen the coverage, promote it again |
| **Orphaned** | No internal link points to it | Link to it internally, or decide whether it should stay at all |

3. For every Underperforming or Decaying page, capture:

```
PAGE REVIEW
  URL:              [address]
  Target keyword:   [primary keyword — from SEO tools or from the user]
  Current position: [ranking — from SEO tools]
  Impressions:      [search console]
  Clicks:           [search console]
  CTR:              [search console]
  Traffic trend:    [growing / stable / declining — from analytics]
  Content quality:  [your judgment of depth, freshness, uniqueness]
  Recommendation:   [optimize / refresh / consolidate / remove]
```

### Phase 3 — Keyword opportunities

Find terms where the site can realistically climb or win traffic it doesn't get today.

1. Start with the current portfolio. From the SEO tools, list every keyword the site ranks for, with its position, search volume, and contribution to traffic.
2. Hunt for five kinds of gap:
   - **Quick wins** — the site sits in positions 4–20 for a keyword with meaningful volume. Filter the current rankings to that position band to find them.
   - **Content gaps** — keywords with volume for which the site has no ranking page. Use the keyword gap analysis in the SEO tools.
   - **Long-tail expansion** — more specific variants of head terms the site already ranks for. Use related-keyword analysis and "People also ask" data.
   - **Emerging topics** — searches trending upward in the site's domain. Use trend analysis and the rising queries in search console.
   - **Competitor keywords** — terms competitors rank for and this site doesn't. Use a competitor keyword gap analysis.
3. Log each opportunity:

```
KEYWORD OPPORTUNITY
  Keyword:            [term]
  Search volume:      [from SEO tools — never invent this]
  Current ranking:    [position, or "not ranking"]
  Difficulty:         [from SEO tools — never invent this]
  Type:               [quick win / content gap / long-tail / emerging / competitor]
  Existing content:   [relevant URL on the site, or "none"]
  Action:             [optimize existing page / create new content / add to existing content]
  Business relevance: [high / medium / low — how well it fits the business goals]
  Priority:           [score from the Phase 5 framework]
```

### Phase 4 — How the site stacks up against competitors

Establish where the site is relatively strong or weak against its competition.

Pick 3–5 competitors and include both kinds: direct business competitors, and search competitors — sites ranking for the same keywords even when they don't chase the same customers. The user names the business competitors; the SEO tools reveal the search competitors.

Compare the site with each of them on:

| What you compare | Metrics | Source |
|---|---|---|
| Domain strength | Domain rating, domain authority, or the tool's equivalent | SEO tools |
| Keyword overlap | Share of keywords in common; keywords unique to each competitor | SEO tools |
| Content volume | Count of indexed pages; how often new content ships | SEO tools or manual check |
| Backlink profile | Total referring domains, spread of link quality, link velocity | SEO tools |
| SERP features | Featured snippets, knowledge panels, image and video results | SEO tools or manual searches |
| Content depth | Average length; how broadly topics are covered | SEO tools or manual assessment |

Write up each competitor like this:

```
COMPETITOR: [name / domain]
  Relationship: [direct competitor / search competitor / both]

  Where they beat us:
  - [Dimension]: [specific evidence from the data]
  - [Dimension]: [...]

  Where we beat them:
  - [Dimension]: [specific evidence from the data]
  - [Dimension]: [...]

  Content they have and we don't:
  - [Topic / keyword]: [their URL, ranking, estimated traffic]

  What to do about it:
  - [Specific action backed by data]
```

### Phase 5 — Scored action plan

Combine everything from Phases 1–4 into a single prioritized plan. Give each recommendation a score from 1 to 3 on three dimensions:

- **Impact** — 1: marginal gain in traffic or rankings · 2: moderate improvement for target keywords · 3: significant effect on traffic, rankings, or conversions
- **Effort** (easier earns more) — 1: significant development or content work · 2: moderate, days rather than weeks · 3: quick fix, hours rather than days
- **Confidence** — 1: hypothesis with little data behind it · 2: directional, partly backed by data · 3: strong evidence in the data

Multiply the three: **Priority = Impact × Effort × Confidence**, with 27 as the maximum. Do the highest-scoring actions first.

```
RECOMMENDATION [N]
  Finding:        [what the audit uncovered]
  From phase:     [Technical / Content / Keyword / Competitor]
  Action:         [specific, actionable step]
  Impact:         [1–3] — [reasoning]
  Effort:         [1–3] — [reasoning]
  Confidence:     [1–3] — [reasoning]
  Priority score: [the product of the three]
  Owner:          [who carries it out — SEO, content, engineering]
  Timeline:       [suggested timeframe]
```

## Deliverable: the audit report

Pull the phases together into this document:

```
# SEO health audit for [Domain]
Date: [date]
Data period: [date range analyzed]
Auditor: [name]

## The short version
  [3–5 sentences: overall SEO health, the three biggest opportunities, the three biggest risks]

## Technical state of the site
  Critical issues: [count]
  High-priority issues: [count]
  [Technical findings, most severe first]

## How existing pages perform
  Pages audited: [count]
  Performing: [count] | Underperforming: [count] | Thin/remove: [count]
  [Most important content findings]

## Keywords worth pursuing
  Quick wins: [count]
  Content gaps: [count]
  [Leading opportunities, highest priority first]

## Versus the competition
  [Main competitor insights and gaps]

## Action plan, ranked by priority score
  [Top 10–15 recommendations, ordered by priority score]

## Supporting data
  [Detailed data tables, complete keyword lists, technical crawl details]
```

## Ground rules

- Never produce SEO metric values yourself. Search volume, keyword difficulty, domain authority, traffic estimates, and CTR by position must all come from the user's tools.
- Never promise better rankings or more traffic. SEO outcomes hinge on many factors nobody controls.
- Never call a keyword "high volume", "low competition", or anything similar unless the user's tool data supports it.
- Tag your output so its origin is visible: `[From SEO data]` for figures pulled from tools, `[Framework methodology]` for this skill's approach, `[AI analysis]` for your own synthesis, and `[Data needed]` for placeholders that still need real data.
