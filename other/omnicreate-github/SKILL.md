---
name: omnicreate-github
description: Use when creating a GitHub pull request (OmniForge). Auto-populates title and description from commits, supports draft PRs, labels, assignees, reviewers, and issue linking
version: 1.0.0
license: Apache-2.0
allowed-tools: Bash, mcp__omniforge__create_github_pr
---

# GitHub Pull Request Creator

## Context

- Current git status: !`git status --porcelain`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -5`
- GitHub remote: !`git remote -v | grep github | head -1`
- gh version: !`gh version 2>/dev/null || echo "NOT_INSTALLED"`
- gh auth status: !`gh auth status 2>&1 || echo "NOT_AUTHENTICATED"`
- Unpushed commits: !`git log @{u}..HEAD --oneline 2>/dev/null || echo "NO_UPSTREAM"`
- Repo root: !`git rev-parse --show-toplevel 2>/dev/null || echo "NOT_A_GIT_REPO"`

## Your Task

Create a GitHub pull request using the `mcp__omniforge__create_github_pr` MCP tool.

> **Why MCP instead of raw bash?**
> The MCP tool validates all inputs, uses safe subprocess execution (no shell interpretation), and provides structured error output — making it safe for use by all models without risk of shell injection.

### Prerequisites

1. Verify `gh` is installed. If not, inform the user:
   ```bash
   brew install gh  # macOS
   sudo apt install gh  # Debian/Ubuntu
   ```
2. Verify the current directory is a git repository with a GitHub remote.
3. Ensure there are commits to create a PR from (not on main/master without changes).

### Pre-Flight Checklist

Before creating the PR, verify:

1. **Check environment**: Verify `gh` is installed and authenticated, git repo has GitHub remote
2. **Check branch**: If on main/master, inform user they need to create a feature branch first
3. **Check for changes**: If no commits, inform user they need to commit changes first
4. **Warn about uncommitted changes**: If working directory is dirty, warn user before proceeding
5. **Get repo root**: Run `git rev-parse --show-toplevel` to obtain the absolute path
6. **Call MCP tool**: Invoke `mcp__omniforge__create_github_pr` with `repo_root` and any user-specified options
7. **Report output**: Show the PR URL, number, and any relevant details from the tool response

### MCP Tool: `mcp__omniforge__create_github_pr`

Use this tool for all PR creation. It wraps `gh pr create` safely.

**Required parameter:**
- `repo_root`: absolute path to the git repository root (from `git rev-parse --show-toplevel`)

**Optional parameters (pass only what the user specified):**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | string | "" | Custom PR title (overrides auto-fill) |
| `description` | string | "" | Custom PR body (overrides auto-fill) |
| `target_branch` | string | "main" | Target/base branch for the PR |
| `source_branch` | string | "" | Source/head branch (default: current branch) |
| `assignees` | string | "" | Comma-separated usernames to assign |
| `reviewers` | string | "" | Comma-separated usernames to request review from |
| `labels` | string | "" | Comma-separated label names |
| `draft` | bool | false | Create as draft PR |
| `fill` | bool | true | Auto-populate title/description from commits |
| `push` | bool | true | Push the branch if not already pushed |

### Common Patterns

**Default PR (auto-filled from commits):**
→ Call `mcp__omniforge__create_github_pr` with just `repo_root`

**PR for a specific target branch with assignee:**
→ `repo_root`, `target_branch="staging"`, `assignees="john"`

**Draft PR with WIP label:**
→ `repo_root`, `draft=true`, `labels="WIP"`

**PR with custom title and description:**
→ `repo_root`, `title="Fix bug"`, `description="Detailed description..."`, `fill=false`

**PR linked to issue #42:**
→ Create PR normally, then manually comment `Closes #42` in the description

### Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `authentication required` | Not logged in | Run `gh auth login` |
| `no upstream branch` | Branch not pushed | The tool handles push automatically (`push=true`) |
| `branch already exists remotely` | Push conflict | Pull and rebase, or force push with caution |
| `merge conflicts detected` | Conflicts with target | Rebase onto target branch and resolve |
| `Could not resolve to a Repository` | Wrong remote | Verify the repo has a GitHub remote |

### Edge Cases to Handle

- **Not a git repo**: Inform user they need to be in a git repository
- **No GitHub remote**: Inform user the repo doesn't have a GitHub remote
- **gh not installed**: Provide installation instructions
- **Not authenticated**: Run `gh auth login` if needed
- **No commits**: Inform user they need to commit changes first
- **Already on main/master**: Ask user which branch to create PR from
- **Uncommitted changes**: Warn user their working directory has changes not in the PR

### Output Format

After the MCP tool returns, provide a summary like:

```
✅ Pull Request created successfully!

**PR #42**: feat: add user authentication
**URL**: https://github.com/owner/repo/pull/42
**Branch**: feature/auth → main
**Draft**: No

Reviewers: @john, @jane
Labels: enhancement, needs-review
```

### Important Notes

- **No `--fill` in gh**: Unlike `glab`, `gh` doesn't have a `--fill` flag. When `fill=True`, the MCP tool auto-populates the title from the latest commit and the description from the commit body.
- **No `--yes` needed**: `gh pr create` is non-interactive when all required arguments are provided via flags.
- **Worktree support**: The tool resolves the main repo root when called from a linked worktree.
