---
name: frankus-geo-audits
description: "Run evidence-based GEO audits using Lili Frankus and duwerk's public approach to user questions, content architecture, brand consistency, external signals, and AI visibility. Use when diagnosing how AI systems categorize, mention, recommend, or cite a brand."
---

# Frankus GEO Audits

Based on Lili Frankus's public method. Not affiliated with or endorsed by Lili Frankus.

## When to use

Use this skill to investigate which customer questions a brand should answer, how generative systems currently describe it, and which content or ecosystem weaknesses deserve action. It suits marketing leaders, content and SEO teams, and B2B businesses with products that require explanation. It also supports a scoped audit for other sectors when relevant customer questions and trustworthy evidence exist.

Produce a reviewable GEO-Audit with a prompt map, observed answer evidence, technical and content findings, external signal gaps, a prioritized action plan, and repeat measurement. Keep discovery visibility, branded accuracy, citations, and commercial outcomes distinct. A mention alone does not establish a recommendation, a correct classification, or a source citation.

This package translates public material into an executable audit workflow. Read the attribution boundary in [references/method.md](references/method.md) before making claims about the method. The package's scoring formulas, evidence fields, and prioritization rules are implementation conventions, not a proprietary duwerk framework. Use the public source register to check attribution and access limitations.

## Procedure

1. **Define the audit decision.** Establish brand, category, audience, market, language, target AI surfaces, competitors, and the business decision the audit must support. Identify evidence already available and missing inputs. Use [references/method.md](references/method.md#1-scope-and-target-classification) and the scope fields in [templates/output-template.md](templates/output-template.md).

2. **Establish a defensible brand description.** Record what the business actually offers, whom it serves, limitations, and dated supporting facts. Compare the desired classification against owned and external descriptions. Follow [references/method.md](references/method.md#2-brand-entity-and-consistency); do not improve visibility by making unsupported claims.

3. **Build Top-Prompts from customer evidence.** Extract questions from search queries, sales, support, CRM, and relevant public communities. Map intent and context, working backward from Decision through Consideration to Awareness. Read [references/method.md](references/method.md#3-top-prompts-and-prompt-mapping) and label AI-generated ideas as unvalidated.

4. **Separate prompt cohorts.** Tag every prompt by journey stage, persona, location, and branded status. Keep brand-led questions out of non-branded discovery scores. Select a manageable, representative baseline and record the sampling limits using [references/method.md](references/method.md#3-top-prompts-and-prompt-mapping).

5. **Capture current answers and competitors.** Use available AI interfaces or tracking exports. Preserve exact prompts, timestamps, surface and mode, answers, source URLs, and brand observations. If live access is unavailable, produce a desk audit with an explicit evidence gap. Follow [references/method.md](references/method.md#4-repeatable-answer-observation).

6. **Diagnose the pattern.** Distinguish absence, wrong category, unsupported facts, weak citation presence, and competitor dominance. Link each finding to captured evidence; label suspected causes as hypotheses. Use [references/method.md](references/method.md#5-diagnosis-and-technical-foundations) and [examples/worked-examples.md](examples/worked-examples.md).

7. **Check technical foundations.** Inspect accessibility, indexing signals, HTML structure, navigation, redirects, and relevant crawler restrictions. Prioritize access failures before rewriting inaccessible pages. Follow [references/method.md](references/method.md#5-diagnosis-and-technical-foundations); technical readiness does not guarantee selection.

8. **Design content that can serve as a source.** Map priority questions to topic clusters, appropriate pages, and concise answer passages. Add verifiable evidence, dates, responsibility, examples, and useful constraints. Apply [references/method.md](references/method.md#6-content-architecture-and-zitierfaehigkeit), using the examples to distinguish substance from promotional language.

9. **Audit the ecosystem.** Compare brand facts across relevant profiles, listings, reviews, partner pages, editorial coverage, and communities. Choose channels from audience relevance and observed sources. Follow [references/method.md](references/method.md#7-external-signals-and-distribution); distinguish sponsored material from independent validation.

10. **Assign work and measure carefully.** Turn findings into bounded actions with owners, dependencies, effort, and verification criteria. Define Mentions, Citations, Visibility Score, and Visibility Share before reporting them. Use [references/method.md](references/method.md#8-prioritization-ownership-and-measurement) and [templates/output-template.md](templates/output-template.md).

11. **Review and schedule iteration.** Complete [checklists/review-checklist.md](checklists/review-checklist.md), deliver the filled template, and propose repeat checks. Compare unchanged cohorts over time, investigate answer quality, and connect leads where evidence permits. Follow [references/method.md](references/method.md#9-iteration-and-edge-cases); report uncertainty and avoid guaranteed outcomes.

## Files in this skill

- [SLUG.txt](SLUG.txt): Package identifier for naming and discovery.
- [SKILL.md](SKILL.md): Entry point, activation guidance, and audit procedure.
- [references/method.md](references/method.md): Principles, operational decisions, warnings, measurement definitions, and edge cases.
- [references/sources.md](references/sources.md): Numbered register of fetched public sources and their evidence limits.
- [examples/worked-examples.md](examples/worked-examples.md): Two invented audit illustrations with weak drafts, improvements, and rule explanations.
- [templates/output-template.md](templates/output-template.md): Deliverable template with instructions for every field.
- [checklists/review-checklist.md](checklists/review-checklist.md): Pass/fail acceptance checks and repairs for common failures.
