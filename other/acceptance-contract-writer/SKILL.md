---
name: acceptance-contract-writer
description: Write precise acceptance criteria and behavior contracts for features and tickets.
category: product
version: 1.0.0
---

# Acceptance Contract Writer

## Purpose

Write precise acceptance criteria and behavior contracts for features and tickets.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Creating issues
- Preparing QA
- Clarifying done criteria

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Feature description
- User roles
- Business rules
- Edge cases

## Workflow

1. Use observable behavior, not vague intent.
2. Define success and failure paths.
3. Include permissions, validation, and empty states.
4. Cover important edge cases.
5. Avoid implementation details unless required.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- User story
- Acceptance criteria
- Edge cases
- Negative cases
- Test notes

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
