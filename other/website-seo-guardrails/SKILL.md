---
name: website-seo-guardrails
description: Audit, design, write, and validate comprehensive website SEO while preventing indexing, quality, spam-policy, crawling, structured-data, scaling, migration, backlink, keyword, Lighthouse, and measurement failures. Use for technical or on-page audits; standardized Google Lighthouse runs; interpreting Lighthouse JSON, HTML, screenshots, or pasted recommendations; prioritized improvements and comparable before/after retests; Google Trends brand, product, category, seasonal, regional, or content research; deciding whether pages, blogs, courses, tools, directories, or generated content should be indexed; SEO writing; Google Search Console, Bing Webmaster Tools, IndexNow, Ahrefs, sitemaps, robots, canonicals, schema, and AI-search visibility; or pre-launch reviews. Apply to new sites, redesigns, migrations, programmatic content, ecommerce, local, multilingual, and JavaScript-rendered sites.
---

# Website SEO Guardrails

Prevent material search risks before chasing marginal optimizations. Treat crawlability, indexability, content value, policy compliance, and measurement as separate gates.

## Operating principles

1. Protect users and the domain before pursuing traffic.
2. Make every indexable URL independently useful; public does not automatically mean indexable.
3. Prefer a smaller coherent index over many thin, repetitive, or speculative pages.
4. Keep visible content, metadata, structured data, canonicals, sitemaps, and robots directives consistent.
5. Treat tool scores and character counts as operational heuristics, not ranking guarantees.
6. Separate observed facts, tool findings, hypotheses, and recommendations.
7. Never guarantee ranking, indexing, rich results, backlinks, or AI citations.
8. Distinguish implementation from account operations: an audit does not authorize submitting URLs, changing settings, linking products, enabling ads, or accepting terms.

## Mandatory workflow

### 1. Establish scope and evidence

Identify the canonical production origin, site purpose, audiences, markets, content types, framework/CMS, rendering mode, analytics, webmaster access, recent migrations, and business constraints. Inspect rendered output as well as source code when possible.

Record evidence from crawls, HTTP responses, rendered HTML, Search Console, Bing Webmaster Tools, analytics, server/CDN logs, backlink tools, and repository tests. Do not report an unverified assumption as a defect.

### 2. Run the catastrophic-risk gate

Check first for:

- sitewide or template-level `noindex`, robots blocks, authentication, firewall, CDN, or bot challenges;
- production pages returning errors, soft 404s, redirect loops/chains, or empty client-rendered shells;
- wrong host/protocol canonicals, conflicting canonicals, sitemap/canonical/noindex contradictions;
- hacked pages, injected spam, malware, manual actions, security issues, or leaked staging URLs;
- accidental mass publication, faceted URL explosions, internal-search indexing, or generated thin pages;
- domain/site migrations without URL mapping, permanent redirects, updated internal links, and monitoring;
- deceptive structured data, fake reviews, false authorship, fake dates, or hidden marked-up content;
- paid/manipulative links, doorway pages, cloaking, scraped content, or scaled content made mainly to rank.

Stop and escalate these before ordinary metadata work. Read [references/01-risk-and-indexability.md](references/01-risk-and-indexability.md) and [references/05-spam-and-policy.md](references/05-spam-and-policy.md).

### 3. Build the URL inventory and indexability matrix

For each page family, record: URL pattern, purpose, owner, source, status, canonical, robots state, sitemap inclusion, internal-link depth, structured-data type, uniqueness/value evidence, freshness rule, and action (`index`, `noindex-follow`, `merge`, `redirect`, `remove`, or `hold`).

Require an explicit allowlist for large generated page families. Only substantively authored lessons, standalone informational articles, and editorially reviewed profiles should earn indexability; usable but repetitive pages may remain public with `noindex,follow` and must stay out of XML sitemaps.

### 4. Design useful website inclusions

Evaluate service/product pages, comparison pages, documentation, original tools/calculators, courses, glossaries, case studies, research, blogs, FAQs, datasets, directories, location pages, and media by user need and first-hand value. Do not create a format merely because it can target keywords. Read [references/02-content-architecture.md](references/02-content-architecture.md).

When page purpose, audience, positioning, journey coverage, conversion friction, information architecture, or content format is uncertain, use the smallest applicable model from [references/17-strategy-behaviour-and-content-frameworks.md](references/17-strategy-behaviour-and-content-frameworks.md). Record the model's inputs, conclusion, evidence, and limitation; do not stack frameworks to manufacture certainty.

For brand keyword, demand-direction, seasonality, regional-language, content-calendar, or product-naming research, use Google Trends as relative evidence rather than search volume. Read [references/15-google-trends-brand-keywords.md](references/15-google-trends-brand-keywords.md) before interpreting a 0-100 score, a zero, a spike, a regional map, or a Rising/Breakout query.

### 5. Write and optimize each approved page

Define primary intent, audience, decision/job to be done, unique evidence, target query cluster, internal-link role, and conversion or learning outcome. Write for task completion, then optimize titles, descriptions, headings, URLs, links, images, and previews. Use the thresholds in [references/03-on-page-writing.md](references/03-on-page-writing.md).

### 6. Validate technical discovery

Validate response codes, rendered content, crawlable links, robots, meta/X-Robots directives, canonicals, sitemaps, pagination/facets, JavaScript rendering, mobile behavior, Core Web Vitals, media discoverability, hreflang, and migrations. Read [references/04-technical-seo.md](references/04-technical-seo.md).

When the user supplies a Lighthouse report or asks for a Lighthouse audit, read [references/16-lighthouse-report-improvement.md](references/16-lighthouse-report-improvement.md). Use the standardized three-run, median-based workflow. Prefer Lighthouse JSON over HTML, screenshots, or copied text; treat missing report sections as unknown. An audit authorizes analysis, not repository edits or deployment. Implement fixes only when requested, then retest representative pages with the same baseline configuration.

### 7. Add only truthful enhancements

Add structured data only when it represents visible primary content and follows the feature-specific policy. Configure GSC, Bing Webmaster Tools, IndexNow, Ahrefs, analytics, and alerts. Address backlinks and AI search without hacks. Use [references/06-structured-data.md](references/06-structured-data.md), [references/07-tools-and-monitoring.md](references/07-tools-and-monitoring.md), [references/08-authority-and-links.md](references/08-authority-and-links.md), and [references/09-ai-search.md](references/09-ai-search.md).

When live UI evidence is required and no connector/API/CLI covers the operation, use the available `browser:control-in-app-browser` skill for Google Trends, Google Search Console, Bing Webmaster Tools, GA4, or AdSense. Default to read-only inspection. Follow [references/11-browser-workflows.md](references/11-browser-workflows.md); use [references/12-ga4-readiness.md](references/12-ga4-readiness.md), [references/13-adsense-readiness.md](references/13-adsense-readiness.md), and [references/15-google-trends-brand-keywords.md](references/15-google-trends-brand-keywords.md) for the relevant implementation.

### 8. Preflight, release, and monitor

Run tests on production-like rendered output. Use `scripts/seo_preflight.py` for a deterministic first pass, then perform the manual checks it cannot prove. Release in reviewable batches, annotate changes, submit only changed canonical URLs where appropriate, and compare outcome cohorts over multiple weeks.

## Severity model

- **P0 — emergency:** security compromise, sitewide deindexing, manual action, destructive migration, or widespread serving failure.
- **P1 — critical:** major indexable templates blocked/broken, mass thin/spam exposure, canonical corruption, or large traffic/revenue path failure.
- **P2 — high:** important orphan pages, incorrect sitemap/noindex state, material duplication, misleading schema, broken internal architecture, or persistent performance failure.
- **P3 — normal:** missing/weak titles, descriptions, alt text, minor schema warnings, isolated links, or content improvements.
- **Observation:** not yet evidenced as harmful; monitor or test.

Prioritize by severity × affected URLs × business importance × confidence. Do not bury a P1 issue under hundreds of low-impact warnings.

## Required deliverables

Unless the user asks for another format, produce:

1. Executive risk summary.
2. Evidence-backed findings with URL/examples and confidence.
3. URL-family indexability matrix.
4. Recommended information architecture and content opportunities.
5. Prioritized remediation backlog with owner, acceptance test, and rollback note.
6. Measurement plan and monitoring cadence.
7. Explicit limitations and items needing webmaster/tool access.
8. When Lighthouse is in scope: run configuration, plain-language findings, prioritized fixes, implementation status, and comparable before/after evidence.

## Navigation

Read [references/INDEX.md](references/INDEX.md) for the complete documentation index and [scripts/INDEX.md](scripts/INDEX.md) for automation usage. Source links and review dates live in [references/10-sources.md](references/10-sources.md); re-check them for policy-sensitive or current work.

## Creator

Created for and maintained by [Brownsmith Dynamics](https://brownsmithdynamics.com).
