---
name: seo-competitor-pages
description: Use when researching, briefing, or drafting fair comparison, versus, or alternative pages using dated, attributable product evidence; avoid unsupported superiority claims, copied competitor content, and artificial SEO comparisons.
---

# Comparison and Alternative Pages

## Purpose

Create useful comparison-page plans and reviewable drafts for a reader making a real choice. The page should make its evidence, scope, and trade-offs clear; it is not a vehicle for unverified claims or competitor disparagement.

Read `references/comparison-evidence-protocol.md` before drafting factual comparisons.

## Input gate

Require the reader/use case, entities/products compared, locale, comparison date, company-owned facts, independently verifiable competitor sources, the user’s actual alternatives/criteria, legal/brand constraints, and review owner. Quote or summarize only what the cited source supports and preserve price, availability, plan, market, and feature scope.

If a competitor fact cannot be verified or may have changed, label it unknown, omit it, or ask for an approved source. Never “complete” a table from memory or an AI answer.

## Workflow

1. **Frame reader value.** State who is deciding, what decision they need to make, and why a comparison is useful beyond a brand-versus-brand keyword.
2. **Build a fact matrix.** Separate company facts, competitor facts, common capabilities, meaningful differences, limitations, and subjective fit. Every material row gets a source and “as of” date/scope.
3. **Choose fair structure.** Use methodology, use-case guidance, eligibility/constraints, and transparent comparison rows. Include alternatives that may genuinely fit the reader; do not hide disqualifying conditions.
4. **Draft with attribution.** Write factual copy in neutral language, preserve product/brand names correctly, cite sources where readers need them, and distinguish opinion from verified fact. Do not copy a competitor’s copy, table, screenshots, reviews, or trademarks beyond authorized/legally reviewed use.
5. **Review and release plan.** Require product, legal/brand, factual, localization, and accessibility review as appropriate. Send site implementation through `seo-content` and `seo-action-plan`.

## Guardrails

- Do not claim “best,” “cheaper,” “more secure,” “#1,” migration ease, feature parity, or performance superiority without scoped support and approval.
- Never fabricate rankings, review aggregates, customer quotes, pricing, availability, integrations, or competitor weaknesses.
- Do not use SEO demand as permission to create a misleading or thin comparison page.
- Do not imply search ranking, AI citation, referral, or conversion outcomes from publishing the page.

## Formal evidence handoff

When this work needs a cross-team, approval-ready plan, package evidence-bound findings as an immutable `seo-findings.json` bundle using the checked-out suite contract. Let `<suite-root>` mean `${CLAUDE_PLUGIN_ROOT}` in Claude Code. In Codex, read `.seo-suite-runtime.json` beside this `SKILL.md` when present and use its `suite_root` value; otherwise use the absolute repository checkout. Keep every referenced capture/source below `raw/`, retain declined claims and limitations, and run `python "<suite-root>/scripts/validate_seo_findings.py" validate-findings <bundle>/seo-findings.json --bundle <bundle>`. Send only a passing bundle to `seo-action-plan`; otherwise label the handoff `provisional`.

## Output

Return a source/date-stamped fact matrix, reader-oriented outline, claim/approval ledger, draft options if requested, and implementation/review handoff. Unverified rows are explicit gaps, not recommendations.
