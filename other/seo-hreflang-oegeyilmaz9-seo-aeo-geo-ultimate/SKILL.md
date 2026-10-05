---
name: seo-hreflang
description: Use when auditing or planning language-region targeting, hreflang clusters, localized URL mappings, canonical alignment, or x-default behavior from an explicit locale and URL inventory; provide safe implementation guidance without inventing translations or markets.
---

# International SEO and hreflang

## Purpose

Validate reciprocal locale clusters and plan language/region targeting that reflects actual localized pages. This skill does not translate content, create markets, change canonicals, or deploy annotations.

Read `references/locale-cluster-protocol.md` before generating a repair plan.

## Input gate

Require a URL-to-locale inventory, declared language/region intent, canonical URLs, current annotations or sitemap/header data, page accessibility, and ownership of each localized variant. Do not infer a locale from a URL slug, browser language, or translated sample alone.

## Workflow

1. **Model the cluster.** Name the page purpose/entity, canonical URL for each actual locale variant, language/region code, content status, and optional x-default intent.
2. **Validate the graph.** Check self-reference, reciprocal links, canonical alignment, absolute/crawlable destination URLs, code syntax, redirects, indexability intent, and parity of the cluster. Record inaccessible URLs as limitations rather than guessing their markup.
3. **Inspect reader fit.** Verify that the destination truly serves the declared language/market and does not silently force a different locale, price, legal regime, or product availability.
4. **Propose bounded repairs.** State the exact source/destination pair, annotation delivery method, owner, test URLs, approval, verification, and rollback. Avoid mass templates until a representative cluster passes.
5. **Verify after change.** Re-crawl all cluster members, compare reciprocal annotations and canonicals, and monitor the relevant platform reports as observations—not guarantees.

## Rules

- Use current official documentation for supported annotation methods and syntax; do not rely on copied country-code lists or stale error folklore.
- `x-default` is purposeful fallback behavior, not a required decoration.
- A hreflang annotation cannot make an untranslated page appropriate for a market, override legal/product availability, or guarantee geographic ranking.
- Do not use `hreflang` to solve duplicate, canonical, or automatic-redirect problems without examining those systems separately.
- Large cluster changes, canonical changes, redirects, and locale gating require an approved `seo-action-plan` with rollback.

## Formal evidence handoff

When this work needs a cross-team, approval-ready plan, package evidence-bound findings as an immutable `seo-findings.json` bundle using the checked-out suite contract. Let `<suite-root>` mean `${CLAUDE_PLUGIN_ROOT}` in Claude Code. In Codex, read `.seo-suite-runtime.json` beside this `SKILL.md` when present and use its `suite_root` value; otherwise use the absolute repository checkout. Keep every referenced capture/source below `raw/`, retain declined claims and limitations, and run `python "<suite-root>/scripts/validate_seo_findings.py" validate-findings <bundle>/seo-findings.json --bundle <bundle>`. Send only a passing bundle to `seo-action-plan`; otherwise label the handoff `provisional`.

## Output

Return a cluster inventory, confirmed mismatches, unresolved access/data gaps, exact repair map, approval/owner, validation steps, and rollback. Use a pass/warn/fail status per check if useful, but never a single international-SEO score.
