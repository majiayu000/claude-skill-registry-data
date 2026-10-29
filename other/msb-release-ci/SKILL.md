---
name: msb-release-ci
description: "Changelog discipline, CI and releases: the one-line CHANGELOG.md entry every behaviour change needs and which group it goes in, scripts/check.sh as exactly what CI runs (syntax, shellcheck, ruff, the unit tests, TOML, PAYLOAD in step, tracked modes, gitleaks), the tracked-mode rule and the sed -i trap, and the tag-driven release with actions pinned by hash and read-only permissions. Use when making any user-visible change, cutting a release, or when CI, a mode or a payload check complains."
---

# Release Ci

Detail carved out of `AGENTS.md`, which keeps only what has to hold in
every session. Repo-specific throughout; the facts here are verified against
msb 0.7.6 and re-checked on 0.7.7.

- **Every behaviour change gets a ONE-LINE entry in `CHANGELOG.md`**, under `## [Unreleased]` in the matching `### Added` / `### Changed` / `### Fixed` / `### Removed` group. One line, user-facing, what changed and what a user must do about it (e.g. "needs a rebuild"). No file lists, no rationale, no commit hashes; the commit message and code comments carry those. Refactors, test-only and CI-only changes with no user-visible effect need no entry.
- `scripts/check.sh` is the static check suite and is exactly what CI runs (syntax, shellcheck, ruff with the rules in `ruff.toml`, the unit tests, TOML, `PAYLOAD` in step between `install.sh` and `package.sh`, tracked modes, gitleaks). Run it before committing. `scripts/smoke-install.sh` packages and installs into a throwaway HOME.
- Tracked modes: a file with a shebang is 755, everything else 644, except `bootstrap.sh` (piped into the guest, never executed from disk, so 644). `sed -i` and some editors recreate a file without its executable bit; `check.sh` reads the git index, so `git add` after any `chmod`.
- Releases are tag-driven (`.github/workflows/release.yml`): move the Unreleased entries under `## [X.Y.Z] - YYYY-MM-DD`, set `VERSION`, merge, then `git tag vX.Y.Z && git push origin vX.Y.Z`. The workflow refuses if the tag, `VERSION` and a non-empty changelog section disagree. Never publish by hand with `gh release create` unless the workflow is broken.
- Workflows use `pull_request`, never `pull_request_target`, with read-only default permissions; actions are pinned by commit hash with the version in a comment (Dependabot keeps them current).
