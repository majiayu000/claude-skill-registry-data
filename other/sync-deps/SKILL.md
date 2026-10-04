---
name: sync-deps
description: Regenerate deps-lock.json after changing deps.edn
---

# Sync Dependencies Lock File

Regenerate `deps-lock.json` after changing `deps.edn`.

## Background

The uberjar build consumes `deps-lock.json` (a clj-nix lock file, wired in as a
flake input) to cache Maven/Clojure dependencies. When `deps.edn` changes, the
lock file must be regenerated or the uberjar build resolves stale dependencies.

## Process

1. Run: `just deps-lock`

2. Check the result: `git diff --stat deps-lock.json`

   An unchanged lock file is fine — it means the resolved artifact set did not
   change (e.g. a dependency was promoted from transitive to explicit at the
   same version).

3. If the lock file changed, verify the uberjar still builds:
   `nix build .#bits-uberjar`

4. Commit `deps.edn` and `deps-lock.json` together.

$ARGUMENTS
