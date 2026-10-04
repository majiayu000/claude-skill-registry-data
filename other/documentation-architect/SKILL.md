---
name: documentation-architect
description: Design documentation structure for products, APIs, developer onboarding, and operations.
category: docs
version: 1.0.0
---

# Documentation Architect

## Purpose

Design documentation structure for products, APIs, developer onboarding, and operations.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Creating docs folder
- Improving maintainability
- Preparing public repo docs

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Audience
- Project scope
- Existing docs
- Support needs

## Workflow

1. Separate user docs, developer docs, API docs, and operations docs.
2. Create navigation that mirrors user intent.
3. Avoid duplicating facts across many files.
4. Define ownership and update triggers.
5. Include examples and troubleshooting.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Docs IA
- Recommended files
- Content outline
- Maintenance rules
- Missing docs

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
