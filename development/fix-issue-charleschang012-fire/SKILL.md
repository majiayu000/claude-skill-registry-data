---
name: fix-issue
description: Reproduce a bug or regression, identify the root cause, implement a targeted fix, and verify the result. Use when the task is to fix an issue, investigate a failing test, or correct broken behavior in an existing codebase.
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash, git]
---

# Fix Issue

Use this skill for bug fixing and targeted corrective implementation work.

---

## Rules

- Start by locating the relevant code path, test, and failure surface before editing
- Prefer `rg` / `rg --files` for search
- Reproduce with the smallest trustworthy case available
- Prefer minimal root-cause fixes over broad rewrites
- Do not revert unrelated user changes
- Verify with the narrowest meaningful test first, then widen scope if needed
- State uncertainty explicitly if the issue cannot be reproduced locally

---

## Step 1 — Scope the Failure

Establish:

- Expected behavior
- Actual behavior
- Reproduction steps
- Likely files, modules, or services involved

If a failing test already exists, use it as the primary entry point.

---

## Step 2 — Reproduce Before Editing

Prefer one or more of:

```bash
rg -n "<error text|symbol|route|function>"
```

```bash
<project test command for the narrow failing case>
```

```bash
git diff --stat
```

Capture the concrete symptom:

- Failing test
- Build error
- Runtime error
- Incorrect output or state transition

If local reproduction is not possible, continue with code-path analysis and say so plainly.

---

## Step 3 — Fix the Root Cause

When editing:

- Preserve existing project patterns
- Add or update tests when the repo supports them
- Avoid speculative refactors unless required to make the fix safe
- Add concise comments only where the logic would otherwise be hard to parse

---

## Step 4 — Verify

Run the smallest meaningful validation first:

```bash
<targeted test command>
```

Then run broader validation only if warranted:

```bash
<broader test/build/lint command>
```

Report:

- What changed
- Why it fixes the issue
- What was verified
- Remaining risk, if any

---

## Output

Return a compact implementation summary:

- Root cause
- Files changed
- Validation run
- Residual risks or follow-ups

---

## Done Criteria

The task is complete only when:

- The relevant code path was inspected
- A concrete fix was implemented or the blocker was clearly identified
- Validation was attempted when feasible
- The final response states outcome and remaining risk
