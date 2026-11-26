---
name: on-page-seo-review
description: Review one URL against its target query and hand back exact Before → After edits for the title, headings, opening, content gaps, links, images, schema and CTA. Use for "review this page for SEO", "why isn't this page ranking for X", "on-page audit", "optimize this blog post".
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/on-page-seo-review
---

# On-page SEO review

Take one URL and the one query it should rank for, compare the page with what Google ranks for that query today, and hand back a prioritised list of exact edits: what the page says now, what it should say instead, why, and how urgent. Every finding is a change someone can paste, not a principle they have to interpret.

> **Romeo's rule:** If you can't write the "After", you haven't found a problem, you've found an opinion.

## Use this when

- A page gets impressions for its target query but sits around positions 5 to 20, and you want to know what to change on the page itself.
- A page is due a refresh and you want a precise edit list before anyone starts rewriting it.
- A page has been indexed for a while and doesn't rank for the query it was written for.
- Someone asks "what's wrong with this page?" and one URL needs a proper review rather than a sitewide skim.
- A product, service or landing page gets search traffic that doesn't convert.

## Don't use this for

- Deciding whether the page is the wrong kind of page altogether (guide vs product page vs list) → `search-intent-match`.
- Sitewide crawling, indexing, rendering or speed problems → `technical-seo-audit`.
- Rewriting titles and meta descriptions across many pages for click-through → `title-meta-ctr`.
- Two of your own pages competing for the same query → `keyword-cannibalization-check`.

## What you need

### Required

- The URL, or the full HTML or text if the page isn't public yet.
- One primary target query, plus up to 5 close variants. If the user doesn't know it, take the query with the most impressions for this page in Search Console and confirm it with them before you start.
- The target market: country and language.

### Helpful

- Search Console data for the page: queries, clicks, impressions, CTR and average position for the last 3 months (Performance report, filter Page = URL, Queries tab).
- The top 5 organic results for the query in the target country, as URLs, saved copies or screenshots.
- Internal links pointing at the page: a crawler export, or Search Console → Links → Internal links.
- The page's conversion goal (sign-up, demo, purchase, call, enquiry) and its conversion data.
- Product facts, prices and brand voice rules, so the After copy is accurate.
- Field data for the URL from PageSpeed Insights or the Chrome UX Report.

### No tools?

All of this works with a browser. Open view-source:URL (or ask for pasted HTML) to read the `<title>`, meta description, canonical, robots meta, headings and JSON-LD. Search the query in a private window set to the target country, or ask for screenshots, to see the ranking pages and SERP features. Search Console's free Performance report and URL Inspection give queries, index status and the rendered HTML; PageSpeed Insights gives field data; the Rich Results Test checks structured data. Anything you couldn't see is "not checked", never guessed.

## Ground rules

- One page, one primary query. If the page is trying to serve two different intents, that is the finding; don't review it twice.
- Compare against what ranks now in the target market, not against a generic checklist. A gap is a subtopic, question, data point, format or proof that most top results give the reader and this page doesn't. Never a word count, never a keyword density.
- The first screen decides. The direct answer, verdict or offer should be visible, or clearly starting, without scrolling past a hero image, a table of contents and three paragraphs of scene-setting.
- Protect what already works. On a page ranking top 3 for its query, edits to the title, H1, URL and opening paragraph carry ranking risk; label them and prefer additive edits (a new section, a better example, a corrected fact).
- Write the After in the site's voice using only facts you have. If a fix needs a price, date, statistic or claim you don't have, write it with a placeholder such as `[confirm: current price]` and say who must fill it.
- The query belongs in the title and H1 in natural form. Repeating it in every heading and alt attribute is a weakness, not optimisation.
- Indexability comes first. A page that is noindexed, canonicalised elsewhere, blocked or not returning 200 can't rank; report that and stop the copy review until it's fixed.
- Use `Leave it` honestly. A 170-character meta description, a skipped heading level or a slightly long URL rarely deserves anyone's afternoon.

## Steps

1. **Confirm the page can rank at all.**
   - Status 200, no redirect chain, not a soft 404. No `noindex` in `<meta name="robots">` or the `X-Robots-Tag` header. robots.txt doesn't block the URL.
   - `<link rel="canonical">` is absolute and points to this URL (same protocol, host, trailing-slash form, no tracking parameters), or deliberately to a preferred version. Canonical to a different page means this page won't rank: `Fix now` unless intended.
   - If URL Inspection is available: "URL is on Google" and Google-selected canonical equals user-declared canonical. If they differ, Google prefers another URL: `Fix now`, and route to `technical-seo-audit`.
   - Main content is in the rendered HTML, not only after a click or a client-side fetch. Compare view-source with the rendered DOM or URL Inspection's crawled page.
2. **Sanity-check intent (five minutes, not an essay).**
   - From the top 5 results, note the dominant page type (guide, list, product, category, tool, comparison, local page), angle (beginner, cheapest, for a role, current year) and format (steps, table, calculator, video).
   - If this page is a different type from nearly all of them, record it as `Fix now` and hand off to `search-intent-match`. A better title won't fix a format mismatch.
   - If it matches, write down the 2 or 3 things every top result gives the reader. Those anchor the gap check in step 7.
3. **Title.**
   - Unique on the site: check the crawl export, or search `site:example.com "exact title"`. Shared with one or two other pages = `Fix next`; a template producing duplicates sitewide = `Fix now`.
   - The primary query, in natural form, sits in roughly the first 40 characters so truncation never removes it.
   - Truncation: Google sets no character limit and cuts by pixel width per device; about 50 to 60 characters is a working guide for desktop. A title that's cut but still makes sense is `Leave it`.
   - Gives a reason to click: outcome, format or differentiator. A year or a number only if true (the page really was updated that year; the list really has that many items).
   - Brand once, short, at the end. "Home | Brand | Brand Ltd" is boilerplate.
   - Search the query and compare the displayed title with the `<title>`. If Google rewrote it, the usual causes are a long, boilerplate or keyword-stuffed title, or one that doesn't match the H1. Note which.
4. **H1 and heading outline.**
   - Exactly one visible H1 on the same topic as the title (wording can differ). Missing, hidden, or the logo wrapped in an H1 = `Fix next`.
   - Extract the H1 to H3 outline. It should read like a table of contents for the answer. Descriptive headings ("How much does a website audit cost?") beat clever ones ("The bottom line").
   - Headings used only for styling (a "Subscribe" H2 in every sidebar) = `Worth doing`. Skipped levels = `Leave it` unless they break the outline's meaning.
5. **Meta description.**
   - Present, unique, specific to this page, includes the query naturally (Google bolds matching words) and states what the reader gets. Around 120 to 155 characters avoids truncation on most devices; that is a guide, not a rule.
   - Google often shows page text instead of the meta description. Still write one: it's the fallback and social platforms reuse it when `og:description` is missing.
   - Missing on a key page = `Fix next`. Slightly long = `Leave it`.
6. **First screen.**
   - Check at phone width (about 390 px). What is visible before scrolling?
   - Informational page: a 2 to 4 sentence direct answer under the H1. How-to: steps start early. Best-of or comparison: shortlist or verdict early. Product or service: what it is, who it's for, a price or "from" price, and the primary CTA.
   - Blockers: a hero image filling the screen, stacked cookie banner and newsletter popup, a long personal intro, a table of contents before any answer. A popup covering the main content on mobile right after arriving from search (intrusive interstitial) = `Fix next`.
7. **Content gaps against the ranking pages.**
   - For each top result, list the sections and questions it answers, the data and examples it uses, its media (table, calculator, video, screenshots) and its proof (named author, testing, sources).
   - A gap is something at least 3 of the 5 cover, that this page doesn't, and that the reader needs. Padding sections and keyword variants are not gaps.
   - Strong gap evidence: "People also ask" questions, and queries in this page's own Search Console data that the page has no section for.
   - If an AI Overview shows for the query, note what it already answers and which pages it cites. A page that only restates that summary gives nobody a reason to click; the edits should add what the summary can't (specifics, examples, tools, judgement).
   - Note information gain: what this site can add that none of them have (its own data, real screenshots, a worked example, prices paid, a mistake it made). These are usually the highest-value edits.
8. **Freshness and dated facts.**
   - Find every year, price, version number, statistic, screenshot of a product UI, legal reference and word like "currently", "new" or "this year". Check each against today's date and its source.
   - Compare the visible "Updated" date, `dateModified` in JSON-LD and what actually changed. Don't recommend bumping a date without a substantive update.
   - A stale fact on a money, health or legal topic = `Fix now`; elsewhere `Fix next`.
9. **Internal links in.**
   - Count the internal pages linking here, where from (navigation, hub pages, related posts, body copy) and with what anchor text.
   - Orphaned, or linked only from paginated archives = `Fix next`. Propose 3 to 5 specific source pages, each with the anchor and the sentence it sits in. A larger plan → `internal-linking-plan`.
   - Anchors should describe the destination and vary naturally. "Click here" and "read more" = `Worth doing`.
10. **Links out.**
    - The next step (product, pricing, the related guide) is linked in context, not only in the footer.
    - Broken links (4xx, 5xx), links to redirected URLs (point them at the final URL) and links to noindexed pages.
    - Claims cite primary sources. Paid or affiliate links carry `rel="sponsored"`, user-generated links `rel="ugc"`. Unqualified paid or affiliate links = `Fix next`; Google's link spam policies ask for `sponsored` or `nofollow` on them.
11. **Images and media.**
    - Content images are `<img>` elements with descriptive alt text, explicit `width` and `height`, and the main above-the-fold image is not `loading="lazy"`.
    - Does the query call for media the top results have (screenshots, diagram, comparison table, video)? Original images beat stock photos. A full image review → `image-seo`.
12. **Structured data.**
    - Find JSON-LD (`application/ld+json`), Microdata (`itemscope`) or RDFa (`typeof`). Run the Rich Results Test on the URL. Check the values match what's visible (author, dates, price, rating).
    - Expected types: Article or BlogPosting with author and dates on editorial pages; Product with Offer on product pages; BreadcrumbList where breadcrumbs are shown; Organization on the home or about page.
    - Don't recommend FAQPage or HowTo markup for rich results: HowTo rich results were removed in 2023, and FAQ rich results were limited to government and health sites in 2023, then retired entirely in May 2026 (per Google's Search Central changelog). Existing markup is harmless: `Leave it`. Writing new markup → `schema-markup`.
13. **URL.**
    - Short, lowercase, hyphenated, readable, contains the main term. An ugly URL that ranks = `Leave it`: changing it means a 301 and a period of instability.
    - A dated slug (`/best-crm-2023/`) on an evergreen page: usually keep the URL and update the content (`Leave it`). Change it only when the page has little to lose, with a 301 and updated internal links (`Worth doing`, with a risk note).
14. **Page experience basics.**
    - Field data at the 75th percentile: LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1. Say whether it's URL-level or origin-level data. Lab-only scores are `tool` evidence with low confidence for ranking impact.
    - Mobile readability (text size, tap targets, no sideways scrolling), HTTPS with no mixed content.
    - Treat this as a tie-breaker: a failing metric is usually `Fix next`, and a fast page with a weaker answer still loses.
15. **Conversion path and CTA.**
    - What should this searcher do next? Commercial pages: CTA in the first screen. Informational pages: CTA after the answer, repeated near the end.
    - Match the ask to the stage: informational readers get a soft next step (template, free tool, related guide); commercial readers get trial, demo, quote or buy.
    - Trust beside the CTA: clear price, real reviews, guarantee, delivery and returns. Missing or vague = `Fix next` on money pages.
16. **Write the edits.**
    - Each edit: element, Before (exact current text, or "missing"), After (exact replacement), Why (one plain sentence tied to evidence), priority, evidence label and confidence.
    - Order by priority, then expected impact. Keep the main list to about 15 edits; put smaller items in a short `Worth doing` list.

## What to hand back

Fill in this template. Quote Before text exactly as it appears on the page.

```markdown
# On-page review: <URL> for "<target query>" (<country, language>, <date>)

**What I found:** <one plain-English sentence>
**What matters most:** <one sentence>
**What to do first:** <one sentence>

## Snapshot
- Indexable: yes / no (<reason>) · Canonical: self / <other URL> · Status: <code>
- Search performance: <clicks, impressions, CTR, avg position, date range> or "not checked"
- Intent match: matches / partial / mismatch (→ `search-intent-match`)
- SERP features on the query: <AI Overview, People also ask, video, shopping, local pack> or "not checked"
- Pages compared: <URLs>

## Edits

### 1. <Element, e.g. Title> · `Fix now`
- Before → After: "<exact current text or 'missing'>" → "<exact replacement>"
- Why: <plain-English reason tied to the evidence>
- Evidence: seen / tool / inferred · confidence: high / medium / low
- Risk: <only if the page ranks top 3 or the edit touches title, H1 or URL>

### 2. ...

## Sections to add
- "<Heading as it should appear>": <what it must cover, which source or own data to use, a 1 to 2 sentence starter> · <priority>

## Internal links to add
- From <source URL>: anchor "<text>" in the sentence "<sentence>" · <priority>

## Leave it
- <thing that looks wrong>: <why it isn't worth changing>

## What I could not check
- <item>: <what would verify it>
```

## Stop and flag if

- The page is noindexed, canonicalised to another URL, redirected or returning an error. Report that alone and route to `technical-seo-audit`.
- There is no target query and no Search Console data to infer one. Ask; reviewing against a guessed query wastes the whole review.
- The intent check shows a different page type ranks. Hand off to `search-intent-match` rather than polishing the wrong page.
- You couldn't see the ranking pages. Say gaps are `inferred`, low confidence, and list what you'd need.
- An After needs facts you don't have, or makes health, money or legal claims. Use placeholders and name who must confirm; never invent.
- The output contains generic advice ("improve content quality", "add more keywords"), word-count or density targets, or an edit without exact Before text. That output is not acceptable; rewrite it.
- You're asked to apply edits to the live page or CMS. Draft them; change nothing without explicit permission for that change.

## Next step

- Intent mismatch → `search-intent-match` with the URL, the query and the top 5 results you collected.
- Big content gaps → `seo-content-brief` as a refresh brief, passing the "Sections to add" list and the information-gain notes.
- Before shipping the edits → `seo-change-monitor` to snapshot the page, then compare 28 days after Google recrawls it.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
