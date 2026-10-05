---
name: seo-audit
description: Use when a site needs a bounded multi-lane SEO assessment with explicit scope, evidence capture, findings, ownership, and limitations; coordinate specialists rather than produce a universal audit score or unverified implementation claim.
---

# Multi-lane SEO Audit

## Purpose

Plan and synthesize a site assessment across the lanes that matter for the stated goal. This skill does not assume that every site needs every check, crawl a site without authorization, fabricate a complete inventory, or implement the findings.

Read `references/audit-scope-protocol.md` before starting an audit.

## Scope first

Record objectives, domains/properties, representative URLs/templates, locales, environments, access/consent, data sources, time window, exclusions, and decision owners. Choose only relevant lanes: technical, page/content, structured data, media, sitemaps, hreflang, programmatic systems, competitive evidence, AEO/GEO, or measurement.

If an authorized crawler, analytics property, Search Console property, log source, or application access is unavailable, state the gap. Do not treat public snippets or third-party scores as a substitute for the inaccessible evidence.

## Workflow

1. **Design the evidence plan.** Define what capture/report proves each expected condition and which findings need current primary documentation.
2. **Run bounded lane assessments.** Route work to the relevant technical, page/content, schema, media, sitemap, international, programmatic, commerce, local, video, news/Discover, agentic, architecture, authority, conventional-performance, or AI-search specialist. Preserve their artifacts and disagreements.
3. **Classify findings.** Mark confirmed defects, supported opportunities, experiments, and unknowns separately. Do not convert incomplete sampling into site-wide certainty.
4. **Synthesize without false precision.** Prioritize by user/business risk, scope, reversibility, dependency, evidence confidence, and owner readiness—not by one blended SEO number.
5. **Plan delivery.** Send validated findings to `seo-action-plan` for owner/approval/verification/rollback, then use `seo-plan` for cross-team sequencing. Establish a baseline before change only when comparison is requested.

## Guardrails

- No universal SEO score, mandatory `llms.txt`, generic crawler policy, or ranking/citation guarantee.
- Do not count pages, links, words, or tests as proof of quality.
- Do not say a crawl, bot request, report row, or tool health check proves indexation, AI retrieval, citation, referral, or conversion.
- Keep security, privacy, accessibility, and legal risks visible even when they are not search-ranking claims.

## Formal evidence handoff

When this audit needs a cross-team, approval-ready plan, package evidence-bound findings as an immutable `seo-findings.json` bundle using the checked-out suite contract. Let `<suite-root>` mean `${CLAUDE_PLUGIN_ROOT}` in Claude Code. In Codex, read `.seo-suite-runtime.json` beside this `SKILL.md` when present and use its `suite_root` value; otherwise use the absolute repository checkout. Keep every referenced capture/source below `raw/`, retain declined claims and limitations, and run `python "<suite-root>/scripts/validate_seo_findings.py" validate-findings <bundle>/seo-findings.json --bundle <bundle>`. Send only a passing bundle to `seo-action-plan`; otherwise label the handoff `provisional`.

## Output

Produce a scoped audit charter, evidence inventory, lane findings, limitations, prioritized ownership map, and proposed next steps. Mark any implementation proposal as pending approval and link it to an action plan when a formal handoff is needed.
