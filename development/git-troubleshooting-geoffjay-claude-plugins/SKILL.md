---
name: git-troubleshooting
description: Git troubleshooting techniques including recovering lost commits, fixing merge conflicts, resolving detached HEAD, and diagnosing repository issues. Use when user encounters git errors or needs to recover from mistakes.
---

# Git Troubleshooting Skill

This skill provides comprehensive guidance on diagnosing and resolving git issues, recovering from mistakes, fixing corrupted repositories, and handling common error scenarios.

## When to Use

Activate this skill when:
- Encountering git error messages
- Recovering lost commits or branches
- Fixing corrupted repositories
- Resolving detached HEAD state
- Handling botched merges or rebases
- Diagnosing repository issues
- Recovering from force push
- Fixing authentication problems

## Recovering Lost Commits

### Using Reflog

```bash
# View reflog (local history of HEAD)
git reflog

# View reflog for specific branch
git reflog show branch-name

# Output example:
# abc123 HEAD@{0}: commit: feat: add authentication
# def456 HEAD@{1}: commit: fix: resolve bug
# ghi789 HEAD@{2}: reset: moving to HEAD~1

# Recover lost commit
git cherry-pick abc123

# Or create branch from lost commit
git branch recovered-branch abc123

# Or reset to lost commit
git reset --hard abc123
```

### Finding Dangling Commits

```bash
# Find all unreachable objects
git fsck --lost-found

# Output:
# dangling commit abc123
# dangling blob def456

# View dangling commit
git show abc123

# Recover dangling commit
git branch recovered abc123

# Or merge it
git merge abc123
```

### Recovering Deleted Branch

```bash
# Find branch commit in reflog
git reflog

# Look for branch deletion:
# abc123 HEAD@{5}: checkout: moving from feature-branch to main

# Recreate branch
git branch feature-branch abc123

# Or if branch was merged before deletion
git log --all --oneline | grep "feature"
git branch feature-branch def456
```

### Recovering After Reset

```bash
# After accidental reset --hard
git reflog

# Find commit before reset:
# abc123 HEAD@{0}: reset: moving to HEAD~5
# def456 HEAD@{1}: commit: last good commit

# Restore to previous state
git reset --hard def456

# Or create recovery branch
git branch recovery def456
```

## Resolving Detached HEAD

### Understanding Detached HEAD

```bash
# Detached HEAD state occurs when:
git checkout abc123
git checkout v1.0.0
git checkout origin/main

# HEAD is not attached to any branch
```

### Recovering from Detached HEAD

```bash
# Check current state
git status
# HEAD detached at abc123

# Option 1: Create new branch
git checkout -b new-branch-name

# Option 2: Return to previous branch
git checkout main

# Option 3: Reattach HEAD to branch
git checkout -b temp-branch
git checkout main
git merge temp-branch

# If you made commits in detached HEAD:
git reflog
# Find the commits
git branch recovery-branch abc123
```

### Preventing Detached HEAD

```bash
# Instead of checking out tag directly
git checkout -b release-v1.0 v1.0.0

# Instead of checking out remote branch
git checkout -b local-feature origin/feature-branch

# Check if HEAD is detached
git symbolic-ref -q HEAD && echo "attached" || echo "detached"
```

## Fixing Merge Conflicts

### Understanding Conflict Markers

```
<<<<<<< HEAD (Current Change)
int result = add(a, b);
||||||| merged common ancestors (Base)
int result = sum(a, b);
=======
int sum = calculate(a, b);
>>>>>>> feature-branch (Incoming Change)
```

### Basic Conflict Resolution

```bash
# When merge conflict occurs
git status
# both modified: file.go

# View conflict
cat file.go

# Option 1: Keep ours (current branch)
git checkout --ours file.go
git add file.go

# Option 2: Keep theirs (incoming branch)
git checkout --theirs file.go
git add file.go

# Option 3: Manual resolution
# Edit file.go to resolve conflicts
git add file.go

# Complete merge
git commit
```

### Aborting Operations

```bash
# Abort merge
git merge --abort

# Abort rebase
git rebase --abort

# Abort cherry-pick
git cherry-pick --abort

# Abort revert
git revert --abort

# Abort am (apply mailbox)
git am --abort
```

### Complex Conflict Resolution

```bash
# Use merge tool
git mergetool

# View three-way diff
git diff --ours
git diff --theirs
git diff --base

# Show conflicts with context
git diff --check

# List conflicted files
git diff --name-only --diff-filter=U

# After resolving all conflicts
git add .
git commit
```

## Fixing Botched Rebase

### Recovering from Failed Rebase

```bash
# Abort current rebase
git rebase --abort

# Find state before rebase
git reflog
# abc123 HEAD@{1}: rebase: checkout main

# Return to pre-rebase state
git reset --hard HEAD@{1}

# Alternative: use ORIG_HEAD
git reset --hard ORIG_HEAD
```

### Rebase Conflicts

```bash
# During rebase conflict
git status
# both modified: file.go

# Resolve conflicts
# Edit file.go
git add file.go
git rebase --continue

# Skip problematic commit
git rebase --skip

# Edit commit during rebase
git commit --amend
git rebase --continue
```

### Rebase onto Wrong Branch

```bash
# Find original branch point
git reflog

# Reset to before rebase
git reset --hard HEAD@{5}

# Rebase onto correct branch
git rebase correct-branch
```

## Repository Corruption

### Detecting Corruption

```bash
# Check repository integrity
git fsck --full

# Check connectivity
git fsck --connectivity-only

# Verify pack files
git verify-pack -v .git/objects/pack/*.idx
```

### Fixing Corrupted Objects

```bash
# Remove corrupted object
rm .git/objects/ab/cd1234...

# Try to recover from remote
git fetch origin

# Rebuild object database
git gc --prune=now

# Aggressive cleanup
git gc --aggressive --prune=now
```

### Fixing Index Corruption

```bash
# Remove corrupted index
rm .git/index

# Rebuild index
git reset

# Or reset to HEAD
git reset --hard HEAD
```

### Recovering from Bad Pack File

```bash
# Unpack corrupted pack
git unpack-objects < .git/objects/pack/pack-*.pack

# Remove corrupted pack
rm .git/objects/pack/pack-*

# Repack repository
git repack -a -d

# Verify integrity
git fsck --full
```

## Fixing References

### Corrupted Branch References

```bash
# View all references
git show-ref

# Manual reference fix
echo "abc123def456" > .git/refs/heads/branch-name

# Or use update-ref
git update-ref refs/heads/branch-name abc123

# Delete corrupted reference
git update-ref -d refs/heads/bad-branch
```

### Fixing HEAD Reference

```bash
# HEAD is corrupted or missing
echo "ref: refs/heads/main" > .git/HEAD

# Or point to specific commit
echo "abc123def456" > .git/HEAD

# Verify HEAD
git symbolic-ref HEAD
```

### Pruning Stale References

```bash
# Remove stale remote references
git remote prune origin

# Remove all stale references
git fetch --prune

# Remove all remote branches that no longer exist
git branch -vv | grep ': gone]' | awk '{print $1}' | xargs git branch -D
```

## Undoing Changes

### Undo Last Commit (Keep Changes)

```bash
# Soft reset (changes staged)
git reset --soft HEAD~1

# Mixed reset (changes unstaged)
git reset HEAD~1
```

### Undo Last Commit (Discard Changes)

```bash
# Hard reset
git reset --hard HEAD~1

# Can still recover via reflog
git reflog
git reset --hard HEAD@{1}
```

### Undo Multiple Commits

```bash
# Reset to specific commit
git reset --hard abc123

# Revert multiple commits (creates new commits)
git revert HEAD~3..HEAD

# Interactive rebase to remove commits
git rebase -i HEAD~5
# Mark commits with 'drop' or delete lines
```

### Undo Changes to File

```bash
# Discard uncommitted changes
git checkout -- file.go

# Or in Git 2.23+
git restore file.go

# Discard staged changes
git reset HEAD file.go
git restore file.go

# Or in Git 2.23+
git restore --staged file.go
git restore file.go

# Restore file from specific commit
git checkout abc123 -- file.go
```

### Undo Public Commits

```bash
# Never use reset on public commits
# Use revert instead
git revert HEAD
git revert abc123
git revert abc123..def456

# Revert merge commit
git revert -m 1 merge-commit-hash
```

## Handling Force Push Issues

### Recovering After Force Push

```bash
# If you were force pushed over
git reflog
# abc123 HEAD@{1}: pull: Fast-forward

# Recover your commits
git reset --hard HEAD@{1}

# Create backup branch
git branch backup-branch

# Merge with force-pushed branch
git pull origin main
git merge backup-branch
```

### Preventing Force Push Damage

```bash
# Always fetch before force push
git fetch origin

# View what would be lost
git log origin/main..HEAD

# Force push with lease (safer)
git push --force-with-lease origin main

# Configure push protection
git config --global push.default simple
```

## Large File Issues

### Finding Large Files

```bash
# Find large files in history
git rev-list --objects --all | \
  git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | \
  awk '/^blob/ {print substr($0,6)}' | \
  sort --numeric-sort --key=2 | \
  tail -10

# Verify current large files
git ls-files | xargs ls -lh | sort -k 5 -h -r | head -20
```

### Removing Large Files

```bash
# Using git-filter-repo (recommended)
git filter-repo --path large-file.bin --invert-paths

# Using BFG
bfg --strip-blobs-bigger-than 100M

# After removal
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force origin main
```

### Preventing Large Files

```bash
# Configure pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
if git diff --cached --name-only | xargs du -h | awk '$1 ~ /M$|G$/' | grep .; then
    echo "Error: Large file detected"
    exit 1
fi
EOF

chmod +x .git/hooks/pre-commit
```

## Authentication Issues

### SSH Key Problems

```bash
# Test SSH connection
ssh -T git@github.com

# Check SSH key
ls -la ~/.ssh

# Generate new SSH key
ssh-keygen -t ed25519 -C "email@example.com"

# Add key to ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Configure SSH
cat > ~/.ssh/config << EOF
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519
EOF
```

### HTTPS Authentication

```bash
# Cache credentials
git config --global credential.helper cache
git config --global credential.helper 'cache --timeout=3600'

# Or use store (less secure)
git config --global credential.helper store

# Update remote URL
git remote set-url origin https://github.com/user/repo.git

# Use personal access token
git clone https://TOKEN@github.com/user/repo.git
```

### Permission Denied

```bash
# Check remote URL
git remote -v

# Change to SSH
git remote set-url origin git@github.com:user/repo.git

# Change to HTTPS
git remote set-url origin https://github.com/user/repo.git

# Verify permissions
ls -la .git/
chmod -R u+rw .git/
```

## Submodule Issues

### Submodule Not Initialized

```bash
# Initialize submodules
git submodule init
git submodule update

# Or in one command
git submodule update --init --recursive
```

### Detached HEAD in Submodule

```bash
# Enter submodule
cd submodule-dir

# Create branch
git checkout -b main

# Or attach to existing branch
git checkout main
git pull origin main

# Update parent repo
cd ..
git add submodule-dir
git commit -m "chore: update submodule"
```

### Submodule Conflicts

```bash
# Check submodule status
git submodule status

# Reset submodule
git submodule update --init --force

# Remove and re-add submodule
git submodule deinit -f path/to/submodule
git rm -f path/to/submodule
git submodule add <url> path/to/submodule
```

## Performance Issues

### Slow Operations

```bash
# Optimize repository
git gc --aggressive

# Repack efficiently
git repack -a -d --depth=250 --window=250

# Prune old objects
git prune --expire now

# Clean up unnecessary files
git clean -fdx
```

### Large Repository

```bash
# Shallow clone
git clone --depth 1 <url>

# Fetch only one branch
git clone --single-branch --branch main <url>

# Partial clone
git clone --filter=blob:none <url>

# Sparse checkout
git sparse-checkout init --cone
git sparse-checkout set folder1 folder2
```

### Memory Issues

```bash
# Increase memory limits
git config --global pack.windowMemory "100m"
git config --global pack.packSizeLimit "100m"
git config --global pack.threads "1"

# Disable delta compression temporarily
git config --global pack.compression 0
```

## Common Error Messages

### "fatal: refusing to merge unrelated histories"

```bash
# Allow merging unrelated histories
git pull origin main --allow-unrelated-histories
```

### "fatal: not a git repository"

```bash
# Reinitialize repository
git init

# Or check if .git directory exists
ls -la .git

# Restore from backup if corrupted
```

### "error: Your local changes would be overwritten"

```bash
# Stash changes
git stash
git pull
git stash pop

# Or discard changes
git reset --hard HEAD
git pull
```

### "error: failed to push some refs"

```bash
# Fetch and merge first
git pull origin main

# Or rebase
git pull --rebase origin main

# Force push (dangerous)
git push --force origin main

# Safer force push
git push --force-with-lease origin main
```

### "fatal: unable to access: SSL certificate problem"

```bash
# Disable SSL verification (not recommended)
git config --global http.sslVerify false

# Or update SSL certificates
git config --global http.sslCAInfo /path/to/cacert.pem
```

## Diagnostic Commands

### Repository Health Check

```bash
# Full integrity check
git fsck --full --strict

# Check connectivity
git fsck --connectivity-only

# Verify objects
git verify-pack -v .git/objects/pack/*.idx

# Check reflog
git reflog expire --dry-run --all

# Analyze repository
git count-objects -vH
```

### Debug Information

```bash
# Enable verbose logging
GIT_TRACE=1 git status
GIT_TRACE=1 git pull

# Debug specific operations
GIT_TRACE_PACKET=1 git fetch
GIT_TRACE_PERFORMANCE=1 git diff
GIT_CURL_VERBOSE=1 git push

# Configuration debugging
git config --list --show-origin
git config --list --show-scope
```

## Prevention Strategies

1. **Regular Backups:** Create backup branches before risky operations
2. **Use Reflog:** Reflog is your safety net, keep it clean
3. **Enable Rerere:** Reuse recorded conflict resolutions
4. **Protect Branches:** Use branch protection rules
5. **Pre-commit Hooks:** Validate commits before they're made
6. **Regular Maintenance:** Run `git gc` periodically
7. **Test Before Force Push:** Always verify with `--dry-run`
8. **Communication:** Inform team about disruptive operations
9. **Learn Git Internals:** Understanding how git works prevents issues
10. **Keep Git Updated:** Use latest stable version

## Resources

Additional troubleshooting guides are available in the `assets/` directory:
- `troubleshooting/` - Step-by-step recovery procedures
- `scripts/` - Diagnostic and recovery scripts
- `checklists/` - Problem diagnosis workflows

See `references/` directory for:
- Git error message database
- Recovery procedure documentation
- Git internal structure guides
- Common pitfall documentation
