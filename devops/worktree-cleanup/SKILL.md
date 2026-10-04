---
name: worktree-cleanup
description: >-
  v1.1.1 — Use when linked git worktrees have piled up and are eating disk: audit every
  worktree of a repository against a fixed expiry rubric, remove only the ones that are
  provably finished — merged, clean, unreferenced by any live agent session and by any
  open, in-progress, blocked or benched note — and report the round round after
  round until no expired worktree is left and none of the live ones was touched.
---

# Worktree cleanup

Task worktrees under a project's shared `.worktrees/<project>/` store are cheap
to create and easy to forget. A few hundred of them cost real disk space, slow
`git worktree list`, and bury the checkouts that still hold work. This skill
reclaims that space **without ever removing work that is still alive**.

It is a scored, repeatable loop, not a one-shot sweep: every run re-measures the
same repository against the same rubric, so two runs a month apart produce
comparable numbers, and a worktree that was in progress last round is simply
re-evaluated this round.

The rule that outranks everything else in this file: **when a worktree's status
cannot be established from evidence, it stays.** Disk space is recoverable;
unmerged or in-flight work is not.

## Project instructions first

Read the repository's own `AGENTS.md` and `CLAUDE.md` before touching anything;
they outrank this skill for ownership, routing, deployment, and local policy.
Follow the independently selected `worktree` and `commits` skills for
isolation and commit → merge → reapply delivery, and `testing`, `logging`, and
`docs` for applicable engineering checks. This skill does not restate their policy; it only adds what is specific to
worktree expiry. Any file this skill changes in a repository is committed
through that shared delivery policy, from a task worktree — never from the live
default branch.

## Non-negotiables

- **Never remove a worktree that fails, or cannot be evaluated against, a single
  gate in *Expiry gates*.** All gates must pass, each with evidence recorded
  this round. "Looks stale" is not evidence, and neither is age.
- **Never remove the live checkout**, the repository's primary/default branch,
  or any worktree that is not inside the project's `.worktrees/<project>/`
  store.
- **Never delete a branch whose commits are not already contained in the primary
  branch.** Unmerged commits are unpublished work.
- **Never touch a worktree that a note references while that note is anywhere
  other than the done collection** — current, in-progress, blocked, scheduled,
  used, or **benched**. A benched note is paused work, not finished work.
- **Never kill, detach, or interrupt an agent session** to make a worktree
  removable. A worktree with a live session assigned to it is in use, full stop.
- **Never use `git worktree remove --force`, `rm -rf`, `git branch -D`, or
  `git clean` to overcome a refusal.** The refusal is the point. Use
  `git worktree remove <path>` and `git branch -d <branch>`, both of which fail
  closed on dirty or unmerged state.
- **Never rewrite history, push, or delete a remote branch.** Removing a local
  worktree is local housekeeping; the remote is the user's call. Record proposed
  remote deletions under *Pending user actions*.
- **Never stash.** The stash stack is shared across every worktree of a
  repository and other sessions may be using it.
- **Never widen the scope to repositories the run was not given.** One run
  covers the repositories the user named; each is audited and reported
  separately.

## Where the score goes

**The audit is reported, never stored.** The score, the inventory, and the
per-worktree evidence go into the run report you hand back to the user. This
skill writes no scorecard file, adds no audit document to any repository, and
commits nothing about the run. An audit names repositories, branches, task
slugs, and filesystem paths — private infrastructure detail that a commit would
publish the moment the host repository is pushed.

Report each audited repository under its own heading. When one round sweeps a
shared worktree store covering many repositories at once, report a
per-repository summary plus, for every repository, each kept worktree with its
failing gate — a consolidated report may never drop per-repository detail. Use
these sections per repository:

```text
Round: <n> — <ISO date> — Score: <points>/100 (<removed>/<expired> expired removed,
<live> live worktrees preserved)

Inventory
| Worktree | Branch | Verdict | Failing gate | Evidence |
| --- | --- | --- | --- | --- |

Removed this round
Kept and why
Pending user actions
```

`Verdict` is `EXPIRED`, `LIVE`, or `UNKNOWN`. `Failing gate` names the first
gate that held the worktree back (`G4 unmerged`, `G6 in-progress note`, …), and
`Evidence` is the command output that decided it — not a summary of it.

## Expiry gates

A worktree is **expired** only when every gate below passes. Evaluate them in
order and stop at the first failure; record that gate as the reason.

- **G1 — In the store.** Its path resolves physically inside
  `<project-parent>/.worktrees/<project>/`, it is not the live checkout, and it
  is not the current worktree the run itself is using.
- **G2 — Registered and present.** `git worktree list --porcelain` knows it. A
  registered worktree whose directory is gone is `prunable`: it holds no files,
  so it is not removed but reaped with `git worktree prune`, and its branch is
  then evaluated by G4 like any other.
- **G3 — Clean.** `git -C <path> status --porcelain --untracked-files=all` is
  empty. Any modified, staged, or untracked file is uncommitted work; the
  worktree stays.
- **G4 — Merged.** `git -C <repo> rev-list --count <primary>..<branch>` is `0`,
  i.e. the primary branch already contains every commit on the branch. Determine
  the actual primary branch from repository metadata; do not assume `master` or
  `main`. A detached-HEAD worktree passes only when its `HEAD` commit is an
  ancestor of the primary branch.
- **G5 — Unoccupied.** No live agent or terminal session is assigned to it. On
  this machine the assignment is published in the session window title
  (`<task description> - <worktree name>`), so a title listing the worktree name
  means occupied. Treat an unreadable session list as occupied, not as free.
- **G6 — Not referenced by living work.** The notes store is the source of truth
  for whether the *task* is finished. A worktree named by any note in the
  current, in-progress, blocked, scheduled, or used collections, or by any note
  flagged benched, is live. Only a worktree whose sole references are notes in
  the done collection — or a worktree no note references at all, once G1–G5 also
  pass — may be removed.
- **G7 — Nothing unique left behind.** No submodule with local changes, no
  worktree-local ignored artifact the user asked to keep (build outputs,
  `.env`), and no `.log/` content the user asked to retain. When in doubt,
  report it under *Pending user actions* and keep the worktree.

### Reading the notes store

On this machine the notes store is the JSON document the
`phrase_automation` notes app owns (`PHRASE_AUTOMATION_NOTES_FILE`, default
`~/projects/notes/notes.json`). Its collections carry the lifecycle:
`current_notes`, `in_progress_notes`, `blocked_notes`, `scheduled_notes` and
`used_notes` are living work; `done_notes` is finished work; a note with
`benched: true` in any collection is paused work and counts as living.

A note names its worktree either in `agent_worktree` (an explicit path or
directory name) or at the end of its published session title `agent_task`,
after the last ` - `. Extract both, compare on the worktree **directory name**,
and treat a name you cannot parse as living.

Read that file **read-only**. Never edit, move, or rewrite the notes store to
make a worktree removable — the notes app owns it and writes it concurrently.

## Work loop

Repeat until the stop condition holds:

1. **Inventory.** For each repository in scope, resolve the live checkout
   physically, list `git worktree list --porcelain`, and record every worktree
   with its branch, its size (`du -sh`), and its store location.
2. **Snapshot the evidence sources once per round.** The notes store, the live
   session titles, and the primary branch tip. Re-read them if a round takes
   long enough for them to change.
3. **Classify.** Run G1–G7 for every worktree, recording per-gate evidence.
   Write the inventory table before removing anything.
4. **Remove the expired ones, one at a time.** `git worktree remove <path>`,
   then `git branch -d <branch>` for the branch it held (the `-d` form refuses
   an unmerged branch, which is a second, independent check of G4). Then
   `git worktree prune`. Verify after each removal that the worktree is gone
   from `git worktree list` and that the repository still reports a clean
   status.
5. **Verify no live worktree moved.** Diff the post-run `git worktree list`
   against the pre-run inventory: every path missing from it must appear in
   *Removed this round* with an `EXPIRED` verdict. Any other difference is a
   defect — report it immediately and stop.
6. **Score and report.** Score the round from this round's evidence and state
   the reclaimed size per repository in the run report. Nothing about the audit
   is written to a file or committed.

### Stop condition

Stop when, for every repository in scope:

- every worktree is classified with evidence from this round, and
- no worktree remains with an `EXPIRED` verdict, and
- every `LIVE` and `UNKNOWN` worktree is still present and untouched, and
- the score is 100/100 or every missing point is explained by a kept worktree
  and listed under *Kept and why*.

A repository whose worktrees are all live scores 100/100 with zero removals.
Removing nothing is a perfect round when nothing was expired.

## Scoring rules

100 points, awarded only from evidence recorded this round:

| # | Criterion | Points |
| --- | --- | --- |
| 1 | Every worktree in scope is classified `EXPIRED`/`LIVE`/`UNKNOWN` with per-gate evidence | 25 |
| 2 | Every `EXPIRED` worktree was removed with `git worktree remove` and its merged branch deleted with `git branch -d` | 25 |
| 3 | Every `LIVE`/`UNKNOWN` worktree is verifiably still present and unmodified after the run | 25 |
| 4 | Post-run `git worktree list` diff matches *Removed this round* exactly, with no extra deletions | 15 |
| 5 | The run report states the score, the reclaimed size per repository, and every kept worktree with its failing gate | 10 |

Penalties, subtracted from the total:

| Penalty | Points |
| --- | --- |
| A worktree was removed with a forced or manual delete (`--force`, `rm -rf`, `git branch -D`) | −100 |
| A worktree with unmerged commits, uncommitted changes, a live session, or a living note was removed | −100 |
| The notes store was written to, or a note was edited, during the run | −100 |
| A branch was deleted on a remote, or history was rewritten or pushed | −100 |
| A worktree was classified without recording the deciding command output | −20 |
| The audit was written into a repository file or committed instead of reported | −20 |

Criterion 3 is the one that matters. A run that removes nothing and proves
everything is a pass; a run that reclaims gigabytes and loses one in-progress
checkout is a failure at any score.

## Measuring

```sh
# Inventory with branches, in machine-readable form
git -C "$REPO" worktree list --porcelain

# Disk cost of the store, largest first
du -sh "$PARENT/.worktrees/$PROJECT"/* | sort -h

# G3 — clean?
git -C "$WT" status --porcelain --untracked-files=all

# G4 — merged? (0 means the primary branch already has everything)
git -C "$REPO" rev-list --count "$PRIMARY..$BRANCH"

# G5 — occupied? (session titles publish "<description> - <worktree>")
tmux list-windows -a -F '#{window_name}'

# G6 — referenced by living work? (read-only)
rg --fixed-strings "$WT_NAME" "${PHRASE_AUTOMATION_NOTES_FILE:-$HOME/projects/notes/notes.json}"
```

Prefer `rg` over `grep` for searching, and prefer porcelain/plumbing Git output
over human-readable output that changes between versions.

## Anti-patterns

- Deleting by age ("older than 30 days") — age says nothing about whether work
  landed.
- Deleting by name pattern ("looks like an experiment").
- Batching removals in one loop that keeps going after a failure, so a refusal
  scrolls past unnoticed.
- Running `git worktree prune` first and calling missing directories "cleaned".
- Treating "the branch is merged" as sufficient. Merged plus dirty means a human
  left something behind.
- Fixing a refusal by committing someone else's uncommitted changes.
- Editing the notes store to close a task so its worktree becomes removable.

## Definition of done

- [ ] Every worktree in scope has a verdict backed by this round's evidence.
- [ ] Every removal used the non-forced commands and was verified afterwards.
- [ ] The post-run inventory differs from the pre-run inventory only by the
      removed, expired worktrees.
- [ ] The run report names the score and the reclaimed size per repository, and
      no audit file was written or committed anywhere.
- [ ] Kept worktrees and anything needing the user's decision are reported.
