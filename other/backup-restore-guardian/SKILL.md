---
name: backup-restore-guardian
description: Review backup, restore, retention, and disaster-recovery procedures.
category: operations
version: 1.0.0
---

# Backup Restore Guardian

## Purpose

Review backup, restore, retention, and disaster-recovery procedures.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Deploying databases
- Handling documents/files
- Preparing production operations

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Data stores
- Backup jobs
- Retention rules
- Recovery objectives

## Workflow

1. Identify all critical data sources and file stores.
2. Define RPO and RTO expectations.
3. Check encryption, retention, and offsite strategy.
4. Verify restore tests, not just backup existence.
5. Document emergency recovery steps.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Backup map
- RPO/RTO
- Gaps
- Restore test plan
- Runbook

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
