---
name: migration-pilot
description: Plan and execute framework, dependency, API, database, config, repository, or naming migrations safely. Use when the user asks to upgrade versions, rename projects, move files, change public contracts, migrate schemas, replace libraries, or perform codemods. Do not use for small isolated edits that have no compatibility or rollout risk.
---

# Migration Pilot

Move systems without losing behavior.

## Workflow

1. Inventory every affected surface: imports, config, docs, tests, scripts, CI, generated files, public APIs, and deployment settings.
2. Identify compatibility constraints and consumers.
3. Choose migration shape:
   - Big bang for tiny private changes.
   - Compatibility layer for public or cross-module contracts.
   - Dual-write/read or backfill for data migrations.
   - Codemod for repeated mechanical edits.
4. Make the smallest reversible slice first.
5. Run targeted verification after each slice.
6. Update docs and cleanup only after the new path is proven.

## Risk Controls

- Preserve old names temporarily when callers may still use them.
- Add deprecation notes before removal.
- Keep rollback notes for releases and database changes.
- Avoid mixing migration with unrelated refactors.
- Check lockfiles, generated artifacts, and examples.

## Output

Use:

```text
Inventory:
Migration strategy:
Compatibility plan:
Implementation slices:
Verification:
Rollback:
Cleanup:
```
