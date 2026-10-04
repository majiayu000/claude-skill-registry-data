---
name: tdd-coach
description: Guide implementation through red-green-refactor with small, testable increments.
category: quality
version: 1.0.0
---

# TDD Coach

## Purpose

Guide implementation through red-green-refactor with small, testable increments.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Writing new logic
- Fixing bugs safely
- Refactoring complex behavior

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Expected behavior
- Current code
- Test framework
- Constraints

## Workflow

1. Start with a failing test that captures behavior.
2. Make the smallest change to pass.
3. Refactor only after tests pass.
4. Keep tests readable and focused on behavior.
5. Repeat in small increments.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- First failing test
- Implementation step
- Refactor notes
- Next test
- Validation command

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
