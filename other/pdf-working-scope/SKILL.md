---
name: pdf-working-scope
description: "Approve a narrow working set for PDF editing and track selected vs non-selected artifacts to avoid duplicate scanning and drift."
---

# PDF Working Scope

## Purpose

Turn intake records into an approved working set so later steps can proceed from one validated scope record instead of repeatedly rescanning the workspace. This is required for consistency, rollback clarity, and traceable completion.

## Prerequisites

- `workflow/intake_checkpoint.json`
- `workflow/continuation_gate.json`

## Actions

1. Read intake checkpoint and continuation gate.
2. Build a selected artifact set required for completion:
   - `/root/input/input.pdf`
   - `/root/input/input.txt`
   - `/root/output/output.pdf` (target artifact)
3. Record explicit non-selected candidates (any unrelated files not needed for this task run).
4. Write `workflow/working_set_record.json` with:
   - `selected_candidates`
   - `non_selected_candidates`
   - `selected_status`: `pending_continuation`
   - `authoritative_next_stage`: `pdf-packet-binder`
5. Write `workflow/scope_summary.json` with a concise summary of task-relevant obligations from input text (fullname usage, redaction requirement, date/signature expectation, no text-covering mistakes).

## Required outputs

- `workflow/working_set_record.json`
- `workflow/scope_summary.json`

## Gate discipline

Do not move to editing/final closure from raw inputs once this file exists; use this approved scope as the single working record.
