---
name: pr-restructure
description: |
  Clean up messy commit history into atomic commits before merge.
  Use when user wants to restructure PR commit history based on final diff. Triggers include:
  - Korean: "PR 히스토리 정리해줘", "커밋 히스토리 정리", "커밋 깔끔하게"
  - English: "clean up commit history", "restructure commits", "organize commits"
  - Context: User has messy commits (WIP, typo fixes) and wants atomic commit structure
---

# PR Commit History Restructurer

## Overview

Analyze final diff and suggest atomic commit organization for cleaner PR history.

## ⚠️ Critical Execution Rules

**NEVER cd to skill folder.** Always execute scripts from user's current working directory to preserve git repository context.

**Script execution:**
- You know where this skill's SKILL.md is located when you load it
- Marketplace root = parent directory of the skill directory
- Scripts are at: `<marketplace_root>/scripts/`
  - `find_base_branch.py` - Find base candidates
  - `analyze_diff.py` - Analyze final diff
- Compute the path, then execute from user's current working directory

## Important Principles

1. **Only final diff matters**: Intermediate commits are reference only
2. **Safety first**: Always create backup before restructuring
3. **Atomic commits**: One logical change per commit
4. **User controls execution**: Provide guidance, execute only if requested

## Workflow

### Step 1: Find Base Branch

Execute find_base_branch to get candidates:

```bash
# Compute path from skill location, then execute from user's directory
python3 <marketplace_root>/scripts/find_base_branch.py --json
```

Show candidates to user and let them select the correct base.

**Why user selection is needed**:
- Feature-from-feature branches won't appear in candidates (only master/main)
- User knows the actual parent branch
- Commit count helps identify closest branch

**Common scenarios**:
- ✅ Direct from master → Select candidate #1 (lowest commit count)
- ⚠️ Feature from feature → Specify parent feature branch manually
- ⚠️ Forked repo → Check which remote is correct

### Step 2: Analyze Final Diff

⚠️ **IMPORTANT**: Analyze final diff (base..HEAD), NOT individual commits.

```bash
python3 <marketplace_root>/scripts/analyze_diff.py <base> --json
```

Returns:
```json
{
  "base_branch": "main",
  "current_branch": "feature/auth",
  "total_diff": "FINAL diff (source of truth)",
  "stats": {"insertions": 120, "deletions": 45, "files_changed": 8},
  "current_commits": [
    {"hash": "abc123", "message": "Add auth", "files": [...], "stats": {...}},
    {"hash": "def456", "message": "Fix typo", "files": [...], "stats": {...}}
  ],
  "backup_command": "git branch backup/feature-auth-20250118-143022",
  "restore_command": "git reset --hard backup/feature-auth-20250118-143022"
}
```

### Step 3: Analyze Final Diff for Logical Groupings

Read `total_diff` to understand final state:
- Identify logical groups of changes
- Ignore intermediate commits that were reverted/changed
- Focus on what actually changed from base to HEAD

**Analysis approach**:
1. Read the diff to understand what changed
2. Group related changes together:
   - Core feature implementation
   - Supporting utilities
   - Tests
   - Configuration/infrastructure
   - Documentation
3. Each group becomes one atomic commit

### Step 4: Suggest Atomic Commits

Present restructuring proposal:

```
Current: 5 commits with WIP/typo fixes mixed in

abc123: Add auth
def456: Fix typo
ghi789: Add JWT
jkl012: Add tests
mno345: Fix test

Suggested restructuring (3 atomic commits):

1. Add user authentication middleware
   - auth.js: Token validation logic
   - middleware/auth.js: Express middleware
   Files: 2, +45 -0

2. Add JWT token generation utilities
   - utils/jwt.js: Token create/verify functions
   - config/jwt.js: JWT configuration
   Files: 2, +38 -5

3. Add authentication test suite
   - tests/auth.test.js: Middleware tests
   - tests/jwt.test.js: Token tests
   Files: 2, +37 -0
```

### Step 5: Provide Restructuring Strategy

Ask user: "How would you like to proceed?"
- **Option A**: "Guide me through interactive rebase" (show commands, user executes)
- **Option B**: "Execute restructuring for me" (automatic, with backup)
- **Option C**: "Just show me the suggestion" (no execution)

**Option A - Interactive Rebase Guidance**:

```
I'll guide you through interactive rebase:

Step 1 - Start interactive rebase:
git rebase -i main

Step 2 - In the editor, modify the rebase plan:
pick abc123 Add auth
fixup def456 Fix typo       # Squash into previous
reword ghi789 Add JWT       # Rewrite message
pick jkl012 Add tests
fixup mno345 Fix test       # Squash into previous

Step 3 - Save and close editor

Step 4 - For 'reword' commits, update commit messages with suggested text

Step 5 - Verify result:
git log --oneline main..HEAD
```

**Option B - Automatic Execution**:

⚠️ **SAFETY FIRST**:

```
Step 1 - Create backup (REQUIRED):
git branch backup/feature-auth-20250118-143022

Backup created: backup/feature-auth-20250118-143022
This backup will allow restoration if anything goes wrong.

Step 2 - Perform restructuring:
[Execute git commands to create atomic commits]

Step 3 - Verify result:
git log --oneline main..HEAD

Expected commits:
- Add user authentication middleware
- Add JWT token generation utilities
- Add authentication test suite

If problems occur, restore with:
git reset --hard backup/feature-auth-20250118-143022
```

**Option C - Just Suggestion**:

Show the suggested structure and let user handle it however they prefer.

### Step 6: Verification

After restructuring (whether manual or automatic):

```bash
# Show new commit history
git log --oneline <base>..HEAD

# Verify final diff is unchanged
git diff <base>..HEAD
```

**Key verification**:
- Number of commits should match suggestion
- Each commit should be atomic (one logical change)
- Final diff should be identical to before restructuring
- No files lost or changed unintentionally

## Safety Features

1. **Always create backup branch before destructuring**:
   ```bash
   git branch backup/<branch-name>-<timestamp>
   ```

2. **Verify backup exists**:
   ```bash
   git rev-parse --verify backup/<branch-name>-<timestamp>
   ```

3. **Provide restore command**:
   ```bash
   git reset --hard backup/<branch-name>-<timestamp>
   ```

4. **Warn about force push**:
   ```
   ⚠️ After restructuring, you'll need to force push:
   git push --force-with-lease origin <branch-name>

   This rewrites history. Only do this if:
   - No one else is working on this branch
   - Or you've coordinated with your team
   ```

## Common Use Cases

**WIP Commits Cleanup**:
```
Before:
- WIP: starting auth
- WIP: still working
- Fix typo
- Almost done
- Fix bug

After:
- Add user authentication system
- Add authentication tests
```

**Mixed Concerns**:
```
Before:
- Add feature A + refactor B
- Fix tests for both
- Update docs

After:
- Refactor component B
- Add feature A using refactored B
- Add tests for new feature
- Update documentation
```

**Reverted Changes**:
```
Before:
- Add feature X
- Revert feature X (didn't work)
- Add feature Y
- Fix feature Y

After:
- Add feature Y (X was reverted, so not in final diff)
```

## Requirements

- Git repository with commits ahead of base branch
- Clean working directory (no uncommitted changes)
- Base branch identified (use pr-analyze if needed)

## Reference

See `references/commit-guide.md` for atomic commit principles and Chris Beams' seven rules.

## Notes

- This workflow rewrites git history (uses rebase)
- Always requires force push after restructuring
- Should only be done on feature branches, never on shared branches
- Final diff before and after should be identical
- Only commit structure changes, not the actual code
