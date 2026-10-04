---
name: xp
description: "Extreme Programming for AI-human pair development. Use when: pair programming with your AI, building incrementally with tests, working with clear role division, or the user mentions XP/YAGNI/simple design/continuous refactoring."
triggers:
  - pair programming with structured cycles
  - test-driven incremental development
  - role-divided driver/navigator flow
  - continuous refactoring discipline
  - small-batch delivery with review
---

# XP Navigator

Extreme Programming adapted for AI-human pairs: continuous code review (live pairing), relentless testing (TDD), constant design improvement (refactoring), frequent releases (small increments).

## What It Does

Drives structured pair-development cycles with five gates per cycle:
1. **Plan** — Define one small, deliverable task with acceptance criteria
2. **Test** — Write a failing test that describes behavior
3. **Implement** — Minimal code to pass the test
4. **Refactor** — Improve while green; extract duplication, clarify names
5. **Release** — Commit the increment; loop or hand off

Each cycle runs 5–30 min. No big-bang features; every cycle ships testable, reviewable code.

## When to Use

- **Pair dev** — Structured iteration with tests + live review (no quick-script mode)
- **Incremental features** — Break work into small cycles; each builds toward the goal
- **Roles unclear** — Need signal for who drives (direction) vs. navigates (reviews)
- **Refactor needed** — Code quality degrading; XP treats refactoring as continuous, not deferred
- **Not a fit** — Skip if: user wants a quick script (no test overhead), one-off task (no iteration benefit), or user is unavailable for review cycles

## Core Patterns

**Read before write.** Explore project structure, conventions, test patterns before proposing changes.

**Test fails first.** Write the test, watch it fail, then implement. Confirms test is real and implementation works.

**Minimal to pass.** No over-engineering, no speculative features. If multiple approaches work, pick the clearest.

**Refactor while green.** Extract duplication, improve names, simplify logic — never refactor while red (test failing).

**Small cycles.** If a cycle takes >30 min, split the task. Faster feedback, easier review.

**Communicate intent.** Explain approach and tradeoffs *before* coding, not after.

## Rules

- Run tests + lint after every change
- Commit after each completed cycle (focused, reviewable diffs)
- Never refactor while red
- Approve test before implementation; approve refactor before commit
- If a cycle stalls, call out the blocker and pivot or escalate

## Handoff

After one or more completed cycles:
1. **Signal-first verdict** — Features working? Tests green? Ready for review?
2. **Blockers (if any)** — Top 3 issues preventing next cycle
3. **Code state** — Diffs staged or on branch; tests passing
4. **Next task** — Pick the next cycle or hand to human for re-prioritization

Use `/handoff` to checkpoint across multi-session pairing.

## Related Skills

- `/tdd` — Deep TDD discipline (red-green-refactor loops)
- `/handoff` — Multi-session checkpoint and resume
- `/code-review` — Live code review during pairing
- `/refactor-plan` — Strategic refactoring planning
