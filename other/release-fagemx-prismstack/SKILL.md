---
name: release
description: |
  Release a new Prismstack version. Runs tests, updates changelog, bumps version, tags, reinstalls globally.
  Trigger: "release", "ship", "bump version", "new version"
  Do NOT use when: still making changes (finish first, then release)
user_invocable: true
---
<!-- Internal maintenance skill — edit this file directly -->

# /release: Ship a New Prismstack Version

You are the release manager. You ensure every release is tested, documented, tagged, and installed.

## Phase 1: Pre-Flight Checks

### Run tests

```bash
bash test/install-test.sh
```

All tests must pass (expect 67/67). If any fail, stop and report: "Cannot release — N test failures. Fix first."

### Check working tree

```bash
git status --short
```

Must be clean (no uncommitted changes). If dirty, stop and report: "Cannot release — uncommitted changes found. Commit or stash first."

### Review changes since last release

```bash
git describe --tags --abbrev=0 2>/dev/null || echo "no-tags"
```

Then show commits since that tag:

```bash
git log --oneline $(git describe --tags --abbrev=0 2>/dev/null || echo "HEAD~20")..HEAD
```

Summarize the changes by category: features, fixes, docs, refactors.

## Phase 2: Determine Version Bump

Read the current version:

```bash
cat VERSION
```

Read `CHANGELOG.md` for any unreleased section.

Apply semantic versioning:
- **breaking:** changes → major bump (0.5.0 → 1.0.0)
- **feat:** changes → minor bump (0.5.0 → 0.6.0)
- **fix:** only → patch bump (0.5.0 → 0.5.1)

Present the proposed version and changelog to the user. Ask for confirmation before proceeding:

"Proposed release: vX.Y.Z with these changes: [summary]. Proceed?"

Do NOT continue without user confirmation.

## Phase 3: Update Files

### VERSION file

Write the new version string (just the number, no `v` prefix).

### CHANGELOG.md

Add a new version header at the top of the changelog (below any title):

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- feat: description (from commit messages)

### Fixed
- fix: description

### Changed
- refactor: description
```

Organize commits under the appropriate heading. Drop trivial commits (typo fixes, etc.) unless they are the only changes.

## Phase 4: Commit and Tag

```bash
git add VERSION CHANGELOG.md
git commit -m "chore: release vX.Y.Z"
git tag vX.Y.Z
```

Verify the tag:

```bash
git tag --list | tail -5
```

## Phase 5: Reinstall Globally

```bash
bash bin/install.sh --global
```

Verify installation:

```bash
ls ~/.claude/skills/prismstack/
```

Confirm the installed skills match the released version.

## Output

Report:
1. **Version**: vX.Y.Z
2. **Changes**: summary of what shipped
3. **Tests**: 67/67 passed
4. **Tag**: created
5. **Install**: confirmed at `~/.claude/skills/prismstack/`

If anything failed, report exactly what and at which phase.
