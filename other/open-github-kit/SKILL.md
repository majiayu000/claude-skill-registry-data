---
name: open-github-kit
description: Operate authorized GitHub repositories end to end, including branches, pull requests, Actions, releases, packages, deployments, issues, and settings. Use when building, repairing, publishing, or auditing GitHub-backed applications while preserving branch protection and least privilege.
---

# Open GitHub Kit

Use the authenticated GitHub connector or `gh` CLI. Treat broad access as the scopes granted by the owner, never permission to bypass repository rules.

## Workflow

1. Confirm account, organization, repository, default branch, and environment.
2. Read repository instructions, protection rules, current checks, and relevant files before writing.
3. Reuse an existing branch or pull request for the same change; otherwise create one focused branch.
4. Make the smallest reversible change. Keep credentials in GitHub secrets or approved vault references.
5. Run formatting, tests, build, secret scan, and workflow validation.
6. Open a pull request with evidence, risks, rollback, and remaining approvals.
7. Merge only after required reviews and checks pass; verify merge SHA, deployment, and health.

## Capabilities

- Repositories, branches, commits, pull requests, reviews, issues, labels, and releases.
- Actions, logs, artifacts, environments, deployments, and protected secret references.
- Packages and containers when GitHub Packages is the selected registry.
- Collaborator/configuration audits; membership or permission changes require confirmation.

## Guardrails

Never push to a protected branch, force-push, disable checks, expose secrets, or delete repositories/releases without approval. Avoid duplicate workflows, PRs, releases, and environments. Report `VERIFIED` only with direct API and CI evidence.
