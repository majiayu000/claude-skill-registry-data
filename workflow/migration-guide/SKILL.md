---
name: migration-guide
description: Write migration guides for breaking changes, API changes, package upgrades, repo restructures, and workflow changes. Use when Codex is asked to help users move from one version, API, setup, host, or process to another.
license: MIT
---

# Migration Guide

## Core Workflow

1. Identify source version, target version, audience, breaking changes, and
   migration deadline.
2. Separate required changes from optional improvements.
3. Provide step-by-step migration instructions with verification after each
   risky step.
4. Include compatibility notes, rollback path, known issues, and support path.
5. Preserve platform/vendor alternatives when the project is vendor-neutral.
6. Flag unknowns, unsupported paths, and user-specific decisions.

## Safety Rules

- Do not invent compatibility, deprecation, or rollback guarantees.
- Do not hide data loss, downtime, security, or breaking-change risks.
- Do not provide destructive migration commands without review and backups.

## Deliverable Shape

For migration guides, provide:

- Who must migrate
- Source and target versions
- What changed
- Required steps
- Verification checks
- Rollback or fallback path
- Known issues
- Support or escalation path

## References

- Read `references/migration-guide-checklist.md` when writing or reviewing
  migration guidance.
