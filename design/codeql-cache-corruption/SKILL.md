---
name: codeql-cache-corruption
description: >-
  Use when a CodeQL analysis step fails with "Invalid checksum for page N of the compressed relation
  ... The database is corrupt and should be re-created", when one branch reddens the
  security-testing workflow identically on every re-run while other branches stay green, or when
  reviewing an actions/cache step that caches a CodeQL database directory behind a restore-keys
  prefix.
---

# CodeQL cache corruption

## Profile keys consumed

- `ci.provider`
- `ci.workflows`

## Overview

A CodeQL database is valid only for the source tree it was built from. Caching that directory under
a key that does not identify the tree lets a database built elsewhere be restored over a different
checkout, and CodeQL aborts on a checksum mismatch. The corruption is sticky: every re-run restores
the same poisoned entry.

## When to use

- The analysis step reports an invalid checksum for a compressed relation and says the database
  should be re-created.
- The same branch fails identically on three consecutive re-runs, including a fresh one — a flake
  would not be deterministic.
- Only one or a few branches fail; the default branch is green.
- A build from a clean branch succeeds against the same commit range.
- Reviewing or porting a workflow that caches a CodeQL database directory.
- Not for: CodeQL alerts, query-pack failures, or an analysis that runs and reports findings.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): no — no CodeQL database cache.
- **Next.js app shape** (routed pages, no aggregate duplication gate): yes — the security-analysis
  workflow listed under `ci.workflows` caches `codeql_databases` keyed on the OS plus a `bun.lock`
  hash, with an OS-prefix `restore-keys` fallback, and pins the CodeQL action's `db-location` to
  that path.
- **Component-library shape** (Storybook-first, no bootable app, published package): yes — the same
  cache shape.

## Procedure

1. Confirm the diagnosis: checksum error, deterministic across re-runs, isolated to one ref.
2. Clear the poisoned entry. In the CI provider named by `ci.provider`, under the repository's
   **Settings > Actions > Caches**, filter by the failing ref (a pull-request ref looks like
   `refs/pull/<number>/merge`), delete every entry matching the cache key prefix (`Linux-codeql-`),
   and re-run the workflow. The next run rebuilds the database from scratch, so this is
   self-healing.
3. Fix the key design on the default branch — the branch that failed cannot fix it for anyone else.

## Why the key is unsound

```yaml
key: ${{ runner.os }}-codeql-${{ hashFiles('**/bun.lock') }}
restore-keys: |
  ${{ runner.os }}-codeql-
```

Neither line identifies the tree. The primary key hashes only the lockfile, so every commit that
leaves dependencies alone shares one key; the `restore-keys` prefix widens that to any commit on any
ref. Two remedies, in order of preference:

- **Drop the database cache.** CodeQL's own overlay-base caching already reuses analysis across
  commits, so an explicit database cache buys little and risks this failure.
- **Key on the commit.** Use `${{ github.sha }}` as the key and omit `restore-keys` entirely, so a
  miss rebuilds instead of restoring a foreign tree.

## Common mistakes

- Re-running the failed workflow without purging the cache — the same entry is restored, so delete
  it first and re-run afterwards.
- Treating it as flakiness and retrying — deterministic repetition is the tell that it is not.
- Adding the tree-specific key to the failing branch only — the cache is written from the default
  branch too, so the fix has to land there.
- Keeping a `restore-keys` fallback "just for warm starts" — that fallback is the defect.
- Changing `db-location` without moving the cache `path` — the cache step then caches nothing and
  the failure looks fixed until the next warm run.
