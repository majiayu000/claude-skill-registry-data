---
name: working-with-github-actions
description: "Use when building, configuring, debugging, or optimizing GitHub Actions CI/CD workflows. Covers workflow YAML syntax, event triggers, job orchestration, matrix builds, reusable workflows, composite actions, secrets and variables, artifact and cache management, OIDC-based cloud deployments, self-hosted runners, and security hardening. Also covers adjacent tooling: release-please, dependabot, CodeQL, labeler, and stale management. Invoke whenever the user mentions GitHub Actions, .github/workflows, CI/CD, workflow files, action versions, self-hosted runners, OIDC cloud deployments, or wants to automate anything that runs on GitHub push/PR/schedule events."
metadata:
  last_updated: "2026-06-06"
---

# Working with GitHub Actions

This skill provides reference docs, a cookbook of real-world patterns, and best practices for GitHub Actions.

## Quick Reference

| Task | Reference file |
|---|---|
| Workflow YAML syntax | `references/workflow-syntax.md` |
| Events / triggers | `references/triggers.md` + `references/trigger-a-workflow.md` |
| Expressions | `references/expressions.md` |
| Contexts (github, env, secrets…) | `references/contexts.md` |
| Runners (hosted) | `references/runners.md` |
| Larger runners | `references/larger-runners.md` |
| Self-hosted runners | `references/self-hosted-runners.md` |
| Choose runner for a job | `references/choose-runner.md` |
| Caching dependencies | `references/caching.md` |
| Artifacts | `references/artifacts.md` |
| Matrix builds | `references/matrix-strategy.md` |
| Reusable workflows | `references/reusable-workflows.md` |
| Custom / composite actions | `references/custom-actions.md` |
| Secrets | `references/secrets.md` + `references/use-secrets.md` |
| Variables | `references/variables-ref.md` + `references/use-variables.md` |
| GITHUB_TOKEN / permissions | `references/github-token.md` |
| Environments and approvals | `references/manage-environments.md` + `references/deployments-and-environments.md` |
| Controlling deployments | `references/control-deployments.md` |
| OIDC overview | `references/oidc-concepts.md` |
| OIDC for cloud providers | `references/oidc-cloud.md` |
| OIDC for AWS | `references/oidc-aws.md` |
| OIDC for GCP | `references/oidc-gcp.md` |
| OIDC for Azure | `references/oidc-azure.md` |
| Security: script injection | `references/script-injections.md` |
| Security: compromised runners | `references/compromised-runners.md` |
| Concurrency control | `references/concurrency.md` + `references/control-concurrency.md` |
| Conditional jobs | `references/control-jobs-with-conditions.md` |
| Workflow commands (::set-output etc) | `references/workflow-commands.md` |
| Current action versions | `references/action-versions.md` |

## Cookbook

Real-world, copy-paste patterns:

| Pattern | File |
|---|---|
| TypeScript/Node.js full CI (pnpm + biome + vitest + build) | `references/cookbook-typescript-node-ci.md` |
| Composite action: reusable setup step | `references/cookbook-composite-action-setup.md` |
| Release Please + npm publish + docs deploy | `references/cookbook-release-please-npm.md` |
| CodeQL security scanning | `references/cookbook-codeql.md` |
| Dependabot for npm and GitHub Actions | `references/cookbook-dependabot.md` |
| PR labeler from file paths | `references/cookbook-labeler.md` |
| Stale issue and PR management | `references/cookbook-stale.md` |
| Python CI (uv + pytest + coverage) | `references/cookbook-python-ci.md` |
| Docker build and push (GHCR) | `references/cookbook-docker-build-push.md` |
| Deploy to AWS via OIDC (no stored secrets) | `references/cookbook-deploy-aws-oidc.md` |
| Reusable workflow: call-and-share pattern | `references/cookbook-reusable-workflow.md` |
| Monorepo: path-filtered jobs | `references/cookbook-monorepo-path-filter.md` |

## Key Concepts

### Workflow structure

A workflow file lives in `.github/workflows/*.yml`. Minimal anatomy:

```yaml
name: CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "hello"
```

### Action pinning

Always pin actions to a full SHA for production workflows, or a major version tag for convenience:

```yaml
# Safest: full SHA (immune to tag moves)
uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2

# Convenient: major version (updates on patch/minor automatically)
uses: actions/checkout@v4
```

Check `references/action-versions.md` for current latest versions of commonly used actions.

### Secrets vs variables vs environments

- **Secrets** (`secrets.MY_SECRET`): encrypted, never logged, unavailable to forked PR workflows by default
- **Variables** (`vars.MY_VAR`): non-sensitive config values, visible in logs
- **Environment secrets/vars**: scoped to a named deployment environment (with optional approval gate)

### GITHUB_TOKEN permissions

Default permissions vary by repo setting. Always declare explicit minimal permissions:

```yaml
permissions:
  contents: read
  pull-requests: write
```

For OIDC cloud auth, add `id-token: write`.

### Concurrency

Prevent overlapping runs on the same branch:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

Use `cancel-in-progress: false` for release/deploy jobs where partial runs are dangerous.

## Cross-References

- `git-github-workflows` skill — router for any git/GitHub task (not CI/CD)
- `working-with-github` skill — gh CLI, REST/GraphQL APIs, PRs, releases, tokens, and the Dependabot/CodeQL **security config** (this skill keeps the Dependabot/CodeQL **workflow** cookbooks)
- `working-with-git` skill — raw git: history rewriting, bisect, conflicts, recovery
- `developing-for-github` skill — GitHub Apps, webhooks, Octokit SDKs
- `deploy` skill — deployment orchestration across providers
