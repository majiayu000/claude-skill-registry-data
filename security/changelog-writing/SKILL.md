---
name: changelog-writing
description: >
  Write and maintain clean, human-readable CHANGELOG.md files adhering to the
  Keep a Changelog convention. Use when documenting releases, updating the
  Unreleased section from commit logs or PRs, preparing release notes, or
  writing migration guides for breaking changes.
compatibility: >
  Agent Skills-compatible coding agents editing Markdown changelogs or
  generating release notes.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "changelog, release-notes, documentation, keep-a-changelog, releases"
  topics: "documentation, devtools, version-control"
---

# Changelog Writing

A changelog is a curated, chronologically ordered file that documents notable changes for each version of a project. Unlike a raw git commit log, a changelog is written for **human consumers** to quickly understand what has changed, why it matters, and how to upgrade.

Follow the [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) standard and align with [Semantic Versioning](https://semver.org/).

## Core Principles

1. **Write for users, not git**: Describe observable effects and user benefits, not internal refactoring minutiae.
2. **Curate and group**: Never dump git commit logs verbatim. Group related changes under standard categories.
3. **Always keep an `[Unreleased]` section**: Track ongoing changes at the top of the changelog before a version is tagged.
4. **Dates follow ISO 8601**: Write dates as `YYYY-MM-DD` (e.g., `2026-10-15`).
5. **Highlight breaking changes**: Document breaking changes prominently with migration guidance.
6. **Link versions and PRs**: Include comparative diff links at the bottom of the changelog.

---

## 1. Standard Section Types

Group changes under these standard subheadings (in order):

- `### Added` — New features and capabilities.
- `### Changed` — Changes in existing functionality.
- `### Deprecated` — Features that will be removed in upcoming releases.
- `### Removed` — Features that have now been removed.
- `### Fixed` — Bug fixes.
- `### Security` — Vulnerability fixes and security enhancements (include CVE IDs when available).

Omit subheadings that have no entries in that release.

---

## 2. Canonical Changelog Format

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Interactive search filters for skill tags (#142).

### Fixed
- Prevent crash when parsing empty YAML frontmatter (#145).

## [1.2.0] - 2026-10-10

### Added
- Multi-threading support for batch file validation (#120).
- Support for custom configuration via `~/.config/app/config.toml` (#124).

### Changed
- Standardized error codes returned by the CLI exit handler (#128).

### Deprecated
- The `--legacy-mode` flag is deprecated and will be removed in v2.0.0. Use `--compat=v1` instead (#130).

### Fixed
- Memory leak in background worker during long-running socket connections (#133).

### Security
- Upgraded `urllib3` to address CVE-2026-XXXXX (#135).

[Unreleased]: https://github.com/org/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/org/repo/compare/v1.1.0...v1.2.0
```

---

## 3. Workflow: Updating the Changelog

### Step 1: Gather Recent Changes
Inspect git log since the last release tag:

```bash
# Find latest release tag
git describe --tags --abbrev=0

# List commits since the tag
git log v1.2.0..HEAD --oneline --no-merges
```

### Step 2: Categorize and Rephrase
Translate internal commits into consumer-oriented entries:

| Raw Commit | Categorized & Rephrased Entry |
| :--- | :--- |
| `feat(auth): add pkce to oauth flow` | `### Added`<br>- PKCE support for OAuth authentication flows to enhance mobile security (#102). |
| `fix: handle None in user profile avatar url` | `### Fixed`<br>- Avoid `AttributeError` when loading user profiles with no avatar set (#108). |
| `refactor: optimize db query in get_stats` | Omit if purely internal with no measurable user effect, or note in `### Changed` if performance is noticeably improved. |

### Step 3: Preparing a Release
When cutting version `1.3.0`:
1. Rename `## [Unreleased]` to `## [1.3.0] - YYYY-MM-DD`.
2. Add a fresh, empty `## [Unreleased]` section above it.
3. Update the compare links at the bottom of the file.

---

## 4. Common Mistakes and Anti-Patterns

| Anti-Pattern | Why It Fails | Correction |
| :--- | :--- | :--- |
| Direct commit log dumps (`fix typo in docs`, `wip`, `update deps`) | Noise that hides meaningful changes from users | Synthesize multiple commits into one clear entry |
| Missing dates or regional date formats (`10/12/26`) | Ambiguous (Oct 12 vs Dec 10) | Always use ISO format: `YYYY-MM-DD` |
| Omitting migration notes on breaking changes | Users upgrade and their software fails with no guidance | Include a `Migration Guide` paragraph or explicit before/after snippet |
| Modifying released version history retroactively | Violates historical record | Only update `[Unreleased]` for ongoing development |

---

## 5. Verification Checklist

- [ ] Every entry is assigned to one of the 6 standard categories (`Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`).
- [ ] Version headings follow `## [X.Y.Z] - YYYY-MM-DD`.
- [ ] An `## [Unreleased]` section exists at the top.
- [ ] All PR / Issue links and markdown reference links at the bottom are valid.
- [ ] Breaking changes and deprecation warnings are clearly stated with migration guidance.
