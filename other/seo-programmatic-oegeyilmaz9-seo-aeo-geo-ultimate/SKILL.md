---
name: seo-programmatic
description: Use when designing, auditing, or improving scaled/template-driven SEO pages, data-backed landing-page systems, or large URL inventories; require source data, usefulness, variation, indexing controls, and rollout safeguards rather than scale or keyword coverage targets.
---

# Programmatic SEO

## Purpose

Assess or plan scalable page systems without creating index bloat, misleading content, or unmaintainable templates. The unit of review is the page system: input data, template logic, user task, content differentiation, URL/canonical rules, quality controls, and rollout behavior.

Read `references/scaled-page-protocol.md` before approving a template or rollout.
Read [editorial-vs-indexability.md](references/editorial-vs-indexability.md) before deriving publication or search status from record fields.
Read [corpus-propagation-contract.md](references/corpus-propagation-contract.md) before changing a canonical, redirect, sitemap, discovery, locale, or whole-corpus rule.

## Input gate

Require the page-system purpose, target reader/task, data dictionary and provenance, source update cadence, template/rendered examples, locale/market rules, canonical/indexability policy, internal linking logic, quality owner, and proposed rollout. Do not infer product facts, locations, prices, availability, comparisons, or user demand from keyword lists alone.

## Workflow

1. **Model the user value and product decision.** Explain what distinct decision/task each page can satisfy, what evidence or data makes it different from nearby variants, and the explicit product-owner end state for the bounded corpus.
2. **Inspect inputs and template.** Verify data ownership, freshness, null/error handling, sourced claims, locale logic, entity identity, URLs, canonical behavior, structured data eligibility, and rendering.
3. **Sample for failure modes.** Review representative normal, sparse-data, conflicting-data, locale, outlier, and deprecation cases. Look for thin duplication, made-up combinations, contradictory claims, inaccessible values, or non-functional internal paths.
4. **Separate the two axes.** Record editorial readiness independently from search status/indexability. Never derive `noindex` from an editorial flag alone. A unique canonical-owner page follows the explicit indexing policy; an owner-linked duplicate source follows the approved redirect/canonical map. `noindex` requires explicit product policy or concrete risk evidence.
5. **Propagate the contract.** Apply the decision consistently across detail pages, search/browse results, hubs, discovery links, sitemap, hreflang, and an optional maintained `llms.txt`, plus feeds/schema/notifications when used. Verify a shared resolver or corpus rule over its full affected route class or a justified closed population.
6. **Define publication gates.** State required fields, minimum useful differentiation, source freshness policy, human/editorial exceptions, explicit index/noindex/redirect/withhold conditions, QA population, monitoring, and removal/rollback behavior. Do not use word counts or static “unique-content percentages” as the gate.
7. **Stage or apply the approved corpus decision.** Prefer an owned reversible cohort when the end state is undecided. When the product owner explicitly approves a whole-corpus end state, do not shrink it to a sample; retain canonical, duplicate, safety, legal, privacy, and access constraints. Route production implementation through `seo-action-plan`.

## Guardrails

- Do not publish pages for entities/locations/products that the source data cannot support.
- Do not mass-generate text, images, reviews, comparisons, schema, or local facts to simulate usefulness.
- Do not treat index coverage, crawl hits, or URL count as proof of user value or search performance.
- Keep data privacy, licensing, local/regulatory requirements, and deletion/update pathways in the design.

## Formal evidence handoff

When this work needs a cross-team, approval-ready plan, package evidence-bound findings as an immutable `seo-findings.json` bundle using the checked-out suite contract. Let `<suite-root>` mean `${CLAUDE_PLUGIN_ROOT}` in Claude Code. In Codex, read `.seo-suite-runtime.json` beside this `SKILL.md` when present and use its `suite_root` value; otherwise use the absolute repository checkout. Keep every referenced capture/source below `raw/`, retain declined claims and limitations, and run `python "<suite-root>/scripts/validate_seo_findings.py" validate-findings <bundle>/seo-findings.json --bundle <bundle>`. Send only a passing bundle to `seo-action-plan`; otherwise label the handoff `provisional`.

## Output

Return a system map, data/provenance gaps, editorial-readiness and search-status matrices, canonical/duplicate map, propagation surfaces, template findings, QA universe, publication gates, rollout/rollback plan, owners, and source-appropriate verification. Do not emit a programmatic SEO score or an ownerless blanket publish recommendation.
