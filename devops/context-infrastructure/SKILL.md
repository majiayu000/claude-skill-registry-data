---
name: context-infrastructure
description: |
  Railway deployment, CI/CD workflows, GitHub Actions, and smoke tests.
  Handles Railway configuration, GitHub Actions workflows, deployment automation, and health checks.
  Use when working with deployment, CI configuration, Railway setup, or infrastructure automation,
  or when user mentions Railway environments, GitHub Actions, deployment issues, CI failures,
  "Build failed" errors, smoke test errors, CI/CD pipelines, Docker configuration, or devops workflows.
tags: [infra, deployment, ci-cd, railway]
---

# Infrastructure

Navigate Railway deployment, GitHub Actions workflows, and infrastructure config.

## Overview

Railway for deployment, GitHub Actions for CI/CD. See `docs/deployment/RAILWAY.md`.

## Railway Configuration

- `railway.toml` (root) - Project-level config
- `backend/railway.toml` - Backend service
- `frontend/railway.toml` - Frontend service

## CI/CD Workflows

- `.github/workflows/*.yml` - All GitHub Actions
- `.github/workflows/deploy.yml` - Deployment workflow (if exists)
- `.github/workflows/test.yml` - Test workflow (if exists)

## Docker

- `Dockerfile` (root) - Docker configuration (if exists)
- `docker-compose*.yml` - Docker Compose (if exists)

## Smoke Tests

- `backend/smoke_endpoints.py` - Backend health checks
- `frontend/e2e-smoke/*.spec.ts` - Frontend smoke tests

## Scripts

- `scripts/test-railway-setup.sh` - Railway testing
- `scripts/db-commands/db-verify.sh` - Database verification

## Documentation

- **Internal**: `docs/deployment/RAILWAY.md`

## Related Areas

- See `context-testing-infrastructure` for smoke test patterns
- See `context-database-schema` for migration deployment
