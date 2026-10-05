---
name: seo-research
description: Use when researching conventional search intent, audience questions, query families, content gaps, site coverage, cannibalization, or competitor/page evidence for a bounded SEO decision; produce a provenance-aware query corpus when the work will drive measurement or implementation, retain source dates and uncertainty, and route formal multi-engine AI-search evidence to ai-search-research.
---

# SEO Research

## Purpose

Build a decision-ready research note for traditional/web-search content and site decisions. This skill is for scoped discovery, not for a fabricated keyword spreadsheet, mass scraping, or a substitute for the immutable multi-engine `ai-search-research` Research Pack.

Read `references/research-evidence-protocol.md` before presenting research conclusions.
Read [query-opportunity-protocol.md](references/query-opportunity-protocol.md) when the goal is to choose what the site should rank for or identify the strongest next query opportunity.

## Input gate

Clarify audience, market/locale, decision to be made, known site/entity URLs, time horizon, access/permissions, and available first-party data. Decide whether the question is conventional search research or AI-search research:

- Use `ai-search-research` for engine/surface-specific AI evidence, ground truth, citations, or formal Research Pack provenance.
- Use this skill for content/search intent, page inventory, query language, competitor/page observations, and source-backed opportunity framing without that formal contract.

## Workflow

1. **Define the decision.** State the audience task, market/locale, entity/page scope, non-goals, and evidence required to decide.
2. **Build a query/question corpus.** Separate user needs, observed search queries, AI prompts, and engine-executed subqueries. Group language by task and stage, not just lexical similarity. Preserve parent families, source, date, locale, country/location, device, engine/surface, conversation turn, coverage, confidence, and limitations. Hash-pin local source and coverage evidence. Treat volume/difficulty/vendor metrics as dated estimates, never ground truth.
3. **Inspect existing coverage and performance.** Map actual pages/assets to the questions they serve. When authorized first-party data exists, preserve query, page, country, device, search type, time window, clicks, impressions, CTR, and average position together; identify head-term/category leadership, near-win visibility, snippet/CTR, coverage-gap, defend, and cannibalization candidates without treating average position as an exact rank. Absence from first-party rows does not remove an owner-mandated high-volume family; retain it with the demand/SERP evidence and record the visibility gap.
4. **Inspect the current result set.** For candidate query families, record a dated locale/device SERP observation: dominant intent, result/page types, visible title/snippet patterns, strong competitor evidence, freshness, authority expectations, and features that change the reader task. A SERP snapshot is evidence for fit, not a stable ranking formula.
5. **Select page-level query ownership.** Choose one primary need/query family and natural supporting language per target page. Preserve owner-named strategic queries, business value, achievable page fit, existing authority, coverage state, and evidence gaps. The highest-volume phrase is not automatically the best short-term opportunity, but every owner-declared relevant high-volume family and the market's highest-relevant-demand family must receive an explicit head-term leadership decision. Difficulty changes the route; it does not erase the ambition.
6. **Research external evidence responsibly.** Use primary docs, authoritative sources, and accessible pages. Capture title, URL, access date, source type, claim, and limitations. Respect robots, terms, rate limits, paywalls, authentication, and copyright.
7. **Synthesize choices.** Return a two-track opportunity slate: nearer-term capture/defense work and high-volume head-term/category leadership. Use `now`, `next`, and `later` to sequence both tracks without allowing easy work to replace the leadership target. Use `defer` for a documented owner decision, genuine intent/product mismatch, or prohibited/misleading target—not merely high difficulty, weak authority, cost, or current absence. Separate observed facts, inferred opportunities, experiments, and unknowns; do not collapse unlike dimensions into a universal keyword score.
8. **Freeze formal query work.** Let `<suite-root>` mean `${CLAUDE_PLUGIN_ROOT}` in Claude Code. In Codex, read `.seo-suite-runtime.json` beside this `SKILL.md` when present and use its `suite_root` value; otherwise use the absolute repository checkout. When the corpus will drive a baseline, audit, page map, or implementation decision, create `query-corpus.json` using the checked-out suite contract and validate it with `python "<suite-root>/scripts/validate_query_corpus.py" validate-corpus <bundle>/query-corpus.json --bundle <bundle>`.
9. **Hand off.** Send conventional performance measurement to `seo-performance`, page search-result review to `seo-page`, content work to `seo-content`, competitor pages to `seo-competitor-pages`, implementation sequencing to `seo-action-plan`, and AI-specific formal work to `ai-search-research`.

## Guardrails

- Do not present a snapshot of results, snippets, third-party tool data, or AI answers as stable truth.
- Do not scrape protected sources, bypass controls, or reproduce copyrighted source text beyond what is needed to substantiate a finding.
- Do not promise rankings, traffic, citations, or business outcomes.
- Do not convert keyword volume, page count, or competitor activity into a universal opportunity score.

## Formal evidence handoff

When this work needs a cross-team, approval-ready plan, package evidence-bound findings as an immutable `seo-findings.json` bundle using the checked-out suite contract. Keep every referenced capture/source below `raw/`, retain declined claims and limitations, and run `python "<suite-root>/scripts/validate_seo_findings.py" validate-findings <bundle>/seo-findings.json --bundle <bundle>`. Send only a passing bundle to `seo-action-plan`; otherwise label the handoff `provisional`.

## Output

Return a decision statement, validated query corpus when required, source register, existing-coverage and query-to-page map, current first-party performance where available, dated SERP intent review, the mandatory head-term leadership track, nearer-term opportunity track, selected primary/supporting query families, leading-result gap map, staged work and measurement milestones, observation/inference split, declined ideas, owners, and evidence gaps. Include collection dates and a refresh trigger for volatile sources.
