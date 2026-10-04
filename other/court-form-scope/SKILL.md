---
name: court-form-scope
description: "Approve the exact working set for the SC-100 fill, separating selected form inputs and verification sources from non-selected material so downstream PDF work stays minimal and reviewable."
---

# Approve the SC-100 Working Set

Use this stage after the intake checkpoint to approve the exact SC-100 working set for the California Small Claims Court fill. Standardize the approved field set, reduce duplicate scanning of `/root/sc100-blank.pdf` and `tests/test_outputs.py`, and keep the selected set pending continuation rather than treating the task as complete.

The prerequisite workflow records freeze the case facts. Use the blank form and verifier file only to confirm which form areas and verification sources belong in scope for the fill.

## Inputs

Read these inputs before writing scope records:

- `workflow/court_form_intake_checkpoint.json`
- `workflow/court_form_continuation_gate.json`
- `/root/sc100-blank.pdf`
- `tests/test_outputs.py`

## Write the Scope Records

Write exactly these two files.

### `workflow/court_form_working_set.json`

```json
{
  "selected_candidates": {
    "primary_artifact": "/root/sc100-blank.pdf",
    "target_artifact": "/root/sc100-filled.pdf",
    "required_case_fields": [
      "claimant identity and contact",
      "defendant identity and contact",
      "claim amount",
      "claim basis text",
      "incident date range",
      "venue basis",
      "filing date",
      "first-time small-claims indicator if present on form"
    ],
    "verification_sources": [
      "tests/test_outputs.py"
    ]
  },
  "non_selected_candidates": [
    "court-filled sections",
    "optional fields not mentioned in case description",
    "blank PDF regions unrelated to stated facts"
  ],
  "status": "approved_for_pending_continuation"
}
```

### `workflow/court_form_scope_summary.json`

```json
{
  "current_record": "workflow/court_form_working_set.json",
  "next_stage": "court-form-binder",
  "reason": "Standardize the approved field set and preserve later review and traceability before packetization."
}
```

## Scope Rules

- Keep `selected_candidates` and `non_selected_candidates` explicitly separated.
- Preserve the exact key names and string values shown above.
- Keep the working set in `approved_for_pending_continuation` status.
- Leave court-filled sections, optional fields not mentioned in the case description, and unrelated blank-form regions out of the selected set.
- Do not place any later route record into `non_selected_candidates`.
- Do not write `/root/sc100-filled.pdf` in this stage.

## Handoff

The next stage reads these exact keys from `workflow/court_form_working_set.json`:

- `selected_candidates.primary_artifact`
- `selected_candidates.target_artifact`
- `selected_candidates.required_case_fields`
- `selected_candidates.verification_sources`
- `non_selected_candidates`
- `status`

## Stop Condition

Stop when both scope records exist, the approved working set is pending continuation, and no PDF output has been created or modified in this stage.
