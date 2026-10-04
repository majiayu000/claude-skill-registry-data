---
model_tier: medium
name: github-ci
description: "When working with GitHub Actions — workflow YAML, quality gates, test matrices, deployment triggers, reusable workflows — even when the user just says 'my CI is failing' or 'add a check'."
domain: devops
workspaces:
  - engineering
packs:
  - engineering-base
---

# github-ci

## When to use

Use this skill when working with GitHub Actions workflows, CI pipeline configuration, or understanding the automated quality and deployment process.

## Procedure: Modify CI workflows

1. Read `.github/workflows/` to understand the full pipeline.
2. Check `AGENTS.md` for quality tool commands and testing setup.
3. Read `commands/fix/ci.md` for CI failure debugging workflow.

## Workflow overview

### Quality pipeline (`quality-tests.yml`)

Triggered on: `pull_request` to `main`, `workflow_dispatch`

Read `.github/workflows/` to discover the actual job matrix. Common patterns:

- PHP version is **extracted from Dockerfile** (`ARG PHP_VERSION`), not hardcoded.
- Static analysis may run on larger runners for memory.
- Tests run in **parallel** with a matrix strategy per test suite.
- Branch comparison for dead code and API docs.

### Deployment workflows

| Workflow | Trigger | Environment |
|---|---|---|
| `deploy-review.yaml` | PR with `review-env` label | Review (ephemeral) |
| `deploy-sta.yaml` | Push to `main` | Stage |
| `deploy-pro.yaml` | Tag `release-X.Y.Z` or schedule (Mon 8AM) | Production |
| `deploy.yml` | After "Static Code Analysis" succeeds on `main` | Envoyer trigger |
| `module-deploy.yaml` | Reusable workflow (called by others) | Parameterized |

### Other workflows

| Workflow | Purpose |
|---|---|
| `pr-review-gate.yaml` | Points-based review system (see `code-review` skill) |
| `destroy-review.yaml` | Cleanup ephemeral review environments |
| `add-labels.yml` | Auto-label PRs |
| `apply-pr-template.yaml` | Apply PR description template |
| `validate-deployment-files.yaml` | Validate AWS deployment configs |
| `template-db-dump.yaml` | Database dump utility |

## Conventions

### Workflow structure

- Use **pinned action versions** with SHA hashes (not tags): `actions/checkout@<sha> # v6.0.2`
- Use **concurrency groups** to prevent duplicate runs: `group: ${{ github.workflow }}-${{ github.ref }}`
- Use **`fail-fast: false`** in matrix strategies for independent job execution.
- Extract shared logic into **reusable workflows** (`module-deploy.yaml` pattern).
- A job with **`container:`** MUST run `git config --global --add safe.directory "$GITHUB_WORKSPACE"` immediately after `actions/checkout` — the checkout is owned by a different UID than the container user, so without it every git-backed step dies with `fatal: detected dubious ownership`.

### Composer auth

Every workflow that installs dependencies needs:
1. `COMPOSER_AUTH` secret validation (check if set, validate JSON).
2. Fallback handling if auth is missing or masked.

### PHP version

- **Never hardcode** the PHP version in workflows.
- Always extract from Dockerfile: `awk -F= '/^ARG PHP_VERSION/ {print $2}' .docker/Dockerfile`
- Pass via job outputs to dependent jobs.

### Runners

Check `.github/workflows/` for the runner types used. Common patterns:
- Standard runners (`ubuntu-latest`) for light jobs.
- Larger or custom runners for heavy jobs (static analysis, tests).
- ARM runners if the project deploys to ARM-based infrastructure.

### Environment variables

- Use `env:` at job level for shared secrets.
- Use `$GITHUB_OUTPUT` for passing data between steps.
- Use `$GITHUB_ENV` for variables needed across multiple steps.

## Debugging CI failures

1. Get the failing run: `GET /repos/{owner}/{repo}/actions/runs?branch={branch}`
2. Get failed jobs: `GET /repos/{owner}/{repo}/actions/runs/{run_id}/jobs`
3. Get logs: `GET /repos/{owner}/{repo}/actions/jobs/{job_id}/logs`
4. Fix locally, verify in container, then push.

See `commands/fix/ci.md` for the full debugging workflow.


## Output format

1. Modified workflow YAML file(s) in `.github/workflows/`
2. Summary of pipeline changes and affected triggers

## Auto-trigger keywords

- GitHub Actions
- CI/CD
- workflow
- pipeline
- quality checks

## Gotcha

- CI workflows run on Ubuntu, not macOS — don't assume macOS-specific tools are available.
- The model forgets to add `--env=testing` to artisan commands in CI — tests will hit the wrong database.
- Secret names are case-sensitive in GitHub Actions — double-check the casing.
- Don't add `continue-on-error: true` to hide failures — fix the actual error.

## Do NOT

- Do NOT use unpinned action versions (e.g., `actions/checkout@v4`).
- Do NOT hardcode PHP versions — always extract from Dockerfile.
- Do NOT add new secrets without documenting them.
- Do NOT change runner types without considering cost and architecture (ARM vs x86).
