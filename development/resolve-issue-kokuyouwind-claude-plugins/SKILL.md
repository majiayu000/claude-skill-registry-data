---
name: resolve-issue
description: Provides a systematic workflow for resolving GitHub Issues. Use this skill when assigned a GitHub Issue or when delegated by the Issue Auto-resolver.
---

# Resolve Issue

## Instructions

### Step 1: Determine Issue Type

Check if the Issue has a `type:*` label. If not, determine the type from the title and body:

| Label | Description |
|-------|-------------|
| `type:bug` | Fix bugs, errors, or defects |
| `type:feature` | Add new features |
| `type:enhancement` | Improve existing features |
| `type:refactoring` | Code refactoring |
| `type:documentation` | Update documentation |
| `type:investigation` | Investigation or analysis tasks |

Default to `type:feature` if unclear.

### Step 2: Follow Type-Specific Instructions

Refer to the corresponding file at `{plugin_base_path}/issue-types/<type>.md`:

- `bug.md` - Bug fixes
- `feature.md` - New features
- `enhancement.md` - Feature improvements
- `refactoring.md` - Code refactoring
- `documentation.md` - Documentation updates
- `investigation.md` - Investigation tasks

### Related Skills

This skill works with the following dev-guidelines skills:

| Skill | When to Use |
|-------|-------------|
| `dev-guidelines:git-repository-workflow` | Git branch management and testing |
| `dev-guidelines:pr-description-format` | Creating PRs with `gh pr create` |
| `dev-guidelines:debugging-process` | Investigating bugs and tracing errors |
| `dev-guidelines:design-alternatives` | Evaluating implementation approaches |

### Notes

- `{plugin_base_path}` refers to the plugin installation directory
- **Language**: Unless otherwise specified, write all Issue comments, PR titles, PR descriptions, and commit messages in Japanese (日本語で記述)
