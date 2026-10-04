---
name: domain-model-auditor
description: Validate entities, relationships, invariants, and business rules in a domain model.
category: engineering
version: 1.0.0
---

# Domain Model Auditor

## Purpose

Validate entities, relationships, invariants, and business rules in a domain model.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Designing database entities
- Reviewing business logic
- Before migrations

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Entities
- Relationships
- Business rules
- Use cases

## Workflow

1. Identify aggregate boundaries and ownership.
2. Check cardinality and lifecycle rules.
3. Surface missing invariants and invalid states.
4. Separate domain rules from UI or infrastructure concerns.
5. Recommend naming that matches the business language.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Domain map
- Invariants
- Invalid states
- Naming issues
- Model improvements

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
