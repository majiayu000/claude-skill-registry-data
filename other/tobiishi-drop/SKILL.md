---
name: tobiishi-drop
description: |
  PM-posture skill that drops an unsealed 飛び石 Tobiishi change unit — halts outside a pm session or
  the pm subagent. shukuba-refine runs it when it judges a halted unit dropped.
  Drop a change unit that will not be finished. Moves `journey/tobiishi/<key>/` whole into
  `journey/tobiishi/drop/<key>/`, marks the project's `CONTEXT_PM.md` as dropped when it names the unit,
  commits the move on main with the reason as the commit body, then closes the change's worktrees while
  keeping every branch unmerged. Takes the project, the change key and the reason, all required — the
  reason is never composed for the caller. Refuses a blank reason, a sealed or already dropped unit, and
  any worktree holding uncommitted work. Touches no station, no seed and no seal. Reports where the
  journey stands and who owns the next move. Asks nothing, so it runs unattended.
  Use when: a change unit is set down for good before it is sealed — its subject went away upstream, its
  intake was halted as several changes the route now walks as separate units, or the work is abandoned. Ordinarily reached through shukuba-refine, which decides the drop.
  Do not use for: a finished unit (use tobiishi-seal — that seals and merges), a station being set down
  (use shukuba-park to set it down unreached, shukuba-retire to close a reached one), or an idea (use
  nemawashi-unpick, or nemawashi-retire).
  Trigger phrases - "drop this change unit", "drop the tobiishi", "abandon this change", "this change is
  dead, set it down", "tobiishi-drop".
license: MIT
metadata:
  author: Eyal Golan
  version: "1.0.7"
  created: "2026-09-19"
  category: journey
  risk: safe
  tags: tobiishi, drop, pm, journey
---

# Tobiishi Drop

## Purpose

**Set down a change unit that will not be finished, and say where that leaves the journey.** A 飛び石
Tobiishi ends one of two ways: it is sealed (`tobiishi-seal`, which merges the work) or it is dropped
(this skill, which merges nothing). A dropped unit keeps its whole folder, at
`journey/tobiishi/drop/<key>/`, and every branch it had stays where it was, unmerged, so nothing the
change made is lost and nothing it made reaches `main`.

**The script decides and moves; this file sequences it and commits.** `scripts/drop.py` refuses what may
not be dropped, moves the folder, marks the context and removes the worktrees. Whatever it refuses, this
skill does not work around.

**The station and the seed are not touched.** Dropping the unit leaves its station open and its seed's
checklist as it was. Whether to open the next station, or to retire a walked seed, is another seat's
call and is named at the end, never performed here.

**Shared mechanics.** How a journey artifact changes folder and how that commit is built is
`<CORE>/docs/journey_move.md` and `<CORE>/doctrine/governance/commit_via_builder.md`. Read them;
this file names the section it leans on at each step and restates none of it.

## Posture

**PM only.** Run in a `pm:` session or as the `pm` subagent. Invoked from anywhere else, halt at once,
change nothing, say the posture is wrong, and name both ways in: open a `pm:` session, or launch the
`pm` subagent. The seat's contract is `<CORE>/roles/loaders/pm_global.md`. Whether a unit is dropped
is the PM's judgment, and `shukuba-refine` is where the PM makes it and runs this skill — the owner's
ruling of 2026-09-19. The gate is there because the run moves, commits and removes worktrees with nobody
answering — `<CORE>/doctrine/setup/authoring_layers.md` § *A skill that acts unattended gates to its
seat*. No other seat may run this skill.

## Input

Three values, all required: **the project**, **the change key** (`<YYYY-MM-DD>_<slug>`, the folder name
under `journey/tobiishi/`) and **the reason**. If any is missing, or the reason is blank, halt and name
what is missing. **Never compose the reason** from the unit's files or the conversation, and never give
it a default: it is the commit's record of why work was set down, and only the caller knows it.

## Workflow

Run from the instance root. `<drop>` is `python3 <CORE>/../skills/pm/.claude/skills/tobiishi-drop/scripts/drop.py --root .`.

### Step 1 — Check, before anything changes

```bash
<drop> check <project> <key> "<reason>"
```

Exit 1 is a refusal: blank reason, a key that is sealed, already dropped or no open unit, or a worktree
with uncommitted work, each named. **Stop at the first refusal** — print it, change nothing, and do not
retry with different values. The script checks every worktree before any effect, so one dirty worktree
stops the whole drop; committing or discarding that work is the owner's call, not this skill's. On
success it lists each worktree `close` will remove.

### Step 2 — Move the unit and mark the context

```bash
<drop> apply <project> <key>
```

It `git mv`s the folder to `tobiishi/drop/<key>/`, creating `drop/` on the first drop. It prints every
path the commit must declare, then a last line saying whether `CONTEXT_PM.md` was marked. Keep the
printed paths, and whether the context was marked.

### Step 3 — Commit on main

Per `<CORE>/docs/journey_move.md` § *The commit* and `<CORE>/doctrine/governance/commit_via_builder.md`, through
`<CORE>/tools/commit_builder.py` with `--repo .`:

- **The move is already staged**, so declare it with `--staged`, naming **both halves** of every path
  `apply` printed. `CONTEXT_PM.md` rides `--add` **only when `apply` said it was marked** — adding it
  otherwise says something false about the commit.
- **Subject** `drop: <key>`. **Body** the reason, verbatim. When the reason holds a backtick, pass it
  through a file rather than the command line.
- **`--actor pm`, and no `--skill`.** A move commits nothing a skill produced.
- **`--directional`** is `Shukuba: <open station> — aside: dropped <key>` when a station is open at the
  project's `journey/shukuba/` root, else `Agari: <project> — aside: dropped <key>`. A drop sets work
  down, and a set-down reads `aside:`, never `progress:`.

Then eyeball `git show --stat`: one rename per file of the unit, plus `CONTEXT_PM.md` only when marked.

### Step 4 — Close the worktrees

```bash
<drop> close <project> <key>
```

Only after the commit. It removes each worktree without `--force` and never deletes a branch. A failure
here leaves a dropped unit with a live worktree, which is safe and is reported as it is. Its output is
the report: the key and its new path, the worktrees closed and branches kept, the context mark, and where
the journey stands.

### Step 5 — Say which pointers the move broke

```bash
python3 "<CORE>/tools/check_journey_links.py" --repo .
```

Report whatever it names, per `<CORE>/docs/journey_move.md` § *After the move, say which pointers it broke*. **Do not
gate on its exit code**: a drop that refuses because some other file points at the wrong place is
stricter than the journey wants.

### Step 6 — Report

Print what `close` printed, in its order, then state the next owner, and only state it:

- The station is still open. Whether it still has work, or is reached, is the route's to say —
  `shukuba-refine`'s when it ran this skill.
- Where no unchecked item remains on the seed, the retire is owed to the **Scrum Master** (`nemawashi-retire`).

This run parks, ticks, opens and retires nothing, and does not offer to.

---

## Outputs

| Effect | Produced when |
|---|---|
| `tobiishi/<key>/` moved to `tobiishi/drop/<key>/`, plus `CONTEXT_PM.md` marked when it names the unit, in one commit on main | Success (Steps 2-3) |
| Worktrees removed, branches kept | Success (Step 4) |
| A report of where the journey stands, and the pointers the move broke | Always after a commit |
| No change; the refusal printed | Any refusal (Step 1), or a wrong posture |

## Critical Rules

- **PM only.** Any other posture halts before a single call, with the way in named.
- **No default reason, no composed reason.** A missing or blank reason halts.
- **Check, then commit, then close.** Every refusal comes before any effect, and the record on `main`
  comes before the teardown, so a failed teardown never leaves a removed worktree for a drop that did not
  commit.
- **A branch is never deleted and a worktree is never force-removed.** This is where a drop departs from
  the seal, which merges and deletes. A drop merges nothing.
- **Nothing else moves.** Never edit anything under `journey/shukuba/`, `journey/nemawashi/` or
  `<CORE>/../skills/pm/.claude/skills/tobiishi-seal/`. A sealed or already dropped unit is refused, never re-dropped.
- **Don't offer the next move.** Name its owner and stop.
