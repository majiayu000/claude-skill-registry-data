---
description: Execute a plan task-by-task with TDD discipline and progress tracking
---

# Build

Execute the implementation plan for "$ARGUMENTS" task-by-task, following test-driven development discipline.

## Prerequisites

Read `.metapowers/development/$ARGUMENTS/01-plan.md`. If this file does not exist, tell the user:

> No plan exists for "$ARGUMENTS". Run `/development:plan $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check and log to `.metapowers/development/$ARGUMENTS/skip-log.md`.

## Process

For each task in the plan:

1. **Write the failing test first:**
   - Write the test that verifies the task's expected behavior
   - Run the test suite — confirm the new test fails
   - If it passes without implementation, the test isn't testing anything — rewrite it

2. **Implement the minimal code to pass:**
   - Write only what's needed to make the failing test pass
   - Don't add features, refactor, or "improve" beyond the task scope
   - Follow existing codebase patterns and conventions

3. **Verify:**
   - Run the full test suite — all tests must pass
   - If other tests broke, fix them before moving on

4. **Commit:**
   - Stage the relevant files
   - Write a clear commit message following the project's convention

5. **Log progress** — after each task, append to the execution log:
   - Task name and status (completed/skipped/blocked)
   - Commit hash
   - Any issues encountered

6. **Write the artifact** to `.metapowers/development/$ARGUMENTS/02-build.md`

## Output

The execution log written to `.metapowers/development/$ARGUMENTS/02-build.md`. Present a summary to the user highlighting:
- Tasks completed vs. total
- All commits made
- Any issues or deviations from the plan
