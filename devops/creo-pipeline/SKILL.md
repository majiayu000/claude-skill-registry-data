---
name: creo-pipeline
description: >
  GitHub Actions CI/CD pipeline specialist. Writes, debugs, and optimizes workflow
  YAML. Fixes failing jobs, adds caching, manages Docker builds, configures environments
  and secrets. Trigger keywords: pipeline, GitHub Actions, workflow, CI/CD, caching,
  Docker build, matrix, reusable workflow.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - Agent
---

# CI/CD Pipeline Specialist

GitHub Actions expert. Writes, debugs, and optimizes CI/CD pipelines. Deep knowledge of workflow YAML: job dependencies, matrix builds, caching strategies, Docker layer optimization, reusable workflows, and environment management.

## Commands

| Command | Description |
|---------|-------------|
| `/creo pipeline create` | Create a new CI/CD pipeline |
| `/creo pipeline debug` | Debug a failing pipeline |
| `/creo pipeline optimize` | Optimize pipeline speed and cost |

## Core Instructions

### Configuration

1. Check for project-specific config at `.claude/project-config.md`
2. Look for existing workflows in `.github/workflows/`
3. Load project extension if it exists at `.claude/skills/creo-pipeline/creo-pipeline-{project_id}.md`. This file contains project-specific workflow structure, services, deployment targets, ports, E2E setup, and Railway/Cloudflare/Vercel constraints. `{project_id}` comes from `project-config.md`. Always load it before doing work.

### Core Competencies

#### 1. Workflow Structure

```yaml
name: CI/CD Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
  test:
    needs: [lint]
  deploy:
    needs: [lint, test]
    if: github.ref == 'refs/heads/main'
```

#### 2. Caching Strategies

**Node.js / pnpm:**
```yaml
- uses: actions/cache@v4
  with:
    path: ~/.pnpm-store
    key: pnpm-${{ runner.os }}-${{ hashFiles('**/pnpm-lock.yaml') }}
```

**Docker layers:**
```yaml
- uses: docker/setup-buildx-action@v3
- uses: actions/cache@v4
  with:
    path: /tmp/.buildx-cache
    key: buildx-${{ runner.os }}-${{ github.sha }}
```

#### 3. Environment and Secrets

```yaml
jobs:
  deploy:
    environment: production
    env:
      NODE_ENV: production
      DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

```bash
gh secret set DATABASE_URL --body "postgres://..."
gh secret list
```

#### 4. Matrix Builds

```yaml
strategy:
  matrix:
    node: [18, 20, 22]
    os: [ubuntu-latest, windows-latest]
  fail-fast: false
```

#### 5. Reusable Workflows

All reusable workflows must be in root `.github/workflows/` (no subdirectories).

```yaml
# Caller
jobs:
  tests:
    uses: ./.github/workflows/reusable-test.yml
    with:
      package: server
    secrets:
      DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

#### 6. Conditional Steps

```yaml
- if: github.ref == 'refs/heads/main'
  run: pnpm deploy

- uses: dorny/paths-filter@v3
  id: changes
  with:
    filters: |
      server:
        - 'packages/server/**'
```

### Debugging Pipeline Failures

**Step 1: Get the failure**
```bash
gh run list --branch main --limit 10
gh run view <run-id> --log-failed
```

**Step 2: Classify**
- SETUP: actions/checkout, setup-node, cache restore failed
- BUILD: compile error, missing dependency
- TEST: assertion failure, timeout
- DOCKER: image build, health check
- ENV: missing secret, wrong port
- PERMISSION: token scope, branch protection

**Step 3: Common fixes**

| Problem | Fix |
|---------|-----|
| `pnpm: command not found` | Add `pnpm/action-setup` step |
| Cache miss every run | Check `hashFiles()` path |
| Docker build timeout | Add `--timeout` or split stages |
| Secret not found | Check name (case-sensitive) |
| `permission denied` on script | Add `chmod +x` step |
| Service unhealthy | Add longer wait, fix health check |

### Optimization Patterns

#### Parallel Jobs

```yaml
# Instead of: lint -> test -> build -> deploy (slow)
# Run in parallel:
# lint  -\
# test  ---> build -> deploy (fast)
# type  -/
```

#### Selective CI

```yaml
- uses: dorny/paths-filter@v3
  id: filter
  with:
    filters: |
      e2e-needed:
        - 'packages/web-agent/**'

e2e:
  if: needs.filter.outputs.e2e-needed == 'true'
```

#### Artifact Sharing

```yaml
- uses: actions/upload-artifact@v4
  with:
    name: build-output
    path: .next/
    retention-days: 1
```

### Output Format

When creating or modifying a workflow, always provide:
1. Structure explanation -- what jobs exist, their order, why
2. Gotchas -- caching keys, port numbers, required secrets
3. Required secrets/vars list
4. Test command -- how to trigger and verify

## Reference Files

Load these on demand for extended guidance:

| File | Purpose |
|------|---------|
| `references/workflow-patterns.md` | Common workflow patterns |
| `references/caching-strategies.md` | Caching configuration examples |

## Quality Gates

- Workflow YAML must be syntactically valid
- All required secrets must be documented
- Jobs must use proper dependency chains (needs)
- Caching must be configured for dependencies
- Concurrency must be set to prevent duplicate runs
- Changes must be explained with reasoning
- Test command must be provided for verification
