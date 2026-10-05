---
name: repo-config
description: Provides dynamic repository configuration patterns for gh-workflow agents. Use when an agent needs the default branch name for diffs, the repository owner/name for API calls, or branch naming and commit conventions for validation.
allowed-tools: Bash, Read
context: fork
agent: Explore
---

# Repository Configuration

Reference skill loaded into agent context via `skills: repo-config`. Provides patterns for dynamic repository detection so agents never hardcode branch names, repo identifiers, or conventions.

## Core Commands

### Default Branch

Used by code-reviewer for diff base and convention-checker for commit range:

```bash
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name')

# Usage in agents:
git diff origin/$DEFAULT_BRANCH..HEAD           # code-reviewer
git log --oneline $DEFAULT_BRANCH..HEAD         # convention-checker
```

### Repository Owner/Name

Used by implementation-planner for GitHub API calls:

```bash
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')

# Usage in agents:
gh api repos/$REPO/issues/$ISSUE_NUMBER/comments
gh api repos/$REPO/pulls/$PR_NUMBER/comments
```

### Combined Fetch

When multiple values are needed, minimize API calls:

```bash
gh repo view --json nameWithOwner,defaultBranchRef --jq '{
  repo: .nameWithOwner,
  default_branch: .defaultBranchRef.name
}'
```

## Conventions

Used by convention-checker to validate branch names and commit messages. These defaults are configurable via `settings.gh-workflow.json` (see `conventions.*` keys in `schema.json`). Commands may also override with project-specific conventions from CLAUDE.md — check CLAUDE.md first, then settings, then these defaults.

### Branch Naming

Configurable via `.conventions.branchPatterns` and `.conventions.additionalBranchTypes` in settings.

| Type | Default Pattern | Example |
|------|----------------|---------|
| Feature | `feature/issue-{N}-{desc}` | `feature/issue-42-add-login` |
| Fix | `fix/issue-{N}-{desc}` | `fix/issue-13-typo` |
| Docs | `docs/issue-{N}-{desc}` | `docs/issue-7-readme` |

Additional branch types can be added via `.conventions.additionalBranchTypes` (e.g., `{"refactor": "refactor/issue-{N}-{desc}", "chore": "chore/issue-{N}-{desc}"}`).

### Commit Prefixes

Configurable via `.conventions.commitTypes` in settings.

| Prefix | Usage |
|--------|-------|
| `feat:` | New features |
| `fix:` | Bug fixes |
| `docs:` | Documentation |
| `refactor:` | Code refactoring |
| `test:` | Test changes |
| `chore:` | Maintenance |

### Detecting Project-Specific Conventions

```bash
# Check CLAUDE.md first (preferred source)
CLAUDE_MD=""
[ -f ".claude/CLAUDE.md" ] && CLAUDE_MD=".claude/CLAUDE.md"
[ -z "$CLAUDE_MD" ] && [ -f "CLAUDE.md" ] && CLAUDE_MD="CLAUDE.md"
[ -n "$CLAUDE_MD" ] && grep -A5 -E "(Branch|Commit|Convention)" "$CLAUDE_MD" 2>/dev/null

# Fall back to inferring from existing patterns
git for-each-ref --sort=-committerdate --format='%(refname:short)' refs/remotes/origin/ | head -10
git log --oneline -20
```

## Agent Integration

This skill is loaded into agent context via `skills: repo-config` in agent frontmatter:

| Agent | What it needs | Key commands |
|-------|--------------|--------------|
| code-reviewer | `DEFAULT_BRANCH` for diff base | `git diff origin/$DEFAULT_BRANCH..HEAD` |
| convention-checker | `DEFAULT_BRANCH` for commit range, conventions for validation | `git log $DEFAULT_BRANCH..HEAD`, branch/commit patterns |
| implementation-planner | `REPO` for GitHub API calls | `gh api repos/$REPO/issues/...` |
| test-runner | Declared but not directly used | — |

## Error Handling

If `gh` commands fail:

| Check | Command | Fix |
|-------|---------|-----|
| Authentication | `gh auth status` | Run `gh auth login` |
| Git repository | `git rev-parse --git-dir` | Navigate to a git repo or run `git init` |
| GitHub remote | `git remote -v` | Add with `git remote add origin <url>` |
