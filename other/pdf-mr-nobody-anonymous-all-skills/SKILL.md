---
name: pdf
description: Read, extract text, summarize, and produce PDF files. Parse structured content where possible.
category: documents
aliases:
- pdf-reading
- pdf-generation
- pdf-extraction
triggers:
- read this PDF
- extract text from PDF
- summarize this PDF
- generate a PDF
- make a PDF
keywords:
- pdf
- document
- extract
- summarize
- generate
- read
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
capabilities:
- pdf-reading
- extract-text
- extract-tables
- summarize
- generate-pdf
inputs:
- pdf_file
outputs:
- text
- markdown
- tables
permissions:
  filesystem: read-write
  network: none
  shell: none
  secrets: none
compatibility:
  generic: true
  claude_code: true
  codex: true
  cursor: true
  cline: true
  opencode: true
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- document
- documents
- extract
- pdf
- summarize
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# PDF

## Purpose

Work with PDF files — read content, extract text and tables, summarize, and produce PDFs.

## When to Use

- User shares a PDF and wants its contents
- User wants a summary or extraction
- User wants to generate a PDF

## When NOT to Use

- The file is actually a scanned image — needs OCR first (use `image` skill)
- The PDF is DRM-protected

## Capabilities

- Text extraction
- Page-by-page reading
- Table extraction
- Summarization
- PDF generation from text / HTML / markdown

## Tools

- Python: `pypdf`, `pdfplumber`, `reportlab`
- Or a CLI tool of choice

## Source

Custom skill, written for this library.

## Notes

Pairs with `summarization`, `data-analysis`.

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

Requests that should activate this skill include: "read this PDF"; "extract text from PDF"; "summarize this PDF".

## Safety

- Preserve user data and existing work.
- Confirm before destructive or externally visible actions.
- Do not expose credentials or claim unverified results.
