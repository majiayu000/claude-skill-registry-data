---
name: dev-swarm-git-merge
description: Perform git partial merges (checkout specific folders from another branch) and squash merges (clean single-commit integration) to selectively integrate changes across branches.
---

# AI Builder - Git Partial and Clean Merge

This skill helps you perform advanced git merge strategies including partial merges (checking out specific folders from another branch) and squash merges (clean single-commit integration).

## When to Use This Skill

- User asks to merge specific folders or files from another branch
- User wants to perform a partial merge without merging the entire branch
- User asks to squash merge a feature branch into main
- User wants a clean, single-commit integration without preserving commit history
- User needs to selectively sync components between branches

## Your Roles in This Skill

- **DevOps Engineer**: Execute git commands safely, verify branch states, and ensure clean merge operations.
- **Project Manager**: Guide the user through merge strategy selection and validate the merge scope.

## Role Communication

As an expert in your assigned roles, you must announce your actions before performing them using the following format:

As a {Role} [and {Role}, ...], I will {action description}

This communication pattern ensures transparency and allows for human-in-the-loop oversight at key decision points.
## Instructions

Follow these steps to perform git partial or clean merges:

### Step 1: Understand the Merge Requirements

**As a Project Manager, ask the user to clarify:**

1. What type of merge do they need?
   - **Partial merge**: Merge specific folders/files only
   - **Squash merge**: Merge all changes as a single commit

2. For partial merge:
   - Which source branch contains the folders/files?
   - Which specific folders/files need to be merged?
   - Which target branch should receive them?

3. For squash merge:
   - Which source branch to merge from?
   - Which target branch to merge into?
   - What should the commit message be?

### Step 2: Check Git Status

**As a DevOps Engineer, verify the current state:**

```bash
# Check current branch
git branch

# Check for uncommitted changes
git status

# View recent branches
git branch -a
```

**Important:** If there are uncommitted changes, ask the user whether to:
- Stash them: `git stash`
- Commit them first
- Abort the merge operation

### Step 3: Perform the Merge

#### Option A: Partial Merge (Specific Folders/Files)

**As a DevOps Engineer, execute the partial merge:**

```bash
# Switch to the target branch (where you want the folders)
git checkout target-branch

# Checkout specific folders from source branch
git checkout source-branch -- path/to/folder1 path/to/folder2

# Stage the changes
git add path/to/folder1 path/to/folder2

# Commit the changes
git commit -m "Merge specific folders from source-branch"
```

**Example:**
```bash
# Merge only the docs and config folders from feature-branch to main
git checkout main
git checkout feature-branch -- docs config
git add docs config
git commit -m "Sync docs and config from feature-branch"
```

#### Option B: Squash Merge (Clean Single-Commit)

**As a DevOps Engineer, execute the squash merge:**

```bash
# Switch to target branch
git checkout target-branch

# Perform squash merge (stages all changes but doesn't commit)
git merge --squash source-branch

# Review staged changes
git status

# Commit with a meaningful message
git commit -m "Add feature: descriptive message summarizing all changes"
```

**Example:**
```bash
# Squash merge a feature branch into main
git checkout main
git merge --squash feature/user-authentication
git commit -m "Add user authentication feature with JWT and OAuth support"
```

### Step 4: Verify the Merge

**As a DevOps Engineer, verify the merge was successful:**

```bash
# Check the commit was created
git log -1

# Verify the changes
git diff HEAD~1

# Check branch status
git status
```

### Step 5: Push Changes (Optional)

**As a Project Manager, ask the user if they want to push:**

If yes, as a DevOps Engineer:
```bash
# Push to remote
git push origin target-branch
```

## Merge Strategy Comparison

| Aspect | Partial Merge | Squash Merge |
|--------|---------------|--------------|
| Scope | Selective files/folders only | All changes from branch |
| Commit History | Not applicable | Squashed into one commit |
| Use Case | Selective sync of components | Clean integration of features |
| Reversibility | Easy to revert specific files | Reverts entire feature at once |

## Best Practices

**Partial Merge:**
- Always review changes with `git diff` before committing
- Use meaningful commit messages indicating source branch
- Verify the correct folders/files are staged before committing

**Squash Merge:**
- Write comprehensive commit messages that summarize all changes
- Review all staged changes before committing
- Document breaking changes or important notes in the commit message
- Consider keeping the source branch until changes are confirmed working

**General:**
- Always work on a clean working directory (commit or stash changes first)
- Test changes thoroughly after merge
- Communicate merge strategy with team members
- Use `git status` frequently to verify state

## Examples

### Example 1: Merge Documentation from Feature Branch

```bash
git checkout main
git checkout feature/new-api -- docs/api
git add docs/api
git commit -m "Update API documentation from feature/new-api"
```

### Example 2: Squash Merge Feature Branch

```bash
git checkout main
git merge --squash feature/shopping-cart
git commit -m "Add shopping cart feature with add/remove/checkout functionality"
git push origin main
```

### Example 3: Merge Multiple Folders

```bash
git checkout develop
git checkout feature/redesign -- src/components src/styles
git add src/components src/styles
git commit -m "Merge redesigned components and styles from feature/redesign"
```

## Common Issues

**Issue: "error: pathspec 'folder' did not match any file(s) known to git"**
- Solution: The folder/file doesn't exist in the source branch. Verify with `git ls-tree -r source-branch --name-only`

**Issue: Merge conflicts during squash merge**
- Solution: Resolve conflicts manually, then `git add` the resolved files and `git commit`

**Issue: Accidentally merged wrong folders**
- Solution: If not pushed yet, use `git reset HEAD~1` to undo the commit, then repeat with correct paths

**Issue: Uncommitted changes blocking checkout**
- Solution: Stash changes with `git stash`, perform merge, then `git stash pop`
