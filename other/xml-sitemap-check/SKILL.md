---
name: xml-sitemap-check
description: Validate your XML sitemaps against the pages that should actually be indexed, and generate a clean one from a page inventory. Use for "check my sitemap", "sitemap errors in Search Console", "submitted URL not indexed", "sitemap couldn't fetch", lastmod questions, or building a sitemap for a custom site.
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/xml-sitemap-check
---

# XML sitemap check

Check every sitemap the site exposes against what should really be in search:
canonical, indexable pages that return 200. You hand back what to remove, what
is missing, whether `lastmod` can be trusted, how the sitemap, crawl and index
counts compare, and, if asked, a spec for a clean sitemap generated from the
page inventory.

> **Romeo's rule:** A sitemap is a list of promises; every URL in it should be
> one you'd be glad to see indexed today.

## Use this when

- Search Console's Sitemaps report shows errors, "Couldn't fetch", or far fewer indexed pages than submitted.
- New or updated pages take weeks to be crawled.
- After a migration, CMS switch, plugin change or URL restructure.
- You generate the sitemap yourself (static site, headless CMS, custom app) and want it right first time.

## Don't use this for

- Diagnosing why indexable pages still aren't indexed → `technical-seo-audit`.
- Deciding which pages should exist, merge or go → `site-content-inventory`, then `keyword-cannibalization-check`.
- Planning languages and regions (not just their sitemap annotations) → `hreflang-international`.
- Alt text, formats and image discoverability on the page → `image-seo`.

## What you need

### Required
- The site URL, plus any sitemap URLs you know of.
- The ability to fetch the sitemaps and sample URLs, or their pasted contents.

### Helpful
- A page inventory from `site-content-inventory` saying which URLs should be indexed.
- A crawler export with status, indexability and canonical for every URL.
- Search Console: Sitemaps report, and Page indexing filtered by each sitemap.
- Bing Webmaster Tools Sitemaps report.
- The generator in use (Yoast, Rank Math, a framework sitemap package, a platform's automatic sitemap), since most fixes happen there, not in the XML.

### No tools?
- Open `/robots.txt` and look for `Sitemap:` lines. Then try `/sitemap.xml`, `/sitemap_index.xml`, `/sitemap-index.xml` and `/wp-sitemap.xml`.
- Use `view-source:` to read the raw XML; the browser's pretty view can hide encoding errors.
- Paste the `<loc>` values into a spreadsheet and spot-check 20 to 50 across every child sitemap with DevTools Network: status, final URL, canonical, robots meta.
- In Search Console, open Page indexing and switch the filter from "All known pages" to "All submitted pages" or a single sitemap.
- For a few hundred URLs, a spreadsheet and patience is enough.

## Ground rules

- A sitemap helps discovery and hints at your preferred URL; it doesn't make Google index anything. Google treats sitemap inclusion as a weak canonical signal.
- List only URLs you want in search: canonical, 200, indexable, not blocked. Every other URL adds noise to your reports and spends crawl on nothing.
- Of the optional `<url>` fields, Google uses only `lastmod`, and only when it's consistently and verifiably accurate. A `lastmod` that changes on every build teaches Google to ignore it. Bing calls `lastmod` a key freshness signal too.
- Google and Bing ignore `<priority>` and `<changefreq>`. Their presence is harmless: `Leave it`. Never spend time tuning them.
- On a small, well-linked site, a sitemap is rarely the reason pages aren't indexed. Don't oversell sitemap fixes.
- Generate sitemaps from the source of truth (database or CMS), not by crawling your own site and listing whatever turned up.
- Google's sitemap ping endpoint is gone (deprecated in 2023). Use Search Console, the robots.txt `Sitemap:` line, and IndexNow for Bing and other engines that support it.

## Steps

1. **Find every sitemap.**
   - robots.txt `Sitemap:` lines: absolute URLs, any number, anywhere in the file, and they may point to another host.
   - Sitemaps submitted in Search Console and Bing Webmaster Tools, common paths, and CMS or plugin defaults.
   - Flag leftovers: sitemaps from an old plugin, old domain or retired subdomain that are still reachable or submitted. They keep feeding stale URLs and confuse the reports.
   - Two generators running at once (a plugin plus the platform's built-in sitemap) is a common cause of duplicates: `Fix next`.

2. **Validate each file.**
   - Returns 200 directly with an XML content type (`text/plain` for a `.txt` sitemap). A single-page app that answers `/sitemap.xml` with its HTML shell and a 200 is a classic failure: `Fix now`.
   - The sitemap file itself isn't disallowed in robots.txt. An `X-Robots-Tag: noindex` on the sitemap file is fine and common: `Leave it`.
   - Well-formed XML, UTF-8, namespace `http://www.sitemaps.org/schemas/sitemap/0.9`. Entities escaped: `&` must be `&amp;`, which breaks most often in parameter URLs.
   - Limits per file: 50,000 URLs and 50 MB uncompressed. Gzip is fine, but the limit applies to the uncompressed size. Each `<loc>` under 2,048 characters.
   - An index file lists up to 50,000 sitemaps as `<sitemap><loc>`, with optional `<lastmod>`. Keep it one level deep (an index lists sitemaps, not other indexes). Search Console accepts up to 500 index files per site.
   - URLs are absolute, with protocol, on the same host and protocol as the sitemap. A sitemap at `/blog/sitemap.xml` only covers `/blog/` unless it's submitted in Search Console. Cross-host sitemaps need verified ownership or a `Sitemap:` line in the target host's robots.txt.
   - `lastmod` uses W3C Datetime: `2026-10-14` or `2026-10-14T09:30:00+00:00`.

3. **Check every listed URL against indexability.** On huge sites, sample at least 1,000 URLs spread across every child sitemap.
   - Returns 200 directly. A redirect means list the final URL instead; a 4xx or 5xx means remove the URL or fix the page.
   - Not `noindex` (meta tag or `X-Robots-Tag` header) and not disallowed in robots.txt.
   - Canonical points to itself. If it points elsewhere, the sitemap should list that canonical, not this URL.
   - Exact variant match: protocol, host, trailing slash and case identical to the canonical. `http://` or a missing slash on every entry is one generator setting: `Fix next`.
   - No parameter, filter, sort, internal-search, session or staging URLs.
   - Rough severity: a few stray URLs from content churn is `Worth doing`; a whole template or child sitemap that's wrong is `Fix next`; a sitemap full of redirects, noindexed URLs, staging or another site's URLs is `Fix now`.

4. **Find what's missing.** Compare the sitemap with the inventory or crawl.
   - List indexable, canonical, 200 URLs with internal links that appear in no sitemap, grouped by template.
   - Usual gaps: page types the plugin doesn't know about (landing pages, docs, programmatic pages), a second app on another subdomain, generators that stop at a fixed count, and pages only reachable through JavaScript routing.
   - Sitemap URLs with no internal links at all are orphans. Note them for `internal-linking-plan`; the sitemap is not a substitute for links.

5. **Test whether `lastmod` is honest.** Sample 10 to 20 URLs and compare each `lastmod` with the page's real last content change.
   - Red flags: every URL shares one timestamp; `lastmod` equals the sitemap's generation time; it changes when only a footer, copyright year or related-posts block changed; dates in the future.
   - A missing `lastmod` is better than a dishonest one: `Worth doing` to add, `Fix next` to correct when it's wrong across a template.
   - Fix at the source: set `lastmod` from the content record's last meaningful update (main content, structured data or links), not from deploy or cache times.

6. **Compare sitemap, crawl and index counts.** Get three numbers per section.
   - In sitemap; indexable URLs found by crawl; indexed, from Page indexing filtered to that sitemap. Splitting sitemaps by section or template is what makes per-section index rates visible.
   - Sitemap much larger than crawl: stale entries or orphans. Crawl much larger than sitemap: the sitemap is incomplete.
   - Sitemap and crawl agree but indexed is far lower: not a sitemap problem. Read the reasons. "Discovered - currently not indexed" points to crawl priority; "Crawled - currently not indexed" points to page value or duplication. Hand both to `technical-seo-audit`.
   - Never use `site:` result counts. Write "not checked" if Search Console data wasn't provided.

7. **Check submission and discovery.**
   - robots.txt on each host references the sitemap index with an absolute URL.
   - Search Console Sitemaps report: status "Success", sensible discovered-URL count, recent "Last read" date. Bing Webmaster Tools: submitted and read recently (Bing usually rereads submitted sitemaps at least daily).
   - "Couldn't fetch" right after submitting often just means not read yet. If it persists for days, request the file as a bot would and check the status code, redirects, and WAF or bot-protection rules.
   - IndexNow can tell Bing and other participating engines about added, changed and deleted URLs as they happen. It complements sitemaps rather than replacing them; Google is not an IndexNow participant at the time of writing.
   - Remove dead submissions from old plugins or domains. After a migration, keeping the old sitemap submitted for a while is deliberate; see `site-migration-check`.

8. **Check special sitemaps only where they earn their place.**
   - Images: Google now uses only `<image:image>` and `<image:loc>` (caption, title, geo_location and license were dropped in 2022), up to 1,000 images per URL. Worth it when images load through JavaScript or image search matters. CDN-hosted images are allowed; check Google's current docs for any verification needs.
   - Video: `<video:thumbnail_loc>`, `<video:title>`, `<video:description>` and `<video:content_loc>` or `<video:player_loc>`. Google indexes video mainly from pages where the video is the main content, so don't annotate pages with a decorative embed.
   - News: only for publishers in Google News. Articles from the last two days, at most 1,000 `<news:news>` entries per sitemap, with publication name, language, publication date and title. Update the same file rather than creating new ones.
   - hreflang: `<xhtml:link rel="alternate" hreflang="..." href="...">` inside each `<url>`, listing itself and every alternate, with `xmlns:xhtml="http://www.w3.org/1999/xhtml"` declared. Annotations add file size fast: a 20-locale site hits 50 MB well before 50,000 URLs. Use one hreflang method across the site and plan it with `hreflang-international`.

9. **Generate a clean sitemap (when asked).**
   - Inclusion rule: status 200 AND indexable AND self-canonical AND not disallowed AND meant for search, taken from the inventory.
   - Split by section or template under one index, and stay well under the limits (for example 10,000 to 45,000 URLs per file) so growth doesn't break it.
   - `lastmod` from the content's real update field. Omit `priority` and `changefreq`.
   - Regenerate on publish, unpublish, redirect and noindex events, so a removed URL leaves the sitemap in the same release.
   - Minimal shapes to hand to a developer, the index at `/sitemap.xml` and one child:

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
     <sitemap><loc>https://www.example.com/sitemaps/blog.xml</loc>
       <lastmod>2026-10-28T09:12:00+00:00</lastmod></sitemap>
   </sitemapindex>
   ```

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
     <url><loc>https://www.example.com/blog/crawl-budget/</loc>
       <lastmod>2026-10-14</lastmod></url>
   </urlset>
   ```

## What to hand back

Fill this in. Name the generator setting to change, not only the bad URLs.

```markdown
What I found: <one sentence>
What matters most: <the biggest problem and how many URLs it affects>
What to do first: <one concrete action, at the generator or CMS level>

Site: <site>, checked <date>
Sitemaps found: <URL, URL count, where found (robots.txt / Search Console / guessed)>
Counts: in sitemaps <n> | indexable canonical 200 <n> | indexed <n or "not checked">
lastmod: <trustworthy | partly | not trustworthy | missing>, based on <n> samples

### Fixes
- [Fix now] <plain-English problem (term)>. Affects: <file or section, count>.
  Evidence: <seen|tool|inferred>, <high|medium|low>: <example URLs>.
  Fix: <change at the generator, plugin or template>.

### Missing from sitemaps
- <template or section>: <n> indexable URLs, e.g. <URL>

### Looks wrong, leave it
- <item>: <why>

### Clean sitemap plan (if requested)
- Index: <URL>. Children: <file: inclusion rule, approx. URL count>
- lastmod source: <field>. Regenerated on: <events>

### What I could not check
- <item>: <what would verify it>
```

## Stop and flag if

- A sitemap lists staging, localhost or another company's URLs: report it as `Fix now` before anything else.
- You can't tell which URLs are meant to be indexed (no inventory, contradictory canonicals): ask before removing anything.
- You're asked to submit or delete sitemaps in Search Console or Bing, or to edit robots.txt: draft it and ask permission for that specific change.
- Unacceptable output: calling URLs "indexed" without Search Console data, a generated sitemap that includes non-canonical or redirected URLs, or advice to tune `priority` and `changefreq`.

## Next step

- `technical-seo-audit` with the canonical 200 URLs that are submitted but not indexed, grouped by Page indexing reason.
- `internal-linking-plan` with the orphan URLs that only the sitemap knows about.
- `seo-change-monitor` to track submitted vs indexed counts after the new sitemap ships.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
