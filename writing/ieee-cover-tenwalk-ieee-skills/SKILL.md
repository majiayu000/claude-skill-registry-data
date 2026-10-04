---
name: ieee-cover
description: >-
  Draft IEEE journal cover letters and editor-facing significance statements for new submissions
  or resubmissions to JSAC, TWC, TCOM, WCL, CL, and related IEEE venues. Use this when the user
  asks for a "cover letter", "submission letter", "letter to the editor", "significance statement",
  "special issue fit", "投稿信", "cover letter怎么写", or wants to frame novelty, scope, ethics,
  suggested reviewers, conflicts, or manuscript fit. For point-by-point reviewer replies use
  ieee-response; for rewriting manuscript sections use ieee-writing or ieee-polishing.
---

# IEEE Cover Letter and Significance Framing

Use this skill to write the editor-facing letter that accompanies an IEEE submission. The cover
letter should help the editor see fit, novelty, evidence, and compliance quickly; it is not a second
abstract and not a reviewer response.

## Core stance

- **Editor first.** State why the manuscript belongs in the target journal or special issue, what
  the technical contribution is, and why the evidence is sufficient.
- **Specific beats promotional.** Use concrete contribution/evidence language; avoid "highly
  novel", "breakthrough", and unsupported impact claims.
- **Do not over-disclose reviewer-response detail.** For a revision, summarize the main changes and
  point to the response letter; do not replay every comment.
- **Compliance matters.** Include originality, non-duplication, conflicts, ethics/data/code
  statements, and suggested/opposed reviewers only when the journal asks or the user supplies them.
- **No fabricated names or claims.** Never invent editor names, reviewer names, manuscript IDs,
  funding statements, conflicts, or data availability.

## When to open extra files

| File | Open when |
|---|---|
| [references/cover-letter-template.md](references/cover-letter-template.md) | Drafting a new-submission or revised-submission cover letter |
| [references/significance-framing.md](references/significance-framing.md) | Writing the significance/fit paragraph for JSAC/TWC/TCOM/WCL/CL, special issues, or interdisciplinary framing |

For target-journal routing, also use `ieee-writing`'s `journal-fit.md` when needed. For reviewer
responses use `ieee-response`.

## Intake

- target journal or special issue;
- manuscript title and paper type;
- one-sentence contribution;
- 2-4 evidence points: theorem/proof, algorithm, simulation, testbed, dataset, or measured result;
- status: new submission, revision, transfer, or resubmission after rejection;
- manuscript ID, editor name, suggested reviewers/conflicts, and required declarations if available.

If target, title, contribution, or evidence is missing, draft with placeholders and list the missing
items.

## Workflow

1. **Write a fit sentence:** target journal/special issue + technical scope + why the paper belongs.
2. **State the contribution plainly:** one paragraph, no hype, no citations unless the journal
   expects them.
3. **Tie evidence to claims:** theorem/proof/simulation/testbed/complexity and the target-specific
   reason it is enough.
4. **For revisions, summarize changes:** new experiments, clarified assumptions, softened claims,
   added comparisons, improved figures.
5. **Add compliance paragraph:** originality, exclusive submission, conflicts, data/code/ethics,
   reviewer suggestions only from supplied facts.
6. **Close briefly** and keep the letter usually under one page.

## Output format

1. `Cover letter:` copy-pasteable editor-facing letter.
2. `Significance / fit note:` 3-5 bullets explaining why the framing matches the target journal.
3. `Compliance checklist:` required statements and whether the user supplied them.
4. `Missing inputs:` exact editor name, manuscript ID, reviewer names, declarations, or evidence.
