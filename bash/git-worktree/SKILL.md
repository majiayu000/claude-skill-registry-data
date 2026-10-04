---
name: "git-worktree"
description: "Create isolated git worktrees for reviewing PRs, branches, tags, or commits without affecting main working directory."
---

# Git Worktree

## Scripts

**Setup:** `"${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/setup-worktree.sh" --pr|--branch|--tag|--commit <VALUE>`
Options: `--editor skip` | `--editor-cmd <code|idea|claude>`

**Open main:** `"${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/open-main-worktree.sh"`

**Cleanup:** `"${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/cleanup-worktree.sh" --pr|--branch <VALUE>`
Options: `--yes` or `-y` (skip confirmation)

## Behavior

- Location: `../<project>.worktrees/<folder-name>`
- IDE auto-detection: VS Code, JetBrains, or Claude CLI
- Branch handling: local branches used directly, remote → `worktree-branch-<name>`, PRs → `worktree-pr-<number>`, tags/commits → detached HEAD
- Windows: prefix with `bash` (requires Git Bash)
