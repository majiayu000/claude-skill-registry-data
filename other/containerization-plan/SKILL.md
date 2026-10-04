---
name: containerization-plan
description: Plan containerization for apps, services, jobs, and development environments. Use when Codex is asked to create or review Dockerfiles, container images, compose files, runtime users, build layers, healthchecks, ports, volumes, or container security.
license: MIT
---

# Containerization Plan

## Core Workflow

1. Identify app runtime, build process, target environment, ports, volumes,
   secrets, healthchecks, and deployment constraints.
2. Choose image strategy: base image, multi-stage build, dependency caching,
   non-root user, filesystem layout, and startup command.
3. Define runtime config: env vars, secrets, volumes, network, healthcheck,
   resource limits, and logs.
4. Review size, reproducibility, security, and local development needs.
5. Include build, run, smoke test, and publish steps.
6. Flag risks before creating production images.

## Safety Rules

- Do not bake secrets, tokens, private keys, or local paths into images.
- Do not run containers as root by default when a non-root runtime is practical.
- Do not publish images or push registries without explicit approval.

## Deliverable Shape

For containerization plans, provide:

- Runtime and target environment
- Image build strategy
- Runtime configuration
- Security and secret handling
- Healthcheck and logging
- Build/run/test commands
- Registry and release notes
- Open risks

## References

- Read `references/containerization-plan-checklist.md` when planning or
  reviewing container setup.
