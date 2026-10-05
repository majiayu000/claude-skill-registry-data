---
name: seo-content
description: Use when auditing, briefing, rewriting, or reviewing site content for a defined audience, page purpose, locale, and evidence set; produce human-reviewable content improvements without formulaic SEO or AI-citation guarantees.
---

# SEO Content

## Purpose

Create evidence-led content audits, briefs, and draft improvements that help a real reader complete a task. Use this after an approved `seo-action-plan` when the request stems from AEO/GEO findings; use it directly for a bounded editorial review with supplied content and facts.

Read `references/editorial-brief-protocol.md` before preparing a formal brief or draft.
Read [snippet-copy-protocol.md](references/snippet-copy-protocol.md) when title or meta-description copy is part of the deliverable.

## Input gate

Ask for or inspect the page/content capture, intended reader and decision/task, locale, page purpose, current factual sources, and any relevant approved action-plan item. Treat a missing fact, source, audience, or locale as an explicit limitation instead of filling it with plausible copy.

For regulated, health, legal, financial, safety, pricing, availability, or comparative claims, require an owner-approved source and human review. Do not use a search snippet, an AI answer, or a competitor page as proof of a claim.

## Workflow

1. **Frame the job.** Identify the reader’s task, search/referral context if known, page type, conversion or information goal, language/region, and what the page must not claim.
2. **Build a claim ledger.** Separate verified facts, interpretation, customer proof, quotations, and unknowns. Pin each factual claim to a supplied source or flag it for verification.
3. **Diagnose usefulness.** Review whether the page answers the actual task, makes ownership and scope clear, offers original evidence or experience where relevant, explains limitations, and is navigable on a small screen. Describe observations; do not assign an E-E-A-T, readability, word-count, or “AI readiness” score.
4. **Create the brief and query contract.** Define the answer/decision the reader needs, primary need/query family, natural supporting language, evidence to show, proposed hierarchy, necessary comparison/steps, entities, internal destinations that are known to exist, media/accessibility needs, locale constraints, CTA, and review owner. Choose headings and metadata for clarity, not fixed character, keyword-density, or passage-length formulas.
5. **Write complete search-result copy when requested.** Produce the actual unique title and meta-description candidate, not “improve metadata” as a placeholder. The description must identify the page, communicate the useful outcome, include a truthful differentiator or concrete page-specific detail, and retain any material qualifier. Rewrite descriptions that are generic, duplicated, fragmentary, or too short to explain why this result fits the query; do not pad them to hit a character count.
6. **Draft only within approved scope.** Supply rewrite options or an implementation-ready draft only from the claim ledger. Keep placeholders unmistakable. Preserve meaningful nuance; do not pad, paraphrase sources mechanically, or manufacture first-hand experience, reviews, citations, author credentials, data, or quotes.
7. **Set acceptance and verification.** Specify a human fact/brand/legal review, rendered-page review, title/meta uniqueness and source-data check, link check, accessibility check, and a source-appropriate measurement plan. A visible answer or structured layout may improve clarity; it does not guarantee ranking, retrieval, citation, traffic, or conversion.

## Content choices that need care

- Use direct answers where the reader asks a direct question, but retain conditions, dates, qualifications, and ownership of the fact.
- Make source attribution useful to readers; citations should support a real claim, not decorate a page or imitate an AI platform requirement.
- Prefer specific examples, methods, screenshots, original research, expert review, or transparent limits over generic “thought leadership.”
- Use internal links only to verified, useful destinations. Do not set link-count quotas or add irrelevant anchors.
- Treat title, H1, meta description, headings, lists, tables, alt text, and schema as reader-facing/technical choices with their own owners—not as universal ranking levers.
- Preserve locale meaning. A translation is not automatically a local-market page; request localized facts, legal wording, pricing/availability scope, and reviewer ownership where needed.

## AI-search and platform boundaries

Google’s current AI guidance treats standard, crawlable, people-first content as the foundation and does not require special AI markup, chunking, or `llms.txt`. Never add those as defaults. Do not claim that an answer-first section, FAQ, schema, or bot access will make a system cite a page. Route platform-specific research to `ai-search-research`, direct-answer audits to `seo-aeo`, citation/entity evidence to `seo-geo`, and repeatable observations to `ai-visibility-monitor`.

## Formal evidence handoff

When this work needs a cross-team, approval-ready plan, package evidence-bound findings as an immutable `seo-findings.json` bundle using the checked-out suite contract. Let `<suite-root>` mean `${CLAUDE_PLUGIN_ROOT}` in Claude Code. In Codex, read `.seo-suite-runtime.json` beside this `SKILL.md` when present and use its `suite_root` value; otherwise use the absolute repository checkout. Keep every referenced capture/source below `raw/`, retain declined claims and limitations, and run `python "<suite-root>/scripts/validate_seo_findings.py" validate-findings <bundle>/seo-findings.json --bundle <bundle>`. Send only a passing bundle to `seo-action-plan`; otherwise label the handoff `provisional`.

## Outputs

Return only the artifacts the evidence supports:

- **Editorial audit:** observations, evidence/limitations, prioritized opportunities, and unanswered questions.
- **Content brief:** reader task, claim ledger, outline, required evidence, locale/accessibility/CTA requirements, review gates, and acceptance criteria.
- **Draft/rewrite options:** clearly marked page copy plus complete title/meta candidates when in scope, with source notes and placeholders; never publish or represent it as approved.
- **Action handoff:** owner, dependencies, verification, rollback for potentially harmful edits, and the matching `seo-action-plan` action ID when one exists.

Do not output a universal content score, minimum word-count mandate, keyword-density target, rigid readability target, or guaranteed AI-citation result.
