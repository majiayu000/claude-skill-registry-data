---
name: git-guide
description: "A comprehensive guide to Git commands and workflows, based on the official Git cheat sheet. Use this skill to learn and reference common Git operations, from basic repository setup to advanced history manipulation."
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

<instructions>

This skill provides a comprehensive guide to Git commands and workflows, based on the official Git cheat sheet. Use it to learn and reference common Git operations.

---

# Getting Started

- **Start a new repo:** `git init`
- **Clone an existing repo:** `git clone <url>`

---

# Prepare to Commit

- **Add untracked file or unstaged changes:** `git add <file>`
- **Add all untracked files and unstaged changes:** `git add .`
- **Choose which parts of a file to stage:** `git add -p`
- **Move file:** `git mv <old> <new>`
- **Delete file:** `git rm <file>`
- **Forget about a file without deleting it:** `git rm --cached <file>`
- **Unstage one file:** `git reset <file>`
- **Unstage everything:** `git reset`
- **Check status:** `git status`

---

# Make Commits

- **Commit (opens editor):** `git commit`
- **Commit with message:** `git commit -m 'message'`
- **Commit all unstaged changes:** `git commit -am 'message'`
- **Change commit message/add forgotten file:** `git commit --amend`

---

# Move Between Branches

- **Switch branches:** `git switch <name>` or `git checkout <name>`
- **Create a branch:** `git switch -c <name>` or `git checkout -b <name>`
- **List branches:** `git branch`
- **List branches by recency:** `git branch --sort=-committerdate`
- **Delete a branch:** `git branch -d <name>`
- **Force delete a branch:** `git branch -D <name>`

---

# Diff Changes

## Diff Staged/Unstaged Changes

- **Diff all staged and unstaged:** `git diff HEAD`
- **Diff just staged:** `git diff --staged`
- **Diff just unstaged:** `git diff`

## Diff Commits

- **Show diff of a commit and its parent:** `git show <commit>`
- **Diff two commits:** `git diff <commit> <commit>`
- **Diff one file since a commit:** `git diff <commit> <file>`
- **Summary of a diff:** `git diff <commit> --stat` or `git show <commit> --stat`

---

# Ways to Refer to a Commit

- **Branch:** `main`
- **Tag:** `v0.1`
- **Commit ID:** `3e887ab`
- **Remote branch:** `origin/main`
- **Current commit:** `HEAD`
- **Relative:** `HEAD~3` (3 commits ago)

---

# Discard Your Changes

- **Delete unstaged changes to a file:** `git restore <file>` or `git checkout <file>`
- **Delete all staged/unstaged changes to a file:** `git restore --staged --worktree <file>`
- **Delete all staged and unstaged changes:** `git reset --hard`
- **Delete untracked files:** `git clean`
- **Stash changes:** `git stash`

---

# Edit History

- **Undo most recent commit (keep directory):** `git reset HEAD^`
- **Squash last 5 commits:** `git rebase -i HEAD~6` (change "pick" to "fixup")
- **Undo failed rebase:** `git reflog BRANCHNAME` then `git reset --hard <commit>`
- **Change commit message/add forgotten file:** `git commit --amend`

---

# Code Archaeology

- **Look at history:** `git log main`, `git log --graph`, `git log --oneline`
- **Show commits modifying a file:** `git log <file>`
- **Show commits including renames:** `git log --follow <file>`
- **Find text in commits:** `git log -G banana`
- **Show who changed each line:** `git blame <file>`

---

# Combine Diverged Branches

- **Rebase:** `git switch banana` -> `git rebase main`
- **Merge:** `git switch main` -> `git merge banana`
- **Squash Merge:** `git merge --squash banana` -> `git commit`
- **Cherry-pick:** `git cherry-pick <commit>`

---

# Restore an Old File

- **Get version from another commit:** `git checkout <commit> <file>` or `git restore <file> --source <commit>`

---

# Remotes & Pushing

- **Add remote:** `git remote add <name> <url>`
- **Push main to origin:** `git push origin main`
- **Push current branch:** `git push`
- **Push new branch:** `git push -u origin <name>`
- **Force push:** `git push --force-with-lease`
- **Push tags:** `git push --tags`

---

# Pull Changes

- **Fetch (no local change):** `git fetch origin main`
- **Pull and rebase:** `git pull --rebase`
- **Pull and merge:** `git pull origin main`

---

# Configuration

- **Set name:** `git config user.name 'Your Name'`
- **Set global option:** `git config --global ...`
- **Add alias:** `git config alias.st status`

---

# Important Files

- **Local config:** `.git/config`
- **Global config:** `~/.gitconfig`
- **Ignore list:** `.gitignore`

</instructions>
