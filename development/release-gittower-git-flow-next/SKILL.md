---
name: release
description: Update changelog and version based on git history using semantic versioning and conventional commits
allowed-tools: Bash, Read, Edit, Grep, Glob
---

# Prepare Release

Automatically update CHANGELOG.md and version files based on git history, semantic versioning, and conventional commits.

## Instructions

### 1. Read Release Guidelines

Read `RELEASING.md` for the full release process and conventions.

### 2. Determine Last Release

```bash
# Get the latest version tag
git describe --tags --abbrev=0
```

### 3. Collect Commits Since Last Release

```bash
# List all commits since last tag, excluding previous version bump commits
git log $(git describe --tags --abbrev=0)..HEAD --oneline --no-merges --grep="^chore: Bump version" --invert-grep
```

Ignore any `chore: Bump version to X.Y.Z` commits — these are artifacts of previous `/release` runs that haven't been tagged yet.

### 4. Determine Version Bump

Analyze commit types (excluding version bump commits) to determine the correct version bump:

- Any `BREAKING CHANGE` in footer or `!` after type → **major** bump
- Any `feat:` commits → **minor** bump
- Only `fix:`, `perf:`, or other patch-level commits → **patch** bump

If there are no user-facing changes (only `docs:`, `refactor:`, `test:`, `chore:`, `ci:`, `style:`), inform the user that there are no releasable changes and ask whether to proceed.

### 5. Categorize Changes for Changelog

Map commits to changelog sections per RELEASING.md:

| Commit Type | Changelog Section | Include? |
|-------------|-------------------|----------|
| `feat:` | Added | Yes |
| `fix:` | Fixed | Yes |
| `BREAKING CHANGE` | Changed | Yes |
| `perf:` | Changed | Yes |
| `build:` | Changed | Only if user-facing |
| `docs:` | — | No |
| `refactor:` | — | No |
| `test:` | — | No |
| `chore:` | — | No |
| `ci:` | — | No |
| `style:` | — | No |

Write human-readable changelog entries:
- Use the commit subject but rewrite if needed for clarity
- Remove commit type prefixes and scopes
- Start each entry with a dash and describe the user-facing change
- Group related commits into a single entry when appropriate

### 6. Update CHANGELOG.md

1. Read current `CHANGELOG.md`
2. Check if there is already an **untagged** version section (a version entry above `[Unreleased]` that has no corresponding git tag). This happens when `/release` was run before but no tag was created yet.
   - **If an untagged version section exists**: Replace that entire section (heading, date, and all entries) with the newly determined version and entries. Do NOT create a duplicate section.
   - **If no untagged version section exists**: Add a new version section under `[Unreleased]` with today's date.
3. Populate with categorized changes (Added, Changed, Fixed, Removed, Security — only include sections that have entries)
4. Update the comparison links at the bottom of the file:
   - Update `[Unreleased]` link to compare new version to HEAD
   - Add/update the version comparison link

### 7. Update Version Files

Update the version string in **both** files (they must match):

- `version/version.go` — the `Version` constant
- `cmd/version.go` — the `Version` variable

### 8. Verify Build

```bash
go build -o /tmp/git-flow main.go && /tmp/git-flow version
```

### 9. Commit

Stage and commit all changes:

```bash
git add CHANGELOG.md version/version.go cmd/version.go
```

Check if the previous commit is already a `chore: Bump version to ...` commit (from a prior `/release` run). If so, **amend** that commit instead of creating a new one:

```bash
# If previous commit is a version bump:
git commit --amend -m "chore: Bump version to X.Y.Z"

# Otherwise create a new commit:
git commit -m "chore: Bump version to X.Y.Z"
```

### 10. Report

Show the user:
- Previous version → new version
- Summary of changelog entries
- Remind them to push and tag when ready:
  ```
  git push origin main
  git tag vX.Y.Z
  git push origin vX.Y.Z
  ```
