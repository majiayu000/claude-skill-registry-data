---
name: image
description: Work with images — read, resize, convert, OCR, and inspect metadata.
category: utilities
aliases:
- images
- ocr
- image-processing
triggers:
- read this image
- OCR this
- resize image
- convert image format
keywords:
- image
- ocr
- resize
- convert
- jpg
- png
- metadata
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- convert
- image
- ocr
- resize
- utilities
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

# Image

## Purpose

Work with image files: read metadata, resize, convert formats, OCR text from images.

## Tools

- Python: `Pillow`, `pytesseract`
- CLI: ImageMagick

## Source

Custom skill, written for this library.

## When to Use

Use when the request matches the documented image capability or its declared triggers.

## When NOT to Use

Do not use when the request is outside this capability, required context is unavailable, or a safer specialized skill applies.

## Capabilities

- Apply the image workflow consistently.
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

Requests that should activate this skill include: "read this image"; "OCR this"; "resize image".

## Safety

- Preserve user data and existing work.
- Confirm before destructive or externally visible actions.
- Do not expose credentials or claim unverified results.

## Notes

This section was normalized to satisfy the library contract; retain more specific guidance elsewhere in this file.
