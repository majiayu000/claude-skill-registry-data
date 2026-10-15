---
name: open-zeabur-kit
description: Deploy and operate authorized Zeabur projects, services, environments, domains, variables, databases, health checks, logs, scaling, and rollbacks. Use for first deployment, repair, promotion, or end-to-end production verification.
---

# Open Zeabur Kit

Use the connected Zeabur interface and repository deployment contract. Keep each hostname owned by one platform.

## Workflow

1. Confirm team, project, region, environment, service, source, branch, and domain ownership.
2. Read builds, runtime settings, variable names, networking, volumes, domains, health, and logs.
3. Reuse projects/services and add only missing configuration.
4. Store secrets in Zeabur variables or approved vault references; never print values.
5. Deploy a reviewed commit or immutable image after tests pass.
6. Verify build, startup, readiness, logs, DNS/TLS, API behavior, dependencies, and rollback.

## Guardrails

Require confirmation before production promotion, domain changes, destructive scaling, database/volume deletion, paid upgrades, or secret/security changes. Never let platforms compete for a hostname, or claim success from a green build alone. Avoid duplicate projects, services, domains, and variables.
