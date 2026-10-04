---
name: ci-cd-pipeline-builder
description: Create or review CI/CD pipelines for build, lint, typecheck, tests, security checks, and deployment.
category: devops
version: 1.0.0
---

# CI CD Pipeline Builder

## Purpose

Create or review CI/CD pipelines for build, lint, typecheck, tests, security checks, and deployment.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Setting up GitHub Actions
- Adding quality gates
- Automating releases

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Tech stack
- Package scripts
- Deployment target
- Secrets requirements

## Workflow

1. Run fast checks before expensive checks.
2. Cache dependencies safely.
3. Separate CI validation from deployment.
4. Protect secrets and environment-specific deploys.
5. Fail clearly with useful logs.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Pipeline design
- Workflow YAML
- Required secrets
- Quality gates
- Release flow

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
