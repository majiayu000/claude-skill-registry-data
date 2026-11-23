---
name: astro-sites
description: "Build content-driven sites with Astro: islands architecture, content collections, SSR versus static output, and image optimization."
type: procedural
category: web
domain: web
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: beginner
triggers:
  - astro islands architecture
  - astro content collection
  - astro ssr adapter
  - astro build performance
  - astro image optimization
keywords:
  - astro
  - islands
  - content-collections
  - ssg
  - ssr
source: custom
enabled: true
---

# Astro Sites

## Purpose

Build content-driven sites with Astro: islands architecture, content collections, SSR versus static output, and image optimization.

## When to Use

- You are building a documentation, blog or marketing site where most pages are static.
- Only a few interactive widgets need client-side JavaScript.
- Content must be typed and validated at build time.

## When NOT to Use

- The app is a highly interactive dashboard where a full SPA framework fits better.
- You need realtime server state on every page.
- The team has no Node build step in its deployment pipeline.

## Capabilities

- Choose the right rendering mode per route.
- Hydrate only the islands that need interactivity.
- Model content collections with schema validation.
- Optimize images and fonts for Core Web Vitals.

## Inputs

- The hosting target and whether SSR is available.
- The content sources (Markdown, CMS, API).
- The pages that genuinely need client-side state.

## Workflow

1. Map each route to static or SSR output based on data freshness needs.
2. Define a content collection schema before writing pages.
3. Add `client:*` directives only to interactive islands.
4. Use the built-in image component and preload critical fonts.
5. Measure the built site's Lighthouse scores and bundle size.

## Tools

- astro CLI
- vite
- Lighthouse / web-vitals

## Examples

- `npm run build && npm run preview`
- `astro add sitemap`
- `npm run astro -- check`

## Safety

- `client:load` on every component defeats the islands model and ships a full JS bundle.
- Content schema changes break builds; migrate content in the same change.
- SSR adapters require a matching runtime; static output cannot read request data.

## Source

All-Skills canonical library (`skills/web/astro-sites`). First-party skill, maintained in this repository.

## Notes

- Default to zero JavaScript; add interactivity per component, not per page.
- Content collections give type-safe frontmatter without a CMS.
- Pairs with: `web/frontend-design`, `web/seo`.
