---
name: release-manager
description: Manage the release process for LibrAgent. Use this skill to analyze changes, update the changelog intelligently, synchronize user documentation (docs/ & website/), refresh in-app feature tips (spotlight) for layman-facing changes, and publish new versions.
---

# Release Manager Skill

This skill defines the standard procedure for releasing a new version of LibrAgent. You (the Agent) act as the Release Manager, responsible for understanding the changes, updating both `CHANGELOG.md` and user documentation (`docs/` & `website/`), refreshing **in-app feature tips** when layman-facing capabilities ship, and communicating them clearly to users on the project site.

## Workflow Overview

1. **Analyze**: Read git history and diffs to understand what changed.
2. **Document, Tips & Sync Docs**:
   - Intelligently update `CHANGELOG.md` with a user-facing summary.
   - **Feature tips**: If this version has layman-discoverable capabilities, update the spotlight tip registry + i18n (see [references/feature-tips.md](references/feature-tips.md)). If none qualify, explicitly note “No tip updates”.
   - Update user documentation (`docs/user/`) and project site pages (`website/`) so new features, UI changes, and guides stay up-to-date.
   - Run `pnpm docs:build` to verify VitePress documentation site builds cleanly.
3. **Commit Docs, Tips & Changelog**: Commit changelog, tip/i18n updates, and doc updates so release scripts run on a clean git state.
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
- **Layman discovery candidates**: Changes a non-developer should notice in-app (feeds tip updates).
- **Internal / Refactoring**: Code cleanup, dev scripts, testing.

### 2. Update Changelog, Feature Tips & User Documentation

Decide the planned **NEW_VERSION** (patch/minor/major) before writing tip `sinceVersion` fields.

#### A. Update `CHANGELOG.md`

- **Format**: Follow existing style (`## [Version] - YYYY-MM-DD`).
- **Content**: Summarize changes concisely with emojis (🚀, 🐛, 🔧).
- **Versioning Rule**: Prepare patch/minor/major bump section (e.g. `## [0.9.22] - YYYY-MM-DD`).

#### B. Update in-app Feature Tips (Spotlight)

**Read and follow** [references/feature-tips.md](references/feature-tips.md).

From the CHANGELOG draft, extract layman-facing bullets and for each:

1. **Skip** if internal / developer-only / invisible restore.
2. **Add or refresh** a tip when users should discover the capability without reading the changelog.
3. Set `sinceVersion` to **NEW_VERSION** so Release Spotlight shows it after upgrade.
4. Update **all 8** locale files under `src/locales/*/common.json` (`spotlight.items.*`).
5. Cap at **1–3** tip adds/refreshes per release.

Primary code file: `src/features/spotlight/feature-spotlights.ts`.

If nothing qualifies: do not invent filler; record “No tip updates this release” in the commit message body.

#### C. Synchronize User Documentation (`docs/` & `website/`)

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

### 3. Commit Documentation, Tips & Changelog

Commit documentation, changelog, and tip/i18n updates so the release script runs on a clean working tree:

```bash
git add CHANGELOG.md docs/ website/ src/features/spotlight/ src/locales/
git commit -m "$(cat <<'EOF'
docs: update changelog, tips, and user documentation for v<NEW_VERSION>

EOF
)"
```

Omit tip paths from `git add` when there were no tip updates.

**Critical**: Release scripts require a clean working tree before execution.
Make sure changelog, tip, and doc edits are committed first.

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

After bump, confirm tip `sinceVersion` values still match the tagged version if tips were added in Step 2 (they should already equal NEW_VERSION).

## Quick Release Checklist

1. Confirm baseline tag and diff scope.
2. Draft user-facing `CHANGELOG.md` section; pick NEW_VERSION.
3. **Tips**: Apply layman tip add/refresh via [references/feature-tips.md](references/feature-tips.md), or mark “No tip updates”.
4. Synchronize user docs under `docs/user/` & project site (`website/`).
5. Run `pnpm docs:build` to verify VitePress site build.
6. Commit changelog, tip/i18n (if any), and documentation updates.
7. Run release script with `patch`/`minor`/`major` or explicit `x.y.z`.
8. Verify branch push + tag push completed successfully.
9. Confirm GitHub Actions release workflow started.

## Merge Policy (Required)

When merging a release PR (`dev/0.9.x` → `main`):

- **Always** use **Create a merge commit**.
- **Never** use squash merge — it breaks history alignment with the long-lived dev branch.
- **After merge**, sync `main` back into `dev/0.9.x` (`git merge origin/main` + push).
