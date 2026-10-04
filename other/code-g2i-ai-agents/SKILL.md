---
name: code
description: Implement production changes with or without new test coverage.
---

# Code

## Invocation

This skill is performed in the `Developer` persona. If you are not already running as `Developer` (for example, the user invoked `/code` directly), read `subagents/developer.md` and adopt its role guidance for the rest of this task. Stay in the current chat—do not delegate to a subagent.

## Objective

Implement the requested change using existing project patterns. This skill covers spec-driven feature work and implementation tasks that are not primarily about new automated tests.

## Instructions

1. Ask for the spec path when the work is spec-driven. If there is no spec, clarify the requested scope and success criteria.
2. Determine whether the change should be test-first:
   - if yes, route to `/tdd` before implementation
   - if not, continue here
3. Read the relevant code paths and follow existing patterns before introducing new structure.
4. Follow the repo's established architecture and conventions.
5. Implement the smallest coherent change that satisfies the task.
6. Run the verification checks that fit the change (linting, type checking, tests, builds, etc.).
7. Summarize the implementation, affected files, checks run, and recommended next step (`/review` or `/draft-pr`).

## Notes

- `code` remains distinct from `/tdd` because some implementation work in this repo does not justify a test-first flow.
- When opening a PR or preparing a review, treat your base branch as the comparison target.
