---
name: seo
description: SEO for web apps — metadata, structured data, sitemaps, robots.txt, Core Web Vitals, E-E-A-T. Auto-loads framework-specific references.
layer: domain
category: frontend
triggers:
  - "seo"
  - "meta tags"
  - "opengraph"
  - "og tags"
  - "structured data"
  - "json-ld"
  - "schema.org"
  - "sitemap"
  - "robots.txt"
  - "core web vitals"
  - "lcp"
  - "inp"
  - "cls"
  - "search engine"
  - "google ranking"
  - "rich snippets"
  - "e-e-a-t"
inputs:
  - Page or route to optimize
  - Target keywords + content type (article / product / service / local-biz / org / event)
  - Framework (Next.js, Remix, Astro, plain HTML)
outputs:
  - Metadata config (title, description, OG, Twitter cards, canonical)
  - JSON-LD blocks for the right schema.org type
  - sitemap.xml + robots.txt
  - Core Web Vitals fixes prioritised by impact
  - E-E-A-T audit findings + remediation list
linksTo:
  - nextjs
  - performance-profiler
  - vercel
linkedFrom:
  - ship
  - optimize
  - ui-ux-pro
preferredNextSkills:
  - performance-profiler
  - nextjs
fallbackSkills:
  - react
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: none
sideEffects: []
references:
  - nextjs-metadata.md
  - jsonld.md
  - sitemap-robots.md
  - core-web-vitals.md
  - eeat.md
templates:
  - assets/templates/article-jsonld.json
  - assets/templates/product-jsonld.json
  - assets/templates/organization-jsonld.json
  - assets/templates/local-business-jsonld.json
scripts:
  - scripts/audit.sh
---

# SEO

Comprehensive SEO for web apps. The bulk of the implementation lives in `references/` — load the one(s) relevant to the user's task. Templates in `assets/templates/` are ready-to-paste JSON-LD blocks parameterised on common fields.

## When to load each reference

| Task | Reference |
|---|---|
| Per-page metadata, OG tags, Twitter cards in Next.js | `references/nextjs-metadata.md` |
| Pick the right schema.org type + paste JSON-LD | `references/jsonld.md` (+ a template from `assets/templates/`) |
| Generate sitemap.xml or robots.txt | `references/sitemap-robots.md` |
| Fix LCP/INP/CLS regressions | `references/core-web-vitals.md` |
| Audit content quality (Experience/Expertise/Authoritativeness/Trust) | `references/eeat.md` |

## Decision tree

```
Is the page user-facing?
├── No  → robots noindex; skip the rest
└── Yes → Continue
    │
    ├── What schema.org type fits?
    │     blog post  → Article            → article-jsonld.json
    │     product    → Product (+ Offer)  → product-jsonld.json
    │     service    → Service / LocalBusiness
    │     org/about  → Organization       → organization-jsonld.json
    │     local biz  → LocalBusiness      → local-business-jsonld.json
    │     event      → Event
    │     person     → Person
    │
    ├── Framework?
    │     Next.js App Router → nextjs-metadata.md (Metadata API)
    │     Remix             → meta() functions
    │     Astro             → <head> with `Astro.url`
    │     Plain HTML        → static `<meta>` + `<script type="application/ld+json">`
    │
    └── Performance?
          → core-web-vitals.md (LCP/INP/CLS playbook)
```

## Run an audit

```bash
.claude/skills/seo/scripts/audit.sh https://example.com
```
The script:
1. Runs PageSpeed Insights (mobile + desktop) and prints the LCP/INP/CLS verdicts
2. Validates structured data via Google's testing endpoint
3. Greps the rendered HTML for missing `<title>`, `<meta description>`, OG tags, canonical
4. Outputs a checklist of fixes ordered by impact

## Quality gates (refuse to ship without these)

| Gate | Why |
|---|---|
| `metadataBase` set on root layout | Without it, OG image URLs resolve relative — broken on social shares |
| Canonical URL on every page | Prevents duplicate-content penalties |
| `description` 50–160 chars | Outside this range Google often rewrites your snippet |
| `og:image` 1200×630 + ≤300KB | Large/wrong-aspect images don't render in feeds |
| `alt` on every content image | a11y + image search ranking |
| LCP < 2.5s on mobile 4G | Below this is a Web Vitals fail and a CrUX field-data drag |
| Unique title per page | Duplicate titles get clustered in SERPs |

## Common pitfalls

- **Mixing Next.js Metadata API with `<Head>`**. Pick one; Metadata API wins for App Router.
- **Forgetting to escape `</script>` inside JSON-LD strings**. Use `dangerouslySetInnerHTML` with sanitised input.
- **`robots.txt` blocking `/_next/static/`**. Don't — Google needs your CSS/JS to render correctly.
- **Setting `noindex` and then linking to the page from elsewhere**. Either commit to noindex or remove the inbound links; mixed signals hurt.
- **Tracking pixels firing during render**. Use `next/script` with `strategy="lazyOnload"` for analytics.
