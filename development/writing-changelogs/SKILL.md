---
name: writing-changelogs
description: Use when releasing a new version, updating CHANGELOG.md, or user asks to document changes - enforces Keep a Changelog format with proper categorization derived from conventional commits
---

# Writing Changelogs

## Overview

Changelogs follow the **Keep a Changelog** specification (v1.1.0) for human-readable release documentation.

**Core principle:** Changelogs are for humans, not machines. Curate meaningful changes—don't dump git logs.

## When to Use

- Creating initial CHANGELOG.md
- Releasing a new version (moving Unreleased to versioned section)
- Adding entries to Unreleased section after completing work
- User says "update changelog", "document changes", "prepare release"

**NOT for:** Commit messages (use making-git-commits skill)

## Changelog Format

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 2025-12-26

### Added
- User authentication with OAuth 2.0 support

### Changed
- Improve error messages for validation failures

### Fixed
- Handle null responses in API client gracefully

[Unreleased]: https://github.com/owner/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/owner/repo/compare/v1.1.0...v1.2.0
```

## Change Categories

| Category | Description | Commit Types |
|----------|-------------|--------------|
| `Added` | New features | `feat` |
| `Changed` | Changes to existing functionality | `refactor`, `perf`, `style` |
| `Deprecated` | Soon-to-be removed features | — |
| `Removed` | Now removed features | — |
| `Fixed` | Bug fixes | `fix` |
| `Security` | Vulnerability fixes | `fix` (security-related) |

**Note:** `docs`, `test`, `build`, `ci`, `chore` commits typically don't appear in changelogs unless user-facing.

## Mapping Commits to Changelog

```
Conventional Commit → Changelog Entry

feat(auth): add OAuth 2.0 support
→ ### Added
  - OAuth 2.0 authentication support

fix(api): handle null response gracefully
→ ### Fixed
  - Handle null responses in API client gracefully

feat(config)!: require explicit environment variable
→ ### Changed
  - **BREAKING:** CONFIG_PATH environment variable now required
```

## Writing Good Entries

**Do:**
- Write for end users, not developers
- Start with verb: "Add", "Fix", "Remove", "Change"
- Explain impact, not implementation
- Group related changes in single entry
- Link to issues/PRs when helpful: `([#42](link))`

**Don't:**
- Copy commit messages verbatim
- Include internal refactoring details
- Use technical jargon unnecessarily
- List every commit

```markdown
# ❌ Bad: Technical, commit-style
- refactor(utils): consolidate date formatting functions
- fix(parser): handle edge case in tokenizer line 847

# ✅ Good: User-focused
- Improve date formatting consistency across the application
- Fix parsing errors when input contains special characters
```

## Release Workflow

```
1. REVIEW: Check commits since last release
2. CATEGORIZE: Group by Added/Changed/Deprecated/Removed/Fixed/Security
3. CURATE: Write human-readable entries (not commit dumps)
4. VERSION: Move Unreleased to new version section with date
5. LINKS: Update comparison links at bottom
6. VERIFY: Ensure date is ISO 8601 (YYYY-MM-DD)
```

## Quick Reference

| Element | Format |
|---------|--------|
| Version header | `## [X.Y.Z] - YYYY-MM-DD` |
| Unreleased | `## [Unreleased]` |
| Category | `### Added` (capitalize) |
| Entry | `- Description starting with verb` |
| Date | ISO 8601: `2025-12-26` |
| Yanked | `## [X.Y.Z] - YYYY-MM-DD [YANKED]` |
| Breaking change | `- **BREAKING:** description` |
| Link reference | `[X.Y.Z]: https://github.com/owner/repo/compare/vA.B.C...vX.Y.Z` |

## Guiding Principles

1. **Changelogs are for humans** — Write prose, not code
2. **Entry for every version** — No gaps in history
3. **Group same types** — All Added together, all Fixed together
4. **Versions are linkable** — Use reference-style links
5. **Latest first** — Reverse chronological order
6. **Show release dates** — ISO 8601 format always
7. **Follow SemVer** — State this in header

## Common Mistakes

| Mistake | Correct |
|---------|---------|
| Dumping git log | Curate meaningful changes |
| `2025/12/26` or `26-12-2025` | `2025-12-26` (ISO 8601) |
| Lowercase category | `### Added` not `### added` |
| Missing Unreleased section | Always keep `## [Unreleased]` at top |
| No comparison links | Add links at bottom of file |
| Past tense entries | "Add feature" not "Added feature" |
| Breaking change buried | Mark clearly with **BREAKING:** |

## Red Flags - STOP

- About to paste raw git log into changelog
- Including `chore:`, `ci:`, `test:` commits directly
- Writing for developers instead of users
- Forgetting to update comparison links
- Using non-ISO date format
- Missing categories for different change types
- No Unreleased section for ongoing work

## Creating Initial CHANGELOG.md

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - YYYY-MM-DD

### Added
- Initial release with core functionality

[Unreleased]: https://github.com/owner/repo/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/owner/repo/releases/tag/v0.1.0
```

## The Bottom Line

**Changelogs tell the story of your project for humans.**

A good changelog answers: "What changed and why should I care?"

Don't let your friends dump git logs into changelogs.
