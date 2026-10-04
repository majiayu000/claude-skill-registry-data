---
name: seo
description: >
  Comprehensive SEO analysis for any website or business type. Orchestrates 52 sub-skills
  (52 active): full site audits, technical SEO (CWV/INP), schema, E-E-A-T content quality,
  images, sitemaps, GEO for AI Overviews, llms.txt generation, AI crawler audit,
  plus live GSC and Ahrefs MCP data. GSC: overview, drops, opportunities, brand-vs-nonbrand,
  cannibalization, compare, content-decay, index-issues, new-keywords. Ahrefs: overview,
  backlinks, keywords, competitors, content-gap, broken-links, new-links, anchor-analysis,
  dr-history, top-pages. Cross-MCP: serp, content-brief, brand-radar, site-audit-pro, report.
  Local: log-analysis, ai-content-check, internal-links, local, migration-check, obsidian-kb.
  AI Readability: llms-txt, robots-ai.
  Performance: lighthouse-audit, core-web-vitals, page-experience.
  Quality & AI Search: rich-results, ai-optimization, eeat-audit, helpful-content.
  Triggers on: "SEO", "audit", "schema", "Core Web Vitals", "sitemap", "E-E-A-T", "AI Overviews",
  "GEO", "technical SEO", "content quality", "structured data", "GSC", "Ahrefs",
  "backlinks", "keywords", "search console", "domain rating", "local SEO", "migration",
  "lighthouse", "pagespeed", "LCP", "INP", "CLS", "page experience", "interstitials",
  "mobile friendly", "rich results", "rich snippets", "schema eligibility", "AI optimization",
  "AI search readiness", "EEAT", "trust signals", "helpful content", "people-first",
  "content quality gate".
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
---

# SEO — Universal SEO Analysis Skill

Comprehensive SEO analysis across all industries (SaaS, local services,
e-commerce, publishers, agencies). Orchestrates 52 specialized sub-skills
(52 active) and 6 subagents.

## Quick Reference

### Active Commands (Phase 1 — Enhanced)

| Command | What it does | Status |
|---------|-------------|--------|
| `/seo audit <url>` | Full website audit with parallel subagent delegation | active |
| `/seo page <url>` | Deep single-page analysis | active |
| `/seo sitemap <url or generate>` | Analyze or generate XML sitemaps | active |
| `/seo schema <url>` | Detect, validate, and generate Schema.org markup | active |
| `/seo images <url>` | Image optimization analysis | active |
| `/seo technical <url>` | Technical SEO audit (8 categories) | active |
| `/seo content <url>` | E-E-A-T and content quality analysis | active |
| `/seo geo <url>` | AI Overviews / Generative Engine Optimization | active |
| `/seo plan <business-type>` | Strategic SEO planning | active |
| `/seo programmatic [url\|plan]` | Programmatic SEO analysis and planning | active |
| `/seo competitor-pages [url\|generate]` | Competitor comparison page generation | active |
| `/seo hreflang [url]` | Hreflang/i18n SEO audit and generation | active |

### Active Commands (Phase 2 — Live MCP Data)

| Command | What it does | Status |
|---------|-------------|--------|
| `/seo gsc overview <site>` | GSC performance overview (clicks, impressions, CTR, position) | active |
| `/seo gsc drops <site>` | Detect keyword/page ranking drops | active |
| `/seo gsc opportunities <site>` | Find high-impression, low-CTR opportunities | active |
| `/seo gsc brand-vs-nonbrand <site>` | Brand vs non-brand traffic split analysis | active |
| `/seo gsc cannibalization <site>` | Detect keyword cannibalization | active |
| `/seo gsc compare <site>` | Period-over-period comparison (MoM, YoY) | active |
| `/seo gsc content-decay <site>` | Pages losing rankings over 90 days | active |
| `/seo gsc index-issues <site>` | Pages not indexed with reasons | active |
| `/seo gsc new-keywords <site>` | Keywords started ranking for recently | active |
| `/seo ahrefs overview <domain>` | Domain authority, traffic, and top metrics | active |
| `/seo ahrefs backlinks <domain>` | Backlink profile analysis | active |
| `/seo ahrefs keywords <domain>` | Organic keyword rankings | active |
| `/seo ahrefs competitors <domain>` | Identify organic competitors | active |
| `/seo ahrefs content-gap <domain>` | Keywords competitors rank for, you don't | active |
| `/seo ahrefs broken-links <domain>` | Find broken backlinks to reclaim | active |
| `/seo ahrefs new-links <domain>` | New referring domains (last 30 days) | active |
| `/seo ahrefs anchor-analysis <domain>` | Anchor text distribution analysis | active |
| `/seo ahrefs dr-history <domain>` | Domain Rating history trend | active |
| `/seo ahrefs top-pages <domain>` | Top pages by organic traffic | active |
| `/seo markdown-audit <path>` | Markdown SEO audit (no MCP needed) | active |

### Active Commands (Phase 3 — Cross-MCP)

| Command | What it does | Status |
|---------|-------------|--------|
| `/seo serp <keyword>` | Live SERP analysis via Ahrefs + WebMCP | active |
| `/seo content-brief <keyword>` | AI content brief from SERP data | active |
| `/seo brand-radar <brand>` | AI search brand monitoring via Ahrefs Brand Radar | active |
| `/seo site-audit-pro <domain>` | Flagship multi-MCP audit (sequential wave architecture) | active |
| `/seo report <type> <domain>` | Automated report generation from available MCP data | active |

### Active Commands (Phase 4 — Local Analysis)

| Command | What it does | Status |
|---------|-------------|--------|
| `/seo log-analysis <file>` | Server log crawl budget analysis | active |
| `/seo ai-content-check <url or file>` | AI content detection and authenticity scoring | active |
| `/seo internal-links <domain>` | Internal link structure analysis and orphan detection | active |
| `/seo local <business>` | Local SEO audit (NAP, schema, GBP, citations) | active |
| `/seo migration-check <old> <new>` | Site migration redirect and SEO validator | active |
| `/seo obsidian-kb --sitemap <url>` | Build an Obsidian knowledge base from a sitemap | active |

### Active Commands (Phase 5 — AI Readability)

| Command | What it does | Status |
|---------|-------------|--------|
| `/seo llms-txt <url\|generate\|validate>` | Generate, validate, or audit llms.txt files | active |
| `/seo robots-ai <url>` | Audit robots.txt for AI crawler access policies | active |

### Active Commands (Phase 6 — Performance & Quality)

| Command | What it does | Status |
|---------|-------------|--------|
| `/seo lighthouse-audit <url>` | Lighthouse audit (CLI or PSI API fallback) with per-audit fixes and Chrome docs | active |
| `/seo core-web-vitals <url>` | CWV deep-dive — CrUX field data + lab fallback, LCP subparts, INP/CLS playbooks | active |
| `/seo page-experience <url>` | Page-experience self-assessment — HTTPS, interstitials, mobile usability, CWV, ads | active |
| `/seo rich-results <url>` | Per-type rich result eligibility check with required/recommended property gap report | active |
| `/seo ai-optimization <url>` | Audit against Google's AI Optimization guide — AI Overviews / AI Mode readiness | active |
| `/seo eeat-audit <url>` | Standalone E-E-A-T scoring rubric (0-5 per dimension) with trust signals | active |
| `/seo helpful-content <url>` | Pre-publish content-quality gate — people-first questions + spam-policy red flags | active |

## Orchestration Logic

When the user invokes `/seo audit`, delegate to subagents in parallel:
1. Detect business type (SaaS, local, ecommerce, publisher, agency, other)
2. Spawn subagents: seo-technical, seo-content, seo-schema, seo-sitemap, seo-performance, seo-visual
3. Collect results and generate unified report with SEO Health Score (0-100)
4. Create prioritized action plan (Critical → High → Medium → Low)

For individual commands, load the relevant sub-skill directly.

**Logic ownership:** All command logic lives in each sub-skill's SKILL.md (not in agent files). Agents are only used for parallel audit work within `/seo audit`.

## Command Routing

### Level 1: Command Group Detection

When the user invokes `/seo <command>`:
1. Match against the routing table below
2. If exact match with active command → load the sub-skill SKILL.md directly
3. If group match (gsc, ahrefs) → extract sub-command and route to specific sub-skill via Level 2 routing
4. If command sub-skill directory does not exist → return "Not Yet Available" message (see below)
5. If no match → suggest the closest command from the Quick Reference table

### Level 2: Sub-command Routing

For grouped commands, extract the sub-command and route to the specific sub-skill:

**GSC sub-commands** (all require GSC MCP — see `references/mcp-degradation.md`):
- `/seo gsc overview <site>` → load `seo-gsc-overview/SKILL.md`
- `/seo gsc drops <site>` → load `seo-gsc-drops/SKILL.md`
- `/seo gsc opportunities <site>` → load `seo-gsc-opportunities/SKILL.md`
- `/seo gsc brand-vs-nonbrand <site>` → load `seo-gsc-brand-vs-nonbrand/SKILL.md`
- `/seo gsc cannibalization <site>` → load `seo-gsc-cannibalization/SKILL.md`
- `/seo gsc compare <site>` → load `seo-gsc-compare/SKILL.md`
- `/seo gsc content-decay <site>` → load `seo-gsc-content-decay/SKILL.md`
- `/seo gsc index-issues <site>` → load `seo-gsc-indexing/SKILL.md`
- `/seo gsc new-keywords <site>` → load `seo-gsc-new-keywords/SKILL.md`

**Ahrefs sub-commands** (all require Ahrefs MCP — see `references/mcp-degradation.md`):
- `/seo ahrefs overview <domain>` → load `seo-ahrefs-overview/SKILL.md`
- `/seo ahrefs backlinks <domain>` → load `seo-ahrefs-backlinks/SKILL.md`
- `/seo ahrefs keywords <domain>` → load `seo-ahrefs-keywords/SKILL.md`
- `/seo ahrefs competitors <domain>` → load `seo-ahrefs-competitors/SKILL.md`
- `/seo ahrefs content-gap <domain>` → load `seo-ahrefs-content-gap/SKILL.md`
- `/seo ahrefs broken-links <domain>` → load `seo-ahrefs-broken-links/SKILL.md`
- `/seo ahrefs new-links <domain>` → load `seo-ahrefs-new-links/SKILL.md`
- `/seo ahrefs anchor-analysis <domain>` → load `seo-ahrefs-anchor-analysis/SKILL.md`
- `/seo ahrefs dr-history <domain>` → load `seo-ahrefs-dr-history/SKILL.md`
- `/seo ahrefs top-pages <domain>` → load `seo-ahrefs-top-pages/SKILL.md`

### Disambiguation Rules

Some trigger phrases match more than one sub-skill. Route by intent:

- **"AI Overviews" / "AI search"** → `seo-ai-optimization` when the user asks about Google's AI features (AI Overviews, AI Mode) or Google's official guidance; → `seo-geo` when the user targets multiple AI engines (ChatGPT, Perplexity, Claude) or says "GEO" broadly. Default for bare "optimize for AI Overviews": `seo-ai-optimization`.
- **"Core Web Vitals" / "site speed"** → `seo-core-web-vitals` for a metric-focused diagnosis (field data, LCP/INP/CLS playbooks); → `seo-technical` only when CWV is part of a broader technical audit request. Default for bare "Core Web Vitals": `seo-core-web-vitals`.
- **"E-E-A-T"** → `seo-eeat-audit` for a standalone E-E-A-T score of a URL or draft; → `seo-content` when the user wants a full content-quality audit that includes E-E-A-T.
- **"lighthouse" / "pagespeed"** → `seo-lighthouse-audit` (never `seo-technical`).

### Routing Table

Full mapping of all 52 commands to sub-skill directory names:

| Command | Sub-skill Directory | Status |
|---------|--------------------|----|
| `/seo audit` | `seo-audit/` | active |
| `/seo page` | `seo-page/` | active |
| `/seo sitemap` | `seo-sitemap/` | active |
| `/seo schema` | `seo-schema/` | active |
| `/seo images` | `seo-images/` | active |
| `/seo technical` | `seo-technical/` | active |
| `/seo content` | `seo-content/` | active |
| `/seo geo` | `seo-geo/` | active |
| `/seo plan` | `seo-plan/` | active |
| `/seo programmatic` | `seo-programmatic/` | active |
| `/seo competitor-pages` | `seo-competitor-pages/` | active |
| `/seo hreflang` | `seo-hreflang/` | active |
| `/seo gsc overview` | `seo-gsc-overview/` | active |
| `/seo gsc drops` | `seo-gsc-drops/` | active |
| `/seo gsc opportunities` | `seo-gsc-opportunities/` | active |
| `/seo gsc brand-vs-nonbrand` | `seo-gsc-brand-vs-nonbrand/` | active |
| `/seo gsc cannibalization` | `seo-gsc-cannibalization/` | active |
| `/seo gsc compare` | `seo-gsc-compare/` | active |
| `/seo gsc content-decay` | `seo-gsc-content-decay/` | active |
| `/seo gsc index-issues` | `seo-gsc-indexing/` | active |
| `/seo gsc new-keywords` | `seo-gsc-new-keywords/` | active |
| `/seo ahrefs overview` | `seo-ahrefs-overview/` | active |
| `/seo ahrefs backlinks` | `seo-ahrefs-backlinks/` | active |
| `/seo ahrefs keywords` | `seo-ahrefs-keywords/` | active |
| `/seo ahrefs competitors` | `seo-ahrefs-competitors/` | active |
| `/seo ahrefs content-gap` | `seo-ahrefs-content-gap/` | active |
| `/seo ahrefs broken-links` | `seo-ahrefs-broken-links/` | active |
| `/seo ahrefs new-links` | `seo-ahrefs-new-links/` | active |
| `/seo ahrefs anchor-analysis` | `seo-ahrefs-anchor-analysis/` | active |
| `/seo ahrefs dr-history` | `seo-ahrefs-dr-history/` | active |
| `/seo ahrefs top-pages` | `seo-ahrefs-top-pages/` | active |
| `/seo markdown-audit` | `seo-markdown-audit/` | active |
| `/seo serp` | `seo-serp/` | active |
| `/seo content-brief` | `seo-content-brief/` | active |
| `/seo brand-radar` | `seo-brand-radar/` | active |
| `/seo site-audit-pro` | `seo-site-audit-pro/` | active |
| `/seo report` | `seo-report/` | active |
| `/seo log-analysis` | `seo-log-analysis/` | active |
| `/seo ai-content-check` | `seo-ai-content-check/` | active |
| `/seo internal-links` | `seo-internal-links/` | active |
| `/seo local` | `seo-local/` | active |
| `/seo migration-check` | `seo-migration-check/` | active |
| `/seo obsidian-kb` | `seo-obsidian-kb/` | active |
| `/seo llms-txt` | `seo-llms-txt/` | active |
| `/seo robots-ai` | `seo-robots-ai/` | active |
| `/seo lighthouse-audit` | `seo-lighthouse-audit/` | active |
| `/seo core-web-vitals` | `seo-core-web-vitals/` | active |
| `/seo page-experience` | `seo-page-experience/` | active |
| `/seo rich-results` | `seo-rich-results/` | active |
| `/seo ai-optimization` | `seo-ai-optimization/` | active |
| `/seo eeat-audit` | `seo-eeat-audit/` | active |
| `/seo helpful-content` | `seo-helpful-content/` | active |

### Unavailable Command Response

If a command's sub-skill directory does not exist:
1. Tell the user: "`[command]` is not yet available."
2. Suggest an alternative from the active commands that provides partial value.
3. Do NOT attempt to fabricate the functionality inline.

Example response for unavailable command (Phase 4 and beyond):
```
/seo [command] is not yet available.

While waiting, you can use:
- `/seo audit <url>` — full site audit using available static analysis
- `/seo site-audit-pro <domain>` — comprehensive multi-MCP audit with live Ahrefs and GSC data
```

## Industry Detection

Detect business type from homepage signals:
- **SaaS**: pricing page, /features, /integrations, /docs, "free trial", "sign up"
- **Local Service**: phone number, address, service area, "serving [city]", Google Maps embed
- **E-commerce**: /products, /collections, /cart, "add to cart", product schema
- **Publisher**: /blog, /articles, /topics, article schema, author pages, publication dates
- **Agency**: /case-studies, /portfolio, /industries, "our work", client logos

## Quality Gates

Read `references/quality-gates.md` for thin content thresholds per page type.
Hard rules:
- WARNING at 30+ location pages (enforce 60%+ unique content)
- HARD STOP at 50+ location pages (require user justification)
- Never recommend HowTo schema (deprecated Sept 2023)
- FAQ schema only for government and healthcare sites
- All Core Web Vitals references use INP, never FID

## Reference Files

Load these on-demand as needed — do NOT load all at startup:
- `references/cwv-thresholds.md` — Current Core Web Vitals thresholds and measurement details
- `references/schema-types.md` — All supported schema types with deprecation status
- `references/eeat-framework.md` — E-E-A-T evaluation criteria (Sept 2025 QRG update)
- `references/quality-gates.md` — Content length minimums, uniqueness thresholds
- `references/mcp-degradation.md` — MCP availability checks, error templates, fallback mapping
- `references/ahrefs-api-reference.md` — Ahrefs MCP tool mapping, response fields, monetary conversion
- `references/gsc-api-reference.md` — GSC MCP tool mapping, property formats, response fields
- `references/llms-txt-spec.md` — llms.txt specification, format rules, tooling, examples, 2000+ adopter list
- `references/ai-crawlers-guide.md` — AI crawler registry, robots.txt tokens, blocking stats, strategy templates

## Scoring Methodology

### SEO Health Score (0-100)
Weighted aggregate of all categories:

| Category | Weight |
|----------|--------|
| Technical SEO | 25% |
| Content Quality | 25% |
| On-Page SEO | 20% |
| Schema / Structured Data | 10% |
| Performance (CWV) | 10% |
| Images | 5% |
| AI Search Readiness | 5% |

### Priority Levels
- **Critical**: Blocks indexing or causes penalties (immediate fix required)
- **High**: Significantly impacts rankings (fix within 1 week)
- **Medium**: Optimization opportunity (fix within 1 month)
- **Low**: Nice to have (backlog)

## Sub-Skills

This skill orchestrates 52 specialized sub-skills (52 active):

**Active (Phase 1 — Static Analysis):**
1. **seo-audit** — Full website audit with parallel delegation
2. **seo-page** — Deep single-page analysis
3. **seo-technical** — Technical SEO (8 categories)
4. **seo-content** — E-E-A-T and content quality
5. **seo-schema** — Schema markup detection and generation
6. **seo-images** — Image optimization
7. **seo-sitemap** — Sitemap analysis and generation
8. **seo-geo** — AI Overviews / GEO optimization
9. **seo-plan** — Strategic planning with templates
10. **seo-programmatic** — Programmatic SEO analysis and planning
11. **seo-competitor-pages** — Competitor comparison page generation
12. **seo-hreflang** — Hreflang/i18n SEO audit and generation

**Active (Phase 2 — GSC MCP, requires GSC MCP registration):**
13. **seo-gsc-overview** — GSC performance dashboard
14. **seo-gsc-drops** — Ranking drop detection
15. **seo-gsc-opportunities** — High-impression, low-CTR opportunity finder
16. **seo-gsc-brand-vs-nonbrand** — Brand vs non-brand traffic split analysis
17. **seo-gsc-cannibalization** — Keyword cannibalization detection
18. **seo-gsc-compare** — Period-over-period comparison
19. **seo-gsc-content-decay** — Pages losing rankings over 90 days
20. **seo-gsc-indexing** — Pages not indexed with reasons
21. **seo-gsc-new-keywords** — Keywords started ranking for recently

**Active (Phase 2 — Ahrefs MCP):**
22. **seo-ahrefs-overview** — Domain authority and top metrics
23. **seo-ahrefs-backlinks** — Backlink profile analysis
24. **seo-ahrefs-keywords** — Organic keyword rankings
25. **seo-ahrefs-competitors** — Organic competitor identification
26. **seo-ahrefs-content-gap** — Content gap analysis
27. **seo-ahrefs-broken-links** — Broken backlink recovery
28. **seo-ahrefs-new-links** — New referring domain monitoring
29. **seo-ahrefs-anchor-analysis** — Anchor text distribution
30. **seo-ahrefs-dr-history** — Domain Rating history
31. **seo-ahrefs-top-pages** — Top pages by organic traffic

**Active (Phase 2 — Local/No MCP):**
32. **seo-markdown-audit** — Markdown file SEO audit (no MCP needed)

**Active (Phase 3 — Cross-MCP):**
33. **seo-serp** — Live SERP analysis
34. **seo-content-brief** — AI content brief from SERP data
35. **seo-brand-radar** — Brand monitoring via Ahrefs Brand Radar
36. **seo-site-audit-pro** — Flagship multi-MCP audit (sequential wave)
37. **seo-report** — Automated report generation

**Active (Phase 4 — Local Analysis):**
38. **seo-log-analysis** — Server log crawl budget analysis
39. **seo-ai-content-check** — AI content detection
40. **seo-internal-links** — Internal link structure audit
41. **seo-local** — Local SEO audit
42. **seo-migration-check** — Site migration validator
43. **seo-obsidian-kb** — Obsidian knowledge base builder from sitemap

**Active (Phase 5 — AI Readability):**
44. **seo-llms-txt** — llms.txt generation, validation, and audit
45. **seo-robots-ai** — AI crawler robots.txt audit

**Active (Phase 6 — Performance & Quality):**
46. **seo-lighthouse-audit** — Lighthouse audits with per-audit fixes and Chrome docs
47. **seo-core-web-vitals** — CWV deep-dive (CrUX field data, LCP subparts, INP/CLS playbooks)
48. **seo-page-experience** — Google page-experience self-assessment
49. **seo-rich-results** — Per-type rich result eligibility checker
50. **seo-ai-optimization** — Google AI Optimization guide audit (AI Overviews / AI Mode readiness)
51. **seo-eeat-audit** — Standalone E-E-A-T scoring rubric with trust signals
52. **seo-helpful-content** — Pre-publish people-first content-quality gate

## Subagents

For parallel analysis during audits:
- `seo-technical` — Crawlability, indexability, security, CWV
- `seo-content` — E-E-A-T, readability, thin content
- `seo-schema` — Detection, validation, generation
- `seo-sitemap` — Structure, coverage, quality gates
- `seo-performance` — Core Web Vitals measurement
- `seo-visual` — Screenshots, mobile testing, above-fold
