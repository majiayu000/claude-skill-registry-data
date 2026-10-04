---
name: csv
description: Read, parse, write, and clean CSV files — dialect handling, type inference, and validation.
category: documents
aliases:
- csv-reading
- csv-cleaning
- csv-generation
triggers:
- read this CSV
- parse CSV
- clean this CSV
- generate a CSV
keywords:
- csv
- comma-separated
- parse
- dialect
- quote
- field
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- comma-separated
- csv
- dialect
- documents
- parse
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

# CSV

## Purpose

Work with CSV files: parse with the right dialect, validate, clean, and write.

## When to Use

- User shares a CSV
- User wants to export data as CSV
- User has a messy CSV and wants it cleaned

## Source

Custom skill, written for this library.

## Notes

Pairs with `data-analysis`.

## When NOT to Use

Do not use when the request is outside this capability, required context is unavailable, or a safer specialized skill applies.

## Capabilities

- Apply the csv workflow consistently.
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

Requests that should activate this skill include: "read this CSV"; "parse CSV"; "clean this CSV".

## Safety

- Preserve user data and existing work.
- Confirm before destructive or externally visible actions.
- Do not expose credentials or claim unverified results.
