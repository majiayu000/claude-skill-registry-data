---
name: refactor-code
description: Restructure code to improve clarity, maintainability, or design without intentionally changing external behavior. Use when the task is to clean up implementation, reduce duplication, simplify logic, or prepare code for future work.
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash, git]
---

# Refactor Code

Use this skill for behavior-preserving structural improvement.

---

## Rules

- Preserve external behavior unless the user explicitly asks for a behavior change
- Define the refactor target before editing
- Prefer small, reviewable transformations over broad rewrites
- Keep validation tight throughout the work
- Stop and call out any case where cleanup exposes a real behavior bug

---

## Step 1 — Define the Refactor Goal

Identify the primary reason:

- Duplication
- Hard-to-follow control flow
- Poor separation of concerns
- Naming or structure that blocks future work
- Excessive coupling or repeated special cases

State what must remain behaviorally unchanged.

---

## Step 2 — Inspect the Current Shape

Trace:

- The existing call path
- Shared dependencies and invariants
- Current tests that protect the behavior
- The smallest safe edit boundary

---

## Step 3 — Perform the Refactor

Prefer transformations such as:

- Extracting coherent helpers
- Consolidating duplicate logic
- Simplifying branching
- Improving module boundaries
- Renaming for clarity where the codebase already supports it safely

Avoid mixing unrelated cleanup into the same change.

---

## Step 4 — Verify Behavior Preservation

Run the closest relevant tests or build command first:

```bash
<targeted test/build command>
```

Then widen if the refactor touched shared code.

---

## Output

Return:

- Refactor goal
- Files changed
- Validation run
- Any residual behavior risk

---

## Done Criteria

The refactor is complete only when:

- The structural goal was defined
- The affected code path was inspected
- The cleanup was implemented
- Behavior-preservation validation was attempted when feasible
