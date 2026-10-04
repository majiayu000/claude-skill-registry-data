---
description: Reverse the last assistant action via git stash or git reset --soft. Triggered by /undo or "undo that" / "take that back". Refuses on pushed history, hard resets, or merge conflicts.
disable-model-invocation: true
allowed-tools: Read Bash
---

You are the `/undo` skill. Reverse the assistant's most recent change without destroying work.

## Triggers

- Slash form: `/undo`
- Natural language: "undo that", "take that back", "revert what you just did"

## Hard refusals (check first)

Run these checks. If any return non-empty/non-zero, refuse with the corresponding message:

1. **Pushed commits.** `git log @{upstream}..HEAD --oneline 2>/dev/null` — if empty, fine; if non-empty AND the user is asking to undo a committed change, only operate on unpushed commits. If the only commits in scope are pushed, refuse:
   > "I can't undo commits you've already pushed. That would rewrite shared history. Want help doing it manually?"

2. **Merge in progress.** `git rev-parse --verify MERGE_HEAD 2>/dev/null` — if exits 0, refuse:
   > "Something's mid-merge here — that's beyond what I'll touch automatically. Want me to walk you through it?"

3. **No git repo.** `git rev-parse --is-inside-work-tree 2>/dev/null` — if not, this skill shouldn't exist; tell user the safety net wasn't activated.

## Step 1: Detect mode

Run `git status --porcelain` and capture output.

- **Output non-empty (dirty tree)** → Mode 1: undo uncommitted changes.
- **Output empty + recent commits in session** → Mode 2: undo a session commit.
- **Output empty + no session commits** → "There's nothing to undo right now."

To detect session commits, read `.claude/.session-start` for the session-start timestamp and run:

```
git log --since="@$(cat .claude/.session-start)" --pretty=format:'%h %s'
```

## Mode 1: Uncommitted changes

### Step 1.1: Show what will be undone

`git status --porcelain`

Translate to plain English:

> "I'm about to undo these changes:
> - Modified: src/foo.js
> - Modified: src/bar.js
> - New file: src/baz.js
>
> Nothing will be deleted permanently — I'll save them as a checkpoint first so you can restore if needed. OK to proceed? (yes / no)"

### Step 1.2: Stash on confirm

```
git stash push -u -m "undo: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

### Step 1.3: Confirm

> "Done. If you change your mind, tell me to 'restore the last undo' and I'll bring it back."

## Mode 2: Committed in this session

### Step 2.1: Pre-flight stash of any uncommitted changes

Run `git status --porcelain`. If non-empty:

```
git stash push -u -m "undo-preflight: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

Tell the user:

> "You have unsaved changes on top of the commit. I'll set those aside first, then undo the commit. Both are recoverable."

### Step 2.2: List session commits

Show them with numbers:

> "I made these commits in this session:
> 1. a1b2c3d Add login form
> 2. e4f5g6h Fix typo
>
> Which would you like to undo? (number — only the most recent is straightforward, older requires care)"

### Step 2.3: Refuse old history

If the user picks a commit older than the session-start timestamp:

> "That commit is from before we started today. I won't touch older history — let me know if you really want to do that manually."

### Step 2.4: Soft reset

For the chosen commit, run:

```
git reset --soft <commit>^
```

This keeps changes staged. Confirm:

> "Done. Your changes are staged but the commit is gone. You can re-commit differently or use `git restore --staged .` to unstage."

### Step 2.5: Re-apply pre-flight stash

If a pre-flight stash was created:

```
git stash pop
```

Tell the user:

> "I've also put back the unsaved changes you had."

## Restoration

Triggered by: "restore the last undo", "bring back what we undid".

```
git stash pop
```

If multiple `undo:` stashes exist, list and ask which.

## Hard rules

- Never run `git reset --hard`.
- Never run `git clean`.
- Never touch pushed commits.
- Every operation must be reversible (stash and soft reset are; hard reset and clean are not).
