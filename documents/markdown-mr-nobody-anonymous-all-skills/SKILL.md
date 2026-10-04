---
name: markdown
description: Read, write, lint, and transform Markdown — headings, links, code fences, tables, and common dialects.
category: documents
aliases:
- md
- markdown-lint
- gfm
triggers:
- format this markdown
- lint markdown
- convert markdown to
- markdown style
keywords:
- markdown
- md
- gfm
- headings
- links
- code
- fence
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- documents
- gfm
- headings
- markdown
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

# Markdown

## Purpose

Work with Markdown — write clean, consistent MD; convert to / from other formats; lint for
common issues.

## When to Use

- User shares markdown
- User wants to convert markdown → HTML / PDF / DOCX
- User wants to enforce a markdown style guide

## Source

Custom skill, written for this library.

## Notes

Pairs with `documentation`, `summarization`.

## When NOT to Use

Do not use when the request is outside this capability, required context is unavailable, or a safer specialized skill applies.

## Capabilities

- Apply the markdown workflow consistently.
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

## Tools

- No mandatory tool unless declared in frontmatter.
- Use only project-approved tools and documented optional dependencies.

## Examples

Requests that should activate this skill include: "format this markdown"; "lint markdown"; "convert markdown to".

## Safety

- Preserve user data and existing work.
- Confirm before destructive or externally visible actions.
- Do not expose credentials or claim unverified results.
