---
name: dependency-governance
description: Control dependency sprawl in agent-edited repos. Use when dependencies are added, removed, audited, approved, unused, risky, vulnerable, or need docs/quality/dependencies.md and scripts/check-dependencies.
---

# Dependency Governance

## Purpose

Make dependency changes intentional, justified, and reviewable.

## Inspect First

- dependency manifests and lockfiles
- existing dependency policy, audit tools, update bots, security baseline, and recent dependency diffs

## Procedure

1. Define policy.
   - Approved libraries and why.
   - Rules for adding, replacing, or removing dependencies.
   - When small local code is preferred over a package.
   - Use `$research-first-change` before adding or replacing packages whose APIs, security posture, or maintenance status need current source evidence.

2. Add checks.
   - Use ecosystem-native audit and unused-dependency tools when present.
   - Use `scripts/check_dependencies.py` for lightweight inventory.
   - Create target repo `scripts/check-dependencies` where useful.

3. Document decisions.
   - Update `docs/quality/dependencies.md`.
   - Record risky additions in PR validation notes.
   - Record source, version, rationale, alternatives, and validation evidence for external dependency decisions.

4. Coordinate security.
   - Use `security-baseline` for vulnerability and secret-related checks.

## Validation

- Run dependency checks or document why unavailable.
- Confirm new dependencies have rationale.
- Confirm docs match manifests.

## Completion Criteria

- Agents cannot add dependencies silently or without a documented reason.
