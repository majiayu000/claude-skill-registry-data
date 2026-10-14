---
name: technical-seo
description: "Technical SEO implementation: crawlability, metadata, sitemaps, structured data, SSR/SSG/ISR, status codes, Core Web Vitals. Use for making pages discoverable and indexable. Content/marketing SEO is out of scope."
---

# technical-seo

If a crawler cannot fetch it, render it, or understand it, content quality is irrelevant.

## Activate when

- Building or auditing pages for search visibility: metadata, sitemaps, structured data, crawl/index behavior, JS-rendered content, migrations with URL changes.

## Do NOT activate for

- Content strategy, keyword writing, link building (marketing SEO — out of scope).
- General performance work without crawl impact (see frontend/performance).

## Procedure

1. Inspect the existing setup first: framework + version, rendering mode per route (SSR/SSG/ISR/CSR), existing sitemap/robots/manifest. Never prescribe Next.js metadata APIs without confirming the installed Next.js major in package.json.
2. Metadata per URL: unique `<title>` (~50–60 chars), meta description (~150–160), canonical URL (self-referencing by default), Open Graph + Twitter cards, `robots` meta only where exclusion is intended.
3. Crawl plumbing: `robots.txt` (allow + sitemap pointer, no security-by-obscurity), XML sitemap(s) with lastmod, internal linking so every indexable URL is within a few clicks, clean URL structure (lowercase, words not IDs, trailing-slash consistent).
4. Structured data: JSON-LD per page type against https://schema.org/ (Article, Product, FAQ, BreadcrumbList…); validate with Google's Rich Results Test before shipping.
5. Status codes: 200 for indexable, 301 for moved (with redirect chains collapsed to one hop), 404 for truly gone, 410 for deliberately removed; soft-404s (200 with error content) are a defect.
6. Pagination/canonicalization: paginated series canonicalize per-page (no canonical-to-page-1 unless content truly duplicates); faceted/filtered URLs canonical or noindexed deliberately.
7. Duplicates: one URL per content (trailing slash, www, http/https, case variants all resolve to canonical); hreflang only for genuine locale alternates, with return links.
8. JavaScript content: verify what the crawler sees — SSR/SSG for index-critical content; if CSR, prove renderability (fetch-and-render test, dynamic rendering only as last resort). Dynamic metadata must be in the initial HTML, not injected post-hydration.
9. Next.js specifics: research the metadata API for the installed major in https://nextjs.org/docs (App Router `metadata`/`generateMetadata` vs Pages `<Head>` — never mix generations); sitemap/robots via route handlers or `next-sitemap` per version docs; ISR revalidation for freshness-sensitive pages.
10. Images: descriptive filenames/alt, responsive sources, sitemap entries for image-search-critical pages (details: `../media-assets/`).
11. Vitals/mobile: Core Web Vitals (LCP/INP/CLS) as ranking inputs — measure with field + lab data; mobile-first indexing means the mobile render is the canonical one (see `../performance/`, `../responsive-design/`).
12. Verify with tooling: IF available use Search Console URL inspection, Rich Results Test, and a crawler (Screaming Frog or equivalent); ELSE verify manually — view-source checks for metadata/canonical/JSON-LD, status-code sweep with curl, robots/sitemap fetch. Record tool used and residual gaps.

## Failure modes

- CSR-only pages with empty initial HTML; canonical pointing at wrong URL; noindex left from staging; redirect chains; duplicate content across locale variants; metadata from the wrong Next.js generation.

## References
- Registry: `../../research/documentation-search/references/framework-registry.yaml` (nextjs, vercel).
- Runtime research: `../../research/documentation-search/` (detect Next.js version first).
- Related: `../performance/`, `../accessibility/` (semantic HTML), `../media-assets/`.
