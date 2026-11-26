---
name: site-migration-check
description: Plan and verify a domain move, HTTPS switch, URL restructure, platform change, redesign or site merge without losing search traffic. Use for "site migration checklist", "redirect map", "moving to a new domain", "switching CMS", "traffic dropped after relaunch", or a pre-launch SEO go/no-go check.
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/site-migration-check
---

# Site migration check

Plan, check and follow up a site migration so every page that earns clicks,
links or sales keeps a working home. You hand back a risk call, a redirect map,
a go/no-go result for launch, launch-day checks, a monitoring plan for the
following 4 to 12 weeks, and rollback criteria agreed before anyone needs them.

> **Romeo's rule:** Every old URL that earned a click or a link gets a named new
> home before launch, not a guess after the 404 report fills up.

## Use this when

- You're changing domain, merging two sites, moving to HTTPS, or changing URL patterns (`/blog/post` to `/resources/post`).
- You're changing CMS or platform (WordPress to Webflow or Next.js, a move to or from Shopify).
- A redesign changes templates, navigation or content, even if URLs stay the same.
- A launch date is set and someone needs an SEO go/no-go.
- Traffic fell after a migration that already happened: run steps 2, 3 and 7 against the old URL list.

## Don't use this for

- Routine deploys that don't change URLs or templates → `seo-change-monitor`.
- Deciding which overlapping pages to merge → `keyword-cannibalization-check`, then bring its decisions into the redirect map.
- A full health audit of the new site once it has settled → `technical-seo-audit`.
- Designing a new language or country structure → `hreflang-international` first, then come back here to move.

## What you need

### Required
- Migration type, launch date, and old and new domains or URL patterns.
- A list of old URLs: a crawl, the old sitemaps, or a CMS export.
- Access to the new site before launch (staging URL and credentials), or a written spec of it.

### Helpful
- Search Console for every old property: Performance by page (16 months), Links → Top linked pages, Page indexing counts.
- Analytics landing-page sessions and conversions for the last 12 months.
- A backlink export (Ahrefs, Semrush or similar) for pages with external links.
- Server logs, existing redirect rules, and where the new redirects will live (server, CDN, CMS or platform redirect manager) with that system's limits.

### No tools?
- Search Console Performance → Pages, export (1,000 rows in the interface, which covers the pages that matter on most small sites).
- The old XML sitemaps give you the URL list. Build the redirect map in a spreadsheet.
- Test redirects on samples with DevTools Network ("Preserve log") or `curl -sIL <url>`.
- After launch, run URL Inspection on one URL per template in the new Search Console property.

## Ground rules

- Change one thing at a time where you can. Domain, URLs, design and platform all at once make a drop impossible to diagnose. If the business insists, say so and plan closer monitoring.
- Redirect each old URL to its closest equivalent: same topic, same intent. Merging several pages into one that covers them is fine. Sending everything to the homepage or a category can be treated as a soft 404 and throws away relevance.
- No equivalent and no links: a 404 or 410 is honest and better than an irrelevant redirect. If the URL has links, find the nearest page that genuinely serves the same need.
- Server-side 301 or 308, one hop, from every old variant (`http`, `www`, trailing slash, case, parameters) straight to the final URL.
- Keep every URL that doesn't need to change. A changed URL carries risk and no benefit of its own.
- Keeping the URL isn't enough. Titles, H1s, main copy, internal links, structured data, image URLs and alt text must survive too; a redesign that drops them is a migration in disguise.
- Expect a wobble. Google says a medium-sized site can take a few weeks or more before new URLs show, longer for big sites, with temporary ranking fluctuation. Judge trends against the benchmark, not the first few days.
- Keep redirects as long as possible. Google's site-move guide says generally at least a year; its Change of Address help says at least 180 days, longer while Google still sends traffic. Default to permanent, and keep the old domain registered so nobody else can buy it and take over your redirects.
- Read-only by default. Draft redirect rules, robots.txt and settings; never deploy, change DNS or file a Change of Address without explicit permission for that action.

## Steps

1. **Classify the move and its risk.**
   - Type: domain, HTTPS, URL restructure, platform, redesign, merge, or a combination. Each extra change adds risk and slows diagnosis.
   - Risk rises with: share of URLs changing, templates changing, rendering moving from server HTML to client-side JavaScript, content being cut, and launch during peak season.
   - Platforms that force URL patterns (Shopify's `/products/` and `/collections/` paths, for example) make some URL changes unavoidable. Map those early.
   - Large sites: recommend moving one section first, ideally one that changes rarely, so problems show early and small.

2. **Benchmark the old site before anything changes.**
   - Crawl every URL: status, indexability, canonical, title, meta description, H1, internal inlinks, depth, structured data types, hreflang, and rendered main content.
   - Search Console: Performance by page and by query for 16 months (the interface exports 1,000 rows; use the API or a Looker Studio connector for more), Page indexing counts, Top linked pages, Core Web Vitals status.
   - Analytics: sessions and conversions by landing page, 12 months.
   - Save robots.txt, sitemaps and existing redirect rules. Old redirects must survive and be flattened.
   - If a rank tracker is available, snapshot positions for the top queries; otherwise Search Console average position by page is the baseline.
   - Tag each old URL with clicks, linking domains and conversions. These set its priority in the map.

3. **Build the redirect map.** One row per old URL that has clicks, links, conversions, or sits in a sitemap, plus images, PDFs and other files with traffic or links.
   - Match type: `1:1` (same content), `merged` (several old pages, one new page covering them), `nearest` (for example a discontinued product with links to its parent category), `retired` (410, no equivalent and no value).
   - Flatten existing rules so A → B → C becomes A → C, and point every old host and protocol variant directly at the final URL.
   - Use pattern rules for large uniform sets, but test them against the full URL list and put exceptions above the pattern.
   - Decide query strings: pass tracking parameters through, drop session parameters.
   - A human checks the top 100 URLs by clicks and the top 50 by links, row by row.
   - Template (CSV, one row per old URL):

   ```csv
   old_url,clicks_12m,linking_domains,conversions_12m,new_url,match_type,code,tested,notes
   https://old.example.com/blog/seo-tips,4210,38,12,https://www.example.com/guides/seo-tips/,1:1,301,,
   https://old.example.com/blog/seo-tips-2023,310,2,0,https://www.example.com/guides/seo-tips/,merged,301,,folded into main guide
   https://old.example.com/product/blue-widget,120,4,3,https://www.example.com/widgets/,nearest,301,,discontinued
   https://old.example.com/tag/misc,0,0,0,,retired,410,,no equivalent and no links
   ```

   - `tested` is filled in later with what actually happened, for example `301>200` or `404`.

4. **Check the new site on staging.** Compare each template with the benchmark.
   - Staging protection: HTTP authentication or an IP allowlist is best, because it keeps staging out of every index. If staging uses `noindex` or `Disallow: /` instead, list each one for removal at launch.
   - Parity: titles, H1s, main content, internal link counts, structured data, image alt text, breadcrumbs, pagination.
   - Canonicals are self-referencing, absolute, and use the final production host, never the staging host.
   - Hreflang points to new URLs and keeps its return links. Internal links point straight at new URLs, not at old ones relying on redirects.
   - New XML sitemaps list only new, canonical, 200 URLs. The 404 page returns a real 404 status.
   - HTTPS moves: every image, script and embed loads over `https://` (no mixed content), and canonicals, hreflang and sitemaps use `https://` URLs.
   - Rendering: compare raw and rendered HTML for main content and links, especially when moving to a JavaScript framework.
   - Speed: run lab tests on the new templates and the old ones. Launching slower templates is a decision to make knowingly, not a surprise.
   - Analytics tags and Search Console verification carried over; new properties verified before launch (a Domain property covers every host and protocol).

5. **Pre-launch go/no-go.** If the new redirects can run on staging or a test host, request every old URL in the map.
   - Pass: every row returns one 301 or 308 to its mapped URL, which returns 200; retired rows return 410 or 404.
   - No-go: any failure among the top 100 URLs by clicks, any template with a canonical or `noindex` problem, or a sitemap listing staging URLs.
   - Record the result in the map's `tested` column and hand the user a clear go or no-go.

6. **Launch day.**
   - Remove staging blocks: authentication, `Disallow: /`, meta `noindex`, `X-Robots-Tag: noindex` (check response headers at the CDN too), and any canonical, hreflang, sitemap or structured data URL that still points to staging.
   - Deploy redirects, then rerun the full old-URL list and the host variants against production at once.
   - New robots.txt is correct and has a `Sitemap:` line. The old host must not disallow old URLs; Google has to crawl them to see the redirects.
   - Submit the new sitemaps in Search Console and Bing Webmaster Tools. Keep the old sitemap submitted for a few weeks so Google recrawls the old URLs; warnings about redirects in it are expected.
   - Domain or subdomain moves only: Change of Address in Search Console from each old property (you must own both properties under the same Google account, and the old homepage must 301 to the new one). Google now asks for it on every verified variant of the old domain, `www`, non-`www` and other subdomains, even ones you don't use. It runs for 180 days. Don't use it for HTTPS, `www` or path changes. Bing Webmaster Tools has its own site move tool; check its current steps in Bing's help.
   - URL Inspection live test on one URL per template in the new property.
   - Update what you control outside the site: Google Business Profile, ad final URLs, social profiles, email templates, and ask the top linking sites to update their links.

7. **Monitor for 4 to 12 weeks.**
   - First week, daily: Googlebot and user 404s and 5xx in logs or a recrawl, hits on old URLs missing from the map (add rows), Page indexing and Crawl stats in the new property.
   - Then weekly to week 12: clicks and impressions for old and new properties combined, against the benchmark for the same weeks, allowing for seasonality; new URLs indexed rising; old URLs moving to "Page with redirect"; the top 100 URLs one by one; conversions.
   - Normal: old-property clicks falling as new-property clicks rise, short-lived ranking swings, old URLs listed as "Page with redirect".
   - Not normal: new URLs marked `noindex`, blocked or soft 404; "Duplicate, Google chose different canonical than user" choosing old URLs (a redirect or canonical is wrong); combined clicks still well below benchmark after most URLs have been recrawled, with no seasonal explanation.

8. **Agree rollback criteria before launch.**
   - Fixing forward is usually better. Once Google has started processing the redirects, rolling back is a second migration.
   - Rollback candidates: checkout or lead forms broken and not fixable within hours; the new platform can't serve pages reliably (sustained 5xx); redirects fundamentally broken with no quick fix; a legal or security problem.
   - Not rollback reasons: a dip in the first weeks within the expected wobble; a few missed redirects (add them).
   - Write down who decides, using which numbers, and by when.

## What to hand back

Fill in the parts that match the stage you were asked about.

```markdown
What I found: <one sentence>
What matters most: <the biggest risk and the traffic or URLs it puts at stake>
What to do first: <one concrete action>

Move: <old> → <new>, checked <date>
Type: <domain | HTTPS | URL restructure | platform | redesign | merge>. Risk: <low | medium | high>, because <reason>
Go/no-go: <go | no-go | not tested>, based on <what was tested>

### Blockers and fixes
- [Fix now] <plain-English problem (term)>. Affects: <URLs/template, clicks at stake>.
  Evidence: <seen|tool|inferred>, <high|medium|low>: <example URL and response>.
  Fix: <exact change>.

### Redirect map
- Rows: <n> (1:1 <n>, merged <n>, nearest <n>, retired <n>). Tested OK: <n of n>
- Top-100 URLs by clicks mapped and tested: <yes | no, list gaps>

### Launch-day checks
- <check>: <pass | fail | not checked>

### Monitoring plan
- <dates, metrics, benchmark figures, owner>

### Rollback criteria
- <trigger, decider, deadline>

### What I could not check
- <item>: <what would verify it>
```

## Stop and flag if

- There's no list of old URLs and no Search Console or analytics data: say the map can't be complete, and ask for the data before launch rather than after.
- The plan sends many old URLs to the homepage, or launches with no redirects at all: mark it as a no-go and explain the traffic at stake.
- You're asked to deploy redirects, change DNS, edit robots.txt or file a Change of Address: draft it and ask permission for that specific action.
- Unacceptable output: a map missing any of the top pages by clicks or links, untested redirect rules reported as working, or recovery promises with dates.

## Next step

- `seo-change-monitor` with the benchmark from step 2, to compare each week after launch.
- `technical-seo-audit` on the new site once most URLs have been recrawled.
- `internal-linking-plan` if the new navigation dropped links to pages that used to rank.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
