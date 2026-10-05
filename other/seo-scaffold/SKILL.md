---
name: seo-scaffold
description: "Scaffolds production-grade SEO for any website: per-page meta tags, Open Graph, Twitter Cards, canonical URLs, JSON-LD structured data, sitemap.xml, robots.txt, and security.txt. Auto-detects the framework and uses its idiomatic approach (Next.js metadata API, Astro layouts, etc.)."
---

# /seo-scaffold

Generates the SEO essentials a website needs to rank, share well, and meet compliance. Wires them into the framework idiomatically so every new page inherits the defaults.

## When to use

- New website project — set up SEO from the start.
- Existing site missing meta tags, sitemap, or structured data.
- Migrating from a framework that didn't have SEO baked in (e.g., CRA → Next.js).
- After `/web-launch-check` flagged SEO gaps.

## What it produces

### 1. Site-wide meta defaults (in your layout / root component)

A single source of truth for site-level metadata, with per-page overrides:

```html
<title>{{ pageTitle }} — {{ siteName }}</title>
<meta name="description" content="{{ pageDescription }}">
<link rel="canonical" href="{{ canonicalUrl }}">

<!-- Open Graph -->
<meta property="og:type" content="{{ ogType | website }}">
<meta property="og:title" content="{{ pageTitle }}">
<meta property="og:description" content="{{ pageDescription }}">
<meta property="og:url" content="{{ canonicalUrl }}">
<meta property="og:image" content="{{ ogImage }}">
<meta property="og:site_name" content="{{ siteName }}">

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{{ pageTitle }}">
<meta name="twitter:description" content="{{ pageDescription }}">
<meta name="twitter:image" content="{{ ogImage }}">

<!-- Misc -->
<meta name="theme-color" content="{{ themeColor }}">
<link rel="icon" href="/favicon.ico">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
```

Implementation depends on the framework:

| Framework | Where to put it |
|---|---|
| Next.js (app dir) | `app/layout.tsx` `metadata` export + per-page `generateMetadata` |
| Next.js (pages dir) | `_document.tsx` + `next/head` per page |
| Astro | `src/layouts/Base.astro` + page frontmatter |
| SvelteKit | `+layout.svelte` + per-page `<svelte:head>` |
| Nuxt | `app.vue` `useSeoMeta` + per-page `useSeoMeta` |
| Remix | `meta` export per route |
| Plain HTML | `<head>` of each page (or via a templating layer) |

### 2. JSON-LD structured data

Generate the right schema.org type for the page:

- **Organization** — once site-wide, in the layout.
- **WebSite** — site-wide, includes the search action for sitelinks search box.
- **BreadcrumbList** — on inner pages.
- **Article / BlogPosting** — on every blog post.
- **Product** — on product pages (price, availability, ratings).
- **FAQPage** — when there's a FAQ section.
- **VideoObject** — for embedded video.
- **Course / Recipe / Event** — domain-specific.

Example FAQ JSON-LD:

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How long does setup take?",
      "acceptedAnswer": { "@type": "Answer", "text": "About 5 minutes." }
    }
  ]
}
```

### 3. `sitemap.xml`

- Generated at build time from your route list.
- Includes `<loc>`, `<lastmod>` (ISO 8601), `<changefreq>` (optional), `<priority>` (optional, often skip).
- Excludes admin / private / paginated tail pages.
- For sites > 50K URLs, generate a sitemap index with multiple sitemaps.

Idiomatic implementation:

| Framework | Approach |
|---|---|
| Next.js (app dir) | `app/sitemap.ts` exporting a default function |
| Astro | `@astrojs/sitemap` integration |
| SvelteKit | `+server.ts` route returning XML |
| Nuxt | `@nuxtjs/sitemap` module |
| Plain | A build-time Node script |

### 4. `robots.txt`

```
User-agent: *
Allow: /

Disallow: /admin/
Disallow: /api/
Disallow: /private/

Sitemap: https://example.com/sitemap.xml
```

Adjust per environment — staging should disallow all crawlers (`Disallow: /`).

### 5. `/.well-known/security.txt`

```
Contact: mailto:security@example.com
Expires: 2027-01-01T00:00:00.000Z
Preferred-Languages: en
Canonical: https://example.com/.well-known/security.txt
```

### 6. Per-page checklist for the developer

When the user later adds a page, remind them:

- Set a unique `<title>` and `description`.
- Set `og:image` (1200×630 PNG) for social sharing.
- Add structured data if the page type warrants it.
- Add the page to the sitemap (or trust your generator).

## Operating method

1. Detect framework + version. Read package.json, framework config files, sample a route.
2. Detect what's already in place — don't duplicate.
3. Generate the missing pieces idiomatically.
4. Add a section to CLAUDE.md (or create one) documenting the SEO conventions used so future contributors follow them.
5. Print a summary of what was added and what the user must fill in (site name, default OG image path, etc.).

## Output format

```
## Detected stack
- Framework: <name + version>
- Existing SEO: <inventory>

## Generated
- File: <path> — <description>
- File: <path> — <description>

## You still need to:
1. Replace placeholder site name "Example Co" with yours.
2. Add /public/og-default.png (1200×630) — the fallback social-share image.
3. Update {{ siteUrl }} in src/config/site.ts.

## Recommended next:
- Run /web-launch-check to verify nothing else is missing.
- Add structured data per page type (Article, Product, etc.) — see references in src/lib/seo.ts.
```

## Don't

- Don't generate empty placeholder JSON-LD that lies (e.g., a Product schema without a real price).
- Don't add `noindex` to production unless the user explicitly asks.
- Don't put the same `og:image` on every page if the site has rich content — but a single fallback is fine for v1.
- Don't generate AMP. It's deprecated in practice.
- Don't include keyword-stuffed meta descriptions. They get truncated and look spammy.
