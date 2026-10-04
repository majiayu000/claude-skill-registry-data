---
name: writing
description: Help the user write clearly — drafts, edits, tone, structure. Apply principles of clear writing.
category: utilities
aliases:
- draft
- edit
- copywriting
triggers:
- help me write
- edit this
- draft an email
- make this clearer
keywords:
- write
- draft
- edit
- copy
- prose
- tone
- clarity
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- copy
- draft
- edit
- utilities
- write
- writing
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

# Writing

## Purpose

Help the user write clearly — for the audience, in the right tone, with the right structure.

## Capabilities

- Draft from outline
- Edit for clarity
- Adjust tone (formal, casual, persuasive)
- Headlines and subject lines
- Email / message / doc drafts

## Source

Custom skill, written for this library.

## Notes

Pairs with `summarization`, `documentation`, `branding`.

## When to Use

Use when the request matches the documented writing capability or its declared triggers.

## When NOT to Use

Do not use when the request is outside this capability, required context is unavailable, or a safer specialized skill applies.

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

Requests that should activate this skill include: "help me write"; "edit this"; "draft an email".

## Safety

- Preserve user data and existing work.
- Confirm before destructive or externally visible actions.
- Do not expose credentials or claim unverified results.
