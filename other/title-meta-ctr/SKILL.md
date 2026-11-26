---
name: title-meta-ctr
description: Find pages with impressions but weak clicks in Search Console, compare their CTR with your own site's CTR-by-position baseline, check what Google really displays, and write 3 title and meta description variants per page with a 28-day test plan. Use for "low CTR", "high impressions low clicks", "rewrite my title tags".
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/title-meta-ctr
---

# Title and meta CTR

Find the pages that Google already shows but searchers rarely click, prove the snippet is the problem (not the position, the SERP layout or the intent), and rewrite the title and meta description with three honest variants per page. You hand back a ranked candidate list, the variants with reasoning, and a test plan that can tell a real gain from noise.

> **Romeo's rule:** Before rewriting a title, check Google is actually showing it; plenty of people have tested words nobody saw.

## Use this when

- Search Console shows pages with lots of impressions and few clicks.
- A page sits on page 1 for its main query but its CTR is well below what your other pages get at the same position.
- Google displays a different title from the one in your `<title>` tag.
- Titles are out of date (last year in the title, old product names, old prices) or a template made them all look the same.
- After a refresh or relaunch, you want snippets that match what the page now offers.

## Don't use this for

- Pages ranking below position 10 on their main queries: the problem is ranking, not the snippet → `on-page-seo-review`.
- Explaining a traffic drop over time → `seo-performance-audit`.
- A page that ranks for queries it doesn't actually answer → `search-intent-match`.
- Winning stars, prices or other rich results in the snippet → `schema-markup`.

## What you need

### Required

- Search Console Performance data for the Web search type with Page and Query dimensions together, ideally the last 3 months (28 days is enough on high-traffic sites). One country filter if the site targets one market.
- The site's brand names and common misspellings, to separate branded queries.
- The current `<title>`, H1 and meta description for each candidate page (crawl export or view-source).

### Helpful

- The Search Console API, Looker Studio connector or BigQuery bulk export, to get page+query rows beyond the UI's 1,000-row limit.
- The branded queries filter in Search Console (top-level properties with enough query volume only; not path or subdomain properties).
- Device and country splits, and SERP screenshots for each candidate's top queries on mobile and desktop.
- Conversions per landing page from analytics, to favour pages whose extra clicks are worth money.
- A log of past title changes with dates.

### No tools?

In Search Console: Performance → Search results, Web, last 3 months. Export the Pages table. For each promising page, click it to filter, open the Queries tab and export again; that gives page+query rows by hand. Build the baseline and the expected-clicks calculation in a spreadsheet. Check what Google displays by searching each top query in a private window set to the target country, on a phone and on a desktop.

## Ground rules

- Use the site's own CTR-by-position curve. Published industry curves come from other people's queries, brands and SERP layouts; they're not a benchmark for yours.
- Keep branded queries out of the baseline and out of the candidate list. Brand searches click at rates no generic query can match and will make every other page look broken.
- Analyse page+query rows, not page totals. A page's average position blends dozens of queries; its CTR at "position 4.3" may be one query at 1 and forty at 9.
- SERP layout sets the ceiling. AI Overviews, ads, shopping units, video and image packs, local packs, "People also ask" and forum results all push organic links down and absorb clicks. Low CTR on a query with an AI Overview and four ads is not a title problem.
- In Search Console, every link inside an AI Overview gets the AI Overview's position. A page cited there at "position 1" with a low CTR is expected, not a snippet failure.
- Check what Google shows before rewriting. Google builds title links from the `<title>`, the main visible heading, `og:title`, anchor text and other sources, and rewrites titles that are half-empty, obsolete, inaccurate, boilerplate, duplicate the site name or don't match the page's main title. Snippets come mostly from page text; the meta description is used when it describes the page better.
- Keep the main query in the title in natural form. Searchers scan for their own words, and Google often bolds matching words in the snippet.
- Numbers, years, prices, "free" and "tested" only if true today and maintained. A year in the title is a promise to update it every year.
- No clickbait. The title promises exactly what the page delivers; overpromising raises bounce and invites a rewrite.
- Small samples lie. Below a few hundred impressions per period, CTR swings are noise; don't call winners from them.

## Steps

1. **Pull the data.** Page+query rows for Web search, 3 months, with clicks, impressions, CTR and position; split by device if volume allows. Page totals will exceed the sum of query rows because Google hides rare (anonymised) queries; work from the rows you have and say so.
2. **Build the baseline.** Remove branded queries with Search Console's branded filter if the property has it, otherwise with a query filter of "Doesn't match regex" listing brand names and misspellings. Using non-branded rows only, bucket by rounded position: 1, 2, 3, 4, 5, 6 to 7, 8 to 10, 11 to 15. For each bucket, CTR = total clicks ÷ total impressions (weighted by impressions, never an average of row CTRs). Need at least about 1,000 impressions per bucket; merge neighbouring buckets until you have it. Build mobile and desktop curves separately if each has the volume.
3. **Find candidates.** Rows with position ≤ 10, non-branded, impressions above a floor that suits the site (start at 300 over 3 months), and CTR below the bucket baseline.
   - Expected clicks = impressions × baseline CTR for that bucket. Missed clicks = expected − actual.
   - Sum missed clicks per page across its rows. Rank pages by missed clicks, weighted up when the page converts. Take the top 10 to 20.
4. **Explain each gap before blaming the snippet.** For the top 1 to 3 queries per candidate, look at the live SERP in the target country, mobile first.
   - SERP features present: AI Overview (and whether this page is cited in it), ads above the results, shopping, video, images, local pack, "People also ask", forum results, top stories.
   - Navigational for another brand ("canva login") or a mismatched intent (the page ranks for something it doesn't serve).
   - Position movement inside the period (check the date chart), seasonality, or a Google update.
   - Search Console's Generative AI performance report shows whether a page earned AI Overview or AI Mode impressions (by page, not by query), but the Performance report doesn't record which other features appeared. Use a live check, screenshots, or SERP-feature data from a rank tracker export, and note the date: layouts change often.
   - Label each candidate: `snippet problem`, `SERP feature drag`, `intent mismatch`, `navigational`, or `data artefact`. Only `snippet problem` pages go on to variants; route `intent mismatch` to `search-intent-match`.
5. **Record what Google displays.** For each top query: the displayed title link, the snippet text, the site name, any date shown, any rich result. Compare with the `<title>`, H1, `og:title` and meta description.
   - Title rewritten: note the likely cause from the list in the ground rules. The fix often includes aligning the H1 with the title, not only editing the title.
   - Snippet taken from page text: find the paragraph Google used. Improving the page's opening answer can matter as much as the meta description.
   - An old date displayed: the page needs a real update, not a new title.
6. **Diagnose the current title and description.**
   - Is the main query there, in the first half? Does truncation cut off the useful part (about 50 to 60 characters on desktop is a working guide; Google sets no limit and truncates by width)?
   - Is it boilerplate shared with sibling pages? Is it indistinguishable from the competing titles on the same SERP?
   - Does it state what the searcher gets: an answer, a price, a template, a comparison, a time saving?
   - Meta description: present, specific, around 120 to 155 characters, with the query and one concrete detail.
7. **Write 3 variants per page.** Each variant is a title plus a meta description, with its angle, its character count and a one-line reason grounded in what you saw on the SERP. Typical angles:
   - Direct answer: the query plus the outcome ("Website audit cost: what you'll pay in 2026 and why").
   - Specific proof: a true number, scope or method ("Website audit checklist: 47 checks we run on every client site").
   - Audience or differentiator: who it's for, or what competing titles lack ("Website audit for Shopify stores: free checklist and fixes").
   - Rules for all three: keep the main query; brand short at the end or dropped if Google already shows the site name; no all caps, emoji or stacked punctuation; years and numbers only if true; match the H1's topic so Google has no reason to rewrite. Mark one variant as recommended and say why.
8. **Plan the test.**
   - Change a batch of 10 to 20 pages at once. Keep a similar set of candidates unchanged as a control, so seasonality and algorithm updates show up in both groups.
   - Log every change: URL, old and new title and description, deploy date. Add a Search Console annotation on the deploy date (right-click the Performance chart → Add annotation; 120 characters max).
   - Request indexing in URL Inspection for the changed pages, then search the main query until Google displays the new title. The test clock starts on the day the new title shows, not the day it deployed.
   - Wait 28 days from the day the new title first shows, then compare those 28 days with the 28 days ending the day before deployment. Leave out the days in between. Both windows are four whole weeks, so weekday patterns cancel.
   - Position-adjusted CTR: for each page+query row in both periods, expected clicks = impressions × baseline CTR at that period's position. Per page, score = total actual clicks ÷ total expected clicks. Compare the score before and after, and against the control group's change. This separates a better snippet from a ranking move.
   - Decide: keep if the score improves by a margin larger than the control group's change and the main query's position held; revert if the main query lost more than about one position and stayed down, or the score fell; extend to 56 days if impressions are too low to call. Check Google's Search Status Dashboard for ranking updates in the window before crediting or blaming the change.
   - Don't touch the same pages again during the test window.
9. **Add the top-3 risk note.** For any page ranking positions 1 to 3 on its main query, the title is also a relevance signal and the page has more to lose than gain.
   - Change it only if CTR is far below your own baseline at that position and there is a clear cause (rewritten, outdated, truncated, boilerplate).
   - Prefer a meta-description-only change first; Google has said it doesn't use the meta description for ranking.
   - Keep the main query's wording, change one top-3 page at a time, and keep the old title ready to restore.

## What to hand back

Rank pages by missed clicks. Show the baseline you used so anyone can recheck it.

```markdown
# Title and meta CTR plan: <site> (<data range>, <country>, <device>)

**What I found:** <one plain-English sentence>
**What matters most:** <one sentence>
**What to do first:** <one sentence>

## Your CTR baseline (non-branded, <date range>)
- Position 1: <CTR> (<impressions>) · 2: <CTR> · 3: <CTR> · 4: <CTR> · 5: <CTR> · 6-7: <CTR> · 8-10: <CTR>

## Candidates
### 1. <URL> · `Fix next` · missed clicks: <n> over <period>
- Top queries: "<query>" pos <x>, <impr> impr, CTR <y> vs baseline <z>; ...
- SERP: <features seen, AI Overview cited yes / no> · seen / tool / inferred · confidence: high / medium / low
- Google displays: title "<displayed title>" (rewritten: yes / no, likely cause) · snippet from: <meta / page text>
- Current: title "<current>" (<chars>) · meta "<current>" (<chars>)
- Diagnosis: <plain English>
- Variant A (recommended): title "<...>" (<chars>) · meta "<...>" (<chars>) · why: <...>
- Variant B: title "<...>" · meta "<...>" · why: <...>
- Variant C: title "<...>" · meta "<...>" · why: <...>
- Also change: <H1 or opening paragraph, if needed>
- Risk: <top-3 note, or "low">

## Not a snippet problem
- <URL>: <SERP feature drag / intent mismatch / navigational / data artefact> · <what to do instead>

## Test plan
- Test batch: <URLs> · control: <URLs>
- Annotate: <date> · clock starts when Google shows the new titles
- Read results on: <date + 28 days> · metric: position-adjusted CTR vs control
- Keep / revert / extend rules: <as agreed>

## What I could not check
- <item>: <what would verify it>
```

## Stop and flag if

- Only page-level totals are available. Say the analysis is low confidence and ask for page+query rows before writing variants.
- The data is too thin to build a baseline (fewer than about 1,000 non-branded impressions in most position buckets). Say so; don't borrow an industry curve to fill the gap.
- A variant would need a claim you can't confirm (a price, a number of items, "updated for 2026", "free"). Leave a `[confirm: ...]` placeholder.
- The user wants to change titles on many top-3 pages at once. Push back with the risk note and propose a smaller test.
- Output with variants but no reasoning, no SERP check, no baseline or no test plan is not acceptable. Neither is clickbait.
- Applying the titles means editing the live CMS. Draft them; change nothing without explicit permission for that change.

## Next step

- Before deploying → `seo-change-monitor` to snapshot the changed pages' titles, positions and CTR.
- Candidates labelled `intent mismatch` → `search-intent-match` with the URL and the mismatched queries.
- Pages where Google rewrote the title because the page itself is weak → `on-page-seo-review` on that URL and query.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
