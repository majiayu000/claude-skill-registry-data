---
name: pipeline-seo-geo-aeo
version: 1.0.0
description: "Standalone SEO/GEO/AEO audit pipeline — 7 stages: technical SEO, structured data, E-E-A-T, AEO, GEO, architecture, and report. Runs against a URL or content files, produces a severity-tiered report with composite score. Can be invoked standalone or as an optional deep-SEO stage within pipeline-content."
---

# /pipeline-seo-geo-aeo — SEO/GEO/AEO Audit Pipeline

Audits existing content or live URLs for SEO, GEO, and AEO readiness. Does NOT create content — that's `/pipeline-content`'s job. This pipeline checks what exists and reports what needs fixing.

## Input

- **url** (required if no files): live URL to audit
- **files** (required if no url): content files to audit (markdown, HTML)
- **scope** (optional): `full` (default) | `technical-only` | `content-only` | `geo-only`
- **brand** (optional): brand name for entity authority checks

## Pipeline State

Create tracker at `.gstack/pipeline-seo-geo-aeo-{date}.md`:

```markdown
## Pipeline: SEO/GEO/AEO Audit
Started: {timestamp}
Target: {url or files}
Scope: {scope}

| # | Stage | Status | Score | Top Issue |
|---|-------|--------|-------|-----------|
| 1 | TECHNICAL | pending | —/10 | — |
| 2 | STRUCTURED DATA | pending | —/10 | — |
| 3 | EEAT | pending | —/10 | — |
| 4 | AEO | pending | —/10 | — |
| 5 | GEO | pending | —/10 | — |
| 6 | ARCHITECTURE | pending | —/10 | — |
| 7 | REPORT | pending | — | — |
```

---

## Stage 1: TECHNICAL

Load `seo-aeo-best-practices/references/technical-seo.md`.

**Check (URL mode):**
- Fetch page HTML (use browse/curl)
- Title tag: present, 50-60 chars, keyword in title
- Meta description: present, 150-160 chars
- Canonical tag: present, correct URL
- Open Graph: `og:title`, `og:description`, `og:image` all present
- HTTPS: URL uses HTTPS
- Fetch `/robots.txt`: check AI crawler entries (GPTBot, ClaudeBot, PerplexityBot)
- Check for `<link rel="sitemap">` or `/sitemap.xml`

**Check (file mode):**
- Verify metadata frontmatter or HTML `<head>` section
- Check for canonical, OG tags in template/layout

**Gate:** Pass if no Critical issues. Missing canonical = High. Missing meta title = Critical.

---

## Stage 2: STRUCTURED DATA

Load `seo-aeo-best-practices/references/structured-data.md`.

**Check:**
- Extract all `<script type="application/ld+json">` blocks
- Identify schema types present
- For each type: validate required fields against reference templates
- Flag missing required fields, date format errors, mismatched content
- Flag schema types that SHOULD be present but aren't:
  - Blog post without Article schema = High
  - FAQ section without FAQPage schema = Medium
  - Homepage without Organization schema = High

**Gate:** Pass if no Critical issues. Missing required field on existing schema = Critical. Expected schema entirely absent = High.

---

## Stage 3: E-E-A-T (parallel with 4, 5)

Load `seo-aeo-best-practices/references/eeat-principles.md`.

**Check:**
- Author attribution visible on page
- Author bio page linked (check for `/about/`, `/team/`, `/author/` links)
- Publication/update date visible
- Sources cited for factual claims (look for inline citations, references section)
- YMYL topic detection (health/finance/legal keywords) — if detected, flag missing credentials as Critical
- Person schema on author page (if accessible)
- Organization schema with `sameAs` on homepage

**Gate:** Pass if no Critical issues. YMYL without credentials = always Critical.

---

## Stage 4: AEO (parallel with 3, 5)

Load `seo-aeo-best-practices/references/aeo-optimization.md`.

**Check:**
- Primary question answered in first 100 words
- H2 headings present — are they question-phrased or topic-clear?
- FAQPage schema present if FAQ section detected (cross-reference Stage 2)
- Content length vs. intent category (flag padding or thinness)
- Extraction zone present for long content (>1,500 words): TL;DR, summary, key takeaways

**Gate:** Pass if no Critical issues. No answer in first 100 words = High.

---

## Stage 5: GEO (parallel with 3, 4)

Load `seo-aeo-best-practices/references/geo-optimization.md`.

**Check:**
- BLUF structure: does each major section open with a direct statement?
- Quantitative claims: count data points with sources
- Organization schema with `sameAs` (cross-reference Stage 2)
- AI crawler access: cross-reference Stage 1 robots.txt — flag if GPTBot/ClaudeBot/PerplexityBot blocked
- Original data or third-party citations present
- Entity authority: check if `sameAs` includes Wikipedia/Wikidata URLs

**Note:** Full GEO measurement (AI mention tracking) cannot be automated in a single audit. Flag as "Recommended: set up GEO monitoring" with tool suggestions.

**Gate:** Pass if AI crawlers not blocked and entity schema signals present. Everything else = Medium or Low.

---

## Stage 6: ARCHITECTURE (skip if URL-only with no site access)

Load `seo-aeo-best-practices/references/content-architecture.md`.

**Check:**
- Internal links: count outbound internal links on page, flag if zero
- URL structure: check for length, date inclusion, parameter sprawl
- Heading hierarchy: H1 → H2 → H3 (no skipped levels)
- Content freshness: `dateModified` in schema vs. visible date

**Gate:** Skip gracefully if no site-wide access. Flag what can be checked on a single page.

---

## Stage 7: REPORT

Load `seo-aeo-best-practices/references/integration-checklist.md` for scoring calibration.

**Output format:**

```markdown
## SEO/GEO/AEO Audit Report

**Target:** {url or files}
**Date:** {YYYY-MM-DD}
**Scope:** {scope}

---

### Composite Score

| Area | Score | Grade | Top Issue |
|------|-------|-------|-----------|
| Technical SEO | X/10 | A-F | {one-liner} |
| Structured Data | X/10 | A-F | {one-liner} |
| E-E-A-T | X/10 | A-F | {one-liner} |
| AEO | X/10 | A-F | {one-liner} |
| GEO | X/10 | A-F | {one-liner} |
| Architecture | X/10 or SKIPPED | A-F | {one-liner} |

**Overall: X/60 (X/50 if Architecture skipped) — Grade: {letter}**

Grade scale: A (50-60) | B (40-49) | C (30-39) | D (20-29) | F (<20)

---

### Critical Issues (fix before publishing)
{severity-tiered findings}

### High Issues (fix within 1 week)
{findings}

### Medium Issues (address in next content update)
{findings}

### Low / Recommended Monitoring
{findings}

---

### Quick Wins (high impact, low effort — fix in under 30 minutes)
1. {item}
2. {item}
3. {item}
```

Update pipeline tracker with final scores, then present report to user.

---

## Scope Shortcuts

| Scope | Stages run |
|-------|-----------|
| `full` | All 7 stages |
| `technical-only` | Stage 1 + 2 + 7 |
| `content-only` | Stage 3 + 4 + 5 + 7 |
| `geo-only` | Stage 5 + 7 |

---

## Integration with pipeline-content

When called from `/pipeline-content` as Stage 4b (optional deep SEO audit after content-critique passes):
- Runs `content-only` scope by default (stages 3-5 + 7)
- The audit supplements content-critique's dimension 5 score with itemized findings
- If composite content score < 30/50: flag as blocker, recommend specific fixes before publishing
