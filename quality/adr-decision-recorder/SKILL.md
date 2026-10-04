---
name: adr-decision-recorder
description: Write Architecture Decision Records that capture context, options, decision, consequences, and follow-up.
category: docs
version: 1.0.0
---

# ADR Decision Recorder

## Purpose

Write Architecture Decision Records that capture context, options, decision, consequences, and follow-up.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Making architecture choices
- Changing core patterns
- Documenting trade-offs

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Decision topic
- Context
- Options considered
- Chosen option

## Workflow

1. State the context and problem clearly.
2. List realistic alternatives, not strawmen.
3. Explain consequences and trade-offs.
4. Define follow-up actions and revisit triggers.
5. Keep the ADR concise and durable.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- ADR title
- Status
- Context
- Decision
- Consequences

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
