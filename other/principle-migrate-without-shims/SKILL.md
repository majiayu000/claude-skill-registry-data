---
name: principle-migrate-without-shims
description: Apply when replacing an internal API that no external user depends on, as part of a simplification in a project that can absorb a coordinated break; or when running a planned rewrite or migration with declared phase boundaries.
disable-model-invocation: true
---

# Migrate without shims

Converge on the target design instead of carrying compatibility code toward it.

## Replacing an internal API

Only when all three hold: nothing outside depends on the API, the change is
part of a simplification, and the project can absorb a coordinated breaking
change. If any fails, this branch does not apply.

- Migrate every caller and delete the old API in the same change, with no
  compatibility layer left behind.

## A planned migration with declared phase boundaries

- An authorized migration group with declared interior breakage is one
  verifiable unit. Only its declared breakage is allowed; any undeclared
  failure stops the work; its boundary checks pass before dependent work
  proceeds.
- Keep fast, high-signal checks running on the areas being changed throughout.
- At the end of the migration or rewrite, run the full static and runtime
  verification, not only the checks the last change touched.
