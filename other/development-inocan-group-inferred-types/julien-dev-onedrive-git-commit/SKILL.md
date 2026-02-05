---
name: julien-dev-onedrive-git-commit
description: Create git commits in OneDrive-synced repositories by bypassing mmap errors using git plumbing commands. Use when git commit fails with "fatal mmap failed Invalid argument" error in OneDrive folders.
---

# OneDrive Git Commit Skill

## Problem

Git repositories stored in OneDrive folders often fail with `fatal: mmap failed: Invalid argument` when executing porcelain commands like `git commit`, `git status`, or `git push`.

This occurs because OneDrive's file system layer interferes with git's memory-mapped file operations.

## Solution

Use **git plumbing commands** to bypass the mmap issue and create commits manually.

## When to Use This Skill

Invoke this skill when:
- User requests git commit in a repo under OneDrive path (`/c/Users/*/OneDrive/`)
- Git command returns `fatal: mmap failed: Invalid argument`
- Standard `git commit` fails repeatedly

## Step-by-Step Commit Process

### 1. Configure Git Memory Settings

Reduce memory usage to minimize mmap calls:

```bash
cd "$REPO_PATH"
git config core.packedGitWindowSize 1m
git config core.packedGitLimit 1m
git config pack.windowMemory 1m
git config pack.packSizeLimit 1m
```

### 2. Create Git Objects for Modified Files

For each file to commit, create a blob object:

```bash
git hash-object -w path/to/file1
git hash-object -w path/to/file2
# Save the SHA hashes returned
```

### 3. Update Git Index

Register each file in the index with its SHA:

```bash
git update-index --add --cacheinfo 100644,<SHA>,path/to/file1
git update-index --add --cacheinfo 100644,<SHA>,path/to/file2
```

**Mode codes:**
- `100644` = regular file
- `100755` = executable file
- `120000` = symbolic link

### 4. Create Tree Object

Generate tree from current index:

```bash
TREE_SHA=$(git write-tree)
echo $TREE_SHA
```

### 5. Get Parent Commit

Retrieve current HEAD SHA:

```bash
PARENT_SHA=$(git rev-parse HEAD)
echo $PARENT_SHA
```

### 6. Create Commit Object

Build commit with message and metadata:

```bash
COMMIT_MESSAGE="feat: Your commit message here

Detailed description if needed

Co-Authored-By: Claude <noreply@anthropic.com>"

COMMIT_SHA=$(echo "$COMMIT_MESSAGE" | git commit-tree $TREE_SHA -p $PARENT_SHA)
echo $COMMIT_SHA
```

### 7. Update Branch Reference

Move HEAD to new commit:

```bash
git update-ref refs/heads/master $COMMIT_SHA
```

Replace `master` with current branch name if different.

### 8. Verify Commit

Check commit was created:

```bash
git log -1 --oneline
```

## Push to Remote

If remote is configured:

```bash
git remote -v
git push origin master
```

**Note:** Push may also fail with mmap error. If so, user must push via Git GUI or GitHub Desktop.

## Alternative: Git GUI

If plumbing commands fail, recommend:
- **Git GUI** (installed with Git for Windows)
- **GitHub Desktop**
- **GitKraken**

These tools don't use mmap and work reliably on OneDrive.

## Common Errors

### "fatal: not a valid object name"
- Check SHA hashes are correct
- Ensure files were successfully written with `hash-object`

### "fatal: refs/heads/master: not a valid SHA1"
- Use `git rev-parse HEAD` to get valid parent commit
- If repo is new, omit `-p $PARENT_SHA` from commit-tree

### "error: unable to write sha1 file"
- OneDrive is syncing - wait for sync to complete
- Temporarily pause OneDrive sync during git operations

## Notes

- This workflow bypasses **all** git porcelain commands
- Works when standard git fails on OneDrive
- Commits are identical to normal git commits
- No data corruption or integrity issues
- Recommended only when necessary (mmap errors)

## Example Complete Workflow

```bash
cd "$REPO_PATH"

# Configure memory
git config core.packedGitWindowSize 1m

# Create objects
SHA1=$(git hash-object -w file1.txt)
SHA2=$(git hash-object -w file2.txt)

# Update index
git update-index --add --cacheinfo 100644,$SHA1,file1.txt
git update-index --add --cacheinfo 100644,$SHA2,file2.txt

# Create tree
TREE=$(git write-tree)

# Get parent
PARENT=$(git rev-parse HEAD)

# Create commit
COMMIT=$(echo "feat: Update files" | git commit-tree $TREE -p $PARENT)

# Update branch
git update-ref refs/heads/master $COMMIT

# Verify
git log -1 --oneline
```

## Success Criteria

Commit is successful when:
- `git log -1` shows new commit
- Commit SHA is different from parent
- Files are included in commit tree
- No mmap errors occur

---

**Last Updated:** November 2025
**Tested On:** Windows 11, Git 2.43+, OneDrive sync enabled
