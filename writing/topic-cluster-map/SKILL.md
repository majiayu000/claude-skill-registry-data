---
name: topic-cluster-map
description: Group a keyword list into pages by the search results they share (not similar wording), pick a hub and spokes per cluster, and map each to create, refresh or merge with a link pattern. Use for "cluster these keywords", "build topic clusters", "which keywords go on one page", or planning content from keyword research.
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/topic-cluster-map
---

# Topic cluster map

Turn a keyword list into a plan of pages. Decide which keywords one page should serve by the search results they share, not by how alike they sound; group those pages into clusters of one broad page linked to narrower supporting pages (hub and spokes); match them to the pages you already have (create, refresh or merge); and define how hub and spokes link. You get a cluster map and a prioritised page plan.

> **Romeo's rule:** Google has already shown you which keywords share a page; going by how words sound instead is how a site ends up with nine thin posts answering one question.

## Use this when

- You have a keyword list (from `seo-opportunity-research`, a tool export or a brainstorm) and need to know how many pages it really means.
- You're about to write a batch of content and want to avoid pages that compete with each other.
- You want hub pages for your main topics and a clear linking pattern between them and the supporting pages.
- Your blog grew post by post and you need to see which topics are covered, doubled up or missing.

## Don't use this for

- Finding the keywords in the first place → `seo-opportunity-research`.
- Deciding what to do with two existing pages already competing → `keyword-cannibalization-check`.
- Writing the brief for one page in the plan → `seo-content-brief`.
- Planning hundreds of template pages from a dataset → `programmatic-seo-plan`.

## What you need

### Required

- A keyword list, plus the target country and language. Volume and difficulty are welcome but not required.
- The site URL and what the business sells, so business value can be judged.

### Helpful

- Top-10 organic URLs for every keyword, for the same country, language and device, collected within a few days of each other (an SEO tool's SERP export, a SERP API, or manual checks).
- The page inventory from `site-content-inventory`, or a Search Console query + page export, to match keywords to existing pages.
- Search volume and difficulty from a named tool (they're estimates; label them `tool`).
- Conversions by landing page, to judge which topics actually bring customers.

### No tools?

Search each keyword in a private window set to the right country and language, and copy the top 10 organic URLs into a sheet; 30 to 50 keywords is a realistic manual batch. For a bigger list, check results for the 30 most valuable keywords and group the rest by intent, marked low confidence. Match keywords to existing pages with Search Console (Performance > Query filter > Pages tab) and a `site:yourdomain.com keyword` search. No volume data? Rank by business value and Search Console impressions instead, and say that's what you did.

## Ground rules

- Shared search results decide which keywords share a page. Wording misleads both ways: two phrases that look almost identical can need different pages (one returns calculators, the other guides), and two that look unrelated can be served by one page.
- House threshold: two keywords belong on the same page when their top-10 organic results share 4 or more URLs. 2 to 3 shared means related (usually separate pages in the same cluster; check intent). 0 to 1 means separate. Why 4: one or two shared URLs often come from a big site that ranks for everything in the niche (a marketplace, Wikipedia, Reddit), so a low threshold lumps different jobs together; demanding 5 or more splits keywords Google is happy to rank one page for. Drop to 3 when result pages carry fewer organic results (heavy with features) or the niche is so long-tail that few URLs repeat; raise to 5 when one or two giant sites fill most results everywhere. Say which threshold you used and why.
- Compare URLs, not domains, after normalising (http/https, www, trailing slash, tracking parameters). Count organic web results only: not ads, AI Overview citations, People also ask, or video and image packs.
- Group around a seed, never by chaining. A sharing 4 URLs with B, and B sharing 4 with C, doesn't put A and C on one page. Compare every keyword to the group's seed.
- Results overlap sets page boundaries; topic and the reader's journey set cluster boundaries. A page group is one page. A cluster is several pages a reader moves between.
- A hub must be useful on its own: a page that answers the broad query and routes readers onward, not a list of links. For shops the hub is usually a category page; for software, a product, use-case or pillar guide page; for services, the service page.
- A cluster is a way of organising useful pages and links, not a ranking trick. Ten thin spokes around a hub add nothing; plan fewer pages that each fully serve their group.
- Pick each page's primary keyword by business value and fit, then volume. The biggest number is often the vaguest intent.
- Check existing pages before planning new ones. A page already ranking around 5 to 20 for a group's keywords is a refresh, not a new page.
- Never invent volume, difficulty or rankings. Unknown is "not checked".

## Steps

1. **Clean the list.** Remove duplicates, off-topic terms, other companies' brand and login queries you can't serve, and queries whose intent the business can't credibly satisfy.
   - Keep plural and spelling variants for now; the results check decides whether they share a page.
   - Record country, language and device for every later step.
2. **Collect the results.** For each keyword: the top 10 organic URLs, same location, language and device, within a short window (results move).
   - Feature-heavy result pages sometimes show fewer than 10 organic results. Use what's there, and flag keywords with 7 or fewer organic results; they may need the lower threshold.
   - Also note the dominant page type (guide, list, product, category, tool, comparison, forum, video, local) and SERP features (AI Overview, local pack, shopping, video). These label intent later.
3. **Measure overlap.** For each keyword pair, count shared normalised URLs in the top 10. For large lists, compare each keyword with the current seeds only.
4. **Form page groups.** Sort keywords by business value, then volume.
   - Take the top unassigned keyword as a seed. Add every unassigned keyword sharing 4 or more URLs with that seed. Repeat until none are left.
   - Check each group: if one member's results show a different page type from the seed's (tools vs guides), split it out.
   - Leftovers become single-keyword groups. If more than half the list ends up alone, the list is very long-tail or the threshold is too strict; say which.
5. **Fallback without results data.** Group by the same core topic, the same intent (learn, compare, buy, find a place, reach a brand) and the same modifier type (best, vs, alternatives, price, how to, template, near me).
   - Mark every such group low confidence.
   - Check the results for the 10 most valuable groups before anyone writes a page.
6. **Label each group.** Primary keyword, secondaries, intent, dominant page type, buyer stage, volume (tool) or Search Console impressions, and difficulty.
   - Don't simply add up the volumes of close variants. Many tools already fold plurals and misspellings into one figure, so summing double counts. Report the primary keyword's volume, and the group total only with that caveat.
   - Difficulty from a tool, labelled `tool`, or an observation: "top 10 is all national brands and marketplaces" is hard for a small site; "top 10 includes forum threads and small blogs" is winnable.
7. **Build clusters.** Group page groups into topics a reader moves through.
   - Hub: the group whose results are broad overviews or category pages, with the highest business value in that topic.
   - Spokes: groups for specific sub-questions, use cases, comparisons and how-tos.
   - A cluster with one spoke isn't a cluster; fold it into the nearest one. Over about 25 spokes, split into sub-hubs.
8. **Map to existing pages.** For each group, find the URL that ranks for or targets it (Search Console query → page, the inventory, a `site:` search). Decide one action:
   - **Create**: no page serves the intent.
   - **Refresh**: a page serves it but ranks outside the top 5, or is stale or thin.
   - **Merge**: two or more existing pages serve one group. Name them and send the pair to `keyword-cannibalization-check` for the final call.
   - **Retarget**: a page aims at the group but is the wrong page type for its results → `search-intent-match`.
   - **Leave**: already in the top 3 for the primary keyword, and converting.
   - Cross-check with Search Console: if one existing page already gets impressions for keywords from two of your groups, Google sees them as related. Look again at whether those groups should be one page before planning a second.
   - When the best existing page sits in the wrong place in the cluster (a narrow post ranking for the hub keyword), keep what ranks and plan around it; moving rankings to a new hub URL is a merge decision, not a tidy-up.
9. **Define the link pattern.** Per cluster:
   - Hub → every spoke, in body copy, with a sentence of context and an anchor describing the spoke.
   - Every spoke → hub once, early in the page, with varied anchors naming the topic.
   - Spoke → spoke only where a reader naturally goes next (comparison → pricing, how-to → template), 2 to 3 per spoke at most.
   - Commercial spokes → the money page (product, pricing, category); informational spokes → the most relevant money page once, where it helps the reader.
   - Make the hub reachable from the main navigation or category structure when the topic matters to the business; a hub reachable only through blog posts is buried itself.
   - Breadcrumbs can follow the hub. Don't move existing URLs into new folders just for neatness; redirects carry risk for no gain.
10. **Prioritise.** Rate each planned page on business value (does the searcher need what you sell?), intent fit, winnability (who ranks now vs this site), and existing assets (a refresh beats a new page at equal value).
    - `Fix now`: merges of pages currently splitting a money query.
    - `Fix next`: high-value, winnable creates and refreshes, hubs first when spokes already exist.
    - `Worth doing`: lower-value spokes.
    - `Leave it`: groups you can't win or don't need, with the reason.
11. **Sanity-check the map.** Every keyword sits in exactly one group; no two planned pages share a primary keyword; no group mixes page types; every spoke links to its hub; every create has been checked against existing pages.

## What to hand back

Fill in this template, clusters ordered by business value.

```markdown
# Topic cluster map: <site> (<country/language>, results collected <dates>)

**What I found:** <n> keywords make <n> pages in <n> clusters; <n> pages exist, <n> to create, <n> to merge.
**What matters most:** <one sentence>
**What to do first:** <one sentence>

Method: <page groups = 4+ shared top-10 URLs with the seed keyword> or <grouped by intent without results data: low confidence>
Overlap data: <where the keyword-by-keyword overlap counts are, so anyone can audit a grouping>

## Cluster: <topic>
- Hub: "<primary keyword>" (+ <n> secondaries). Intent: <...>. Page type: <...>. Page: <URL or proposed slug>. Action: <Create / Refresh / Merge / Leave>. `Fix next`
- Spoke: "<primary keyword>" (secondaries: <...>). Intent, page type, <URL or none>, action, priority. Evidence: secondaries share <n> to <n> of 10 results with this seed; <n>/10 with the hub seed (tool or seen, <confidence>)
- Spoke: ...
- Links: hub → <all spokes>; spokes → hub; <spoke> → <spoke>; <spokes> → <money page>

## Page plan (in order)
1. `Fix now`: Merge <URL A> + <URL B> into <URL> for "<keyword>". Why: <...>. Next: `keyword-cannibalization-check`
2. `Fix next`: Create <slug> for "<keyword>" as a <page type>. Why: <...>. Next: `seo-content-brief`
3. ...

## Keywords not used
- "<keyword>": <off-topic / can't win / served by <URL>>

## What I could not check
- <e.g. no volume data; results for 140 of 200 keywords grouped by intent only>
```

## Stop and flag if

- The list has fewer than about 10 keywords. There's little to cluster; check the results for each and go to `search-intent-match` or `seo-content-brief`.
- Results were collected for different countries, devices or months apart; the overlap counts are not comparable.
- The list is mostly other companies' brand or navigational queries.
- A planned page would duplicate an existing page. Map it to that page instead.
- The output is unacceptable if it groups by wording without saying so, invents volumes, puts one keyword on two pages, or proposes a hub that is only a list of links.

## Next step

- Run `seo-content-brief` on the top `Fix next` page, passing its group (primary and secondary keywords), page type, cluster role and required links.
- Send every merge pair to `keyword-cannibalization-check` with the shared keywords.
- Run `internal-linking-plan` with the link pattern to turn it into exact sentences on existing pages.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
