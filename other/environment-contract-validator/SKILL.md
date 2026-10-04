---
name: environment-contract-validator
description: Validate environment variables, configuration contracts, examples, and deployment consistency.
category: devops
version: 1.0.0
---

# Environment Contract Validator

## Purpose

Validate environment variables, configuration contracts, examples, and deployment consistency.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Creating .env.example
- Debugging missing vars
- Preparing deployment docs

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Code config usage
- .env
- .env.example
- Deployment environment

## Workflow

1. Find required and optional environment variables.
2. Check naming consistency across frontend, backend, jobs, and docs.
3. Separate public, private, build-time, and runtime variables.
4. Ensure example values are safe and useful.
5. Recommend startup validation for required variables.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Variable inventory
- Missing variables
- Unsafe values
- Example file
- Validation recommendations

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
