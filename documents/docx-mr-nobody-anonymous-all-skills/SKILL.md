---
name: docx
description: Read, edit, and generate Microsoft Word .docx files — extract text, modify structure, and produce documents programmatically.
category: documents
aliases:
- word
- docx-reading
- docx-generation
triggers:
- read this Word doc
- extract from docx
- generate a Word document
- edit this docx
keywords:
- docx
- word
- document
- .docx
- openxml
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- .docx
- document
- documents
- docx
- word
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

# DOCX

## Purpose

Work with .docx files: read content, edit structure, generate documents from templates.

## When to Use

- User shares a .docx and wants its contents
- User wants to produce a Word document
- User wants to fill a Word template

## Tools

- Python: `python-docx`
- Or a CLI tool of choice

## Source

Custom skill, written for this library.

## Notes

Pairs with `summarization`, `report-generation`.

## When NOT to Use

Do not use when the request is outside this capability, required context is unavailable, or a safer specialized skill applies.

## Capabilities

- Apply the docx workflow consistently.
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

Requests that should activate this skill include: "read this Word doc"; "extract from docx"; "generate a Word document".

## Safety

- Preserve user data and existing work.
- Confirm before destructive or externally visible actions.
- Do not expose credentials or claim unverified results.
