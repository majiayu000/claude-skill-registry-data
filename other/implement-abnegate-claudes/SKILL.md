---
name: implement
description: Full TDD implementation of a feature with review cycles
argument-hint: <feature description>
---

# Implement Feature (TDD)

Complete end-to-end implementation of a feature using Test-Driven Development with code review cycles.

**YOU MUST NOT STOP UNTIL THE ENTIRE PLAN IS IMPLEMENTED. NO TODOS. NO PARTIAL WORK.**

## Arguments

- `$ARGUMENTS` - Feature, fix, or chore description

## Phase 0: Clarify Requirements

Ask questions until you have COMPLETE understanding:

- What exactly should this feature do?
- What are the edge cases and acceptance criteria?
- Are there existing patterns to follow?
- Are there any constraints or requirements?

Use `AskUserQuestion` to gather any missing information. Do NOT proceed with ambiguity.

## Phase 1: Orchestrate

Invoke the **consolidation** skill, which loads the full orchestration cycle into your context. You become the conductor and dispatch each stage:

```
Skill(skill="skills:consolidation", args="## Task\n[full feature description from $ARGUMENTS]\n\n## Acceptance criteria\n[from Phase 0]\n\n## Constraints\n- TDD: write failing tests before implementation for every subtask\n- Every subtask must include its own tests\n- Follow project conventions\n\n## Working directory\n[cwd]")
```

The cycle handles:
1. **Planner** — decomposes the feature into subtasks, maps files and dependencies
2. **Verifier** — validates the plan for correctness and efficiency
3. **Parallel architects** — execute subtasks in worktrees (each doing TDD red-green-refactor)
4. **Consolidator** — merges all branches, resolves overlaps, wires integration points
5. **Reviewer** — reviews the merged output, fixes are applied
6. **Verifier** — confirms all acceptance criteria are met, tests pass, lint clean

The skill runs in *your* context: you conduct it (the consolidation skill decides whether to delegate workstreams to `conductor` subagents).

## Phase 2: Commit

After the cycle completes, delegate to `skills:commit` (or `skills:commit-all` if multiple logical groups).

## Completion Criteria

The cycle's final verifier confirms these before it ends, but double-check:

1. ALL tests pass
2. Code is reviewed (reviewer) and issues addressed
3. No TODOs or placeholders in code
4. Feature works end-to-end
5. Lint and build pass

## Hard Rules

1. **NO STOPPING MID-FEATURE** — complete the entire task
2. **NO SKIPPING TESTS** — TDD is mandatory (communicated via skill args)
3. **NO PLACEHOLDERS** — implement fully or don't start
4. **ASK QUESTIONS EARLY** — don't guess requirements (Phase 0)
5. **NO "PRE-EXISTING" EXCUSES** — if any test fails, fix it. Always complete with passing tests.
