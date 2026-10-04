---
name: seo-audit
description: >-
  Audit and optimize public-facing web pages for search engines and AI search.
  Covers technical SEO audits (crawlability, Core Web Vitals, structured
  data), local SEO (LocalBusiness schema, geo-metadata), on-page signals
  (title tags, meta descriptions, heading hierarchy), and AI search readiness
  (GEO, llms.txt, structured data for LLM extraction).
  Use when the user asks about SEO audit, meta tags, structured data, local
  SEO, Core Web Vitals, crawlability, robots.txt, or public page optimization.
  Delegates depth to the everything-seo skill.
user-invocable: false
disable-model-invocation: false
version: "2.1.0"
author: "Ali Farahat"
tags: ["seo-audit", "local-seo", "technical-seo", "structured-data", "geo"]
when_to_use: |
  USE WHEN:
  - User asks about SEO audit, meta tags, or structured data implementation.
  - User is working on public-facing pages, landing pages, or profile pages.
  - User needs LocalBusiness schema or local SEO optimization.
  - User mentions Core Web Vitals, crawlability, or robots.txt.
  - User needs AI search readiness (GEO, llms.txt).

  DO NOT USE WHEN:
  - User needs high-level SEO strategy (use everything-seo).
  - User needs well-known agent discovery, Auth.md, A2A, MCP, or agentic
    commerce endpoints (use agent-ready).
  - User needs content marketing or keyword research (use startup-marketing-brain).
  - User needs PPC or paid search advice.
---

# SEO Audit & Optimization

> **Leading words:** technical SEO audit, crawlability, Core Web Vitals,
> structured data, LocalBusiness, schema drift, IndexNow, robots.txt
> governance.

A phase-separated audit workflow for any public-facing page (local-business
public profiles, landing pages, marketing pages). Depth lives in
`references/` and in the companion `everything-seo` skill.

## Phase 1 — Crawl

```
- [ ] GET /robots.txt is text/plain 200. Allow retrieval bots (OAI-SearchBot,
      ChatGPT-User, AppleBot, PerplexityBot) when search=yes; block training
      scrapers if policy says so (GPTBot, ClaudeBot, Bytespider); keep
      Googlebot fully allowed.
- [ ] Content-Signal on robots.txt matches those User-agent lines, or
      n/a: policy not declared yet (name the skip reason).
- [ ] GET /sitemap.xml is XML 200 listing canonical public URLs (not only
      "submitted to GSC").
- [ ] Sitemap submitted to Google Search Console + Bing Webmaster Tools.
- [ ] IndexNow implementation present (Bing + Yandex push).
```

🛑 **Checkpoint:** Confirm the crawl surface is mapped. Do not proceed to
Audit until robots.txt (served + policy) + sitemap served + IndexNow
status are each named. Well-known agent cards → `agent-ready`.

## Phase 2 — Audit

```
- [ ] Page titles: format "[Business Name] in [City] | [Value Prop]" for
      local-business public profiles.
- [ ] Meta descriptions: 120-160 chars, value prop + CTA verb, city if natural.
- [ ] Structured data: LocalBusiness JSON-LD validates in Google Rich Results
      Test + Bing Webmaster Tools.
- [ ] Core Web Vitals: INP < 200ms, LCP < 2.5s, CLS < 0.1.
- [ ] Schema drift check: does the JSON-LD match the rendered page content?
      (Cypress/Puppeteer test that compares rendered text to JSON-LD fields.)
- [ ] Heading hierarchy: exactly one H1, logical H2/H3 nesting, no skipped
      levels.
```

Pull [references/local_seo_checklist.md](references/local_seo_checklist.md)
for the full LocalBusiness JSON-LD field list and common mistakes.

🛑 **Checkpoint:** List every audit failure with the page URL + the specific
failure. Do not proceed to Fix until the failure list is enumerated.

## Phase 3 — Fix

```
- [ ] Fix each Phase 2 failure in order: titles → meta → schema → vitals → drift.
- [ ] Bump CONTENT_VERSION (or whatever signal the site uses) so AI indexers
      re-fetch.
- [ ] Update llms.txt if new pages were added or page roles changed.
- [ ] Re-run schema validation on every changed page.
```

## Phase 4 — Verify

```
- [ ] Re-run Google Rich Results Test on every changed page — green.
- [ ] Verify robots.txt changes with Google's robots.txt tester.
- [ ] Run a single-page Core Web Vitals check (Lighthouse or field data).
- [ ] Submit changed URLs via IndexNow for Bing + Yandex.
- [ ] Re-check schema drift on the changed pages.
```

Any miss → back to Phase 3.

## What NOT to do

- **No black-hat SEO.** No keyword stuffing, no hidden text, no cloaking, no
  link-buying, no private blog networks. Algorithmic penalties are recoverable
  but expensive.
- **Do not ignore Bing.** Bing + Yandex still drive meaningful traffic in
  some niches and regions. IndexNow submission is cheap.
- **Do not use client-side rendering for content that needs to rank.** Use
  SSR/ISR so the HTML the crawler receives contains the content. CSR-only
  pages may not be indexed reliably.
- **Do not skip the schema drift check.** Valid JSON-LD that contradicts the
  rendered page is worse than no JSON-LD — it signals inconsistency to both
  classical search and AI extractors.

## References

| File | Use it for |
|---|---|
| [references/local_seo_checklist.md](references/local_seo_checklist.md) | LocalBusiness JSON-LD field list, common mistakes, Bing considerations, robots.txt patterns |
| `../everything-seo/references/semantic_intent.md` | AEO/GEO patterns for AI search |
| `../everything-seo/references/content_automation.md` | Content quality + AI writing detection |
| `../everything-seo/references/technical_seo.md` | Deep technical SEO (bot governance, IndexNow, INP) |
| `../agent-ready/SKILL.md` | Well-known agent discovery (not a page-SEO audit) |
