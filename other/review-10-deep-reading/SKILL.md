---
name: review-10-deep-reading
description: Produce structured deep-reading notes from full-text medical papers. Use when extracting methods, results, mechanisms, limitations, and usable review material from PDFs.
---

# Review 10 Deep Reading

## Purpose

Extract evidence in a way that preserves the boundary between reported findings and interpretation.

## Required Inputs

- Full-text PDFs or readable text.
- Classification table.
- Review question and target themes.

## Output

Create one note per paper under `07_reading_notes/paper_notes/` with:

- Citation and study type.
- Objective and design.
- Population/model/sample.
- Key findings with page/table/figure location.
- Limitations.
- Usable manuscript point.
- Do-not-overstate warning.

## Completion Gate

Pass only when key claims include source location and evidence strength.

## Stop Rules

Do not convert association into mechanism or causality unless the original paper supports it experimentally.
