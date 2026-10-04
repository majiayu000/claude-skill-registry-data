---
name: branding
description: Brand identity work — voice, naming, visual language, and consistency.
category: design
aliases:
- brand
- identity
- voice
- naming
triggers:
- brand this
- help with brand voice
- naming ideas
- visual identity
keywords:
- brand
- voice
- identity
- naming
- logo
- visual
- language
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- brand
- branding
- design
- identity
- naming
- voice
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

# Branding

## Purpose

Help the user develop and apply brand identity: voice, naming, visual language, and
consistency across touchpoints.

## Source

Custom skill, written for this library.

## When to Use

Use when the request matches the documented branding capability or its declared triggers.

## When NOT to Use

Do not use when the request is outside this capability, required context is unavailable, or a safer specialized skill applies.

## Capabilities

- Apply the branding workflow consistently.
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

Requests that should activate this skill include: "brand this"; "help with brand voice"; "naming ideas".

## Safety

- Preserve user data and existing work.
- Confirm before destructive or externally visible actions.
- Do not expose credentials or claim unverified results.

## Notes

This section was normalized to satisfy the library contract; retain more specific guidance elsewhere in this file.
