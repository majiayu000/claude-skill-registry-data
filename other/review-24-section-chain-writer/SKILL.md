---
name: review-24-section-chain-writer
description: Drive a medical review manuscript through a stepwise writing chain from title and abstract to introduction, body sections, discussion, conclusion, figures, tables, and final audit. Use when the user says next step, generate abstract, generate introduction, continue the review, write the next section, or wants a Codex-driven SCI review workflow with evidence checkpoints between sections.
---

# Review 24 Section Chain Writer

## Overview

Use this skill as the manuscript state machine. It decides the next writing step, calls the right local review skill, and prevents the manuscript from advancing when evidence, references, figures, or logic are not ready.

For Chinese users, respond in Chinese unless the manuscript section itself must be drafted in English.

## Position In The Workbench

- Use `review-01` and `review-02` to lock topic, question, scope, and target journal.
- Use `review-23-reference-curator` before drafting evidence-heavy sections.
- Use `review-14`, `review-15`, and `review-16` for introduction, main body, discussion, and conclusion drafting.
- Use `review-25-zotero-pdf-pipeline` when citations require full-text reading or Zotero evidence.
- Use `review-26-figure-table-factory` when a section requires figures, tables, graphical abstract, SVG, BioRender, Figma, or Excel outputs.
- Use `review-17-citation-audit` and `review-21-personal-qc` before submission.

## Section State Machine

Advance in this order unless the user explicitly changes the target:

1. `Topic lock`: disease, population/model, key mechanism or clinical question, review type, target journal.
2. `Title options`: 5-10 candidate titles with scope, novelty angle, and risk.
3. `Narrative spine`: background, gap, question, purpose, main viewpoint, expected figures/tables.
4. `Abstract`: structured or journal-style abstract, with no unsupported claims.
5. `Introduction`: funnel logic from broad field to gap to review purpose.
6. `Body outline`: 3-6 major sections with claim map and citation needs.
7. `Main body sections`: write one section at a time, each with claim-citation mapping.
8. `Discussion and conclusion`: synthesize, evaluate controversies, limitations, and future directions.
9. `Figures and tables`: plan, generate, source-check, and caption.
10. `Reference audit`: numbering, DOI/PMID, claim matching, source quality.
11. `Submission package`: target journal formatting and final QC.

## Gate Before Next Step

Do not move to the next section until the current step has:

- A clear scientific purpose.
- Key claims labeled as supported, citation needed, or opinion/viewpoint.
- No invented references, data, mechanisms, or statistics.
- No causal wording based only on association evidence.
- A note of what still needs literature support.
- A saved or clearly named output artifact when working inside a project folder.

If evidence is missing, pause section generation and call `review-23-reference-curator` or `review-25-zotero-pdf-pipeline`.

## Writing Rules By Section

### Abstract

- Write after title and narrative spine are clear.
- Use `background/objective-methods-content-conclusion` logic for narrative reviews.
- Avoid numeric claims unless already verified.
- End with the review's specific contribution, not a broad slogan.

### Introduction

- Use funnel structure: disease or field burden, recent development, unresolved gap, why the gap matters, review objective.
- Cite key claims close to where they appear.
- Do not preview every body section mechanically.

### Main Body

- Each subsection should follow `claim -> evidence -> interpretation -> boundary`.
- Separate what is known, what is debated, and what the review argues.
- For mechanisms, distinguish validated mechanism, plausible mechanism, and hypothesis.
- For clinical content, separate guideline-level evidence, trial evidence, observational evidence, and expert opinion.

### Discussion And Conclusion

- Synthesize across sections rather than repeat them.
- State limitations of the literature and limitations of the review.
- Give concrete future directions, not generic calls for more research.

## Standard Output

When advancing a manuscript, return:

1. Current stage.
2. Readiness check.
3. Draft or revision for the current section.
4. Citation needs or reference tasks.
5. Figure/table needs.
6. Next step and required inputs.

## Reference File

Read `references/section-gates.md` when deciding whether a manuscript can move from abstract to introduction, from introduction to body, or from body to figures and final audit.
