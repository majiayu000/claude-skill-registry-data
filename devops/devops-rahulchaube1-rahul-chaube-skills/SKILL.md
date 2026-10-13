---
name: devops
description: Deployment pipelines, Docker configurations, and container registries.
---

# Devops

Deployment pipelines, Docker configurations, and container registries.

## Core Guidelines

- **Multi-stage Builds**: Use multi-stage Dockerfiles to keep image footprints small and secure.
- **Cache Layers**: Order Dockerfile commands to maximize build cache effectiveness.
- **Linting**: Lint configurations before push.
