---
name: pr-worktree-manager
description: Manages the complete lifecycle of feature development using git worktrees and pull requests. Use when user wants to create feature branches with worktrees, manage PR workflow, clean up after merge, or needs guidance on worktree best practices.
license: MIT
allowed-tools:
  - Bash(git *)
  - Bash(gh *)
  - Bash(ls *)
  - Bash(rm *)
  - Bash(mkdir *)
  - Read(*)
  - Write(*)
---

# PR Worktree Manager

## Overview

This skill manages the complete lifecycle of feature development using git worktrees, from creation through PR merge and cleanup. It provides automation, best practices, and safety checks for a professional development workflow.

## When to Use This Skill

Claude should use this skill when the user:
- Wants to create a new feature branch with worktree
- Mentions "create worktree" or "new feature branch"
- Asks about PR workflow or best practices
- Wants to clean up after PR merge
- Needs help managing multiple worktrees
- Asks "how do I work on multiple features"
- Mentions "delete worktree" or "cleanup branch"

## Workflow Phases

### Phase 1: Feature Setup (Create Worktree)

**When**: User wants to start a new feature

**Process**:
1. **Understand Requirements**
   - Ask feature name (kebab-case preferred)
   - Confirm base branch (usually `main`)
   - Determine worktree location preference

2. **Pre-Creation Checks**
   ```bash
   # Verify we're in a git repository
   git status

   # Check current worktrees
   git worktree list

   # Ensure base branch is up to date
   git fetch origin
   git checkout main
   git pull origin main
   ```

3. **Create Worktree**
   ```bash
   # Format: git worktree add <path> -b <branch-name>
   git worktree add ../<project-name>-<feature-name> -b <feature-name>
   ```

   Example:
   ```bash
   git worktree add ../trustie-mobile-FE-authentication -b feature/authentication
   ```

4. **Verify Creation**
   ```bash
   # List all worktrees
   git worktree list

   # Navigate to new worktree
   cd ../<project-name>-<feature-name>

   # Verify branch
   git branch --show-current
   ```

5. **Initial Setup** (if needed)
   - Run `npm install` or equivalent
   - Create initial commit if needed
   - Push branch to remote: `git push -u origin <branch-name>`

### Phase 2: Development

**When**: User is actively working in the feature worktree

**Guidance**:
1. Work normally in the feature worktree
2. Commit changes regularly
3. Push to remote branch frequently
4. Keep feature branch updated with main (if needed):
   ```bash
   git fetch origin
   git rebase origin/main
   # or
   git merge origin/main
   ```

### Phase 3: Create Pull Request

**When**: Feature is ready for review

**Process**:
1. **Pre-PR Checks**
   ```bash
   # Ensure all changes are committed
   git status

   # Verify tests pass (if applicable)
   npm test

   # Ensure branch is pushed
   git push origin <branch-name>
   ```

2. **Create PR**
   ```bash
   # Using GitHub CLI (recommended)
   gh pr create --title "Feature: <description>" --body "<detailed description>"

   # Or provide URL for manual creation
   echo "Create PR at: https://github.com/<owner>/<repo>/compare/<branch-name>"
   ```

3. **PR Best Practices**
   - Write clear title and description
   - Link to relevant issues
   - Request specific reviewers
   - Add labels/milestones
   - Include testing instructions

### Phase 4: Review & Updates

**When**: PR needs changes based on feedback

**Process**:
1. Make changes in the feature worktree
2. Commit changes
3. Push to remote (PR updates automatically):
   ```bash
   git add .
   git commit -m "Address review feedback: <description>"
   git push origin <branch-name>
   ```

### Phase 5: Cleanup After Merge

**When**: PR has been merged, time to clean up

**IMPORTANT**: Always clean up after PR merge to:
- Reclaim disk space (~2GB per worktree)
- Keep git status clean
- Remove stale branches
- Maintain professional workflow

**Complete Cleanup Process**:

```bash
# Step 1: Navigate to main worktree
cd /path/to/main/worktree

# Step 2: Update main branch with merged changes
git checkout main
git pull origin main

# Step 3: Verify the merge is in main
git log --oneline -10  # Should see your commits

# Step 4: Remove the feature worktree
git worktree remove ../project-name-feature-name

# If it complains about uncommitted changes:
git worktree remove --force ../project-name-feature-name

# Step 5: Delete local branch
git branch -d feature-name

# If not fully merged (rare after PR merge):
git branch -D feature-name  # Force delete

# Step 6: Delete remote branch
# Method A (easiest): Via GitHub UI
# On the PR page, click "Delete branch" button

# Method B: Via command line
git push origin --delete feature-name

# Step 7: Prune stale references
git fetch --prune

# Step 8: Clean up directory (if still exists)
rm -rf ../project-name-feature-name

# Step 9: Verify clean state
git worktree list  # Should not show removed worktree
git branch -a      # Should not show deleted branches
```

**Quick Cleanup One-Liner** (for advanced users):
```bash
cd /path/to/main/worktree && \
git checkout main && \
git pull origin main && \
git worktree remove ../worktree-name --force && \
git branch -d branch-name && \
git fetch --prune && \
rm -rf ../worktree-name
```

Then delete remote branch via GitHub UI.

## Troubleshooting

### Problem: "worktree remove" fails with uncommitted changes

**Solution**:
```bash
cd /path/to/feature/worktree
git status

# Option 1: Commit them
git add -A
git commit -m "Final changes"
git push

# Option 2: Discard them
git reset --hard HEAD

# Option 3: Force remove
cd /path/to/main/worktree
git worktree remove --force ../feature-worktree
```

### Problem: "Cannot delete branch - not fully merged"

**Solution**:
```bash
# Verify branch is actually merged
git branch --merged main | grep feature-name

# If truly merged, force delete
git branch -D feature-name

# For remote
git push origin --delete feature-name --force
```

### Problem: Worktree directory still exists after removal

**Solution**:
```bash
# Manually delete
rm -rf /path/to/worktree-directory

# Clean up git's internal worktree list
git worktree prune
```

### Problem: Multiple worktrees, confused which is which

**Solution**:
```bash
# List all worktrees with branches
git worktree list

# Shows:
# /path/to/main     [main]
# /path/to/feature  [feature-branch]
```

## Best Practices

### Naming Conventions

**Branch Names**:
- Use descriptive names: `feature/authentication`, `fix/login-bug`
- Use kebab-case: `feature-name`, not `feature_name` or `FeatureName`
- Prefix with type: `feature/`, `fix/`, `refactor/`, `docs/`

**Worktree Directory Names**:
- Match project pattern: `project-name-feature-name`
- Keep as siblings to main worktree: `../project-name-feature`
- Example: If main is `trustie-mobile-FE`, feature could be `trustie-mobile-FE-authentication`

### Workflow Tips

1. **One Feature, One Worktree**: Don't try to work on multiple features in one worktree
2. **Keep Main Worktree Clean**: Always work on features in separate worktrees
3. **Delete Promptly**: Clean up worktrees immediately after PR merge
4. **Use GitHub UI for Remote Deletion**: Easiest and safest method
5. **Verify Before Deleting**: Always check `git log` to confirm merge before cleanup

### Storage Management

- Each worktree duplicates: `node_modules`, builds, `.git` data (~2GB)
- Maximum recommended: 2-3 active worktrees
- Clean up merged PRs within 24 hours
- Use `git worktree list` regularly to track active worktrees

## Common Workflows

### Starting a New Feature

**User says**: "I want to work on a new authentication feature"

**Claude does**:
1. Ask for confirmation on feature name
2. Check current worktrees
3. Create worktree with branch
4. Navigate to new worktree
5. Provide next steps

### Cleaning Up After Merge

**User says**: "My PR was just merged, clean it up"

**Claude does**:
1. Verify PR is merged (check GitHub)
2. Update main branch
3. Run cleanup sequence
4. Verify clean state
5. Confirm success

### Managing Multiple Features

**User says**: "I have 3 features in progress, show me status"

**Claude does**:
1. Run `git worktree list`
2. For each worktree, show:
   - Branch name
   - Last commit
   - PR status (if applicable)
3. Suggest which can be cleaned up

## Quick Reference

### Essential Commands

```bash
# Create worktree
git worktree add <path> -b <branch-name>

# List worktrees
git worktree list

# Remove worktree
git worktree remove <path>

# Delete branch
git branch -d <branch-name>

# Prune stale references
git fetch --prune
git worktree prune
```

### Workflow Checklist

**Creating**:
- [ ] Main branch is up to date
- [ ] Feature name is clear
- [ ] Worktree created successfully
- [ ] Branch pushed to remote

**Cleaning Up**:
- [ ] PR is merged
- [ ] Main branch updated
- [ ] Worktree removed
- [ ] Local branch deleted
- [ ] Remote branch deleted (via GitHub UI)
- [ ] References pruned
- [ ] Verified clean with `git worktree list`

## When NOT to Use Worktrees

- Quick fixes on current branch
- Simple one-file changes
- Documentation updates
- Reviewing someone else's PR (use `gh pr checkout` instead)

For simple changes, just work on a branch in your main worktree.

## Integration with Other Tools

### With GitHub CLI (`gh`)

```bash
# Create PR from worktree
gh pr create

# Check PR status
gh pr status

# Checkout someone's PR
gh pr checkout 123

# Delete branch after merge (from GitHub)
# Use UI's "Delete branch" button on PR page
```

### With VS Code

- Each worktree can be opened as a separate VS Code window
- Settings are shared if using workspace settings
- Extensions work in each worktree independently

### With Node/NPM

- Each worktree needs its own `node_modules`
- Run `npm install` in new worktrees
- Consider `node_modules` in `.gitignore` to avoid committing

## Summary

This skill provides a complete, professional workflow for:
1. ✅ Creating feature worktrees
2. ✅ Managing development in parallel
3. ✅ Creating and updating PRs
4. ✅ Cleaning up after merge
5. ✅ Maintaining clean git state

**Key Benefits**:
- Work on multiple features without switching
- Keep features isolated
- Clean, organized workflow
- Automated cleanup
- Best practices built-in
