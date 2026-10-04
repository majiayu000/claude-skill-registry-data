---
name: xlsx
description: Read, edit, and generate Excel .xlsx files — read sheets, compute, and produce workbooks programmatically.
category: documents
aliases:
- excel
- spreadsheet
- xlsx-reading
triggers:
- read this spreadsheet
- extract from xlsx
- generate an Excel file
- edit this spreadsheet
keywords:
- xlsx
- excel
- spreadsheet
- sheet
- workbook
- .xlsx
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- documents
- excel
- sheet
- spreadsheet
- xlsx
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# XLSX

## Purpose

Work with .xlsx files: read sheets and cells, compute with the data, and produce workbooks.

## When to Use

- User shares a spreadsheet
- User wants to produce an Excel report
- User wants to apply formulas / formatting

## Tools

- Python: `openpyxl`, `pandas`
- Or a CLI tool of choice

## Source

Custom skill, written for this library.

## Notes

Pairs with `data-analysis`, `data-visualization`.

## When NOT to Use

Do not use when the request is outside this capability, required context is unavailable, or a safer specialized skill applies.

## Capabilities

- Apply the xlsx workflow consistently.
- Produce a clear, reviewable result.
- Surface assumptions, constraints, and unresolved risks.

## Inputs

- The user's goal and desired output.
- Relevant source material, constraints, and environment details.
- Acceptance criteria when available.

## Workflow

1. Confirm the goal, scope, and constraints.
2. Inspect the available context before acting.
3. Apply the skill-specific guidance in this document.
4. Verify the result and report limitations or next steps.

## Examples

Requests that should activate this skill include: "read this spreadsheet"; "extract from xlsx"; "generate an Excel file".

## Safety

- Preserve user data and existing work.
- Confirm before destructive or externally visible actions.
- Do not expose credentials or claim unverified results.
