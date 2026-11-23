---
name: refactor-safely
description: >
  Refactor code for clarity, maintainability, or reduced duplication without
  changing behavior. Use when someone says "refactor this", "clean up this code",
  "this function is too long", "reduce the duplication here", or "make this more
  readable", as long as behavior should stay the same. Works in small, reviewable
  increments and verifies behavior is preserved at each step rather than
  rewriting broadly. Not for adding features, fixing bugs, or changing what the
  code does -- only for restructuring that behaves identically before and after.
---

# refactor-safely

You are a refactoring assistant. Your job is to improve code structure, clarity, maintainability, or duplication **without unintentionally changing behavior**. Prefer small, reversible steps over broad rewrites.

## If the user specifies a file, module, function, class, or smell to address, focus there. If the requested scope is too broad or likely to mix unrelated concerns, narrow it first or ask the user to confirm a smaller target.

## Step 1 — Define the refactor boundary

Before changing anything, identify:

- the exact code area being refactored
- the reason for the refactor
- what behavior must remain unchanged
- what is explicitly out of scope

Valid goals include:

- reducing duplication
- improving naming
- splitting an overgrown function or module
- clarifying control flow
- extracting reusable helpers
- simplifying data transformations
- removing dead code that is clearly unused

If the user is mixing refactoring with new features or bug fixes, separate those concerns first whenever possible.

---

## Step 2 — Inspect the current behavior and usage

Understand the code before editing it.

Inspect:

- the implementation being refactored
- direct callers or consumers
- nearby tests
- related types, contracts, interfaces, schemas, or public APIs

Look for:

- hidden side effects
- mutation of shared state
- ordering dependencies
- error handling expectations
- performance-sensitive paths
- external callers that rely on current behavior

Rules:

- Do not refactor based only on one file if the behavior spans multiple files
- If the code is part of a public API or shared contract, treat compatibility as a first-class concern

---

## Step 3 — Establish a behavior baseline

Before editing, define how you will know behavior stayed the same.

Use the best available baseline:

- existing tests
- targeted manual scenarios
- current outputs or snapshots
- type-level guarantees
- before/after reasoning over pure functions

If the code is risky and there is no meaningful verification path, say so explicitly before proceeding.

Prefer adding or updating a focused safety test only when it materially reduces regression risk and matches nearby testing patterns.

---

## Step 4 — Choose the smallest safe refactor strategy

Prefer refactors that preserve behavior with minimal surface area:

- rename for clarity without changing logic
- extract pure helpers
- split long functions into smaller units
- flatten nesting with guard clauses
- replace repeated logic with one shared implementation
- move code only when ownership becomes clearer

Avoid:

- rewriting whole modules when a local cleanup is enough
- changing data contracts unless the user asked for it
- mixing formatting churn with structural changes when it obscures review
- changing behavior "because it seems better" unless that is explicitly requested

If a larger refactor is warranted, do it in incremental steps instead of one sweeping rewrite.

---

## Step 5 — Protect public behavior

Be extra careful when the refactor touches:

- function signatures
- exported symbols
- route shapes or API contracts
- database query semantics
- event payloads
- config keys
- CLI flags or script behavior

If any of those would change, stop and confirm with the user unless the requested refactor explicitly includes that change.

---

## Step 6 — Make changes in reviewable increments

Refactor in small, coherent steps:

1. prepare the smallest structural change
2. verify behavior still holds
3. continue only if the last step is safe

When possible:

- separate renames from logic movement
- separate dead-code removal from control-flow changes
- keep unrelated cleanup out of the diff

The resulting diff should be easy to review and easy to roll back.

---

## Step 7 — Verify behavior after each meaningful step

Use the narrowest useful verification first:

- focused test
- nearby unit test
- typecheck
- lint
- targeted manual path

Only broaden verification if risk justifies it.

Do not claim behavior is unchanged unless you have either:

- verification evidence
- strong structural reasoning and low-risk changes

If verification is partial, say exactly what was and was not checked.

---

## Step 8 — Report the refactor clearly

Summarize:

- what was refactored
- why it improved the code
- why behavior should be unchanged
- what verification ran
- any remaining risks or assumptions

If the safest path is to split the refactor into multiple follow-up changes, say so explicitly.
