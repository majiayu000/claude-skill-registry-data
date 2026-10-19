---
name: github-actions-ci
description: Use when setting up CI/CD with GitHub Actions, writing or fixing a workflow YAML, running tests or lint on pull requests, caching dependencies, deploying on push, or debugging a failing or slow GitHub Actions run.
---

# GitHub Actions CI

## Overview

A good pipeline runs the same checks a developer runs locally, fails fast with a clear message, and finishes in minutes. Build it from the project's real commands and keep it secure by default.

## Method

1. **Discover the checks** the project already has: install, lint, typecheck, test, build commands from `package.json`, `Makefile`, `pyproject.toml`, `pom.xml`, `go.mod`. Note runtime versions and services the tests need (Postgres, Redis).
2. **Write `.github/workflows/ci.yml`** from the template below. Add a deploy workflow only if asked, and only on `main` after CI passes.
3. **Validate** with `actionlint` if available. Push to a branch and watch the run: `gh run watch`.
4. **Debugging a failing run:** `gh run view <id> --log-failed`, reproduce the failing command locally with the same runtime version, compare environment variables and service versions.

## Template

```yaml
name: CI

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  check:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version-file: .nvmrc
          cache: npm
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm test
      - run: npm run build
```

For other stacks swap the setup step: `actions/setup-python@v5` (`cache: pip`), `actions/setup-java@v4` (`cache: maven`), `actions/setup-go@v5` (cache built in).

Services for integration tests:

```yaml
    services:
      postgres:
        image: postgres:16
        env: { POSTGRES_PASSWORD: postgres }
        ports: ["5432:5432"]
        options: >-
          --health-cmd pg_isready --health-interval 5s --health-retries 10
```

## Rules

| Rule | Why |
|---|---|
| Least privilege: top-level `permissions: contents: read`, widen per job only | Limits damage from a compromised step |
| Secrets via `${{ secrets.X }}` only, never echoed; no secrets on `pull_request` from forks | Prevents leaks |
| Pin third-party actions to a full commit SHA; official `actions/*` to a major version | Supply-chain safety |
| Cache dependencies through the setup action | Faster runs |
| `concurrency` with cancel-in-progress | No queue of outdated runs |
| `timeout-minutes` on every job | Hung jobs do not burn minutes |
| Matrix only where it matters (supported runtime versions, OSes) | Each entry costs time |

## Common mistakes

- CI runs commands that do not exist locally, so failures cannot be reproduced.
- Using `npm install` instead of `npm ci`.
- `pull_request_target` with checkout of the PR code: gives untrusted code access to secrets.
- Deploying from a workflow that does not depend on tests passing.
- Hiding failures with `continue-on-error: true` or `|| true`.

---

Made by **Wageesha Tripathi** · [LinkedIn](https://www.linkedin.com/in/wst2002/) · [Email](mailto:tripathiwageesha2002@gmail.com) · [More skills](https://github.com/WST2002/claude-code-skills)
