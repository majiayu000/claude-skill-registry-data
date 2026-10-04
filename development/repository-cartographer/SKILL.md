---
name: repository-cartographer
description: Map a codebase structure, identify key modules, and explain how the project fits together.
category: engineering
version: 1.0.0
---

# Repository Cartographer

## Purpose

Map a codebase structure, identify key modules, and explain how the project fits together.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Onboarding into a repo
- Understanding unfamiliar code
- Preparing architecture docs

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Repository tree
- Important files
- Build commands
- Runtime services

## Workflow

1. Identify entry points, modules, and boundaries.
2. Explain frontend, backend, database, jobs, and infrastructure if present.
3. Separate framework conventions from custom code.
4. Highlight duplicated or confusing areas.
5. Produce a map a new contributor can actually use.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- System map
- Module inventory
- Data flow
- Runtime flow
- Onboarding notes

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
