---
name: git-pr-helper
description: Git workflow assistant for pull request creation, branch management, and merge coordination. Use when creating PRs, merging branches, resolving conflicts, or cleaning up session branches. Provides intelligent PR descriptions, safety checks, and workflow guidance.
allowed-tools: [Bash, Read, Write, Edit, Glob, Grep]
---

# Git PR Helper

Expert at managing git workflows for pull requests, merges, and branch management with a focus on safety, quality, and best practices.

## Core Mission

Assist with pull request creation, branch management, merge coordination, and conflict resolution while ensuring code quality and preventing data loss.

## When to Use This Skill

Use this skill when:
- Creating a pull request from a feature branch
- Merging branches (feature → main/master)
- Resolving merge conflicts
- Cleaning up old session or feature branches
- Generating PR descriptions from commits
- Checking if work is ready to merge
- Recovering from git mistakes

**Do NOT use this skill for:**
- Preventing file deletion (use git hooks + CLAUDE.md instead)
- Creating session branches at workflow start (use CLAUDE.md guidance)
- Enforcing branch policies (use git hooks instead)

## Skill Capabilities

### 1. Pull Request Creation

**Purpose:** Create high-quality pull requests with comprehensive descriptions

#### Create PR with Generated Description

To create a PR:

1. **Verify we're on a feature branch:**
   ```bash
   CURRENT_BRANCH=$(git branch --show-current)
   if [ "$CURRENT_BRANCH" = "main" ] || [ "$CURRENT_BRANCH" = "master" ]; then
       echo "❌ ERROR: Cannot create PR from main/master branch"
       exit 1
   fi
   echo "✓ Current branch: $CURRENT_BRANCH"
   ```

2. **Check git status is clean:**
   ```bash
   if [ -n "$(git status --porcelain)" ]; then
       echo "⚠️  WARNING: Uncommitted changes detected"
       git status --short
       echo ""
       echo "Commit these changes before creating PR? (y/n)"
       # Ask user via AskUserQuestion tool
   else
       echo "✓ Working tree clean"
   fi
   ```

3. **Determine base branch:**
   ```bash
   # Try to detect default branch
   BASE_BRANCH=$(git remote show origin 2>/dev/null | grep 'HEAD branch' | cut -d' ' -f5)

   # Fallback to checking what exists
   if [ -z "$BASE_BRANCH" ]; then
       if git show-ref --verify --quiet refs/heads/main; then
           BASE_BRANCH="main"
       elif git show-ref --verify --quiet refs/heads/master; then
           BASE_BRANCH="master"
       else
           echo "⚠️  Cannot detect base branch. Please specify manually."
       fi
   fi

   echo "Base branch: $BASE_BRANCH"
   ```

4. **Get all commits on this branch:**
   ```bash
   # Get commit history since branch diverged from base
   git log $BASE_BRANCH..HEAD --oneline

   # Get detailed commit info
   git log $BASE_BRANCH..HEAD --format="%h %s%n%b" --reverse
   ```

5. **Get diff summary:**
   ```bash
   # File changes summary
   git diff $BASE_BRANCH...HEAD --stat

   # List changed files
   git diff $BASE_BRANCH...HEAD --name-only
   ```

6. **Generate PR description:**

   Analyze commits and changes to create:

   ```markdown
   ## Summary
   - [Brief bullet points of main changes]
   - [Focus on WHY, not WHAT]
   - [User-facing impact]

   ## Changes Made
   - [Detailed technical changes]
   - [Components affected]
   - [API changes if applicable]

   ## Testing
   - [ ] Unit tests added/updated
   - [ ] Manual testing completed
   - [ ] Edge cases considered
   - [ ] Documentation updated

   ## Related Issues
   Closes #[issue-number] (if applicable)

   ## Notes for Reviewers
   [Any context reviewers should know]
   [Areas needing special attention]
   ```

7. **Check if remote tracking branch exists:**
   ```bash
   if git rev-parse --verify --quiet origin/$CURRENT_BRANCH >/dev/null 2>&1; then
       echo "✓ Remote branch exists"
   else
       echo "⚠️  Remote branch does not exist. Need to push first."
       echo "Push now? (y/n)"
       # If yes: git push -u origin $CURRENT_BRANCH
   fi
   ```

8. **Create PR using GitHub CLI:**
   ```bash
   gh pr create \
       --title "[Generated title from commits]" \
       --body "$(cat <<'EOF'
   [Generated PR description]
   EOF
   )" \
       --base "$BASE_BRANCH" \
       --head "$CURRENT_BRANCH"
   ```

9. **Update CLAUDE-activeContext.md (if exists):**
   ```bash
   if [ -f CLAUDE-activeContext.md ]; then
       # Add PR link to active context
       PR_URL=$(gh pr view --json url -q .url)
       echo "PR created: $PR_URL" >> CLAUDE-activeContext.md
   fi
   ```

#### Generate PR Description Only

To generate a PR description without creating the PR:

1. Follow steps 1-6 above
2. Output the generated description for user review
3. Ask if user wants to create PR with this description

### 2. Merge Coordination

**Purpose:** Safely merge branches with conflict detection and resolution guidance

#### Check Merge Readiness

To check if branch is ready to merge:

```bash
echo "=== MERGE READINESS CHECK ==="
echo ""

# 1. Check current branch
CURRENT_BRANCH=$(git branch --show-current)
BASE_BRANCH=${BASE_BRANCH:-main}

if [ "$CURRENT_BRANCH" = "$BASE_BRANCH" ]; then
    echo "❌ ERROR: Already on base branch $BASE_BRANCH"
    exit 1
fi

echo "✓ Feature branch: $CURRENT_BRANCH"
echo ""

# 2. Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo "❌ Uncommitted changes detected:"
    git status --short
    echo ""
else
    echo "✓ Working tree clean"
    echo ""
fi

# 3. Fetch latest from remote
echo "Fetching latest from remote..."
git fetch origin $BASE_BRANCH
echo ""

# 4. Check if base branch has new commits
BEHIND=$(git rev-list --count HEAD..origin/$BASE_BRANCH)
if [ "$BEHIND" -gt 0 ]; then
    echo "⚠️  Base branch has $BEHIND new commits"
    echo "Consider rebasing: git rebase origin/$BASE_BRANCH"
else
    echo "✓ Up to date with base branch"
fi
echo ""

# 5. Check for conflicts
echo "Checking for potential conflicts..."
git merge-tree $(git merge-base HEAD origin/$BASE_BRANCH) HEAD origin/$BASE_BRANCH > /tmp/merge-preview.txt

if grep -q "changed in both" /tmp/merge-preview.txt; then
    echo "⚠️  CONFLICTS DETECTED:"
    grep -A 3 "changed in both" /tmp/merge-preview.txt
    echo ""
else
    echo "✓ No conflicts detected"
    echo ""
fi

# 6. Run tests (if test command exists)
if [ -f package.json ] && grep -q "\"test\"" package.json; then
    echo "Running tests..."
    npm test
elif [ -f pytest.ini ] || [ -d tests ]; then
    echo "Running tests..."
    pytest
elif [ -f Cargo.toml ]; then
    echo "Running tests..."
    cargo test
else
    echo "ℹ️  No test command found (skipped)"
fi
echo ""

# 7. Check CI status (if using GitHub)
if command -v gh &> /dev/null; then
    echo "Checking CI status..."
    gh pr checks 2>/dev/null || echo "ℹ️  No PR found or CI configured"
fi

echo ""
echo "=== READINESS CHECK COMPLETE ==="
```

#### Merge Branch Safely

To merge a feature branch:

1. **Run merge readiness check** (above)

2. **Ask user for merge strategy:**
   - Regular merge (preserves all commits)
   - Squash merge (single commit)
   - Rebase and merge (linear history)

3. **For regular merge:**
   ```bash
   git checkout $BASE_BRANCH
   git merge --no-ff $FEATURE_BRANCH -m "Merge branch '$FEATURE_BRANCH'"
   ```

4. **For squash merge:**
   ```bash
   git checkout $BASE_BRANCH
   git merge --squash $FEATURE_BRANCH

   # Generate commit message from all commits
   git log $BASE_BRANCH..$FEATURE_BRANCH --format="%s" > /tmp/commit-msg.txt

   git commit -m "$(cat <<'EOF'
   [Squashed commit title]

   Changes included:
   $(cat /tmp/commit-msg.txt)
   EOF
   )"
   ```

5. **For rebase and merge:**
   ```bash
   git checkout $FEATURE_BRANCH
   git rebase $BASE_BRANCH
   git checkout $BASE_BRANCH
   git merge --ff-only $FEATURE_BRANCH
   ```

6. **Push to remote:**
   ```bash
   git push origin $BASE_BRANCH
   ```

7. **Clean up feature branch (optional):**
   ```bash
   # Delete local branch
   git branch -d $FEATURE_BRANCH

   # Delete remote branch
   git push origin --delete $FEATURE_BRANCH
   ```

### 3. Conflict Resolution

**Purpose:** Guide through merge conflict resolution

#### Detect and Analyze Conflicts

When conflicts occur:

1. **Show conflicted files:**
   ```bash
   git status | grep "both modified"
   ```

2. **For each conflicted file, show conflict markers:**
   ```bash
   grep -n "<<<<<<< HEAD" $CONFLICTED_FILE
   ```

3. **Explain the conflict:**
   - `<<<<<<< HEAD` = Your current branch changes
   - `=======` = Separator
   - `>>>>>>> branch-name` = Incoming branch changes

4. **Provide resolution strategies:**
   - Accept current changes (ours): `git checkout --ours $FILE`
   - Accept incoming changes (theirs): `git checkout --theirs $FILE`
   - Manually resolve: Edit file to keep both/choose wisely

5. **After resolution:**
   ```bash
   git add $RESOLVED_FILE
   git status  # Verify all conflicts resolved
   git merge --continue  # or git rebase --continue
   ```

#### Abort Problematic Merge

If merge goes wrong:

```bash
# Abort merge
git merge --abort

# Abort rebase
git rebase --abort

# Return to clean state
git status
```

### 4. Branch Cleanup

**Purpose:** Safely remove old session/feature branches

#### List Branches for Cleanup

To identify branches that can be cleaned up:

```bash
echo "=== BRANCH CLEANUP ANALYSIS ==="
echo ""

# Get current branch and base branch
CURRENT_BRANCH=$(git branch --show-current)
BASE_BRANCH=${BASE_BRANCH:-main}

# List all local branches
echo "Local branches:"
git branch -vv
echo ""

# List merged branches (safe to delete)
echo "Merged branches (safe to delete):"
git branch --merged $BASE_BRANCH | grep -v "^\*" | grep -v "$BASE_BRANCH"
echo ""

# List unmerged branches (check before deleting)
echo "Unmerged branches (verify before deleting):"
git branch --no-merged $BASE_BRANCH | grep -v "^\*"
echo ""

# Show last commit date for each branch
echo "Branch activity (last commit date):"
for branch in $(git branch | sed 's/^\*/ /'); do
    printf "%-30s %s\n" "$branch" "$(git log -1 --format=%cd --date=relative $branch)"
done
```

#### Clean Up Merged Branches

To delete merged branches:

```bash
# Get list of merged branches (excluding current and base)
MERGED_BRANCHES=$(git branch --merged $BASE_BRANCH | grep -v "^\*" | grep -v "$BASE_BRANCH" | grep -v "main" | grep -v "master")

if [ -z "$MERGED_BRANCHES" ]; then
    echo "No merged branches to clean up"
else
    echo "The following merged branches will be deleted:"
    echo "$MERGED_BRANCHES"
    echo ""
    echo "Proceed? (requires user confirmation)"

    # If confirmed:
    echo "$MERGED_BRANCHES" | xargs git branch -d

    echo "✓ Local merged branches deleted"
    echo ""
    echo "Delete remote branches too? (requires user confirmation)"

    # If confirmed:
    echo "$MERGED_BRANCHES" | xargs -I {} git push origin --delete {}
fi
```

#### Clean Up Session Branches

To clean up old session branches specifically:

```bash
# Find session branches (pattern: session/*)
SESSION_BRANCHES=$(git branch | grep "session/" | sed 's/^\*/ /' | xargs)

if [ -z "$SESSION_BRANCHES" ]; then
    echo "No session branches found"
else
    echo "Session branches:"
    for branch in $SESSION_BRANCHES; do
        MERGED=$(git branch --merged $BASE_BRANCH | grep -q "$branch" && echo "✓ merged" || echo "✗ unmerged")
        LAST_COMMIT=$(git log -1 --format="%cd" --date=relative $branch)
        printf "%-40s %-12s %s\n" "$branch" "$MERGED" "$LAST_COMMIT"
    done
    echo ""

    # Ask which to delete
    echo "Delete merged session branches? (y/n)"
    # If yes, delete only merged ones
fi
```

### 5. PR Review Assistance

**Purpose:** Help review PRs and provide feedback

#### Analyze PR Changes

To review a PR:

```bash
# Get PR number from user or current branch
PR_NUMBER=${1:-$(gh pr view --json number -q .number 2>/dev/null)}

if [ -z "$PR_NUMBER" ]; then
    echo "No PR found. Specify PR number or create a PR first."
    exit 1
fi

# Get PR details
gh pr view $PR_NUMBER

# Get diff
gh pr diff $PR_NUMBER

# Get file changes summary
gh pr diff $PR_NUMBER --name-only

# Check CI status
gh pr checks $PR_NUMBER

# Get review comments
gh pr view $PR_NUMBER --comments
```

#### Suggest Reviewers

To suggest reviewers based on changed files:

```bash
# Get files changed in PR
CHANGED_FILES=$(gh pr diff $PR_NUMBER --name-only)

# For each file, find who modified it recently (git blame approach)
echo "Suggested reviewers based on file ownership:"
for file in $CHANGED_FILES; do
    if [ -f "$file" ]; then
        git log --format='%an' -n 5 "$file" | sort | uniq -c | sort -rn | head -1
    fi
done | sort | uniq
```

### 6. Emergency Recovery

**Purpose:** Recover from git mistakes

#### Undo Last Commit (Not Pushed)

To undo the last commit while keeping changes:

```bash
# Soft reset (keep changes staged)
git reset --soft HEAD~1

# Mixed reset (keep changes unstaged)
git reset HEAD~1

# Verify
git status
```

#### Recover Deleted Branch

To recover a recently deleted branch:

```bash
# Find the commit SHA of the deleted branch
git reflog | grep "$BRANCH_NAME"

# Recreate branch from that commit
git branch $BRANCH_NAME $COMMIT_SHA

# Verify
git log $BRANCH_NAME --oneline -n 5
```

#### Undo Merge

To undo a merge that was pushed:

```bash
# Find merge commit
git log --oneline --merges -n 5

# Revert the merge (safe for shared branches)
git revert -m 1 $MERGE_COMMIT_SHA

# Push the revert
git push origin $BASE_BRANCH
```

## Workflow Examples

### Example 1: Create PR from Feature Branch

User request: "Create a PR for my authentication feature"

**Workflow:**
1. Check current branch is `feature/add-auth`
2. Verify working tree is clean
3. Get commits: `git log main..HEAD`
4. Analyze changes: Added `auth.js`, `login.js`, updated `server.js`
5. Generate PR description highlighting JWT implementation, login endpoint, and tests
6. Check remote branch exists, push if needed
7. Create PR: `gh pr create --title "Add JWT authentication" --body "..."`
8. Output PR URL to user

### Example 2: Merge with Conflicts

User request: "Merge my feature branch but there are conflicts"

**Workflow:**
1. Run merge readiness check
2. Detect conflicts in `config.js` and `package.json`
3. Attempt merge: `git merge feature/update-deps`
4. Conflicts occur - pause and analyze
5. Show conflicted sections for each file
6. Guide user: "In package.json, both branches updated dependencies. Accept theirs for packages, ours for custom scripts."
7. After user resolves: `git add config.js package.json`
8. Complete merge: `git merge --continue`
9. Push: `git push origin main`

### Example 3: Clean Up Old Session Branches

User request: "Clean up my session branches from last week"

**Workflow:**
1. List all session branches: `git branch | grep session/`
2. Find: `session/20241020-add-api`, `session/20241021-refactor-db`
3. Check merge status for each
4. First branch merged, second branch not merged
5. Show unmerged commits for second branch
6. Ask user: "Second branch has 3 unmerged commits. Delete anyway?"
7. If yes to merged: `git branch -d session/20241020-add-api`
8. If yes to unmerged: `git branch -D session/20241021-refactor-db` (force delete)
9. Clean remote branches: `git push origin --delete session/20241020-add-api`

### Example 4: Emergency - Undo Accidental Merge

User request: "I accidentally merged the wrong branch into main!"

**Workflow:**
1. Check git log: Find merge commit 5 minutes ago
2. Verify not pushed yet: `git status` shows "ahead of origin/main"
3. Undo merge: `git reset --hard HEAD~1`
4. Verify: `git log` shows merge is gone
5. Guide: "If already pushed, use `git revert -m 1 $SHA` instead"
6. User confirms correct state restored

## Best Practices

1. **Always run readiness check** before merging
2. **Generate PR descriptions from commits** - saves time, ensures completeness
3. **Use semantic branch names** - `feature/`, `fix/`, `session/` prefixes
4. **Clean up merged branches promptly** - reduces clutter
5. **Test before creating PR** - ensures CI will pass
6. **Squash WIP commits** - clean up "wip", "fix typo" commits before merging
7. **Update CLAUDE-activeContext.md** with PR links for tracking
8. **Never force-push to shared branches** without team coordination
9. **Use `--no-ff` for feature merges** - preserves branch history
10. **Rebase feature branches** regularly to avoid large conflicts

## Integration with CLAUDE.md

This skill complements CLAUDE.md git safety protocol:
- **CLAUDE.md**: Prevents issues (branch creation, safety checks before destructive ops)
- **git-pr-helper**: Assists with workflows (PR creation, merge coordination, cleanup)

Both work together:
1. CLAUDE.md guides creating branches before work
2. User does work, commits regularly
3. **git-pr-helper** helps create quality PR when ready
4. **git-pr-helper** assists with merge
5. **git-pr-helper** cleans up branches

## Safety Features

- ✅ Always checks working tree status before operations
- ✅ Detects conflicts before merging
- ✅ Requires user confirmation for destructive operations
- ✅ Preserves unmerged work (warns before deleting)
- ✅ Provides recovery guidance for mistakes
- ✅ Never auto-merges without user review
- ✅ Tests integration with base branch before merge

## Limitations

- Cannot prevent file deletion before commits (use git hooks + CLAUDE.md)
- Cannot automatically invoke at session boundaries (no session concept)
- Cannot enforce branch policies (use git hooks)
- Requires `gh` CLI for GitHub PR operations
- Requires network connectivity for remote operations
- Cannot resolve semantic conflicts (only syntactic)
- PR description generation quality depends on commit message quality

## Quick Reference Commands

```bash
# PR Creation
gh pr create --title "..." --body "..."              # Create PR
gh pr view                                           # View current PR
gh pr checks                                         # Check CI status

# Merge Operations
git merge --no-ff feature/branch                     # Merge preserving history
git merge --squash feature/branch                    # Squash all commits
git rebase main                                      # Rebase onto main

# Branch Management
git branch --merged main                             # List merged branches
git branch -d branch-name                            # Delete local branch
git push origin --delete branch-name                 # Delete remote branch

# Conflict Resolution
git merge --abort                                    # Abort merge
git checkout --ours file.txt                         # Accept our version
git checkout --theirs file.txt                       # Accept their version

# Recovery
git reflog                                           # View ref history
git reset --soft HEAD~1                              # Undo last commit
git revert -m 1 $SHA                                 # Revert merge
```

## Related Skills

- **devcontainer-manager**: Manages infrastructure, can invoke git-pr-helper before risky operations
- **cross-doc-linker**: Checks documentation consistency before PR
- **ai-cross-verifier**: Can validate complex changes before PR submission
