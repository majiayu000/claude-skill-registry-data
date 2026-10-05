---
name: review-15-main-body-writer
description: Draft thematic main-body sections for a medical review. Use when synthesizing mechanisms, clinical evidence, omics findings, methods, or therapeutic implications across studies.
---

# Review 15 Main Body Writer

## Purpose

Write synthesis, not paper-by-paper summaries.

## Required Inputs

- Manuscript outline.
- Evidence matrix.
- Deep-reading notes.
- Figure/table plan.
- Literature master table with DOI/PMID status for core references.
- Target journal or a documented journal-level constraint.

## Output

Create section files in the project's `03_正文撰写_框架填充` folder, or use the folder required by the target journal, with:

- Topic sentence.
- Evidence synthesis.
- Comparison across studies.
- Limitations of evidence.
- Link to figure/table if needed.
- Citation keys.

## Drafting Rules

1. Start each section with a synthesis statement that answers the section question; do not open with a study-by-study catalogue.
2. Link every substantive sentence to `direct_evidence`, `synthesis_from_multiple_sources`, `background_only`, or `author_interpretation` in the evidence matrix.
3. Keep findings, interpretation, and clinical implication distinct. Do not convert an association, prognostic signal, or biological rationale into a treatment recommendation.
4. Use numerical results, effect estimates, diagnostic performance, and mechanistic details only when the cited full text supports them. An abstract-only record cannot support a central claim, figure, or table value.
5. Where studies conflict, state the source of heterogeneity when known; otherwise describe the inconsistency without forcing a conclusion.
6. Treat author proposals as proposals. Use conditional wording such as “may”, “could”, or “requires prospective validation” when action validation is absent.
7. Draft in short, specific sentences. Remove generic transitions, promotional adjectives, and repetitive end-of-section summaries.

## Paragraph Template

For each paragraph, record internally:

- Claim: the limited statement the paragraph can defend.
- Evidence: cited studies and the evidence status.
- Boundary: population, setting, design, or uncertainty that limits the claim.
- Link: whether the paragraph supplies a figure/table source or a transition to the next decision question.

Do not expose this template as manuscript prose. It is an audit aid.

## Completion Gate

Pass only when every section:

- distinguishes observed findings, interpretation, and unresolved questions;
- has claim-to-citation traceability in the evidence matrix;
- contains no uncited quantitative or clinical-action claim;
- uses citations in first-appearance order compatible with the manuscript reference system; and
- has been checked against related figures and tables for consistent terminology, numbers, and conclusions.

## Stop Rules

Do not draft formal manuscript text when the evidence matrix, core-reference metadata, or full-text status is missing. In that situation, return only the missing-evidence list and the next retrieval or verification action.

Do not report invented statistics, sample sizes, pathways, clinical recommendations, DOI, PMID, or bibliographic details.
