---
name: "content-seo"
description: "Copy + discoverability requirements every delivered app must meet — real-brand extraction, anti-slop voice, per-page SEO/JSON-LD, pSEO, GEO/AI-search, truth/citations, competitor floor, i18n, trust surfaces."
triggers:
  - "content"
  - "copy"
  - "seo"
  - "brand"
  - "blog"
priority: 2
pack: "content"
stage: stable
---

# Content & SEO — every app's copy + discoverability must satisfy

## Brand extraction (rebuilds / clients)

- Extract the REAL brand (logo, colors, fonts, tone; Wayback if the source is down). NEVER invent colors, never use Emdash defaults for clients, never infer from category.
- Colors derive from the logo (hue-distance verified). Logo luminance + source-site theme decide light/dark. Every logo render contrasts its container ≥4.5:1. Exactly ONE logo asset per container.

## Anti-AI-slop (mandatory scan)

- Banned words: delve, leverage, unleash, revolutionize, seamless, robust, synergy, elevate, empower, transformative, best-in-class, cutting-edge, discover, innovative.
- Banned patterns: "Welcome to", "Discover [product]", vague aspirational headlines, hedging ("may help"), generic superlatives. Test: "Would the founder actually say this?" — no → rewrite.

## Copy

- Headlines benefit-first, specific, ≤8 words. Subheads 15-25 words. Body one idea/paragraph, active, concrete. Max sentence 25 words. Flesch ≥60 (microcopy ≥70).
- CTAs: action-verb-first, ≤3 words preferred; never "Click here" / "Submit" / "Learn more". Above fold + page end.
- Microcopy: errors = [what happened] + [what to do]; empty states suggest the first action; toasts past-tense success / present in-progress.

## SEO — every page

- Title 50-60 chars keyphrase-first · meta description 120-156 · canonical · OG image 1200×630 · exactly one H1 in prerendered HTML.
- JSON-LD: WebPage floor; Org/BreadcrumbList/FAQPage/Person/Product/Service ONLY when the entity is real — never pad (FAQPage only with real FAQs).
- sitemap.xml (+lastmod) · robots.txt · llms.txt · humans.txt · security.txt.

## pSEO (when used)

- 5 page types: integration · comparison · use-case · template · location. Each: unique H1 + meta + 800+ unique words + ≥1 unique image + ≥3 internal links + ≥1 outbound citation. Never templatize verbatim.

## GEO / AI search

- Quotable answer blocks (40-60 words). FAQPage schema. Every JSON-LD fact also appears as visible HTML. Lead paragraph answers the query in <40 words. EEAT: author bio + Person schema + `sameAs` + dated revisions + ownership.

## Truth & citations

- Every factual claim APA-cited to a real source. Never fabricate people, stats, timelines, or testimonials. Testimonials carry verifiable attribution.

## Reach

- Competitor floor: outscore the top 5-10 peer sites on every rubric dimension by ≥15% before "done".
- i18n by demographics: any community ≥10% local share (ACS B16001) gets a `/{locale}/*` mirror + hreflang.

## Required pages

- `/privacy` · `/terms` · `/accessibility` · About/Team with real bios.
