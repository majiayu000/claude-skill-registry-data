---
name: workflow
description: Enforces development phases. Triggers on implement, build, create, fix, refactor.
---

# Required Workflow

## Phase 1: ANALYSIS
- What is being asked?
- Search codebase for related files (Read, Glob, Grep)
- Identify dependencies and existing patterns

**Output:** Findings summary
**Gate:** Wait for acknowledgment

## Phase 2: PLANNING
- Break into 2-3 atomic tasks
- Create `.planning/PLAN-{feature}.md`
- Define verification criteria

**Output:** Plan document
**Gate:** Wait for approval

## Phase 3: IMPLEMENTATION
- Follow plan exactly
- Run tests after each change
- Deviation rules:
  - Bugs/blockers: fix immediately, document
  - Architecture changes: STOP and ask
  - Enhancements: log to ISSUES.md, continue

**Output:** Working code with tests

## Phase 4: VALIDATION
- Run tests
- Type check
- Lint
- Manual verification

**Gate:** All checks pass

## Context Management
- 50%+ used: mention it
- 70%+ used: create handoff document
- Never start large tasks below 15%
