---
name: accessibility
description: Accessibility (a11y) testing — WCAG checks, keyboard navigation, screen-reader semantics, color contrast.
category: web
aliases:
- a11y
- wcag
- accessibility-testing
triggers:
- accessibility check
- a11y audit
- WCAG
- is this accessible
- keyboard navigation
keywords:
- accessibility
- a11y
- wcag
- keyboard
- screen
- reader
- contrast
- aria
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- a11y
- accessibility
- keyboard
- wcag
- web
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

# Accessibility

## Purpose

Audit UI / web content for accessibility. Check against WCAG principles, keyboard
navigation, screen-reader semantics, and color contrast.

## When to Use

- User wants an accessibility audit
- User is shipping a UI
- User is fixing reported a11y issues

## Safety

- Accessibility is a practice, not a checklist
- Include users with disabilities when designing

## Source

Custom skill, written for this library.

## Notes

Pairs with `browser-automation` (to run automated checks) and `code-review` (to enforce standards).

## When NOT to Use

Do not use when the request is outside this capability, required context is unavailable, or a safer specialized skill applies.

## Capabilities

- Apply the accessibility workflow consistently.
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

Requests that should activate this skill include: "accessibility check"; "a11y audit"; "WCAG".
