---
name: e2e
description: >
  Orchestrate E2E test triage and fix implementation: runs triage-ci then implement sequentially.
  Accepts test names, --agent, artifact path, or CI run reference.
  For individual phases, use /e2e:triage-ci, /e2e:debug, or /e2e:implement.
  Use when the user says "triage e2e", "fix e2e failures", or wants the full triage-to-fix pipeline.
---

# E2E Triage & Fix — Full Pipeline

Run triage-ci then implement sequentially. Parameters are collected once and reused across both phases.

## Parameters

The user provides one or more of:
- **Test name(s)** -- e.g., `TestInteractiveMultiStep`
- **`--agent <agent>`** -- optional, defaults to all agents that previously failed
- **A local artifact path** -- skip straight to analysis of existing artifacts
- **CI run reference** -- `latest`, a run ID, or a run URL

## Phase 1: Triage CI

Read and follow the full procedure from `.claude/skills/e2e/triage-ci.md`.

This produces a findings report with classifications (flaky/real-bug/test-bug) for each test+agent pair.

## Phase 2: Implement Fixes

Read and follow the full procedure from `.claude/skills/e2e/implement.md`.

Uses the findings from Phase 1 (already in conversation context) to propose, apply, and verify fixes.
