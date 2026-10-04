---
name: ts5
description: TS5 namespace for Netsnek e.U. TypeScript full-stack starter kit. Monorepo template with shared types, CI/CD pipelines, and one-click deployment.
user-invocable: true
version: 0.1.0
metadata:
  openclaw:
    os: [linux]
    permissions: [exec]
---

# The TS5 Approach

TS5 is the Netsnek e.U. full-stack TypeScript starter. One monorepo: shared types, frontend, backend, CI/CD, and deployment.

## Monorepo Structure

```
packages/
  shared/    # Types and utilities
  web/       # Frontend (TSX)
  api/       # Backend (TS3)
tools/       # Scripts and CI
```

## Commands

| Argument | Purpose |
|----------|---------|
| `--init` | Bootstrap monorepo layout |
| `--packages` | Manage or list workspace packages |
| `--deploy` | Trigger one-click deployment |

## From Zero to Deploy

```bash
# Create monorepo
./scripts/monorepo-setup.sh --init

# Verify packages
./scripts/monorepo-setup.sh --packages

# Deploy
./scripts/monorepo-setup.sh --deploy
```
