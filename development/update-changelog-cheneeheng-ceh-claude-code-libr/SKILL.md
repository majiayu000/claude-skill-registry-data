---
name: update-changelog
description: >-
  Load this skill when updating CHANGELOG.md or writing release notes, as a versioned section or an
  Unreleased entry in Keep a Changelog format. Trigger on "update the changelog", "write release
  notes", "log this under unreleased", "what changed since the last release".
disable-model-invocation: false
user-invocable: true
allowed-tools: Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check-semver.py *)
compatibility: >-
  Requires the git CLI on PATH and a git working tree, to read history since the last tag. The
  validator step needs Python 3 (stdlib only); without it, the changelog is checked by hand.
license: Apache-2.0
---

# Update changelog

Inspect the project's git history, existing CHANGELOG.md, and codebase to produce or update a
well-structured changelog following **Semantic Versioning** and **Keep a Changelog** format.

## Procedure

### 1. Gather context

```bash
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null)   # current version (empty if none)
if [ -n "$LAST_TAG" ]; then
  git log "$LAST_TAG"..HEAD --oneline --no-merges        # changes since last release
else
  git log --oneline --no-merges                          # no tags yet: full history
fi
git tag --sort=-v:refname | head -20                     # version history
cat CHANGELOG.md 2>/dev/null || echo "No CHANGELOG.md found"
```

If no tag exists, read the version from whatever manifest the project uses (e.g. `package.json`,
`pyproject.toml`, `Cargo.toml`, `*.csproj`, `build.gradle`, `VERSION`).

### 2. Determine version and categorize

**Unreleased mode.** When the caller says the change is not being released — no version bump, no
tag — skip the version entirely: categorize as below, then add the bullets under the existing
`## [Unreleased]` heading (create it directly under the intro if missing) and stop after step 5. Do
not invent a version number, do not add a dated header, and do not touch the comparison links.
Everything else in this skill applies unchanged.

Apply semver rules and map to Keep a Changelog sections in one pass:

| Commit signal                                   | Bump  | Section           |
| ----------------------------------------------- | ----- | ----------------- |
| `BREAKING CHANGE:` footer or `feat!:` / `fix!:` | MAJOR | Removed / Changed |
| `feat:`                                         | MINOR | Added             |
| `fix:`                                          | PATCH | Fixed             |
| `perf:`                                         | PATCH | Changed           |
| `chore:`, `docs:`, `refactor:`, `test:`         | PATCH | (use judgment)    |
| Security patches                                | PATCH | Security          |

Skip: merge commits, version bumps, CI config, trivial formatting.

If the user specifies the version explicitly, use it. If uncertain about the bump level, explain
reasoning and ask before writing.

### 3. Write the entry

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added

- Imperative description (#PR or commit ref)

### Changed / Fixed / Removed / Security

- ...
```

- Imperative mood: "Add support for X" not "Added"
- One line per change; group related items
- Link PRs/issues with `[#123](url)`
- Omit empty sections

### 4. Update CHANGELOG.md

**Existing file:** Prepend new entry after `[Unreleased]` (create the section if missing). Update
comparison links at bottom.

**No file:** Create from scratch:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [X.Y.Z] - YYYY-MM-DD

...
```

Add comparison links at the bottom (infer repo URL from `git remote get-url origin`):

```markdown
[Unreleased]: https://github.com/owner/repo/compare/vX.Y.Z...HEAD
[X.Y.Z]: https://github.com/owner/repo/compare/vX.Y.Z-1...vX.Y.Z
```

### 5. Validate

Run the bundled validator. `${CLAUDE_PLUGIN_ROOT}` is substituted with the plugin's directory, so
the path resolves wherever the plugin is installed:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/check-semver.py" CHANGELOG.md
```

If the script cannot be located, scan `CHANGELOG.md` manually: verify all version headers match
`MAJOR.MINOR.PATCH` (with optional `-prerelease` or `+build`), dates are `YYYY-MM-DD`, versions are
newest-first, no duplicates.

## Rules

- Never invent changes — only document what git log and diffs evidence.
- Never include secrets, credentials, or internal infra details.
- Only modify `CHANGELOG.md`.
- Versions must always increase.
