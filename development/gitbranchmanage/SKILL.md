---
name: git.branch.manage
description: Create, checkout, rebase, and manage git branches following Carbon ACX naming conventions and workflows.
---

# git.branch.manage

## Purpose

This skill automates git branch management for Carbon ACX by:
- Creating branches with proper naming conventions
- Checking out existing branches safely
- Managing branch state (tracking, upstream)
- Performing rebases and merges
- Detecting and reporting merge conflicts
- Cleaning up stale branches
- Ensuring proper branch hygiene

## When to Use

**Trigger Patterns:**
- "Create a branch for..."
- "Switch to branch..."
- "Rebase this branch"
- "Update my branch from main"
- "Delete old branches"
- Before starting new work on a feature/fix

**Do NOT Use When:**
- Making commits (use `git.commit.smart`)
- Creating PRs (use `git.pr.create`)
- Resolving complex merge conflicts (requires human judgment)

## Allowed Tools

- `bash` - Git commands
- `grep` - Search branch lists, commit messages

**Access Level:** 2 (Git operations - can create/delete branches)

**Tool Rationale:**
- `bash`: Required for all git branch operations
- `grep`: Filter branch lists and search patterns

**Explicitly Denied:**
- No force deleting branches without confirmation
- No rebasing published branches without warning
- No modifying main/master branches

## Expected I/O

**Input:**
- Type: Branch management request
- Context: Current working state, branch name/description
- Optional: Base branch (defaults to main/master)

**Example:**
```
"Create a feature branch for dark mode"
"Switch to the UX improvements branch"
"Rebase my branch on main"
"Delete merged branches"
```

**Output:**
- Type: Branch operation completed
- Format: Confirmation message with branch state
- Includes:
  - Branch name used
  - Operation performed (create, checkout, rebase, delete)
  - Current HEAD position
  - Any conflicts or warnings

**Validation:**
- Branch name follows conventions
- No uncommitted changes (or properly handled)
- Operations succeed without data loss
- User informed of branch state changes

## Dependencies

**Required:**
- Git repository
- Clean working directory (or stashing strategy)

**Optional:**
- Remote repository configured for push/pull operations

## Workflow

### Branch Creation

#### Step 1: Determine Branch Name

**Naming Convention:**
```
<type>/<description>
```

**Types:**
- `feat/` or `feature/` - New features
- `fix/` or `bugfix/` - Bug fixes
- `chore/` - Maintenance, tooling, dependencies
- `docs/` - Documentation only
- `refactor/` - Code restructuring
- `test/` - Test additions/updates
- `perf/` - Performance improvements

**Description:**
- Lowercase with hyphens (kebab-case)
- Concise but descriptive (3-5 words)
- No special characters except hyphens

**Examples:**
- `feat/dark-mode-toggle`
- `fix/aviation-calculation-error`
- `chore/update-react-dependencies`
- `docs/update-api-documentation`
- `refactor/component-structure`

**Alternative naming (also accepted):**
- `feature/description`
- `bugfix/description`
- User-specified names (if they follow convention)

#### Step 2: Check for Existing Branch

```bash
git branch --list "feat/dark-mode-toggle"
git branch -r --list "*/feat/dark-mode-toggle"
```

**If exists:** Ask user if they want to:
- Checkout existing branch
- Create with different name
- Delete and recreate (dangerous!)

#### Step 3: Determine Base Branch

```bash
# Check if main exists
git rev-parse --verify main 2>/dev/null

# Otherwise check for master
git rev-parse --verify master 2>/dev/null
```

**Default:** `main` (or `master` if main doesn't exist)
**User can override:** "Create branch from develop"

#### Step 4: Fetch Latest

```bash
git fetch origin
```

**Ensures base branch is up-to-date**

#### Step 5: Create and Checkout

```bash
git checkout -b feat/dark-mode-toggle origin/main
```

**Alternative (two-step):**
```bash
git branch feat/dark-mode-toggle origin/main
git checkout feat/dark-mode-toggle
```

#### Step 6: Confirm

```bash
git status
git log -1 --oneline
```

**Report to user:**
```
✅ Branch created: feat/dark-mode-toggle
Base: origin/main (abc1234)
Current HEAD: abc1234 chore: prepare release v1.3.0
Status: No commits yet, ready for work
```

### Branch Checkout

#### Step 1: Check Working Directory

```bash
git status --porcelain
```

**If uncommitted changes:**
- Offer to stash: `git stash push -m "WIP: auto-stashed by git.branch.manage"`
- Or require commit first

#### Step 2: Find Branch

**Local branches:**
```bash
git branch --list "*pattern*"
```

**Remote branches:**
```bash
git branch -r --list "origin/*pattern*"
```

**If multiple matches:** Present list to user for selection

**If no matches:** Suggest creating new branch

#### Step 3: Checkout

**Local branch:**
```bash
git checkout feat/dark-mode-toggle
```

**Remote branch (first checkout):**
```bash
git checkout -b feat/dark-mode-toggle origin/feat/dark-mode-toggle
```

#### Step 4: Confirm

```bash
git status
```

**Report:**
```
✅ Switched to branch: feat/dark-mode-toggle
Tracking: origin/feat/dark-mode-toggle
Status: Up to date with remote
```

### Branch Rebase

#### Step 1: Verify Current Branch

```bash
git rev-parse --abbrev-ref HEAD
```

**Safety check:** Never rebase main/master directly

#### Step 2: Check Uncommitted Changes

```bash
git status --porcelain
```

**If uncommitted:** Require commit or stash first

#### Step 3: Fetch Latest

```bash
git fetch origin
```

#### Step 4: Rebase

```bash
git rebase origin/main
```

**If conflicts:**
```
⚠️ Rebase conflict detected

Conflicting files:
- apps/carbon-acx-web/src/components/Dashboard.tsx
- package.json

Options:
1. Resolve conflicts manually
2. Abort rebase: git rebase --abort

To continue after resolving:
- git add <resolved-files>
- git rebase --continue
```

**Do NOT auto-resolve conflicts** - require human judgment

#### Step 5: If Successful

```bash
git log --oneline -5
```

**Report:**
```
✅ Rebase successful

Your branch has been rebased on origin/main
Previous HEAD: abc1234
New HEAD: xyz9876

Commits on this branch: 3
- feat(web): add dark mode state management
- feat(web): create theme toggle component
- test(web): add theme switching tests

⚠️ Note: Branch history has been rewritten
If already pushed, you'll need to force-push: git push --force-with-lease
```

### Branch Cleanup

#### Step 1: List Merged Branches

```bash
# Local branches merged to main
git branch --merged main | grep -v "main\|master\|\*"

# Remote merged branches
git branch -r --merged main | grep -v "main\|master"
```

#### Step 2: Present List

**Show user:**
```
Merged branches (safe to delete):
Local:
- feat/dark-mode-toggle
- fix/aviation-calculation

Remote:
- origin/chore/update-dependencies

Delete these branches? (yes/no)
```

#### Step 3: Delete (if approved)

**Local:**
```bash
git branch -d feat/dark-mode-toggle
```

**Remote:**
```bash
git push origin --delete feat/dark-mode-toggle
```

**Report:**
```
✅ Deleted 2 local branches
✅ Deleted 1 remote branch

Remaining branches: 5
```

## Examples

### Example 1: Create Feature Branch

**User:** "Create a branch for dark mode feature"

**Claude Process:**
1. Parse intent: Feature branch
2. Generate name: `feat/dark-mode-toggle`
3. Check if exists: No
4. Fetch origin
5. Create from `origin/main`:
   ```bash
   git fetch origin
   git checkout -b feat/dark-mode-toggle origin/main
   ```
6. Report:
   ```
   ✅ Created branch: feat/dark-mode-toggle
   Base: origin/main (abc1234)
   Ready to start work on dark mode feature
   ```

### Example 2: Switch to Existing Branch

**User:** "Switch to the UX improvements branch"

**Claude Process:**
1. Search branches: `git branch --list "*ux*"`
2. Find match: `feat/ux-improvements`
3. Check working directory: Clean ✅
4. Checkout:
   ```bash
   git checkout feat/ux-improvements
   ```
5. Report:
   ```
   ✅ Switched to: feat/ux-improvements
   Last commit: d4e5f6g refactor(web): improve dashboard layout
   Status: 2 commits ahead of origin/main
   ```

### Example 3: Rebase on Main

**User:** "Rebase my branch on main"

**Claude Process:**
1. Current branch: `feat/dark-mode-toggle`
2. Check uncommitted: Clean ✅
3. Fetch: `git fetch origin`
4. Rebase:
   ```bash
   git rebase origin/main
   ```
5. **Success:**
   ```
   ✅ Rebase successful
   Your branch is now up-to-date with origin/main
   3 commits rebased
   ```
6. Warn about force-push if already pushed

### Example 4: Handle Rebase Conflict

**User:** "Update my branch from main"

**Claude Process:**
1. Current branch: `feat/emission-chart`
2. Rebase: `git rebase origin/main`
3. **Conflict detected:**
   ```
   ⚠️ Rebase stopped due to conflicts

   Conflicting files:
   - apps/carbon-acx-web/src/components/Chart.tsx
     (both modified)

   Conflict type: Content conflict
   Your changes: Added EmissionChart component
   Main changes: Refactored base Chart component

   Resolution needed:
   1. Open Chart.tsx and resolve conflict markers
   2. Keep both changes if compatible
   3. After fixing:
      git add Chart.tsx
      git rebase --continue

   To abort: git rebase --abort
   ```
4. Wait for user to resolve
5. Do NOT auto-resolve

### Example 5: Clean Up Merged Branches

**User:** "Delete old branches"

**Claude Process:**
1. List merged:
   ```bash
   git branch --merged main
   ```
2. Found: `feat/dark-mode-toggle`, `fix/typo-readme`
3. Present list:
   ```
   Merged branches (safe to delete):
   - feat/dark-mode-toggle (merged in PR #42)
   - fix/typo-readme (merged in PR #38)

   Delete these? (yes/no)
   ```
4. User confirms: yes
5. Delete:
   ```bash
   git branch -d feat/dark-mode-toggle fix/typo-readme
   ```
6. Report:
   ```
   ✅ Deleted 2 local branches
   Remaining: 3 active branches
   ```

### Example 6: Create Branch from Specific Base

**User:** "Create a hotfix branch from v1.2.3 tag"

**Claude Process:**
1. Parse: Hotfix, base is tag v1.2.3
2. Verify tag exists: `git rev-parse v1.2.3`
3. Generate name: `hotfix/urgent-security-fix` (ask user for description)
4. Create:
   ```bash
   git checkout -b hotfix/urgent-security-fix v1.2.3
   ```
5. Report:
   ```
   ✅ Created branch: hotfix/urgent-security-fix
   Base: v1.2.3 (tag)
   ⚠️ This branch is behind main - use for hotfix only
   ```

## Limitations

**Scope Limitations:**
- Cannot auto-resolve merge conflicts (requires human judgment)
- Cannot rebase published/shared branches without warning
- Cannot delete branches with unmerged changes (safety)
- Cannot modify protected branches (main/master)

**Known Edge Cases:**
- Detached HEAD state → Warn user, suggest creating branch from current state
- Diverged branches (force-push needed) → Warn about risks
- Stale remote branches → Suggest pruning with `git remote prune`
- Branch name conflicts → Suggest alternative names

**Performance Constraints:**
- Rebasing many commits (100+) may take time
- Fetching from slow remotes may delay operations
- Large conflicts difficult to present in text format

**Security Boundaries:**
- Does not force-delete branches without confirmation
- Does not auto-resolve conflicts (data loss risk)
- Does not push to protected branches
- Respects repository permissions

## Validation Criteria

**Success Metrics:**
- ✅ Branch names follow conventions
- ✅ Operations complete without data loss
- ✅ User informed of branch state changes
- ✅ Conflicts detected and reported (not auto-resolved)
- ✅ Working directory state preserved (stash if needed)
- ✅ Remote tracking configured when appropriate

**Failure Modes:**
- ❌ Uncommitted changes → Suggest commit or stash
- ❌ Branch name invalid → Suggest corrected name
- ❌ Merge conflict → Report, provide resolution steps
- ❌ Remote unreachable → Suggest checking network
- ❌ Branch doesn't exist → Suggest creating or list similar names

**Recovery:**
- If conflict during rebase: Provide clear resolution steps
- If branch exists: Offer alternatives (checkout, rename, delete)
- If uncommitted changes: Offer stash or commit options
- If operation fails: Provide git status and suggest next action

## Related Skills

**Composes With:**
- `git.commit.smart` - Commit work before switching branches
- `git.pr.create` - Create PR after branch work complete
- `git.release.prep` - Create release branch

**Dependencies:**
- None - foundational skill

**Alternative Skills:**
- For commits: `git.commit.smart`
- For PRs: `git.pr.create`

## Maintenance

**Owner:** Workspace Team (shared skill)
**Review Cycle:** Quarterly
**Last Updated:** 2025-10-24
**Version:** 1.0.0

**Maintenance Notes:**
- Update branch naming conventions if Carbon ACX changes standards
- Review rebase strategies as git workflows evolve
- Adjust conflict detection logic for better reporting
- Keep stash/unstash behavior synchronized with user preferences
