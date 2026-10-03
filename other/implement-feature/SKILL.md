---
name: implement-feature
description: Plan and implement a new feature or enhancement in an existing codebase. Use when the task is to add behavior, extend a workflow, or ship a scoped product or engineering change rather than fix a defect.
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash, git]
---

# Implement Feature

Use this skill for new feature work and scoped enhancements.

---

## Rules

- Identify user-visible behavior and acceptance criteria before editing
- Trace the existing architecture before choosing an implementation path
- Prefer changes that fit existing patterns unless the user asks for a structural shift
- Keep the implementation scoped to the requested outcome
- Add or update tests when the repository supports them

---

## Step 1 — Define the Target Behavior

Establish:

- What the feature should do
- What should remain unchanged
- Entry points, screens, endpoints, or services affected
- Constraints from existing architecture or product behavior

If requirements are ambiguous, make the smallest reasonable assumption and surface it.

---

## Step 2 — Inspect the Existing Path

Read only the relevant code needed to map:

- Current behavior
- State and data flow
- Integration points
- Existing tests covering adjacent logic

Prefer small extensions to proven code paths over parallel implementations.

---

## Step 3 — Implement

When editing:

- Reuse existing abstractions where they remain coherent
- Avoid broad cleanup unless it is required for correctness
- Keep related changes grouped so the resulting diff is reviewable
- Add concise comments only for non-obvious logic

---

## Step 4 — Verify

Run the narrowest meaningful validation first:

```bash
<targeted test/build command>
```

Then widen validation if the change crosses module boundaries.

---

## Output

Return:

- What was implemented
- Files changed
- Validation run
- Notable tradeoffs or follow-ups

---

## Done Criteria

The feature work is complete only when:

- Target behavior was defined
- Relevant code paths were inspected
- The feature was implemented in code
- Validation was attempted when feasible
