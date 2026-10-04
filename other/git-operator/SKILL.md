---
name: git-operator
description: Git operations for repository inspection and management (read-only by default)
activation_keywords: [git, commit, branch, diff, log, status, repository, repo]
execution_mode: client
---

# Git Operator Skill

Provides Git repository operations (read-only mode for safety):
- View repository status
- List commits, branches, tags
- View diffs and file changes
- Show file content at specific commits

Use `builtin_git_operator` tool with fields:
- `operation`: one of "status", "log", "diff", "branch", "show", "blame"
- `repo_path`: path to the git repository
- `args`: (optional) additional arguments (e.g., branch name, file path, commit hash)

Note: Write operations (commit, push, merge) are disabled by default for safety.
