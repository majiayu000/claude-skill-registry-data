---
name: pdf-intake-checkpoint
description: "Create an intake checkpoint for PDF update tasks so downstream edits use a frozen task identity and a clear continuation gate."
---

# PDF Intake Checkpoint

## Purpose

Create a small intake checkpoint before editing so the task stays consistent across steps. This prevents scope drift (for example, mixing draft files or stale instructions) and makes the next action explicit.

## When to use

Use this at the start of a PDF update task where:
- an input PDF and instruction text are provided,
- output path is predetermined,
- later steps must remain reviewable and reproducible.

## Inputs

- `/root/input/input.pdf`
- `/root/input/input.txt`
- intended output path: `/root/output/output.pdf`

## Actions

1. Confirm the two required inputs exist.
2. Read `input.txt` once and capture high-level obligations (fill/update fields, redact if requested, date/signature requirements).
3. Write `workflow/intake_checkpoint.json` with frozen identity fields:
   - `task_type`
   - `primary_input_pdf`
   - `instruction_source`
   - `primary_output_pdf`
   - `checkpoint_status`
4. Write `workflow/continuation_gate.json` with only the immediate next obligation:
   - `next_stage`: `pdf-working-scope`
   - `gate_reason`: standardize approved working set before editing
   - `proceed_condition`: working set record exists

## Required outputs

- `workflow/intake_checkpoint.json`
- `workflow/continuation_gate.json`

## Notes

- Keep this stage lightweight: identity freeze + next-step gate only.
- Do not edit the PDF in this stage.
- Downstream stages should treat this checkpoint as the canonical starting record.
