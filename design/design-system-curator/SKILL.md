---
name: design-system-curator
description: Review and improve UI consistency through tokens, components, states, accessibility, and usage rules.
category: design
version: 1.0.0
---

# Design System Curator

## Purpose

Review and improve UI consistency through tokens, components, states, accessibility, and usage rules.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Building a component library
- Improving UI consistency
- Reviewing frontend implementation

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Components
- Design tokens
- Screenshots
- Brand requirements

## Workflow

1. Check typography, spacing, radius, colors, and shadows.
2. Review component states: default, hover, focus, disabled, loading, error.
3. Validate accessibility and keyboard behavior.
4. Identify one-off components that should be standardized.
5. Create usage rules that developers can follow.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Design system audit
- Token recommendations
- Component issues
- Accessibility notes
- Implementation plan

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
