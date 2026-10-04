---
name: pptx
description: Read, edit, and generate PowerPoint .pptx files — extract slides, build decks from outlines.
category: documents
aliases:
- powerpoint
- slides
- deck
- presentation-generation
triggers:
- read this PowerPoint
- generate a slide deck
- make a presentation
- extract slides from
keywords:
- pptx
- powerpoint
- slides
- deck
- presentation
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- deck
- documents
- powerpoint
- pptx
- slides
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

# PPTX

## Purpose

Work with PowerPoint files: read existing decks, generate decks from outlines, edit slides.

## When to Use

- User shares a deck and wants its contents
- User wants to produce a presentation
- User wants to apply a consistent template

## Source

Custom skill, written for this library.

## Notes

Pairs with `summarization`, `presentation-design`.

## When NOT to Use

Do not use when the request is outside this capability, required context is unavailable, or a safer specialized skill applies.

## Capabilities

- Apply the pptx workflow consistently.
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

Requests that should activate this skill include: "read this PowerPoint"; "generate a slide deck"; "make a presentation".

## Safety

- Preserve user data and existing work.
- Confirm before destructive or externally visible actions.
- Do not expose credentials or claim unverified results.
