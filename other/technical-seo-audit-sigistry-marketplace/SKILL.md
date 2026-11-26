---
name: technical-seo-audit
description: Check whether search engines can reach, render, index and pick the right URL for your pages, and whether they are fast on a phone. Use for "technical SEO audit", "why is this page not indexed", "crawled currently not indexed", "check my robots.txt", canonical or redirect problems, or Core Web Vitals.
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/technical-seo-audit
---

# Technical SEO audit

Find what stops search engines from reaching, rendering, indexing and choosing
the right version of your pages, and what makes them slow or broken on a phone.
You hand back a short, prioritised fix list grouped under four questions: can it
be reached, can it be indexed, is the right URL chosen, is it fast and usable.

> **Romeo's rule:** Find the one setting that hides ten thousand pages before
> you argue about the one page that loads slowly.

## Use this when

- Pages are missing from Google, or Search Console's "Not indexed" count is large or growing.
- Traffic fell right after a deploy, redesign, CMS update, CDN or hosting change.
- A new site or section launched weeks ago and nothing from it shows in search.
- Search Console shows an indexing reason or Core Web Vitals status you don't understand.
- You're about to invest in content and want to know the site can carry it.

## Don't use this for

- Moving domains, URLs or platforms → `site-migration-check` (then run this on the new site).
- One page's title, headings and content → `on-page-seo-review`.
- Rules for AI crawlers, llms.txt and agent access → `ai-agent-readiness`.
- A traffic drop with no technical cause in sight → `seo-performance-audit`.

## What you need

### Required
- The root URL, plus which sections or templates make money (product, blog, docs).
- Either the ability to fetch URLs and read response headers, or pasted HTML and headers.

### Helpful
- Search Console exports: Page indexing (per reason), Core Web Vitals, Crawl stats, Sitemaps, URL Inspection for key URLs.
- A crawler export (Screaming Frog, Sitebulb or similar) with status, indexability, canonical, depth, inlinks, and raw vs rendered HTML.
- 30 days of server logs filtered to verified Googlebot (reverse DNS or Google's published IP ranges).
- Bing Webmaster Tools Site Scan. The CMS, framework and CDN in use, since many defects are platform defaults.

### No tools?
- Open `/robots.txt` in a browser. Use `view-source:` for raw HTML and DevTools Elements for the rendered DOM.
- DevTools Network with "Preserve log" on shows every redirect hop, status code and `X-Robots-Tag` header.
- Rich Results Test works on any public URL without ownership; "View tested page" shows Google's rendered HTML and a screenshot.
- PageSpeed Insights: the top block is field data from real Chrome users, the lower block is a lab test.
- Search Console Page indexing: open each reason and export (up to 1,000 example URLs per reason).
- Treat `site:` searches as a rough sanity check, never as an index count.

## Ground rules

- Rank by scale times severity. A sitewide `noindex` outranks every speed issue; a template defect outranks a one-off URL.
- Read raw HTML and headers first. Status codes, `X-Robots-Tag` and meta robots are read before rendering and can stop rendering from happening.
- robots.txt controls crawling, not indexing. A disallowed URL can still be indexed from links, without content, and its `noindex` is never seen.
- Canonicals, redirects, sitemaps, hreflang and internal links are votes. Google weighs them; your job is to make them all name the same URL.
- "Not indexed" is often correct. Filtered views, internal search and true duplicates should stay out. Ask "should this URL be indexed?" before calling it a bug.
- Field data decides Core Web Vitals; lab data is for diagnosis. No field data means "not enough data", not "passing".
- Fix the source: a redirected internal link is fixed by editing the link, not by adding another redirect.
- Don't send anyone to retired tools: the URL Parameters tool (2022), the robots.txt Tester (replaced by the robots.txt report in 2023), the Mobile-Friendly Test (2023), the crawl rate setting (2024).

## Steps

1. **Scope and sample.** Count URLs and templates before you crawl.
   - Under about 10,000 URLs: crawl everything with JavaScript rendering on.
   - Larger: list templates (home, category, product, article, tag, search, pagination, filters) and sample 20 to 50 URLs per template, mixing top pages from Search Console Performance with random long-tail URLs. Crawl big sections with a page cap.
   - A defect on 3+ sampled URLs of one template is a template defect. Report it as "likely on all N URLs of this template" (`inferred`) and say how to confirm.
   - Per section, collect three counts: URLs in sitemaps, indexable URLs found by crawl, indexed (Page indexing filtered by sitemap). The biggest gap tells you where to dig.
   - With verified Googlebot logs, compare hits per section with each section's value. Crawling spent on parameters and old redirects while key templates go unvisited is the clearest evidence of crawl waste.

2. **Can it be reached: robots.txt.** Every host (www, non-www, each subdomain) has its own file.
   - It must return 200, or 404 for "no rules". A 5xx or 429 makes Google treat the whole site as disallowed for about 12 hours, then fall back to its last cached copy: `Fix now`.
   - Google reads `user-agent`, `allow`, `disallow` and `sitemap`, with `*` and `$` wildcards. The longest matching path wins; on a tie the less restrictive rule wins. `crawl-delay` and `noindex` lines are ignored by Google. Content past 500 KiB is ignored.
   - Look for `Disallow: /` left over from staging, and blocked CSS, JS or image paths (`/_next/`, `/wp-includes/`, `/assets/`) that the page needs to render: `Fix now` if main content or layout disappears.
   - Rules match by prefix: `Disallow: /blog` also blocks `/blog-pricing`. Check every disallow against real URLs.
   - Blocking is right for internal search results, cart, checkout, account, admin and endless filter or sort combinations.
   - AI bot groups (GPTBot, ClaudeBot, Google-Extended) are policy for `ai-agent-readiness`. Only flag them here if a rule accidentally catches Googlebot or Bingbot.

3. **Can it be reached: status codes and redirects.**
   - Every URL you want indexed returns 200 directly. Check the server's response, not the page the browser ends up on.
   - 5xx and timeouts make Google slow its crawl and eventually drop URLs that keep failing. Recurring 5xx on indexable templates: `Fix now`. Check Crawl stats, "By response", for the trend.
   - 401 or 403 on public pages, usually a WAF, bot challenge or country block (Googlebot mostly crawls from US IPs): `Fix now`.
   - Internal links to 4xx: `Fix next`, or `Fix now` when they sit in navigation or on many pages. A 404 or 410 for a page that's truly gone is correct.
   - Soft 404s: a 200 that is really empty or an error (empty category, "no results", SPA "not found" view, thin out-of-stock template). Return 404 or 410, or give the page real content.
   - Permanent moves use 301 or 308, a strong signal that the target is the URL to index. 302 and 307 are weak signals and keep the old URL as a candidate. A 302 standing in for a permanent move for months: `Fix next`.
   - Googlebot follows up to 10 hops, but each costs crawl and latency. More than one hop from internal links or important old URLs: `Fix next`. Loops: `Fix now`.
   - Instant meta refresh counts as permanent, delayed as temporary. JavaScript redirects only work when rendering succeeds. Prefer server-side.

4. **Can it be reached: links, depth and crawl traps.**
   - Google follows `<a href="/real-path">`. It does not follow `onclick` handlers, buttons, `href="#"`, `javascript:` links or `#/route` fragment URLs.
   - Pages that should rank but sit 5+ clicks from the homepage, or are reachable only through pagination or site search, tend to be crawled rarely (a rule of thumb, not a Google threshold). Send orphans and deep pages to `internal-linking-plan`.
   - Crawl traps: filter and sort combinations, endless calendar "next month" links, session IDs or `utm_` parameters on internal links, relative-link bugs that build `/a/b/a/b/` paths, linked internal search pages.
   - Signs of a trap: the crawl never ends, thousands of near-identical URLs, Crawl stats dominated by parameter URLs, "Discovered - currently not indexed" piling up.
   - Fixes from strongest to weakest: stop generating the links (or move filters into a `#` fragment), disallow the pattern in robots.txt, return 404 for empty or nonsensical combinations. `rel=canonical` and `nofollow` reduce trap crawling only slowly.

5. **Can it be indexed: robots directives.**
   - Check both `<meta name="robots">` (and `googlebot`) in the HTML and the `X-Robots-Tag` response header. The header is how PDFs get noindexed, and how some CDNs and hosts noindex preview domains.
   - The most restrictive rule wins, and a `googlebot` tag adds to the generic one.
   - `noindex` on a page that should rank: `Fix now`. A `noindex` in raw HTML that JavaScript later removes may never be noticed, because Google can skip rendering once it sees `noindex`.
   - `nosnippet` (or `max-snippet:0`, its equivalent) also stops the content being used directly in Google's AI Overviews and AI Mode. Flag it if it looks accidental. Excluding the property under Search Console's Settings → Search generative AI (sites are included by default) keeps it out of those features too; check it if AI visibility vanished.
   - `noarchive` and `nocache` do nothing in Google Search today: `Leave it` for Google. Bing still reads them as Copilot controls until 1 March 2027, so check whether they were set on purpose before removing them.
   - A URL that is both disallowed and `noindex`ed: the `noindex` is invisible. To get it out of the index, allow crawling until it drops, then decide whether to block.

6. **Can it be indexed: rendering and mobile parity.**
   - Per template, compare raw HTML with the rendered DOM (URL Inspection live test, Rich Results Test, or a rendering crawler). Check main content, H1, title, canonical, meta robots, internal links, structured data.
   - Main content or key links present only after rendering: Google can usually index them, but later and less reliably, and many other crawlers (most AI crawlers included) don't run JavaScript. `Fix next` on revenue templates; recommend server-side rendering or static generation.
   - Content that needs a click, typing or a cookie-banner choice to appear is not seen. Content in tabs and accordions is fine if it is in the HTML.
   - Canonical, meta robots or title that differ between raw and rendered HTML: `Fix now` when they conflict. JavaScript must not change a canonical that exists in the HTML.
   - Non-200 pages may not be rendered, so a single-page app's error view needs a real 404 status or a JavaScript-added `noindex`.
   - Google indexes the mobile version. Compare mobile and desktop rendered HTML for main content, headings, structured data, internal links, image alt text and robots tags. Anything missing on mobile is effectively missing from Google: `Fix now` if it's main content.

7. **Can it be indexed: read the Page indexing reasons.** Name the cause of each big bucket before recommending anything.
   - "Crawled - currently not indexed": Google fetched the page and chose not to index it, for now. Usually a value or duplication call on that page or template. Fix with distinct content, merging, or stronger internal links; re-requesting indexing rarely helps.
   - "Discovered - currently not indexed": Google knows the URL but hasn't fetched it. Usually crawl priority or capacity: too many low-value URLs, a slow server, weak internal links. Fix traps, speed and linking; don't rewrite content Google hasn't read. On small sites crawl budget is rarely the cause (Google's crawl budget guide is aimed at roughly 1M+ pages, or 10,000+ changing daily), so look at internal links and perceived value first.
   - "Duplicate without user-selected canonical": no canonical declared and Google picked another URL. Add canonicals or make the page distinct.
   - "Duplicate, Google chose different canonical than user": your canonical lost the vote. Compare both URLs in URL Inspection; usually internal links, sitemaps or redirects point the other way, or the pages aren't really duplicates.
   - "Alternate page with proper canonical tag": expected for variants. `Leave it`.
   - The noindex, robots.txt, redirect, 404, soft 404, 5xx and 401/403 reasons: check whether each URL should be indexed at all. Old redirected and deleted URLs listed here are normal history.
   - "Indexed, though blocked by robots.txt": decide. To index it, unblock; to remove it, unblock and add `noindex`.
   - "Page indexed without content": Google got an empty page, often a bot challenge or failed render. `Fix now` on important URLs.
   - Each reason exports at most 1,000 example URLs, so shares computed from them are `inferred`. Validation can take about two weeks.

8. **Is the right URL chosen: canonicals.**
   - Each indexable page has one `<link rel="canonical">` inside `<head>`, with an absolute URL, pointing to itself unless it's a true duplicate. Use the HTTP `Link` header only for non-HTML files like PDFs, and never both with different values.
   - Problems: missing on parameter-heavy templates (`Fix next`); multiple or conflicting canonicals, which Google may ignore entirely (`Fix now` on templates); canonical pointing to a redirect, 404, noindexed or blocked URL (`Fix now`); canonical in `<body>`, which is ignored (`Fix next`); every page pointing to the homepage (`Fix now`); relative canonicals that resolve to a staging host (`Fix now`).
   - Canonical plus `noindex` on one page gives opposite instructions. Pick one: canonical for duplicates you want merged, `noindex` for pages you want gone.
   - Paginated pages canonicalise to themselves, not to page 1. `rel=prev/next` isn't used by Google: `Leave it` if present, don't add it.
   - Agreement check: canonical, sitemap entry, internal links, hreflang targets and redirect targets should all name the same URL.

9. **Is the right URL chosen: host, protocol and URL variants.**
   - Request `http://` and `https://`, `www` and non-`www`, for the homepage and one deep URL. All should reach one HTTPS host with a single 301. Two variants both returning 200: `Fix now`.
   - Trailing slash, uppercase, `index.html`, double slashes and tracking parameters should each resolve to one URL by redirect or canonical. `/page` and `/page/` are different URLs to Google.
   - HTTPS: a valid certificate on every host, no HTTPS-to-HTTP redirects, and `https://` in canonicals, hreflang, sitemaps and internal links.
   - Mixed content (HTTP scripts, images or iframes on HTTPS pages): browsers block scripts and iframes (`Fix now` if something breaks) and upgrade or block images (`Fix next`).
   - HSTS is good hygiene, not a ranking lever: `Worth doing`.

10. **Is it fast and usable: Core Web Vitals.**
    - Start with field data: Search Console's Core Web Vitals report (mobile and desktop separate, similar URLs grouped) and the top block of PageSpeed Insights or the CrUX API (opted-in Chrome users, rolling 28 days, 75th percentile).
    - Good: LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1. Poor: LCP > 4 s, INP > 500 ms, CLS > 0.25. These have held since INP replaced FID in March 2024; check web.dev if you suspect a change.
    - Low-traffic URLs have no page-level field data and PageSpeed Insights falls back to the whole origin. Say which level you used. Never estimate field numbers.
    - A lab page-load test can't measure INP; Total Blocking Time is the proxy. A Lighthouse score of 60 with passing field data is `Leave it`.
    - Name the cause per template: LCP image lazy-loaded or discovered late, slow server response, render-blocking CSS or fonts; INP from heavy third-party scripts or long hydration tasks; CLS from images, ads, embeds or banners without reserved space.
    - Poor field data on templates that earn traffic is `Fix next`. It's `Fix now` only when pages are close to unusable; indexing defects come first.
    - Usability: a missing `<meta name="viewport">` is `Fix now`; pop-ups that cover the content on mobile entry are `Fix next`.

11. **Write it up.** Group findings under the four questions, order by priority, merge repeats into template-level findings, and give each a fix a developer can act on: the file, setting, rule or exact header to change, and how to verify it.

## What to hand back

Fill this in. Every finding names URLs or a template, a count, and evidence.

```markdown
What I found: <one sentence>
What matters most: <the biggest blocker and how many URLs it touches>
What to do first: <one concrete action>

Site: <site>, checked <date>
Scope: <full crawl | sample of N URLs across M templates>, rendering <on/off>
Data used: <crawl, Search Console exports, logs, PageSpeed Insights, none>
Counts: in sitemaps <n> | indexable in crawl <n> | indexed <n or "not checked">

### 1. Can it be reached
- [Fix now] <plain-English problem (term)>. Affects: <template/URLs, count>.
  Evidence: <seen|tool|inferred>, <high|medium|low>: <what you saw, example URL>.
  Fix: <exact change>. Verify: <how to confirm it worked>.

### 2. Can it be indexed
- ...

### 3. Is the right URL chosen
- ...

### 4. Is it fast and usable
- ...

### Looks wrong, leave it
- <item>: <why it isn't worth the time>

### What I could not check
- <item>: <what would verify it>
```

## Stop and flag if

- robots.txt or the homepage returns 5xx, or Googlebot is blocked sitewide: report it at once as an outage, not as item 7 of a list.
- You're asked to change robots.txt, redirects, CDN rules, headers or Search Console settings: draft the change and ask permission for that specific change.
- You can't tell which URLs are meant to be indexed: ask before calling exclusions errors.
- Fetches hit a bot challenge or login wall: say so, and don't audit the challenge page as if it were the site.
- Unacceptable output: Core Web Vitals numbers without a named source, index counts from `site:`, findings without evidence labels, or checklist items that name no URL or template.

## Next step

- `xml-sitemap-check` with the list of URLs this audit says should be indexed.
- `internal-linking-plan` with the orphan and deep pages found here.
- `seo-change-monitor` to snapshot the fixed state before the next deploy.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
