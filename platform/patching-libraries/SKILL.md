---
name: patching-libraries
description: Patching, forking or replacing broken third-party libraries. Use when a dependency has a bug with no released fix, for patch-package versus fork decisions, patches breaking after an upgrade, or an abandoned library.
user-invocable: false
---

# Patching third-party libraries without regret

## The decision ladder

Work down, stop at the first rung that holds:

1. **A released fix exists**: upgrade. Check the library's releases and the issue matching your exact error before doing anything clever.
2. **The fix is small and upstream is alive**: patch locally AND open the upstream PR (or link the existing one). The patch is a bridge, not a home.
3. **The fix is small and upstream is dead**: patch locally and put the library on the replacement list. A patched corpse is still a corpse.
4. **The library is dead and load-bearing**: replace it with the maintained alternative. The new-architecture skill lists the standard swaps.
5. **No alternative exists and the code is small**: vendor it (copy the source into the repo, keep its license header, own it openly). Honest ownership beats a fork nobody watches.
6. **Fork** only when you truly need a living divergent copy. A fork is a maintenance subscription with no unsubscribe button: every upstream fix, security patch and New Architecture change becomes your homework.

## Patch mechanics

The classic tool is patch-package (edit inside node_modules, run it, commit the generated diff, apply via a postinstall script). Modern package managers carry the same idea natively: `pnpm patch`, `yarn patch`, `bun patch`. Use whichever matches the repo's package manager; mixing patch-package into a pnpm repo when `pnpm patch` exists just adds a second mechanism to forget about.

Discipline that keeps patches from rotting:

- Every patch carries a comment block at the top of the change or in the patch file's name area: WHY it exists and the upstream issue/PR link. A patch without a link is undeletable, because nobody remembers when it is safe to remove.
- Patches are pinned to exact library versions. That is a feature: after any dependency upgrade, a failing patch application is the system telling you to re-check whether upstream fixed it. Re-diff or delete; never blindly re-roll.
- Review patches in PRs with the same care as first-party code. They ARE first-party code now.
- Keep count. One or two patches is normal life; ten is a sign the dependency choices need revisiting, not the patching tooling.

## Failure modes worth knowing in advance

- **Patch applies locally, fails in CI**: the lockfile resolved a different version of the library in CI, or the postinstall hook order differs. Compare resolved versions first.
- **Patch silently no-ops after an SDK upgrade**: the file you patched moved or was rewritten. This is why the upgrade workflow re-validates every patch as a standard step.
- **Patching build files** (gradle files, podspecs) works but is the most fragile category; those files churn with every toolchain release. Prefer config-level overrides (build properties, resolution strategies) when the platform offers one.
- **Patching native code in a CNG/prebuild project**: patches against `node_modules` survive prebuild fine; patches against the generated `ios/`/`android/` folders are erased by design. If you find yourself patching generated folders, the change belongs in a config plugin instead.

## The exit habit

Once a quarter, or at every SDK upgrade, walk the patch directory: for each patch, is the upstream issue closed? A patch whose upstream fix shipped is negative value: it hides the real version from you. Deleting patches feels like losing work; it is actually the payoff.
