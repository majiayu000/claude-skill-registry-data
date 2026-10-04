---
name: migration-risk-planner
description: Plan safe database, infrastructure, or application migrations with rollback and validation steps.
category: engineering
version: 1.0.0
---

# Migration Risk Planner

## Purpose

Plan safe database, infrastructure, or application migrations with rollback and validation steps.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Applying migrations
- Changing storage
- Updating production services

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Current state
- Target state
- Data volume
- Rollback requirements

## Workflow

1. Classify migration risk and downtime impact.
2. Separate schema change, data backfill, and application rollout.
3. Define pre-checks, deploy steps, post-checks, and rollback.
4. Account for compatibility during rolling deploys.
5. Include observability and verification commands.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Migration plan
- Pre-checks
- Execution steps
- Rollback plan
- Validation checklist

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
