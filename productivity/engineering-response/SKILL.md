---
name: engineering-response
description: Draft, audit, or revise English response letters and revision plans for engineering papers from advisor, senior-author, reviewer, or editor comments. Use when the user provides comments, decision letters, rebuttal notes, revision drafts, or asks how to respond, what to revise, how to classify comments, how to avoid over-editing, or how to map each comment to manuscript changes.
---

# Engineering Response

Use this skill to turn comments into traceable revision tasks and professional
English responses.

## Core Stance

- Preserve each comment before responding.
- Answer every concern or mark it as unresolved.
- Map responses to manuscript evidence, a revision location, or explicit author
  input needed.
- Do not invent experiments, line numbers, figures, citations, analyses, or
  manuscript changes.
- Prefer concise, evidence-linked responses over defensive explanations.
- When a comment reveals misunderstanding, first check whether the manuscript
  caused it.

## Boundaries

- Use this skill for comment triage, revision planning, rebuttal drafts, and
  response letters.
- Use `engineering-writing` for manuscript section drafting after a comment has
  been turned into a concrete edit.
- Use `engineering-polishing` for prose-only improvements.
- Use `engineering-figure-table` for caption, figure, or table revisions.
- Use `engineering-validation` before claiming a response package is complete or
  before using final line numbers.

## When to Open Extra Files

| File | Open when |
|---|---|
| [references/comment-routing.md](references/comment-routing.md) | Classifying advisor/reviewer comments and deciding which section to edit first |
| [references/revision-tracker.md](references/revision-tracker.md) | Turning comments into concrete edit tasks with acceptance evidence |
| [references/comment-resolution-worksheet.md](references/comment-resolution-worksheet.md) | Building a full comment-to-action worksheet before editing |
| [references/response-letter.md](references/response-letter.md) | Drafting point-by-point English responses |
| [references/comment-examples.md](references/comment-examples.md) | Handling common comments about experiments, methods, claims, captions, related work, conclusions, or abstract |
| [references/tone-and-risk.md](references/tone-and-risk.md) | Handling disagreement, impossible requests, missing experiments, or high-risk claims |
| [references/contradictory-reviewer-strategy.md](references/contradictory-reviewer-strategy.md) | Reviewers ask for conflicting detail, compression, experiments, or framing |
| [references/partial-compliance-response.md](references/partial-compliance-response.md) | Authors can only partially satisfy a reviewer request |
| [references/rebuttal-vs-revision-mode.md](references/rebuttal-vs-revision-mode.md) | Deciding whether the output is rebuttal, revision response, or camera-ready note |
| [references/diff-verification.md](references/diff-verification.md) | A response says a manuscript change, line number, experiment, figure, or table has already been added |
| [references/examples.md](references/examples.md) | Needing concrete response tracker and reply examples |
| [references/failure-modes.md](references/failure-modes.md) | Handling false completed-change claims or impossible reviewer requests |
| [../_shared/evidence-boundary.md](../_shared/evidence-boundary.md) | A response may claim unsupported experiments, citations, or edits |
| [../_shared/citation-boundary.md](../_shared/citation-boundary.md) | A response mentions added or corrected references |
| [../_shared/citation-verification-workflow.md](../_shared/citation-verification-workflow.md) | A response relies on externally discovered references that have not passed a verification gate |
| [../_shared/claim-strength.md](../_shared/claim-strength.md) | A response or manuscript change needs claim downgrading |
| [../_shared/list-to-argument.md](../_shared/list-to-argument.md) | A comment batch arrives as an unordered list |
| [../_shared/output-mode.md](../_shared/output-mode.md) | The user asks for response text only |
| [../_shared/terminology-ledger.md](../_shared/terminology-ledger.md) | A comment asks for renaming methods, metrics, or categories |

## Workflow

1. Split editor/advisor/reviewer comments into stable IDs.
2. Classify each comment by type, severity, section, and missing input.
3. Identify the real complaint, not just the surface wording.
4. Choose `revise`, `defer with reason`, or `no change with reason`.
5. Define prohibited over-edit.
6. Define acceptance evidence and minimum verification.
7. Decide whether the mode is rebuttal, revision response, camera-ready note,
   or internal revision plan.
8. If the response claims completed changes, run the diff-verification gate.
9. Draft the response only after the change or placeholder is clear.
   If the change is planned but not done, draft a plan or author-input note,
   not a final completed-change response.
10. Run completeness and factuality checks before calling the package ready.

## Default Output

```text
Response strategy summary
- Package status:
- Main risks:
- Response mode:
- Validation needed before final response:

Comment-response tracker
| ID | Original comment | Type | Severity | Real complaint | First target | Second target | Action | Evidence/change needed | Prohibited over-edit | Acceptance evidence | Verification | Line-number status | Status |

Allowed status values: `Done with evidence`, `Planned`,
`Needs author input`, `Defer with reason`, `No change with reason`, and
`Not supported`.

Draft response
[English point-by-point response]

Unverified items
- line numbers:
- experiments:
- citations:
- figures/tables:

Revision checklist
- ...
```
