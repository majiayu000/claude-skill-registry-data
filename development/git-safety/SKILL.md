---
name: git-safety
description: Git safety rules and mandatory gates for all git operations
---

# Git Safety Skill

**CRITICAL:** All git operations MUST go through the `git-operator` worker agent.

## Mandatory Gates (Cannot Be Bypassed)

1. **MUST** verify not on main/master before ANY commit
2. **MUST** check for uncommitted changes before checkout
3. **MUST** restore stashes after workflow completion
4. **MUST** use `-d` not `-D` for branch deletion

## How to Perform Git Operations

- Orchestrators spawn git-operator automatically
- Specialists should spawn git-operator if needed
- **NEVER run git commands directly in agents**

## git-operator Operations

| Operation | Description |
|-----------|-------------|
| `preflight` | Check for uncommitted changes, offer stash |
| `branch-create` | Create and checkout new branch |
| `branch-checkout` | Switch to existing branch |
| `commit` | Stage, commit, verify not on main |
| `push` | Push to origin with tracking |
| `merge` | Squash merge, delete source branch |
| `restore-workflow` | Return to original branch, pop stash |
| `health-check` | Diagnose repository state |

## Workspace Operations (Parallel Execution)

| Operation | Purpose |
|-----------|---------|
| `workspace-create` | Create isolated git worktree |
| `workspace-status` | Poll all workspace states |
| `workspace-commit` | Commit in workspace context |
| `workspace-push` | Push workspace branch |
| `workspace-merge` | Merge with AI conflict resolution |
| `workspace-cleanup` | Remove completed workspaces |

## Branch Naming Convention

```
{type}/{short-description}
```

| Type | Use Case |
|------|----------|
| `feat/` | New features |
| `fix/` | Bug fixes |
| `refactor/` | Code refactoring |
| `docs/` | Documentation only |
| `test/` | Test additions/changes |
| `chore/` | Maintenance tasks |

## Commit Message Format

```
<type>(<scope>): <short description>

<longer description if needed>

- Bullet points for specific changes
- Include test summary if applicable

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

## Spawning git-operator

Example prompt for spawning:

```yaml
subagent_type: git-operator
prompt: |
  [DEPTH: 2/5]

  operation: commit
  files:
    - src/feature.py
    - tests/test_feature.py
  message: |
    feat(feature): Add new feature implementation

    - Core logic implementation
    - Unit tests added (5 tests, all passing)
```

## Safety Verification

Before any destructive operation, git-operator will:

1. Check current branch (abort if main/master)
2. Check for uncommitted changes (offer stash)
3. Verify remote tracking branch exists
4. Confirm operation with user if high-risk
