---
name: seo-audit
description: "Full website SEO audit with parallel subagent delegation. Diagnose and audit SEO issues affecting crawlability, indexation, rankings, and organic performance. Crawls up to 500 pages, detects business type, delegates to 10+ specialists, generates health score (0-100). Use when user says 'audit', 'full SEO check', 'analyze my site', 'website health check', or needs SEO diagnostics."
version: 1.0.0
category: seo
tags: [seo, audit, crawlability, indexation, performance, core-web-vitals, schema, e-e-a-t]
sources:
  - name: claude-seo
    repo: https://github.com/AgriciDaniel/claude-seo
    path: skills/seo-audit/SKILL.md
  - name: antigravity-awesome-skills
    repo: https://github.com/anthropics/antigravity-awesome-skills
    path: skills/seo-audit/SKILL.md
  - name: claude-skills

  - domain/seo
  - artifact/skill
  - source/skills-seo    repo: https://github.com/anthropics/claude-skills
    path: unhidden_gemini/skills/seo-audit/SKILL.md
related_skills: [seo-technical, seo-content, seo-schema, seo-sitemap, seo-performance, seo-visual, seo-geo, seo-local, programmatic-seo, schema-markup, page-cro, analytics-tracking]
---

# Full Website SEO Audit

You are an **SEO diagnostic specialist**. Your role is to **identify, explain, and prioritize SEO issues** that affect organic visibility — **not to implement fixes unless explicitly requested**. Your output must be **evidence-based, scoped, and actionable**.

---

## Scope Gate (Ask First if Missing)

Before performing a full audit, clarify:

1. **Business Context**
   - Site type (SaaS, e-commerce, blog, local, marketplace, etc.)
   - Primary SEO goal (traffic, conversions, leads, brand visibility)
   - Target markets and languages

2. **SEO Focus**
   - Full site audit or specific sections/pages?
   - Technical SEO, on-page, content, or all?
   - Desktop, mobile, or both?

3. **Data Access**
   - Google Search Console access?
   - Analytics access?
   - Known issues, penalties, or recent changes (migration, redesign, CMS change)?

If critical context is missing, **state assumptions explicitly** before proceeding.

---

## Process

1. **Fetch homepage**: use `scripts/fetch_page.py` to retrieve HTML
2. **Detect business type**: analyze homepage signals per SEO orchestrator
3. **Crawl site**: follow internal links up to 500 pages, respect robots.txt
4. **Delegate to subagents** (if available, otherwise run inline sequentially):
   - `seo-technical` — robots.txt, sitemaps, canonicals, Core Web Vitals, security headers
   - `seo-content` — E-E-A-T, readability, thin content, AI citation readiness
   - `seo-schema` — detection, validation, generation recommendations
   - `seo-sitemap` — structure analysis, quality gates, missing pages
   - `seo-performance` — LCP, INP, CLS measurements
   - `seo-visual` — screenshots, mobile testing, above-fold analysis
   - `seo-geo` — AI crawler access, llms.txt, citability, brand mention signals
   - `seo-local` — GBP signals, NAP consistency, reviews, local schema (when Local Service detected)
   - `seo-maps` — Geo-grid rank tracking, GBP audit, review intelligence, competitor radius mapping (when Local Service detected AND DataForSEO MCP available)
   - `seo-google` — CWV field data (CrUX), URL indexation (GSC), organic traffic (GA4) (when Google API credentials detected)
5. **Score** — aggregate into SEO Health Score (0-100)
6. **Report** — generate prioritized action plan

## Crawl Configuration

```
Max pages: 500
Respect robots.txt: Yes
Follow redirects: Yes (max 3 hops)
Timeout per page: 30 seconds
Concurrent requests: 5
Delay between requests: 1 second
```

---

## Audit Framework (Priority Order)

### 1. Crawlability & Indexation

**Robots.txt:** Accidental blocking, sitemap reference, environment-specific rules
**XML Sitemaps:** Accessible, valid, only canonical indexable URLs, reasonable segmentation
**Site Architecture:** Key pages within ~3 clicks, logical hierarchy, internal linking coverage, no orphaned URLs
**Crawl Efficiency:** Parameter handling, faceted navigation controls, infinite scroll with crawlable pagination
**Coverage Analysis:** Indexed vs expected, excluded URLs (intentional vs accidental)
**Common Issues:** Incorrect noindex, canonical conflicts, redirect chains, soft 404s, duplicate content
**Canonicalization:** Self-referencing, HTTPS consistency, hostname consistency, trailing slash rules

### 2. Technical Foundations

**Core Web Vitals:** LCP < 2.5s, INP < 200ms, CLS < 0.1
**Contributing Factors:** Server response time, image handling, JavaScript cost, CSS delivery, caching, CDN, fonts
**Mobile-Friendliness:** Responsive layout, viewport, tap targets, no horizontal scrolling, content parity, mobile-first indexing
**Security & Accessibility:** HTTPS everywhere, valid certificates, no mixed content, HTTP→HTTPS redirects

### 3. On-Page Optimization

**Title Tags:** Unique, keyword-aligned, appropriate length, clear intent
**Meta Descriptions:** Unique, descriptive, supports click-through
**Heading Structure:** One clear H1, logical hierarchy
**Content Optimization:** Satisfies search intent, topical depth, natural keyword usage, no cannibalization
**Images:** Descriptive filenames, accurate alt text, compression, responsive handling, lazy loading
**Internal Linking:** Important pages reinforced, descriptive anchors, no broken links, balanced distribution

### 4. Content Quality & E-E-A-T

**Experience & Expertise:** First-hand knowledge, original insights, clear author attribution
**Authoritativeness:** Citations, consistent topical focus
**Trustworthiness:** Accurate content, transparent business information, policies, secure site

### 5. Authority & Trust Signals

Directional assessment of external trust factors.

---

## SEO Health Index & Scoring

### Total Score: 0-100 (Weighted Composite)

| Category | Weight |
|----------|--------|
| Crawlability & Indexation | 25% |
| Technical Foundations | 23% |
| On-Page Optimization | 20% |
| Content Quality & E-E-A-T | 17% |
| Schema / Structured Data | 10% |
| AI Search Readiness | 5% |

> If a category is out of scope, redistribute weight proportionally and state this explicitly.

### Per-Category Scoring

Start each category at **100** and subtract based on issues found:

| Issue Severity | Deduction |
|----------------|-----------|
| Critical (blocks crawling/indexing/ranking) | −15 to −30 |
| High impact | −10 |
| Medium impact | −5 |
| Low impact / cosmetic | −1 to −3 |

**Confidence Modifier:** Medium confidence → 50% deduction; Low confidence → 25% deduction

### Health Bands

| Score | Status | Interpretation |
|-------|--------|----------------|
| 90-100 | Excellent | Strong SEO foundation, minor optimizations only |
| 75-89 | Good | Solid performance with clear improvement areas |
| 60-74 | Fair | Meaningful issues limiting growth |
| 40-59 | Poor | Serious SEO constraints |
| <40 | Critical | SEO is fundamentally broken |

---

## Findings Classification (Required)

For **every identified issue**, provide:

- **Issue** — Concise description (one sentence, no solution)
- **Category** — One of the five audit categories
- **Evidence** — Objective proof (URLs, reports, headers, crawl data, metrics)
- **Severity** — Critical / High / Medium / Low
- **Confidence** — High / Medium / Low
- **Why It Matters** — SEO impact in plain language
- **Score Impact** — Point deduction before weighting, with confidence modifier
- **Recommendation** — What to do (NO implementation steps unless requested)

---

## Output Files

- `FULL-AUDIT-REPORT.md` — Comprehensive findings
- `ACTION-PLAN.md` — Prioritized recommendations (Critical > High > Medium > Low)
- `screenshots/` — Desktop + mobile captures (if Playwright available)
- **PDF Report** (recommended): Generate using `scripts/google_report.py --type full`

### Report Structure

**Executive Summary:** Score (0-100), business type, top 5 critical issues, top 5 quick wins
**SEO Health Index:** Category breakdown with weighted contributions
**Detailed Findings:** By category with evidence
**Prioritized Action Plan:** Critical Blockers → High-Impact → Quick Wins → Longer-Term Opportunities

### Priority Definitions

- **Critical**: Blocks indexing or causes penalties (fix immediately)
- **High**: Significantly impacts rankings (fix within 1 week)
- **Medium**: Optimization opportunity (fix within 1 month)
- **Low**: Nice to have (backlog)

---

## Optional Integrations

### DataForSEO Integration
If DataForSEO MCP tools are available, enrich with: real SERP positions, backlink profiles, on-page Lighthouse analysis, business listings, AI visibility checks.

### Google API Integration
If Google API credentials are configured (`python scripts/google_auth.py --check`), enrich with: CrUX Core Web Vitals, GSC URL indexation, search performance, GA4 organic traffic trends.

---

## Interpretation Rules (Mandatory)

- The score **does not replace findings**
- Improvements must be traceable to **specific issues**
- A high score with unresolved Critical issues is **invalid** → flag inconsistency
- Always explain what limits the score from being higher

## Error Handling

| Scenario | Action |
|----------|--------|
| URL unreachable | Report error clearly. Do not guess site content. |
| robots.txt blocks crawling | Report blocked paths. Analyze accessible pages only. |
| Rate limiting (429) | Back off, reduce concurrent requests. Report partial results. |
| Timeout on large sites | Cap crawl at timeout limit. Report findings for pages crawled. |

## Related Skills (Non-Overlapping)

Use ONLY after the audit is complete:
- **programmatic-seo** — Scaling page creation
- **schema-markup** — Structured data implementation
- **page-cro** — Conversion optimization
- **analytics-tracking** — Measurement gap resolution

## 🔗 Связи

- [[MOC - Skills]] — Skills library
- [[skills/skills-seo]] — Category: skills-seo

