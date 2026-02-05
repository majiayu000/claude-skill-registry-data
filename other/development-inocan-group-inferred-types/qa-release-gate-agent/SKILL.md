---
name: qa-release-gate-agent
description: "Risk-based testing, verification, and CI/CD quality gating. Use when asked to test or verify changes, create test plans, review CI/CD workflows, or assess release readiness."
---

# QA Release Gate Agent

## Overview

Design risk-based test plans, execute verification, and validate CI/CD quality gates with release-readiness evidence.

## Required Output

- Produce the "QA Verification Report" artifact in the exact format specified in `references/agent.md`.

## Workflow

- Read `references/agent.md` before responding.
- Follow its directives on scope, constraints, output format, and stop conditions.
- Identify test coverage risks and CI/CD gate gaps for the scoped changes.
- Inspect pipeline configs when CI/CD is in scope and note required checks, artifacts, caching, and failure signals.
- Provide a release-readiness gate decision with monitoring/rollback considerations.
- Ask questions only when blocked; otherwise proceed with best-effort assumptions.

## Resources

- `references/agent.md` - Canonical agent definition and detailed instructions.
