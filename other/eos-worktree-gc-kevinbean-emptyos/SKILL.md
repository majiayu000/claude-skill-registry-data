---
name: eos-worktree-gc
description: Garbage-collect stale git worktrees safely — prune ONLY worktrees that are clean (no uncommitted changes) AND whose HEAD is already contained in main, leaving every dirty or unmerged worktree and the main tree untouched. Use when the user says "clean worktrees", "prune worktrees", "garbage collect worktrees", "/eos-worktree-gc", or the worktree list is cluttered with abandoned codex/fix-agent/sandbox checkouts. NEVER commits, never merges, never force-deletes. This is GC only — for committing a session's own work use /eos-session-wrapup; this skill never touches the shared main working tree or another session's uncommitted work. NOT for committing entangled work (use eos-commit-mine) and NOT for reclaiming disk generally (use eos-storage-cleanup).
---

# EmptyOS Worktree GC

Prune **stale** git worktrees and nothing else. EmptyOS spawns real git worktrees from several places — `fix-agent` (worktree-per-fix), the sandbox pool (`source_root`), `Agent(isolation: "worktree")`, and external **codex** CLI sessions (`~/.codex/worktrees/*`). They accumulate as detached-HEAD checkouts. This skill removes only the ones that are provably safe to remove, and **surfaces — never touches — anything with live work**.

This is the GC half of "clean up the repo." It deliberately does **NOT** do the dangerous half:

- It **never commits** — committing the shared main tree's uncommitted files is the parallel-session-hijack the git discipline forbids (`.claude/rules/environment.md`). Use `/eos-session-wrapup` (scoped, by-path) for that.
- It **never merges** — worktree HEADs that are *ahead* of main are unmerged work; this skill reports them and stops.
- It **never force-deletes** — a worktree that won't remove cleanly is treated as possibly-live, not an obstacle to bulldoze.

## Safety classification (the whole skill)

For every worktree except the main one, compute two facts:

```bash
cd <main-repo>            # D:/emptyos
git worktree list --porcelain | grep '^worktree ' | sed 's/^worktree //' | while read wt; do
  [ "$wt" = "<main-repo>" ] && continue
  head=$(git -C "$wt" rev-parse HEAD 2>/dev/null)
  dirty=$(git -C "$wt" status --porcelain 2>/dev/null | wc -l)
  if git merge-base --is-ancestor "$head" main 2>/dev/null; then merged=yes; else merged=no; fi
  ahead=$(git rev-list --count main.."$head" 2>/dev/null)
  echo "$wt dirty=$dirty merged=$merged ahead=$ahead"
done
```

| Class | Condition | Action |
|---|---|---|
| **STALE** | `dirty=0` AND `merged=yes` | prune (`git worktree remove`) — zero data loss, every commit is in main |
| **DIRTY** | `dirty>0` | **skip** + surface — uncommitted work, may be a live session |
| **UNMERGED** | `merged=no` / `ahead>0` | **skip** + surface — has commits not in main; report `git log` of the unique commits, never auto-merge |
| **LOCKED** | remove fails (`Directory not empty` / `Permission denied` on `.pytest_cache`/`__pycache__`) | **skip** + surface — a gitignored cache lock usually means a process (e.g. a running pytest in a codex session) is **actively using** the worktree. Treat as live. Do NOT force-delete. |

## Procedure

1. **Classify** every worktree with the loop above. Print the table.
2. **Prune STALE only**, one at a time, capturing each result:
   ```bash
   git worktree remove "<path>"   # plain — NO --force
   ```
   - On success → pruned.
   - On `Directory not empty` / permission error → reclassify as **LOCKED**, leave it, surface it. (git may have already deregistered it from the registry while failing to delete the physical dir — note the orphaned dir for the user to clean when the owning session is idle.)
3. `git worktree prune -v` to tidy stale admin refs.
4. **Report** (see below). Surface DIRTY / UNMERGED / LOCKED worktrees with one line each on *why* they were kept and *who* likely owns them (path tells you: `.codex/` = codex, fix-agent/sandbox dirs = EmptyOS subsystems).

## Orphaned directories — the ones `git worktree list` cannot see

A worktree that was deregistered but not deleted leaves a directory with **no
`.git` at all**. The registry shows nothing, so steps 1–3 above are a clean
no-op while hundreds of MB sit on disk. Measured 2026-08-30: the registry held
only `main` while `~/.codex/worktrees/` held **40 orphaned dirs / 807 MB**.

Sweep the spawner roots (`~/.codex/worktrees/*`, any `emptyos-wt*` /
`*-worktree-*` path) for dirs that are not in `git worktree list`. Codex nests
the real checkout one level down (`<hash>/emptyos/`), so test the child too.

### Prove it is disposable before deleting — the blob check

Without a `.git` you cannot ask git anything about the directory, so ask the
**repo** instead: hash every file and look the blob up in the object database.
A blob that is present was committed at some point, so nothing is lost.

```bash
find "$d" -type f ! -path '*/__pycache__/*' ! -path '*/.pytest_cache/*' \
     ! -path '*/node_modules/*' ! -name '*.pyc' > /tmp/list.txt
sed 's|^|C:/absolute/prefix/|' /tmp/list.txt > /tmp/wlist.txt   # Windows git needs C:/, not /c/
git -C <repo> hash-object --stdin-paths < /tmp/wlist.txt > /tmp/sha.txt
test "$(wc -l < /tmp/sha.txt)" -eq "$(wc -l < /tmp/list.txt)" || echo "HASHING FAILED — do not trust the result"
paste /tmp/sha.txt /tmp/list.txt > /tmp/pair.txt
cut -f1 /tmp/pair.txt | git -C <repo> cat-file --batch-check | grep -c ' missing$'
```

**Assert the hashed count equals the input count.** A path-form mismatch makes
`hash-object` emit nothing, and "no unmatched blobs" then reads exactly like
"nothing unique here" — a vacuous pass (`.claude/rules/audits.md` §Failure mode 3).

Triage the unmatched set by path before concluding anything. Expect most of it
to be legitimately absent: gitignored `data/` runtime state, `emptyos.toml`,
pytest fixtures written at runtime by a tracked test. Real salvage candidates
are source paths **untracked in `main`** — and note a nested repo
(`apps/personal/`) keeps its blobs in a *different* object DB, so its files read
as missing here and must be checked against that repo instead.

### Permission-denied is not empty

A dir carrying a **deny-read ACE** (codex's Windows sandbox leaves these) cannot
be enumerated, so a file count over it returns a **floor, not a truth** — `find`
reports 0 files for a directory holding hundreds. Never let an
"it's empty" reading that came from an unreadable dir authorise a delete.

Unlock first, then re-count, then decide:

```powershell
takeown /F <root> /R /A /D Y      # /A needs elevation; plain takeown may still be denied
icacls  <root> /reset /T /C
```

Both are **elevated** operations — `takeown /A` assigns to the Administrators
group, and the deny ACE blocks `WRITE_OWNER` even for the owning user, so an
unelevated shell cannot do this. Re-enumerate after the reset and **refuse to
delete if files appear that were invisible before**. Measured 2026-08-30: 275
files were hidden this way behind dirs that had reported 0.

Deletion still needs the user's explicit say-so (see Hard rules).

## Hard rules

- **Never** `git worktree remove --force`. Force defeats the entire safety model.
- **Never** `rm -rf` an orphaned worktree dir without explicit user confirmation — a `.pytest_cache` lock is evidence of an active process, not an obstacle.
- **Never** touch the main worktree (`D:/emptyos`), commit anything, or stage files. GC removes *redundant checkouts*; it never alters repo content.
- **Always** confirm GitHub sync read-only at the end (`git rev-list --left-right --count origin/main...main`) — report it, don't act on it. Pushing is `/eos-session-wrapup`'s job, only for the current session's own commits.

## When NOT to use

- You want to commit/push your session's work → `/eos-session-wrapup`.
- A worktree has unmerged commits you actually want in main → that's a real merge decision; do it by hand with the diff in front of you, not via GC.
- Syncing code to another machine → `/eos-deploy-homepc` (user-global skill — lives in `~/.claude/skills`, not in the repo) or a plain `git push`.

## Report

```
Worktree GC:
  Pruned (stale):   N  — <ids>
  Kept (dirty):     N  — <id>: <file count> uncommitted (owner: <codex|fix-agent|...>)
  Kept (unmerged):  N  — <id>: <ahead> commit(s) ahead of main
  Kept (locked):    N  — <id>: cache-locked, likely an active session — leave it
  Registry: <main + N remaining>
  GitHub: origin/main <ahead>/<behind> main

  Orphaned dirs (not in the registry): N found, <size>
    Salvageable:  N — <path>: <what is untracked in main>
    Disposable:   N — blob-checked, <what the unmatched files turned out to be>
    Unreadable:   N — deny-read ACE, count is a floor; needs an elevated unlock
```

Report orphans even when you delete nothing — an invisible 800 MB is the finding.
