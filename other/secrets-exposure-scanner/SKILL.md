---
name: secrets-exposure-scanner
description: Find and prevent accidental exposure of tokens, credentials, keys, and sensitive configuration.
category: security
version: 1.0.0
---

# Secrets Exposure Scanner

## Purpose

Find and prevent accidental exposure of tokens, credentials, keys, and sensitive configuration.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Reviewing commits
- Preparing public repos
- Auditing .env usage

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Repository files
- Environment variables
- CI logs
- Deployment config

## Workflow

1. Look for hardcoded tokens, passwords, private keys, and connection strings.
2. Check examples, docs, logs, and test fixtures.
3. Recommend .env.example patterns without real secrets.
4. Define rotation steps when exposure is suspected.
5. Add prevention through gitignore and CI scanning.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Exposure findings
- Risk level
- Immediate actions
- Rotation plan
- Prevention steps

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
