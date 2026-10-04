---
name: requirements-crystallizer
description: Convert vague requests into clear functional and non-functional requirements.
category: product
version: 1.0.0
---

# Requirements Crystallizer

## Purpose

Convert vague requests into clear functional and non-functional requirements.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- A request is ambiguous
- Before implementation
- Before writing tickets

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- User request
- Business rules
- Constraints
- Acceptance expectations

## Workflow

1. Extract explicit requirements from the request.
2. Infer likely implicit requirements and mark them as assumptions.
3. Identify missing decisions that block implementation.
4. Separate functional, non-functional, data, and security requirements.
5. Make requirements testable.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Functional requirements
- Non-functional requirements
- Assumptions
- Open questions
- Acceptance criteria

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
