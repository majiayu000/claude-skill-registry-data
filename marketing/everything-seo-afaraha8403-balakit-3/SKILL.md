---
name: everything-seo
description: >-
  Expert SEO advisor for modern search optimization. Covers technical SEO
  audits, crawlability, semantic SEO, E-E-A-T, digital PR, GEO (Generative
  Engine Optimization), RAG optimization, and multi-engine (Google + Bing)
  strategy. Use for: technical audits, on-page SEO, semantic search, keyword
  intent, link building, CRO, content automation, schema markup, and AI
  search readiness.
user-invocable: false
disable-model-invocation: false
version: "1.3.0"
author: "Ali Farahat"
derived_from: "NotebookLM"
tags: ["SEO", "technical-SEO", "on-page-SEO", "link-building", "digital-PR", "CRO", "content-automation", "E-E-A-T", "Core-Web-Vitals", "GEO", "RAG-optimization"]
when_to_use: |
  - User asks about SEO, search optimization, or ranking improvement.
  - User needs technical SEO audit, crawlability, or indexing help.
  - User asks about on-page SEO, content optimization, or semantic SEO.
  - User needs keyword research, intent mapping, or topical authority.
  - User asks about link building, digital PR, or backlink strategies.
  - User wants to improve E-E-A-T signals or site trustworthiness.
  - User asks about Core Web Vitals, page speed, or performance.
  - User needs schema markup, structured data, or rich results.
  - User asks about CRO and SEO integration or A/B testing.
  - User wants Bing SEO optimization or Google vs Bing differences.
  - User asks about AI content automation or Generative Engine Optimization (GEO).
  - User mentions SEO penalties, SpamBrain, or algorithm updates.
  - DO NOT USE for: paid search (PPC), social media marketing, or general web
    design. For local-business / public-profile audits specifically, prefer the
    seo-audit skill (it carries the phase-separated Crawl > Audit > Fix > Verify
    workflow and delegates depth here). For well-known agent discovery
    (Auth.md, A2A, MCP, ACP/UCP/x402), use agent-ready.
---

# Everything SEO

> **Leading words:** technical SEO audit, crawlability, GEO, semantic SEO,
> E-E-A-T, digital PR, schema drift, IndexNow, Intent-to-Entity Proximity
> Score, BLUF, RAG optimization.

A comprehensive SEO playbook for 2026: technical audits, semantic search,
AI-driven content, digital PR, CRO integration, and multi-engine optimization.
Treat the site as a structured data source for the decentralized web and
autonomous AI agents — technical SEO is the foundation, content is the signal,
links are the votes.

## Phase 1 — Audit

```
- [ ] Crawlability & bot governance (/robots.txt text/plain 200; Content-Signal
      matches User-agent policy; allow retrieval bots when search=yes; block
      training scrapers when ai-train=no).
- [ ] Indexing architecture (ISR/SSR, not CSR — Google's Dec 2025 rendering
      shift excludes non-200 pages from the JS rendering queue).
- [ ] Core Web Vitals (INP < 200ms via scheduler.yield(); LCP < 2.5s via
      fetchpriority="high" + AVIF; CLS < 0.1).
- [ ] Structured data validation (Google Rich Results Test; combat schema
      drift with Cypress/Puppeteer tests that fail builds on JSON-LD/DOM
      mismatch).
- [ ] Intent mapping audit (Intent-to-Entity Proximity Score P_s ≈ 1.0).
- [ ] E-E-A-T signal audit (bios, credentials, original data, photos,
      "Last updated" timestamps).
```

Pull [references/technical_seo.md](references/technical_seo.md) for the full
5-pillar audit and [references/semantic_intent.md](references/semantic_intent.md)
for intent mapping + E-E-A-T depth.

🛑 **Checkpoint:** List every audit failure with the page URL + the specific
failure. Do not proceed to Optimize until the failure list is enumerated.

## Phase 2 — Optimize

```
- [ ] Content: BLUF answers under H2 (40-60 words), HTML tables for
      comparisons, definition lists for specs (LLMs select these 82% of the
      time over plain text).
- [ ] E-E-A-T signals: author bios with credentials, original research,
      photos, consistent publishing.
- [ ] Digital PR: Authority Nodes (original surveys 500+, calculators,
      industry reports). Platform sniping on Connectively / Qwoted /
      Featured.com within 1 hour with concise quotes (< 200 words) + specific
      stats (60%+ placement boost).
- [ ] Link building: diversify anchor text (40-60% branded, 20-30% generic,
      < 20% exact-match). Reclaim unlinked mentions monthly (30%+ success
      rate via Ahrefs Content Explorer).
- [ ] GEO: llms.txt at the root, CONTENT_VERSION bumping for AI indexers,
      sameAs + ProfilePage schema to link entities to authoritative sources.
- [ ] CRO + SEO integration: shared KPIs (Revenue influenced by organic
      traffic, not rankings), commitment-based CTAs, social proof adjacent
      to CTAs, flicker-free server-side A/B testing (Convert, VWO).
```

Pull [references/content_automation.md](references/content_automation.md),
[references/link_building.md](references/link_building.md), and
[references/cro_integration.md](references/cro_integration.md) for depth.

## Phase 3 — Maintain

```
- [ ] IndexNow for Bing + Yandex push (instant index update on content/price
      changes).
- [ ] Reclaim unlinked brand mentions monthly.
- [ ] Platform sniping cadence (Connectively, Qwoted, Featured.com within
      1 hour).
- [ ] Annual data updates on Authority Nodes (compounds backlinks).
- [ ] Backlink profile audit (no manual penalties, natural anchor text
      distribution, no PBNs / link farms / bought links).
- [ ] Schema drift tests green on every changed page.
```

Pull [references/bing_google.md](references/bing_google.md) for the Bing vs
Google decision matrix and IndexNow setup details.

## The 2026 Expert SEO Tool Stack

- **Riff Analytics:** Track brand citation rate + "answer share" inside
  generative AI engines (ChatGPT, Perplexity, Claude, Gemini).
- **SEOTesting:** Bypass Google's 1,000-row limit; run time-based, split, and
  LLM SEO tests using GSC data.
- **Screaming Frog / Sitebulb:** Desktop + cloud crawlers for technical
  audits and rendering diagnostics.
- **Ahrefs / Semrush:** Competitive link gap analysis, backlink indexes,
  keyword clustering.
- **Convert Experiences / VWO:** Flicker-free, SEO-safe A/B testing +
  personalization.

## What NOT to do

- **No black-hat tactics:** PBNs, link farms, cloaking, keyword stuffing,
  bought links — SpamBrain AI devalues and penalizes these.
- **No exact-match anchor text for all backlinks.** Diversify naturally.
- **Do not ignore Bing.** It powers ChatGPT and Copilot search; IndexNow is
  cheap.
- **Do not recommend CSR** for e-commerce or news sites. Use ISR or SSR.
- **No PPC or paid search advice.** This is an organic SEO skill.
- **No vague advice** like "write quality content." Be specific about
  structure, schema, and technical execution.

## SEO Mastery Checklist

- [ ] Technical audit complete: crawlability, indexing, CWV, schema, rendering.
- [ ] `/robots.txt` is served; Content-Signal matches User-agent policy.
- [ ] Faceted navigation uses canonical/noindex to prevent combinatorial explosion.
- [ ] All unique page templates pass Google's Rich Results Test with zero errors.
- [ ] Cypress/Puppeteer automated tests implemented to prevent Schema Drift.
- [ ] LCP images use `fetchpriority="high"` and AVIF formats.
- [ ] INP < 200ms using `scheduler.yield()`, LCP < 2.5s, CLS < 0.1.
- [ ] IndexNow implemented for instant Bing/AI push notifications.
- [ ] Intent mapping maintains a high Intent-to-Entity Proximity Score (P_s ≈ 1.0).
- [ ] Content uses BLUF, HTML tables, and definition lists for AI extraction.
- [ ] Commercial pages have visible informational off-ramps to capture loopback queries.
- [ ] E-E-A-T signals demonstrated: bios, credentials, original data, photos.
- [ ] Digital PR campaigns focus on Authority Nodes over guest posts.
- [ ] Sourcing platforms sniped within 60 minutes.
- [ ] Unlinked brand mentions monitored and reclaimed monthly.
- [ ] A/B testing uses canonical tags + flicker-free server-side testing.
- [ ] CTAs use personal, commitment-based language; reviews placed adjacent to CTAs.
- [ ] Shared KPIs track "Revenue influenced by organic traffic" instead of rankings.
- [ ] No manual penalties. Backlink profile is natural and diverse.

## Reference Index

| File | When to Load |
|---|---|
| [references/technical_seo.md](references/technical_seo.md) | Technical audits, crawlability, indexing, Core Web Vitals, schema markup, JS rendering, robots.txt, hreflang. Agent protocol cards → `agent-ready`. |
| [references/semantic_intent.md](references/semantic_intent.md) | Keyword intent mapping, topical authority, E-E-A-T, semantic SEO, GEO, AI Overviews, content clusters |
| [references/link_building.md](references/link_building.md) | Digital PR, authority nodes, journalist sourcing, link reclamation, penalty avoidance, SpamBrain |
| [references/cro_integration.md](references/cro_integration.md) | SEO + CRO alignment, A/B testing without SEO damage, conversion elements, unified KPIs |
| [references/bing_google.md](references/bing_google.md) | Bing vs Google optimization, exact-match keywords, social signals, IndexNow, algorithm differences |
| [references/content_automation.md](references/content_automation.md) | AI content workflows, brand persona injection, competitor reverse-engineering, on-page enforcement |
