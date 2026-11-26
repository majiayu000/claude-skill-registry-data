---
name: search-intent-match
description: Check whether a page is the kind of page Google ranks for its query (page type, format, angle, depth, freshness, SERP features) and say exactly what to change, or which page to build instead. Use for "why won't this page rank", "does my page match search intent", or "should this be a blog post or a category page".
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/search-intent-match
---

# Search intent match

Check whether a page is the kind of page Google currently ranks for its target query. Read the live results (page type, format, angle, depth, freshness, and the extra boxes Google adds such as AI Overviews and People also ask, known as SERP features), work out what the searcher wants to do next, compare your page against that pattern, and return a match, partial or mismatch verdict with exact changes, or a recommendation to build a different kind of page.

> **Romeo's rule:** You can't out-write a page-type mismatch: when Google shows ten category pages, a brilliant essay is applying for the wrong job.

## Use this when

- A page is indexed and decent, and still stuck beyond the first page for its main query.
- Before writing or refreshing a page, to decide what kind of page it should be.
- Rankings fell while the page didn't change, and you suspect Google changed what it shows for the query.
- You're debating blog post vs landing page vs category page vs tool for a keyword.
- Search Console shows the page getting impressions mostly for queries it wasn't written for.

## Don't use this for

- Choosing which queries to target → `seo-opportunity-research`.
- A full on-page review (title, headings, images, links, schema) once the page type is right → `on-page-seo-review`.
- Two of your pages showing for the same query → `keyword-cannibalization-check`.
- Map-pack rankings and Business Profile work for local queries → `local-seo-audit`.

## What you need

### Required

- The target query (one main query, plus up to 3 close variants if they matter).
- The page: its URL, or its HTML or text if it isn't live yet.
- Target country, language and device. Default: mobile, the site's main country.

### Helpful

- The search results captured from the target location: a SERP API or SEO tool export, or full-page screenshots. An agent's own Google searches often hit bot checks; don't try to get around them.
- Search Console data for the page: the queries it gets impressions for, and its position over time.
- What the business wants the searcher to do (buy, sign up, book, call, read).
- Results for 1 or 2 close variants of the query, to see whether the intent holds steady.

### No tools?

Search the query in a private window, signed out, with the country set to the target market, on a phone or a narrow browser window. Screenshot the whole first page, including the AI Overview, People also ask and any map, product or video blocks, then open the top 5 results. Paste the screenshots or list the 10 result titles and URLs. For your own page, view-source or pasted text is enough. Search Console's Performance report, filtered to the page, shows which queries Google already associates with it.

## Ground rules

- The results page is the spec. Google shows what has satisfied people searching that query; an opinion about what the query "should" want loses to it.
- Page type is the hard constraint. Angle, format and depth are softer. Fix type first; polishing the wrong type is wasted work.
- Weight the top 3 to 5 results more than positions 6 to 10; they show what wins, the rest show what's tolerated.
- Mixed results mean the query has several meanings or Google is hedging. Pick the slice the business serves best; one page shouldn't try to be a guide and a product grid at once.
- Match the pattern, then beat it on substance: first-hand experience, real numbers, worked examples, a tool or template. A copy of the top 10's outline gives Google no reason to rank you above them.
- Freshness is earned. Update the visible date or put the year in the title only when the content really changed; Google's own guidance calls out changing dates to look fresh.
- SERP features change what a click is worth, not whether to try. When an AI Overview answers the simple version on the results page, the page needs something a summary can't give: a tool, data, a decision, depth.
- Don't plan for retired features. FAQ rich results stopped showing in Google in May 2026, and HowTo rich results went in 2023. People also ask boxes are a different thing and still worth answering in the text.
- One snapshot can mislead. Results vary by location, device and day; if the verdict hinges on a close call, check twice.
- Never promise that matching intent will produce a ranking.

## Steps

1. **Pin down the search.** Query, country, language, device and date.
   - Note if the query is local ("near me", a city, or Google shows a map), branded, or ambiguous (several meanings).
2. **Read the results.** For each of the top 10 organic results record:
   - position, site type (brand or vendor, publisher, marketplace, forum, government or education, video platform);
   - page type: guide or how-to, list, product page, category or collection page, tool, calculator or template, comparison or "vs", review, video, forum thread, local business page, homepage, news, glossary;
   - format cues: numbered steps, comparison table, "N best" list, embedded video, calculator, price list;
   - angle from the title: year, best, cheap or free, beginner, for a specific audience, near me, template, examples;
   - visible date, if any.
   - Then list SERP features top to bottom: ads, AI Overview (and the sites it cites, if shown), featured snippet, People also ask (copy the questions), videos or short videos, discussions and forums, local pack, shopping or product grids, top stories, images, knowledge panel, sitelinks.
3. **Name the dominant pattern.** House thresholds:
   - Page type: shared by 6 or more of the top 10 = dominant (high confidence); 4 to 5 = leading, with a secondary type; no type above 3 = mixed.
   - Angle: a modifier in 4 or more of the top-10 titles (the year, "for small business", "free") is part of the intent.
   - Depth: compare scope, not length. Which subtopics do most top results cover? Do they carry tables, prices, screenshots, original data, or a short direct answer? Never set a word count.
   - Freshness: if most top results show dates in the last 12 months, or the topic changes often (prices, software, laws, product rankings), currency is part of the intent.
4. **Read the features as intent signals.**
   - Local pack or map: local intent. A page without a local presence will struggle → `local-seo-audit`.
   - Shopping or product grids: people want to buy. Product and category pages win; articles rarely do.
   - Videos or short videos: people want to watch it done. A good video on the page helps, and the video itself can rank separately.
   - Discussions and forums: people want first-hand opinions. Add real experience, named examples and honest drawbacks.
   - People also ask: sub-questions to answer in the text, briefly, under relevant headings.
   - AI Overview: the quick answer is given on the results page. Compete on depth, decision help or tools; to be cited in it → `ai-search-visibility`.
   - Featured snippet: a concise definition, list or table near the top is expected.
   - Top stories: news freshness; an evergreen page may not compete for that slot.
   - Knowledge panel or sitelinks for one brand: navigational. Not winnable unless it's your brand.
5. **Handle mixed results.** List each intent slice with its count and positions (e.g. guides at 1, 3, 5, 8; vendor pages at 2, 4, 7; lists at 6, 9).
   - Target the slice that fits the business and holds the higher positions.
   - Build one page per slice when both are worth it, and link them to each other.
   - If a close variant of the query has cleaner results ("what is X" vs "X software"), consider targeting the variant.
6. **Place the searcher.** Buyer journey stage:
   - learning about the problem; looking for ways to solve it; comparing options (best, vs, alternatives, reviews, pricing); ready to act (buy, sign up, book, download, near me); existing customer (login, support, how to use).
   - The next click: what the searcher wants to do right after reading (see options with prices, try the tool, copy the template, compare two products, book, buy). Top results usually make it obvious near the top of the page; write down what it is.
7. **Read your page the same way.** Page type, format, angle, depth (subtopics, tables, media, original material), freshness (visible date, current facts and prices), what's visible on a phone screen before scrolling, and the next click it offers.
   - Check Search Console: if the page gets impressions mostly for other queries, Google reads it as serving a different intent.
8. **Give the verdict.**
   - **Match**: same page type as the dominant one, main angle covered, comparable depth, current, offers the next click. The problem is elsewhere (links, authority, technical, snippet); route it.
   - **Partial**: right page type, but angle, format, depth, freshness or the next click is off.
   - **Mismatch**: wrong page type, wrong buyer stage or wrong audience. Edits won't fix it.
9. **Write the changes.** For a partial match, specific edits with before → after:
   - title and H1 angle (e.g. add the audience the results are written for);
   - the opening: answer the query in the first two or three sentences;
   - format: add the comparison table, put the steps first, show prices;
   - missing subtopics that most top results cover, and People also ask questions worth answering;
   - freshness: which facts, prices or screenshots to update (not just the date);
   - the next click, placed near the top: product list, tool, template, booking or pricing link.
   - Give each change a priority label and evidence.
10. **Prescribe the right page for a mismatch.** Name the page type needed and where it should live (a category page, a landing page, a free tool). Then decide what happens to the current page:
    - retarget it to a query whose results match it (name the query and show the evidence);
    - keep it as a supporting page that links to the new one; or
    - merge it into the new page.
    - Don't rewrite a blog post's intro and call it a category page.
    - If the winning page type is something the business can't or shouldn't build (marketplace listings, a government form, a free tool it can't support), say so and recommend a different query. `Leave it` is a valid answer.

## What to hand back

Fill in this template.

```markdown
# Search intent match: "<query>" → <URL> (<country>, <device>, checked <date>)

**What I found:** <Match / Partial / Mismatch, in one plain sentence>
**What matters most:** <the single biggest gap>
**What to do first:** <one action>

## What Google shows
- Dominant page type: <type>, <n>/10 (<high / medium / low> confidence). Secondary: <type>, <n>/10
- Angle: <modifiers seen in n/10 titles>
- Depth: <what most top results cover and include>
- Freshness: <n>/10 dated within 12 months; <does currency matter?>
- SERP features, top to bottom: <list>
- Mixed intent: <no / yes: slices and positions>
- Buyer stage: <stage>. Next click: <what the searcher wants to do next>
- Evidence: <seen: screenshots / tool: SERP API or SEO tool name>, <confidence>

## Your page
- Page type, angle, depth, freshness, next click: <one line each>
- Queries Google sends it (Search Console): <top 3 or not checked>

## Verdict: <Match / Partial / Mismatch>
<2-3 sentences: why>

## Changes
1. `Fix now`: <change>. Before: "<...>" After: "<...>". Evidence: <...>
2. `Fix next`: ...

## If a different page is needed
- Build: <page type> at <proposed URL>, targeting "<query>"
- Current page: <retarget to "<query>" / keep as supporting page linking to the new one / merge>

## What I could not check
- <e.g. results from one location and one day only; AI Overview not captured in the export>
```

## Stop and flag if

- You can't see the results (no screenshots, no SERP export or API data). Don't reconstruct them from memory; ask for screenshots.
- The results look personalised or from the wrong place (local results from another city, a signed-in browser).
- The query is another company's brand or a navigational search; a mismatch by design. Say so and suggest a different query.
- The page isn't indexed, is blocked or redirects. Run `technical-seo-audit` first.
- The output is unacceptable if the verdict has no listed results evidence, if the advice is generic ("add more content", "improve quality"), if it sets a word count, or if it recommends changing dates without changing content.

## Next step

- For a partial match or a new page type, run `seo-content-brief` with this report as the intent and results section. When the page needed is a product, feature or service landing page, run `landing-page-writer` instead.
- For a match, run `on-page-seo-review` on the page, then `title-meta-ctr` if it ranks but earns few clicks.
- If an AI Overview dominates the results, run `ai-search-visibility` for this query.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
