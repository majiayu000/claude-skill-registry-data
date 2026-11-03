---
name: commit-changelog
description: Generate a structured CHANGELOG.md from a list of commit messages. Use when someone provides git commits and wants a formatted changelog.
license: MIT
---

# Commit Changelog Generator

Generates a structured `CHANGELOG.md` from commit messages.

## Sections

Include a section only when there are commits that belong to it:

- **Breaking Changes** — commits containing `BREAKING CHANGE:` in the message
- **New Features** — commits with `feat:` prefix
- **Bug Fixes** — commits with `fix:` prefix
- **Other** — commits not matching any of the above

## Output Format

```
## Breaking Changes
- `abc1234`: commit subject

## New Features
- `def5678`: commit subject

## Bug Fixes
- `ghi9012`: commit subject

## Other
- `jkl3456`: commit subject
```

## Rules

- Only include a section if there are commits of that type — omit empty sections entirely
- List commits in reverse chronological order within each section
- Each entry format: `- \`short-hash\`: subject line`
- Save to `CHANGELOG.md`
