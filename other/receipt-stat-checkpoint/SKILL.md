---
name: receipt-stat-checkpoint
description: "Receipt OCR intake checkpoint for the sorted JPG receipt set and stat_ocr.xlsx workbook contract."
---

# Receipt OCR Intake Checkpoint

## Purpose
Freeze the sorted JPG receipt set and the `stat_ocr.xlsx` workbook contract before any OCR pass. This stage creates the canonical intake record that later receipt OCR stages must cite directly instead of rebuilding the source inventory from scratch.

## Inputs
- Source directory: `/app/workspace/dataset/img`
- Output workbook: `/app/workspace/stat_ocr.xlsx`
- Verifier contract: `tests/test_outputs.py`

## Write
- `workflow/receipt_intake_checkpoint.json`
- `workflow/receipt_continuation_gate.json`

## Procedure
1. Create `workflow/` if it does not already exist.
2. Read the task prompt and `tests/test_outputs.py` only to confirm the workbook contract: one sheet named `results`, header `filename`, `date`, `total_amount`, rows ordered by filename, and blank cells when a field cannot be extracted.
3. Enumerate only `.jpg` files under `/app/workspace/dataset/img`. Record filename-only values in lexical ascending order. Do not include absolute paths, directories, or non-`.jpg` files.
4. Write `workflow/receipt_intake_checkpoint.json` with exactly these keys and task-visible values:

```json
{
  "task_id": "jpg-ocr-stat",
  "source_directory": "/app/workspace/dataset/img",
  "image_filenames": ["...sorted filenames..."],
  "output_workbook": "/app/workspace/stat_ocr.xlsx",
  "sheet_name": "results",
  "columns": ["filename", "date", "total_amount"],
  "filename_sort": "lexical ascending by filename",
  "date_format": "YYYY-MM-DD",
  "amount_format": "string with exactly two decimal places",
  "keyword_priority": [
    "GRAND TOTAL",
    "TOTAL RM",
    "TOTAL: RM",
    "TOTAL AMOUNT",
    "TOTAL",
    "AMOUNT",
    "TOTAL DUE",
    "AMOUNT DUE",
    "BALANCE DUE",
    "NETT TOTAL",
    "NET TOTAL"
  ],
  "exclusion_keywords": [
    "SUBTOTAL",
    "SUB TOTAL",
    "TAX",
    "GST",
    "SST",
    "DISCOUNT",
    "CHANGE",
    "CASH TENDERED"
  ],
  "null_policy": "Leave the workbook cell blank when date or total_amount cannot be extracted; never write the literal string null."
}
```

5. Write `workflow/receipt_continuation_gate.json` with exactly these keys:

```json
{
  "current_record": "workflow/receipt_intake_checkpoint.json",
  "next_skill": "receipt-stat-scope",
  "immediate_obligation": "Use workflow/receipt_intake_checkpoint.json and workflow/receipt_continuation_gate.json to approve the receipt OCR working set before any OCR pass or workbook assembly.",
  "why_not_complete_yet": "The source inventory and workbook contract are frozen, but no receipt rows have been approved and /app/workspace/stat_ocr.xlsx has not been written."
}
```

6. Re-open both workflow files and validate all of the following before stopping:
- each file parses as JSON
- each file contains the required keys above
- `image_filenames` is already in lexical ascending order
- `sheet_name` is exactly `results`
- `columns` is exactly `["filename", "date", "total_amount"]`
- `/app/workspace/stat_ocr.xlsx` was not created in this stage

## Output Contract
- `image_filenames` must contain only filename-sorted `.jpg` entries from `/app/workspace/dataset/img`.
- Keep `sheet_name` exactly `results`.
- Keep `columns` exactly `filename`, `date`, `total_amount` in that order.
- Keep ISO date normalization, two-decimal amount formatting, and blank-cell null handling explicit in the checkpoint.
- Do not perform OCR, write `/app/workspace/stat_ocr.xlsx`, or mention route binding in this stage.

## Continuation Command
Run `receipt-stat-scope` with `workflow/receipt_intake_checkpoint.json` and `workflow/receipt_continuation_gate.json` as the canonical inputs. The next stage should consume these records directly instead of recreating the sorted receipt inventory.

## Stop Condition
Stop once both workflow files exist, pass the validation above, and the gate points only to `receipt-stat-scope`.
