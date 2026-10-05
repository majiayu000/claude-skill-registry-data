---
name: git-safety
description: Stops an agent from destroying uncommitted work with git. Requires git status and git diff before any command that discards changes, treats "revert" and "undo" as manual edits, and never runs reset, checkout, clean, stash drop, or force push without explicit approval. Use when a task involves reverting, undoing, resetting, cleaning, rebasing, or force pushing, or before any git command in a repo with uncommitted changes.
---

# Git safety

These rules exist because one `git checkout -- .` erased two days of work. Follow them every time, not only when it feels risky.

## Before any git command

1. `git status`. Read it.
2. If anything is modified or untracked, stop. Say what is there. Ask before proceeding with anything that could touch those files.
3. Suggest `git stash push -m "<why>"` if the user needs a clean tree and wants the work kept.

## Commands that need explicit approval

Never run these on your own. Show the exact command, say what it will destroy, and wait for a yes.

| Command | What it destroys |
| --- | --- |
| `git reset --hard` | every uncommitted change |
| `git checkout -- <file>` or `git restore <file>` | uncommitted changes in that file |
| `git checkout -- .` or `git restore .` | uncommitted changes in every file |
| `git clean -fd` | every untracked file and folder |
| `git stash drop` or `git stash clear` | stashed work |
| `git push --force` or `--force-with-lease` | remote history other people may have |
| `git branch -D` | a branch and any commits only it holds |
| `git rebase` on a shared branch | commit ids other people have |

"Explicit approval" means the user saw the command and said yes to it. A general "go ahead" from earlier in the conversation does not count.

## Revert and undo mean edit

When the user says "revert that", "undo that", or "go back":

1. Ask which change. Committed or uncommitted? All of it or one part?
2. `git diff <file>` to see exactly what would be lost.
3. Read the current file.
4. Edit the file by hand to remove the specific lines that are wrong. Keep everything else.
5. Show the result.

Do not reach for `git checkout` or `git restore`. They remove everything in the file, including the parts the user liked.

For committed changes, `git revert <sha>` is safe because it creates a new commit. Still show the sha and the commit message first.

## Diff before discard

Any time a change is about to be thrown away, the user sees `git diff` output for it first. No exceptions. If the diff is long, show `git diff --stat` and offer the full diff.

## Commits, pushes, deploys

Do not commit, push, tag, publish, or deploy unless the user asks in the current message. When the work is done, print a suggested commit message and stop.

```
Suggested commit:
fix: dedupe heartbeat writes within 10s window
```

## Safe defaults

These are fine to run without asking:

- `git status`, `git log`, `git diff`, `git show`, `git blame`
- `git stash push -m "<message>"` when the user asked for a clean tree
- `git add <specific files>` when the user asked to commit
- `git checkout -b <new-branch>` from a clean tree
- `git revert <sha>` after showing the commit

## Checklist

Before a git command:

- [ ] `git status` ran and I read it
- [ ] no uncommitted work is in the blast radius, or the user approved
- [ ] I showed `git diff` for anything being discarded
- [ ] the command is not in the approval table, or the user said yes to this exact command

When asked to revert or undo:

- [ ] I know which change and whether it is committed
- [ ] I am editing the file, not checking it out
- [ ] everything the user did not mention stays
