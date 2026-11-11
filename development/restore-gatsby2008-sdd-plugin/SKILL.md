---
name: restore
description: List paused pipeline branches and restore the selected one. Filters stashes by pipeline context (.specwork/ artifacts).
allowed-tools: Bash(git stash:*), Bash(git branch:*), Bash(git rev-parse:*), Bash(git status:*), Bash(git switch:*)
---

# Restore Feature

**Load**: `view ${CLAUDE_PLUGIN_ROOT}/skills/restore/SKILL.md`

---

## What It Does

| Step | Action |
|------|--------|
| 1 | Lists all stashes created by `/sdd:pause` (`pause:` prefix in message) |
| 2 | Deduplicates by branch — keeps the most recent stash per branch, flags older ones |
| 3 | For each, reads pipeline progress from the stashed `.specwork/` |
| 4 | Shows a menu with branch name and pipeline progress |
| 5 | Verifies the current working tree is safe to switch away from |
| 6 | Switches to the recorded branch and restores the selected stash |
| 7 | Drops the stale duplicate stashes for the resumed branch |

At entry, rehydrate auto mode from pipeline state when available:

```bash
if [ "${SDD_NON_INTERACTIVE:-0}" != "1" ]; then
  SLUG="$(python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py resolve-slug)"
  SDD_MODE="$(python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py non-interactive "$SLUG" 2>/dev/null || echo 0)"
  [ "$SDD_MODE" = "1" ] && export SDD_NON_INTERACTIVE=1
fi
```

---

## Step 1 — Find Pipeline Stashes

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/stash.py list   # "<ref>\t<branch>" — deduped, newest per branch
```

`stash.py list` filters to `pause:` stashes (created by `/sdd:pause`, guaranteed
to contain `.specwork/` artifacts) and keeps only the most recent stash per
branch. Older duplicates are available via `python3 ${CLAUDE_PLUGIN_ROOT}/lib/stash.py stale`
(refs only) for cleanup in Step 7.

If no `pause:` stashes exist, abort:

```
No paused pipeline branches found.

To pause a pipeline branch, run /sdd:pause while on the branch that owns the current .specwork state.
```

---

## Step 2 — Deduplicate by Branch

A branch can have more than one `pause:` stash (e.g. paused twice without
resuming in between). Deduplication is done in code: `stash.py list` (Step 1)
already returns only the most recent stash per branch, and `stash.py stale`
returns the older duplicate refs (to drop after a successful resume, Step 7).

If `stash.py stale` returns any refs, warn before the menu (pluralize naturally —
"1 older stash" / "2 older stashes"):

```
(2 older stashes for the same branch — using the most recent only)
```

The menu in Step 4 shows each branch exactly once.

---

## Step 3 — Read Pipeline Context

For each kept (deduplicated) stash, inspect its contents to check for a spec:

```bash
git stash show -p <stash-ref> -- "*.specwork/_spec/*-spec.md" 2>/dev/null
```

Extract the feature slug from the spec filename to label the menu entry.

---

## Step 4 — Show Menu

Display only the deduplicated `pause:` stashes. Non-pipeline stashes are hidden entirely.

```
Paused pipeline branches:

  [0]  feature/PROJ-15535
  [1]  feature/PROJ-16843

  (2 other stashes exist but have no pipeline context — use git stash list to see them)

Resume which branch? (0 / 1 / cancel)
```

If only one pipeline stash exists, skip the menu and ask for confirmation directly:

```
One paused pipeline branch found:

  bugfix/existing-work

Resume? (yes / cancel)
```

If pipeline context cannot be read (e.g. stash has no `.specwork/`), show:

```
  [N]  bugfix/existing-work   (pipeline context unreadable)
```

---

## Step 5 — Verify Current Working Tree

Before switching branches, require a clean current working tree:

```bash
git status --porcelain
```

If anything is staged, unstaged, or untracked, abort:

```
Cannot resume while the current working tree has changes.

Commit, stash, or discard them first, then run /sdd:restore again.
```

---

## Step 6 — Restore

On selection, switch to the recorded pipeline branch (create locally if needed) and pop the stash:

```bash
git switch -c <branch_name> 2>/dev/null || git switch <branch_name>
git stash pop <stash-ref>
```

Print confirmation:

```
Resumed bugfix/existing-work.

Run /sdd:implement to continue.
```

---

## Step 7 — Drop Stale Duplicates

Only after the resume in Step 6 succeeds, drop the stale duplicate stashes
recorded for the resumed branch in Step 2:

```bash
git stash drop <stale-ref>
```

For each one, print:

```
  Dropping stale duplicate stash <stale-ref> ...
```

Drop only the duplicates of the **branch that was just resumed** — leave other
branches' stashes untouched. If the resume did not succeed, do not drop anything.

---

## Rules

- Keep only the most recent stash per branch; never resume from a stale duplicate.
- Drop stale duplicates only after a successful pop, and only for the resumed branch.
- Never touch non-pipeline stashes or other branches' stashes.

---

## Related Skills

- `pause` — stashes current pipeline work without switching branches
- `implement` — picks up the next pending plan step after resuming
- `whatnext` — shows full pipeline status after resuming
