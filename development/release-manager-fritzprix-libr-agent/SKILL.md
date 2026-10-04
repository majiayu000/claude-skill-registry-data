---
name: release-manager
description: Manage the release process for LibrAgent. Use this skill to analyze changes, update the changelog intelligently, synchronize user documentation (docs/ & website/), and publish new versions.
---

# Release Manager Skill

This skill defines the standard procedure for releasing a new version of LibrAgent. You (the Agent) act as the Release Manager, responsible for understanding the changes, updating both `CHANGELOG.md` and user documentation (`docs/` & `website/`), and communicating them clearly to users on the project site.

## Workflow Overview

1. **Analyze**: Read git history and diffs to understand what changed.
2. **Document & Sync Docs**:
   - Intelligently update `CHANGELOG.md` with a user-facing summary.
   - Update user documentation (`docs/user/`) and project site pages (`website/`) so new features, UI changes, and guides stay up-to-date.
   - Run `pnpm docs:build` to verify VitePress documentation site builds cleanly.
3. **Commit Docs & Changelog**: Commit changelog and doc updates so release scripts run on a clean git state.
4. **Verify & Publish**: Use release scripts to run checks, bump versions, tag, and push.

## Step-by-Step Instructions

### 1. Analysis (The "Brain" Work)

First, determine what has changed since the last release.

```bash
# Find the last tag
git describe --tags --abbrev=0

# Define baseline tag
LAST_TAG=$(git describe --tags --abbrev=0)

# List commits since that tag (exclude merge noise)
git log ${LAST_TAG}..HEAD --no-merges --pretty=format:"%h %s"

# Inspect impact scope and file diffs
git diff --name-only ${LAST_TAG}..HEAD
git diff --shortstat ${LAST_TAG}..HEAD
```

**Task**: Read the commit messages and diffs. Group them into:
- **New Features & Capabilities**: New tools, assistants, UI features, slash commands.
- **User-facing Fixes**: Bug fixes, reliability improvements.
- **Internal / Refactoring**: Code cleanup, dev scripts, testing.

### 2. Update Changelog & User Documentation

#### A. Update `CHANGELOG.md`

- **Format**: Follow existing style (`## [Version] - YYYY-MM-DD`).
- **Content**: Summarize changes concisely with emojis (🚀, 🐛, 🔧).
- **Versioning Rule**: Prepare patch/minor/major bump section (e.g. `## [0.8.40] - YYYY-MM-DD`).

#### B. Synchronize User Documentation (`docs/` & `website/`)

**Critical**: Do not let project documentation become outdated during releases!

1. **Identify Affected User Guides**:
   - Check if new features require updates to existing guides under `docs/user/guides/` (e.g. `assistants.md`, `skills.md`, `custom-mcp.md`, `sessions.md`, `automation.md`).
   - Check if getting-started pages (`docs/user/getting-started/`) or FAQ (`docs/user/faq/`) need new entries.
2. **Update Multilingual Docs (if applicable)**:
   - Synchronize both Korean (`docs/user/`) and English (`docs/user/en/`) documentation when features change.
3. **Verify VitePress Site Build**:
   ```bash
   pnpm docs:build
   ```
   Ensure VitePress renders pages cleanly without broken links or missing assets.

### 3. Commit Documentation & Changelog

Commit all documentation and changelog updates so the release script runs on a clean working tree:

```bash
git add CHANGELOG.md docs/ website/
git commit -m "docs: update changelog and user documentation for v<NEW_VERSION>"
```

**Critical**: Release scripts require a clean working tree before execution.
Make sure changelog and doc edits are committed first.

### 4. Verification & Publishing (The "Grunt" Work)

Finally, use the provided scripts to handle mechanical steps: tests, build checks, version bump, commit, tag, and push.

```bash
# Linux/macOS
./scripts/release.sh <patch|minor|major|x.y.z>

# Windows PowerShell
./scripts/release.ps1 <patch|minor|major|x.y.z>
```

- **Checks**: Scripts abort on failed checks (`pnpm test:run`, `pnpm rust:test`, `pnpm build`, `cargo check`).
- **Automation**: Scripts run `scripts/bump-version.cjs`, which automatically synchronizes direct download links inside root READMEs (`README.md`, `README.ko.md`, etc.), updates version manifests (`package.json`, `Cargo.toml`, `Cargo.lock`, `tauri.conf.json`), commits, tags (`v<NEW_VERSION>`), and pushes.

## Quick Release Checklist

1. Confirm baseline tag and diff scope.
2. Draft user-facing `CHANGELOG.md` section.
3. Synchronize user docs under `docs/user/` & project site (`website/`).
4. Run `pnpm docs:build` to verify VitePress site build.
5. Commit changelog and documentation updates (`git commit -m "docs: update changelog and user documentation for v<NEW_VERSION>"`).
6. Run release script with `patch`/`minor`/`major` or explicit `x.y.z`.
7. Verify branch push + tag push completed successfully.
8. Confirm GitHub Actions release workflow started.

## Merge Policy (Required)

When merging a release PR (`dev/0.8.x` → `main`):
- **Always** use **Create a merge commit**.
- **Never** use squash merge — it breaks history alignment with the long-lived dev branch.
- **After merge**, sync `main` back into `dev/0.8.x` (`git merge origin/main` + push).
