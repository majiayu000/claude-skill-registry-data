---
name: release-changelog
description: Standardized release workflow — version bump, Keep a Changelog formatting, and CI/CD pipeline integration with auto-tagging and release automation. Works for any language (Python, Rust, Node, Go, etc.). Use when the user asks to cut a release, bump version, update changelog, or prepare release notes.
---

# Release & Changelog Skill

## Pattern

A release workflow where:
1. **Version is single-sourced** in the project's canonical config file (e.g. `Cargo.toml`, `package.json`, `pyproject.toml`, `version` file)
2. **Changelog follows Keep a Changelog** + SemVer format
3. **CI/CD auto-creates tags and releases** on push to main/default branch

## Detection triggers

Activate when the user says:
- "cut a release"
- "bump the version"
- "update the changelog"
- "create release notes"
- "prepare a release"
- "release version X.Y.Z"

## Protocol

### Step 1: Find the version source

Identify where the canonical version lives. Common locations by language:

| Language | File | Field |
|---|---|---|
| Rust | `Cargo.toml` | `version = "X.Y.Z"` |
| JavaScript/Node | `package.json` | `"version": "X.Y.Z"` |
| Python | `pyproject.toml` | `version = "X.Y.Z"` |
| Go | `version.go` or `internal/version/version.go` | Varies |
| Generic | `VERSION` file, `gradle.properties`, `pom.xml` | Varies |

Bump the version to the target.

### Step 2: Write the changelog entry

Add a section at the top of `CHANGELOG.md`:

```
## [X.Y.Z] - YYYY-MM-DD
```

Use these categories as needed:
- `### Added` — new features
- `### Changed` — changes in existing functionality
- `### Removed` — removed features
- `### Fixed` — bug fixes
- `### Security` — security fixes
- `### Performance Improvements` — perf changes

Each bullet uses present tense, imperative mood. If a commit trace tool exists, include:

```
### Commit Trace
- Since `prev_version`: `sha1`, `sha2`, ...
```

### Step 3: Verify pre-release gates

Run the project's own quality checks — do not assume specific tools:
- **Lint**: run project's linter (ruff, clippy, eslint, golangci-lint, etc.)
- **Format**: run project's formatter check (black, rustfmt, prettier, gofmt, etc.)
- **Type check**: if applicable (mypy, tsc, etc.)
- **Tests**: run project's test suite (pytest, cargo test, npm test, go test, etc.)
- **Build**: ensure the project builds/compiles cleanly
- **Security**: if applicable, run project's security scanner

Check what commands the project uses (look at `scripts/`, `Makefile`, `package.json` scripts, `Justfile`, `Taskfile.yml`, or CI workflow files).

### Step 4: Commit and push

Commit the version bump and changelog changes. Push to the default branch.

### Step 5: Verify pipeline automation

After push, confirm these automated workflows fire:
- **Auto-tag** workflow creates `vX.Y.Z` tag from the version file change
- **Release** workflow creates a GitHub/GitLab Release, runs tests, builds artifacts
- **Versioned-doc sync** workflow updates version references across files

If any workflow fails, fix and re-push.

## When NOT to use

- The project doesn't use SemVer or Keep a Changelog
- The project has its own established release process (always defer to existing patterns)
- The user explicitly asks not to touch versioning or changelog
- You're just fixing a typo in the changelog — use direct edit, not the full protocol

## Cross-references

- **follow-existing-patterns** — Always defer to the project's existing release conventions before applying this skill. Read 2-3 prior changelog entries and the version file first to match style.
- **self-validate** — Run validation after the release batch (version bump + changelog + push) to confirm everything took effect.
- **verify-and-cite** — Verify version numbers match between the version file, changelog, and CI configs before declaring done.
- **universal-format-lint** — Format the changelog after writing to match project's Markdown conventions.
- **project-backup-status** — Backup before starting the release process to guard against destructive mistakes.
- **anti-premature-termination** — Do not declare "release complete" until tags, CI, and docs sync have all been verified.
- **todo-bootstrap** — If the release involves many steps (multi-repo, multiple changelogs, coordinated tags), use a checklist.
- **project-scripts** — Discover build, test, and deploy scripts before cutting a release to ensure all release automation steps are accounted for.
- **audit-project** — Verify dependency health and build integrity before cutting a release.
- **skill-loader** — Apply the expanded release-task cap when deciding which release and validation skills should also be active.
- **security-best-practices** — Check for security advisories before releasing if the project has security-sensitive changes.
- **git-workflow-conventional-commits** — Conventional commit types determine changelog sections (feat→Added, fix→Fixed, etc.). Ensure commits follow conventions for automatic changelog generation.
- **ci-cd-automation** — CI/CD pipelines should trigger release workflows. release-changelog defines the release process; CI/CD automates it.
- **shipping-and-launch** — Run release-changelog first (version bump, changelog, tag), then shipping-and-launch (deploy, rollout, monitor).

## CI/CD Workflow Reference (typical)

| Workflow | Trigger | Action |
|---|---|---|
| auto-tag | push to default branch changing version file | Creates git tag `vX.Y.Z` |
| release | tag push `v*.*.*` | Release, tests, build artifacts |
| versioned-doc sync | tag push or version file change | Syncs version badges/docs |
