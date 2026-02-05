---
name: XP
description: Extreme Programming workflow orchestrator. Use when implementing features. Coordinates planning, TDD, refactoring, and commits.
---

# Extreme Programming Workflow

## Overview

This skill orchestrates the full XP workflow for feature implementation. It coordinates sub-skills and ensures proper sequencing of phases.

## The XP Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  📋 PLAN     → Discuss and break down the feature          │
│  🔴 DEVELOP  → TDD cycle (red-green)                       │
│  🔵 REFACTOR → Improve design (tests stay green)           │
│  💾 COMMIT   → Save working state                          │
│  🔁 ITERATE  → Next task or feature complete              │
└─────────────────────────────────────────────────────────────┘
```

## Phase 1: Planning (📋 PLAN)

**Goal:** Understand and decompose the feature before writing any code.

**Invoke:** Switch to `planning` skill

---

## Phase 2: Development (🔴 DEVELOP)

**Goal:** Implement the task using strict TDD.

**Invoke:** Switch to `development` skill

---

## Phase 3: Refactoring (🔵 REFACTOR)

**Goal:** Improve code design while keeping tests green.

1. **Invoke:** Switch to `refactor` skill
2. STOP
   - [ ] Ask the user if they want to see any other changes
3. Ensure all tests pass before continuing

---

## Phase 4: Commit (💾 COMMIT)

**Goal:** Save working state with clear, simple, commit message.

**Invoke:** Switch to `commit-helper` skill

### Commit Points

- After each passing test
- After completing a task
- After refactoring session

---

## Phase 5: Iterate (🔁 ITERATE)

**Goal:** Continue until feature complete.

1. Mark task as done
2. Review remaining tasks
3. Adjust plan if needed (new learnings)
4. Return to Phase 2 for next task
5. When all tasks complete → feature done

---

## Announcing Phase Transitions

When switching phases, announce clearly:

```
📋 PLAN → Starting feature discussion
🔴 DEVELOP → Writing failing test for [task]
🟢 DEVELOP → Making test pass
🔵 REFACTOR → Improving [aspect]
💾 COMMIT → Saving [task] implementation
🔁 ITERATE → Moving to next task
✅ COMPLETE → Feature done
```

## Integration with Sub-Skills

| Phase | Skill |
|-------|-------|
| PLAN | `planning` |
| DEVELOP | `development` |
| REFACTOR | `refactor` |
| COMMIT | `commit-helper` |

## Core Principles (Always Apply)

- **Communication first** — discuss before coding
- **Small steps** — one task, one test, one change at a time
- **Continuous feedback** — tests run constantly
- **Simplicity** — implement only what's needed now
- **Courage** — refactor fearlessly (tests protect you)
