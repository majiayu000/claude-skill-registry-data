---
name: simple-release
description: Cut a release with a semantic version bump, a changelog from commit history, and a git tag. Use only when the user asks to release, bump the version, or write a changelog.
disable-model-invocation: true
metadata:
  author: denniemok
  version: "1.0.0"
license: MIT
---

# Simple Release

Prepare a release from the commit history. Propose first, then apply only after the user confirms the version.

## Workflow

1. Check state: clean working tree, on the release branch, up to date. Stop and say so if not.
2. Find the last tag (`git describe --tags --abbrev=0`) and read the commits since it (`git log <tag>..HEAD --oneline`). With no tag, use the full history.
3. Pick the bump from the commits:
   - Breaking change (`!` after the prefix, or `BREAKING CHANGE`): major
   - Any `feat`: minor
   - Only `fix`, `perf`, and others: patch
   - Before 1.0.0, breaking changes bump minor
4. Show the proposed version and changelog entry, and wait for confirmation.
5. Apply: update the version file (`package.json`, `pyproject.toml`, or the one the project uses), add the entry to `CHANGELOG.md`, and commit as `chore(release): vX.Y.Z`.
6. Tag the commit `vX.Y.Z`.
7. Report the version, the tag, and the next command to push. Push only when the user asks.

## Changelog entry

Newest first, one section per version, grouped by type. Write for users, not for the commit author.

```text
## [1.4.0] - 2026-09-30

### Added
- Avatar upload on the profile page

### Fixed
- Login redirect loop on expired sessions

### Changed
- Faster chapter loading
```

| Commit prefix | Section |
|---------------|---------|
| feat | Added |
| fix | Fixed |
| perf, refactor | Changed |
| revert | Removed or Reverted |
| docs, style, test, build, ci, chore | Leave out, unless users would care |

- Rewrite commit subjects into plain sentences, and merge duplicates.
- Flag breaking changes at the top of the entry with what to do about them.
- Link the compare URL at the bottom if the repo has a remote.

## Rules

- Never push commits or tags unless asked.
- Never move or delete an existing tag.
- Do not add `Co-Authored-By` or any AI attribution to the release commit.
- If the commits do not follow a convention, read the diffs and group the changes yourself, and say that you did.
- Create a GitHub release with `gh release create` only when asked.
