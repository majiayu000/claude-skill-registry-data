---
name: seo-optimization
description: Technical/on-page SEO, Core Web Vitals, structured data, GEO/LLM SEO, and quality-gate signals.
---

# SEO Optimization

Reference material for `seo-specialist`. Stack-agnostic — applies to any framework that renders HTML for a public, indexable surface.

## Detection Signals — When SEO Is Required

A project counts as "needs SEO" when any of these hold. Use this table to decide whether `seo-specialist` must be spawned, not just invited.

| Signal type | Examples |
|---|---|
| Project category | Institutional/marketing site, landing page, e-commerce/online store, blog, documentation portal, portfolio — any surface meant to be found via search or cited by an AI answer |
| File presence | `sitemap.xml`, `robots.txt`, `next-seo.config.*`, `astro.config.*` with `site:` set, `gatsby-config.js`, CMS content directories (`content/`, `posts/`, `blog/`) |
| Route shape | Product detail pages, category/listing pages, checkout funnel entry pages, blog post routes, `/blog/`, `/produtos/`, `/p/` |
| Dependency signals | `next-seo`, `react-helmet`, `vue-meta`, `schema-dts`, `astro-seo`, sitemap generator packages |
| Explicit request | User mentions SEO, ranking, Google, meta tags, structured data, sitemap, Core Web Vitals, ou "otimizar para IA/LLM" |

**Not required** for: internal admin panels, authenticated-only dashboards, CLIs, backend services with no rendered HTML, mobile-only apps with no web surface.

---

## Technical SEO Checklist

- `robots.txt` present, not blocking pages that should be indexed, and pointing to the sitemap
- `sitemap.xml` generated (static or dynamic), includes all indexable routes, excludes noindex/private routes
- Canonical URL (`<link rel="canonical">`) on every page — prevents duplicate-content splitting
- One `<h1>` per page, logical heading hierarchy (`h1` → `h2` → `h3`, no skipped levels)
- `hreflang` tags when the project serves more than one locale
- HTTPS enforced, no mixed content
- Clean, descriptive URLs (no query-string-only routing for canonical content, no unnecessary IDs)
- 404s return real `404` status, not `200` with a "not found" page (soft 404)
- Redirects use `301` for permanent moves, never chained more than one hop

## On-Page SEO Checklist

- `<title>` unique per page, 50–60 characters, primary keyword near the front
- Meta description unique per page, 140–160 characters, includes a reason to click
- Image `alt` text descriptive (not keyword-stuffed), decorative images use `alt=""`
- Internal linking uses descriptive anchor text, not "click here"
- Content answers the query in the first 1–2 sentences before elaborating (also serves GEO — see below)
- Open Graph (`og:title`, `og:description`, `og:image`, `og:url`) and Twitter Card tags present for shareable pages
- **Share preview check** — verify those tags in the HTML served to the `facebookexternalhit` crawler, not just in source. Procedure: `references/share-preview-check.md`

## Off-Page Signals (advisory, not gated)

- Structured internal linking supports topic authority — flag orphaned pages with no inbound internal links
- Flag broken outbound links found during review
- Backlink strategy, PR, and external outreach are outside this agent's scope — note when the user should involve marketing/growth, don't attempt to execute them

---

## Core Web Vitals — Thresholds ("Good")

| Metric | Threshold | What it measures |
|---|---|---|
| LCP (Largest Contentful Paint) | ≤ 2.5s | Perceived load speed |
| INP (Interaction to Next Paint) | ≤ 200ms | Responsiveness |
| CLS (Cumulative Layout Shift) | ≤ 0.1 | Visual stability |

Common fixes: preload the LCP image/font, avoid layout shift from late-loading web fonts or images without explicit `width`/`height`, defer non-critical JS, avoid render-blocking CSS.

---

## Structured Data (schema.org / JSON-LD)

Emit as `<script type="application/ld+json">`. Pick the type that matches the page's real content — never mark up content that isn't visible to the user (Google Rich Results Test and other engines penalize mismatches).

| Page type | Schema type | Key fields |
|---|---|---|
| Homepage / brand | `Organization` | `name`, `url`, `logo`, `sameAs` (social profiles) |
| Landing / service page | `Service` or `WebPage` | `name`, `description`, `provider` |
| Product page | `Product` | `name`, `image`, `description`, `offers` (`price`, `priceCurrency`, `availability`), `aggregateRating` if reviews exist |
| Blog post / article | `Article` or `BlogPosting` | `headline`, `author`, `datePublished`, `dateModified`, `image` |
| FAQ section | `FAQPage` | `mainEntity` array of `Question`/`Answer` pairs — only for content genuinely visible as Q&A on the page |
| Navigation trail | `BreadcrumbList` | ordered `itemListElement` matching the visible breadcrumb |
| Local business | `LocalBusiness` | `address`, `openingHours`, `telephone` |

Validate with structured-data testing tools before shipping when the project has one configured; otherwise flag as "unverified, spot-check recommended."

---

## GEO — SEO for LLMs / AI Search (Generative Engine Optimization)

Search is increasingly answered by AI systems (chat assistants, AI Overviews, agentic browsers) that read and cite pages rather than only ranking them. These practices make content easier to extract and cite correctly:

- **`llms.txt`** at the site root — a plain-Markdown index of the site's key pages for LLM consumption: a short site description, then a linked list of the most important pages with a one-line summary each. Keep it accurate — a stale `llms.txt` is worse than none, since it misdirects the citation.
- **Answer-first structure** — state the direct answer to the likely query in the first sentence or two of a section, then elaborate. LLMs extract from the top of a block; burying the answer under preamble reduces citation accuracy.
- **Self-contained sections** — each `h2`/`h3` section should make sense read in isolation (LLMs often extract a section, not the whole page). Avoid "as mentioned above" references that only work in full-page context.
- **Explicit entities** — name the product, company, or concept by its full name near the top of the page instead of relying on pronouns or implied context established elsewhere.
- **Clean semantic HTML** — proper `<article>`, `<section>`, heading hierarchy, and lists (`<ul>`/`<ol>`) over div-soup; extraction quality tracks markup quality.
- **Structured data doubles as GEO signal** — the same JSON-LD that helps traditional search also gives LLM crawlers unambiguous facts (price, author, date) instead of forcing them to infer from prose.
- **Avoid content gated behind JS-only rendering** with no server-rendered fallback — some AI crawlers do not execute JavaScript; SSR or static generation ensures the content is visible to both search and AI crawlers.
- **`robots.txt` AI-crawler directives** — if the project has a stated policy on AI training/crawling (e.g. `GPTBot`, `ClaudeBot`, `Google-Extended`), reflect it explicitly rather than leaving it to each crawler's default.

---

## Quality Gate Output Format

Use this exact structure when reporting an SEO review (see `agents/seo-specialist.md` for when it is mandatory vs. advisory):

```
## SEO Quality Gate

### Technical SEO
[PASS / ISSUE / BLOCKER] — [finding]

### On-Page SEO
[PASS / ISSUE / BLOCKER] — [finding]

### Core Web Vitals
[PASS / ISSUE / BLOCKER] — [finding, with measured value if available]

### Structured Data
[PASS / ISSUE / BLOCKER] — [finding]

### GEO / LLM Readiness
[PASS / ISSUE / BLOCKER] — [finding]

### Verdict
[APPROVED / APPROVED WITH NOTES / BLOCKED]
```

`BLOCKER` = missing sitemap/robots.txt, missing canonical on a duplicated route, broken structured data, LCP/CLS in "poor" range, a soft-404, or a shareable page answering `403`/`429` to the `facebookexternalhit` crawler while a regular browser User-Agent gets `200` (see `references/share-preview-check.md`). Everything else non-passing is `ISSUE`. `BLOCKED` verdict when any `BLOCKER` is present.
