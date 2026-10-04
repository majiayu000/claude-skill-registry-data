---
name: safe-refactor-orchestrator
description: Plan and review refactors while preserving external behavior and reducing regression risk.
category: engineering
version: 1.0.0
---

# Safe Refactor Orchestrator

## Purpose

Plan and review refactors while preserving external behavior and reducing regression risk.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Refactoring legacy code
- Reducing duplication
- Changing architecture

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Current code
- Target design
- Test coverage
- Known constraints

## Workflow

1. Define the behavior that must not change.
2. Identify characterization tests before refactoring.
3. Prefer small reversible steps.
4. Avoid mixing refactor and feature changes.
5. Create validation commands for each stage.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Refactor plan
- Behavior contract
- Test gaps
- Step sequence
- Risk controls

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
