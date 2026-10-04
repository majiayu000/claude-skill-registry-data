---
name: seo-optimizer
description: Audit and improve ethical technical, on-page, content, local, ecommerce, and structured-data SEO for websites or supplied HTML. Use for evidence-backed prioritization and verification; never promise rankings or use spam, deception, or manipulative link schemes.
---

# SEO Optimizer

Improve search visibility by fixing discoverability and usefulness problems that can be demonstrated from the site, its analytics, or authoritative search documentation. Treat ranking position as an observed outcome, not a guarantee.

## Workflow

1. Scope the property, target audience, locations, languages, business goals, templates, and available evidence. Separate a local HTML audit from claims about live indexing or ranking.
2. Inspect crawlability and indexability: status codes, robots directives, XML sitemaps, canonical URLs, redirects, duplicate routes, mobile rendering, and page speed evidence. Do not override an intentional noindex or canonical without confirming intent.
3. Audit on-page usefulness: search intent, title, meta description, one clear H1, headings, topical coverage, internal links, image alt text, clear calls to action, and visible authorship/trust information where relevant.
4. Check structured data against the page content and the appropriate schema vocabulary. Flag invalid, misleading, or unsupported markup instead of adding markup solely to chase rich results.
5. For local or ecommerce work, verify consistent business facts, location/service pages, product availability, price/currency, reviews, breadcrumbs, and category-to-product internal linking. Keep claims and offers truthful.
6. Use `scripts/audit_html.py` for a deterministic first pass over local HTML, then classify findings as confirmed, needs-live verification, or recommendation. Prioritize by expected impact, confidence, effort, and risk.
7. Implement only the requested changes. Re-run the audit, compare the diff, and record what still needs Search Console, analytics, crawler, or production verification.

Read [audit-checklist.md](references/audit-checklist.md) for the evidence and prioritization checklist. The HTML helper is dependency-free and intentionally reports signals; it is not a substitute for a live crawl or ranking measurement.

## Boundaries

- Never guarantee first-page placement, traffic, indexing, or a particular time to rank.
- Do not recommend keyword stuffing, doorway pages, cloaking, hidden text, fake reviews, purchased manipulative links, or automated spam.
- Do not claim a live result from static HTML. Label assumptions and request the missing evidence when it matters.
