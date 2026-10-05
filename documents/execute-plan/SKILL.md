---
name: execute-plan
description: Execute a previously created implementation plan — implement, test, document, and close out. Use when a plan file exists and is ready for implementation.
---

# Execute Implementation Plan

You have been given a plan file. Your job is to **implement it fully** — code, test, document, and close out.

## Instructions

### 1. Read the Plan

- Read the attached plan file completely.
- Understand every section: Context, Current State, Target State, Implementation Steps, Testing Plan, Post-Implementation Checklist.
- Note the gate structure.

### 2. Review Recent Context

- Read latest task log(s) in `docs/task/logs/`.
- Read `docs/task/todo.md` for conflicts.
- Read `docs/task/lessons.md` for relevant lessons.
- Read agent observation logs in `docs/agent-observations/` for relevant unresolved items.

If the plan is stale or conflicts, **STOP and tell the user**.

### 3. Execute Implementation Steps

Work through each step in order:
- Mark checkboxes as you complete them.
- Follow exact file paths, line numbers, and descriptions.
- If line numbers have drifted, locate by context.
- If blocked or plan is wrong, **STOP and tell the user**.

### 4. Execute Testing Plan (BLOCKING)

After ALL implementation steps, execute the Testing Plan:
1. Run every Automated Check.
2. Execute every Browser Verification step using Chrome MCP tools. Log in at `http://localhost:8080/wp-admin` (admin/password). Resize to 1900×1200.
3. Execute every Regression Check.
4. Verify Edge Cases.

**Reading code is not testing. You must use Chrome MCP tools for UI verification.** If any test fails, fix and re-test.

### 5. Documentation & Logging (only after testing passes)

1. Update affected documentation per the trigger map in `AGENTS.md`.
2. Add task log entry to today's `docs/task/logs/YYYY-MM-DD.md`.
3. Log observations to `docs/agent-observations/`. If none: "Observations: none."

### 6. Close Out

1. Update plan status to **Complete**.
2. Mark all Post-Implementation Checklist items checked.
3. Remove task from `docs/task/todo.md`.
4. Move plan file from `draft/` to `completed/`.
5. Confirm to user: what was done, what was tested, result.

## Rules

- **Follow the plan exactly.** No adding/skipping/reordering unless blocked.
- **Testing is not optional.** Gate 2 must pass before Gate 3.
- **Do not ask the user to test.** You are the tester.
- **If the plan is outdated**, STOP and tell the user.
- **Do not close with undocumented observations.**
- **No backup files in source directories.**
- **Follow all rules in `AGENTS.md`.**
