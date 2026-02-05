---
name: update-changelog
description: Updates notes/changelog.md based on git history. Use when user says "update changelog", "changelog entry", "release version", "release X.Y.Z", or runs /update-changelog.
---

# Update Changelog

Analyze git history since last changelog update and draft entries for `notes/changelog.md`.

## Quick Start

```bash
git log -1 --format="%H" -- notes/changelog.md  # baseline
git log <hash>..HEAD --oneline --no-merges       # commits
git diff <hash>..HEAD --name-only                # files
```

Draft entries → get approval → add to `[Latest additions]` section.

## What to Include

**User-facing:**
- New commands, features, UI changes
- Bug fixes users would notice
- Tool/integration improvements

**Major technical:**
- Architecture changes
- New integrations or services
- Performance improvements
- Security updates

**Exclude:**
- CLAUDE.md, README.md, CONTRIBUTION.md
- Minor refactoring, code cleanup
- Dev tooling config (ruff, mypy)
- Test-only changes, skills

## Entry Format

```markdown
**Added:**
• Feature (what it does for users)

**Changed:**
• Improvement description
```

## Style Guide

**Length:** 1-2 lines max. If longer, split or simplify.

**Patterns:**
- Feature: `Feature name: what it does for users`
- Command: `/command to do X`
- Rename: `Renamed /old → /new`
- Tech context: `(optional detail)` at end

**Start with:**
- Noun (feature name)
- Verb (Support, Improve)
- Command (`/name`)

**Avoid:**
- "Added support for..." → just "Support for..."
- Implementation-only descriptions
- Entries over 2 lines

**Bullets:** Always use `•` (not `-`)

## Release Version

When user says "release X.Y.Z":

1. Move `[Latest additions]` content to new `**[X.Y.Z] - YYYY-MM-DD**` section
2. Update version in:
   - `pyproject.toml`
   - `letta_bot/__init__.py`
3. Leave `[Latest additions]` empty with `**Added:**` and `**Changed:**` placeholders
