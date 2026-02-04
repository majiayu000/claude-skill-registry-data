---
name: git-writer
description: Safe workflow for git write operations (git rm). Use for removing files from git.
---

# git-writer Skill

## 🎯 Purpose

This skill provides a safe, documented workflow for git write operations. Currently supports `git rm` for removing files from the repository.

**Use this skill when:**
- User asks to remove files from git ("git rm api/commit.diff")
- User wants to delete tracked files ("remove api/commit.diff from git")
- User needs to unstage and delete files in one operation
- Any git write operation that modifies repository state

**Complements git-reader agent:**
- git-reader: Read-only operations (status, diff, log, show, branch)
- git-writer: Write operations (rm - more to come)

---

## Core Principle: Safe Git Write Operations - NEVER Destroy Data

**🚨 CRITICAL: git-writer ONLY allows operations that NEVER destroy uncommitted data**

**What's allowed:**
- ✅ `git rm` - Removes tracked files (can be restored from git history)
- ✅ `git rm --cached` - Removes from git but keeps in working directory
- ✅ Operations that only affect committed data (restorable)

**What's BANNED:**
- ❌ ANY operation that destroys uncommitted changes
- ❌ `git checkout -f` (destroys unstaged changes)
- ❌ `git reset --hard` (destroys uncommitted work)
- ❌ `git clean -fd` (destroys untracked files permanently)
- ❌ Operations affecting files with uncommitted changes (unless user explicitly confirms)

**The Safety Principle:**
- If data exists ONLY in working directory/staging area → NEVER touch it
- If data is committed to git history → Safe to remove (restorable via `git restore`)
- When in doubt → Ask user to confirm before removing

**ALL git commands go through skills:**
- Read operations → git-reader agent
- Write operations → git-writer skill (this)

This ensures safe, documented, and traceable git operations.

---

## Step 1: Verify Current State and Safety

Before removing files, check what will be affected and verify safety:

```bash
# Check git status to see tracked files and modifications
git status

# If removing specific files, verify they exist
ls -la path/to/file

# Check if file is tracked by git
git ls-files path/to/file

# Check if file has uncommitted changes
git diff path/to/file  # Check unstaged changes
git diff --cached path/to/file  # Check staged changes
```

**Expected output for tracked file:**
```
path/to/file
```

**Expected output for untracked file:**
```
(no output - file not tracked)
```

**🚨 CRITICAL SAFETY CHECK: Uncommitted Changes**

If `git diff` shows output, the file has uncommitted changes:

```bash
# Example: File has uncommitted changes
git diff api/main.py
# Shows: diff --git a/api/main.py b/api/main.py
#        ... changes ...
```

**STOP - Ask user before proceeding:**
```markdown
⚠️ WARNING: api/main.py has uncommitted changes.

Running `git rm` will DESTROY these uncommitted changes permanently.

**Uncommitted changes detected:**
[Show the diff output]

**Options:**
1. Commit changes first: `git commit -am "Save work"`
2. Stash changes: `git stash`
3. Proceed anyway (DESTROYS uncommitted work): `git rm -f api/main.py`

**Which would you like to do?**
```

**DO NOT proceed with `git rm` if uncommitted changes exist unless user explicitly confirms.**

**Decision tree:**
- Untracked → Use `rm` instead (no git needed)
- Tracked + no changes → Proceed to Step 2
- Tracked + uncommitted changes → STOP and ask user

---

## Step 2: Remove File with git rm

Use `git rm` to remove files from both git and working directory:

```bash
# Remove single file
git rm path/to/file

# Remove multiple files
git rm file1 file2 file3

# Remove directory and all contents
git rm -r path/to/directory/

# Remove from git but keep in working directory (cached)
git rm --cached path/to/file
```

**Common use cases:**

**Case 1: Remove .diff files after review**
```bash
git rm api/commit.diff
```

**Case 2: Remove accidentally committed secrets**
```bash
git rm --cached .env
# Then add .env to .gitignore to prevent future commits
```

**Case 3: Remove generated files**
```bash
git rm -r build/
git rm dist/*.js
```

**Expected output:**
```
rm 'api/commit.diff'
```

---

## Step 3: Verify Removal

Check that the file was removed and staged:

```bash
# Check git status
git status
```

**Expected output:**
```
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        deleted:    api/commit.diff
```

**Verification checklist:**
- [ ] File appears in "Changes to be committed" as deleted
- [ ] File removed from working directory (unless --cached used)
- [ ] No error messages during removal

---

## Step 4: Complete the Operation

**The removal is now staged but not committed.**

Explain to the user what happened and what they need to do next:

```markdown
✅ File removed from git and staged for commit.

**What happened:**
- `git rm api/commit.diff` removed the file from git tracking
- The deletion is staged (ready to commit)
- The file is deleted from your working directory

**Next steps (you must run these yourself):**
1. Review the change: `git status`
2. Commit the deletion: `git commit -m "Remove commit.diff file"`
3. Push if needed: `git push`

**To undo (before committing):**
- Restore file: `git restore --staged api/commit.diff && git restore api/commit.diff`
```

---

## Common Violations

### ❌ BANNED: Running git rm without checking status first

**WRONG:**
```bash
git rm some/file  # Without checking if it exists or is tracked
```

**RIGHT:**
```bash
git status  # Check current state
git ls-files some/file  # Verify file is tracked
git rm some/file  # Now safe to remove
```

**Why:** Prevents errors and gives context about what's being removed.

---

### ❌ BANNED: Using rm instead of git rm for tracked files

**WRONG:**
```bash
rm api/commit.diff  # Just deletes file, doesn't stage removal
git add api/commit.diff  # Have to manually stage
```

**RIGHT:**
```bash
git rm api/commit.diff  # Deletes and stages in one command
```

**Why:** `git rm` is cleaner and atomic (delete + stage together).

---

### ❌ BANNED: Committing the removal yourself

**WRONG:**
```bash
git rm api/commit.diff
git commit -m "Remove file"  # ❌ You cannot commit!
```

**RIGHT:**
```bash
git rm api/commit.diff
# Explain to user they need to commit
```

**Why:** Per arsenal restrictions, agents cannot run git commit. User must commit themselves.

---

## git rm Command Reference

### Basic Usage

```bash
# Remove file (delete + stage)
git rm <file>

# Remove multiple files
git rm <file1> <file2> <file3>

# Remove directory recursively
git rm -r <directory>/

# Remove from git but keep in working directory
git rm --cached <file>

# Force removal (if file has uncommitted changes)
git rm -f <file>
```

### Common Patterns

```bash
# Remove all .diff files in a directory
git rm api/*.diff

# Remove specific file types recursively
git rm -r **/*.log

# Remove from git but keep locally (for .env, etc.)
git rm --cached .env
echo ".env" >> .gitignore
```

### Flags Explained

- **No flags**: Remove from git and working directory, stage deletion
- **--cached**: Remove from git but keep file in working directory
- **-f, --force**: Remove even if file has uncommitted changes
- **-r**: Recursive removal (for directories)
- **-n, --dry-run**: Show what would be removed without doing it

---

## When to Use git rm vs Regular rm

**Use `git rm` when:**
- ✅ File is tracked by git
- ✅ You want to remove from repository
- ✅ You want removal staged for commit

**Use regular `rm` when:**
- ✅ File is untracked (not in git)
- ✅ File is already in .gitignore
- ✅ You just want to delete locally without git involvement

**Check if file is tracked:**
```bash
git ls-files path/to/file
# Output = tracked
# No output = untracked
```

---

## Troubleshooting

### Problem: "fatal: pathspec 'X' did not match any files"

**Cause:** File doesn't exist or isn't tracked by git

**Solution:**
```bash
# Check if file exists
ls -la path/to/file

# Check if git knows about it
git ls-files path/to/file

# If untracked, use rm instead
rm path/to/file
```

---

### Problem: "error: 'X' has local modifications"

**Cause:** File has uncommitted changes and git won't remove by default

**Solution:**
```bash
# Option 1: Force removal (loses changes)
git rm -f path/to/file

# Option 2: Commit changes first, then remove
git add path/to/file
# (user commits)
git rm path/to/file

# Option 3: Stash changes, then remove
git stash
git rm path/to/file
```

---

### Problem: Removed wrong file

**Cause:** Typo or wrong path

**Solution (before committing):**
```bash
# Restore from staging and working directory
git restore --staged path/to/file
git restore path/to/file

# File is back!
```

**Solution (after committing):**
```bash
# User must run:
git revert <commit-hash>
# Or
git reset --soft HEAD~1  # Undo commit, keep changes
git restore --staged path/to/file
git restore path/to/file
```

---

## Success Criteria

You've successfully used git-writer when:

- [ ] Checked git status before removal
- [ ] Verified file is tracked (or chose rm for untracked)
- [ ] Ran `git rm` with appropriate flags
- [ ] Verified removal was staged with `git status`
- [ ] Explained to user what happened and next steps
- [ ] Did NOT run `git commit` yourself (user must do it)

---

## Examples

### Example 1: Remove a single .diff file

```bash
# Step 1: Check status
git status
# Shows: api/commit.diff (tracked, unmodified)

# Step 2: Remove file
git rm api/commit.diff
# Output: rm 'api/commit.diff'

# Step 3: Verify
git status
# Shows: deleted: api/commit.diff (staged)

# Step 4: Explain to user
# ✅ Removal staged. User should commit with: git commit -m "Remove commit.diff"
```

---

### Example 2: Remove from git but keep locally

```bash
# Step 1: Check status
git status
# Shows: .env (tracked)

# Step 2: Remove from git only
git rm --cached .env
# Output: rm '.env'

# Step 3: Prevent future commits
echo ".env" >> .gitignore

# Step 4: Verify
git status
# Shows:
# - deleted: .env (staged)
# - .gitignore (modified)
# File still exists in working directory

# Step 5: Explain to user
# ✅ .env removed from git but kept locally. Add .gitignore to prevent future commits.
```

---

### Example 3: Remove directory

```bash
# Step 1: Check what's in directory
git ls-files build/
# Shows files tracked in build/

# Step 2: Remove directory
git rm -r build/
# Output: rm 'build/file1.js'... (all files)

# Step 3: Verify
git status
# Shows: deleted: build/ (all files staged)

# Step 4: Explain to user
# ✅ Entire build/ directory removed and staged for commit.
```

---

## Related Skills

- **git-reader agent**: Read-only git operations (status, diff, log)
- **skill-writer**: How to create/edit skills like this one

---

## Future Enhancements

This skill currently supports only `git rm`. Future versions may add:

- `git add` - Stage files for commit
- `git restore` - Restore files from git
- `git mv` - Rename/move files in git
- `git reset` - Unstage files

For now, these operations should be explained to the user to run manually.

---

## Restrictions Reminder

**Per arsenal CLAUDE.md, you CANNOT run:**
- ❌ `git commit` (user must commit)
- ❌ `git push` (user must push)
- ❌ `git reset --hard` (destructive)
- ❌ `git rebase` (complex, user must run)
- ❌ Any destructive git operations

**You CAN run (via this skill):**
- ✅ `git rm` (removes files, user commits)
- ✅ `git status` (read-only, also via git-reader)

