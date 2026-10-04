---
name: production-readiness-check
description: Validate that an application is ready for production deployment and operation.
category: operations
version: 1.0.0
---

# Production Readiness Check

## Purpose

Validate that an application is ready for production deployment and operation.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Before launch
- Before exposing public traffic
- Before customer onboarding

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Architecture
- Deployment config
- Runbooks
- Monitoring setup

## Workflow

1. Verify health checks, startup, shutdown, and resource limits.
2. Check migrations, backups, secrets, and environment variables.
3. Review logging, metrics, alerts, and error handling.
4. Validate security headers, TLS, rate limits, and auth.
5. Confirm rollback and incident procedures.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Readiness score
- Blocking gaps
- Operational risks
- Launch checklist
- Rollback notes

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
