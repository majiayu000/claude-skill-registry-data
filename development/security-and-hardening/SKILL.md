---
name: security-and-hardening
description: Use when the change touches auth, secrets, audited state, audit trails, infrastructure, or external inputs — treat security as a design constraint, not final polish.
type: skill
license: MIT
compatibility:
  - claude-code
  - codex
effort: max
context: fork
user-invocable: false
---

# Security And Hardening

## Active Stack

```!
echo "--- Tech Stack ---"
cat .claude/tech-stack 2>/dev/null || echo "(not set)"
```

## Overview

Treat security and compliance as design constraints, not final review polish. Changes to serious software must preserve confidentiality, integrity, auditability, and least privilege.

## When To Use

- Auth or authorization changes; secrets or configuration changes
- Audited state mutations (e.g. financial state, patient records, legal documents — see domain supplement)
- New endpoints, external integrations, infrastructure, or IAM changes

### When NOT To Use

- Purely internal non-sensitive refactors with no new data flow or boundary change

## Workflow

1. Read the domain and security supplement (`.claude/references/domain-finance.md`, or the team's `domain-<name>.md`) for regulated state, sensitive data, audit invariants and review questions.
2. Read the stack skill's `## Framework Patterns` for framework-level auth and validation idioms.
3. Identify trust boundaries:
   - user input
   - external service input
   - internal privileged operations
4. Check auth and authorization requirements.
5. Check PII, secrets, and logging behavior.
6. Check audit requirements for state changes that require an audit trail.
7. Check query safety, transaction boundaries, and error exposure.
8. For infra, check least privilege, blast radius, and secret access scope.
9. **Supply chain — dependency intake.** If the diff adds or replaces a third-party dep (any of `package.json`, `*.csproj`, `Directory.Packages.props`, `requirements.txt`, `pyproject.toml`, `Pipfile`, `go.mod`, `Cargo.toml`, `Gemfile`, `composer.json`), walk the new dep through `.claude/references/dependency-intake-checklist.md` — scope, maintenance, size, security, license. Two `Poor` ratings block; one `Poor` requires written override. Cite concrete evidence (CVE id, last-release date, license SPDX) per Poor rating.
10. If a requirement is unclear, stop and ask rather than guessing.

## Rules

- No secrets in code or logs.
- No unaudited state mutation where the domain requires audit trails.
- No trust in external input without validation.
- No wildcard IAM/resource access without explicit justification.
- No new third-party dep that fails the six-criteria intake gate (`.claude/references/dependency-intake-checklist.md`).

## Verification

- [ ] Trust boundaries were identified
- [ ] Auth/authz expectations were checked
- [ ] Audit requirements were checked (domain supplement consulted if present)
- [ ] No secrets or PII leakage is introduced
- [ ] Infra permissions remain least-privilege
- [ ] Any new third-party dep cleared the intake checklist (or has documented override)
