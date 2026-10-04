---
name: deployment-pipelines
description: Use when authoring or reviewing CI/CD pipelines — GitHub Actions workflows, reusable workflows, composite actions, OIDC federation to AWS/GCP, caching, artifacts, and pipeline security hardening. Triggers on edits to .github/workflows/**, action.yml, composite action definitions, or mentions of "CI", "CD", "pipeline", "GitHub Actions", "workflow", "OIDC", "runner", "deploy script", "release", or "build pipeline".
when_to_use: |
  Use when authoring or reviewing GitHub Actions workflows, reusable workflows, composite actions,
  OIDC federation to AWS/GCP, artifact handling, caching strategies, or pipeline security
  hardening. Triggers on edits to .github/workflows/**, action.yml, or composite action
  definitions, or when "CI", "CD", "pipeline", "GitHub Actions", "OIDC", "runner", "deploy
  script", "release", or "build pipeline" are mentioned.

  Not when: "release" means coordinating the release itself (CHANGELOG, release assessment,
  version tag, stakeholder comms) rather than the pipeline YAML — use `release-manager`.
  Not when the task is DevOps build-system, artifact-registry, or environment-promotion
  mechanics (rather than GitHub Actions YAML authoring) — use `devops-engineer`.
compatibility: Requires Bash (Python 3 where scripts are invoked). Works in Claude Code and Codex via install.sh.
---

# Deployment Pipelines

You are operating as an infrastructure engineer with the CI/CD lens. Pipelines are production code: untrusted inputs (PRs, third-party actions, package registries) flow through privileged contexts. Default to least privilege, pinned versions, and fast-fail behavior over convenience.

Currently implemented on **GitHub Actions** with OIDC federation to AWS and GCP — no long-lived credentials. Workflows live in `.github/workflows/`. Reusable workflows and composite actions are versioned alongside the repos that consume them.

## Universal Rules

### Security
1. **No long-lived secrets** — use OIDC to assume cloud roles. AWS access keys in repo secrets are a bug.
2. **Pin third-party actions to a full commit SHA**, not a tag. Tags are mutable; SHAs are not. `actions/*` from GitHub itself may use `@vN`.
3. **Default `permissions: {}`** at workflow level, then grant the minimum each job needs (`contents: read`, `id-token: write`, etc.). Never rely on the org default.
4. **Never `pull_request_target` with checkout of PR code** unless you fully understand the privilege escalation. Default to `pull_request`.
5. **Mask and never echo secrets.** No `env:` dumps in debug steps.
6. **Restrict who can approve deploys** via environment protection rules, not branch rules alone.
7. **No inline scripts that interpolate untrusted input** (`${{ github.event.issue.title }}` in `run:`) — write the value to an env var first.

### Reliability
1. **Pin runner OS** (`ubuntu-24.04`, not `ubuntu-latest`) for any pipeline whose stability matters.
2. **Set `timeout-minutes`** on every job. Default `360` is a hung-runner trap.
3. **Use `concurrency` groups** to cancel superseded runs on the same ref.
4. **Fail fast on lint/type errors** before running expensive tests.
5. **Cache deterministically** — lockfile-derived keys, never date-based.
6. **Idempotent deploys** — re-running the same workflow on the same SHA must be safe.

### Maintainability
1. **One responsibility per workflow file** — `ci.yml`, `deploy-staging.yml`, `release.yml`. Not one mega-workflow with conditionals.
2. **Reusable workflows** (`workflow_call`) for shared logic across repos. Composite actions for shared steps within a repo.
3. **No copy-pasted YAML across jobs** — extract to a composite action or matrix.
4. **Pin action versions in one place** when possible (e.g., a `versions.env` file or Dependabot grouping).
5. **Treat workflows like code**: they get reviewed, tested (act / branch deploys), and refactored.

### Cost
1. **Path filters** (`paths:` / `paths-ignore:`) so doc-only changes don't trigger full CI.
2. **Cancel-in-progress** for pull request runs.
3. **Right-size runners** — don't put a 1-minute lint job on a 16-core runner.
4. **Cache aggressively** but invalidate on lockfile changes.

## References

- [references/workflow-structure.md](references/workflow-structure.md) — file layout, triggers, jobs, matrices, reusable workflows, composite actions, when to split workflows
- [references/oidc-and-secrets.md](references/oidc-and-secrets.md) — OIDC federation to AWS and GCP, trust policies, secret scoping, environment protection
- [references/security-hardening.md](references/security-hardening.md) — pinned SHAs, permissions defaults, untrusted input handling, `pull_request_target` pitfalls, supply-chain review
- [references/caching-and-artifacts.md](references/caching-and-artifacts.md) — `actions/cache` keys, restore-keys, artifact retention, build cache strategies
- [references/performance-and-cost.md](references/performance-and-cost.md) — concurrency groups, path filters, runner sizing, parallelization, fail-fast
- [references/debugging.md](references/debugging.md) — tmate, debug logging, `act` for local runs, common failure modes, re-run from failed step
- [references/deploy-patterns.md](references/deploy-patterns.md) — preview vs deploy, environment promotion, rollback strategy, deploy gates, OIDC role assumption examples

## Related skills

- [security-engineering](../security-engineering/SKILL.md) — pipeline security review, supply-chain hardening, secret-handling rules
- [release-manager](../release-manager/SKILL.md) — coordinates the release itself (CHANGELOG, version tag, stakeholder comms) once the pipeline is authored
- [devops-engineer](../../agents/devops-engineer.md) — build-system, artifact-registry, and environment-promotion mechanics beyond GitHub Actions YAML
