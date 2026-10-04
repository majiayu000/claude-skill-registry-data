---
name: release-process
description: AI repo versioning and changelogs via release-please — never edit CHANGELOG.md or pyproject version by hand. Use when the user asks about releases, version bumps, changelogs, or preparing a release.
license: MIT
compatibility: claude cursor opencode
metadata:
  version: "1.0.0"
  languages: all
  audience: developers
  workflow: documentation
  since: "2026-05-22"
---

# Release process (release-please)

Versions and changelogs in this repo are **fully automated**. Do not manually edit release artifacts in feature PRs.

## What release-please owns

- Every workspace package `CHANGELOG.md`
- `version = "..."` in each package `pyproject.toml`
- `.release-please-manifest.json`

Config: `release-please-config.json` and manifest at repo root. Full lifecycle: `docs/contributing/release-process.md`.

## CI guard — do not bypass

`.github/scripts/check-no-manual-release.sh` **fails PRs** that modify:

- any `CHANGELOG.md`
- `.release-please-manifest.json`
- the `version = "..."` line in any `pyproject.toml`

Exception: release-please's own standing Release PR (opened by the Release Workflow App).

## What you do in a feature PR

1. Land code with **conventional commit** subjects (`git-conventional-commits` skill).
2. Use scopes that match the package path when helpful (e.g. `feat(sdk): ...`, `feat(toolkit): ...`).
3. Let release-please accumulate notes on the standing Release PR (title: `chore: stable release main` per `group-pull-request-title-pattern` in `release-please-config.json`; target CalVer is in the PR diff, not the title).
4. Merge the Release PR when ready to ship — release-please rewrites versions, changelogs, tags, and triggers PyPI publish.

| Intent | Commit type | Notes |
|--------|-------------|-------|
| New feature | `feat(scope): ...` | Appears under release notes |
| Bug fix | `fix(scope): ...` | Bug Fixes section |
| Breaking change | `feat(scope)!: ...` + `BREAKING CHANGE:` footer | Major bump per package |
| Internal deps only | `chore(deps): ...` | Hidden from user-facing changelog |

CalVer scheme: `YYYY.WW.PATCH` — see `docs/contributing/release-process.md`.

## When the user asks to "bump version" or "update changelog"

**Do not** edit `CHANGELOG.md` or `pyproject.toml` `version`. Instead:

1. Explain that release-please handles it on the standing Release PR.
2. Ensure their work is committed with the right conventional commit type/scope.
3. Point them to merge the Release PR or read `docs/contributing/release-process.md` for hotfixes/RC/dev cuts.

## Hotfixes on `release/*`

Backport fixes from `main` with **cherry-pick**, not direct edits on the release branch.

| Rule | Why |
|------|-----|
| Cherry-pick from `main` | CI checks patch equivalence (`git cherry` vs `main`), not identical SHAs |
| **Rebase and merge** only | Squash collapses N commits → 1; release-please loses per-commit changelog entries |
| Conventional commit subjects | release-please attributes each merged commit to changelog sections |
| Skip release-please bot PRs | `chore: hotfix release/...` PRs are automation — CI skips lineage for `release-please--*` branches |

Script: `.github/scripts/check-release-lineage.sh` (runs in CI for human PRs targeting `release/*`; patch-equivalence only, no commit-metadata allowlist).

## Monorepo consumers (different repo)

Bumping a **published** `unique_toolkit` / `unique_sdk` version inside the **monorepo** (e.g. `assistants-core` `pyproject.toml`) is a separate step after a stable AI release — not a manual ai-repo changelog edit. See `model-deployment` LESSONS-LEARNED for cherry-pick checklists.

## Related skills

- `hotfix-backport` — cherry-pick workflow and rebase-merge rules for `release/*`
- `git-conventional-commits` — commit/PR title format
- `security-maintenance` — same no-manual-release rules for CVE/CodeQL PRs
