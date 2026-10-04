---
name: pause
description: Stash all work including .specwork/ artifacts without switching branches. Use when switching away from the active pipeline branch mid-pipeline.
allowed-tools: Bash(git stash:*), Bash(git branch:*), Bash(git rev-parse:*), Bash(git status:*), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py:*)
---

# Pause Feature

**Load**: `view ${CLAUDE_PLUGIN_ROOT}/skills/pause/SKILL.md`

---

## What It Does

| Step | Action |
|------|--------|
| 1 | Deterministically verifies `.specwork/` belongs to the *current* branch |
| 2 | Checks for any uncommitted changes (staged or unstaged) |
| 3 | Stashes everything including gitignored files with a labeled message |
| 4 | Prints confirmation and leaves branch switching to the developer |

---

## Step 1 — Verify Branch (STRICT — do not skip this call)

`.specwork/` is gitignored, so it does **not** move with branch changes. It
commonly still holds a *different* branch's pipeline after a `git checkout`.
Never decide this by eyeballing branch names — call the shared check, which
inspects every `state.json`'s recorded `branch` field, not just the first one:

```bash
BRANCH="$(git rev-parse --abbrev-ref HEAD)"
STATUS="$(python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py pipeline-branch-status "$BRANCH")"
```

`STATUS` is one JSON object: `has_any_pipeline`, `owns_pipeline`, `slug`,
`recorded_branch`, `recorded_base_branch`, `is_base_branch`.

- **`has_any_pipeline` is `false`** — nothing on disk at all. Abort:
  ```
  No active pipeline state found for this branch. Run /sdd:start first.
  ```
- **`has_any_pipeline` is `true` but `owns_pipeline` is `false`** — a pipeline
  exists, but it belongs to a *different* branch (`recorded_branch`, slug
  `slug`). This is the dangerous case: stashing here would fold that other
  pipeline's state into a stash labeled with *this* branch's name, corrupting
  `/sdd:restore`'s bookkeeping. Abort — do not stash:
  ```
  ✗ Cannot pause here.

  .specwork/ belongs to '<recorded_branch>' (slug '<slug>'), not '<BRANCH>'.
  It's gitignored and didn't move when you switched branches — it is still on
  disk, but it is not this branch's pipeline to pause.

    • To pause it: switch to '<recorded_branch>' and run /sdd:pause there.
    • To start fresh work here: this branch has no pipeline yet — run /sdd:start.
  ```
- **`owns_pipeline` is `true`** — this branch's own pipeline. Continue to Step 2.

---

## Step 2 — Check Working Tree

Run `git status --porcelain`. If the working tree is completely clean AND
`.specwork/` does not exist or is empty, abort:

```
Nothing to pause — working tree is clean and no .specwork/ artifacts found.
```

---

## Step 3 — Stash

Use `--all` to include gitignored files (captures `.specwork/`).
Label the stash with the branch name so `/sdd:restore` can identify it:

```bash
git stash push --all --message "pause: <branch_name>"
```

Example message: `pause: bugfix/existing-work`

---

## Step 4 — Confirm

```
Paused bugfix/existing-work → stash saved.

You can now switch to any branch you need.
Resume later with /sdd:restore.
```

---

## Related Skills

- `restore` — restores a paused pipeline branch, filtering only pipeline stashes
