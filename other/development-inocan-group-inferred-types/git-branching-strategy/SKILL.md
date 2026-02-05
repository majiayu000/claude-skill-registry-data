---
name: git-branching-strategy
description: This skill should be used when starting new feature work, mid-feature when wanting to add unrelated changes, when a branch has grown beyond 20 commits, or when unsure whether to create a new branch. Covers one-feature-one-branch rule, branch size targets, and when to split branches.
---

# Git Branching Strategy

Prevent monster branches by following disciplined branching and merge practices.

## When to Use This Skill

Invoke this skill when:

### ✅ Starting New Work
- About to implement a new feature
- Planning to fix a bug
- Starting refactoring work
- Adding documentation

### ⚠️ Mid-Feature Warning Signs
- Thinking "while I'm here, I'll also..."
- Wanting to add unrelated functionality
- Branch has grown beyond 20 commits
- Multiple unrelated files changed
- Changes would be difficult to understand

### 🎯 Decision Points
- Unsure whether to create new branch or continue current
- Wondering if branch is getting too large
- Considering adding "just one more thing"
- Ready to merge but branch feels messy

---

## ⚠️ Pre-Implementation Checklist

**BEFORE writing ANY code, answer these questions:**

### 1. Is this non-trivial work?

**Non-trivial = ANY of these:**
- ✅ Changes **>2 files**
- ✅ Refactoring existing code
- ✅ Adding new features/functionality
- ✅ Implementing planned tasks
- ✅ Bug fixes requiring changes to multiple components

**Trivial = ALL of these:**
- ❌ Fixing typo in single file
- ❌ Updating documentation only (markdown, comments)
- ❌ One-line fix in single file

### 2. If Non-Trivial → CREATE FEATURE BRANCH

```bash
# Ensure main branch is up to date
git checkout main
git pull origin main

# Create feature branch (choose appropriate prefix)
git checkout -b feature/descriptive-name    # For new features
git checkout -b refactor/descriptive-name   # For refactoring
git checkout -b fix/descriptive-name        # For bug fixes
```

**Examples:**
- `feature/user-authentication` - New auth implementation
- `refactor/error-handling` - Standardize error handling
- `fix/login-redirect` - Fix login redirect bug

### 3. Golden Rule

**When in doubt, use a feature branch.**

Feature branches provide:
- 📝 Documentation of what changed and why
- 📊 Clear history of feature development
- 🔄 Easy to revert if needed
- 🧪 Isolated testing before merge

---

## The Problem: Monster Branches

### What Happens

**Timeline:**
- Started as "add feature X"
- Grew to include features Y, Z, refactoring, and bug fixes
- **100+ commits**, multiple intertwined features
- Difficult to review, hard to merge, risky to revert

**Symptoms:**
- ❌ Multiple distinct features mixed together
- ❌ Hard to describe what the branch does in one sentence
- ❌ Changes span unrelated systems
- ❌ Commit history is difficult to follow
- ❌ Rolling back one feature means losing others

**Consequences:**
- Long-lived branch diverges from main
- Merge conflicts accumulate
- Testing becomes all-or-nothing
- Can't ship features incrementally
- Hard to isolate bugs introduced

## Solution: Small, Focused Branches

### The Golden Rule

**One feature, one branch, one merge.**

If you can't describe the branch in a single sentence without using "and", it's too big.

### Good Examples

✅ **Good:** `feat/user-auth` - "Add basic user authentication"
✅ **Good:** `feat/smart-fields` - "Implement smart field system"
✅ **Good:** `fix/race-condition` - "Fix optimistic update race condition"
✅ **Good:** `refactor/scss-modules` - "Convert SCSS to module system"
✅ **Good:** `docs/contributing` - "Add contributing guidelines"

### Bad Examples

❌ **Bad:** `feat/improvements` - Too vague, likely includes unrelated changes
❌ **Bad:** `fix/various-bugs` - Multiple unrelated fixes should be separate branches
❌ **Bad:** `wip/stuff` - Not descriptive, suggests unfocused work

## Branch Size Guidelines

### Target Size

**Ideal:** 5-15 commits, 1-5 files changed significantly
**Acceptable:** Up to 30 commits, up to 10 files
**Too Large:** 50+ commits, 20+ files

**Exception:** Large refactors that are purely mechanical

### Commit Count Checkpoints

```
5 commits → Normal feature pace
10 commits → Check: Am I still focused on one feature?
20 commits → WARNING: Consider splitting or wrapping up
30 commits → CRITICAL: Finish and merge, or split into multiple branches
50+ commits → MONSTER: This should have been 3-5 separate branches
```

### When Branch Size is Justified

✅ **Acceptable large branches:**
- Pure refactoring (converting styles, modularization)
- Data migrations (changing structure across many files)
- Framework version upgrades (mechanical API changes)
- Initial feature implementation with tests and docs

❌ **Unacceptable large branches:**
- Multiple unrelated features
- Feature + "while I'm here" improvements
- Feature + unrelated bug fixes
- Feature + refactoring that isn't required for feature

## Decision Tree: New Branch or Continue?

### Question 1: Is this change related to current branch?

```
New change → Related to current feature?
  ↓ YES (same system, same goal)
  → Continue current branch

  ↓ NO (different system, different goal)
  → Question 2
```

### Question 2: Is current branch ready to merge?

```
Current branch → Ready to merge?
  ↓ YES (feature complete, tests pass)
  → Merge current, then new branch for new work

  ↓ NO (feature incomplete)
  → Question 3
```

### Question 3: Is new work required for current feature?

```
New work → Required for current feature to work?
  ↓ YES (dependency)
  → Continue current branch

  ↓ NO (nice-to-have, improvement, unrelated)
  → Stash current, new branch, finish new, resume current
```

## Branch Naming Conventions

### Format

```
<type>/<short-description>
```

### Types

- **feat/** - New feature or enhancement
- **fix/** - Bug fix
- **refactor/** - Code restructuring without behavior change
- **docs/** - Documentation only
- **test/** - Adding or fixing tests
- **chore/** - Build, tooling, dependencies

### Examples

```
feat/user-auth
feat/smart-fields
feat/dashboard
fix/login-redirect
fix/memory-leak
refactor/scss-modules
refactor/modularization
docs/contributing
docs/api-guide
chore/update-deps
```

### Avoid

❌ `feature/` - Use `feat/` (shorter)
❌ `bugfix/` - Use `fix/` (shorter)
❌ `wip/` - Work in progress is implied, use descriptive name
❌ `my-branch` - Not descriptive
❌ `feat/add-feature` - Redundant "add"

## Branch Lifecycle

### 1. Plan and Scope

**Before creating branch:**
- [ ] Can I describe this in one sentence?
- [ ] Is this the smallest useful increment?
- [ ] Does this depend on other incomplete work?
- [ ] Will this take more than 30 commits?

**If >30 commits expected:** Break into smaller features first.

### 2. Create Branch

```bash
# From main (or integration branch)
git checkout main
git pull origin main

# Create feature branch
git checkout -b feat/descriptive-name
```

### 3. Work on Feature

**Commit discipline:**
- Small, focused commits
- Clear commit messages
- Commit related changes together
- Don't mix formatting with logic changes

**Check progress regularly:**
```bash
# How many commits?
git log main..HEAD --oneline | wc -l

# How many files changed?
git diff main --stat

# Am I still focused?
git log --oneline -10  # Review recent commits
```

### 4. Recognize When to Split

**Warning signs:**
- Commit messages use "and" frequently
- Multiple unrelated `// TODO` comments
- You've forgotten what early commits did
- Summary of changes needs 3+ bullet points for unrelated changes

**How to split:**

```bash
# Option A: Finish current, branch for next
git commit -m "Complete X feature"
# Merge feat/x
git checkout -b feat/y  # Start next feature

# Option B: Stash incomplete, branch for urgent work
git stash
git checkout -b fix/urgent-bug
# Fix and merge
git checkout feat/original
git stash pop
```

### 5. Prepare for Merge

**Before merging:**
```bash
# Rebase on latest main
git fetch origin
git rebase origin/main

# Review all changes
git diff origin/main

# Check commit history is clean
git log origin/main..HEAD --oneline

# Run tests if applicable
npm test  # or your test command
```

### 6. Merge to Main

```bash
# Switch to main and merge
git checkout main
git pull origin main
git merge --no-ff feat/descriptive-name

# Push to remote
git push origin main

# Delete local branch
git branch -d feat/descriptive-name
```

**Note:** `--no-ff` creates a merge commit even for fast-forward merges, preserving branch history.

## Commit Message Conventions

### Format

```
<type>: <short description>

<optional body>

<optional footer>
```

### Types

Same as branch types:
- **feat:** - New feature
- **fix:** - Bug fix
- **refactor:** - Code restructuring
- **docs:** - Documentation
- **test:** - Tests
- **chore:** - Build/tooling

### Guidelines

**Good commit messages:**
```
feat: Add smart field system with lookups

Implements interactive fields that open selection dialogs
filtered by context. Includes helper and click handler integration.

Closes #42
```

**Bad commit messages:**
```
❌ "Updates"
❌ "Fix stuff"
❌ "WIP"
❌ "More changes"
❌ "Final commit (hopefully)"
```

### Commit Message Best Practices

- **Present tense:** "Add feature" not "Added feature"
- **Imperative mood:** "Fix bug" not "Fixes bug"
- **Capitalize first word:** "Add feature" not "add feature"
- **No period at end:** "Add feature" not "Add feature."
- **Body explains why, not what:** Code shows what, message explains why

## When to Split an Existing Branch

### Recognize the Need

**You should split if:**
- Branch has 40+ commits and isn't done
- You can't summarize the changes coherently
- Rolling back would lose multiple independent features
- Commit history mixes unrelated changes

### How to Split

**Strategy A: Extract Completed Features**

```bash
# Current branch: feat/massive (50 commits)
# Goal: Extract first feature into separate branch

# 1. Create new branch from main
git checkout main
git checkout -b feat/extracted-feature

# 2. Cherry-pick relevant commits
git log feat/massive --oneline  # Find commit SHAs
git cherry-pick abc123 def456 ghi789

# 3. Merge the extracted feature
git checkout main
git merge --no-ff feat/extracted-feature
git push origin main
git branch -d feat/extracted-feature

# 4. Rebase massive branch to remove duplicates
git checkout feat/massive
git rebase main
```

**Strategy B: Start Fresh, Reference Old**

```bash
# Current branch: feat/massive (too messy to salvage)

# 1. Create new branch from main
git checkout main
git checkout -b feat/feature-1-clean

# 2. Manually apply changes from massive branch
# (Copy files, make clean commits)

# 3. Repeat for each feature
git checkout main
git checkout -b feat/feature-2-clean

# 4. Abandon feat/massive after all features extracted
git branch -D feat/massive
```

## Quick Checklist

### Before Starting Work

- [ ] One sentence description of what I'm building
- [ ] Checked if this should be separate from current branch
- [ ] Created appropriately named branch from main
- [ ] Estimated this will take <30 commits

### During Work

- [ ] Commit messages are clear and focused
- [ ] Not mixing unrelated changes in same commit
- [ ] Checking commit count every 5-10 commits
- [ ] Resisting "while I'm here" temptations

### Before Merging

- [ ] Branch has <30 commits (or justifiable if larger)
- [ ] All commits are related to the same feature
- [ ] Rebased on latest main
- [ ] Can describe changes in 1-3 sentences
- [ ] Commit history is clean and logical
- [ ] Tests pass (if applicable)

### Danger Signs (Stop and Split)

- [ ] ⚠️ More than 30 commits
- [ ] ⚠️ Changed more than 15 unrelated files
- [ ] ⚠️ Commit messages have "also", "and", "while here"
- [ ] ⚠️ Can't remember what early commits did
- [ ] ⚠️ Summary needs multiple unrelated bullet points

## Common Scenarios

### "I'm halfway through feature X, noticed bug Y"

**If bug blocks feature X:**
→ Fix in current branch

**If bug is unrelated:**
→ Stash current work, create `fix/bug-y`, merge it, resume feature X

### "I want to add feature B while working on feature A"

**If B is required for A:**
→ Continue current branch

**If B is independent:**
→ Finish A first, then branch for B

**If B is urgent and A is incomplete:**
→ Stash A, branch for B, merge B, resume A

### "My branch has 40 commits, should I split?"

**Yes.** Options:
1. Extract completed portions into separate branches (cherry-pick)
2. Finish current branch as-is, vow to split next time
3. Start fresh with clean branches for each feature

### "I made formatting changes along with feature changes"

**Separate them:**
```bash
# Approach 1: Amend last commit to remove formatting
git reset HEAD~1
git add <feature files only>
git commit -m "feat: add feature"
git add <formatting files>
git commit -m "chore: format code"

# Approach 2: Split into two branches
# - Branch 1: Formatting only (refactor/format-cleanup) - merge first
# - Branch 2: Feature only (feat/my-feature) - merge after
```

---

**Remember:** When in doubt, split it out. Smaller branches are easier to understand, safer to merge, and faster to ship.

---

**Last Updated**: 2026-01-05
