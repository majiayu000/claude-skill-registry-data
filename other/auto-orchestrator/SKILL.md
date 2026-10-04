---
name: auto-orchestrator
description: Intelligent workflow orchestrator that automatically chains the right skills (spec, plan, build, test, review, code-simplify, ship) based on the current state of the work. Use when you want Claude to drive a feature or task end-to-end without manually invoking each skill.
---

# Auto Orchestrator

## Overview

This skill automatically detects where you are in the development lifecycle and invokes the right skills in sequence. Instead of manually calling `/spec`, then `/plan`, then `/build`, etc., you describe what you want and this skill figures out what's needed and drives through each phase with gate checks between them.

## When to Use

- You have a feature, project, or task and want Claude to drive it end-to-end
- You're not sure which skill to start with
- You want the full lifecycle: spec -> plan -> build -> test -> review -> simplify -> ship

## How It Works

### Phase Detection

Before doing anything, assess the current state:

```
1. Does a spec exist for this work?
   - NO  -> Start at Phase 1 (Spec)
   - YES -> Move to next check

2. Is the work broken into tasks?
   - NO  -> Start at Phase 2 (Plan)
   - YES -> Move to next check

3. Is there code to implement?
   - YES, unfinished tasks remain -> Start at Phase 3 (Build + Test)
   - YES, all tasks done -> Move to next check

4. Has the code been reviewed?
   - NO  -> Start at Phase 4 (Review + Simplify)
   - YES -> Move to next check

5. Is it ready to ship?
   - YES -> Start at Phase 5 (Ship)
```

### Phase 1: Spec (`spec-driven-development`)

**Trigger:** No spec exists, requirements are vague or incomplete.

**Action:** Read `${HAMZAISH_ROOT:-$HOME/Claude/Hamzaish}/factory/skills/spec-driven-development/SKILL.md` and follow its full process.

**Gate:** Present the spec to the user. Do NOT proceed to Phase 2 until the user approves the spec.

**Output:** A structured spec with acceptance criteria.

---

### Phase 2: Plan (`planning-and-task-breakdown`)

**Trigger:** Spec exists but work hasn't been broken into tasks.

**Action:** Read `${HAMZAISH_ROOT:-$HOME/Claude/Hamzaish}/factory/skills/planning-and-task-breakdown/SKILL.md` and follow its full process.

**Gate:** Present the task breakdown to the user. Do NOT proceed to Phase 3 until the user approves the plan.

**Output:** Ordered list of tasks with acceptance criteria and dependencies.

---

### Phase 3: Build + Test (`incremental-implementation` + `test-driven-development`)

**Trigger:** Tasks exist but implementation is incomplete.

**Action:**
1. Read `${HAMZAISH_ROOT:-$HOME/Claude/Hamzaish}/factory/skills/incremental-implementation/SKILL.md`
2. Read `${HAMZAISH_ROOT:-$HOME/Claude/Hamzaish}/factory/skills/test-driven-development/SKILL.md`
3. For each task in order:
   a. Write a failing test (TDD red phase)
   b. Implement the minimum code to pass (TDD green phase)
   c. Refactor if needed (TDD refactor phase)
   d. Verify the task's acceptance criteria
   e. Mark the task complete
   f. Brief the user on progress

**Gate:** After all tasks are implemented, confirm with the user before moving to review.

**Output:** Working code with tests for every task.

---

### Phase 4: Review + Simplify (`code-review-and-quality` + `code-simplification`)

**Trigger:** Implementation is complete, code hasn't been reviewed.

**Action:**
1. Read `${HAMZAISH_ROOT:-$HOME/Claude/Hamzaish}/factory/skills/code-review-and-quality/SKILL.md` and run the five-axis review:
   - Correctness
   - Readability
   - Architecture
   - Security
   - Performance
2. Fix any issues found during review.
3. Read `${HAMZAISH_ROOT:-$HOME/Claude/Hamzaish}/factory/skills/code-simplification/SKILL.md` and simplify:
   - Remove unnecessary complexity
   - Consolidate duplicate logic
   - Simplify abstractions that aren't earning their weight

**Gate:** Present review findings and simplification changes to the user. Get approval before shipping.

**Output:** Reviewed, simplified code ready for production.

---

### Phase 5: Ship (`shipping-and-launch`)

**Trigger:** Code is reviewed and approved, ready for production.

**Action:** Read `${HAMZAISH_ROOT:-$HOME/Claude/Hamzaish}/factory/skills/shipping-and-launch/SKILL.md` and follow its full process:
- Pre-launch checklist
- Monitoring setup
- Rollback plan
- Staged deployment

**Gate:** Final confirmation from the user before deploying.

**Output:** Code deployed to production with monitoring in place.

---

## Rules

1. **Always gate between phases.** Never silently advance from spec to plan to build. The user must approve each phase's output before the next begins.

2. **Read the actual skill file before executing each phase.** This orchestrator tells you WHICH skill to invoke and WHEN. The skill file itself contains the detailed process. Do not skip reading it.

3. **You can start at any phase.** If the user says "I already have a spec, just build it," start at Phase 2 or 3. If they say "review this code," start at Phase 4. Match the entry point to the current state.

4. **You can stop at any phase.** If the user says "just spec and plan this, don't build yet," stop after Phase 2. Respect scope.

5. **Surface assumptions at every phase transition.** Before moving to the next phase, state what you're assuming about readiness and ask if it's correct.

6. **Track progress visibly.** At each phase transition, show:
   ```
   PROGRESS:
   [x] Phase 1: Spec — approved
   [x] Phase 2: Plan — 8 tasks identified, approved
   [>] Phase 3: Build + Test — task 3/8 in progress
   [ ] Phase 4: Review + Simplify
   [ ] Phase 5: Ship
   ```

7. **If a phase fails or reveals problems with a previous phase, go back.** If during Build you discover the spec was wrong, go back to Spec. If during Review you find architectural issues, go back to Plan. Don't paper over upstream problems.

## Quick Start

When invoked, say:

```
AUTO ORCHESTRATOR — Starting lifecycle assessment.

Analyzing current state...
- Spec: [exists/missing]
- Plan: [exists/missing]  
- Implementation: [complete/partial/not started]
- Tests: [passing/failing/missing]
- Review: [done/not done]

Recommended starting phase: Phase [N] — [Name]
Shall I proceed?
```

Then wait for user confirmation before executing.
