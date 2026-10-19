---
name: seo-audit
description: Use when a site does not rank or show up on Google, asked for an SEO audit or technical SEO check, adding meta tags, sitemap, robots.txt, structured data or Open Graph, or preparing a new website or Next.js/React/static site for search engines.
---

# SEO Audit

## Overview

Make every important page crawlable, indexable, understandable and fast. Check the site the way a search engine sees it — the HTML it receives — and fix issues in the code that generates it.

## Method

1. **List the important pages** (home, product, category, articles) and the main search intent of each.
2. **See what search engines see:** `curl -sL <url>` (or the build output for static sites). Content rendered only by client-side JavaScript may be missed or delayed.
3. **Run the checklist** below per page template, not per page.
4. **Check site-wide files:** `robots.txt`, `sitemap.xml`, redirects, canonical domain (www vs non-www, http to https), 404 handling.
5. **Report** with the contract below, highest impact first.

## Checklist

| Area | Check |
|---|---|
| Indexing | Page returns 200; no `noindex` by accident; not blocked in `robots.txt`; listed in `sitemap.xml` |
| Canonical | One `<link rel="canonical">` with the absolute preferred URL; duplicates (params, trailing slash) point to it |
| Title | Unique per page, 50-60 characters, main keyword first, brand last |
| Meta description | Unique, 140-160 characters, describes the page and invites the click |
| Headings | Exactly one `<h1>` with the main topic; logical `h2`/`h3` order |
| Content in HTML | Main text present in server-rendered HTML (SSR/SSG), not only after client fetch |
| Links | Descriptive anchor text, crawlable `<a href>` (not `onclick`), no broken internal links |
| Images | Meaningful `alt`, compressed, explicit dimensions |
| Structured data | JSON-LD matching the page (`Organization`, `Person`, `Product`, `Article`, `BreadcrumbList`, `FAQPage`); valid in Rich Results Test |
| Social | `og:title`, `og:description`, `og:image` (1200×630), `twitter:card` |
| Mobile and speed | Viewport meta; Core Web Vitals pass (see web-performance-audit) |
| International | `hreflang` and `lang` attribute if multiple languages |
| URLs | Short, lowercase, hyphenated, stable; 301 redirects for changed URLs |

Framework notes: Next.js App Router — `metadata` / `generateMetadata`, `app/sitemap.ts`, `app/robots.ts`. React SPA — prerender or move to SSR/SSG for pages that must rank.

## Output contract

```
### [High | Medium | Low] Title
- Pages: <URL or template>
- Problem: what search engines see or miss
- Fix: exact tag, file and line, or config
```

Then: **Search Console steps** if the site is not verified (verify, submit sitemap, request indexing), and **Already good**.

## Common mistakes

- Auditing the browser view instead of the HTML returned by the server.
- Same title and description on every page.
- Canonical tags pointing to the wrong domain or to a localhost URL.
- Sitemap listing redirected or `noindex` pages.
- Keyword stuffing instead of writing for the search intent.

---

Made by **Wageesha Tripathi** · [LinkedIn](https://www.linkedin.com/in/wst2002/) · [Email](mailto:tripathiwageesha2002@gmail.com) · [More skills](https://github.com/WST2002/claude-code-skills)
