---
name: refactor
description: Safe refactoring with diagnostics, tests, and architectural guidance
disable-model-invocation: true
user-invocable: true
argument-hint: "<what to refactor>"
---

# Safe Refactor

Refactor the following: $ARGUMENTS

## Process

1. **Assess** — Before changing anything:
   - Read the code to understand current structure
   - Run existing tests to establish baseline
   - Identify all callers/consumers of the code being refactored

2. **Plan** — Determine the refactoring approach:
   - For architectural changes, use Agent(subagent_type="Plan") first
   - Break large refactors into small, testable steps
   - Identify risks and rollback points

3. **Execute** — Apply changes incrementally:
   - Make one logical change at a time
   - Run tests after each step
   - Verify no regressions before proceeding

4. **Verify** — After all changes:
   - Run full test suite
   - Check for type errors / lint issues
   - Confirm all callers still work correctly

## Rules

- Never refactor and add features simultaneously
- Maintain backward compatibility unless explicitly asked to break it
- Each step should leave the codebase in a working state
- If tests don't exist for the code being refactored, write them first
