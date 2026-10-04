---
name: insurance-waiver-pdf-scope
description: "Approve the exact insurance-waiver field edits, separate selected from non-selected candidates, and keep the PDF pending continuation."
---

# Insurance Waiver PDF Scope

## Approve the Exact Insurance-Waiver Field Edits

Approve the exact insurance-waiver field edits before packetization so downstream PDF work inherits one reviewable working set, one pending output target, and a clear separation between selected edits and excluded choices. This stage exists to standardize the approved working set, reduce duplicate scanning, and preserve later review traceability while the PDF remains unfinished.

## Insurance Waiver PDF Inputs

Read these inputs:

- `workflow/insurance_waiver_intake_checkpoint.json`
- `workflow/insurance_waiver_continuation_gate.json`
- `/root/input/input.txt`
- `tests/test_outputs.py`

Use the checkpoint and continuation gate as the canonical prerequisite records. Use `/root/input/input.txt` as the source of truth for field values and instructions. Use `tests/test_outputs.py` only as a verification-hint source for what the finished form must still expose; do not treat it as a replacement for the instruction text.

## Insurance Waiver PDF Outputs

Write these exact files:

- `workflow/insurance_waiver_working_set_record.json`
- `workflow/insurance_waiver_scope_summary.json`

Do not write or modify `/root/output/output.pdf` in this stage.

## Write the Insurance Waiver Working-Set Record

Create `workflow/insurance_waiver_working_set_record.json` with exactly these keys and values:

```json
{
  "selected_artifacts": {
    "source_pdf_path": "/root/input/input.pdf",
    "instruction_text_path": "/root/input/input.txt",
    "verification_hint_path": "tests/test_outputs.py"
  },
  "selected_field_updates": [
    {
      "field": "Student Name",
      "value": "Jinya Jiang"
    },
    {
      "field": "School Email",
      "value": "jiang@ucsd.edu"
    },
    {
      "field": "Date of Birth",
      "value": "2004/06/18"
    },
    {
      "field": "Phone",
      "value": "(253) 798-6666"
    },
    {
      "field": "Student ID",
      "value": "****5678",
      "mode": "true_redaction"
    },
    {
      "field": "Signature",
      "value": "Jinya Jiang"
    },
    {
      "field": "Date",
      "value": "2026/07/23"
    },
    {
      "field": "Appeal Reason",
      "value_lines": [
        "I have enrolled in a health insurance plan that meets all the waiver requirements outlined by the university.",
        "I will be graduating in the upcoming Spring 2026 quarter, and the coverage period I currently have is from Jan 2nd to June 30th, which aligns with the coverage dates listed on the university's official waiver guidelines."
      ]
    }
  ],
  "non_selected_candidates": [
    {
      "field": "Nickname",
      "value": "Yaya",
      "reason": "use the full name unless explicitly requested otherwise"
    },
    {
      "field": "Student ID plain text",
      "value": "A12345678",
      "reason": "the selected path is redaction with only the last four digits visible"
    },
    {
      "field": "Duplicate current PDF values",
      "reason": "do not add information again when the document already contains the correct value"
    }
  ],
  "pending_primary_artifact": "/root/output/output.pdf",
  "status": "pending_continuation"
}
```

Treat this working-set record as the only approved edit list for downstream packetization.

## Write the Insurance Waiver Scope Summary

Create `workflow/insurance_waiver_scope_summary.json` with exactly these keys and values:

```json
{
  "form_sections": [
    "student information",
    "appeal reason",
    "signature/date"
  ],
  "selected_vs_non_selected_record": "workflow/insurance_waiver_working_set_record.json",
  "next_skill_name": "insurance-waiver-pdf-binder"
}
```

## Output Contract

Before handoff, confirm all of the following:

- `selected_artifacts` contains exactly the source PDF, instruction text, and verification hint paths.
- `selected_field_updates` contains exactly eight field entries: `Student Name`, `School Email`, `Date of Birth`, `Phone`, `Student ID`, `Signature`, `Date`, and `Appeal Reason`.
- `non_selected_candidates` contains only the nickname, the plain student ID, and duplicate current PDF values as excluded candidates.
- `pending_primary_artifact` remains `/root/output/output.pdf`.
- `status` remains `pending_continuation`.
- `workflow/insurance_waiver_scope_summary.json` points to `workflow/insurance_waiver_working_set_record.json` and `insurance-waiver-pdf-binder`.

## Insurance Waiver Scope Rules

- Keep `selected_field_updates` and `non_selected_candidates` explicitly separate.
- Keep the full-name selection reviewable: `Jinya Jiang` is selected for name and signature, and `Yaya` remains excluded.
- Keep the student ID decision reviewable: only `****5678` may appear in the selected path, and the plain-text ID stays excluded.
- Reserve `non_selected_candidates` for rejected field-value options only; do not move task-local continuation context or later-stage operational notes into that list.
- Preserve the exact downstream keys the next stage consumes: `selected_artifacts`, `selected_field_updates`, `non_selected_candidates`, `pending_primary_artifact`, `status`, `form_sections`, `selected_vs_non_selected_record`, and `next_skill_name`.
- Leave the PDF pending continuation and untouched in this stage.

## Continuation Command

After both workflow files are written and checked, continue with `insurance-waiver-pdf-binder`.

## Stop Condition

Stop only when both workflow records exist with the exact required keys and values, the selected-versus-non-selected decisions are reviewable from those records alone, and `/root/output/output.pdf` has not been created or modified in this stage.
