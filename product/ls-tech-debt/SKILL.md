---
name: ls-tech-debt
description: Guide technical-debt audits and backlog shaping. Use to identify, rank,
  scope, and plan debt work without opportunistic rewrites.
metadata:
  version: '1.0'
extensions:
  external_skill:
    source_kind: native-reference
    source_url: https://github.com/anthropics/knowledge-work-plugins
    source_path: engineering/skills/tech-debt/SKILL.md
    source_commit: a84404cb0156a15702c9ecf4d16051346cacce49
    source_ref: main
    source_sha256: ed3b4b1450c0fd9b8dad17313b5a4fafd8e6947d380b79b36a2e8259f3b1df0f
    license: Apache-2.0
    import_date: '2026-07-03'
    vetting_status: provenance-recorded-no-bundled-tooling-executed
---

# Technical Debt

Use this skill when working on technical debt tasks.

## Workflow

- Tie each debt item to an observable cost: incidents, slow delivery, flaky tests, security risk, support load, or onboarding drag.
- Separate cleanup, risk reduction, migration, and feature work; avoid mixing them in one diff.
- Define smallest useful debt payment with validation and rollback criteria.

## Boundaries

- Inspect the target repository before making changes.
- Prefer existing project patterns, declared package managers, and documented validation commands.
- Do not expose secrets, credentials, private user data, or production account identifiers in source, examples, or logs.
- When external APIs or current vendor behavior matter, verify against official docs before implementation.

## Provenance

- Source: `https://github.com/anthropics/knowledge-work-plugins`
- Ref: `main` at `a84404cb0156a15702c9ecf4d16051346cacce49`
- Source path: `engineering/skills/tech-debt/SKILL.md`
- License classification: `Apache-2.0`
- Source SHA-256: `ed3b4b1450c0fd9b8dad17313b5a4fafd8e6947d380b79b36a2e8259f3b1df0f`
