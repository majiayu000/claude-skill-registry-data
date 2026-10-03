---
name: ls-docker-best-practices
description: Guide Dockerfile, Compose, and container best practices. Use for images,
  builds, runtime security, caching, volumes, networking, and deploy readiness.
metadata:
  version: '1.0'
---

# Docker

Use this skill when working on Docker tasks.

## Workflow

- Inspect base image, build context, multi-stage use, dependency cache, user, exposed ports, volumes, and health checks.
- Avoid baking secrets into images, layers, args, logs, or Compose files.
- Validate image size, rebuild determinism, non-root runtime, signal handling, and environment-specific config.

## Boundaries

- Inspect the target repository before making changes.
- Prefer existing project patterns, declared package managers, and documented validation commands.
- Do not expose secrets, credentials, private user data, or production account identifiers in source, examples, or logs.
- When external APIs or current vendor behavior matter, verify against official docs before implementation.

## Provenance

- Source classification: `official-docs-reference`
- This is a LocalSetup-native skill written from project workflow requirements and public/official documentation routing.
