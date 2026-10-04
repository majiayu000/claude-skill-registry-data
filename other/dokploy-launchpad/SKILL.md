---
name: dokploy-launchpad
description: Prepare applications for deployment on Dokploy with Docker, networks, domains, Traefik, and environment variables.
category: devops
version: 1.0.0
---

# Dokploy Launchpad

## Purpose

Prepare applications for deployment on Dokploy with Docker, networks, domains, Traefik, and environment variables.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Deploying to Dokploy
- Debugging Dokploy services
- Preparing self-hosted SaaS

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Project stack
- Compose file
- Domains
- Environment variables
- Service logs

## Workflow

1. Validate the expected Dokploy deployment mode.
2. Check internal service names, ports, and public domains.
3. Review Traefik labels or external routing expectations.
4. Separate build-time and runtime variables.
5. Provide exact diagnostic commands.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Deployment plan
- Required variables
- Network/routing notes
- Debug commands
- Rollback advice

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
