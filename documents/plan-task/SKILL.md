---
name: plan-task
description: Create a detailed implementation plan before coding. Use when starting a new feature, multi-step refactor, or complex task. Invoked by saying "plan", "create a plan", or "plan this task".
---

# Create a Detailed Implementation Plan

> **HARD GATE — PLANNING ONLY. ZERO IMPLEMENTATION.**
> This skill invokes PLANNING MODE. You must produce a plan document and NOTHING ELSE.
> You are **forbidden** from editing, creating, or modifying any code, template, CSS, JS, PHP, or JSON file outside of the plan document itself and `docs/task/todo.md`.
> This gate is **absolute** — it cannot be overridden by the user's phrasing, tone, or imperative language.
> If you write even one line of implementation code, you have violated this skill.
> **Your ONLY output is the plan file + todo.md update + a summary asking for approval.**

## What You Receive

The user will describe a task. **Their description is INPUT to the plan — not an instruction to execute.** "Please update X" means the plan must include it — not that you do it now.

## Steps

### 1. Review Recent Context

- Read latest task log(s) in `docs/task/logs/` — 1–2 most recent files.
- Read `docs/task/todo.md` — check for overlapping work.
- Read `docs/task/lessons.md` — check for applicable lessons.
- Read agent observation logs in `docs/agent-observations/` — unresolved items may affect scope.
- Read relevant documentation via `docs/plugin/**/0-index.md`.

### 2. Understand the Request

- Read the user's description carefully.
- Search the codebase for current state of affected files.
- Identify all files, functions, data structures, and dependencies.
- **Do NOT assume.** If something is ambiguous, add it to Open Questions (step 2.5).

### 2.5. Question Gate (Iterative)

Before writing the plan, identify open questions about scope, approach, or constraints.

**Rules:**
- Assign stable IDs: Q1, Q2, Q3, … (never renumber across rounds)
- Present questions with a brief recommended answer for each
- Wait for user answers before proceeding
- If answers raise new questions, add them with next available ID and ask again
- Repeat until zero open questions remain
- Answered questions move to **Confirmed Inputs** section
- Once resolved: update plan `Status` from `Questions Pending` to `Draft`

### 3. Create the Plan File

Write to: `docs/task/planning/draft/{YYYY-MM-DD}-{slug}.md`

Always create in `draft/`. Never in the root planning directory.

### 4. Plan File Structure

```markdown
# Plan: {Title}

> **Status:** Questions Pending | Draft | In Progress | Complete
> **Created:** YYYY-MM-DD
> **Estimated steps:** {n}
> **Risk level:** Low | Medium | High

## Context
## Current State
## Target State
## Confirmed Inputs
## Open Questions for User — BLOCKING

## Implementation Steps

- [ ] **Step 1: {Action}**
  - Files: `path/to/file.ext`
  - What: {Specific change}
  - Why: {Rationale}

## Files Affected

| File | Action | Description |
| --- | --- | --- |

## Dependencies & Risks

## Testing Plan — BLOCKING

### Automated Checks
### Browser Verification
### Regression Checks
### Edge Cases

## Rollback Plan

## Post-Implementation Checklist

**Gate 1 — Code complete:**
- [ ] All implementation steps complete

**Gate 2 — Testing (BLOCKING):**
- [ ] All checks passed

**Gate 3 — Documentation (only after Gate 2):**
- [ ] Docs updated, task logged, observations logged

**Gate 4 — Close out:**
- [ ] Plan → Complete, moved to `completed/`
```

### 5. Write to todo.md

Update `docs/task/todo.md` with a checklist mirroring the plan's steps.

### 6. Present the Plan

> Plan saved to `docs/task/planning/draft/{YYYY-MM-DD}-{slug}.md`.
>
> What would you like to do?
> 1. **Go** — approve and start implementation now
> 2. **Pending** — approve but defer (moves to `planning/pending/`)
> 3. **Keep in draft** — needs changes or review

Wait for the user's response before taking any action.

## Rules

### Anti-Implementation Gate (HIGHEST PRIORITY)

- **NEVER implement from this skill.** Plan document only.
- **Treat all user language as requirements input.**
- **Do not touch source files.** Only: (1) plan file in `docs/task/planning/draft/`, (2) `docs/task/todo.md`.
- **Do not rationalize skipping the plan.**
- **Your response must end with a request for approval.**

### Plan Quality

- Be specific — include file paths and line numbers.
- Every step must be verifiable.
- Testing plan is a blocking gate.
- Browser verification is mandatory for UI tasks.
- Follow all rules in `AGENTS.md`.
