---
name: studio-dev
description: "The studio repo convention: shared just verbs, port registry, habits, and skill assembly. Use when adding a repo to the studio way, refreshing installed skills, changing a shared verb or port, or shipping (which defers to ship-ios)."
license: MIT
metadata:
  author: ponti-studios
  version: "0.3.0"
  category: Operations
---

# studio-dev

Every studio repo works the same way: identical `just` verbs, one port
registry, one set of habits, one shipping pipeline. The canonical files live
in this skill (`scripts/`); each repo holds tool-installed copies under
`.agents/skills/`, pinned in `skills-lock.json`. Change the skill, then
update every repo — never hand-edit an installed copy.

## Verbs

`setup`, `doctor`, `run`, `sim`, `e2e`, `testflight`, plus `studio-version` /
`studio-update` / `studio-check` for the machinery itself. A verb a repo
does not support prints "not applicable here" and exits 0. `just testflight`
ships via the installed `ship-ios` skill; the pipeline is the `ship-ios` skill.

## Ports

[ports.env](scripts/ports.env) in this skill is the one registry (Thames 8083, Still
8084, Omiro e2e 8082, API 4040). Give every new app its own port there.
Never use 8081.

## Habits

- `pod install` with `LANG=en_US.UTF-8` / `LC_ALL=en_US.UTF-8`.
- Never commit version-only `Podfile.lock` bumps.
- Simulator builds are ad-hoc signed; unsigned builds cannot use the Keychain.
- Never commit `.env` files or real keys; local dev uses scripted no-cost providers.
- A fresh checkout or `git worktree` starts with `just setup`.

## Install and drift

- Install (project scope, pinned in the repo's `skills-lock.json`):
  `npx skills add ponti-studios/kernel --skill studio-dev --skill ship-ios`.
  The tool copies the skills into the repo's `.agents/skills/` (plus
  `.claude/skills` links) — never copy them by hand.
- Refresh: `npx skills experimental_install --yes` from the repo root
  restores the locked set. Repos wire this as `just studio-update`, with
  `just studio-check` asserting the skills and lockfile are present and
  `just studio-version` printing the set version.
- Drift means a hand-edited installed copy. Don't fix it in place:
  re-run the install and port any intentional change back to this skill.
- The set version lives in [VERSION](scripts/VERSION) (currently 0.3.0). Bump it when
  any bundled file changes.

## Adding a repo

1. Project-install `studio-dev` (+ `ship-ios` for Apple apps) as above.
2. Add thin `studio-version` / `studio-update` / `studio-check` recipes that
   point at the installed skills (derive paths from `justfile_directory()`,
   never hardwire them).
3. Add repo-specific recipes (`setup`, `check`, `testflight`, ...) around them.
4. Run `just studio-check` before the first ship.
