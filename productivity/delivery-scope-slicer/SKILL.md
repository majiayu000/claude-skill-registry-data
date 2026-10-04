---
name: delivery-scope-slicer
description: Break large scopes into coherent increments without losing the complete product vision.
category: product
version: 1.0.0
---

# Delivery Scope Slicer

## Purpose

Break large scopes into coherent increments without losing the complete product vision.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Scope is too large
- Planning delivery phases
- Avoiding endless MVP debates

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Full scope
- Deadlines
- Team capacity
- Dependencies

## Workflow

1. Preserve the final vision while defining deliverable slices.
2. Identify the smallest valuable release that is not disposable.
3. Sequence foundation, core workflows, automation, and polish.
4. Call out dependencies and risky late-stage work.
5. Define exit criteria for each phase.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Phase plan
- Slice definitions
- Dependencies
- Risks
- Done criteria

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
