---
name: edge-case-scout
description: Discover edge cases, invalid inputs, concurrency issues, and abnormal states.
category: quality
version: 1.0.0
---

# Edge Case Scout

## Purpose

Discover edge cases, invalid inputs, concurrency issues, and abnormal states.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Designing features
- Writing tests
- Hardening APIs

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Feature behavior
- Data model
- User roles
- Input constraints

## Workflow

1. Test empty, null, invalid, duplicated, and oversized inputs.
2. Check permission boundaries and role changes.
3. Consider concurrency, retries, and partial failures.
4. Review time zones, localization, and formatting.
5. Include abnormal but realistic production states.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Edge case list
- Negative cases
- Concurrency risks
- Permission cases
- Test ideas

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
