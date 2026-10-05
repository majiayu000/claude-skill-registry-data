---
name: receipt-scanner
description: Receipt OCR and structuring skill. Use when Codex needs to extract vendor, date, totals, and categories from receipts or expense images.
---

# Receipt Scanner

Use this skill when the user has messy receipts, scans, or screenshots that need structured output.

## Workflow
- Extract key fields and normalize formats.
- Return tabular output for spreadsheets.
- Flag low-confidence fields instead of guessing.

## Deliverables
- Structured receipt rows or CSV-ready output.
- A short manual-review list.

## Guardrails
- Do not pretend uncertain OCR is certain.
- Do not mix categories without a declared taxonomy.
