---
name: pr
description: "Create a pull request with intelligent base branch detection. Use when: (1) User says 'create pr', 'make pr', or 'open pr', (2) User wants to create a PR from the current branch, (3) User has finished work on a feature branch and needs a PR. Auto-detects base branch from conversation, git history, or repo default."
argument-hint: "[target-branch]"
---

# PR Command

Create a pull request with automatic base branch detection from conversation history, git log, or repository default.

## Usage

- `/pr` - Create PR with auto-detected base branch
- `/pr <target-branch>` - Create PR targeting the specified branch

## Steps

### 1. Verify Current State

```bash
git status
git branch --show-current
```

Ensure you're on a feature branch (not main/master/develop).

### 2. Determine Base Branch

**Priority order for base branch detection:**

1. **Explicit argument**: If `<target-branch>` is provided, use it directly
2. **Conversation context**: Search conversation history for mentions of:
- "based on", "branch from", "create branch from"
- PR context or issue references that mention a target branch
- Recent git commands showing branch creation
3. **Git history**: Auto-detect from git log and merge-base
4. **Repository default**: Use the default branch as fallback

#### Conversation History Check

Search the current conversation for clues about the base branch:

- Look for phrases like "create branch from develop", "based on feature-x"
- Check if user mentioned which branch they started from
- Look for issue/PR context that indicates the target

#### Git History Detection

```bash
# Fetch latest remote refs
git fetch origin

# Find merge-base with candidate branches
for branch in main master develop staging; do
  git merge-base HEAD origin/$branch 2>/dev/null && echo "Found: $branch"
done

# Check which branch has the closest merge-base
# The branch with most recent common ancestor is likely the parent
```

#### Repository Default Fallback

```bash
# Get the default branch
gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'
```

### 3. Check for Existing PR

```bash
gh pr list --head $(git branch --show-current)
```

If PR exists, ask user if they want to view or update it.

### 4. Analyze Changes

```bash
# Get commits
git log origin/<base-branch>..HEAD --oneline

# Get file changes
git diff origin/<base-branch>..HEAD --stat
```

### 5. Confirm with User

Before creating, confirm:

- **Current branch**: `<branch-name>`
- **Target base branch**: `<base-branch>` (with detection method: "specified", "from conversation", "auto-detected", or "default")
- **Commits**: Number of commits to include
- **Suggested PR title**: Based on commits/branch name

### 6. Push and Create PR

```bash
# Push if needed
git push -u origin $(git branch --show-current)

# Create PR
gh pr create \
  --base <base-branch> \
  --title "<title>" \
  --body "$(cat <<'EOF'
## Summary
<description>

## Changes
- <change 1>
- <change 2>

## Test Plan
<testing instructions>
EOF
)"
```

### 7. Report Result

Display:

- PR URL
- PR number
- Base branch (and how it was determined)
- Head branch

## Detection Logic

The command uses this logic to find the base branch:

1. **User-specified**: Highest priority - use the argument directly
2. **Conversation analysis**: Check conversation for branch context
3. **Git merge-base**: Find closest common ancestor with candidate branches
4. **Default branch**: Ultimate fallback using `gh repo view`

If detection is ambiguous, ask the user to clarify before creating the PR.

## Important Notes

- Never assume main/master without verification
- Always inform user how the base branch was determined
- Verify branch is pushed before creating PR
- Include meaningful PR title and description
