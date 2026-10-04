---
name: audit-on-page-seo
description: Use when auditing a webpage's on-page SEO factors to identify ranking gaps and technical issues
source: Google Search Essentials, Moz On-Page Ranking Factors Study, Google Core Web Vitals documentation
tags: [seo, on-page, audit, core-web-vitals, technical-seo, content-optimization]
verified: true
---

# Audit On-Page SEO

Systematically evaluate all on-page SEO factors for a given URL to surface ranking blockers and improvement opportunities.

## Why This Is Best Practice

**Adopted by:** Moz, Ahrefs, Semrush audit methodologies; Google Search Console recommendations
**Impact:** Moz's 2023 On-Page Ranking Factors study found content relevance and page experience signals account for over 40% of ranking variance

**Why best:** On-page audits catch issues invisible to casual review — thin content, duplicate tags, poor Core Web Vitals — that silently suppress rankings. Structured checklists prevent omission of any factor class. Regular audits track regressions after site changes.

## Steps

1. **Crawl the URL** — Use Screaming Frog or Ahrefs Site Audit to extract title, meta description, headings, canonical, and status codes in one pass.
2. **Audit title tag** — Verify primary keyword appears in first 60 characters; check for duplicates across site.
3. **Audit heading hierarchy** — Confirm single H1 containing target keyword; H2s cover topical subtopics; no skipped heading levels.
4. **Evaluate content depth** — Compare word count and topical coverage against top-5 SERP competitors; identify missing entities and subtopics.
5. **Check Core Web Vitals** — Run PageSpeed Insights for LCP (<2.5s), INP (<200ms), CLS (<0.1); flag failures as critical blockers.
6. **Audit internal linking** — Verify target page receives contextual links from relevant hub pages; anchor text is descriptive.
7. **Check structured data** — Validate Schema markup with Google's Rich Results Test; add missing applicable types (Article, FAQ, Product).
8. **Compile prioritized issue list** — Rank issues by estimated impact (critical / high / medium / low) and assign owners.

## Rules

- Always audit mobile and desktop separately — Core Web Vitals scores differ by device.
- Never ignore canonical tags; a misconfigured canonical silently splits link equity.
- Flag keyword stuffing (>3% density) as a risk, not an optimization.
- Treat a missing or duplicate title tag as a P0 issue — fix before content work.
- Do not conflate word count with quality; topical coverage matters more than length.

## Examples

A product page ranks #8 for "noise-cancelling headphones under $100." Audit reveals: title tag missing price qualifier, LCP of 4.1s on mobile, no FAQ schema despite competitors using it, and zero internal links from the blog. Fix order: LCP → title → internal links → schema. After fixes, page moves to #4 within 6 weeks.

## Common Mistakes

- Auditing desktop-only — mobile Core Web Vitals are the ranking signal, not desktop.
- Fixing meta tags without addressing content gaps — rankings require relevance, not just technical hygiene.
- Ignoring cannibalization — two pages targeting the same keyword split signals and suppress both.
- Running a one-time audit — on-page SEO degrades with CMS updates and content edits; schedule quarterly reviews.

## When NOT to Use

- Do not perform an on-page SEO audit on URLs that are intentionally noindexed (login pages, thank-you pages, internal tools) — these pages are excluded from search indexing and on-page optimization has no ranking effect.
- Do not use this audit process as the primary diagnostic for a site experiencing a sudden traffic drop — a manual penalty, algorithm update, or domain-level issue requires a site-wide audit and backlink analysis, not a page-level on-page review.
- Do not apply on-page SEO optimization to pages targeting informational keywords when the core problem is insufficient domain authority — technical hygiene cannot overcome a domain rating gap against established competitors in high-competition SERPs.
