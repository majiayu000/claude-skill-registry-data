---
name: dotfiles-multi-machine-sync
description: This skill should be used when working on the dotfiles repo across two Macs (work + personal), when a local branch turns out to be already merged/deleted elsewhere, or to recover uncommitted work onto an updated main.
---

# Dotfiles Multi-Machine Sync (work + personal Mac)

The dotfiles repo is edited from two Macs. Branches merged + deleted on one machine
leave a stale local branch on the other. Always sync before working.

## Before starting work — pull first

```bash
git checkout main && git pull --ff-only
```

This is the #1 prevention. Skipping it is how you end up committing onto a local
branch that was already merged into origin/main from the other Mac.

## Symptoms of a stale local branch

Running `git fetch --prune` then:
- `git status -sb` shows `origin/<branch> [gone]` → the remote branch was deleted
  (merged via PR with auto-delete).
- `git log origin/main..<branch> --oneline` is **empty** → all that branch's commits
  are already in origin/main. The branch is dead.
- `git rev-list --left-right --count main...origin/main` shows `0  N` → local main is
  N commits behind; the other Mac advanced it.

## Recover uncommitted work onto updated main

When the working tree has uncommitted changes on a dead branch:

```bash
# 1. stash ONLY your files (named, includes untracked with -u)
git stash push -u -m "<desc>" -- <file1> <file2> <dir>/

# 2. move to main and update
git checkout main && git pull --ff-only

# 3. reapply
git stash pop
```

Expect a **merge conflict** if the other Mac touched the same files. Resolve by
keeping BOTH sides when the changes are additive (e.g. one Mac added an Obsidian
block, the other a Tailscale block — keep both, drop the markers).

## Verify after recovery

```bash
grep -nc '^<<<<<<<\|^=======\|^>>>>>>>\|^||||||| ' <file>   # 0 = clean
git rev-list --left-right --count main...origin/main         # 0  0 = aligned
```

For Ansible changes also run: `ansible-playbook playbooks/site.yml --syntax-check`
and `yamllint` (see `ansible-dotfiles-setup` skill).
