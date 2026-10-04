---
name: test-strategy-designer
description: Design a layered test strategy for frontend, backend, APIs, integrations, and critical workflows.
category: quality
version: 1.0.0
---

# Test Strategy Designer

## Purpose

Design a layered test strategy for frontend, backend, APIs, integrations, and critical workflows.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Planning tests
- Improving QA
- Adding quality gates

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Feature scope
- Architecture
- Risk areas
- Existing tests

## Workflow

1. Identify critical user journeys.
2. Choose unit, integration, E2E, contract, and smoke tests appropriately.
3. Avoid over-testing implementation details.
4. Include fixtures, mocks, and test data strategy.
5. Define CI execution order and failure policy.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Test matrix
- Critical scenarios
- Tooling recommendations
- CI plan
- Coverage gaps

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
