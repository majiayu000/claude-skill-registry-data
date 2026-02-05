---
name: worktree
description: Manages git worktrees for parallel development. Creates isolated working directories for tickets/branches, lists active worktrees, and cleans up after merging. Use when starting work on a ticket or cleaning up completed work.
user-invocable: true
allowed-tools: Bash, AskUserQuestion
---

# Worktree Management

## Purpose

Manage git worktrees to enable parallel development. Worktrees let you work on multiple branches simultaneously without stashing or switching — each branch gets its own directory.

## Concepts

### What is a worktree?

A worktree is a linked working directory that shares the same `.git` repository. You can have multiple worktrees, each checked out to a different branch.

### Directory structure

Worktrees are created in a `.worktrees/` directory alongside the main repo:

```
~/projects/
  my-project/                         <- main worktree (on main branch)
  .worktrees/
    my-project-42-feature/            <- linked worktree
    my-project-57-bugfix/             <- linked worktree
```

All worktrees share the same git history but have independent working directories.

### Naming convention

Worktree directories follow the pattern:
```
<repo-name>-<branch-name>
```

Example: If the repo is `api-service` and branch is `42-rate-limiting`:
```
../.worktrees/api-service-42-rate-limiting/
```

## Commands

### Create a worktree

**Usage:** `/worktree create [branch-name]`

Creates a new worktree for the specified branch. If the branch doesn't exist, creates it from origin/main.

#### Workflow

1. **Verify environment**
   ```bash
   git remote -v
   git fetch origin
   ```
   Ensure we have a remote and fresh refs.

2. **Determine repo name**
   ```bash
   basename $(git rev-parse --show-toplevel)
   ```

3. **Ensure .worktrees directory exists**
   ```bash
   mkdir -p ../.worktrees
   ```

4. **Check branch doesn't already exist as worktree**
   ```bash
   git worktree list
   ```
   If branch already has a worktree, report its location instead.

5. **Create the worktree**

   If branch exists remotely:
   ```bash
   git worktree add ../.worktrees/<repo>-<branch> <branch>
   ```

   If branch is new:
   ```bash
   git worktree add ../.worktrees/<repo>-<branch> -b <branch> origin/main
   ```

6. **Report the path**
   Tell the user:
   - Full path to the new worktree
   - How to navigate there: `cd ../.worktrees/<worktree-dir>`
   - Remind them to return to main repo when done

### List worktrees

**Usage:** `/worktree list`

Shows all active worktrees for this repository.

```bash
git worktree list
```

Output shows:
- Path to each worktree
- Current commit
- Branch name

### Clean up a worktree

**Usage:** `/worktree clean [worktree-path-or-branch]`

Removes a worktree after work is complete (typically after PR is merged).

#### Workflow

1. **List current worktrees**
   ```bash
   git worktree list
   ```

2. **Identify which to remove**
   User provides path or branch name. If ambiguous, ask.

3. **Check for uncommitted changes**
   ```bash
   cd <worktree-path>
   git status --porcelain
   ```

   **If changes exist:** STOP and warn user. Ask if they want to:
   - Commit the changes first
   - Discard changes and proceed (requires `--force`)
   - Cancel

4. **Check if branch is merged**
   ```bash
   git branch --merged main | grep <branch-name>
   ```

   If not merged, warn user but allow proceeding if they confirm.

5. **Remove the worktree**
   ```bash
   git worktree remove <worktree-path>
   ```

   Or with force if user confirmed:
   ```bash
   git worktree remove --force <worktree-path>
   ```

6. **Optionally delete the branch**
   Ask user if they also want to delete the branch:
   ```bash
   git branch -d <branch-name>
   ```

7. **Report success**
   Confirm removal and list remaining worktrees.

### Clean up all merged worktrees

**Usage:** `/worktree clean-merged`

Removes all worktrees whose branches have been merged to main.

#### Workflow

1. **List worktrees**
   ```bash
   git worktree list
   ```

2. **For each non-main worktree, check if merged**
   ```bash
   git branch --merged main
   ```

3. **Show user what will be removed**
   List the merged worktrees and ask for confirmation.

4. **Remove each confirmed worktree**
   ```bash
   git worktree remove <path>
   git branch -d <branch>
   ```

5. **Report results**
   Show what was removed and what remains.

## Safety Rules

1. **Never force-remove without explicit user confirmation**
2. **Always check for uncommitted changes before removal**
3. **Warn if branch is not merged before removal**
4. **Never delete main/master worktree**
5. **Never delete branches that aren't fully merged without user confirmation**

## Common Patterns

### Starting work on a ticket

```bash
# From main repo
/worktree create 42-add-rate-limiting

# Output:
# Created worktree at /Users/you/projects/.worktrees/api-service-42-add-rate-limiting
# Navigate there with: cd ../.worktrees/api-service-42-add-rate-limiting
```

### Checking what you're working on

```bash
/worktree list

# Output:
# /Users/you/projects/api-service                                    abc1234 [main]
# /Users/you/projects/.worktrees/api-service-42-add-rate-limiting    def5678 [42-add-rate-limiting]
```

### After PR is merged

```bash
/worktree clean 42-add-rate-limiting

# Output:
# Removed worktree: /Users/you/projects/.worktrees/api-service-42-add-rate-limiting
# Deleted branch: 42-add-rate-limiting
#
# Remaining worktrees:
# /Users/you/projects/api-service  abc1234 [main]
```

## Troubleshooting

### "fatal: '<path>' is already checked out"
The branch is already checked out in another worktree. Use `/worktree list` to find it.

### "worktree is dirty"
There are uncommitted changes. Commit or stash them before removing.

### Branch not found
Ensure you've fetched: `git fetch origin`. If it's a new branch, use the create command which will create it from main.

## Checklist

### Creating
- [ ] Fetch latest from origin
- [ ] Ensure ../.worktrees directory exists
- [ ] Verify branch doesn't already have a worktree
- [ ] Create worktree with correct naming convention
- [ ] Report path and navigation instructions

### Cleaning
- [ ] Check for uncommitted changes
- [ ] Check if branch is merged
- [ ] Get user confirmation if needed
- [ ] Remove worktree
- [ ] Optionally delete branch
- [ ] Report remaining worktrees
