---
name: strategy-pressure-test
description: Stress-test ideas, plans, features, and implementation proposals before execution.
category: strategy
version: 1.0.0
---

# Strategy Pressure Test

## Purpose

Stress-test ideas, plans, features, and implementation proposals before execution.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- A plan feels vague
- A user wants a stronger solution
- A feature may have hidden risks

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Goal
- Current plan
- Constraints
- Success criteria

## Workflow

1. Clarify the real objective and non-goals.
2. Identify assumptions, missing context, and risky shortcuts.
3. Challenge complexity, sequencing, and dependencies.
4. Force trade-off decisions instead of accepting vague scope.
5. Convert weak ideas into concrete next actions.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Decision summary
- Critical questions
- Risks
- Required clarifications
- Improved plan

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
