---
name: threat-modeler
description: Identify assets, trust boundaries, abuse cases, attack paths, threats, and required security controls.
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

# Threat Modeler

## Purpose

Identify assets, trust boundaries, abuse cases, attack paths, threats, and required security controls.

## When to use

Use this skill when the task matches the description above or when the central agent instructions route work to `$threat-modeler`.

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

- Define scope, actors, assets, data flows, trust boundaries, and entry points before listing threats.
- Model realistic attacker goals and capabilities instead of generic theoretical threats.
- Map threats to existing controls, missing controls, residual risk, and verifiable mitigations.

## Skill-Specific Checklist

- Assets include sensitive data, credentials, privileged operations, availability, integrity, and audit evidence.
- Boundaries include network, identity, tenant, environment, repository, CI/CD, and runtime boundaries.
- Threats cover spoofing, tampering, repudiation, information disclosure, denial of service, and privilege escalation where relevant.

## Decision Rules

- Do not assume a control exists unless code, config, docs, or platform policy shows it.
- Prioritize threats by impact and plausibility, not checklist completeness alone.
- Use `unknown` explicitly when architecture or control evidence is missing.

## Acceptance Criteria

- Assets, boundaries, entry points, and key data flows are named.
- Top threats include attacker path, impact, existing controls, and recommended controls.
- Mitigations are specific enough to become implementation or governance tasks.

## Output Requirements

- Provide scope and system map summary first.
- List threats by priority with abuse case, impact, controls, gaps, and mitigation.
- Include assumptions and out-of-scope areas.

## Changelog

### 1.1.0 - 2026-06-10

- Added production-ready skill-specific operating model, checklist, decision rules, acceptance criteria, and output requirements.

### 1.0.0 - 2025-01-01

- Initial release.
