---
name: managing-stacked-prs
description: Manages stacked pull requests using git-spice. Creates smaller, reviewable PRs that build on each other, submits them for review, handles feedback, and maintains clean stack history. Use when working with git-spice, stacked PRs, or managing dependent branches.
---

# Managing Stacked PRs with git-spice

This skill helps you work with git-spice for managing stacked pull requests - breaking large features into smaller, reviewable chunks that build on each other.

## Core Concepts

**Stacking** means creating branches that build on top of each other:
```
main → feature/database → feature/api → feature/ui
```

Each branch:
- Builds on the one below it
- Can be reviewed and merged independently
- Stays in sync through restacking

## Essential Commands

### Creating Stacks
```bash
gs bc <branch-name>    # Branch Create - stack new branch on current
gs log short           # View stack structure
```

### Submitting PRs
```bash
gs ss                  # Stack Submit - submit all branches as PRs
gs uss                 # Upstack Submit - submit current + above
gs dss                 # Downstack Submit - submit current + below
gs bs                  # Branch Submit - submit only current branch
```

### Keeping in Sync
```bash
gs rs                  # Repo Sync - update trunk, clean merged branches
gs sr                  # Stack Restack - rebase all branches
gs upstack restack     # Rebase current branch + above
```

## Quick Workflows

### Starting a New Stack

1. Sync with trunk: `gs rs`
2. Create first branch: `gs bc feature/part-1`
3. Make changes, commit normally with git
4. Stack next branch: `gs bc feature/part-2`
5. Repeat for each layer
6. View structure: `gs log short`
7. Submit all: `gs ss`

### Handling Review Feedback

1. Checkout the branch: `git checkout <branch-name>`
2. Make changes, commit
3. Restack branches above: `gs upstack restack`
4. Push changes: `git push --force-with-lease`
5. Update upstack PRs: `gs upstack submit`

### After Merges

1. Sync: `gs rs` (updates trunk, removes merged branches)
2. Restack remaining: `gs sr`
3. Update PRs: `gs ss`

## Key Principles

✅ **Always use git-spice for rebasing** - Never use `git rebase` directly on stacked branches

✅ **Sync regularly** - Run `gs rs` to stay up-to-date with trunk

✅ **Restack after changes** - Any change to a lower branch needs `gs upstack restack`

✅ **Commit with git, manage stack with git-spice** - Use normal git for commits, git-spice for stack operations

✅ **Test each layer** - Each branch should work independently

## Common Patterns

### Check current state
```bash
gs log short                    # See stack structure
git status                      # Check for uncommitted changes
gh pr list --author @me        # View your PRs
```

### Submit for review with GitHub CLI
```bash
gs ss                          # Create/update PRs
gh pr view <pr-number>         # View a specific PR
gh pr edit <pr-number> --add-label "stack"
```

### Handle conflicts during restack
```bash
# git-spice will pause, showing conflicts
# Fix conflicts in your editor
git add <resolved-files>
git rebase --continue
# Or abort: git rebase --abort
```

## Detailed Workflows

For step-by-step guides:
- Creating stacks → See [workflows/creating-stacks.md](workflows/creating-stacks.md)
- Submitting and updating → See [workflows/handling-changes.md](workflows/handling-changes.md)

For complete command reference → See [reference/commands.md](reference/commands.md)

## Integration with GitHub

git-spice works with GitHub CLI (`gh`):
- PRs include navigation comments showing stack relationships
- Use `gh pr` commands alongside git-spice
- Edit PR titles/descriptions with `gh pr edit`

## Tips

💡 Use shorthands: `gs bc`, `gs ss`, `gs sr` instead of full commands

💡 Run `gs log short` frequently to verify stack structure

💡 Keep branches small and focused - easier to review and manage

💡 Merge PRs bottom-up - lower branches first, then dependencies

💡 Use `--force-with-lease` when force pushing - safer than `--force`
