---
name: keyword-cannibalization-check
description: Find pages on your own site competing for the same search with the same intent, and decide per conflict to merge, differentiate, canonicalize, de-optimize or leave it, with evidence. Use for "are my pages cannibalizing each other", "two pages ranking for the same keyword", or "Google keeps switching which page ranks".
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/keyword-cannibalization-check
---

# Keyword cannibalization check

Find the searches where two or more of your own pages compete for the same query with the same intent, separate real conflicts from harmless overlap, and decide for each one whether to merge, differentiate, canonicalize, de-optimize or leave it. Every decision comes with the Search Console numbers, search-result evidence and per-URL risk checks behind it.

> **Romeo's rule:** Two of your pages on page one is a win; it only becomes a problem when they take turns being mediocre.

## Use this when

- Search Console shows one query sending impressions to two or more of your URLs, and neither ranks well.
- The page Google shows for a keyword keeps switching, and the position wobbles with it.
- You have several posts on nearly the same topic ("best CRM for startups", "top CRMs for small teams") and none of them breaks into the top 5.
- A blog post outranks your product, pricing or category page for a buying query.
- Before a content refresh, pruning project or migration, to decide which pages to combine.

## Don't use this for

- The same page reachable at several URLs (http/https, www, trailing slash, parameters) → `technical-seo-audit`.
- Language or country versions of a page showing in the wrong market → `hreflang-international`.
- Planning new content so it doesn't overlap in the first place → `topic-cluster-map`.
- Explaining a general traffic drop → `seo-performance-audit`.

## What you need

### Required

- Search Console Performance data with query and page on the same row, web search type, at least the last 3 months (16 months if you can, to see the ranking URL change over time). The standard UI export puts queries and pages on separate tabs, which is not enough on its own; see "No tools?" for the free workaround.
- What each URL involved is meant to do (from `site-content-inventory` if it exists, or a sentence per page from the user).

### Helpful

- Query + page + date rows (Search Console API, Looker Studio, or the BigQuery bulk export) to detect the ranking URL flipping week to week.
- External links per URL: Search Console's Links report ("Top linked pages") or an Ahrefs/Semrush export.
- Conversions per landing page (GA4 key events by landing page) and non-search traffic per URL (email, ads, social, partner links).
- Top-10 results for the conflicting queries in the target country, from a SERP API, an SEO tool's SERP export, or screenshots.
- Crawl data per URL: title, H1, canonical, indexability, and the internal anchors pointing at it.

### No tools?

In Search Console, open Performance > Search results, add a Query filter with "Exact query", then open the Pages tab: every URL listed got impressions for that query. Do this for your 20 to 50 most valuable non-brand queries, or reverse it (filter one page, read its Queries tab) for pages you suspect. Use "Compare" on the date filter to see whether the leading URL changed between periods. Search the query yourself in a private window set to the right country to see which of your URLs appear. `site:yourdomain.com keyword` shows candidate pages but says nothing about rankings. GA4's landing-page report covers conversions, and Search Console's Links report covers external links per page.

## Ground rules

- Real cannibalization needs all of: the same query, the same intent, two or more of your URLs getting meaningful impressions, and a cost (neither ranks as well as one strong page would, or the wrong page ranks). Missing any one, it isn't a conflict.
- Not cannibalization: two of your URLs both in the top 5 (Google chose to show both; keep it); different intents on an ambiguous query (a "what is" guide and a pricing page both getting impressions for "crm software"); one URL with about 90% or more of the impressions while another catches stray ones deep in the results; homepage plus product page on brand queries; the same page in different languages.
- Compare URLs at page level. When data is grouped by page, Search Console counts an impression for every one of your URLs shown, so page totals for one query can add up to more than the query's own total. Compare the URLs with each other, not with the query row.
- Search results confirm intent better than titles do. If the queries each page targets return mostly the same top-10 pages, Google treats them as one intent. If they share almost nothing, the pages do different jobs.
- The surviving URL is the one with the external links, conversions and history, not the one with the nicer slug. Check before choosing.
- A merge moves content, then redirects. Carry over what's useful, 301 (or 308) the old URL straight to the survivor, update internal links to point at the survivor directly, and keep the redirect permanently if you can (Google's site-move guidance says at least a year).
- `rel=canonical` is for duplicate or near-duplicate pages. Pointing the canonical of one distinct article at another tends to be ignored by Google; merge or differentiate instead.
- Don't use noindex or robots.txt to pick a winner between two real pages. Noindex removes the page from search entirely, and a robots.txt block stops Google seeing the page's content, including its canonical. A page with no search value of its own (a thin tag archive, internal search results) outranking a real page is different: taking it out of the index is fine, and it's an index-hygiene fix to flag for `technical-seo-audit`.
- Google's choice is evidence. If it keeps showing the "wrong" page, read that page before overruling it; it may answer the query better than the page you meant to rank.
- Small numbers lie. Don't act on a few weeks of data or on queries with a handful of impressions, where URL switching is mostly noise.

## Steps

1. **Clean the data.** Web search type only. Separate brand queries: use Search Console's branded-queries filter where your property has it, or a regex of brand names and misspellings.
   - Drop the bare brand name (homepage plus other pages there is normal). Keep brand queries with a modifier (pricing, reviews, login, vs, alternatives, integrations); those are where the wrong page often ranks.
   - Normalise URLs (strip tracking parameters and fragments). If http/https or slash variants appear as separate rows, note it as a technical issue and route it; don't treat it as cannibalization.
   - Rare queries are hidden by Search Console for privacy, so totals are incomplete. Say so in the report.
2. **Find candidate queries.** Per query, list every URL with impressions, clicks, average position and its share of the query's page-level impressions.
   - Candidate when 2 or more URLs each hold at least 10% of the page-level impressions, and the query has enough volume to matter (house default: 100+ impressions in 3 months for a small site; raise it for big sites).
   - Drop queries where both URLs average a top-5 position: that is a double listing, not a conflict. Note them under "isn't cannibalization".
   - An AI Overview counts as one position, shared by every link in it. A URL cited there while another of your URLs ranks below is two listings, not a fight; check the results before calling it a conflict.
   - Average position is an average across many searches. A URL "at 18" may be at 6 for some users and 40 for others; read it as a direction, not a spot.
   - Keep queries where the "wrong" page leads (a blog post above the pricing page for "<product> pricing") even at lower volume; those cost revenue.
3. **Check for flips.** With query + page + date data, find the URL with the most impressions for the query each week.
   - A flip is the leading URL changing 2 or more times in 8 to 12 weeks, or a handover that coincides with a position drop. Flips plus position swings are the strongest evidence you'll get.
   - In the UI: compare two periods on the query's Pages tab.
   - Free route to weekly rows: Looker Studio's Search Console connector (the URL impression table has query, landing page and date) exported to a sheet.
4. **Group into conflicts.** One conflict is a set of competing URLs plus the queries they share; one pair of pages usually shares many queries.
   - Rank conflicts by clicks and impressions at stake on the shared queries, then by the business value of those queries.
5. **Confirm intent with search results.** For the 1 to 3 most valuable shared queries, check the top 10 in the target country and language, on mobile.
   - Note which of your URLs appear and where.
   - Compare the results for each page's own main query: 4 or more shared top-10 URLs means Google sees one intent (real conflict likely); 3 is borderline, so let the next check decide; 0 to 2 means different intents (differentiate or leave it).
   - Read both pages: same angle, same audience, same format? Two "beginner's guide" posts are one job; a guide and a calculator are two.
6. **Collect survival evidence per URL.** For every URL in a conflict: clicks and impressions across all its queries (3 and 16 months), referring domains and notable external links, conversions and revenue, non-search traffic, contextual internal inlinks, publish and last-update date, and whether navigation, ads, emails or product UI link to it. Write "not checked" for anything you couldn't see.
7. **Decide.** One decision per conflict:
   - **Leave it**: different intents confirmed by the results, both URLs in the top 5, too little volume, only stray impressions, or a broad head term where Google rotates different page types while it works out what people want.
   - **Merge**: same intent, both pages substantial, neither clearly winning, and one combined page would be better than either. The survivor is the URL with more external links, conversions and history (tie-break: the one ranking higher for the shared queries). List the sections to move, the 301, the internal links to update, and the sitemap change.
     - Before merging, filter Search Console to the losing URL and read its Queries tab. Every query it earns clicks for needs a home on the survivor, or those clicks go with it.
     - Keep the survivor's title and H1 unless the merge widens its scope; a merge is not the moment to also rewrite a ranking page's title.
   - **Differentiate**: both pages are worth keeping and an honest separate intent exists for one of them (a "CRM for startups" guide vs a "CRM pricing comparison"). Retarget the weaker-fit page: new title, H1, opening and section focus around its new query; point internal anchors at each page using its own intent; cross-link the two.
   - **Canonicalize**: both URLs must exist for users but the content is nearly identical (print versions, colour variants of one product, syndicated copies, parameter variants). Canonical from the copy to the main version; keep internal links and the sitemap on the main version. Afterwards, URL Inspection's "Google-selected canonical" shows whether Google agreed; the tag is a strong signal, not an order.
   - **De-optimize**: the wrong page ranks because it borrows the right page's words. Remove the query from the wrong page's title, H1 and the internal anchors pointing at it; add a clear link from it to the right page using that query's wording; strengthen the right page's internal links.
     - Check the internal anchors first: when ten articles link to a blog post with "<product> pricing" as the anchor, the site itself is telling Google which page is about pricing.
   - Priority: wrong page ranking for a money query, or a conflict on queries with real clicks at stake: `Fix now`. Same-intent posts splitting a mid-value query: `Fix next`. Low-volume long tail: `Worth doing` or `Leave it`.
8. **Stress-test merges and redirects.**
   - If the losing URL has more referring domains or conversions than the survivor, swap the survivor or reconsider.
   - If it ranks top 3 for other queries the survivor doesn't cover, move those sections across, or differentiate instead.
   - If ads, emails, docs or partners link to it, list them so they can be updated. The redirect keeps visitors arriving, but ad destination checks, campaign tracking and landing-page reports will all change.
9. **Write the change list.** For each conflict: redirect lines (from → to, 301), title and H1 before → after, sections to move or cut, internal links to update (how many, on which pages), canonical tags to add. This is a draft; don't change the live site, redirects or CMS without permission for that change.
   - Redirect straight to the survivor. If other old URLs already redirect to the losing page, point them at the survivor too, so nothing chains.
   - Take the losing URL out of the XML sitemap, and make sure the survivor's canonical points at itself.
   - Deleting a page outright (404 or 410) instead of merging is only for pages with no external links, clicks or conversions worth keeping.
10. **Set the check.** Name the shared queries to watch and the metric (the survivor's clicks, impressions and position on them). Compare equal date spans before and after, once URL Inspection shows Google has recrawled both URLs. No promises on timing or outcome.

## What to hand back

Fill in this template, highest priority first.

```markdown
# Keyword cannibalization check: <site> (<date range>, <country>)

**What I found:** <n> real conflicts among <n> queries with more than one URL; <n> look like cannibalization but aren't.
**What matters most:** <the conflict costing the most clicks or revenue, in plain English>
**What to do first:** <one action>

## Decisions at a glance
- <short name>: <decision>, `<priority>`, <clicks or impressions at stake>
- ...

## Conflicts

### 1. <short name>: <Merge / Differentiate / Canonicalize / De-optimize / Leave it>, `Fix now`
- Shared queries: "<q1>" (<page-level impressions>), "<q2>" (...), "<q3>" (...)
- <URL A>: <share>% of impressions, avg position <n>, clicks <n>, referring domains <n or not checked>, conversions <n or not checked>
- <URL B>: <same fields>
- Flip evidence: <e.g. leading URL changed 3 times in 10 weeks>. Evidence: tool (Search Console), high
- Intent evidence: <n>/10 shared top-10 URLs; <what Google shows>. Evidence: seen, medium
- Why this decision: <2-3 sentences>
- Changes: <301 from → to / title before → after / sections to move / n internal links to update / canonical>
- Risks checked: <links, conversions, campaigns pointing at the old URL>

## Looks like cannibalization, isn't
- "<query>": <URLs>. <why it's fine, e.g. both in top 5; different intents>. `Leave it`

## What I could not check
- <e.g. no backlink data, so the survivor choice rests on clicks and conversions only>
```

## Stop and flag if

- The data has no query + page pairing. You can't detect conflicts from separate query and page lists; explain how to get the pairing (UI filter, API, Looker Studio) and stop.
- The window is under 4 weeks, or the queries have so few impressions that any split is noise.
- A merge would redirect a URL with more external links or conversions than the survivor, or one used in ads, emails, docs or partner pages. Ask before recommending it.
- The "conflict" is one page at several URLs (protocol, slash, parameters). That's duplication; route it to `technical-seo-audit`.
- The output is unacceptable if it recommends a merge or redirect without per-URL links, conversions and traffic (or without marking them "not checked" and flagging the risk), treats every multi-URL query as a problem, uses canonical between distinct pages, or promises rankings will recover.

## Next step

- For each merge or differentiate decision, run `seo-content-brief` with the conflict entry as input (a consolidation or refresh brief).
- Run `internal-linking-plan` with the decisions list to repoint links at survivors and split anchors between differentiated pages.
- Before redirects ship, run `seo-change-monitor` on every URL involved so you can compare after Google recrawls.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
