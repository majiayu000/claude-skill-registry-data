---
name: employee-diff-scope
description: "Approve the employee-diff working set and comparison rules for reconciling the old employee PDF table with the current Excel rows before the final diff report is written."
---

# Employee-Diff Working Set and Comparison Rules

Use this stage to freeze the employee-diff working set and the comparison rules before any row-by-row diff is produced. The goal is to keep the PDF-as-older and Excel-as-newer interpretation fixed, avoid duplicate rescans, and leave a reviewable scope record for the next stage.

## Inputs

Read:

- `workflow/employee_diff/intake_checkpoint.json`
- `workflow/employee_diff/continuation_gate.json`

Use those records plus the task-visible files they point to. Treat `/root/employees_backup.pdf` as the original employee table and `/root/employees_current.xlsx` as the current employee table. Carry that old-versus-new interpretation forward exactly, and do not write `/root/diff_report.json` in this stage.

## Write the Working-Set Record

Write `workflow/employee_diff/working_set_record.json` with exactly these keys:

```json
{
  "selected_candidates": [],
  "non_selected_candidates": [],
  "comparison_fields": [],
  "pending_continuation_status": "pending_continuation",
  "primary_artifact_path": "/root/diff_report.json"
}
```

Requirements:

- `selected_candidates` must list the files that are actually needed for the employee diff workflow. Keep the PDF backup and the current Excel workbook in the selected set. Include only files the next stage should continue from.
- `non_selected_candidates` must be present even when empty. Use it for paths or notes reviewed but not needed for the direct employee diff.
- `comparison_fields` must contain every shared employee field that should be compared after matching on the employee ID key. Exclude the ID key itself. Preserve one canonical header form so the next stage does not have to re-normalize field names. This includes text fields plus `Salary`, `Years`, and `Score` when present in both sources. Do not include output-only keys such as `deleted_employees` or `modified_employees`.
- `pending_continuation_status` must show that the working set is approved but not yet executed.
- `primary_artifact_path` must remain `/root/diff_report.json`.

## Write the Scope Summary

Write `workflow/employee_diff/scope_summary.json` with exactly these keys:

```json
{
  "pdf_role": "",
  "excel_role": "",
  "id_key": "",
  "numeric_fields": [],
  "sorting_rule": ""
}
```

Requirements:

- `pdf_role` must record that the PDF is the older/original employee table source.
- `excel_role` must record that the Excel file is the newer/current employee table source.
- `id_key` must be the shared employee identifier column used to align rows across both sources. Reuse the exact key already established in the checkpoint if it is present; otherwise record the shared header or token that holds values like `EMP00002`. Treat its values as strings so the identifier format is preserved exactly.
- `numeric_fields` must preserve the numeric comparison fields required by the task. Use the canonical task order `["Salary", "Years", "Score"]` for fields that are present in both sources.
- `sorting_rule` must state that both `deleted_employees` and `modified_employees` are sorted by employee ID in ascending order for the final JSON output.

## Approval Checks

Before ending this stage, verify:

- selected and non-selected candidates are explicitly separated
- the employee ID key is fixed once for both sources and treated as a string identifier
- numeric fields stay marked for numeric output downstream
- the working set remains pending continuation
- `/root/diff_report.json` has not been written yet

## Continuation

Stop after both workflow files are written. The next stage should be able to read `selected_candidates`, `non_selected_candidates`, `comparison_fields`, `pending_continuation_status`, `primary_artifact_path`, `id_key`, `numeric_fields`, and `sorting_rule` directly from these two records without reopening scope decisions.
