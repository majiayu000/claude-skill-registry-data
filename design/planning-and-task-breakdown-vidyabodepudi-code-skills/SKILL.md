---
name: planning-and-task-breakdown
description: >
  Decompose approved designs into bite-sized implementation tasks with
  exact file paths, verification steps, and dependency ordering. Use
  after brainstorming/spec approval, before implementation begins.
  Each task should take 2-10 minutes for an agent to complete.
version: 1.0.0
permissions:
  - fs.read
  - fs.write
triggers:
  - context: "design has been approved"
  - context: "spec has been approved"
  - context: "ready to implement"
  - command: "/plan"
platforms:
  - claude-code
  - cursor
  - gemini-cli
  - copilot
  - codex
  - opencode
  - windsurf
  - kiro
dependencies:
  - brainstorming@^1.0.0
model_variants:
  claude:
    enforcement_style: "human-partner collaborative"
    task_phrasing: "Let's break this down into small, focused tasks that we can implement and verify one at a time."
  gemini:
    enforcement_style: "structured-checklist"
    task_phrasing: "TASK TEMPLATE: ☐ File paths ☐ What to implement ☐ Test expectations ☐ Verification command ☐ Dependencies"
  gpt:
    enforcement_style: "directive-imperative"
    task_phrasing: "Each task MUST include: exact file paths, implementation scope, test expectations, verification command."
author: codehands-core
signed: true
tier: 1
---

## Overview

Good plans produce good code. This skill transforms approved designs into a sequence of small, independent, verifiable implementation tasks. Each task is scoped so an agent can complete it in a single focused cycle — read the task, implement, test, commit.

## When to Use

- After `codehands:brainstorming` design approval
- After `codehands:spec-driven-development` spec sign-off
- Before any implementation begins
- When an existing plan needs re-planning due to scope changes
- NOT during implementation (if you need to re-plan mid-implementation, pause and re-enter this skill)

## Process

### 1. Read the Spec Completely

Read the approved design/spec document end-to-end. Do not start decomposing until you've read it all. You're looking for:
- Every requirement that requires code changes
- Dependencies between requirements
- Shared infrastructure needed by multiple features
- Testing requirements

### 2. Identify Implementation Order

Dependencies dictate order. Build in this sequence:
1. **Shared infrastructure** — Types, interfaces, utilities used by multiple components
2. **Data layer** — Database schemas, models, data access
3. **Business logic** — Core functions, services, algorithms
4. **Integration layer** — API endpoints, event handlers, coordinators
5. **Presentation** — UI components, CLI output, response formatting
6. **Polish** — Error messages, logging, documentation

### 3. Write Task Definitions

Each task MUST include ALL of these fields:

```markdown
### Task N: [Brief descriptive title]

**Files:**
- `src/models/user.ts` (CREATE)
- `src/services/auth.ts` (MODIFY, lines 45-60)
- `tests/models/user.test.ts` (CREATE)

**Implement:**
- [Specific behavior to implement]
- [Exactly what to build — no ambiguity]
- [Include code patterns to follow if relevant]

**Test Expectations:**
- [What the test should verify]
- [Expected inputs and outputs]

**Verification:**
```bash
npm test -- --grep "User model"
```

**Depends On:** Task 1, Task 3
**Estimated Scope:** [Small/Medium/Large]
```

### 4. Size Each Task Correctly

| Size | Lines of Code | Time | When to Use |
|---|---|---|---|
| **Small** | < 50 LOC | 2-5 min | Single function, simple test |
| **Medium** | 50-150 LOC | 5-10 min | Component + tests, API endpoint |
| **Large** | 150+ LOC | 10-15 min | Maximum size — consider splitting |

> **If a task would take > 15 minutes or touch > 3 files, split it.**

### 5. Verify the Plan

Before presenting to the user:
- [ ] Every spec requirement is covered by at least one task
- [ ] Dependencies are acyclic (no circular dependencies)
- [ ] Each task can be verified independently
- [ ] The first task can be started without any other task completing
- [ ] Shared infrastructure tasks come before tasks that depend on them
- [ ] Tests are included IN each task (not "add tests later")

### 6. Save and Get Approval

Save the plan to `docs/plans/YYYY-MM-DD-<topic>-plan.md` and present to the user:

> "Implementation plan written to `<path>`. It has N tasks with an estimated scope of [Small/Medium/Large]. Review and let me know if you'd like any changes before I start."

## Plan Format

```markdown
# Implementation Plan: [Feature Name]

**Spec:** `docs/specs/YYYY-MM-DD-<topic>-spec.md`
**Created:** YYYY-MM-DD
**Tasks:** N total | N small | N medium | N large
**Estimated Total Scope:** [Sum of task sizes]

## Dependency Graph
```
Task 1 → Task 3 → Task 5
Task 2 → Task 3
Task 4 (independent)
```

## Tasks

### Task 1: [Title]
[Full task definition as specified above]

### Task 2: [Title]
...
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I can keep the plan in my head" | Context windows are finite and unreliable. Written plans survive context switches, session restarts, and hand-offs. Always write it down. |
| "The spec is clear enough to implement directly" | Specs describe WHAT. Plans describe HOW and IN WHAT ORDER. Even clear specs need decomposition into verifiable steps. |
| "This is only 2-3 tasks, I don't need formal planning" | Even 2-3 tasks benefit from explicit file paths, test expectations, and verification commands. The format takes 2 minutes to write and saves 20 minutes of confusion. |
| "I'll figure out the order as I go" | Implementing without dependency ordering causes rework. Building a component before its dependency is ready means guessing at interfaces. |
| "Tests can be a separate task at the end" | Tests in each task, not at the end. Deferring tests creates a "testing debt" that never gets paid. TDD means the test IS the task. |

## Red Flags

- Tasks without file paths (where will the code go?)
- Tasks without verification commands (how will you know it works?)
- Tasks that touch 5+ files (too big — split it)
- "Add tests" as the last task
- No dependency ordering
- Tasks that duplicate spec content verbatim without decomposition

## Verification

- [ ] Every requirement from the spec is covered by at least one task
- [ ] Each task has: files, implementation description, test expectations, verification command
- [ ] No task exceeds 15 minutes or 3 files
- [ ] Dependencies are explicit and acyclic
- [ ] Tests are included in each task (not deferred)
- [ ] Plan saved to `docs/plans/` and user has approved
- [ ] First task can begin immediately without blocking

## See Also

- `codehands:brainstorming` — Design phase that precedes planning
- `codehands:spec-driven-development` — Spec that drives the plan
- `codehands:multi-agent-orchestration` — Execute the plan with subagents
- `codehands:executing-plans` — Execute the plan in parallel sessions
- `codehands:context-engineering` — Manage context during planning
