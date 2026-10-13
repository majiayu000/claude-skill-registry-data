---
name: claude-worktree-reap
description: >
  Find Claude-created git worktrees in the current repo, write a human-readable
  PLAN file (path, size, danger notes) for the user to approve, delete the
  approved worktrees, write a RESULTS file (space saved, what was removed), then
  clean up both files once the user confirms. Two explicit confirmation gates,
  no auto-delete.

  Trigger this skill when:
  - User says "reap claude worktrees", "clean up claude worktrees", "delete
    claude worktrees", "purge worktrees", or invokes `/claude-worktree-reap`.
  - A repo has accumulated stray worktrees from Claude Code isolated runs.
---

## What this does

Three-stage flow with a user confirmation between every stage. The agent NEVER
deletes anything before the user reads and approves the PLAN file.

```
Stage 1  scan  → write worktree-reap-PLAN.txt         → user reads + approves
Stage 2  reap  → delete approved + write worktree-reap-RESULTS.txt → user reads
Stage 3  clean → delete PLAN + RESULTS files           → only after user confirms
```

Both generated files live at the **repo root** (so the user can open them in
their editor), named:

- `worktree-reap-PLAN.txt`
- `worktree-reap-RESULTS.txt`

---

## Stage 1 — Scan and write the PLAN file

1. **List every worktree** in the current repo:
   ```
   git worktree list --porcelain
   ```

2. **Classify each entry.** Skip the main worktree (the one whose path equals the
   repo root / `git rev-parse --show-toplevel`) — it is NEVER a candidate.

   Mark a worktree as **Claude-created** if ANY of these match:
   - path contains `claude`, `.claude`, or a session-UUID segment
     (`????????-????-????-????-????????????`)
   - path is under a scratchpad / temp dir Claude Code uses
     (`*/claude-*/`, `*/scratchpad/*`, `$TMPDIR/claude*`)
   - the checked-out branch name starts with `claude/` or contains `claude`

   Worktrees that don't match are **ambiguous** — list them separately and DO
   NOT pre-select them; the user opts them in explicitly.

3. **For each candidate, gather:**
   - **Size** — `du -sh <path>` (real disk weight of the worktree tree).
   - **Danger notes** — check, in order, and record every one that applies:
     - `LOCKED` — `git worktree list --porcelain` shows a `locked` line → do not
       remove without `--force`; flag loudly.
     - `DIRTY` — `git -C <path> status --porcelain` non-empty → uncommitted
       changes would be lost.
     - `UNMERGED` — branch has commits not in `master`/`main`/`dev`:
       `git -C <path> log --oneline <base>..HEAD` non-empty → unpushed work.
     - `NO-BRANCH` — detached HEAD (nothing named pins the work).
     - `PATH-MISSING` — recorded path no longer exists on disk → stale entry,
       `git worktree prune` territory, safe.
   - **Verdict** — `SAFE` (clean, merged, unlocked) / `REVIEW` (one soft flag) /
     `DANGER` (dirty, unmerged, or locked).

4. **Write `worktree-reap-PLAN.txt`** at the repo root. Plain text, scannable:

   ```
   CLAUDE WORKTREE REAP — PLAN
   repo: /Users/.../nimbus-skills
   generated: <stamp>

   TOTAL RECLAIMABLE: 1.9 GB across 3 worktrees

   [1] SAFE      412 MB  /tmp/claude-xxxx/wt/feat-foo
       branch: claude/feat-foo  (merged to master)
       notes:  clean, unlocked
   [2] REVIEW    880 MB  /tmp/claude-yyyy/wt/spike-bar
       branch: claude/spike-bar
       notes:  UNMERGED — 4 commits not in master (listed below)
                 a1b2c3d  wip parser
                 ...
   [3] DANGER    620 MB  /Users/.../.claude/wt/hotfix
       branch: claude/hotfix
       notes:  DIRTY — 7 uncommitted files; LOCKED
       !! deleting this LOSES uncommitted work. Excluded by default.

   AMBIGUOUS (not Claude-tagged, NOT selected — opt in manually):
   [A] 120 MB  /Users/.../wt/manual-thing  branch: feature/manual

   DEFAULT SELECTION TO DELETE: [1], [2]
   Excluded: [3] (danger), [A] (ambiguous)
   ```

5. **Stop and hand the file to the user.** Say the file is written, print the
   path, and ask them to read it and reply with their approval — which items to
   delete (default selection, or an edited set). Do not proceed until they answer.

---

## Stage 2 — Reap and write the RESULTS file

Only after explicit user approval of a specific item set.

1. **Re-verify before each removal** (state may have changed since the scan):
   re-run the DIRTY / LOCKED / UNMERGED checks. If a worktree flipped to DANGER
   since the plan, STOP and re-confirm that specific one — never silently force.

2. **Remove**, capturing size first so the tally is accurate:
   ```
   before=$(du -sk <path> | cut -f1)      # KB, before deletion
   git worktree remove --force <path>
   ```
   Then, if the user also asked to delete the branch, hand off to the
   `worktree-cleanup` ordering (`worktree remove` THEN `git branch -D`). By
   default this skill removes the **worktree only** and leaves the branch.

3. **Prune** stale entries at the end: `git worktree prune`.

4. **Write `worktree-reap-RESULTS.txt`** at the repo root:

   ```
   CLAUDE WORKTREE REAP — RESULTS
   repo: /Users/.../nimbus-skills
   ran: <stamp>

   SPACE SAVED: 1.29 GB

   DELETED:
     [1] 412 MB  /tmp/claude-xxxx/wt/feat-foo        ✓ removed
     [2] 880 MB  /tmp/claude-yyyy/wt/spike-bar       ✓ removed
   SKIPPED (per plan / your choice):
     [3] 620 MB  /Users/.../.claude/wt/hotfix        — DANGER, kept
     [A] 120 MB  /Users/.../wt/manual-thing          — ambiguous, kept
   BRANCHES: left intact (worktree-only reap)
   PRUNED:   2 stale worktree entries

   Disk before: 4.10 GB in worktrees
   Disk after:  2.81 GB in worktrees
   ```

5. **Stop and hand the results file to the user.** Print the path and the
   headline space-saved number.

---

## Stage 3 — Clean up the generated files

Only after the user has seen the RESULTS file.

1. Ask: "Delete the two report files now?" — list them:
   `worktree-reap-PLAN.txt`, `worktree-reap-RESULTS.txt`.
2. On explicit yes: `rm -f worktree-reap-PLAN.txt worktree-reap-RESULTS.txt`.
3. If the user wants to keep them, leave them and remind them they are at the
   repo root (add to `.gitignore` if not already covered, so they don't get
   committed).

---

## Do not

- **Never delete a worktree before the user approves the PLAN file.** The plan
  write and the reap are two separate turns with a confirmation between them.
- **Never force-remove a DIRTY or LOCKED worktree** without a second explicit
  confirmation naming that worktree — uncommitted work is unrecoverable.
- **Never touch the main worktree** (repo root) — it is not a candidate, ever.
- **Never delete the branch by default** — worktree-only reap. Only delete
  branches if the user explicitly asks, and then follow `worktree-cleanup`
  ordering.
- **Never auto-select ambiguous (non-Claude) worktrees** — the user opts them in.
- **Never commit or push** the PLAN / RESULTS files.

## Notes

- Sizes: `du -sh` for display, `du -sk` (KB) for arithmetic so the space-saved
  tally is exact.
- If `git worktree list` shows only the main worktree, report "no Claude
  worktrees to reap" and stop — no files written.
- Base branch for the UNMERGED check: prefer `master`, else `main`, else `dev`
  (`git rev-parse --verify` to pick the one that exists).
