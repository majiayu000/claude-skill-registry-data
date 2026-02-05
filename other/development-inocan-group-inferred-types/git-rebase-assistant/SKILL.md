---
name: Git Rebase Assistant
description: Performs interactive rebases with smart commit management and conflict resolution. Use when rebasing branches, cleaning up commit history, resolving conflicts, or when the user mentions "rebase", "interactive rebase", "squash commits", or wants to update their branch with latest changes from main/develop.
---

# Git Rebase Assistant

Helps perform safe, effective rebases with intelligent conflict detection and resolution guidance. Creates safety backups and provides step-by-step assistance through the entire rebase process.

## Core Responsibilities

1. **Prerequisite validation** - Ensure working directory is clean before rebasing
2. **Safety backup creation** - Create backup branches before destructive operations
3. **Smart base branch detection** - Determine appropriate rebase target
4. **Conflict pre-analysis** - Warn about potential conflicts before starting
5. **Step-by-step conflict resolution** - Guide users through resolving conflicts
6. **Interactive rebase support** - Help with squashing, reordering, and editing commits
7. **Recovery assistance** - Help restore branch state if things go wrong

## When to Use Rebase

**Use Rebase when**:
- Updating feature branch with latest main/develop changes
- Cleaning up local commit history before creating PR
- Creating linear, readable git history
- Squashing work-in-progress commits
- Working on branches not yet pushed or shared

**Use Merge when**:
- Working on shared/public branches others depend on
- Preserving exact historical timeline is important
- Merging pull requests into main branch
- You want to avoid force-pushing
- Team prefers merge-based workflows

**Best Practices**:
- ✅ Always create backup branches before rebasing
- ✅ Ensure working directory is clean before starting
- ✅ Use `--force-with-lease` instead of `--force`
- ✅ Test code after resolving conflicts
- ✅ Communicate with team about rebased shared branches
- ❌ Never rebase public/shared branches without coordination
- ❌ Never force push to main/master
- ❌ Never rebase commits already in production

## Quick Reference

### Basic Commands
```bash
# Simple rebase
git rebase <base-branch>
git rebase main
git rebase develop

# Interactive rebase
git rebase -i <base-branch>
git rebase -i HEAD~<n>

# Advanced rebase
git rebase --onto <new-base> <old-base> <branch>
git rebase -i --autosquash <base>
git rebase --rebase-merges <base>
git rebase -i --exec "npm test" <base>

# During rebase
git rebase --continue    # After resolving conflicts
git rebase --abort       # Cancel rebase
git rebase --skip        # Skip current commit

# Force push (after rebase)
git push --force-with-lease                # Safer (recommended)
git push --force-with-lease origin <branch>
git push --force                           # Dangerous
```

### Interactive Rebase Commands
- `pick` (p) - Use commit as-is
- `reword` (r) - Edit commit message
- `edit` (e) - Stop for amending
- `squash` (s) - Combine with previous, keep both messages
- `fixup` (f) - Combine with previous, discard this message
- `drop` (d) - Remove commit
- `exec` (x) - Run shell command

### Conflict Resolution
```bash
git status                     # Check conflicted files
git diff                       # View conflicts
git checkout --theirs <file>   # Accept their changes
git checkout --ours <file>     # Accept our changes
git add <file>                 # Stage resolved file
git rebase --continue          # Continue rebase
```

### Safety & Recovery
```bash
# Create backup before rebase
git branch backup/<branch-name>

# Restore from backup
git reset --hard backup/<branch-name>

# Find lost commits
git reflog
git reset --hard HEAD@{n}
```

## Safe Rebase Workflow (8 Steps)

### Step 1: Validate Prerequisites
```bash
git status                    # MUST be clean
git fetch origin              # Get latest changes
git branch -vv                # View branch info
```
**Stop if**: uncommitted changes exist (commit/stash first) or wrong branch

### Step 2: Create Safety Backup
```bash
git branch backup/$(git branch --show-current)
git branch | grep backup      # Verify created
```

### Step 3: Determine Target Base
- Feature branches → rebase onto `develop` (or `main` if no develop)
- Develop branch → rebase onto `main`
- Hotfix branches → rebase onto `main`

### Step 4: Pre-analyze Conflicts (Optional)
```bash
git diff <base-branch>...HEAD --check
git log --oneline --left-right --cherry-pick <base-branch>...HEAD
```

### Step 5: Execute Rebase
```bash
git rebase <base-branch>      # Standard
git rebase -i <base-branch>   # Interactive
```

### Step 6: Handle Conflicts (If Any)
**Conflict markers**:
```
<<<<<<< HEAD (yours)
Your changes
=======
Incoming changes
>>>>>>> base-branch
```

**Resolve and continue**:
```bash
# Edit files to resolve, then:
git add <resolved-files>
git rebase --continue
```

### Step 7: Verify and Push
```bash
git status
git log --oneline -10
git push --force-with-lease origin $(git branch --show-current)
```

### Step 8: Clean Up Backup
```bash
git branch -d backup/<branch-name>    # Or -D to force
```

## Conflict Resolution

### Conflict Types & Solutions
- **Code conflicts** (both modified same code) → Manually merge logic
- **Dependency conflicts** (different versions) → Choose newer or test compatibility
- **Deletion conflicts** (deleted vs modified) → Decide keep or delete
- **Rename conflicts** (renamed vs modified) → Apply changes to renamed file

### Resolution Strategies

**Accept theirs** (base branch wins):
```bash
git checkout --theirs <file> && git add <file>
```

**Accept ours** (your changes win):
```bash
git checkout --ours <file> && git add <file>
```

**Manual merge** (combine both):
1. Open file, review conflict markers
2. Combine logic from both sides
3. Remove markers (`<<<<<<<`, `=======`, `>>>>>>>`)
4. Test merged code
5. Stage file: `git add <file>`

### Validation
```bash
npm run lint && npm test && npm run build   # JS/TS
python -m py_compile <file> && pytest       # Python
cargo check && cargo test && cargo build    # Rust
```

## Common Scenarios

### 1. Update Feature Branch with Latest Main
```bash
git fetch origin
git checkout feature/my-feature
git rebase origin/main
git push --force-with-lease
```

### 2. Squash Multiple WIP Commits
```bash
git rebase -i HEAD~5
# Change 'pick' to 'squash' for commits to combine
```

### 3. Clean Up Commit Messages
```bash
git rebase -i HEAD~3
# Change 'pick' to 'reword' for commits to rename
```

### 4. Uncommitted Changes Error
```bash
# Error: cannot rebase: You have unstaged changes

# Solution 1: Stash
git stash push -m "WIP before rebase" && git rebase main && git stash pop

# Solution 2: Commit
git add . && git commit -m "WIP" && git rebase main
```

### 5. Wrong Branch
```bash
git rebase --abort
git checkout correct-branch
git rebase main
```

### 6. Multiple Conflicts
```bash
# Resolve each conflict iteratively:
# 1. Edit files → 2. git add <files> → 3. git rebase --continue
# Repeat until complete
```

### 7. Force Push Rejected
```bash
# Someone else pushed - coordinate with team first!
git fetch origin
git log origin/branch..HEAD    # Review changes
git push --force-with-lease    # Safe force push
```

## Recovery from Failed Rebase

```bash
# Abort current rebase
git rebase --abort

# Restore from backup
git reset --hard backup/<branch-name>

# Or find lost commits via reflog
git reflog
git reset --hard HEAD@{n}
```

## Advanced Techniques

### Autosquash Workflow
```bash
# During development, create fixup commits
git commit --fixup=a1b2c3d

# Later, autosquash during rebase
git rebase -i --autosquash main
```

### Exec Commands During Rebase
```bash
# Run tests after each commit
git rebase -i --exec "npm test" main
git rebase -i --exec "npm run lint && npm test" main
```

### Preserving Merge Commits
```bash
git rebase --rebase-merges main
```

### Rebase Onto Specific Commit
```bash
git rebase <commit-hash>
git rebase -i <commit-hash>
git rebase --onto <new-base> <old-base> <branch>
```

### With GitHub/GitLab PRs
```bash
gh pr checkout 123
git rebase main
git push --force-with-lease
# PR automatically updates
```

### With Merge Tools
```bash
git mergetool
git config --global merge.tool vimdiff
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **Rebase stuck/hanging** | Check for editor input or conflict markers; `git status`; abort: `git rebase --abort` |
| **Can't continue after resolving** | Ensure all files staged: `git add <files>`; check for remaining conflict markers; `git diff --check` |
| **Lost commits** | `git reflog` → `git reset --hard HEAD@{n}` or restore from backup |
| **Force push rejected** | Use `--force-with-lease`; if fails, someone pushed → fetch and coordinate with team |
| **Detached HEAD** | `git checkout -b recovery-branch` or `git checkout <branch-name>` |
| **Editor not opening** | Set editor: `git config --global core.editor "vim"` or `GIT_EDITOR=vim git rebase -i main` |

## Resources

- Official Git docs: https://git-scm.com/docs/git-rebase
- Git Book - Rewriting History: https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History
- Atlassian Git tutorials: https://www.atlassian.com/git/tutorials/rewriting-history/git-rebase
- Interactive rebase guide: https://thoughtbot.com/blog/git-interactive-rebase-squash-amend-rewriting-history
- Git rebase vs merge: https://www.atlassian.com/git/tutorials/merging-vs-rebasing
