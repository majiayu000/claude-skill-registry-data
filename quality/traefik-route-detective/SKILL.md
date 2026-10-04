---
name: traefik-route-detective
description: Diagnose Traefik routing, TLS, middleware, service discovery, and upstream connectivity issues.
category: devops
version: 1.0.0
---

# Traefik Route Detective

## Purpose

Diagnose Traefik routing, TLS, middleware, service discovery, and upstream connectivity issues.

Use this skill to produce clear, actionable work. Avoid generic advice. Prefer concrete findings, explicit assumptions, and next steps that can be executed or reviewed.

## Use When

- Getting 404/502/503
- TLS certificate problems
- Host routing mismatch

## Required Context

Ask for missing context only when it blocks a correct answer. Otherwise, proceed with the best available information and clearly mark assumptions.

- Traefik config
- Docker labels
- Logs
- Domains
- curl results

## Workflow

1. Distinguish router mismatch from upstream failure.
2. Check entrypoints, host rules, TLS resolver, and middlewares.
3. Validate target service port and Docker network membership.
4. Use curl with Host headers to isolate layers.
5. Recommend minimal safe config changes.

## Guardrails

- Do not invent facts, files, commands, credentials, or project state.
- Separate confirmed information from assumptions.
- Prefer concise recommendations over long theoretical explanations.
- Make trade-offs explicit.
- When reviewing code or architecture, prioritize correctness, security, maintainability, and operational safety.
- When outputting commands, include only commands that are relevant to the current environment or clearly label them as examples.

## Output Contract

Always structure the final answer with these sections when applicable:

- Likely failure layer
- Evidence
- Commands
- Config fixes
- Verification steps

## Quality Bar

A strong result from this skill should be specific enough that a developer, reviewer, maintainer, or product owner can act on it without needing a second clarification round.
