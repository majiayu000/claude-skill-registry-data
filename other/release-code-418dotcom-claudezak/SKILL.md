---
description: Generate audience-aware release notes from git history
argument-hint: "[version or date range]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(git log:*, git tag:*, git diff:*, date:*)
---

Auto-generate release notes from git history. Produces audience-appropriate versions — technical changelog, marketing announcement, or executive summary — from the same data.

## Steps

### Step 1: Determine the range

Figure out what commits to include:
- If user specified a version → find the tag range (e.g., `git log v1.2.0..v1.3.0`)
- If user specified dates → use date range (`git log --after="2025-01-01" --before="2025-02-01"`)
- If nothing specified → changes since last tag (`git log $(git describe --tags --abbrev=0)..HEAD`)

### Step 2: Gather commit data

```bash
git log [range] --format="%h %s" --no-merges
```

Also check:
- PR descriptions if available (`git log --merges` for merge commit messages)
- Any CHANGELOG entries
- Modified files to understand scope (`git diff --stat [range]`)

### Step 3: Categorise changes

Sort every change into:

| Category | Icon | Example |
|----------|------|---------|
| **New Features** | Added | New capability, new endpoint, new component |
| **Improvements** | Changed | Performance boost, UX improvement, refactor |
| **Bug Fixes** | Fixed | Resolved issue, corrected behaviour |
| **Breaking Changes** | Breaking | API change, removed feature, migration needed |
| **Dependencies** | Deps | Updated packages, new dependencies |
| **Internal** | Internal | Tests, CI, docs, refactoring |

### Step 4: Write release notes (3 versions)

**Version 1 — Technical Changelog** (for developers):
```markdown
# [Version] — [Date]

## Breaking Changes
- [change with migration instructions]

## New Features
- [feature]: [description] ([commit hash])

## Improvements
- [improvement] ([commit hash])

## Bug Fixes
- [fix] ([commit hash])

## Dependencies
- Updated [package] from [old] to [new]
```

**Version 2 — Marketing Announcement** (for customers/public):
```markdown
# What's New in [Version]

[1-2 sentence hook — the most exciting change]

### [Feature Name]
[Benefit-focused description — what it means for the user, not how it works]

### [Improvement]
[User-facing improvement with before/after if applicable]

### Bug Fixes
[Summary — "Fixed X issues including..." — no commit hashes]
```

**Version 3 — Executive Summary** (for stakeholders):
```markdown
# Release Summary — [Version]

**Impact:** [one sentence — what this release accomplishes]

**Key changes:**
- [Top 3 changes, business-impact framing]

**Metrics:**
- [X] features added
- [X] bugs fixed
- [X] files changed

**Risk:** [any breaking changes or migration needs — or "None"]
```

### Step 5: Save and output

Save to `releases/[version]-release-notes.md` with all three versions.

Output the marketing version by default (most commonly needed), and mention the other versions are in the file.
