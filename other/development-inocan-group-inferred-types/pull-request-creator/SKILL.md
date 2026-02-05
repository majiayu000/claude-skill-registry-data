---
name: Pull Request Creator
description: Creates and updates well-formatted pull requests using GitHub CLI. Use when creating PRs, pull requests, submitting code for review, or when the user mentions "pr", "pull request", "create pr", or wants to open a code review. Analyzes all commits since branch divergence and handles existing PRs gracefully.
---

# Pull Request Creator

Helps create comprehensive, well-formatted pull requests following best practices. Automatically analyzes branch commits, detects base branches, and handles existing PRs by updating them instead of failing.

## Core Responsibilities

1. **Prerequisite validation** - Ensure all changes are committed and pushed
2. **Parallel git operations** - Run status checks and branch analysis concurrently
3. **Smart base branch detection** - Automatically determine target branch (develop vs main)
4. **Comprehensive commit analysis** - Review ALL commits since branch divergence
5. **PR template support** - Use `.github/pull_request_template.md` if available
6. **Graceful existing PR handling** - Update existing PRs instead of failing
7. **GitHub CLI integration** - Use `gh` commands for PR management

## When to Use PR Creation vs Manual GitHub UI

**Use this skill when**:
- Need to create PRs quickly from the command line
- Want automated analysis of all commits in the branch
- Need consistent PR formatting across team
- Working with PR templates that should be auto-populated
- Creating multiple PRs in succession
- Integrating PR creation into automated workflows

**Use GitHub UI when**:
- Need to attach screenshots or complex media
- Prefer visual drag-and-drop interface
- Want to browse and compare files visually
- Need to edit PR description with rich formatting
- First time creating a PR in a new repository (to learn the process)

## Installation Check

Verify GitHub CLI is installed and authenticated:

```bash
gh auth status  # Check authentication
# If not installed: brew install gh (macOS) or sudo apt install gh (Linux)
# Then authenticate: gh auth login
```

## Workflow Steps

### Step 1: Validate Prerequisites (Parallel Operations)

Run these commands in parallel using Bash tool:
```bash
# Check for uncommitted changes
git status

# Check if branch is pushed to remote
git branch -vv

# Fetch latest changes from origin
git fetch origin
```

**Stop conditions**:
- If uncommitted changes exist: Prompt user to commit first
- If branch not pushed: Auto-push with `git push -u origin <branch>`

### Step 2: Determine Base Branch

Smart base branch detection following Git Flow patterns:

**Feature branches** (e.g., `feature/auth`, `fix/bug-123`):
- Check if `develop` branch exists
- If yes → target `develop`
- If no → target `main`

**Develop branch**:
- Target `main`

**Other branches**:
- Target `main`

**Override**: User can specify `--base <branch>` to override detection

### Step 3: Analyze Commits

Use `git diff` and `git log` to understand all changes:

```bash
# Get commit history since divergence
git log --oneline <base-branch>...HEAD

# Get detailed diff for analysis
git diff --stat <base-branch>...HEAD
git diff <base-branch>...HEAD
```

**Important**: Analyze ALL commits in the branch, not just the latest one!

### Step 4: Check for PR Template

Look for `.github/pull_request_template.md`:
```bash
# Check if template exists
ls .github/pull_request_template.md
```

If template exists:
- Use template structure
- Fill in relevant sections based on commit analysis

If no template:
- Use default PR format

### Step 5: Generate PR Content

**Title**: Brief, descriptive summary of main change
- Use conventional commit style when appropriate
- Focus on the primary purpose of the PR

**Body structure** (default format):
```markdown
## Description
[Describe the changes made and why they were made]

## Related Issue(s)
[Link or list issues this PR addresses, e.g., Closes #123]

## Type of change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## How has this been tested?
[Describe testing performed to ensure changes work as expected]

## Checklist for Reviewers
- [ ] Code follows project style guidelines
- [ ] Tests cover the new functionality or bug fixes
- [ ] Documentation is updated if necessary
- [ ] Changes do not introduce new security vulnerabilities

Generated with [Claude Code](https://claude.ai/code)
```

### Step 6: Create or Update PR

**Check if PR exists**:
```bash
# Check for existing PR for current branch
gh pr view
```

**If no PR exists**:
```bash
# Create new PR using HEREDOC for body
gh pr create --title "<title>" --body "$(cat <<'EOF'
<PR body content>
EOF
)"
```

**If PR already exists**:
```bash
# First read existing PR to understand current state
gh pr view

# Update existing PR with new title and body
gh pr edit --title "<updated-title>" --body "$(cat <<'EOF'
<updated PR body content>
EOF
)"
```

### Step 7: Handle Options and Flags

Support common `gh pr create` flags:
- `--draft`: Create as draft PR
- `--base <branch>`: Override base branch detection
- `--reviewer <users>`: Request specific reviewers
- `--assignee <users>`: Assign PR to users
- `--label <labels>`: Add labels to PR

Example:
```bash
gh pr create --draft --base develop --title "<title>" --body "..."
```

### Step 8: Return PR URL

After successful creation/update, provide the PR URL to user.

## Base Branch Detection Logic

```
Current Branch Pattern → Target Base
========================   ===========
feature/*               → develop (if exists), else main
fix/*                   → develop (if exists), else main
hotfix/*                → main
develop                 → main
release/*               → main
Other                   → main
--base flag             → Override with specified branch
```

## Common Use Cases

### Feature Branch → Develop/Main
```bash
# Analyze commits and create PR
git log --oneline develop...HEAD
gh pr create --base develop --title "feat: implement user authentication" --body "..."
```

### Hotfix → Main (Urgent)
```bash
gh pr create --base main \
  --title "fix: critical security vulnerability" \
  --label security,priority-critical \
  --reviewer @security-team
```

### Update Existing PR
```bash
gh pr view  # Check existing PR
gh pr edit --body "$(cat <<'EOF'
## Summary
[Updated content]

## Changes from Review
- Fixed issues mentioned in review

🤖 Updated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

### Draft PR for Early Feedback
```bash
gh pr create --draft --title "WIP: Refactor database layer" --body "..."
gh pr ready  # Mark as ready when done
```

### Cross-Repository PR (Fork)
```bash
git remote add upstream https://github.com/original/repo.git
git push -u origin fix/typo
gh pr create --repo original/repo --base main --head username:fix/typo
```

## Error Handling

### PR Already Exists
```bash
# Error: GraphQL: A pull request already exists
gh pr view  # Check existing PR
gh pr edit --title "New title" --body "Updated description"
```

### Uncommitted Changes / Branch Not Pushed
```bash
git status  # Check for uncommitted changes
git push -u origin <branch>  # Push if needed
```

### Authentication Failed
```bash
gh auth login  # Re-authenticate
gh auth status  # Check status
```

### Merge Conflicts
```bash
git fetch origin
git merge origin/main  # Resolve conflicts
git push  # PR auto-updates
```

## Best Practices

- **Clear titles**: Use conventional commit style (feat:, fix:, docs:)
- **Comprehensive summaries**: Explain WHY, not just WHAT; link to issues
- **Test plans**: Include steps for reviewers to verify changes
- **Atomic PRs**: Keep focused; split large changes into multiple PRs

## Security Checks

Never include in PRs:
- API keys, tokens, passwords, certificates
- Database credentials, `.env` files
- `credentials.json`, `*.pem`, `*.key` files

```bash
# Pre-PR security scan
git secrets --scan || gitleaks detect --source .
```

## Quick Reference

```bash
# Create PR
gh pr create --title "feat: feature" --body "Description"
gh pr create --draft  # Draft PR
gh pr create --base develop --reviewer @alice --label bug

# Manage PR
gh pr view  # View current PR
gh pr view --web  # Open in browser
gh pr edit --title "New title" --body "New description"
gh pr comment --body "Comment"
gh pr ready  # Mark draft as ready

# Checks & Merge
gh pr checks  # View CI checks
gh pr checks --watch  # Watch checks
gh pr merge --squash  # Merge with squash
gh pr merge --auto --squash  # Auto-merge when ready

# Analysis
git status  # Check for uncommitted changes
git log --oneline main...HEAD  # View commits
git diff --stat main...HEAD  # View file changes

# List PRs
gh pr list  # All PRs
gh pr list --label bug --author @me  # Filtered
```

## Resources

- GitHub CLI: https://cli.github.com/manual/
- Conventional commits: https://www.conventionalcommits.org/
