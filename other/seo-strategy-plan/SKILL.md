---
name: seo-strategy-plan
description: Build a 90-day SEO plan for one specific business that diagnoses the site's stage, puts money pages first, sets content pillars from real customer problems, lists what to skip, and fits the hours you have. Use for "make me an SEO plan", "SEO strategy for my startup", "what should I do for SEO first".
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/seo-strategy-plan
---

# SEO strategy plan

Builds a 90-day SEO plan for one specific business. It works out what stage
the site is at, which pages to build or fix first, which customer problems to
own as content pillars and what to leave alone for now, then schedules the
work week by week against the hours and people actually available. It hands
back a plan with owners, a measurement baseline and a one-paragraph "why this
order".

> **Romeo's rule:** Build the pages people read right before they pay you
> first; the thought-leadership essays can wait until somebody is reading.

## Use this when

- You have a site (or launch soon) and need to know what to do about SEO in
  the next three months, and in what order.
- You have a few hours a week and a list of fifty SEO to-dos, and need to
  know which five matter.
- Traffic exists but doesn't turn into signups, calls or sales.
- You're about to hire a writer, freelancer or agency and want a plan to hold
  them to.
- You've run `site-content-inventory` and want it turned into priorities.

## Don't use this for

- Not sure SEO is even the right first job → `seo-start-here`
- Finding and scoring individual keywords → `seo-opportunity-research`
- Working out why traffic dropped → `seo-performance-audit`
- A full crawl-and-index audit → `technical-seo-audit` (this skill only
  checks the baseline)

## What you need

### Required
- What you sell, to whom, and how people buy (self-serve signup, demo,
  quote, phone call, checkout, walk-in).
- Price points and rough margin or customer lifetime value. A page that earns
  $5 a sale needs far more visitors than one that earns $500.
- Customer problems in their own words: sales notes, support tickets,
  reviews, onboarding answers.
- The site URL and its current state, or `site-content-inventory` output.
- Resources: hours per week, who writes, whether anyone can change templates
  or code, any budget for writers or tools.
- Two to five competitors that customers actually compare you with.
- The goal in business terms (demos, trials, orders, calls) and by when.

### Helpful
- Search Console access or exports: Performance (16 months, queries and
  pages) and Page indexing.
- Analytics with conversions set up (GA4 key events or similar), or CRM
  "how did you hear about us" data.
- Bing Webmaster Tools, including its AI Performance report.
- Keyword exports (Ahrefs, Semrush or similar); launches or price changes
  planned in the next 90 days.

### No tools?
Run it with a browser and the owner's knowledge. Open `/robots.txt`,
`/sitemap.xml` and view-source on the homepage and one key page. Read each
competitor's navigation, footer and sitemap to see which comparison, use-case
and integration pages they bothered to build. Use Google autocomplete,
"People also ask" and customer emails as demand evidence, labelled
`inferred`. Without volume data, rank pages by business value and evidence of
demand, never by guessed numbers. If Search Console isn't set up, that is
task one: it's free and it's the only source of Google's own data about the
site.

## Ground rules

- **Stage decides the plan.** A new site has nothing to optimise yet; it needs
  pages that deserve to exist and get indexed. An established site's quickest
  wins usually sit in pages it already has. Running one plan on the other
  wastes the quarter.
- **Money pages before traffic pages** on new and small sites: product and
  feature pages, use-case pages, integrations, comparisons, "alternatives"
  pages. Small search volume, high intent, winnable without much authority,
  and they convert. Broad "what is X" articles come once there's something for
  them to link to.
- **Pillars come from customer problems, not keyword tools.** A pillar is a
  problem the product solves that people search around. If a pillar doesn't
  connect to something you sell, it's a hobby.
- **Price shapes the page set.** A $20-a-month self-serve tool needs many
  low-friction pages and an obvious signup path. A $50k-a-year contract needs
  fewer, deeper pages a buying committee reads: security, integrations,
  pricing logic, case studies.
- **The technical baseline is a gate, not a project.** Crawlable, indexable,
  in a sitemap, one canonical version of the site. Then stop. A deep audit of
  a 20-page site is procrastination with a spreadsheet.
- **Plan to the hours, with a buffer.** Book at most 80% of stated capacity.
  Planning assumptions, overridden by the user's own numbers: a solid new page
  4 to 8 hours, a refresh 1 to 3, a comparison page with screenshots 6 to 10.
- **Say no on purpose.** Every plan has a "not yet" list, each item with the
  trigger that would make it worth doing.
- **Measure in order:** indexed pages, then impressions, then clicks, then
  conversions. A new site is judged on the first two in month one, not on
  revenue. No ranking promises, no traffic forecasts dressed up as facts.
- **AI answers are the same job.** Google says AI Overviews and AI Mode need
  nothing beyond normal SEO; ChatGPT, Perplexity and Copilot tend to cite pages
  that state specific facts plainly. Track AI visibility; don't build a
  separate "AI strategy" inside a 90-day plan.
- **A task has an owner and a finish line.** "Work on SEO" is not a task.
  "Publish the Acme comparison, owner Sam, done when live, in the sitemap and
  linked from /pricing" is.

## Steps

1. **Write the business profile.** Five lines: what you sell, to whom, price
   and margin, how people buy, the one conversion that counts.
   - Missing price or margin: ask. It decides whether a small page earns a day.
   - Months-long sales cycle: set 90-day goals on demos or trials, not revenue.
2. **Diagnose the stage.** Pick one and show the evidence:
   - New: under about 6 months of Search Console data, few pages indexed, most
     impressions on the brand name.
   - Growing: non-branded impressions on a handful of pages, little else.
   - Established: 12+ months of data, non-branded impressions on many pages.
   - Recovering: a sharp drop in the last 6 months → `seo-performance-audit`.
   - Split branded from non-branded with Search Console's branded queries
     filter where offered (not for low-volume sites or path and subdomain
     properties); otherwise a regex on the brand name and its misspellings.
3. **Check the technical baseline.** Quick checks only; anything failing is
   `Fix now` in week one:
   - Key pages return 200, carry no `noindex`, and have a self-referencing
     canonical.
   - One version of the site: http and www (or non-www) variants 301 to the
     single preferred host.
   - `robots.txt` doesn't block important paths; an XML sitemap exists and is
     submitted in Search Console.
   - Main content is in the HTML, or visible in URL Inspection's crawled page,
     not stuck behind client-side JavaScript.
   - Page indexing report: indexed count against "Crawled - currently not
     indexed" and "Discovered - currently not indexed".
   - Anything bigger becomes a scheduled `technical-seo-audit` run. Chasing
     lab speed scores when field Core Web Vitals are "good": `Leave it`.
4. **Map the money pages.** Which bottom-of-funnel pages exist, which are
   missing, and which competitors have built:
   - One page per feature or job people search for ("invoice reminder
     software"), not one page listing every feature.
   - Use-case, industry or role pages only where the product or the pitch
     genuinely differs for that group.
   - Integration pages only for integrations that exist.
   - "You vs competitor", "competitor alternatives" and "best X for Y" pages
     for the competitors customers mention (→ `comparison-page-writer`).
   - A pricing page that answers price questions in text.
   - Local business: service pages, and area pages only for areas served
     (→ `local-seo-audit`). Shop: category pages before blog posts
     (→ `ecommerce-seo-audit`).
   - Rate each page: business value, demand evidence (labelled), effort, and
     who ranks now. Forums and small sites on page one = winnable; ten big
     brands = later.
5. **Derive two to four pillars.** From tickets, sales notes, reviews of you
   and competitors, community threads and "People also ask":
   - For each: the problem in customer words, the money page it feeds, a hub
     topic and 5 to 10 supporting questions.
   - Test: is a reader one step closer to needing the product? If not, cut it.
   - Grouping the questions into pages by shared results → `topic-cluster-map`.
6. **Established sites: harvest before you build.** From Search Console:
   - Average position roughly 5 to 20 with steady impressions → refresh
     (`on-page-seo-review`, `search-intent-match`).
   - Many impressions, low CTR for the position → `title-meta-ctr`.
   - Two pages swapping places for one query → `keyword-cannibalization-check`.
   - Clicks down year on year → refresh or merge. No impressions in 12 months,
     no links, no conversions → improve, merge or remove, page by page.
7. **Write the "not yet" list.** Typical entries, each with its trigger:
   - Link-building outreach: once there are pages worth linking to.
   - Programmatic pages: only with a repeatable query pattern and unique data
     per page (→ `programmatic-seo-plan`).
   - New languages or countries: once the home market converts.
   - Head terms owned by big publishers, daily news posts, a 200-term
     glossary, a redesign.
   - llms.txt and other "AI files": Google says its AI features don't need
     them. `Leave it` unless there's a concrete agent use case
     (→ `ai-agent-readiness`).
8. **Set the measurement baseline on day one.** No baseline, no proof.
   - Leading, weekly: indexed pages (Page indexing, filtered to the sitemap),
     non-branded impressions, number of queries with impressions, new pages
     getting their first impressions.
   - Lagging, monthly: non-branded clicks, organic signups, demos or orders,
     revenue from organic landings or CRM source.
   - AI visibility, monthly: a fixed list of 10 to 20 questions customers ask,
     run in ChatGPT, Perplexity, Google AI Mode and Copilot; log cited,
     mentioned or absent. Bing Webmaster Tools' AI Performance report (public
     preview since February 2026) counts citations in Copilot and Bing AI
     answers. Search Console's generative AI performance report (all sites
     since August 2026, once they have enough AI impressions) shows
     impressions in AI Overviews and AI Mode by page, country and device; that
     data is part of the Performance report's "Web" totals, not extra to
     them. Referrals from chatgpt.com,
     perplexity.ai and similar show up in analytics.
   - Targets are directions ("non-branded impressions rising"), not promises.
9. **Build the calendar.** Fill the weeks from the priority list:
   - Month 1: Search Console and baseline, `Fix now` items, the first two or
     three money pages.
   - Month 2: more money pages, the first pillar hub, links from the homepage
     and navigation to the new pages.
   - Month 3: supporting articles, refreshes based on first data, a review of
     what moved and what changes for the next 90 days.
   - Every line: task, owner, hours, done-when, dependency. Weekly hours at or
     under 80% of capacity.
10. **Write "why this order", then reread as a skeptic.** One paragraph in
    plain English, tied to this business's prices, stage and hours. Check that
    every task traces to the goal, no number is invented, the hours add up,
    and the "not yet" list exists.

## What to hand back

Return the plan in this shape. Every line should be something a person can
act on this week.

```markdown
**What I found:** <stage and one-line state of the site, with evidence label>
**What matters most:** <the page type or fix that moves the goal>
**What to do first:** <week-1 task, owner, done-when>

## Business profile
- Sells: <...> | Buyers: <...> | Price and margin: <...> | Buys via: <...>
- Conversion that counts: <...> | Goal: <...> by <date>

## Stage
- <New / Growing / Established / Recovering>: <evidence> (<seen/tool/inferred>, <confidence>)

## Priorities
1. `Fix now` <task>: <why> (<evidence label>, <confidence>)
2. `Fix next` <task>: <why> (<evidence label>, <confidence>)
3. `Worth doing` <task>: <why>
- `Leave it` <thing that looks urgent but isn't>: <why>

## Content pillars
- <Pillar>: <customer problem> → feeds <money page> → hub + <n> supporting questions

## Not yet
- <Item>: <why not now>. Revisit when <trigger>.

## Plan by week
### Month 1 (weeks 1-4), Month 2 (weeks 5-8), Month 3 (weeks 9-13)
- Week 1: <task> | <owner> | <hours> | done when <...>

## Measurement
- <Metric> (leading / lagging / AI): baseline <value or "not checked"> on <date> | source | check weekly or monthly

## Why this order
<One paragraph.>

## What I could not check
- <Item>: <what would verify it>
```

## Stop and flag if

- You don't know how the business makes money or which conversion counts.
  Ask; a plan built around traffic alone is the wrong plan.
- The stated hours can't cover even the `Fix now` items. Hand back the
  reduced plan and say plainly what was cut.
- There are signs of a manual action, mass deindexing or a recent sharp drop.
  Route to `seo-performance-audit` or `technical-seo-audit` first.
- A domain, URL or platform move is planned inside the 90 days. Plan around
  `site-migration-check`, not over it.
- The goal is a ranking or a date guarantee. Decline the promise; offer
  leading indicators instead.
- Health, finance, legal or safety topics: flag the need for qualified
  authors and schedule `eeat-trust-review` early.
- The output is unacceptable if it invents search volumes or traffic, has
  tasks without owners, exceeds the stated hours, or has no "not yet" list.

## Next step

- `seo-opportunity-research` with the money-page list and pillars, to confirm
  demand and pick the first ten pages.
- `comparison-page-writer` or `seo-content-brief` for the first week-two page.
- `seo-change-monitor` to snapshot the baseline before anything changes.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
