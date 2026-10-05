---
name: seo-sitemap
description: Use when auditing, generating, or planning XML sitemap changes from a verified canonical URL inventory, discovery evidence, and current protocol guidance; do not promise crawling or indexing from sitemap inclusion.
---

# XML Sitemaps

## Purpose

Compare sitemap files with the URLs a site actually intends to expose, then produce safe inventory, generation, or cleanup recommendations. A sitemap is a discovery hint; it neither forces crawling nor guarantees indexation.

Read `references/sitemap-inventory-protocol.md` before creating or changing a sitemap.

## Input gate

Require the current sitemap/index files, expected canonical/indexable URL inventory, preferred host/protocol, robots/sitemap discovery context, relevant locale rules, and source of truth for update time. Do not generate a sitemap from an unfiltered crawler export or an unverified CMS list.

## Workflow

1. **Parse and retain evidence.** Record sitemap URL, fetch time/status, declared locations, syntax errors, and any nested sitemap references.
2. **Compare with intent.** Check whether each listed URL is expected to be canonical, accessible, indexable, stable, and within the declared locale/host policy. Separately identify important intended URLs that are absent.
3. **Classify mismatches.** Distinguish sitemap hygiene, canonical/indexability conflict, stale inventory, locale mapping, server delivery, and unresolved access issues.
4. **Generate only from verified inventory.** Use current official protocol/engine documentation for limits and fields. Include `lastmod` only when it is a truthful, reliable content-change timestamp. Do not fill optional fields with invented values.
5. **Release safely.** State source system, affected sitemap/index, rollout, test URL, validation, monitoring, and rollback. Coordinate locale URLs with `seo-hreflang` and technical delivery with `seo-technical`.

## Guardrails

- Do not list redirecting, error, duplicate, blocked, noindex, session, staging, faceted, or unapproved URLs merely to increase coverage.
- Do not submit every URL variant, use sitemap timestamps as a freshness hack, or assume sitemap acceptance proves indexing.
- Keep user-facing availability, crawlability, canonicalization, and actual indexed state as separate measurements.
- For large/sensitive changes, create an approved `seo-action-plan`; this skill only prepares the change and validation path.

## Formal evidence handoff

When this work needs a cross-team, approval-ready plan, package evidence-bound findings as an immutable `seo-findings.json` bundle using the checked-out suite contract. Let `<suite-root>` mean `${CLAUDE_PLUGIN_ROOT}` in Claude Code. In Codex, read `.seo-suite-runtime.json` beside this `SKILL.md` when present and use its `suite_root` value; otherwise use the absolute repository checkout. Keep every referenced capture/source below `raw/`, retain declined claims and limitations, and run `python "<suite-root>/scripts/validate_seo_findings.py" validate-findings <bundle>/seo-findings.json --bundle <bundle>`. Send only a passing bundle to `seo-action-plan`; otherwise label the handoff `provisional`.

## Output

Return the verified inventory comparison, sitemap defects/opportunities, source-of-truth assumptions, a generated XML proposal when authorized, and test/rollback instructions. Never output a sitemap “score” or an indexing guarantee.
