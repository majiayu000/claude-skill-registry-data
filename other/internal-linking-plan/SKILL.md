---
name: internal-linking-plan
description: Find orphan pages, buried pages, links to redirects or 404s, nofollowed links and weak anchors, then get an exact list of links to add (source, target, anchor, sentence, reason). Use for "plan my internal links", "find orphan pages", "which pages should link to this page", or after a site crawl.
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/internal-linking-plan
---

# Internal linking plan

Map how your pages link to each other, find the pages that are cut off, buried or under-supported, and hand back a concrete list of links to add or fix: which page, which sentence, which words, and why. Works from a crawler export, or from your sitemap and the pages themselves when there is no crawler.

> **Romeo's rule:** Link where a reader would actually want to go next; a link nobody would click is wallpaper, and Google has seen a lot of wallpaper.

## Use this when

- A page you care about gets impressions but sits around positions 5 to 20 and needs support from the rest of the site.
- You published a batch of pages and nothing links to them yet.
- A crawl shows pages nothing links to (orphan pages), pages four or more clicks from the homepage (deep pages), or internal links pointing at redirects and 404s.
- Your money pages (product, pricing, service, category) are linked only from the menu and footer.
- You are creating or tidying hub pages for a topic and need the links between hub and supporting pages.

## Don't use this for

- Sitewide crawling and indexing problems (redirect chains, noindex mistakes, robots.txt, rendering) → `technical-seo-audit`.
- Deciding which of two competing pages should survive before you point links at it → `keyword-cannibalization-check`.
- Designing topic clusters and deciding which pages should exist → `topic-cluster-map`.
- Earning links from other websites → `backlink-profile-review`.

## What you need

### Required

- The site URL and a list of its pages: a crawl export, the XML sitemap, or the inventory from `site-content-inventory`.
- The pages that matter most to the business (the ones that sell, sign people up or book calls). If not given, ask; don't guess from URLs alone.

### Helpful

- A crawler export with inlinks, unique inlinks, crawl depth, status code, indexability and per-link data (source, target, anchor, rel, link position), e.g. Screaming Frog's "All Inlinks" bulk export or Sitebulb's links export.
- A Search Console Performance export by page (clicks, impressions, average position, last 3 months).
- Search Console's Links report: "Top linked pages" for both internal and external links.
- Each page's main target query, from the inventory or `seo-opportunity-research`.
- Whether body copy is editable in the CMS, and whether "related posts" blocks are automatic.

### No tools?

Start from /sitemap.xml (or /sitemap_index.xml, or the Sitemap: line in /robots.txt). If you can fetch URLs, fetch each page and record every `<a href>` in the main content separately from header, nav, sidebar and footer links, then walk the links from the homepage to get click depth. If you can't fetch, ask for view-source HTML of the 10 to 30 pages that matter; pasted plain text loses the links, so findings from it are content-match suggestions only. Search Console's free Links report gives internal link counts per target page as a cross-check. Say how much of the site you actually covered, and mark findings from a sample as medium confidence at best.

## Ground rules

- Relevance beats authority. A link earns its place when a reader of the source page would plausibly want the target next. A strong page linking to an unrelated target helps nobody.
- Plan links inside the body text (contextual links). Menus and footers already link sitewide; adding a page to the footer is not an internal linking plan, and footers stuffed with keyword anchors look manipulative.
- Google says there is no ideal number of links per page. The house cap for one round of changes: at most 5 new links per source page, fewer on short pages (as a rough guide, no more than one new link per 150 words of body copy), and one link per target per source page. The cap keeps pages readable and the change reviewable.
- No self-links. New links never point at redirected, 404, noindexed, canonicalized-away or robots-blocked URLs; link to the final 200, canonical URL.
- Anchors say what the target page is, in words that make sense read on their own. Vary them across sources: the target's main term on a minority of links, natural variants and descriptive phrases on the rest. The same exact-match anchor from 30 pages reads as manipulation.
- Don't nofollow links to your own indexable pages. It doesn't send ranking value to your other links instead; it only weakens the signal to a page you want found.
- Links must be crawlable: an `<a>` element with a real URL in `href`. Buttons, `onclick` handlers, `<span>` "links" and `javascript:` URLs are not reliably followed.
- An orphan is not automatically a page to link. Thank-you pages, ad landing pages and dead campaign pages may deserve noindex, a redirect or removal instead. Ask before treating every orphan as a target.
- Deep pages are usually a structure problem (long paginated archives, missing category pages). Fix structure with hubs and category links, not with hundreds of hand-placed body links.
- Automatic "related posts" widgets help discovery but tend to link newest, not best. They don't replace contextual links.

## Steps

1. **Agree the priority pages.** List the 5 to 20 pages that make money or are meant to, with their target queries.
   - Everything later is ranked by how much it helps these pages, then by how many pages it affects.
   - If the user can't say, propose a list from conversions (GA4 key events by landing page) or from page type (pricing, product, service, category) and confirm it.
2. **Build the link graph.** One record per link: source, target, anchor, rel, location (content or template), and the target's status code.
   - From a crawler export: use the per-link export, not just inlink totals. Template links (nav, header, footer, sidebar, breadcrumbs) are usually labelled by link position or can be identified because they appear on nearly every page.
   - Without a crawler: resolve relative URLs, drop fragments and tracking parameters, and normalise trailing slashes and case to the site's canonical pattern. Links inside `<nav>`, `<header>`, `<footer>` or `<aside>` (or containers named menu, footer, sidebar) are template; links inside `<main>`, `<article>` or the post body are content.
   - From pasted page text: keep any links the paste preserved (Markdown or HTML). If it lost them, you can't see what already links where; plan additions only and ask the user to confirm each target isn't already linked from that page.
   - JavaScript sites: links that only appear after scripts run are missing from raw HTML. If a page's fetched HTML has far fewer links than the page shows in a browser, say so, and use rendered HTML (a crawler with rendering on, or the URL Inspection tool's rendered HTML) for that template.
   - Compute click depth breadth-first from the homepage over crawlable links.
   - Per URL, record: unique contextual inlinks (distinct source pages), template inlinks, depth, status, canonical, indexable, and anchors received.
   - If the crawl hit a page limit, was blocked, or didn't render JavaScript menus, say so now; it changes every finding below.
3. **Find orphans.** Compare the pages that should exist (sitemap, Search Console pages with impressions, analytics landing pages) with the pages reachable in the crawl. Listed but unreachable = orphan. A crawl that starts at the homepage can't find orphans by itself.
   - Priority page or page with impressions, orphaned: `Fix now`.
   - Ordinary post with no traffic, orphaned: `Fix next`, or ask whether to keep it at all.
   - Intentional orphans (thank-you, paid-campaign landing pages): `Leave it`, but check they're noindexed if they shouldn't be in search.
4. **Find buried pages.** Flag indexable pages more than 3 clicks from the homepage. Three is a house heuristic, not a Google rule; the real question is whether important pages are reachable in a few clicks.
   - Typical causes: blog archives paginated to /page/12/, categories nested several levels, products reachable only through filters, posts linked only from the archive.
   - Fixes, best first: link from a relevant hub or category page; add to a curated "start here" or "popular" block; add contextual links from strong related pages. Pagination itself is fine.
   - Priority page deeper than 3: `Fix next`. Old low-value post at depth 5: `Worth doing` or `Leave it`.
5. **Measure support for important pages.** For each priority page: unique contextual inlinks, the share of inlinks that are template-only, and the anchors used.
   - Flag when contextual inlinks are below the site median or under 3, when 90% or more of inlinks come from nav and footer, or when nearly all anchors are identical or generic.
   - Compare with the site's own numbers, not an industry figure.
6. **Find pages close to page one (striking distance).** From the Search Console page export: average position roughly 5 to 20 with impressions in the top third of the site's pages.
   - Filter the report to the page and read its Queries tab: confirm the queries are ones the page should rank for.
   - If the page is the wrong kind of page for its query, links won't fix that → `search-intent-match`. If two of your pages split the query → `keyword-cannibalization-check` first.
7. **Fix the broken plumbing.** These are edits to existing links, not new ones.
   - Links to 404, 410 or 5xx URLs: point them at the right live page or remove them. In nav or footer, or across many pages: `Fix now`. One body link: `Fix next`.
   - Links to redirects: change the href to the final URL. Template link or a chain of two or more hops: `Fix next`. Single body link through one 301: `Worth doing`; Google follows it, this is housekeeping.
   - Links to non-canonical variants (http, parameters, a mismatched trailing slash) or to noindexed pages: point to the canonical URL.
   - `rel="nofollow"` on links to your own indexable pages: remove. On login, cart or account links: `Leave it`.
   - Generic anchors ("click here", "read more", "learn more", "this post", bare URLs) and image links with empty alt text: rewrite. A "Read more" button on a blog card next to a descriptive title link: `Leave it`; the title link carries the meaning.
   - Uncrawlable links (buttons, `onclick`, `<span>`) as the only route to an important page: `Fix now`.
8. **Choose source pages for each target.** Shortlist 3 to 8 sources per target that:
   - cover a related topic, ideally the step just before the target in the reader's journey (a how-to guide → the product that does the job; a comparison → pricing);
   - are indexable, 200, canonical pages;
   - have their own clicks, rankings or external links (Search Console page clicks, Links report "Top linked pages");
   - don't already link to the target and aren't over the cap.
   - Find candidates with the crawler's body-text search, a `site:yourdomain.com "topic phrase"` search, or pages whose Search Console queries overlap the target's.
9. **Write each link.** Find the sentence in the source that already talks about the target's subject and put the link on the words that describe the target.
   - Quote the current sentence and the new version. If no sentence fits, write one new sentence that adds information; "Check out our guide" doesn't count.
   - Anchor: usually 2 to 6 words, specific to the target, not already used for a different target on the same page.
   - Across all sources for one target, no single anchor more than twice.
10. **Plan hubs.** A topic with 5 or more related pages and no page tying them together needs a hub: an existing category, a pillar guide, or a new page.
    - The hub links to each supporting page with a sentence of context; each supporting page links back to the hub once, early.
    - Bigger than a handful of pages, or unsure which pages should exist? Hand it to `topic-cluster-map`.
11. **Check the plan before handing it back.**
    - No source over the cap, no self-links, no target linked twice from one source.
    - Every target returns 200, is indexable and is the canonical URL.
    - Every link has a reason a reader would accept, and an exact sentence.
    - Sort by priority, then by the target's business value.

## What to hand back

Fill in this template. Sort links by priority, then by target value. Draft only: don't edit the live site without permission for that change.

```markdown
# Internal linking plan: <site> (<crawl or data date>)

**What I found:** <one plain-English sentence, e.g. 12 pages have no links pointing to them and the pricing page gets 2 links from articles>
**What matters most:** <one sentence>
**What to do first:** <one sentence>

Coverage: <full crawl of n URLs / sitemap + n fetched pages / n pasted pages>

## Priority pages: current support
- <URL> (target: "<query>"): contextual inlinks <n> (site median <n>), template inlinks <n>, depth <n>, avg position <n or not checked>. Evidence: <seen / tool: name / inferred>, <high / medium / low>

## Links to add (<n> total)
### 1. `Fix next`: <source URL> → <target URL>
- Anchor: "<anchor text>"
- Current sentence: "<quote>" (or: new sentence, placed after "<quote>")
- New sentence: "<sentence with the [anchor] in brackets>"
- Reason: <why a reader goes there next, and the problem it fixes: orphan / depth / striking distance / weak support / hub>
- Evidence: <e.g. tool: crawler shows 1 contextual inlink; Search Console avg position 11.4>, <confidence>

## Links to fix
- `Fix now`: <n> pages link to <URL> (404) from <location>. Change to <URL>. Evidence: <...>
- `Fix next`: <n> links point at <URL> (301 → <final URL>). Update the href.

## Orphans and buried pages
- <URL>: <orphan / depth n>, <impressions or none>. Decision: link it / noindex / redirect / remove (ask first). <priority>

## Hubs
- <topic>: hub <URL or "create">. Links missing: hub → <URLs>; <URLs> → hub.

## Leave it
- <what looks wrong but isn't worth changing, and why>

## What I could not check
- <e.g. no crawler, so JavaScript-rendered menus were not seen; no backlink data, so source strength is inferred>
```

## Stop and flag if

- You don't know the priority pages and can't infer them confidently. Ask before planning.
- The crawl is partial (page limit, firewall, robots.txt block, JavaScript links not rendered). Report coverage and don't label pages orphans from it.
- A large share of internal links (say over 10%) point at errors or redirects, or the site has sitewide crawling problems. Run `technical-seo-audit` first; a link plan on broken plumbing is wasted.
- A target page is noindexed, canonicalized to another URL, or splitting its query with another of your pages. Resolve that first.
- The output is unacceptable if any link lacks an exact sentence, if anchors repeat one exact-match keyword across many sources, if links are added only to "pass authority" with no reader reason, or if it proposes editing the live site without permission.

## Next step

- Before shipping the changes, run `seo-change-monitor` on the target pages so you can compare clicks, impressions and position once Google has recrawled the sources.
- For striking-distance targets that already have plenty of relevant links, run `on-page-seo-review` or `search-intent-match` on the target: the problem is the page, not its links.
- If several topics had no hub, run `topic-cluster-map` with the inventory and this plan.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
