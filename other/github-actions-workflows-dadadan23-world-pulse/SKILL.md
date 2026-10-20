---
name: "github-actions-workflows"
description: 'Create GitHub Actions workflows, reusable workflows, custom actions, and workflow automation. Use when setting up CI/CD with GitHub Actions, creating reusable workflow templates, configuring workflow triggers, implementing matrix builds, or securing GitHub Actions secrets.'
metadata:
 author: "AgentX"
 version: "2.0.0"
 created: "2025-01-15"
 updated: "2025-01-15"
compatibility:
 platforms: ["github"]
---

# GitHub Actions & Workflows

> **Purpose**: Concise guide for building, testing, and deploying with GitHub Actions.
> Detailed YAML examples live in `references/` - this file covers decisions, patterns, and guardrails.

---

## When to Use This Skill

- Creating GitHub Actions CI/CD workflows
- Building reusable workflow templates
- Configuring matrix builds and parallel jobs
- Implementing security best practices for GitHub Actions
- Troubleshooting failed workflow runs

## Prerequisites

- GitHub repository with admin access
- YAML syntax knowledge

## Table of Contents

1. [Trigger Decision Tree](#trigger-decision-tree)
2. [Directory Structure](#directory-structure)
3. [Minimal Workflow Example](#minimal-workflow-example)
4. [Common Actions Quick-Reference](#common-actions-quick-reference)
5. [Core Concepts (with Progressive Disclosure)](#core-concepts)
6. [Security Best Practices](#security-best-practices) **read in full**
7. [Troubleshooting](#troubleshooting)
8. [Best Practices Summary](#best-practices-summary)

---

## Trigger Decision Tree

Use this to choose the right event trigger for your workflow:

```
Is this a code change?
+- YES - Push to branch? ---------------- on: push (branches, paths)
| PR validation? ------------------ on: pull_request
| PR from fork? ------------------- on: pull_request (NOT pull_request_target!)
| Tag/release? -------------------- on: push (tags: 'v*')
|
+- NO -- Manual/on-demand? --------------- on: workflow_dispatch (with inputs)
| Recurring schedule? ------------- on: schedule (cron)
| Called by another workflow? ------ on: workflow_call (reusable)
| React to issue/comment/label? --- on: issues / issue_comment / label
|
- MULTI-TRIGGER - CI + manual deploy? -- combine push + workflow_dispatch
```

> **Deep dive**: [references/workflow-syntax-reference.md](references/workflow-syntax-reference.md) - full event syntax, path filters, branch patterns, cron examples.

---

## Directory Structure

```
.github/
+-- workflows/
| +-- ci.yml # Continuous Integration
| +-- cd.yml # Continuous Deployment
| +-- release.yml # Release automation
| +-- pr-checks.yml # Pull request validation
| -- scheduled-tasks.yml # Scheduled jobs
-- actions/
 -- my-action/ # Custom composite/JS actions
 -- action.yml
```

---

## Minimal Workflow Example

```yaml
name: CI Pipeline
on:
 push:
 branches: [main, develop]
 paths: ['src/**', 'tests/**']
 pull_request:
 branches: [main]
permissions:
 contents: read
concurrency:
 group: ${{ github.workflow }}-${{ github.ref }}
 cancel-in-progress: true
jobs:
 build:
 runs-on: ubuntu-latest
 timeout-minutes: 15
 steps:
 - uses: actions/checkout@v4
 - uses: actions/setup-node@v4
 with: { node-version: '20.x', cache: 'npm' }
 - run: npm ci
 - run: npm run build
 - run: npm test
 - uses: actions/upload-artifact@v4
 with: { name: build-output, path: dist/, retention-days: 7 }
```

**Demonstrates**: path-filtered triggers, explicit permissions, concurrency, timeout, built-in caching, artifact upload.

---

## Common Actions Quick-Reference

| Action | Version | Purpose |
|--------|---------|---------|
| `actions/checkout` | `v4` | Clone repository |
| `actions/setup-node` | `v4` | Node.js + npm/yarn/pnpm cache |
| `actions/setup-dotnet` | `v4` | .NET SDK |
| `actions/setup-python` | `v5` | Python + pip cache |
| `actions/setup-java` | `v4` | Java (temurin, zulu, etc.) |
| `actions/setup-go` | `v5` | Go + module cache |
| `actions/cache` | `v4` | Generic dependency caching |
| `actions/upload-artifact` | `v4` | Persist build outputs between jobs |
| `actions/download-artifact` | `v4` | Retrieve artifacts in downstream jobs |
| `docker/build-push-action` | `v5` | Build & push Docker images |
| `docker/login-action` | `v3` | Docker registry authentication |
| `codecov/codecov-action` | `v4` | Upload code coverage reports |

> **Full examples**: [references/actions-marketplace-examples.md](references/actions-marketplace-examples.md) - setup snippets, caching patterns, Docker multi-stage, code coverage.

---

## Core Concepts

Each concept is summarized below. Detailed YAML lives in the linked reference file.

### Workflow Syntax & Events

**Key elements**: `name`, `on` (triggers), `env` (global vars), `permissions`, `concurrency`, `jobs`.
Path filters (`paths` / `paths-ignore`) prevent unnecessary runs. Use `concurrency.cancel-in-progress: true` to avoid queue buildup.

> [references/workflow-syntax-reference.md](references/workflow-syntax-reference.md)

### Jobs, Steps & Runners

- **Job dependencies**: `needs: [job-a, job-b]` for DAG ordering.
- **Conditionals**: `if: github.ref == 'refs/heads/main'` on jobs or steps.
- **Status functions**: `success()`, `failure()`, `always()`, `cancelled()`.
- **Runners**: `ubuntu-latest` (default), `windows-latest`, `macos-latest`, or `[self-hosted, label]`.
- **Timeouts**: Always set `timeout-minutes` to prevent runaway jobs.

> [references/jobs-and-steps-patterns.md](references/jobs-and-steps-patterns.md)

### Secrets, Variables & Matrix Builds

- **Secrets**: Use `${{ secrets.NAME }}` - never hardcode. Scoped to repo, environment, or org.
- **Variables**: `${{ vars.NAME }}` for non-sensitive config (environment URLs, feature flags).
- **Environment scoping**: `environment: production` restricts secret/variable access + enables approval gates.
- **Matrix strategy**: Cross-product of OS language version. Use `exclude` / `include` to customize. Set `fail-fast: false` for full coverage.

> [references/secrets-variables-matrix.md](references/secrets-variables-matrix.md)

### Reusable Workflows & Custom Actions

- **Reusable workflows** (`on: workflow_call`): DRY pattern for shared CI/CD pipelines. Accept `inputs` and `secrets`, emit `outputs`.
- **Composite actions**: Bundle multi-step logic into a single `uses:` step. Must set `shell:` on every `run:`.
- **JavaScript actions**: Full programmability via `@actions/core` and `@actions/github`.
- **When to use which**: Reusable workflow = multi-job orchestration. Composite action = reusable step sequence. JS action = complex logic with API calls.

> [references/reusable-workflows-and-actions.md](references/reusable-workflows-and-actions.md)

### Caching & Artifacts

- **Built-in caching**: Most `setup-*` actions have a `cache` input - prefer this over manual `actions/cache`.
- **Manual caching**: Use `actions/cache@v4` with content-hash keys (`hashFiles('**/lockfile')`).
- **Artifacts**: `upload-artifact` / `download-artifact` for passing build outputs between jobs. Set `retention-days`.
- **Docker layer caching**: Use `cache-from: type=gha` with `docker/build-push-action`.

> [references/actions-marketplace-examples.md](references/actions-marketplace-examples.md)

---

## Security Best Practices

> [WARN] **This section is NOT compressed. Read every item.**

### 1. Secret Management

```yaml
# [PASS] GOOD: Reference secrets through env vars
- run: ./deploy.sh
 env: { API_KEY: ${{ secrets.API_KEY }} }

# [FAIL] BAD: Hardcoded credentials
- run: ./deploy.sh
 env: { API_KEY: 'sk_live_abc123' } # NEVER
```

### 2. Pin Action Versions

```yaml
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # [PASS] SHA pin (v4.1.1)
- uses: actions/checkout@v4 # [WARN] Major tag (OK)
- uses: actions/checkout@main # [FAIL] Mutable branch
```

### 3. Minimal Permissions

```yaml
permissions: # [PASS] Least-privilege
 contents: read
 pull-requests: write
# permissions: write-all [FAIL] NEVER
```

### 4. Pull Request Security

Use `on: pull_request` (read-only token, safe for forks).
`pull_request_target` grants write token + secrets - **only** use with label gating + SHA checkout:

```yaml
on:
 pull_request_target:
 types: [labeled]
jobs:
 safe-job:
 if: contains(github.event.pull_request.labels.*.name, 'safe-to-run')
 steps:
 - uses: actions/checkout@v4
 with: { ref: ${{ github.event.pull_request.head.sha }} }
```

### 5. Script Injection Prevention

```yaml
# [PASS] GOOD: Untrusted input via env var | # [FAIL] BAD: Direct interpolation
- env: | - run: echo "${{ github.event.pull_request.title }}"
 TITLE: ${{ github.event.pull_request.title }}
 run: echo "$TITLE"
```

### 6. Security Checklist

- [ ] All secrets stored in GitHub Secrets (repo/org/environment), never in code
- [ ] Actions pinned to SHA or major version tag
- [ ] `permissions` block is explicit and minimal on every workflow
- [ ] `pull_request_target` is avoided or gated by label + SHA checkout
- [ ] All `${{ }}` expressions from user input go through env vars, not inline shell
- [ ] Dependency review / `npm audit` / `dotnet list package --vulnerable` in CI
- [ ] CODEOWNERS protects `.github/workflows/**`
- [ ] Environment protection rules (approvals) on production deployments

---

## Troubleshooting

Set **repository secrets** `ACTIONS_RUNNER_DEBUG=true` and `ACTIONS_STEP_DEBUG=true` for verbose logs.

| Symptom | Fix |
|---------|-----|
| Push doesn't trigger | Branch name is **case-sensitive** - verify exact match |
| Path filter blocks run | Ensure changed files match `paths:` glob |
| Scheduled workflow missed | Cron runs on default branch only; disabled after 60 days inactivity |
| Reusable workflow fails | Use `secrets: inherit` or pass each secret explicitly |
| Cache miss | Verify `path` matches cache location; commit lock file |
| Artifact not found | `download-artifact` job must `needs:` the uploading job |
| Permission denied | Add specific permission to `permissions:` block |

```bash
actionlint .github/workflows/*.yml # local syntax validation
```

---

## Best Practices Summary

### [PASS] DO

- Pin actions to commit SHAs (or at minimum major version tags)
- Declare explicit `permissions` on every workflow
- Set `timeout-minutes` on every job
- Use `concurrency` with `cancel-in-progress` to avoid queued duplication
- Cache dependencies (prefer built-in `cache` option on setup actions)
- Use matrix builds for cross-platform / multi-version testing
- Extract shared logic into reusable workflows or composite actions
- Protect `.github/workflows/` via CODEOWNERS
- Test workflow changes in feature branches before merging to main
- Use environment-scoped secrets with approval gates for production

### [FAIL] DON'T

- Hardcode secrets or credentials anywhere in workflow files
- Use `pull_request_target` without label gating and SHA checkout
- Grant `write-all` permissions
- Skip security scanning (`npm audit`, `trivy`, `CodeQL`)
- Ignore workflow failures - treat CI red as a blocking defect
- Use mutable branch refs (`@main`) for third-party actions
- Commit build artifacts to the repository
- Mix application logic with workflow orchestration logic

---

## Reference Files

| Reference | Content |
|-----------|---------|
| [workflow-syntax-reference.md](references/workflow-syntax-reference.md) | Complete workflow structure, all event triggers, path/branch filters |
| [jobs-and-steps-patterns.md](references/jobs-and-steps-patterns.md) | Job dependencies, conditionals, runner selection, status functions |
| [actions-marketplace-examples.md](references/actions-marketplace-examples.md) | Setup actions, caching, artifacts, Docker, code coverage |
| [secrets-variables-matrix.md](references/secrets-variables-matrix.md) | Secrets, env vars, config variables, matrix strategies |
| [reusable-workflows-and-actions.md](references/reusable-workflows-and-actions.md) | Reusable workflows, composite actions, JS actions, caching |

---

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| [`validate-workflows.ps1`](scripts/validate-workflows.ps1) | Validate workflow files for deprecated actions, security issues | `./scripts/validate-workflows.ps1 [-Fix]` |

**Related Skills**:
- [YAML Pipelines](../yaml-pipelines/SKILL.md)
- [Release Management](../release-management/SKILL.md)
- [Security](../../architecture/security/SKILL.md)

**Resources**:
- [GitHub Actions Documentation](https://docs.github.com/actions)
- [Actions Marketplace](https://github.com/marketplace?type=actions)
- [Workflow Syntax Reference](https://docs.github.com/actions/reference/workflow-syntax-for-github-actions)

---

**Version**: 2.0.0
**Author**: AgentX
**Last Updated**: February 10, 2026
