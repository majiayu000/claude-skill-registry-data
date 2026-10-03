---
name: engineering-validation
description: Validate English engineering manuscript readiness before claiming edits are complete. Use when the user asks to check a paper, compile LaTeX, inspect references, page count, citations, figure/table consistency, claim-evidence anchors, final-paper synchronization, submission checklist, or whether a conference/journal manuscript is safe to submit. This is readiness validation, not certification that experiments, citations, or claims are true unless the relevant sources and checks were actually provided and inspected.
---

# Engineering Validation

Use this skill before saying a paper edit is complete, fixed, or ready.

## Core Stance

- No verification, no completion claim.
- A dry read is not a build check.
- Report exactly what was run and what was not run.
- Treat evidence anchors, citations, figures, tables, and PDF output as part of
  manuscript correctness.
- For existing paper repos, read the current live draft and project-specific
  instructions before validating.
- This is readiness validation, not truth certification. Never certify
  experiment truth, citation truth, or venue compliance without the relevant
  source files, tools, and checks.

## Boundaries

- Use this skill for readiness checks, not for drafting new manuscript prose.
- Use `engineering-writing` when the user needs new section structure or
  claim-evidence planning before validation.
- Use `engineering-polishing` for prose-only improvements.
- Use `engineering-figure-table` for visual design before final consistency
  checks.
- Use `engineering-response` for reviewer/advisor reply drafting before final
  response package validation.

## Status Vocabulary

- `PASS`: checked directly and no issue found.
- `FAIL`: checked directly and an issue was found.
- `PARTIAL`: checked only in part; name the unchecked part.
- `NOT_RUN`: check was relevant but not run.
- `UNKNOWN`: cannot determine from provided material.

Overall readiness can only be `READY`, `NOT_READY`, or `CANNOT_DETERMINE`.

`READY` is allowed only when every required check for the user's stated goal is
`PASS`. If any required check is `FAIL`, `PARTIAL`, `NOT_RUN`, or `UNKNOWN`,
overall readiness must be `NOT_READY` or `CANNOT_DETERMINE`.

## When to Open Extra Files

| File | Open when |
|---|---|
| [references/live-draft-check.md](references/live-draft-check.md) | Confirming source draft, input order, title, author/blind state, or final sync |
| [references/latex-build.md](references/latex-build.md) | Compiling LaTeX, checking bibitem count, page count, warnings, or diff checks |
| [references/evidence-audit.md](references/evidence-audit.md) | Checking contributions, claims, section anchors, citations, and overclaims |
| [references/final-readonly-check.md](references/final-readonly-check.md) | Running the final 30-minute style read-only inspection |
| [references/error-archive.md](references/error-archive.md) | Diagnosing common manuscript failure symptoms and the first section to inspect |
| [references/submission-checklist.md](references/submission-checklist.md) | Final read-only inspection before submission |
| [references/venue-checklist.md](references/venue-checklist.md) | Venue family changes limits, reproducibility, checklist, or AI-disclosure requirements |
| [references/citation-metadata-check.md](references/citation-metadata-check.md) | Citation existence, DOI, venue, year, or BibTeX consistency needs verification |
| [references/ai-disclosure-check.md](references/ai-disclosure-check.md) | AI-assisted writing, citation, or figure generation may require author verification or disclosure |
| [references/examples.md](references/examples.md) | Needing concrete validation report examples |
| [references/failure-modes.md](references/failure-modes.md) | Handling requests to certify readiness without running checks |
| [../_shared/story-spine.md](../_shared/story-spine.md) | Checking whether Abstract/Conclusion claims match Methods/Experiments evidence |
| [../_shared/evidence-boundary.md](../_shared/evidence-boundary.md) | Validation touches claims, citations, results, or completion status |
| [../_shared/citation-boundary.md](../_shared/citation-boundary.md) | Citation existence, citation placement, or reference claims are part of the check |
| [../_shared/citation-verification-workflow.md](../_shared/citation-verification-workflow.md) | Externally discovered references need existence, metadata, or claim-support verification before readiness |
| [../_shared/claim-strength.md](../_shared/claim-strength.md) | High-risk claim verbs need audit during validation |
| [../_shared/ai-assisted-writing-policy.md](../_shared/ai-assisted-writing-policy.md) | Venue disclosure or author-verification status is part of readiness |
| [../_shared/output-mode.md](../_shared/output-mode.md) | The user asks for a short validation result only |

## Workflow

1. State the validation goal being interpreted from the user request.
2. Identify manuscript root and live draft.
3. Read local instructions and relevant build files.
4. Check structure anchors: thesis, contribution list, main results, ablation,
   limitations.
5. Check story spine: Abstract and Conclusion claims must have Methods,
   Experiments, figure/table, and boundary anchors.
6. Check figures, tables, captions, labels, and category/metric names.
7. Run the smallest relevant build and consistency commands.
8. If tools or files are unavailable, mark command-dependent checks `NOT_RUN`
   and perform only the file-based or local-text audit that evidence allows.
9. For venue readiness, report whether official policy was checked, including
   source URL and source date. If not checked, venue compliance is `NOT_RUN` or
   `PARTIAL`. Static venue profiles count only as
   `STATIC_SUMMARY_NOT_LIVE_CHECK`, not as official policy verification.
10. Report evidence, failures, and unverified items.

## Default Output

```text
Validation result
- Goal interpreted as:
- Build: PASS / FAIL / NOT_RUN / UNKNOWN
- References: PASS / FAIL / PARTIAL / NOT_RUN / UNKNOWN
- Figures/tables: PASS / FAIL / PARTIAL / NOT_RUN / UNKNOWN
- Claim-evidence audit: PASS / FAIL / PARTIAL / NOT_RUN / UNKNOWN
- Story-spine audit: PASS / FAIL / PARTIAL / NOT_RUN / UNKNOWN
- AI/disclosure check: PASS / FAIL / PARTIAL / NOT_RUN / UNKNOWN
- Venue readiness: PASS / FAIL / PARTIAL / NOT_RUN / UNKNOWN
- Private/stale wording scan: PASS / FAIL / NOT_RUN / UNKNOWN
- Overall readiness: READY / NOT_READY / CANNOT_DETERMINE

Evidence
- Commands run:
- Files inspected:
- Outputs observed:
- Failures:
- Not verified:
- Official policy checked:
- Official policy source/date:
- Official page opened this run:
- Policy excerpt checked:
- Profile-only status:

Blocking issues
- ...

Next actions
- ...
```
