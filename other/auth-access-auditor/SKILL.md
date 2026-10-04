---
name: auth-access-auditor
description: Audit authentication, sessions, roles, permissions, tenancy, and access-control boundaries.
category: security
version: 1.0.0
---

# Auth Access Auditor

## Purpose

Audit authentication, sessions, roles, permissions, tenancy, and access-control boundaries.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Implementing login
- Adding roles
- Building admin modules
- Reviewing multitenancy

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Auth flow
- Role matrix
- Routes
- Data ownership rules

## Workflow

1. Map identity, session, authorization, and audit flow.
2. Check vertical and horizontal privilege escalation risks.
3. Review admin actions, impersonation, and tenant boundaries.
4. Validate secure defaults and failure behavior.
5. Recommend tests for permission boundaries.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Access model
- Permission risks
- Missing checks
- Test matrix
- Required fixes

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
