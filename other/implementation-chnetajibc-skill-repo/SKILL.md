---
name: implementation
description: "Implement as thin vertical slices: implement, test, verify, commit with flags and safe defaults."
---

# implementation

One thin slice at a time: implement, test, verify, commit. Each slice shippable, each commit revertable.

## Activate when

- Any multi-file change; every feature, fix, or migration task.

## Do NOT activate for

- Single-line trivial edits (still test, but inline the workflow).

## Procedure

1. Slice: one behavior per slice, ordered by dependency; feature-flag incomplete paths so main stays deployable.
2. Inspect before writing: read the target module, its tests, and its conventions; match them.
3. Implement the slice: minimal diff, safe defaults, no unrelated changes, no speculative abstractions.
4. Security hooks (activate when the slice touches these): auth paths → backend/authorization; user input → backend/validation; secrets/config → security/secrets-supply-chain; DB queries → databases/database-security; new deps → core/dependency-research. Source-to-sink reasoning for every finding, not generic lists.
5. Test the slice now (see core/testing); run typecheck/lint for the repo.
6. Commit atomically with a conventional message; push behind CI.
7. Verify: slice behavior demonstrated (test output or runtime evidence), no scope creep in the diff, gates green.
8. On verification failure: revert the slice (not patch-on-patch), diagnose per core/debugging, re-implement. Two failed verifications → stop and re-plan.

## References

- Related: `../testing/`, `../debugging/`, `../code-review/`, `../../git/git-workflow/`.
