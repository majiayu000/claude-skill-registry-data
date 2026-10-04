---
name: safe-implementer
description: Create or modify code, tests, configuration, and project files safely with real file changes.
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

# Safe Implementer

## Purpose

Create or modify code, tests, configuration, and project files safely with real file changes.

## When to use

Use this skill when the task matches the description above or when the central agent instructions route work to `$safe-implementer`.

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

- Inspect existing patterns, ownership boundaries, tests, config, and generated files before changing code.
- Make the smallest coherent change that satisfies the request while preserving behavior outside scope.
- Protect user work: check the working tree, avoid reverting unrelated changes, and work with concurrent edits.

## Skill-Specific Checklist

- Relevant code, tests, docs, config, and sync/generation paths were read before editing.
- Changes are scoped to the requested behavior and directly necessary support files.
- Formatting, tests, build, lint, or focused manual checks are run where practical.

## Decision Rules

- Do not revert user changes unless explicitly requested.
- Do not stop at a plan when implementation is requested and context is sufficient.
- Ask before destructive filesystem changes, releases, deployments, or credential access.

## Acceptance Criteria

- Requested behavior is implemented or the blocker is clearly documented.
- Relevant validation passes, or failures are reported with cause and next step.
- Generated or synchronized files match their canonical source when applicable.

## Output Requirements

- State what changed and which files matter most.
- Report validation commands and results exactly as run.
- Mention residual risks, skipped checks, and follow-up work succinctly.

## Changelog

### 1.1.0 - 2026-06-10

- Added production-ready skill-specific operating model, checklist, decision rules, acceptance criteria, and output requirements.

### 1.0.0 - 2025-01-01

- Initial release.
