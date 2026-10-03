---
name: minimalist-audit
description: >
  Audit a codebase or directory for deletion candidates: dead code, unused
  dependencies, single-use abstractions, config that never varies, and
  duplicated helpers. Use when the user says "minimalist audit" or asks
  what can be deleted from a project.
license: MIT
---

# Minimalist Audit

Walk the target and produce a ranked deletion list. For each candidate:
`path — est. LOC removable — evidence — risk (low/med/high)`.

Look for:
1. Exports with zero references (verify by searching, don't guess).
2. Dependencies in the manifest never imported, or imported for one function the stdlib has.
3. Abstractions (interfaces, factories, base classes) with exactly one concrete user.
4. Config values that have never differed between environments.
5. Copy-pasted helpers that already exist elsewhere in the repo.
6. Commented-out code and "TODO later" scaffolding older than the file's median age.

End with a one-paragraph summary: total estimated removable LOC and the top
three lowest-risk deletions to start with. Never mark tests, validation, auth
or error paths as dead without proven zero references.
