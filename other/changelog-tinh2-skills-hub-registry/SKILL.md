---
name: changelog
description: "Generate or update CHANGELOG.md from git history. Parses conventional commits, groups by version tags, categorizes into Added/Fixed/Changed/Breaking sections using keep-a-changelog format, and creates comparison links. Use when you need to create a changelog, update release notes, document version history, or prepare release documentation."
version: "2.0.0"
category: docs
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Parse the git history and
produce a well-structured CHANGELOG.md.

INPUT:
$ARGUMENTS

Accepted arguments:
- No arguments: generate full changelog from all git history.
- `since vX.Y.Z` or `since <tag>`: generate only entries since that tag/version.
- `unreleased`: generate only the Unreleased section since the last tag.
- `update`: read existing CHANGELOG.md, append only new entries since last documented version.

============================================================
PHASE 1: GIT HISTORY EXTRACTION
============================================================

Step 1.1 -- Identify Version Boundaries

Run:
- `git tag --sort=-version:refname` to list all tags (newest first)
- `git log --format="%H|%ai|%s|%b|%D" --reverse` to get all commits with refs

For each tag, record:
- Tag name (vX.Y.Z or X.Y.Z)
- Tagged commit hash
- Tag date

If no tags exist, group commits by time periods (monthly or weekly).

Step 1.2 -- Parse Commits

For each commit between version boundaries, parse the message:

| Prefix | Category |
|--------|----------|
| `feat:` `feat(scope):` | Features |
| `fix:` `fix(scope):` | Bug Fixes |
| `docs:` `docs(scope):` | Documentation |
| `refactor:` `refactor(scope):` | Refactoring |
| `perf:` `perf(scope):` | Performance |
| `test:` `test(scope):` | Tests |
| `chore:` `chore(scope):` | Chores |
| `ci:` `ci(scope):` | CI/CD |
| `style:` `style(scope):` | Style |
| `build:` `build(scope):` | Build |
| `revert:` | Reverts |
| `BREAKING CHANGE:` in body | Breaking Changes |
| `!` after type (e.g., `feat!:`) | Breaking Changes |

For non-conventional commits (no prefix), classify by content:
- Messages containing "fix", "bug", "patch", "resolve" -> Bug Fixes
- Messages containing "add", "new", "feature", "implement" -> Features
- Messages containing "update", "upgrade", "bump" -> Chores
- Messages containing "remove", "delete", "deprecate" -> Removed
- All others -> Other Changes

Step 1.3 -- Extract Metadata

For each commit, also extract:
- PR/MR number from message (e.g., `(#123)`, `Merge pull request #123`)
- Issue references (e.g., `fixes #45`, `closes #78`)
- Scope from conventional commit (the part in parentheses)
- Author name

============================================================
PHASE 2: CHANGELOG GENERATION
============================================================

Step 2.1 -- Read Existing Changelog

If CHANGELOG.md exists:
- Read its full contents
- Identify the most recent documented version
- Only generate entries for commits AFTER that version
- Preserve the existing file header and formatting style

Step 2.2 -- Format Entries

Use keep-a-changelog format (https://keepachangelog.com):

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [X.Y.Z] - YYYY-MM-DD

### Breaking Changes
- Description of breaking change ([#PR](url))

### Added
- New feature description ([#PR](url))

### Fixed
- Bug fix description ([#PR](url))

### Changed
- Change description ([#PR](url))

### Deprecated
- Deprecation notice ([#PR](url))

### Removed
- Removal description ([#PR](url))

### Security
- Security fix description ([#PR](url))
```

Category mapping from conventional commits to changelog sections:
- feat -> Added
- fix -> Fixed
- perf -> Changed
- refactor -> Changed
- BREAKING CHANGE -> Breaking Changes
- revert -> Removed
- security-related fixes -> Security
- deprecation notices -> Deprecated

Step 2.3 -- Group and Deduplicate

- Group entries by version/tag boundary
- Within each version, group by category (Breaking Changes first, then Added, Fixed, etc.)
- Deduplicate: if a fix commit directly references a feat commit in the same version,
  mention only the feature (the fix was part of getting it right)
- Collapse "fix: fix typo" chains into a single entry
- Omit low-value entries: merge commits, version bumps, pure chore/ci commits
  (unless they are the only changes in a version)

Step 2.4 -- Link Generation

If the project has a git remote, generate comparison links:

```markdown
[Unreleased]: https://github.com/owner/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/owner/repo/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/owner/repo/releases/tag/v1.1.0
```

Detect the remote URL from `git remote get-url origin`.

============================================================
PHASE 3: WRITE AND VERIFY
============================================================

Step 3.1 -- Write CHANGELOG.md

- If updating: prepend new version sections after the header, before existing entries
- If creating: write the complete file
- Ensure consistent formatting throughout

Step 3.2 -- Verify

- Count commits parsed vs entries generated
- Confirm version ordering is correct (newest first)
- Confirm dates match tag dates
- Confirm PR/issue links are properly formatted


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing documentation, validate completeness:

1. Verify all required sections are present and non-empty.
2. Verify internal cross-references and links resolve correctly.
3. Verify no placeholder text remains ("{TODO}", "[TBD]", "...", "etc.").
4. Verify code examples are syntactically valid.

IF VALIDATION FAILS:
- Identify which sections are incomplete or contain placeholders
- Re-generate only the deficient sections
- Repeat up to 2 iterations

============================================================
OUTPUT
============================================================

## Changelog Generated

- **Versions documented:** N
- **Total entries:** N
- **New entries added:** N (if updating)
- **Commits parsed:** N
- **Commits skipped:** N (merge commits, version bumps)
- **File:** CHANGELOG.md

### Version Summary

| Version | Date | Added | Fixed | Changed | Breaking |
|---------|------|-------|-------|---------|----------|
| Unreleased | -- | N | N | N | N |
| vX.Y.Z | YYYY-MM-DD | N | N | N | N |
| ... | ... | ... | ... | ... | ... |


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /changelog — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

============================================================
DO NOT
============================================================

- Do NOT fabricate entries. Every changelog entry must correspond to an actual commit.
- Do NOT include commit hashes in the changelog (use PR/issue links instead).
- Do NOT include internal tooling changes that have no user-facing impact unless
  the project has no user-facing changes at all.
- Do NOT overwrite manually-written changelog entries. Preserve them and append new ones.
- Do NOT include "Co-Authored-By" or similar attribution lines in entries.

NEXT STEPS:

After generating the changelog:
- "Run `/document` to check overall documentation health."
- "Run `/readme` to update the README with the latest version info."
