---
name: creating-pull-requests
description: Guides creating GitHub pull requests with proper branch naming, commit messages, and PR descriptions. Use when asked to create a PR, submit changes for review, or push a feature branch.
---

# Creating Pull Requests

Process for creating well-structured GitHub pull requests.

## Before Creating a PR

```bash
# 1. Check modified files
git status
git diff

# 2. Ensure you're on a feature branch, not master
git branch

# 3. Run pre-commit checks
npm run format && npm run lint && npm run test:unit
```

## Branch Naming

| Prefix | Use Case |
|--------|----------|
| `feature/` | New functionality |
| `fix/` | Bug fixes |
| `docs/` | Documentation changes |
| `chore/` | Maintenance, dependencies, config |

Examples:
- `feature/folder-organization`
- `fix/episode-tracking-bug`
- `docs/update-readme`
- `chore/upgrade-dependencies`

## Commit Message Prefixes

Match the branch type:

| Branch | Commit Prefix |
|--------|---------------|
| `feature/` | `feat:` |
| `fix/` | `fix:` |
| `docs/` | `docs:` |
| `chore/` | `chore:` |

Additional prefixes: `test:`, `refactor:`, `style:`

**Format:** 72 characters max for title line

```bash
git commit -m "feat: add folder organization for anime lists

- Implement drag-and-drop reordering
- Add color customization for folders
- Include collapse/expand functionality"
```

## PR Description Format

```markdown
## Problem
[What issue or limitation exists? Why is this change needed?]

## Solution
[High-level description of the approach taken. No code details—focus on the "what" and "why"]
```

Keep descriptions concise and reviewer-friendly. Explain context at a higher level without referencing specific code changes.

## Creating the PR

```bash
# 1. Create and switch to feature branch
git checkout -b feature/your-feature-name

# 2. Make changes and commit
git add .
git commit -m "feat: description of changes"

# 3. Push to remote
git push -u origin feature/your-feature-name

# 4. Create PR using GitHub CLI
gh pr create --title "feat: your feature title" --body "$(cat <<'EOF'
## Problem
Description of the problem or need.

## Solution
High-level description of the solution.
EOF
)"
```

## Complete Workflow Example

```bash
# Check current state
git status
git diff

# Create feature branch
git checkout -b feature/add-dark-mode

# Make changes...

# Run checks
npm run format && npm run lint && npm run test:unit

# Commit
git add .
git commit -m "feat: add dark mode toggle

- Add theme context provider
- Implement CSS variables for theming
- Add toggle in settings page"

# Push and create PR
git push -u origin feature/add-dark-mode

gh pr create \
  --title "feat: add dark mode toggle" \
  --body "$(cat <<'EOF'
## Problem
Users have requested dark mode support to reduce eye strain during nighttime viewing sessions.

## Solution
Implemented a theme toggle in the settings page that switches between light and dark modes using CSS variables. The preference is persisted in chrome.storage.local.
EOF
)"
```

## PR Examples

### Good PR Description

```markdown
## Problem
Users cannot organize their anime lists into custom categories, making it difficult to manage large collections.

## Solution
Added folder functionality that allows users to create, rename, and color-code folders. Anime items can be dragged between folders, and folder order can be customized via drag-and-drop.
```

### Bad PR Description (avoid)

```markdown
## Problem
Need folders

## Solution
Added FolderList.vue component with createFolder(), deleteFolder(), and renameFolder() methods. Modified useAnimeStore to include folders array and folderMap object...
```

## Checklist

- [ ] On feature branch (not master)
- [ ] Branch name follows convention (`feature/`, `fix/`, `docs/`, `chore/`)
- [ ] All changes committed with proper prefix
- [ ] Pre-commit checks pass (`npm run format && npm run lint && npm run test:unit`)
- [ ] PR title matches commit prefix
- [ ] PR description has Problem and Solution sections
- [ ] Description is high-level, not code-focused
