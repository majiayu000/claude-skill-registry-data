---
name: dependency-upgrade
description: >-
  Upgrade dependencies safely: read changelogs, classify breaking changes,
  stage bumps, and gate on tests. Use when updating packages, resolving
  security advisories (npm audit, dependabot), upgrading a framework or
  runtime version, or unpinning stale dependencies. Do not use for adding a
  brand-new dependency (that's a design choice — consider architecture).
---

# Dependency Upgrade

An upgrade is someone else's breaking-change list applied to your code. Read it before you take it.

## Workflow

1. **Inventory** — what's being upgraded and why (security advisory, staleness, feature need). Current version → target version. Note whether it's a direct or transitive dependency; transitive fixes may only need a resolution/override.
2. **Read the release notes between the versions** — actual changelogs/migration guides, all majors in the jump (`v2 → v4` means reading v3's breaking list too). Extract: breaking changes, deprecations, behavior changes, new peer/runtime requirements.
3. **Map breakage to this codebase** — search for each breaking API's usage. The result is a concrete edit list, possibly empty. Unknown usage (dynamic access, config-driven) → flag it, don't assume absence.
4. **Stage the bumps** — one major at a time; separate commits per risky package (or tight group). Security patches for unrelated packages don't ride along with a framework major.
5. **Gate each stage** — install clean (lockfile updated intentionally), typecheck, lint, run the test suite, and exercise the feature areas the changelog flagged. For a security advisory: verify the vulnerable path is actually gone (`npm audit` / equivalent re-run).
6. **Watch for silent behavior changes** — defaults that flipped, stricter parsing, changed serialization. The taxonomy in the `contract-guard` skill applies: if the upgraded dependency sits behind one of *your* external contracts, confirm your own surface didn't change with it.
7. **Record** — commit message lists package, version range, notable breaking changes handled, and evidence run. Update pinned-version docs if the project keeps them.

## Constraints

- Never bulk-upgrade everything to latest in one commit "while at it".
- A green suite after a major bump with zero code changes deserves suspicion, not celebration — check the suite actually covers the usage.
- Don't suppress peer-dependency warnings with force flags; resolve them or defer the upgrade with a note.
- Runtime/toolchain upgrades (Node, TypeScript, database) get the same treatment plus a check of CI images and deploy targets.

## Verification

- [ ] Release notes read across the full version jump
- [ ] Usage of each breaking API located (or absence confirmed)
- [ ] Bumps staged, one risky upgrade per commit
- [ ] Full gate run per stage (install, typecheck, lint, tests, flagged areas)
- [ ] Security advisories: vulnerability confirmed resolved
- [ ] Own external contracts unaffected (contract-guard check when applicable)
