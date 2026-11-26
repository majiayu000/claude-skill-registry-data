---
name: programmatic-seo-plan
description: Plan template pages at scale (integrations, locations, use cases, data pages) only where real search demand meets unique data for every page, with quality gates, URL and hub structure, batch rollout and spam-policy checks. Use for "programmatic SEO", "generate pages from my database", "why are my template pages not indexed".
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/programmatic-seo-plan
---

# Programmatic SEO plan

Decides whether template pages at scale make sense for this site and, if they
do, plans them: the query pattern, the data that makes each page different,
the template, the quality gate that decides which pages get indexed, URLs and
hubs, internal links, and a rollout in batches watched in Search Console. It
hands back a go / pilot / no-go call, a page plan, a quality-gate checklist
and a rollout schedule.

> **Romeo's rule:** If you can't say what page 4,000 tells a reader that page
> 3,999 doesn't, don't publish page 4,000.

## Use this when

- A search pattern repeats with one changing part: "[app] integration",
  "[job] salary in [city]", "[tool] for [industry]", "[A] to [B] converter".
- You have a dataset (integrations, listings, locations, prices, specs,
  statistics) and want pages built from it.
- Template pages are already live and many sit in "Crawled - currently not
  indexed" or "Discovered - currently not indexed".
- Someone has proposed "5,000 AI pages" and you need a sober go or no-go.

## Don't use this for

- Finding the keywords in the first place → `seo-opportunity-research`
- Hand-written "vs" and "alternatives" pages → `comparison-page-writer`
- Shop product and category templates, faceted navigation → `ecommerce-seo-audit`
- Service-area or city pages for a local business → `local-seo-audit`

## What you need

### Required
- The proposed pattern and what a visitor should do on the page (sign up,
  contact, compare, buy).
- The data: fields, row count, completeness, update frequency, who owns it,
  and whether you have the right to publish it.
- The platform and who can build templates; whether `noindex` and sitemap
  inclusion can be set per page.
- Search Console access for the rollout, or a commitment to set it up.

### Helpful
- Keyword exports for the pattern with demand per modifier, even rough.
- A random sample of 20 data rows (random, not the best 20).
- Existing template pages and their Page indexing status, or a crawler export
  (Screaming Frog, Sitebulb).
- Competitor examples that rank for the pattern.

### No tools?
Type the pattern into Google with ten different modifiers. If autocomplete
suggests them and the results are pages of that same pattern (competitors'
templates, directories), demand and format are real. Open the data as a
spreadsheet and add a column counting the filled, page-specific fields per
row; that column is your quality gate. After launch, the free Search Console
Page indexing report, filtered to the batch's sitemap, is the number that
matters.

## Ground rules

- **Two conditions, both required:** a repeatable pattern with real demand
  across many modifiers, and unique, useful data for every page. Demand
  without data makes thin pages; data without demand makes pages nobody
  visits. Fail either one and it's a no-go.
- **Google judges the pages, not the method.** Its scaled content abuse policy
  covers many pages made mainly to manipulate rankings that add little value,
  "no matter how it's created". Templates and AI aren't the problem;
  unoriginal pages at scale are. Its doorway abuse policy covers near-identical
  city or region pages that funnel visitors to one place.
- **Uniqueness lives in the data, not the wording.** Swapping the city name,
  or having an LLM rephrase one paragraph 3,000 times, adds nothing. Each page
  needs facts only it has: counts, prices, lists, dates, specs, reviews, steps,
  or comparisons computed from the data.
- **Index only what passes the gate.** Below the gate, don't generate the page,
  or keep it for users with `noindex` and out of the sitemap. Never index an
  empty state ("0 results", "no listings yet", "coming soon"). Don't block
  noindexed pages in `robots.txt`: Google has to crawl them to see the
  `noindex`.
- **Prove it small, then scale.** The first batch is 50 to 200 of the
  strongest pages. A young site that publishes 10,000 URLs at once tends to
  collect "Discovered - currently not indexed".
- **Hubs are real pages.** Category pages that list their children with
  useful summaries are how crawlers and people find the leaves. A sitemap of
  10,000 URLs with no internal links is not a structure.
- **One URL per intent.** Modifiers that mean the same thing (NYC, New York
  City) share one page. Don't generate combinations nobody searches: 50 tools
  × 50 tools × 20 industries is 50,000 pages and almost no demand.
- **Freshness must be real.** When the data changes, the page changes and
  `lastmod` says so. Google only uses `lastmod` that is consistently accurate.
- **The template multiplies everything.** One fix improves 5,000 pages; one
  bug breaks 5,000. Test it on the worst rows, not the best.
- **Only build what you can maintain.** Stale data across 3,000 pages is
  worse than no pages.

## Steps

1. **Run the fit test.** Answer each with evidence and a label:
   - Pattern: do results for ten modifiers show pages of this same pattern?
   - Demand spread: dozens of modifiers with some demand, not one head term
     plus noise? Volume counts as `tool` only if an export was given.
   - Data: across 20 random rows, does each have enough page-specific fields
     to pass a gate?
   - Value: would the searcher's job be done better here than on today's top
     result?
   - Rights and upkeep: can you publish this data and keep it current?
   - Verdict: Go, Pilot (one small batch) or No-go. For No-go, offer the
     better option: a few hand-written pages, one tool or calculator page, or
     a single hub.
2. **Map the pattern.** Head term × modifier sets (locations, integrations,
   industries, roles, sizes, pairs). For each set: count, demand evidence, and
   the data each page needs. Drop combinations with neither demand nor data.
   Modifiers that change intent ("free", "jobs", "near me", "template") need
   their own template or no page at all.
3. **Define what makes each page different.** Per page type:
   - Required unique fields, and optional ones.
   - Computed insights: rank within the parent, difference from the average,
     nearest alternatives.
   - What the visitor can do: filter, compare, contact, start a trial.
   - Shared boilerplate kept short and below the unique content.
   - One sentence: "This page is the only place that tells you <...>."
4. **Design the template.**
   - The top of the page answers the query from the data (the price, the
     count, the setup steps), not an intro.
   - Sections render only when their data exists; no walls of "N/A".
   - Title and H1 carry the modifier; variety comes from real data (counts,
     dates), not spun synonyms.
   - Generated prose, if any, is written from that page's facts and
     spot-checked; never LLM text with no data behind it.
   - Self-referencing canonical, and a per-page index switch driven by the
     gate.
   - Main content in server-rendered HTML, not fetched by JavaScript after
     load.
   - Structured data only for what's visible (→ `schema-markup`).
5. **Set the quality gate** as rules a developer can code:
   - Minimum page-specific data points, the primary fact present, at least one
     item where the page is a list.
   - Near-duplicate check: compare main content across a sample; pairs that
     differ only by name get merged.
   - Outcome per page: indexable and in the sitemap / built with `noindex` /
     not built.
   - Re-run on every data refresh. Pages that fall below get `noindex`; pages
     whose subject is gone return 404 or 410, or 301 to the parent if it
     serves the same need.
6. **Plan URLs and hubs.** Short, readable, stable, lowercase, hyphenated:
   `/integrations/slack/`, `/salaries/data-analyst/leeds/`. No IDs or
   parameters on indexable URLs; one trailing-slash policy. Home → hub →
   optional sub-hub → leaf, every leaf within three or four clicks. Paginate
   hubs with plain `<a href>` links, not infinite scroll alone. Hub filters
   stay unindexed unless a filter combination is itself a demanded pattern.
7. **Plan internal links.** Hubs link to every child (paginated). Leaves link
   up to their hub and across to 3 to 8 siblings chosen by the data (nearest
   city, similar integration). Money pages link to the top hubs; editorial
   articles link to the strongest leaves. Breadcrumbs on every leaf. No giant
   footer link blocks.
8. **Roll out in batches.**
   - Batch 1: 50 to 200 pages with the most data and demand, in their own
     sitemap file, submitted in Search Console. A sitemap file holds at most
     50,000 URLs or 50 MB uncompressed; beyond that, use a sitemap index.
   - Wait until most of the batch has been crawled (Page indexing filtered to
     that sitemap; URL Inspection on a sample). Often weeks, not days.
   - Indexed ratio = indexed ÷ submitted for that sitemap. Read the reasons:
     "Crawled - currently not indexed" often signals Google wasn't convinced
     the pages are worth it; "Discovered - currently not indexed" means it
     hasn't crawled them yet; "Duplicate, Google chose different canonical
     than user" means the pages are too alike.
   - Rule of thumb, not a Google number: if well under half of a crawled batch
     is indexed, stop adding. Raise the gate, enrich the data or merge.
   - Scale in steps (say two to five times the last batch) only while the
     ratio holds and indexed pages start earning impressions.
9. **Check policy risk.** Against Google's spam policies: scaled content
   abuse, doorway abuse, thin affiliation (if pages carry affiliate links) and
   the site reputation policy (if pages are third-party content on your
   domain).
   Rate the plan low, medium or high risk, with the reason.
10. **Plan upkeep.** Data refresh schedule, `lastmod` on real changes, a
    monthly indexed-ratio check, a template regression check after each
    deploy (→ `seo-change-monitor`), and a named owner for all of it.

## What to hand back

Return the decision and plan in this shape:

```markdown
**What I found:** <pattern, demand evidence, data coverage>
**What matters most:** <the gate, and why it's set there>
**What to do first:** <Go / Pilot / No-go, and the first batch or the alternative>

## Decision
- <Go / Pilot / No-go>: <reason> (<seen/tool/inferred>, <confidence>)
- Policy risk: <low / medium / high>: <reason>

## Page plan
- Pattern: <head term> × <modifier set>: <n> possible, <n> pass the gate
- Unique per page: <fields and computed insights>
- URLs: <pattern> | Hub: <URL> | Links: <rule>

## Priorities
1. `Fix now` <e.g. empty-state pages currently indexed>: <evidence>
2. `Fix next` <...>: <evidence>
- `Leave it` <e.g. long-tail combinations with no demand>: <why>

## Quality-gate checklist (every page, before it's indexable)
- [ ] The primary fact for the query is present and current
- [ ] At least <n> page-specific data points, not counting the name
- [ ] Not an empty state, placeholder or "coming soon"
- [ ] Main content differs from its nearest sibling by more than the name
- [ ] The answer is in the HTML, not loaded only by JavaScript
- [ ] Returns 200 with a self-referencing canonical
- [ ] Linked from its hub and from at least three siblings
- [ ] Title, H1 and meta carry the modifier and a real data point
- [ ] Structured data matches visible content
- [ ] Pass → indexable, in the batch sitemap. Fail → `noindex` and out of the sitemap, or not built

## Rollout
- Batch 1: <n> pages | sitemap <file> | submitted <date>
- Review when most of the batch has been crawled
- Scale / fix / stop rules: <rules>

## What I could not check
- <Item>: <what would verify it>
```

Worked example. Illustrative only: the company and every number are
invented.

- Business: "Ledgerly", a bookkeeping app with 240 integrations in its
  database, 140 live and 100 "requested".
- Pattern: "[app] bookkeeping integration", "connect [app] to accounting".
- Unique data per page: sync direction, fields mapped, sync frequency, setup
  steps, plan required, known limits, date last verified, one screenshot.
- Gate: live integration, at least three setup steps, at least five mapped
  fields, a real screenshot.
- Result: 92 pass now and 48 pass after docs work. The 100 requested
  integrations get one section on the hub with a vote button, not pages.
- Batch 1: the 60 passing pages with the most active users, in
  `sitemap-integrations-1.xml`, linked from `/integrations/` by category.
- Rule: add the other 32, then the 48, once batch 1 is mostly indexed and
  earning impressions; otherwise merge thin pages into category sections.

## Stop and flag if

- Either fit condition fails (no repeatable demand, or no unique data per
  page). Say no-go plainly and offer the smaller alternative.
- The plan relies on scraped or licensed data you may not have the right to
  republish.
- The proposal is near-identical city, region or "for [industry]" pages that
  all funnel to one offer: that's doorway territory.
- Live template pages show a manual action, or an indexed ratio that keeps
  falling. Pause new batches and run `technical-seo-audit`.
- Nobody owns data upkeep after launch.
- The output is unacceptable if it plans an index of pages that fail the gate,
  indexes empty states, launches everything at once, or invents demand numbers.

## Next step

- `topic-cluster-map` to place the hubs within the site's existing clusters.
- `internal-linking-plan` with the hub and leaf rules, before batch 1 ships.
- `seo-change-monitor` to snapshot batch 1 and catch template regressions.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
