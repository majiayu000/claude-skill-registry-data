---
name: privacy-lgpd-guardian
description: Review personal-data handling with privacy-by-design and LGPD-oriented controls.
category: security
version: 1.0.0
---

# Privacy LGPD Guardian

## Purpose

Review personal-data handling with privacy-by-design and LGPD-oriented controls.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Handling user data
- Building exports
- Creating admin dashboards
- Storing logs

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Data fields
- Processing purpose
- Access roles
- Retention needs

## Workflow

1. Identify personal and sensitive data categories.
2. Verify purpose limitation and data minimization.
3. Review access, retention, deletion, anonymization, and audit logs.
4. Check exports, backups, and third-party sharing.
5. Recommend practical privacy controls.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Data inventory
- Privacy risks
- Controls
- Retention notes
- Audit requirements

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
