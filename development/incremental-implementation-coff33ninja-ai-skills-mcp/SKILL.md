---
name: incremental-implementation
description: Breaks changes into thin vertical slices. Start with a minimal end-to-end slice, then add layers. Prevents massive diffs that are impossible to review and merge conflicts from long-lived branches.
---

# Incremental Implementation

## Problem it solves

Large changes are risky and hard to review:
- Massive diffs that reviewers (human or AI) cannot meaningfully review
- Long-lived branches that drift from main and cause merge conflicts
- No partial rollback — if something goes wrong, the entire change is lost
- Difficulty isolating which change caused a regression
- High cognitive load from holding the entire change in your head at once

## Protocol

### 1. Plan the slices

Before coding, decompose the work into thin vertical slices:

A slice is:
- **End-to-end**: crosses all layers (UI → API → logic → data), not a horizontal layer
- **Independently valuable**: could be shipped alone (even if hidden behind a flag)
- **Reviewable**: under ~200 lines of diff
- **Testable**: can be verified independently

Bad slicing (horizontal):
```
Layer 1: Database schema
Layer 2: API endpoints
Layer 3: Business logic
Layer 4: UI
```

Good slicing (vertical):
```
Slice 1: Read-only list view (no auth, no editing)
Slice 2: Add item form
Slice 3: Edit item form
Slice 4: Authentication
```

### 2. Start with the thinnest possible end-to-end slice

Build the smallest vertical slice that proves the concept works end-to-end:
- A single working path from input to output
- Hardcode what you can, add configuration later
- Skip error handling for now — handle only the happy path
- Use stubs/mocks for anything not in this slice

### 3. Each slice is RED → GREEN → REFACTOR

Per slice:
1. Write the spec for this slice only
2. Write tests (see test-driven-development)
3. Implement the minimal code to pass
4. Refactor within the slice
5. Review (see code-review)
6. Merge to main before starting the next slice

### 4. Feature flags for incomplete slices

If a slice cannot ship without all slices complete:
- Wrap new behavior in a feature flag
- Default the flag to off
- Only enable when all slices are complete

### 5. Keep slices independent

- Do not build slice N+1 until slice N is merged
- Each slice should have zero dependencies on unmerged work
- If slices are interdependent, they are not properly sliced — re-plan

### 6. Handle discovered scope

If mid-implementation you discover something the spec missed:
- Do NOT expand the current slice
- Add it to the plan for a future slice
- Keep the current slice focused

## Detection triggers

Activate when:
- Starting a feature that requires more than one file change
- The diff would exceed ~200 lines
- User describes a multi-step feature
- User says "build this" and the scope is non-trivial

## When NOT to use

- Trivial changes (single file, clear intent, <50 lines)
- Emergency fixes that need to ship immediately
- Prototyping or exploration (spike first, then incremental implementation)
- User explicitly says "just do it all at once"

## Cross-references

- **spec-driven-development** — Write the overall spec first, then decompose into slice specs.

- **test-driven-development** — Each slice follows TDD: write tests, implement, refactor.

- **code-review** — Slices are sized for review. Each slice should be reviewable in one pass.

- **git-workflow-conventional-commits** — Each slice produces atomic commits. One slice = one or more conventional commits.

- **anti-premature-termination** — Do not declare the feature done until all slices are merged and verified.

- **follow-existing-patterns** — Each slice must follow the project's existing patterns. Don't start with perfect patterns — refactor toward them across slices.
