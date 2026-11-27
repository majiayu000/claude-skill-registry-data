---
name: document-writing
description: Write or revise Document Studio Korean/Japanese copy for reading reports, approvals, proposals, operations guides, research briefs, existing templates and live speaker scripts. Use for document-specific writing, captions, genre voice, evidence fidelity and page consistency.
---

# Final-language document writing

For newly laid-out documents, use the [accepted guide baseline](../report-html-pptx/references/accepted-composition-default.md) for substantive native copy connected to images/diagrams; follow the selected reading or presentation form. Rich visual composition does not reduce the body to slogans or erase conditions.

## Match the writing to its use

For an explicitly opted-in [Editorial Consulting session](../report-html-pptx/references/editorial-consulting-mode.md), the assistant **leads adaptive co-writing** after the author has selected a strategy/early visual direction. Spend effort on the canonical final-language argument and whole-document coherence; offer a sourced Consultant Challenge only for a consequential countercase, weak claim, meaningful structural alternative or pivotal section. Routine copy work proceeds without line-by-line approval. Accepted exploratory visual geometry never dictates the manuscript. Record actual author decisions and revised source/section IDs; a later author objection reopens affected editorial work and invalidates stale manuscript acceptance. Only an explicitly accepted manuscript is handed to the ordinary final Design → Export flow, whose production-intake and real QA gates remain unchanged.

Select the document function and accepted format before choosing structure or voice:
- **Formal reading report**: complete findings, reasoning, figures/captions, status and qualifications in coherent paragraphs with concrete nominal headings.
- **Approval/decision copy**: state the requested approval or decision, recommendation/options, criteria, exceptions and responsible follow-up concisely. Preserve any required form labels and sign-off fields.
- **Persuasive proposal or implementation plan**: explain a supported business case, feasible actions, owners, schedule, constraints, costs/risks and assumptions; use message headings only where appropriate.
- **Operational guide/SOP**: write direct, reproducible task steps, inputs, outputs, examples, checkpoints, exceptions and escalation contacts; prioritize scanning and accurate instructions over rhetoric.
- **Analytical/research brief**: define scope, methodology and terms before findings; attach limitations and data definitions to each consequential conclusion.
- **Existing template/form**: fill or revise prescribed fields in their original sequence, status and register; do not rearrange them to create a story.
- **Live lecture/presentation**: use a **speakable script** and essential on-screen copy, with transitions and teaching moments. Do not impose the DEMO ESG report voice or noun-only titles on speech.

**No forced story beats** for formal reports, approval forms, checklists, operations guides or fixed templates. Preserve official names, claims, quantitative conditions and business caution in every genre. Refer to [document-family page contracts](../report-html-pptx/references/editorial-story-research.md) only when the work actually needs substantive page restructuring.

For speaker manuscripts, keep one canonical slide ID per page with: on-screen core message, full spoken words in natural target language, important source/qualification notes, transition to the next page, intended audience understanding, estimated speaking/demo/visual time and a visual/motion explanation brief when useful. Demonstrations include necessary setup, fallback if they fail and a non-misleading simulated-data label. Separate speech from production instructions, so cues are not read aloud. Estimate times from real script length and actions; reconcile section totals and allocate rehearsal buffer. Label timing as estimate until a timed read-through occurs.

For live/persuasive material, treat each page as an argumentative unit: spoken claim must be supported by the same page's evidence or a clearly connected earlier source; examples should illuminate a mechanism, not replace proof. For reading reports, forms and guides, instead inspect required sections/fields, information findability, evidence adjacency and instruction correctness. Revise the affected page and adjacent transitions when a new fact changes the storyline. Apply [editorial development](../report-html-pptx/references/editorial-story-research.md) for narrative/script QA, and send the finalized source-linked visual job to Design/Open Design only when visual production is requested.

Reuse the current brief, page map, evidence and accepted copy, including documented working assumptions. Pending required choices allow unaffected notes/source review; final-language copy waits for the relevant decision. Write directly in the final language; no mandatory Korean draft for Japanese output, duplicate manuscript or separate humanizing stage.

For Korean formal reading material, use DEMO ESG's formal body voice (~합니다 / ~하고 있습니다 / ~하였습니다) with concise noun headings. Explain actual context/purpose, operation, evidence/current state and warranted interpretation or next action in connected paragraphs; this is not a fixed sentence quota. Make subjects, responsibilities and relationships concrete. Split overloaded sentences at real changes in role while retaining the logic.

Distinguish completed/ongoing activity, proposal, goal, forecast and expected effect. Preserve names, quantities, units, period, scope, exceptions, responsibilities and uncertainty. Do not strengthen causality or commitments to make the copy memorable. Reading pages retain sufficient explanation beside evidence; live pages select essentials and keep necessary detail in notes or a reading appendix.

For a new Korean formal report voice, retrieve a few full paragraph/function models with scripts/find_writing_reference.py --function process --section excerpts --limit 2, choosing the actual function. Query the library rather than loading its 368 pages. Reuse selected models. Read [DEMO writing](references/demo-esg-writing.md), [long form](references/demo-esg-korean-longform.md), [patterns](references/demo-esg-writing-patterns.md) or company profiles only for a current unresolved issue; company commitments never become Document Studio commitments.

When a Company Pack is selected, **replace** the DEMO writing lookup with `scripts/find_writing_reference.py --company-pack PACK --language LANG --document-family FAMILY --writing-function FUNCTION`. Do not mix the built-in DEMO examples into that company's style evidence. Each reference must retain `source_ids`, `origin_pack`, `confidence` when available, and `observed` versus `suggested` status. If no match exists, use general writing principles and flag the style as unverified; never manufacture an official company voice. Do not automatically call optional Korean/Japanese translation skills when absent from the installed skill inventory.

Use [Japanese translation/register](../business-japanese-translation/SKILL.md) when that optional skill is installed and the task needs Japanese terminology/register; use [Korean translation](../business-korean-translation/SKILL.md) under the same condition for its target issue. Do not load both automatically. If unavailable, use general writing guidance and mark specialist review as unverified. Consequential bilingual work applies [translation quality](../report-html-pptx/references/translation-quality.md) and reconciles common terms, numbers and responsibilities.

Apply [expression](../report-html-pptx/references/design-expression.md) to concrete titles and truthful captions. For [creative bodies](../report-html-pptx/references/body-composition.md), write substantive scene-level and local-subject paragraphs that design can associate with the corresponding image. Generated concepts and same-source detail crops have accurate status. Keep decision conditions instead of replacing prose with slogans.

Before design, apply the relevant checks in [Korean copy quality](references/korean-copy-quality.md) to all new/changed Korean copy, headings, prompts, tables and notes. Review subjects/predicates, transitions, concrete wording and spacing consistently; retain the formal DEMO voice and all facts/conditions. This is part of writing, not an optional external skill or a separate approval. Allowed spelling variants are style choices, not automatic errors.

Apply [semantic line breaks](references/semantic-linebreaks.md) after writing and before composition. For Korean guides/prompts, begin a fresh visual line when instructions turn into follow-up action, constraints, retained conditions or a separate output request. Keep same-function prose continuous and evaluate every affected multi-sentence block. This proactive reading-unit pass is required even with zero wrapping warnings; do not wait for overflow.

Keep one canonical copy; typography-specific line breaks stay in HTML, not the manuscript. Review support, register, transitions and caption/figure agreement together. After composition review actual Korean [line flow](references/demo-esg-korean-lineflow.md) and [rendered text](../report-html-pptx/references/text-flow-and-wrapping.md), or Japanese kinsoku: particles, number-unit pairs, parentheses, predicate tails, titles and notes. Repair affected language/geometry without shrinking everything. [Content review](../report-html-pptx/references/consulting-content-review.md) is one editorial check, not another approval round.

Return changed copy/label IDs, checked scope and unresolved source/argument issues to their owners. Accepted unaffected text remains reusable; font, copy, width or export changes reopen the affected checks.

## Report headings and varied body progression

Apply [report heading style](../report-html-pptx/references/report-heading-style.md) to formal reading-report page titles and subheads: concrete noun phrases for reading reports, full explanatory sentences in the body. Avoid Korean/Japanese sentence-ending subheads unless message headlines or original wording were explicitly selected. Rewrite the meaning instead of chopping endings and retain proposal/forecast/verification status. Check all headings, table of contents and final exported headings.

Use [expression and rhythm](../report-html-pptx/references/visual-expression-and-rhythm.md) to vary the actual narrative job across body pages. Consistent terms/register do not require the same background→list→expected-effect story each time. Write the relevant mechanism, evidence interpretation, case, comparison, judgment or execution conditions, with substantive captions that design can connect to real images/visualizations. Do not invent results to support a striking image or title.
