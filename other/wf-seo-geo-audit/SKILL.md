---
name: wf-seo-geo-audit
description: >
  Combined SEO + GEO audit and optimization workflow. Runs traditional SEO audit
  and AI search optimization in parallel, then produces a unified action plan
  covering both Google rankings and AI citations. Use when user says "full SEO
  and GEO audit", "audit my site for SEO and AI", "SEO + AI visibility",
  "comprehensive site audit", "optimize for Google and AI", "audit for search
  and AI engines", or "complete search audit". Chains 15+ SEO and GEO skills.
---

# SEO + GEO Combined Audit Workflow

Run a comprehensive search audit covering traditional SEO and AI engine optimization.

## Phase 1: Parallel Audits

Dispatch these two audits concurrently:

### Track A — Traditional SEO Audit
Invoke `seo-audit` which orchestrates:
- `seo-technical` — crawlability, indexability, security, Core Web Vitals
- `seo-content` — E-E-A-T, readability, thin content
- `seo-schema` — structured data detection and validation
- `seo-sitemap` — XML sitemap analysis
- `seo-images` — alt text, file sizes, formats, lazy loading
- `seo-page` — deep dive on key pages
- `seo-hreflang` — international SEO (if multi-language detected)

### Track B — GEO Audit
Invoke `geo-audit` which orchestrates:
- `geo-citability` — passage-level AI citation scoring
- `geo-crawlers` — AI crawler access map (GPTBot, ClaudeBot, etc.)
- `geo-llmstxt` — llms.txt analysis/generation
- `geo-brand-mentions` — brand authority across AI training sources
- `geo-content` — E-E-A-T for AI citability
- `geo-schema` — structured data for AI discoverability
- `geo-technical` — technical audit with GEO-specific checks
- `geo-platform-optimizer` — per-platform optimization (ChatGPT, Perplexity, Gemini, etc.)

**Output**: Two parallel reports — SEO Health Score + GEO Score (both 0-100).

---

## Phase 2: Gap Analysis (after both audits complete)

### Step 2A — Cross-Reference Findings
Compare overlapping areas:
- Schema: `seo-schema` vs `geo-schema` — unified recommendation
- Content: `seo-content` vs `geo-content` — E-E-A-T alignment
- Technical: `seo-technical` vs `geo-technical` — merge issues lists

### Step 2B — AI SEO Deep Dive
Invoke `ai-seo` with findings from both tracks:
- Three-pillar optimization (Structure, Authority, Presence)
- Platform-specific recommendations

### Step 2C — Site Architecture Review
Invoke `site-architecture` if structural issues found:
- Internal linking optimization for both crawlers and AI
- Topic cluster architecture

---

## Phase 3: Action Plan

### Step 3A — Content Strategy
Invoke `content-strategy` informed by both audits:
- Topics that serve both Google rankings AND AI citations
- Content gap priorities

### Step 3B — Schema Implementation
Invoke `schema-markup` for:
- Unified JSON-LD implementation covering both SEO rich results and AI discoverability

### Step 3C — Programmatic SEO (if applicable)
Invoke `programmatic-seo` if scale opportunities identified:
- Template pages, data sources, thin content safeguards

---

## Phase 4: Reporting

### Step 4A — Client Report
Invoke `geo-report` to generate combined report, then
Invoke `geo-report-pdf` for PDF deliverable

### Step 4B — Competitor Comparison Pages (if relevant)
Invoke `competitor-alternatives` or `seo-competitor-pages` for:
- "vs" and "alternatives" pages targeting competitor keywords

---

## Skill Chain Summary

```
Phase 1 (parallel): seo-audit ║ geo-audit
Phase 2 (sequential): cross-reference → ai-seo → site-architecture
Phase 3 (parallel): content-strategy + schema-markup + programmatic-seo
Phase 4: geo-report → geo-report-pdf
```

## Rules
- Phase 1 tracks MUST run in parallel for efficiency.
- If user only wants SEO or only GEO, run just that track — but recommend the other.
- De-duplicate overlapping recommendations between SEO and GEO.
- Phase 4 reporting is optional — ask user if they need a client-facing deliverable.
