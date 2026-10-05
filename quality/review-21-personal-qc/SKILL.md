---
name: review-21-personal-qc
description: Final personal quality-control audit for medical SCI reviews and translational manuscripts. Use before submission, major revision, or journal targeting to check evidence traceability, numeric/statistical consistency, conceptual overclaiming, figure/table source integrity, reporting statements, and target-journal fit using the user's distilled review-writing workflow.
---

# Review 21 Personal QC

## Purpose

Run the user's final "reviewer-before-reviewer" audit. This skill is stricter than ordinary polishing: it checks whether the manuscript can survive peer review on evidence, statistics, framing, reporting, and submission packaging.

## Audit Order

1. Identify manuscript type: narrative review, systematic review, meta-analysis, translational cohort, prediction model, or mixed evidence article.
2. Read the manuscript, evidence matrix, citation audit, journal target report, and any numeric/statistical verification files.
3. Build a risk ledger with `critical`, `major`, `moderate`, and `minor` issues.
4. Separate four domains: evidence truth, numeric consistency, conceptual framing, and journal readiness.
5. Recommend concrete edits, not generic advice.

## Personal Gates Distilled From Prior Work

- Meta-analysis gate: verify PMID/DOI, event counts, effect measure, heterogeneity, sensitivity analyses, absolute-risk translation, and PRISMA limitations.
- Translational manuscript gate: do not claim integration when molecular data and clinical cohort are parallel rather than patient-matched.
- Prediction-model gate: distinguish exploratory, internally validated, externally validated, and clinically deployable tools.
- Observational cohort gate: downgrade causal wording to association unless design supports causal inference.
- Outcome gate: rename study-defined outcomes precisely and justify thresholds.
- Figure gate: every panel needs source evidence, panel order, legend alignment, and permission/redraw status.
- Submission gate: verify declarations, ethics, funding, data availability, author contributions, target journal scope, and upload order.

## Output

Create or update `18_final_qc/personal_qc_report.md` with:

- Overall verdict: ready, minor revision, major revision, or not ready.
- Top 5 risks.
- Claim-to-evidence problems.
- Numeric/statistical problems.
- Framing and language changes.
- Missing reporting items.
- Journal-fit and submission-package gaps.
- Next revision checklist.

## Stop Rules

Do not invent missing data, references, ethics statements, funding, author contributions, or statistical outputs. Mark gaps explicitly and request user confirmation.
