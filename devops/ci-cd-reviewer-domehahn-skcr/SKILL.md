---
name: ci-cd-reviewer
description: Review CI/CD pipelines, runners, permissions, artifacts, caches, deployment gates, and token exposure.
version: "1.1.0"
since: "2026-06-10"
last_modified: "2026-06-10"
authors:
  - platform-engineering
stability: stable
min_platform_version:
  codex: "unknown"
  claude-code: "unknown"
  github-copilot: "unknown"
  gitlab-duo: "unknown"
  opencode: "unknown"
  openhands: "unknown"
  cursor: "unknown"
  roo-code: "unknown"
  kiro: "unknown"
  junie: "unknown"
  gemini-cli: "unknown"
  windsurf: "unknown"
  ollama: "unknown"
deprecated_since:
replaces:
supersedes: []
changelog:
  - version: "1.1.0"
    date: "2026-06-10"
    change: "Added production-ready skill-specific operating model, checklist, decision rules, acceptance criteria, and output requirements"
  - version: "1.0.0"
    date: "2025-01-01"
    change: "Initial release"
---

# CI/CD Reviewer

## Purpose

Review CI/CD pipelines, runners, permissions, artifacts, caches, deployment gates, and token exposure.

## When to use

Use this skill when the task matches the description above or when the central agent instructions route work to `$ci-cd-reviewer`.

## Operating model

1. Clarify the goal and constraints.
2. Inspect the minimum relevant repository context.
3. Produce a concise execution plan for non-trivial work.
4. Execute with tools when implementation is requested.
5. Validate the result with repository-native checks.
6. Summarize changed files, validation results, and residual risks.

## DevSecOps guardrails

- Do not read secrets, `.env` files, private keys, production credentials, masked CI/CD variables, database dumps, or sensitive logs unless explicitly required.
- Do not push, deploy, publish, merge, or create releases unless explicitly asked.
- Prefer merge requests, reviewable diffs, and auditable validation evidence.
- Prefer least privilege, minimal changes, and explicit rollback notes.
- Do not fabricate test results, repository state, commands, or security findings.

## Skill-Specific Operating Model

- Inventory workflows, jobs, triggers, runner types, permissions, secrets, artifacts, caches, environments, and deployment gates.
- Follow privileged paths first: release, deploy, publish, signing, image build, and infrastructure mutation jobs.
- Compare behavior across pull requests, forks, protected branches, tags, scheduled runs, and manual runs.

## Skill-Specific Checklist

- Untrusted events cannot reach privileged jobs, secrets, or write-scoped tokens.
- Artifacts, caches, and build outputs are scoped, retained, and consumed safely.
- Deployments have approvals, environment protection, concurrency, rollback, and audit evidence.

## Decision Rules

- Block on secret exposure, write-token access from untrusted code, or deploy paths without approvals.
- Warn on mutable third-party actions/images unless a documented update policy exists.
- Do not remove security gates to improve speed without an equivalent compensating control.

## Acceptance Criteria

- Privileged CI/CD paths and their controls are explicitly covered.
- Findings identify the workflow, job, key, or file involved.
- Recommendations include validation steps such as dry runs, branch tests, or permission checks.

## Output Requirements

- Report findings by severity with workflow/job references.
- Summarize token, secret, runner, artifact, cache, and deployment posture.
- Separate repository-only fixes from platform-admin actions.

## Changelog

### 1.1.0 - 2026-06-10

- Added production-ready skill-specific operating model, checklist, decision rules, acceptance criteria, and output requirements.

### 1.0.0 - 2025-01-01

- Initial release.
