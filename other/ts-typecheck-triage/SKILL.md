---
name: ts-typecheck-triage
description: 'Triages TypeScript errors, applies minimal safe fixes, and validates results in focused waves'
---

# TS Typecheck Triage

Use this skill when TypeScript errors block implementation progress.

## Inputs

- Target scope (file(s), folder, or full project)
- Current compiler command (`tsc`, project config)
- Any known hot files from previous runs

## Workflow

1. Capture current error set (diagnostics or `tsc --noEmit`)
2. Group by root cause (imports, typings, model mismatch, syntax)
3. Fix highest-leverage root cause first
4. Re-run focused validation
5. Re-run broader validation
6. Update tracker only with verified numbers

## Fix Strategy

- Prefer API/name alignment over introducing aliases unless needed.
- Prefer local state/service fallback when store exports are missing.
- Keep edits minimal and reversible.

## Output

- Files changed
- Error count before/after
- Remaining blockers by file and category

## Gotchas

- Terminal output can lag or buffer; corroborate with diagnostics.
- Be careful with encoding when writing tracker markdown from terminal.

<!-- Inspired by awesome-copilot skills structure -->
