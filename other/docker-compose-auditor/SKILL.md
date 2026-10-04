---
name: docker-compose-auditor
description: Review Docker Compose files for correctness, security, networking, volumes, health checks, and deployability.
category: devops
version: 1.0.0
---

# Docker Compose Auditor

## Purpose

Review Docker Compose files for correctness, security, networking, volumes, health checks, and deployability.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Preparing local or Dokploy deployment
- Debugging containers
- Reviewing Compose changes

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- compose.yaml
- .env
- Dockerfiles
- Deployment target

## Workflow

1. Validate services, images, build contexts, ports, and networks.
2. Check volumes, persistence, restart policy, and health checks.
3. Review secrets, environment variables, and public exposure.
4. Detect invalid or target-specific Compose options.
5. Recommend commands to verify config and runtime state.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Compose assessment
- Blocking issues
- Security notes
- Network/volume notes
- Validation commands

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
