---
name: devops-deployment-automation
description: Dockerization, CI/CD pipelines (GitHub Actions), deployment targets (Vercel, AWS, Railway), and environment management. Use when containerizing apps, setting up automated pipelines, or configuring production deployments.
version: "1.0.0"
verified_date: 2026-04-30
category: infra
---

# DevOps & Deployment Automation

## Purpose
Provide production-grade patterns for containerization, automated CI/CD pipelines, and deployment configuration. This skill bridges the gap between "it works locally" and "it runs reliably in production."

## When to Use This Skill
Use when:
- Containerizing an application with Docker
- Setting up CI/CD pipelines (GitHub Actions, GitLab CI)
- Configuring deployment to Vercel, AWS, Railway, Fly.io
- Managing environment variables across dev/staging/production
- Debugging deployment failures or build pipeline issues

Do NOT use when:
- Writing application logic (use backend/frontend agents)
- The project will only ever run locally

## Phase 1: Containerization (Docker)

### Dockerfile Rules
1. **Multi-stage builds** — separate build deps from runtime
2. **Layer ordering** — least-frequently-changed layers first (OS → deps → code)
3. **No secrets in images** — never `COPY .env` or use `ARG` for secrets
4. **.dockerignore** — always include: `node_modules`, `.git`, `.env*`, `dist`, `coverage`
5. **Health checks** — add `HEALTHCHECK` for orchestrated environments
6. **Pin versions** — `node:20.12-alpine`, not `node:latest`
7. **Non-root user** — always `adduser` and `USER` directive

## Phase 2: CI/CD Pipelines (GitHub Actions)

### Pipeline Order
**Lint → Typecheck → Test → Build → Deploy** — always this order.

### Pipeline Rules
1. **Fail fast** — cancel in-progress runs on new commits
2. **Cache dependencies** — use `actions/cache` or built-in cache
3. **Secrets via GitHub Secrets** — never hardcode credentials in workflow files
4. **Branch protection** — require CI to pass before merging to main
5. **Concurrency control** — prevent parallel deploys to same environment

## Phase 3: Deployment Targets

| Platform | Best For | Key Feature |
|----------|----------|-------------|
| Vercel | Next.js / Static | Zero-config, preview deploys |
| Railway | Full-stack | Built-in Postgres, Nixpacks |
| AWS ECS | Production scale | Container orchestration |
| Fly.io | Edge APIs | Global distribution |

## Phase 4: Environment Management

### Hierarchy
```
.env.example          ← committed, documents required variables (no values)
.env.local            ← local dev, never committed
.env.test             ← test env, may be committed if no secrets
.env.production       ← NEVER committed, managed via platform
```

### Rules
1. `.env.example` is mandatory — committed with variable names, no secret values
2. `.env` files are gitignored — verify `.gitignore` includes `.env*`
3. Validate at startup — use Zod or `envalid` to validate required env vars
4. No optional secrets — crash on startup if a required secret is missing

## Behavior Rules
1. **Never embed secrets in code, Dockerfiles, or CI configs.**
2. **Always include `.dockerignore`** alongside any Dockerfile.
3. **Always include `.env.example`** when env vars are required.
4. **Deployments must be reproducible** — same commit = same deployment.

## Output Format / Delivery
- Output is deployment config code (Dockerfiles, YMLs) and step-by-step CI/CD pipeline logic.

## Safety Guardrails
1. **Secret Exposure Patch**: Verify no secret values in plain text. Use `${{ secrets.NAME }}`.
2. **Production Deploy Patch**: Deployment steps must have `if:` condition restricting to main branch.
3. **Docker Security Patch**: Use non-root users, never copy `.env` into images.
4. **Self-Rejection Clause**: If deployment target is unknown, **ABORT OUTPUT** and emit: *"REJECTED: Cannot generate deployment config without knowing the target platform."*

## Maintenance Notes
- Created 2026-04-30 as part of the Operational Gap analysis.
- Complements `backend-dev-guidelines` with infrastructure to ship.
- Complements `testing-quality-engineering` with pipeline to enforce tests.
