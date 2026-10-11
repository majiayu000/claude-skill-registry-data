---
name: ci-cd-repair
description: Diagnose and fix automated CI/CD pipeline failures. Use when Codex needs to investigate GitHub Actions, GitLab CI, Bitbucket Pipelines, Azure Pipelines, CircleCI, Vercel, Render, Railway, Fly.io, or other test, lint, format, build, package, Docker, artifact, release, or deployment workflows that fail because of logs, workflow YAML, scripts, dependency installation, runtime versions, caches, working directories, monorepo paths, environment variables, secrets, permissions, artifacts, deployment steps, or local-vs-CI differences.
---

# CI/CD Repair

Use this skill when an automated pipeline fails or behaves incorrectly and the fix must be based on logs, workflow configuration, project commands, and deployment safety.

## Core Rule

Diagnose the failing job from evidence before editing. Identify the first meaningful failure, connect it to workflow configuration or project code, apply the smallest safe fix, and verify with local equivalents or a rerun plan.

## Workflow

1. Identify the pipeline failure:
   - platform, workflow file, event, branch or pull request, job, step, command, exit code, first useful error, expected behavior, and actual behavior
2. Inspect CI/CD configuration:
   - `.github/workflows/*.yml`, `.gitlab-ci.yml`, `bitbucket-pipelines.yml`, `azure-pipelines.yml`, `.circleci/config.yml`, deployment config, package scripts, lockfiles, Docker files, and monorepo paths
3. Classify the failure:
   - trigger, setup, dependency, lint/format, test, build, Docker, environment, service dependency, artifact, deployment, permission, cache, path filter, or timeout/performance issue
4. Compare CI commands with local commands:
   - README/runbook instructions, package manager, package scripts, Makefile targets, Docker Compose commands, documented test/build/deploy commands, and previous working commands
5. Check runtime and tool versions:
   - Node, Python, Java, PHP, Ruby, Go, Flutter, Docker, package manager, framework CLI, and version files such as `.nvmrc`, `.node-version`, `.python-version`, `runtime.txt`, `package.json`, or `pyproject.toml`
6. Check dependency installation and lockfiles:
   - package manager consistency, frozen lockfile behavior, cache keys, install working directory, registry auth, and generated files that must be committed
7. Check working directories and monorepo paths:
   - `working-directory`, `defaults.run.working-directory`, Docker build context, artifact paths, app folders, changed-path filters, and package locations
8. Check environment variables and secrets:
   - `.env.example`, workflow `env`, repository or environment secrets, deployment platform variables, frontend build-time variables, backend runtime variables, and secret scope without printing secret values
9. Check service dependencies:
   - databases, Redis, object storage, browsers, health checks, ports, connection strings, migrations, seed data, and readiness/wait logic for tests
10. Diagnose the relevant failure layer:
   - lint/format, tests, production build, Docker build, artifact upload/download, release publishing, deployment, or post-deploy health check
11. Check workflow permissions and safety gates:
   - minimum token permissions, branch conditions, environment approvals, OIDC/cloud auth, registry permissions, deploy branch rules, and release conditions
12. Inspect cache behavior:
   - lockfile hash keys, package manager cache path, stale dependency risk, Docker layer cache, and whether the cache hides or causes the failure
13. Identify root cause with evidence:
   - cite the log/config mismatch instead of describing only the final failed status
14. Apply the smallest safe fix:
   - command, runtime, install step, lockfile, working directory, env reference, service readiness, artifact path, cache key, permission, Docker context, deployment condition, or test setup fix
15. Verify the repair:
   - run local equivalent commands when possible, validate workflow syntax/config, state whether the hosted pipeline must be rerun, and explain any limits
16. Summarize the pipeline problem, evidence, root cause, fix, files changed, verification, remaining risks, and follow-up.

Read `references/pipeline-repair-checklist.md` for platform files, root-cause patterns, repair checks, verification commands, and the final report format.

## Non-Negotiable Rules

- Do not edit workflow files before inspecting the failing log or available failure evidence.
- Do not disable tests, lint rules, type checks, branch gates, or deployments just to make CI green.
- Do not print, hardcode, commit, or fabricate secret values.
- Do not mix package managers without evidence that the project uses the replacement.
- Do not ignore lockfile drift, generated files, or monorepo working directories.
- Do not grant broad workflow permissions when a narrower permission fixes the issue.
- Do not change deployment branch rules, environments, or release targets casually.
- Do not claim a pipeline is fixed unless verified locally, rerun remotely, or clearly marked as pending hosted CI confirmation.
- Keep changes minimal, reproducible, and documented.

## Output Contract

When using this skill, provide:

1. Pipeline problem: platform, workflow, job, step, trigger, and command.
2. Evidence: failing log lines, relevant config, and local command comparison.
3. Failure classification.
4. Root cause.
5. Fix applied and files changed.
6. Verification commands and actual results, or remote rerun requirement.
7. Safety notes for secrets, permissions, deployment targets, and branch gates.
8. Remaining risks.
9. Recommended follow-up.
