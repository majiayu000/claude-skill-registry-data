---
name: data-model-sentinel
description: Review database schema, indexes, constraints, naming, migrations, and query patterns.
category: engineering
version: 1.0.0
---

# Data Model Sentinel

## Purpose

Review database schema, indexes, constraints, naming, migrations, and query patterns.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Designing tables
- Reviewing migrations
- Fixing slow queries

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Schema
- Queries
- Expected volume
- Access patterns

## Workflow

1. Validate primary keys, foreign keys, unique constraints, and nullability.
2. Check indexes against actual query patterns.
3. Review naming, normalization, and data lifecycle.
4. Identify migration risks and backfill needs.
5. Consider reporting, BI, and audit requirements.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Schema assessment
- Index recommendations
- Constraint issues
- Migration risks
- Query notes

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
