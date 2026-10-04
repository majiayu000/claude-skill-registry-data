---
name: secrets-reviewer
description: Detect and prevent exposure of secrets, tokens, credentials, private keys, CI variables, and sensitive logs.
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

# Secrets Reviewer

## Purpose

Detect and prevent exposure of secrets, tokens, credentials, private keys, CI variables, and sensitive logs.

## When to use

Use this skill when the task matches the description above or when the central agent instructions route work to `$secrets-reviewer`.

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

- Inspect diffs, config, examples, docs, logs, CI files, artifacts, and generated output for credential exposure patterns.
- Distinguish real secrets, high-entropy candidates, placeholders, test fixtures, and documented examples.
- Trace access impact, usage location, rotation requirement, and prevention controls.

## Skill-Specific Checklist

- Check API keys, tokens, private keys, passwords, cookies, kubeconfigs, cloud credentials, and connection strings.
- Review code, tests, docs, CI variables, artifacts, logs, images, lockfiles, and generated files.
- Confirm scanning, redaction, masked variables, ignore rules, and secret-manager references.

## Decision Rules

- Never print full suspected secret values; show type, location, and a short fingerprint only if needed.
- Treat private keys and live tokens as critical until proven otherwise.
- Do not mark a value safe solely because it appears in a test file.

## Acceptance Criteria

- Suspected secrets are classified with confidence and recommended action.
- Confirmed or likely live credentials include rotation/revocation guidance.
- Preventive controls are proposed for the exposure path.

## Output Requirements

- Lead with confirmed and high-confidence exposures by severity.
- Reference files and line numbers without revealing secret values.
- Provide containment steps: remove, rotate/revoke, audit, prevent.

## Changelog

### 1.1.0 - 2026-06-10

- Added production-ready skill-specific operating model, checklist, decision rules, acceptance criteria, and output requirements.

### 1.0.0 - 2025-01-01

- Initial release.
