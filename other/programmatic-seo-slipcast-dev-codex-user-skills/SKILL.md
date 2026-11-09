---
name: "programmatic-seo"
description: "How to design and run a programmatic SEO program that produces durable traffic instead of penalty-bait. Data source identification, template design, schema patterns, quality control at scale, internal linking architecture, crawl budget management, AEO/GEO for programmatic pages, refresh discipline, and the make-or-break question of whether pSEO is the right answer for your program at all. Triggers on programmatic SEO, pSEO, scaled content, page generation, template SEO, location pages, comparison pages, directory site, listing site, scaled landing pages, programmatic content. Also triggers when a content set is not ranking, has been hit by an algorithm update, or when a team is considering pSEO as a growth lever."
---

# Programmatic SEO

A senior SEO strategist's playbook for designing and running programmatic SEO programs that produce durable traffic instead of penalty-bait.

Programmatic SEO has a complicated reputation. Sites like Zillow, Airbnb, TripAdvisor, Indeed, and Yelp have built billion-dollar traffic engines on pSEO. Other sites have built pSEO programs that got hit by Google's helpful-content updates and lost 80% of their traffic in a week. The difference is rarely the technique; it is the underlying data quality and the quality control discipline at scale.

This skill is the playbook for getting that distinction right. It assumes you have decided what keyword space to target (see `seo-keyword`) and how the broader content program is shaped (see `content-strategy`). It does not write individual editorial pieces (see `content-and-copy` for that) and does not architect editorial topic hubs (see `pillar-content-architecture` for that). What it does is teach the discipline of generating high-volume pages programmatically from structured data sources without producing thin content, duplicate content, or scale-without-substance pages that get penalized.

When to use this skill: deciding whether pSEO is a fit for the program at all (the most important question), designing a new pSEO system, auditing an existing pSEO set that is not ranking or has been hit by an algorithm update, or building quality-control discipline for a pSEO program that grew faster than its quality processes.

---

## What this skill is for

This skill spans scaled-content programs from data source through quality control. It composes with five sister and adjacent skills, and the distinction between them is what keeps each one sharp.

- `content-strategy` is program-scope: editorial pillars, calendar, governance. Decides whether pSEO fits the program at all.
- `pillar-content-architecture` is hub-scope: one topic with 10 to 15 intentional editorial pieces. Editorial in nature.
- `content-brief-authoring` is per-piece scope: brief for one editorial artifact.
- `content-and-copy` is execution scope: writing individual editorial pieces.
- This skill is scaled scope: 100s to 100,000s of pages generated programmatically from structured data sources, each targeting a long-tail query.

The clean reading order: `content-strategy` decides whether pSEO is a fit, `seo-keyword` surfaces the long-tail keyword space, this skill designs the pSEO system, `editorial-qa` (forthcoming) provides the QA discipline for sampled quality control across the set. `content-and-copy` and `content-brief-authoring` are not in the loop for pSEO at scale; those skills are for editorial pieces, not data-driven generated pages.

The audience: SEO content strategists, content engineers, agencies running pSEO programs, in-house teams considering pSEO as a growth lever. The voice is senior SEO strategist to junior PM or marketer. Specific, opinionated, honest. The reputation problem is not pSEO; it is pSEO without underlying value.

---

## If required data is unavailable

This skill's output depends on data, measurements, or tool results it cannot generate on its own. When a required input, tool, or data source is unavailable or unverifiable, the sanctioned output is the deliverable with the gap stated: what was needed, what was actually obtained or verified, and which parts of the output are affected. Fabricating, estimating, or interpolating a required number to complete the deliverable is never sanctioned. A stated gap is a complete answer.

---

## Reference files

- [`references/when-pseo-works-decision.md`](references/when-pseo-works-decision.md) - Five-criterion decision framework with worked examples of yes, no, and maybe.
- [`references/data-source-identification-patterns.md`](references/data-source-identification-patterns.md) - First-party, licensed, public, expert-curated, synthesized; defensibility analysis.
- [`references/template-design-patterns.md`](references/template-design-patterns.md) - Variable density, above-the-fold answer, heading hierarchy, schema integration, link slots.
- [`references/schema-design-patterns.md`](references/schema-design-patterns.md) - Field count, computed fields, cross-record fields, update tags, schema-as-product.
- [`references/quality-control-at-scale.md`](references/quality-control-at-scale.md) - Sampling strategy, automated checks, manual review checklist, failure thresholds, cohort tracking.
- [`references/internal-linking-at-scale.md`](references/internal-linking-at-scale.md) - Hub-and-spoke, sibling linking, anchor text variation, orphan prevention.
- [`references/crawl-budget-management.md`](references/crawl-budget-management.md) - Sitemap segmentation, noindex patterns, canonicalization, crawl rate monitoring, pruning criteria.
- [`references/aeo-geo-for-programmatic-pages.md`](references/aeo-geo-for-programmatic-pages.md) - Direct-answer extraction, structured data signals, citation patterns, two-engine optimization.
- [`references/refresh-at-scale.md`](references/refresh-at-scale.md) - Data refresh cadence, template versioning, cohort migration, pruning lifecycle.
- [`references/common-pseo-failures.md`](references/common-pseo-failures.md) - Eleven-plus failure patterns with diagnoses and fixes.

---


## Conditional methods

Before applying a method below, read its linked section. For a narrow task select only relevant methods; for a full audit/design use the framework and relevant failure patterns. Existing references remain available for deeper details.

- When pSEO is the right answer: [method](references/domain-guide.md#when-pseo-is-the-right-answer).
- Data source identification: [method](references/domain-guide.md#data-source-identification).
- Template design: [method](references/domain-guide.md#template-design).
- Schema design: [method](references/domain-guide.md#schema-design).
- Quality control at scale: [method](references/domain-guide.md#quality-control-at-scale).
- Internal linking across the set: [method](references/domain-guide.md#internal-linking-across-the-set).
- Crawl budget management: [method](references/domain-guide.md#crawl-budget-management).
- AEO and GEO for programmatic pages: [method](references/domain-guide.md#aeo-and-geo-for-programmatic-pages).
- Refresh and maintenance at scale: [method](references/domain-guide.md#refresh-and-maintenance-at-scale).
- Common failure modes: [method](references/domain-guide.md#common-failure-modes).
- The framework: 12 considerations for programmatic SEO: [method](references/domain-guide.md#the-framework-12-considerations-for-programmatic-seo).
- Closing: quality at scale or not at all: [method](references/domain-guide.md#closing-quality-at-scale-or-not-at-all).
