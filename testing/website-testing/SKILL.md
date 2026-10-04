---
name: website-testing
description: End-to-end testing of websites — happy paths, edge cases, browser matrix, and visual regressions.
category: web
aliases:
- e2e-testing
- end-to-end
- visual-regression
triggers:
- test this website
- e2e tests
- end-to-end test
- visual regression
keywords:
- test
- e2e
- end-to-end
- regression
- browser
- matrix
- automation
dependencies:
- optional:playwright-or-cypress
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- e2e
- end-to-end
- regression
- test
- testing
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

# Website Testing

## Purpose

End-to-end test a website's user flows across browsers. Catch regressions and ensure core
flows work.

## When to Use

- Shipping a web product
- Pre-release verification
- Continuous integration

## Safety

- Use stable selectors (test IDs, ARIA roles) over CSS
- Don't test implementation details

## Source

Custom skill, written for this library.

## Notes

Pairs with `browser-automation`, `accessibility`.

## When NOT to Use

Do not use when the request is outside this capability, required context is unavailable, or a safer specialized skill applies.

## Capabilities

- Apply the website-testing workflow consistently.
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

Requests that should activate this skill include: "test this website"; "e2e tests"; "end-to-end test".
