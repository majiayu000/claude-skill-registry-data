---
name: start-issue
description: Start working on a GitHub issue. Use when the user wants to work on an issue, start an issue, or begin implementation.
allowed-tools: [Bash, Read, Grep]
---

# Start Issue Skill

Assists with starting work on a GitHub issue.

**IMPORTANT: When using this skill, announce to the user**: "Using start-issue skill to begin work on an issue."

## Workflow

### 1. View Issue Details

```bash
# View issue content
gh issue view [ISSUE_NUMBER]

# Check labels
gh issue view [ISSUE_NUMBER] --json labels -q '.labels[].name'
```

### 2. Verify Clean State

```bash
# Ensure on main branch with clean state
git checkout main
git pull
git status
```

### 3. Create Branch

Determine prefix based on labels:

| Label | Prefix |
|-------|--------|
| `enhancement` | `feature/` |
| `bug` | `fix/` |
| `refactor` | `refactor/` |
| other | `chore/` |

Branch naming: `prefix/issue-title-in-kebab-case`

```bash
# Example
git checkout -b feature/implement-list-format
```

**Branch naming rules:**
- Use kebab-case (lowercase with hyphens)
- Keep it concise but descriptive
- Derived from issue title
- Examples:
  - `feature/implement-list-format`
  - `fix/memory-leak-in-cache`
  - `chore/update-dependencies`

### 4. Implementation Guide

After creating the branch:

1. **Summarize the issue** - Provide a brief overview of what needs to be implemented
2. **Identify key files** - If the issue specifies files to modify, list them
3. **Outline implementation steps** - Break down the task into actionable steps
4. **Note test requirements** - Highlight any testing needs

### 5. Next Steps

After implementation is complete, guide the user to:

1. **Commit changes** - Use `commit` skill
2. **Create PR** - Use `create-pr` skill
3. **Merge PR** - Use `merge-pr` skill (after CI passes)

## Example Workflow

```bash
# 1. View issue
gh issue view 42

# 2. Check labels
gh issue view 42 --json labels -q '.labels[].name'
# Output: enhancement

# 3. Ensure clean state
git checkout main
git pull

# 4. Create branch (prefix based on label)
git checkout -b feature/add-dark-mode

# 5. Begin implementation...
```

## Key Rules

- **Always start from main branch** with latest changes
- **Use kebab-case** for branch names
- **Derive branch name from issue title** - keep it concise
- **Check labels** to determine appropriate prefix
- **Never include AI attribution** in any output
