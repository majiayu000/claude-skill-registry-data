---
name: merge-pr
description: Safely merges GitHub pull requests using gh CLI. Use when the user wants to merge a PR, merge a pull request, or complete code review.
allowed-tools: [Bash, Read, Grep]
---

# Merge PR Skill

Assists with safely merging GitHub pull requests using the `gh` CLI, following best practices for code review, CI checks, and merge strategies.

**IMPORTANT: When using this skill, announce to the user**: "Using merge-pr skill to merge a pull request safely."

## Instructions

### 1. Pre-Merge Checks

ALWAYS verify the following before merging:

```bash
# View PR details, status checks, and reviews
gh pr view [PR_NUMBER]

# Check CI status
gh pr checks [PR_NUMBER]

# View PR diff (optional, for review)
gh pr diff [PR_NUMBER]
```

**Required conditions before merging:**
- ✅ All required CI checks must pass
- ✅ Required approvals must be met (check branch protection rules)
- ✅ No unresolved review comments or change requests
- ⚠️ Confirm you have permission to merge

If checks fail:
- Wait for CI to complete
- Address review feedback
- Fix failing tests
- Re-run checks if needed: `gh pr checks --watch [PR_NUMBER]`

### 2. Merge Strategy Selection

**Default: Merge Commit (--merge)**
- Preserves all commits from the PR branch
- Creates a merge commit
- Maintains complete history
- **ALWAYS specify merge commit subject** in this format: `:inbox_tray: Merge pull request #[PR_NUMBER] from [BRANCH_NAME]`

```bash
# Get PR branch name with owner (e.g., "owner/branch-name")
BRANCH_NAME=$(gh pr view [PR_NUMBER] --json headRepositoryOwner,headRefName -q '.headRepositoryOwner.login + "/" + .headRefName')

# Merge with custom subject
gh pr merge [PR_NUMBER] --merge --subject ":inbox_tray: Merge pull request #[PR_NUMBER] from $BRANCH_NAME"
```

**Alternative strategies (use only when appropriate):**

**Squash Merge (--squash)**
- Combines all commits into a single commit
- Use when: PR has many small/WIP commits that should be consolidated
```bash
gh pr merge [PR_NUMBER] --squash
```

**Rebase Merge (--rebase)**
- Replays commits from PR branch onto base branch
- Use when: Small PRs with clean commits, want linear history without merge commit
```bash
gh pr merge [PR_NUMBER] --rebase
```

### 3. Branch Deletion

Branch deletion is handled by GitHub repository settings:
- Repository settings → "Automatically delete head branches"
- If enabled, branches are deleted automatically after merge
- If disabled, branches remain for manual cleanup
- **Do NOT use `--delete-branch` flag** - respect the repository configuration

### 4. Post-Merge Local Update

After merging a PR, ALWAYS update your local default branch:

```bash
# 1. Get the repository's default branch name
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name)

# 2. Switch to the default branch
git checkout "$DEFAULT_BRANCH"

# 3. Pull the latest changes (including the merge)
git pull

# 4. (Optional) Clean up local merged branches
git branch --merged | grep -v "\*" | grep -v "$DEFAULT_BRANCH" | xargs -n 1 git branch -d
```

**Alternative (if you know the default branch name):**
```bash
# If you know it's 'main'
git checkout main && git pull

# If you know it's 'master'
git checkout master && git pull
```

### 5. Complete Merge Workflow

Follow this sequence:

```bash
# 1. Check PR status and reviews
gh pr view [PR_NUMBER]

# 2. Verify all checks pass
gh pr checks [PR_NUMBER]

# 3. Get PR branch name with owner for merge commit subject
BRANCH_NAME=$(gh pr view [PR_NUMBER] --json headRepositoryOwner,headRefName -q '.headRepositoryOwner.login + "/" + .headRefName')

# 4. Merge with default strategy (merge commit) and custom subject
gh pr merge [PR_NUMBER] --merge --subject ":inbox_tray: Merge pull request #[PR_NUMBER] from $BRANCH_NAME"

# 5. Verify merge completed
gh pr view [PR_NUMBER]
# Should show status: MERGED

# 6. Update local repository
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name)
git checkout "$DEFAULT_BRANCH"
git pull

# 7. (Optional) Clean up local merged branches
git branch --merged | grep -v "\*" | grep -v "$DEFAULT_BRANCH" | xargs -n 1 git branch -d
```

### 6. Safety Guidelines

**NEVER merge if:**
- ❌ CI checks are failing
- ❌ There are unresolved change requests from reviewers
- ❌ You don't have proper permissions
- ❌ The PR targets the wrong base branch
- ❌ Required approvals are missing

**ALWAYS:**
- ✅ Read PR description and understand what's being merged
- ✅ Verify CI passes completely
- ✅ Check that required reviews are approved
- ✅ Use `--merge` (default strategy) to preserve commit history
- ✅ Specify merge commit subject as `:inbox_tray: Merge pull request #[PR_NUMBER] from [BRANCH_NAME]`
- ✅ Update local default branch after merging
- ✅ Let GitHub repository settings handle branch deletion

### 7. Common gh pr merge Options

```bash
# Basic merge commit (DEFAULT) - with custom subject
BRANCH_NAME=$(gh pr view [PR_NUMBER] --json headRepositoryOwner,headRefName -q '.headRepositoryOwner.login + "/" + .headRefName')
gh pr merge [PR_NUMBER] --merge --subject ":inbox_tray: Merge pull request #[PR_NUMBER] from $BRANCH_NAME"

# Squash merge (only when needed)
gh pr merge [PR_NUMBER] --squash

# Rebase merge (only when needed)
gh pr merge [PR_NUMBER] --rebase

# Auto-merge (merge when checks pass) - with custom subject
BRANCH_NAME=$(gh pr view [PR_NUMBER] --json headRepositoryOwner,headRefName -q '.headRepositoryOwner.login + "/" + .headRefName')
gh pr merge [PR_NUMBER] --auto --merge --subject ":inbox_tray: Merge pull request #[PR_NUMBER] from $BRANCH_NAME"

# Merge current branch's PR
BRANCH_NAME=$(gh pr view --json headRepositoryOwner,headRefName -q '.headRepositoryOwner.login + "/" + .headRefName')
gh pr merge --merge --subject ":inbox_tray: Merge pull request #[PR_NUMBER] from $BRANCH_NAME"

# Disable auto-merge
gh pr merge [PR_NUMBER] --disable-auto
```

### 8. Working with the Current Branch

If you're on a branch with an open PR:

```bash
# Get current PR number and branch name
PR_NUMBER=$(gh pr view --json number -q .number)
BRANCH_NAME=$(gh pr view --json headRepositoryOwner,headRefName -q '.headRepositoryOwner.login + "/" + .headRefName')

# Merge the PR for current branch
gh pr merge --merge --subject ":inbox_tray: Merge pull request #$PR_NUMBER from $BRANCH_NAME"

# Check PR status for current branch
gh pr status

# View current branch's PR
gh pr view
```

## Examples

### Example 1: Standard Merge with Merge Commit (Default)

```bash
# Check PR status
gh pr view 42

# Verify checks pass
gh pr checks 42

# Get branch name and merge with custom subject
BRANCH_NAME=$(gh pr view 42 --json headRepositoryOwner,headRefName -q '.headRepositoryOwner.login + "/" + .headRefName')
gh pr merge 42 --merge --subject ":inbox_tray: Merge pull request #42 from $BRANCH_NAME"

# Update local default branch
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name)
git checkout "$DEFAULT_BRANCH"
git pull
```

### Example 2: Complete Workflow with Cleanup

```bash
gh pr view 42
gh pr checks 42

# Get branch name and merge
BRANCH_NAME=$(gh pr view 42 --json headRepositoryOwner,headRefName -q '.headRepositoryOwner.login + "/" + .headRefName')
gh pr merge 42 --merge --subject ":inbox_tray: Merge pull request #42 from $BRANCH_NAME"

# Update and clean up
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name)
git checkout "$DEFAULT_BRANCH"
git pull
git branch --merged | grep -v "\*" | grep -v "$DEFAULT_BRANCH" | xargs -n 1 git branch -d
```

### Example 3: Auto-merge with Local Update

```bash
# Get branch name and set PR to auto-merge when checks pass
BRANCH_NAME=$(gh pr view 99 --json headRepositoryOwner,headRefName -q '.headRepositoryOwner.login + "/" + .headRefName')
gh pr merge 99 --auto --merge --subject ":inbox_tray: Merge pull request #99 from $BRANCH_NAME"

# Wait for merge, then update
gh pr view 99  # Check if merged

DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name)
git checkout "$DEFAULT_BRANCH"
git pull
```

### Example 4: Merge Current Branch

```bash
# When you're on the PR branch
gh pr view  # Verify it's the right PR

# Get PR number and branch name
PR_NUMBER=$(gh pr view --json number -q .number)
BRANCH_NAME=$(gh pr view --json headRepositoryOwner,headRefName -q '.headRepositoryOwner.login + "/" + .headRefName')
gh pr merge --merge --subject ":inbox_tray: Merge pull request #$PR_NUMBER from $BRANCH_NAME"

# Update default branch
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name)
git checkout "$DEFAULT_BRANCH"
git pull
```

## Common Pitfalls to Avoid

1. **Don't merge with failing checks**: Always verify `gh pr checks` passes
2. **Don't specify branch deletion**: Let GitHub settings handle it
3. **Don't merge without reviews**: Check that required approvals are present
4. **Don't merge to wrong branch**: Verify base branch in `gh pr view`
5. **Don't forget to update local**: Always pull the default branch after merging
6. **Don't hardcode branch name**: Use `gh repo view --json defaultBranchRef` to get the correct default branch
7. **Don't use squash by default**: Use `--merge` to preserve commit history
8. **Don't forget merge commit subject**: Always use `:inbox_tray: Merge pull request #[PR_NUMBER] from [BRANCH_NAME]` format

## Error Recovery

### If merge fails due to conflicts:
```bash
# PR cannot be merged automatically
# You need to resolve conflicts first

# Update branch with base
gh pr checkout [PR_NUMBER]
git fetch origin
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name)
git merge "origin/$DEFAULT_BRANCH"
# Resolve conflicts
git push

# Then retry merge with custom subject
BRANCH_NAME=$(gh pr view [PR_NUMBER] --json headRepositoryOwner,headRefName -q '.headRepositoryOwner.login + "/" + .headRefName')
gh pr merge [PR_NUMBER] --merge --subject ":inbox_tray: Merge pull request #[PR_NUMBER] from $BRANCH_NAME"
```

### If accidentally merged wrong PR:
```bash
# Revert the merge commit
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name)
git checkout "$DEFAULT_BRANCH"
git pull
git log  # Find the merge commit hash
git revert -m 1 [MERGE_COMMIT_HASH]
git push
```

### If local update fails:
```bash
# Check current branch
git branch

# Ensure you're on the default branch
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name)
git checkout "$DEFAULT_BRANCH"

# If you have uncommitted changes
git stash
git pull
git stash pop
```

## Advanced Usage

### Check repository default branch:
```bash
# Get default branch name
gh repo view --json defaultBranchRef -q .defaultBranchRef.name

# Get full default branch info
gh repo view --json defaultBranchRef
```

### Check if PR is ready to merge:
```bash
# View detailed status
gh pr view [PR_NUMBER] --json statusCheckRollup,reviewDecision

# Watch checks until they complete
gh pr checks [PR_NUMBER] --watch
```

### Merge multiple PRs:
```bash
# Use a loop (be careful!)
for pr in 42 43 44; do
  if gh pr checks $pr; then
    BRANCH_NAME=$(gh pr view $pr --json headRepositoryOwner,headRefName -q '.headRepositoryOwner.login + "/" + .headRefName')
    gh pr merge $pr --merge --subject ":inbox_tray: Merge pull request #$pr from $BRANCH_NAME"
  fi
done

# Update local once after all merges
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name)
git checkout "$DEFAULT_BRANCH"
git pull
```

### Query mergeable state:
```bash
# Check if PR can be merged
gh pr view [PR_NUMBER] --json mergeable,mergeStateStatus
```

## Project-Specific Conventions

Always check if the project has specific merge requirements:
- Read `CONTRIBUTING.md` for merge strategy preferences
- Check branch protection rules on GitHub
- Follow team conventions for commit messages
- Respect required reviewers and approvals
- Default to `--merge` unless project specifies otherwise
- Branch deletion is controlled by repository settings, not by this skill
- Use `gh repo view --json defaultBranchRef` to detect the default branch dynamically
- **Merge commit subject format**: Always use `:inbox_tray: Merge pull request #[PR_NUMBER] from [BRANCH_NAME]`
