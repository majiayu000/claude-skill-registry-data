---
name: "secrets-reviewer"
description: "Detect and prevent exposure of secrets, tokens, credentials, private keys, CI variables, and sensitive logs."
version: "1.0.0"
since: "2026-09-09"
last_modified: "2026-09-09"
authors:
  - "platform-engineering"
stability: "stable"
min_platform_version:
  codex: "unknown"
  amazon-q: "unknown"
  antigravity: "unknown"
  auggie: "unknown"
  bob: "unknown"
  claude-code: "unknown"
  cline: "unknown"
  codebuddy: "unknown"
  continue: "unknown"
  costrict: "unknown"
  crush: "unknown"
  github-copilot: "unknown"
  gitlab-duo: "unknown"
  factory: "unknown"
  forgecode: "unknown"
  opencode: "unknown"
  openhands: "unknown"
  cursor: "unknown"
  roo-code: "unknown"
  kiro: "unknown"
  junie: "unknown"
  gemini-cli: "unknown"
  iflow: "unknown"
  kilocode: "unknown"
  kimi: "unknown"
  lingma: "unknown"
  pi: "unknown"
  qoder: "unknown"
  qwen: "unknown"
  windsurf: "unknown"
  ollama: "unknown"
deprecated_since:
replaces:
supersedes: []
changelog:
  - version: "1.0.0"
    date: "2026-09-09"
    change: "Initial generated production-ready SDLC / DevSecOps skill"
---
# Secrets Reviewer

## Purpose

Identify and handle secrets, credentials, tokens, private keys, passwords, `.env` files, CI variables, config files, logs, fixtures, database dumps, rotation, revocation, scanning, and false positives.

## Goal and behavioral contract

The authoritative Goal and artifact references are defined in `descriptor.yaml`. Capability boundaries, identity and delegation requirements, tool permissions, data boundaries, invariants, approval requirements, output contract, and operational limits are defined in `contract.yaml`. MCP/A2A trust boundaries and the reviewed execution closure live in `integrations/` and `dependencies.yaml`; ASPS and assurance requirements live in `assurance.yaml`.

Treat those declarations as mandatory execution constraints. `skcr` validates requirements but does not claim verification or enforce them at runtime.

## When to use

- A change adds or modifies credentials, tokens, config, logs, CI variables, fixtures, dumps, or secret references.
- A suspected secret exposure needs triage without printing secret values.
- Secret storage, rotation, revocation, scope, or ownership is unclear.
- CI/CD, examples, docs, or tests may leak sensitive values.
- The central agent routes to secrets review.

## Operating model

1. Inspect likely secret locations while redacting values in output.
2. Classify each candidate as real secret, placeholder, test fixture, public identifier, or unknown.
3. Assess exposure path: repository content, history, logs, artifacts, CI, docs, images, or dumps.
4. Recommend containment: remove, rotate, revoke, scope down, and prevent recurrence.
5. Report only fingerprints, paths, and safe excerpts.

## Spec-Driven Change Context

- Treat repository specs, ADRs, runbooks, change proposals, design notes, and task files as durable context that outlives a chat session.
- For non-trivial changes, prefer a checked-in change artifact or equivalent proposal/design/tasks record before implementation begins.
- Capture requirement deltas explicitly: added, modified, removed, deprecated, or unchanged behavior.
- Keep implementation tasks traceable to acceptance criteria, affected specs, validation commands, and owners.
- During verification, compare the implementation against the proposal, design decisions, task checklist, and spec deltas.
- After completion, sync or archive completed change artifacts so the repository's source of truth reflects the final behavior.
- If the repository has no spec workflow yet, report the missing artifact and provide a minimal proposal/spec/tasks outline instead of relying on chat-only intent.

## Skill-Specific Review Scope

- API keys, tokens, private keys, passwords, `.env` files, and CI variables.
- Config files, logs, fixtures, artifacts, database dumps, and history exposure.
- Secret storage, rotation, revocation, scope, and owners.
- Secret scanning, false positives, prevention controls, and follow-up actions.
- Output redaction and safe handling of suspected values.

## Skill-Specific Checklist

- [ ] Search code, configs, docs, examples, tests, logs, artifacts, and CI files for high-entropy or credential-like values.
- [ ] Classify each candidate without echoing full secret values.
- [ ] Check whether placeholders use safe fake values and clear naming.
- [ ] Check CI/CD variables, workflow logs, debug output, and artifact upload paths.
- [ ] Check `.env`, sample env files, config maps, secrets manifests, and local setup docs.
- [ ] Check database dumps, fixtures, snapshots, screenshots, and generated files for sensitive data.
- [ ] Assess token scope, expiry, environment, owner, and blast radius when exposed.
- [ ] Recommend rotation and revocation for real or likely real secrets.
- [ ] Recommend secret-manager references, environment indirection, or scoped CI variables.
- [ ] Identify prevention controls such as scanning, pre-commit hooks, deny patterns, and log redaction.
- [ ] Call out history rewrite or artifact deletion when repository history or builds contain secrets.
- [ ] Document false-positive rationale safely.

## Decision Rules

- If a value could authenticate to a real system, treat it as a secret until proven otherwise.
- If a secret reached git history, logs, artifacts, package images, or third-party systems, require rotation and revocation.
- If a token is broad-scope, long-lived, or production-scoped, raise severity.
- If examples need credentials, use obvious fake placeholders and setup instructions.
- If output would reveal a secret, redact all but a short fingerprint.
- If ownership is unclear, require owner identification before closure.

## Finding Categories

- Hardcoded credential, token, private key, password, or connection string.
- Secret leakage through logs, artifacts, screenshots, fixtures, dumps, or generated files.
- Unsafe CI/CD secret scope, masking, debug output, or environment exposure.
- Missing rotation, revocation, owner, expiry, or scope reduction.
- False positive or placeholder requiring safe classification.
- Secret prevention gap in scanning, hooks, docs, or review process.

## Severity Guidance

- Critical: immediate exploitability or operational failure can expose secrets, regulated data, production safety, or release integrity.
- High: credible security, reliability, compliance, rollback, or user-impact risk requires owner action before merge or release.
- Medium: meaningful maintainability, validation, documentation, or process gap should be tracked and resolved.
- Low: advisory improvement, clarity issue, or hardening opportunity with limited immediate impact.

## DevSecOps Guardrails

- Do not read secrets, `.env` files, private keys, production credentials, masked CI/CD variables, database dumps, or sensitive logs unless explicitly required.
- Do not push, deploy, publish, merge, or create releases unless explicitly asked.
- Prefer merge requests, reviewable diffs, and auditable validation evidence.
- Prefer least privilege, minimal changes, and explicit rollback notes.
- Do not fabricate test results, repository state, commands, security findings, or validation outcomes.
- Report assumptions, uncertainty, residual risk, and validation gaps clearly.

## Output Requirements

- Redacted findings with path, line/context, secret type, confidence, and fingerprint.
- Exposure assessment covering repository, history, logs, artifacts, CI, docs, and packages.
- Rotation, revocation, removal, and prevention steps with owners.
- False-positive list with safe rationale.
- Validation commands or scanning evidence used.
- Residual risk and whether release or merge should be blocked.

## Acceptance Criteria

- No full secret value is printed in output.
- Real or likely real secrets have rotation and revocation guidance.
- Exposure paths and blast radius are assessed.
- False positives are justified without unsafe disclosure.
- Prevention controls are recommended for recurring classes.
- Release recommendation reflects secret severity and containment state.

## Anti-Patterns

- Printing full credentials to prove a finding.
- Dismissing tokens as test data without evidence.
- Removing a secret from the current file while ignoring git history, logs, or artifacts.
- Rotating without revoking old credentials.
- Using production-looking examples in documentation.
- Treating masked CI variables as safe when debug output or artifacts expose them.

## Changelog

### 1.0.0 - 2026-09-09

- Initial generated production-ready SDLC / DevSecOps skill.
