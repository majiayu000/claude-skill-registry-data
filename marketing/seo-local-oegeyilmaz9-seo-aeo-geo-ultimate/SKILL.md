---
name: seo-local
description: Use when auditing or planning local search visibility for a storefront, service-area business, practitioner, or multi-location brand across Google Business Profile, Bing Places, NAP/hours/categories, location pages, LocalBusiness data, reviews, duplicates, service areas, and location-aware query evidence; require authorized profile data and never promise map rankings, calls, visits, or revenue.
---

# Local SEO

Audit the relationship between real-world business facts, authorized platform profiles, location pages, structured data, reviews, and location-aware query demand.

Read [local-evidence-protocol.md](references/local-evidence-protocol.md) before a formal audit.

## Procedure

1. Define business model, eligible locations/practitioners, service areas, markets/locales, official entity names, profile owners, and customer tasks.
2. Capture authorized Google Business Profile/Bing Places data when available, official business records, representative location pages, LocalBusiness markup, citations, and review-policy evidence.
3. Reconcile name, address, phone, website, hours, special hours, categories, services, areas served, coordinates, booking/order links, and status across first-party and platform surfaces.
4. Build or consume a Query Corpus with locale, country/location, device, intent, current/target URL, and source. Separate local intent from a generic keyword and keep demand unavailable when no evidence exists.
5. Inspect location-page uniqueness, crawlability, internal discovery, canonical/hreflang behavior, accessibility, conversion task completion, and truthful business/entity support.
6. Identify duplicate, moved, closed, practitioner, department, review, category, or policy risks. Do not merge or suspend profiles without an authorized owner and current platform guidance.
7. Route structured data to `seo-schema`, page/content to `seo-content`, technical/index issues to `seo-technical`, task flows to `seo-agentic`, and measurement to `seo-performance`.
8. Package formal findings as SEO Findings `1.1.0` with `business_profile`, `web_page`, or `locale_cluster` targets and `local`, `entity`, `content`, `technical`, or `policy` categories.

## Guardrails

Never fabricate an address, service area, category, review, rating, practitioner relationship, opening status, or profile access. Do not create doorway location pages or promise Local Pack placement.

## Formal evidence handoff

Package only supported observations as SEO Findings `1.1.0`. Let `<suite-root>` mean `${CLAUDE_PLUGIN_ROOT}` in Claude Code. In Codex, read `.seo-suite-runtime.json` beside this `SKILL.md` when present and use its `suite_root` value; otherwise use the absolute repository checkout, then run `python "<suite-root>/scripts/validate_seo_findings.py" validate-findings <bundle>/seo-findings.json --bundle <bundle>`. Keep the handoff provisional until this command passes.

## Output

Return the location/entity inventory, profile-page-schema parity, query/location map, duplicates and policy risks, prioritized owners, verification, rollback, and evidence gaps—without a local visibility score.
