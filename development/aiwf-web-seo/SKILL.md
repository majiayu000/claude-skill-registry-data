---
name: aiwf-web-seo
description: Use for technical SEO involving crawlability, indexability, status codes, redirects, titles and descriptions, canonical URLs, robots directives, sitemaps, structured data, JavaScript rendering, internal links, performance, accessibility, and production search validation. Use aiwf-aeo-geo for answer and generative-search visibility.
---

# AIWF Web SEO

## Core Rule

Audit the rendered site and its HTTP behavior before rewriting copy. SEO work must preserve truthful claims, useful pages, stable URLs, accessible content, and working product flows. No skill can guarantee ranking or inclusion in an index.

## Workflow

1. Identify the canonical production URL, framework, render mode, routes, deployment host, analytics or Search Console evidence, sitemap, robots rules, and structured data.
2. Check crawl and index basics: status codes, redirects, canonical tags, robots directives, sitemap URLs, internal links, unique titles, descriptions, headings, and text visibility after rendering.
3. Match each page to a real user intent and a real service, product, project, or evidence source. Remove duplicate or unsupported claims before adding keywords.
4. Add only structured data that matches visible page content and an applicable schema type.
5. Validate the production build, representative routes, rendered `<head>`, mobile layout, performance budget, and structured data.

## Guardrails

- Do not promise first-place rankings, indexing, rich results, traffic, or answer-engine citation.
- Route answer-engine, generative-engine, AI-search citation, entity-clarity, and source-worthy content work to `aiwf-aeo-geo`.
- Do not use `robots.txt` to prevent indexing; use the correct page or response directive when exclusion is intended.
- Keep one consistent canonical URL per indexable page and use absolute canonical URLs in sitemaps and metadata.
- Do not generate location, service, FAQ, testimonial, metric, or case-study pages without real supporting content.
- Keep important information in accessible text, not only images, canvas, or client-side state.
- Add `aiwf-react-coding` or `aiwf-vue-vitepress-coding` for framework changes, `aiwf-aeo-geo` for answer visibility, and `aiwf-avoid-ai-design` for visual cleanup.

## Validation

Report which URLs and rendered states were checked. Use the site's build and browser tests, inspect response status and head metadata, validate JSON-LD with an appropriate official validator, and record unresolved indexing evidence separately from code correctness.

## Primary Sources

- Google SEO Starter Guide: https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- Google Search crawl and index guidance: https://developers.google.com/search/docs/fundamentals/how-search-works
- Canonical URL guidance: https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- JavaScript SEO basics: https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics
