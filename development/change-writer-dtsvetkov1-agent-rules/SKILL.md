---
name: change-writer
description: Generates clean, human-readable changelogs and release notes from git commits and file changes. Use when preparing for a release or summarizing recent work.
---

# Change Writer Skill

This skill analyzes recent changes in the repository to generate structured changelogs. It categorizes changes into Features, Fixes, and Refactors.

## Instructions

1. **Analyze History**: Run the git log command to see recent changes.
2. **Identify Impact**: Look at changed files to understand the scope (e.g., UI, logic, infrastructure).
3. **Draft Notes**: Group changes by type (Feat, Fix, Chore, Docs).
4. **Format**: Output in Markdown format compatible with `CHANGELOG.md` or GitHub Releases.

## Categories

- **🚀 Features**: New functionality.
- **🐛 Bug Fixes**: Resolving issues.
- **⚡ Performance**: Speed optimizations.
- **🧹 Chores**: Internal tasks, dependency updates.
- **📝 Documentation**: Changes to docs.

## Example Output

```markdown
## [1.2.0] - 2025-12-27

### 🚀 Features
- Added `Zustand` store for global theme management.
- Implemented `api-expert` skill for better backend integration.

### 🐛 Bug Fixes
- Fixed keyboard avoiding view overlap on Android.
- Resolved race condition in auth flow.

### 🧹 Chores
- Updated `expo` to SDK 54.
- Cleaned up unused assets.
```

Run `scripts/get-changes.sh` to see a summary of unstaged changes.
