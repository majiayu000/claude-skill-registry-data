---
name: changelog
description: Generate a user-facing changelog from git commits — categorize, filter noise, translate to user language. Runs in isolated fork context.
disable-model-invocation: true
context: fork
allowed-tools: Bash(git *) Write
argument-hint: "[since-tag-or-date e.g. v1.0.0 or 2026-04-01]"
---

# Changelog Generator

Generate a clean, categorized changelog from git commits.

## Process

### 1. Gather Commits

Use `$ARGUMENTS` as starting point (tag or date). Default: last 2 weeks.

```bash
# From a tag
git log --oneline --no-merges v1.0.0..HEAD

# From a date
git log --oneline --no-merges --since="$ARGUMENTS"

# Default
git log --oneline --no-merges --since="2 weeks ago" | head -50
```

### 2. Categorize Changes

- **✨ New Features** — new functionality visible to users
- **🔧 Improvements** — enhanced existing functionality
- **🐛 Bug Fixes** — resolved defects
- **🔒 Security** — CVE fixes, dependency upgrades
- **⚠️ Breaking Changes** — API changes, schema migrations
- **📝 Documentation** — doc updates

### 3. Filter Noise

**Exclude**: refactoring, test-only changes, CI/CD changes, merge commits, lint formatting

### 4. Translate to User-Friendly Language

- Remove ticket prefixes
- Replace internal service names with user-facing terms
- Focus on **what changed for the user**, not how

### 5. Output

```markdown
# Release Notes — [Version or Date]

## ✨ New Features
- **[Feature Name]**: [User-facing description]

## 🔧 Improvements
- **[Area]**: [What improved]

## 🐛 Bug Fixes
- Fixed [user-visible issue]

## 🔒 Security
- Updated [dependency] to fix [CVE-ID]
```

Write output to `claude/tasks/changelog-draft.md`.

