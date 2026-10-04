---
name: citation-scope
description: "Review the BibTeX file for likely fake or hallucinated citations, separate selected and non-selected cleaned titles, and record an approved working set that remains pending continuation."
allowed-tools: "Read Write Edit Bash"
license: MIT
---

# Citation Scope Review

Use this stage after the intake checkpoint for the bibliography integrity check on `/root/test.bib`. The goal is to separate likely fake or hallucinated citation titles from non-candidates, freeze that split into an approved working set, and keep the result pending continuation. This standardizes the working set, reduces duplicate scanning, and preserves later review traceability without marking the task complete.

## BibTeX Inputs

- `workflow/intake_checkpoint.json`
- `workflow/continuation_gate.json`
- `/root/test.bib`

Read the checkpoint artifacts first to confirm the bibliography path, the answer target, and that the task is still in continuation rather than completion.

## Approved Working Set Outputs

Write:

- `workflow/approved_working_set.json`
- `workflow/scope_summary.json`

`workflow/approved_working_set.json` must contain these exact keys:

```json
{
  "selected_citations": ["cleaned title"],
  "non_selected_citations": ["cleaned title"],
  "pending_continuation": true,
  "scope_notes": "brief note explaining why the selected set remains pending continuation"
}
```

`workflow/scope_summary.json` should be a compact companion record such as:

```json
{
  "selected_count": 0,
  "non_selected_count": 0,
  "pending_continuation": true,
  "scope_notes": "same working-set decision in summary form"
}
```

Rules:

- `selected_citations` holds cleaned titles for entries that should continue as likely fake or hallucinated citations.
- `non_selected_citations` holds cleaned titles reviewed in this pass that should not continue.
- Store titles, not BibTeX keys.
- Clean titles by removing BibTeX braces and escape backslashes, then normalize whitespace.
- Sort both title arrays alphabetically for stable handoff.
- Keep `pending_continuation` set to `true`.
- Do not write `/root/answer.json` in this stage.

## Review and Separate Citation Scope

1. Read `workflow/intake_checkpoint.json` and `workflow/continuation_gate.json` to confirm the current task scope and output expectations.
2. Parse `/root/test.bib` entry by entry and extract one cleaned title per citation.
3. Select titles for `selected_citations` only when the current review indicates they are likely fake or hallucinated citations that should continue to the next stage.
4. Place every other reviewed title in `non_selected_citations` so the approved working set stays explicit and disjoint.
5. Use `scope_notes` to record the high-level selection basis and to state that the approved working set remains pending continuation. Preserve only the task-local context needed for later bounded route discovery by keeping the checkpoint artifacts and `/root/test.bib` available; if the checkpoint references any task-local operational note, keep it outside the citation arrays rather than discarding it.
6. Write both workflow records and stop.

## Output Contract

- Every cleaned title reviewed from `/root/test.bib` must appear in exactly one of `selected_citations` or `non_selected_citations`.
- `workflow/approved_working_set.json` is the current working record for later stages.
- This stage prevents over-inclusion or omission before later continuation.
- This stage does not finalize the fake citation list and does not complete the bibliography integrity check.

## Continuation Command

```bash
jq '{selected_citations, non_selected_citations, pending_continuation, scope_notes}' workflow/approved_working_set.json
```

## Stop Condition

Stop when `workflow/approved_working_set.json` exists with the exact keys `selected_citations`, `non_selected_citations`, `pending_continuation`, and `scope_notes`, `pending_continuation` is `true`, and `workflow/scope_summary.json` reflects the same working-set decision without claiming that the bibliography task is complete.
