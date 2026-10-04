---
name: roadmap-strategist
description: Create a practical roadmap balancing user value, technical foundation, risk, and sequencing.
category: product
version: 1.0.0
---

# Roadmap Strategist

## Purpose

Create a practical roadmap balancing user value, technical foundation, risk, and sequencing.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Planning quarters
- Prioritizing features
- Preparing GitHub milestones

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Product goals
- Feature list
- Risks
- Capacity

## Workflow

1. Group work by outcomes, not only components.
2. Sequence technical prerequisites before dependent features.
3. Balance quick wins with platform foundations.
4. Define milestones with visible outcomes.
5. Identify what should explicitly not be built yet.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Milestones
- Priorities
- Dependencies
- Risks
- Deferred scope

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
