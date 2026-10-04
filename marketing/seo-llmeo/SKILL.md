---
name: seo-llmeo
description: >
  SEO and LLM Engine Optimization (LLMEO) skill for BroomVA content. Analyzes pages
  for traditional search-engine signals (meta tags, structured data, Core Web Vitals,
  internal linking) and for LLM discoverability (llms.txt, semantic headings, FAQ
  schema, citation-friendly structure). Generates actionable audits and rewrites.
  Use when: (1) auditing a page or site for SEO health, (2) optimizing content for
  LLM citation and AI search surfaces, (3) generating meta tags and structured data,
  (4) creating or updating llms.txt, (5) improving content structure for both Google
  and AI answer engines.
version: 1.0.0
category: publishing
tags:
  - seo
  - llmeo
  - llms-txt
  - meta-tags
  - structured-data
  - core-web-vitals
  - content-optimization
dependencies:
  - content-creation
  - arcan-glass
---

# SEO / LLMEO

Search-engine optimization plus LLM engine optimization for BroomVA content.

## Capabilities

| Area | What it does |
|------|-------------|
| Traditional SEO | Meta tags, Open Graph, canonical URLs, sitemap, robots.txt, structured data (JSON-LD) |
| Core Web Vitals | LCP, CLS, INP guidance based on page structure |
| LLMEO | `llms.txt` generation, semantic heading hierarchy, FAQ schema, citation-friendly paragraphs |
| Content audit | Readability score, keyword density, internal/external link ratio |
| Rewrite suggestions | Actionable diffs to improve both SEO and LLMEO signals |

## Commands

### `audit <url-or-path>`

Run a full SEO + LLMEO audit on a page. Returns a scored checklist with fix suggestions.

### `llms-txt <site-root>`

Generate or update an `llms.txt` file for the site, following the emerging standard for
LLM-friendly site descriptions.

### `meta <url-or-path>`

Generate optimal meta tags (title, description, OG, Twitter card) for a page.

### `structured-data <url-or-path>`

Generate JSON-LD structured data (Article, FAQ, HowTo, etc.) for a page.

## Audit Checklist

### Traditional SEO Signals

- [ ] Title tag present, 50-60 characters, includes primary keyword
- [ ] Meta description present, 150-160 characters, includes CTA
- [ ] Canonical URL set correctly
- [ ] Open Graph tags complete (og:title, og:description, og:image, og:url)
- [ ] Twitter Card tags present (twitter:card, twitter:title, twitter:description, twitter:image)
- [ ] H1 tag present, unique per page, includes primary keyword
- [ ] Heading hierarchy valid (no skipped levels)
- [ ] Internal links present (minimum 3 per page)
- [ ] Images have alt text
- [ ] Structured data valid (JSON-LD, no errors in schema.org validator)
- [ ] robots.txt allows crawling
- [ ] sitemap.xml present and valid

### LLMEO Signals

- [ ] `llms.txt` present at site root
- [ ] Semantic heading hierarchy (H1 > H2 > H3, logically nested)
- [ ] FAQ schema present where appropriate
- [ ] Citation-friendly paragraphs (clear topic sentences, factual claims with sources)
- [ ] Content chunked into digestible sections (300-500 words per section)
- [ ] Key definitions and concepts clearly stated (not buried in prose)
- [ ] Tables used for structured comparisons
- [ ] Code blocks properly labeled with language

### Core Web Vitals Guidance

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP | < 2.5s | 2.5s - 4.0s | > 4.0s |
| CLS | < 0.1 | 0.1 - 0.25 | > 0.25 |
| INP | < 200ms | 200ms - 500ms | > 500ms |

## llms.txt Specification

The `llms.txt` file lives at the site root and describes the site for LLM crawlers:

```
# Site Name

> Brief description of what this site is about.

## Docs

- [Page Title](url): Description of what this page covers
- [Another Page](url): Description

## API

- [Endpoint docs](url): API reference description

## Optional

- [Less important page](url): Description
```

## Integration

Works with:
- `content-creation` — apply SEO/LLMEO checks before publishing
- `arcan-glass` — ensure design system pages have proper meta
- `broomva.tech` — site-wide audit and llms.txt management
- `brand-icons` — ensures OG/Twitter meta tags reference correct image assets
