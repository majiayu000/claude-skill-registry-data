---
name: quality-gatekeeper
description: Apply a release-quality checklist before code is merged, shipped, or deployed.
category: quality
version: 1.0.0
---

# Quality Gatekeeper

## Purpose

Apply a release-quality checklist before code is merged, shipped, or deployed.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Before merge
- Before release
- Before deploying to production

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Change summary
- Diff
- Test status
- Deployment context

## Workflow

1. Validate build, lint, typecheck, and tests.
2. Confirm security, privacy, and permission impact.
3. Verify migrations, environment variables, and compatibility.
4. Check documentation and changelog needs.
5. Assign an approval status with required fixes.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Status
- Required fixes
- Recommended improvements
- Validation commands
- Release risk

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
