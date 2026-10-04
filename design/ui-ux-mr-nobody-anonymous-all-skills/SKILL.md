---
name: ui-ux
description: Design UI / UX — flows, screens, components, and interaction patterns. Produce wireframes-in-prose and design feedback.
category: design
aliases:
- ux
- ui
- interaction-design
- wireframe
triggers:
- design this UI
- UX feedback
- how should this screen work
- wireframe this
keywords:
- ui
- ux
- design
- screen
- flow
- wireframe
- component
- interaction
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- design
- screen
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

# UI / UX

## Purpose

Help the user design a screen, flow, or interaction. Produce wireframes-in-prose, identify
states, and give actionable design feedback.

## When to Use

- User is designing a screen / flow
- User wants UX feedback on an existing design
- User wants component specs

## When NOT to Use

- Visual brand decisions (route to `branding`)
- Pure implementation help (route to `coding`)

## Capabilities

- Map user flows
- Identify screen states (loading, empty, error, success)
- Suggest component composition
- Review against UX heuristics (Nielsen)

## Source

Custom skill, written for this library.

## Notes

Pairs with `frontend`, `accessibility`, `branding`.

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

Requests that should activate this skill include: "design this UI"; "UX feedback"; "how should this screen work".

## Safety

- Preserve user data and existing work.
- Confirm before destructive or externally visible actions.
- Do not expose credentials or claim unverified results.
