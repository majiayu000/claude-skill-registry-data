---
name: tdd-workflow
description: Use this skill when writing new features, fixing bugs, or refactoring code. Enforces test-driven development
  with 80%+ coverage including unit, integration, and E2E tests.
category: testing
sources:
- repository: ecc
  original_path: skills/tdd-workflow/SKILL.md
  sha256: f5d8543733c557f0c53b688d40f14e9b870a6b2c7e405bab07433954e363828a
principles:
- core/think-before-coding
- core/simplicity-first
- core/surgical-changes
- core/goal-driven-execution
---

> **Library use:** Apply the [compatibility and execution contract](../../COMPATIBILITY.md). Source roles, memory claims, command names, hooks, and integrations are instructions or prerequisites—not installed capabilities.

# Tdd Workflow

Use this skill when writing new features, fixing bugs, or refactoring code. Enforces test-driven development with 80%+ coverage including unit, integration, and E2E tests.

## Required procedure

Read [the complete methodology](references/methodology.md) before performing this skill. It retains the full procedure, examples, constraints, and failure handling.

Procedure topics: Test-Driven Development Workflow; When to Activate; Plan Handoff; Core Principles; 1. Tests BEFORE Code; 2. Coverage Requirements; 3. Test Types; 4. Git Checkpoints; TDD Workflow Steps; Step 0: Detect the Test Runner; Step 1: Write User Journeys; Step 2: Generate Test Cases; Step 3: Run Tests (They Should Fail); Tests should fail - we haven't implemented yet.

## Runtime prerequisites

See [the dependency ledger](../../DEPENDENCIES.md) and this skill’s records in [dependencies.json](../../dependencies.json). Native gstack/ECC CLIs, browsers, hooks, model tools, credentials, and memory stores must be available before invoking their steps. No runtime installation or execution has been performed. CSO requires its trusted helper; do not emulate that helper on the host.

## Related skills and principles

- [core/goal-driven-execution](../../core/goal-driven-execution/SKILL.md)
- [core/simplicity-first](../../core/simplicity-first/SKILL.md)
- [core/surgical-changes](../../core/surgical-changes/SKILL.md)
- [core/think-before-coding](../../core/think-before-coding/SKILL.md)
- [developer-experience/bun-runtime](../../developer-experience/bun-runtime/SKILL.md)
- [workflows/plan](../../workflows/plan/SKILL.md)

## Source provenance

- `ecc/skills/tdd-workflow/SKILL.md`
