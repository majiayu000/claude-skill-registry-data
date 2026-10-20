---
name: make-page-crawlable
description: >-
  Load this skill when creating or shipping a public web page or route that crawlers and AI engines
  will see: a landing, docs, or blog page. Trigger on "add SEO", "meta tags", "open graph",
  "structured data", "sitemap", or a new public route. Not for README text.
disable-model-invocation: false
user-invocable: true
license: Apache-2.0
---

# Web discoverability

A public page is not done until its discoverability surface is complete. Search engines and
generative engines both work from the same raw material: the initial HTML response, the head
metadata, and sentences that survive being quoted out of context. Ship all three with the page,
not as a later "SEO pass".

## Procedure

1. Complete the per-page head. Every indexable page ships with:
   - **`<title>`** — unique per page, ≤ 60 characters, page-specific words first, site name last
     (`Pricing — Acme`, not `Acme | Home of the best...`).
   - **Meta description** — ≤ 155 characters, stating the answer or value, not a teaser. This is
     the excerpt search results and AI engines show; write it as the sentence you want quoted.
   - **Canonical link** — exactly one per page. Required wherever the same content is reachable
     under multiple URLs (trailing slash, query params, www).
   - **Open Graph + Twitter card** — `og:title`, `og:description`, `og:image` (1200×630),
     `og:type`; `twitter:card` = `summary_large_image`. Every shared link renders through these.
     The `og:image` file must actually exist and be a real 1200×630 PNG or JPG — link-preview
     crawlers render SVG inconsistently, and a dangling image reference silently kills every
     share card.
   - **Robots meta only to exclude** — `noindex` on thin, duplicate, or gated pages. Absence
     means index; never add an empty or permissive robots meta out of habit.
   - **No `<meta keywords>`** — dead surface; adding it only signals template cargo-culting.
2. Cover the site-level surfaces:
   - **`sitemap.xml`** — canonical URLs only, referenced from `robots.txt`.
   - **`robots.txt`** — allow by default; block only genuinely private paths. Blocking AI
     crawlers (GPTBot, ClaudeBot, PerplexityBot) is a product decision, not a default — flag it
     to the user rather than deciding either way silently.
   - **`llms.txt`** at the site root — a curated markdown reading list for AI agents, shipped
     alongside the sitemap and kept current as public pages change. `ceh-seo:write-llms-txt` owns
     its format and curation.
   - **404s return HTTP 404.** An SPA fallback serving every unknown path as 200 poisons the
     index with phantom pages.
   - **Moved pages get a 301** at the server/adapter level — no redirect chains, no client-side
     `window.location` redirects. Most AI crawlers run no JavaScript, and each hop in a chain
     loses signal.
3. Add structured data:
   - JSON-LD in a `<script type="application/ld+json">` block — never microdata attributes. JSON-LD
     sits apart from the visible markup, so it is generated and validated without touching
     templates.
   - Match the type to the page: `WebSite` + `Organization` on the home page,
     `Article`/`BlogPosting` on posts, `SoftwareApplication` or `Product` on product pages,
     `FAQPage` on FAQ content.
   - Only mark up content actually visible on the page — invisible structured data is a
     penalty surface, not a bonus.
4. Check rendering:
   - **Content must be in the initial HTML response.** Most AI crawlers do not execute
     JavaScript, and search rendering is deferred and unreliable. A client-only SPA page is
     invisible to the engines this skill exists for.
   - SvelteKit: `export const prerender = true` on static public routes; SSR for dynamic ones.
   - React + Vite: public pages need a prerender/SSG pass — a bare client-side SPA is not a
     discoverable page, whatever its meta tags say.
5. Write the page text for citation by generative engines (GEO):
   - **Answer-first sections.** Open each section with the claim; elaborate after. Engines quote
     sentences, not pages — a section whose first sentence is throat-clearing gets skipped.
   - **Extractable facts.** State facts in standalone sentences that survive quoting alone
     ("X supports Y since v2.1"), with concrete numbers over adjectives.
   - **Question-shaped headings** for question-shaped content — the heading is the query the
     engine matches against.

## Rules

- No keyword stuffing, hidden text, or doorway pages — engines derank all three.
- No SEO library or framework plugin for what static head tags do — a `<svelte:head>` or
  React helmet-equivalent block is a few lines.
- Never trade accessibility for SEO. Semantic headings, landmarks, and alt text serve both;
  when they appear to conflict, accessibility wins.
