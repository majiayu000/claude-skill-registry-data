---
name: changelog
description: |
  Generates and maintains CHANGELOG.md files following Keep a Changelog conventions — from git history, commit messages, or a description of changes. Use when asked to write a changelog, update release notes, or document what changed in a version.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-changelog
    version: "1.0.0"
    created: 2026-04-08T00:00:00Z
    category: engineering
    layer: 3
    uses:
      - skill: release-semver
        purpose: Determine the correct version number for a release entry.
---

# Changelog

## Intro

Follow the [Keep a Changelog](https://keepachangelog.com) convention:
one `CHANGELOG.md` at the repo root, entries in reverse chronological
order (newest first), each release tagged with a semantic version and
date, changes grouped under seven standard categories. Write for
humans, not machines — the reader is a developer evaluating whether
to upgrade.

## Overview

### File structure

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] — 2026-04-08

### Added
- ...

### Changed
- ...

### Deprecated
- ...

### Removed
- ...

### Fixed
- ...

### Security
- ...

[Unreleased]: https://github.com/org/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/org/repo/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/org/repo/releases/tag/v1.1.0
```

The `[Unreleased]` section accumulates changes since the last
release. On release, it becomes the new version block.

### The seven change categories

Use exactly these headings — no others:

| Category | What goes here |
|---|---|
| **Added** | New features, new endpoints, new configuration options |
| **Changed** | Changes to existing behavior, updated defaults, refactors that change observable behavior |
| **Deprecated** | Features that will be removed in a future version |
| **Removed** | Features removed in this version |
| **Fixed** | Bug fixes |
| **Security** | Vulnerability fixes — always include CVE IDs where available |

Omit sections that have no entries for a release. Do not use custom
categories (e.g. "Performance", "Refactor") — map to the nearest
standard one.

### Extracting changes from git

Use the git log to find changes since the last release:

```bash
# Changes since the last tag
git log v1.1.0..HEAD --oneline

# Changes between two tags
git log v1.1.0..v1.2.0 --oneline

# With full messages for detail
git log v1.1.0..HEAD --format="%h %s%n%b" | head -100
```

Then group commits by type:
- `feat:` or `add` → **Added**
- `fix:` → **Fixed**
- `chore:`, `refactor:`, `perf:` → **Changed** (if user-visible)
- `BREAKING CHANGE:` → **Removed** or **Changed** (prominently)
- `security:` or CVE mentions → **Security**

Discard: merge commits, version bumps, CI config changes, typo
fixes in comments, and any change the end user will never notice.

### Writing good changelog entries

Each entry is a single sentence describing the user-visible change.
Format: verb phrase in past tense, describing the observable
behavior change, not the implementation detail.

**Good:**
- Added `--dry-run` flag to the `sync` command that previews changes without applying them
- Fixed a race condition in the connection pool that caused intermittent 500 errors under high load
- Removed support for Python 3.8, which reached end-of-life in October 2024

**Bad:**
- Refactored the database layer (not user-visible)
- Updated dependencies (too vague — say which and why if it matters)
- Fixed bug (say what bug, what symptom)

Link to the relevant issue or PR for every entry where one exists:
`Added dark mode support ([#142](https://github.com/org/repo/issues/142))`

### Releasing: promote [Unreleased] to a version

When releasing version `1.2.0`:

1. Replace `## [Unreleased]` with `## [1.2.0] — YYYY-MM-DD`
2. Add a new empty `## [Unreleased]` section at the top
3. Add the version link at the bottom:
   `[1.2.0]: https://github.com/org/repo/compare/v1.1.0...v1.2.0`
4. Update the `[Unreleased]` link:
   `[Unreleased]: https://github.com/org/repo/compare/v1.2.0...HEAD`

### Breaking changes

Breaking changes deserve special treatment:

1. Place them first in the **Changed** or **Removed** section
2. Add a `> **Breaking change:**` blockquote before the entry
3. Include migration steps or a link to the migration guide

```markdown
### Changed

> **Breaking change:** The `auth` configuration key has been renamed
> to `authentication`. Update your config files before upgrading.
> See the [migration guide](docs/migration/v2.md).

- Renamed `config.auth` to `config.authentication` for clarity
```

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Including implementation-only changes that users will never notice.** A changelog entry for "refactored the database connection pool to use a factory pattern" tells users nothing useful. Filter to changes with observable user-visible effects — if the user can't see it, benchmark it, or configure it, it doesn't belong in the changelog.
- **Writing entries that describe what changed in the code instead of what changed for the user.** "Updated the auth middleware to validate JWT expiry" is an implementation detail; "Fixed a bug where expired tokens were accepted without re-authentication" is the user-facing fact. Write from the user's perspective, not the developer's.
- **Using custom category names instead of the seven Keep a Changelog standard ones.** Adding "Performance", "Internal", or "Refactoring" sections breaks compatibility with tools that parse CHANGELOG.md (release generators, changelog aggregators) and confuses readers who expect the standard headings. Map every change to the nearest standard category.
- **Forgetting to update the comparison links at the bottom.** CHANGELOG.md links at the bottom reference Git tags. After every release, two links change: the `[Unreleased]` link and the new version link. Leaving them pointing to old tags makes the diff links wrong for everyone who clicks them.
- **Putting the [Unreleased] section below past releases instead of at the top.** The `[Unreleased]` section must always be the first entry, immediately after the file header. Entries below it are older releases in reverse chronological order. An [Unreleased] section buried below past versions is invisible to maintainers accumulating pre-release notes.
- **Including every commit message verbatim.** Raw commit messages ("wip", "fix test", "revert previous", "merge branch main") are noise in a changelog. Synthesize: group related commits into one user-visible entry, discard implementation churn, and rewrite technical commit shorthand into plain language.
- **Not marking breaking changes prominently.** A breaking change buried as the fifth bullet in "Changed" will be missed by users scanning the changelog before upgrading. Breaking changes must be clearly marked — use a blockquote, bold text, or a dedicated sub-heading — so they are impossible to miss.

## Full reference

### Conventional Commits mapping

If the project uses [Conventional Commits](https://conventionalcommits.org):

| Commit prefix | Changelog category |
|---|---|
| `feat:` | Added |
| `fix:` | Fixed |
| `perf:` | Changed |
| `refactor:` (visible) | Changed |
| `docs:` (user-facing) | Changed |
| `BREAKING CHANGE:` footer | Changed or Removed (prominent) |
| `security:` | Security |
| `chore:`, `test:`, `ci:` | Omit |
| `deprecate:` | Deprecated |

### Automating changelog generation

Tools that parse Conventional Commits and generate a draft changelog:
- `git-cliff` — highly configurable, supports custom templates
- `conventional-changelog-cli` — Node.js, many preset styles
- `release-please` (Google) — GitHub Actions workflow

These produce a draft; always human-review before publishing.
The agent's job when automation is available: **review and edit**
the generated draft, not generate from scratch.

### GitHub release notes vs. CHANGELOG.md

GitHub's "Generate release notes" button is not a substitute for
CHANGELOG.md:
- GitHub release notes are per-release and not accumulated
- They are structured around PR titles, not user-visible changes
- They are only accessible via GitHub, not in the repository

CHANGELOG.md is the authoritative, cumulative, human-readable record.
GitHub release notes can be generated from it, not the other way
around.

### Old changelog entries — when to leave them alone

Never rewrite or delete old changelog entries, even when they are
wrong about what a version contained. Old entries are part of the
project's permanent history. If a past entry was incorrect, add a
note in a later version's section that corrects the record.
