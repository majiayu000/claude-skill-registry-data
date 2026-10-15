---
name: technical-seo-audit
description: Audit whether search engines can crawl, render, understand and correctly index a site - robots.txt, sitemap, canonical URLs, metadata, structured data, Open Graph and X cards, redirects, broken links, duplicate content, URL structure and programmatic pages - with Next.js App Router specifics. Use before launch, before a domain move, or when pages are missing from the index.
---

# /technical-seo-audit

Verify everything against the **production build** (`next build && next start`, or the deployed site), never the dev server. For page content and headings, run `/seo-auditor`. Don't promise rankings; make indexing correct.

## 1. One origin

- Decide the production origin (e.g. `https://example.com`) and put it in one config value.
- In Next.js set `metadataBase: new URL(origin)` in the root layout, so relative canonical and OG URLs resolve absolutely.
- **Grep** the repo for `localhost`, old domains, placeholder domains and `http://`. None may reach production metadata, sitemaps or JSON-LD.
- Redirect the other variants (http → https, www ↔ apex) with a single 301 hop.

## 2. robots.txt

- `app/robots.ts` returning `{ rules, sitemap }`. Allow the site; disallow only what is genuinely not for search (iframe-only preview routes, internal tools, search-result URLs).
- Never use robots.txt to remove a page from the index; that needs `noindex` on a crawlable page.
- **Verify:** `curl $ORIGIN/robots.txt` shows the sitemap line with the absolute production URL.

## 3. Sitemap

- `app/sitemap.ts` built from the same data as the routes (the registry, the CMS, the database), so it can't drift.
- Include only canonical, indexable, 200-status URLs. No query-string variants, no noindexed pages, no redirects.
- **Verify:** fetch every URL in the sitemap and assert 200 and that its canonical equals itself.

## 4. Canonicals and duplicates

- Every indexable page sets `alternates: { canonical: path }`.
- Filtered and sorted views (`?category=`, `?q=`, `?sort=`) canonicalise to the unfiltered page, or are noindexed.
- Preview, print and embed routes: `robots: { index: false }`.
- Trailing slashes and casing are consistent; duplicates 301 to one form.

## 5. Metadata on generated routes

- Use `generateMetadata` on dynamic routes and build title, description and canonical from the item's own data.
- **Check uniqueness:** extract `<title>` and `<meta name="description">` from every built page and count duplicates. Zero duplicate titles is the target.

## 6. Social cards

- Open Graph `title`, `description`, `url`, `siteName`, `type` and an image of 1200×630 (`app/opengraph-image.tsx` with `next/og`), plus `twitter: { card: "summary_large_image" }`.
- **Verify** the rendered `<meta property="og:image">` is an absolute production URL and that the image returns 200 with `content-type: image/png`.

## 7. Structured data

- Add only what is true: `WebSite` and `Organization` on the home page, `BreadcrumbList` on nested pages, an item type that honestly fits (e.g. `SoftwareSourceCode`, `CreativeWork`, `Article`, `Product` only if it's for sale).
- Never invent ratings, reviews, prices or FAQ markup for content that isn't a visible FAQ.
- Render it as `<script type="application/ld+json">` with `<` escaped. **Verify** by parsing every block from the built HTML with `JSON.parse` and checking required fields; then spot-check in a rich-results validator.

## 8. Rendering and status codes

- Important content is in the server-rendered HTML (`curl` the page and grep for the `h1` and body text).
- Unknown slugs return a real 404 (`notFound()`), not a 200 with an empty state.
- **Crawl** internal links from the home page and report every non-200 and every redirect chain.

## 9. URL structure

- Lowercase, hyphenated, readable, stable: `/components/silk-field`, not `/c?id=42`. Changing a URL needs a 301 from the old one.

## Output

A checklist with pass/fail and evidence (the command and what it printed) for each section, then the fixes, then the same checklist re-run.
