---
name: refactoring-10-security-privacy
description: Use when checking for data leaks, PII handling, and license risks in Python research code.
---

# Refactoring 10: Security and Privacy

## Goal

Reduce risk of data leakage, PII exposure, or license violations.

## Sequence

- Order: 10
- Previous: refactoring-09-performance-profiling
- Next: refactoring-11-ci-automation

## Workflow

- Scan for hardcoded secrets, tokens, or private endpoints.
  - Success: Secrets and risky endpoints are identified.
- Identify PII fields and confirm how they are stored and logged.
  - Success: PII fields and handling are documented.
- Check dataset and library licenses for compatibility.
  - Success: License constraints are verified and noted.
- Ensure `.gitignore` excludes sensitive outputs and large artifacts.
  - Success: Sensitive outputs are not tracked by git.
- Document required security or privacy constraints in `README.md`.
  - Success: README describes required constraints and handling rules.

## Guardrails

- Do not delete or redact data without approval.
- Escalate if sensitive data is discovered.
- Keep changes minimal and focused on safety.
