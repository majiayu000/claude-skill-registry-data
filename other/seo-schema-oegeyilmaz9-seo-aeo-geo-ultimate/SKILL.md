---
name: seo-schema
description: Use when detecting, validating, planning, or generating truthful Schema.org markup tied to visible page content and current search-feature documentation; do not use it to promise rich results, AI citations, or rankings.
---

# Structured Data

## Purpose

Audit or draft structured data that accurately represents the visible page and verified entity facts. JSON-LD is a convenient implementation format, but format choice, schema validity, and rich-result eligibility are distinct questions.

Read `references/structured-data-review-protocol.md` before generating implementation code.

## Input gate

Require the rendered page or trusted page source, canonical URL, visible factual content, entity/offer/author/media facts, locale, and intended result or user purpose. For feature eligibility, check current primary search-engine documentation at the time of the work. Do not depend on a static “active/deprecated type” list.

If a fact is unknown—price, availability, rating source, author, date, image, address, certificate, or relationship—leave a clearly marked placeholder or decline the field. Never manufacture missing structured facts.

## Workflow

Let `<suite-root>` mean `${CLAUDE_PLUGIN_ROOT}` in Claude Code. In Codex, read `.seo-suite-runtime.json` beside this `SKILL.md` when present and use its `suite_root` value; otherwise use the absolute repository checkout. Before relying on a shipped platform feature state, run `python "<suite-root>/scripts/validate_platform_controls.py" validate-registry "<suite-root>/manifests/platform-controls.json" --bundle "<suite-root>/manifests" --as-of <current-UTC-time>`. Refresh primary documentation when the registry is stale or the feature is absent.

1. **Inventory.** Detect JSON-LD, Microdata, and RDFa; identify duplicate, conflicting, malformed, or disconnected entity graphs.
2. **Map visible truth.** For every proposed property, locate the reader-visible source or an approved authoritative data source. Confirm URLs, dates, locale, entity identity, and nesting match the page.
3. **Separate three checks.** Validate Schema.org vocabulary/syntax; validate platform-specific feature eligibility and lifecycle (`current`, `preview`, `deprecated`, or `removed`); then validate rendered visible-content alignment. Passing one is not proof of the others.
4. **Check lifecycle freshness.** Require a current Platform Controls registry row and primary documentation for the exact feature, market, locale, and surface.
5. **Draft the smallest truthful graph.** Prefer a coherent entity model over markup volume. Include only supported types/properties and use absolute, canonical URLs where appropriate. Do not add FAQ/HowTo/review/product/organization fields merely as an SEO tactic.
6. **Plan safe release.** State template/URL scope, owner, test environment, validation method, source-of-truth, rollout, and rollback. Route deployment through `seo-action-plan` when it changes production templates or data pipelines.
7. **Verify.** Re-render the page, parse the delivered markup, compare it against visible content, and run the relevant current validator. Record warnings and feature ineligibility honestly.

## Guardrails

- Structured data does not guarantee a rich result, AI citation, indexation, ranking, or traffic.
- Do not add “AI schema,” invisible facts, fabricated reviews, self-serving ratings, or non-existent offers.
- Do not convert a page’s hidden/internal data into public markup without authorization and privacy review.
- JavaScript-injected markup should be tested in the actual rendered output; critical metadata must not be assumed visible to a crawler merely because application code contains it.
- Current official docs outrank stale type lists, third-party generators, and historical rollout claims.

## Formal evidence handoff

When this work needs a cross-team, approval-ready plan, package evidence-bound findings as an immutable `seo-findings.json` bundle using the checked-out suite contract. Keep every referenced capture/source below `raw/`, retain declined claims and limitations, and run `python "<suite-root>/scripts/validate_seo_findings.py" validate-findings <bundle>/seo-findings.json --bundle <bundle>`. Send only a passing bundle to `seo-action-plan`; otherwise label the handoff `provisional`.

## Output

Return a detection/validation report, field-to-evidence mapping, precise implementation options, and optional JSON-LD snippet only when the required facts are supplied. Label placeholders and approvals. Include test/rollback steps and never present generated code as already deployed or feature-eligible.
