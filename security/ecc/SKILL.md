---
name: ecc
description: >
  Everything Claude Code (ECC) / Agent Harness OS. Imposes a disciplined, multi-step engineering pipeline
  (plan, test, implement, review, verify, remember) with strict verification gates, memory persistence, and anti-slop rules.
license: MIT
---

# ECC (Everything Claude Code) — Agent Harness Operating System

ECC acts as a persistent middle layer that forces coding agents to follow rigorous software engineering practices instead of improvising or writing unverified code.

## The ECC Gated Pipeline

Agents running under the ECC harness must follow this immutable sequence:

1. **Reconnaissance & Contract**:
   - Inspect existing architecture, test suites, and contracts before touching any files.
   - Establish explicit acceptance criteria.
2. **Test-Driven Gating (Failing Tests First)**:
   - Write failing automated tests (or reproducer scripts) before generating production code.
   - No code generation is approved without a verified red test.
3. **Scoped Implementation**:
   - Write the minimum necessary changes to pass the test.
   - Stay strictly within the declared write scope.
4. **Autonomous Verification**:
   - Run the full test suite, linter, and type checker.
   - Verify that test output passes (Green).
5. **Architectural & Security Audit**:
   - Check against known vulnerability vectors and agent anti-patterns.
6. **Memory & Reflection**:
   - Persist key architectural decisions and failure recoveries for future sessions.

## Commands & Workflows
- `/plan`: Create structured step-by-step implementation contracts.
- `/verify`: Run multi-agent automated review and evidence verification.
- `/remember`: Store repo-specific constraints into project context memory.
