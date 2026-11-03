---
name: nemawashi-retire
description: |
  Scrum Master-posture skill that retires a project's walked 根回し Nemawashi seed — halts outside a
  scrum-master session or the scrum-master subagent.
  Mechanical: it gates, moves and commits, and decides nothing. It checks that the seed sits at the
  project's seedbed root, that every item of its checklist is ticked, and that no station and no change
  unit is left open; then it moves the seed whole into `nemawashi/trail/` and deletes the seed's line
  from `## Picked seeds` in `system/contexts/CONTEXT_PPM.md`, in one commit. It writes no report file and
  makes no judgment about the seed's folder or the seedbed; it says what it did and names the
  Principal PM's nemawashi-refine as owed.
  Park-don't-strike: the seed is relocated, never struck through.
  Project level only. An instance seed under `system/nemawashi/` is retired by hand.
  Use when: a project seed's checklist is fully walked — typically right after shukuba-retire ticked
  its last item — and you want it filed in `trail/`.
  Do not use for: an idea being **killed** (use nemawashi-drop), an idea set down to be **picked up
  again** (use nemawashi-unpick), a 宿場 Shukuba station (use shukuba-retire), a 飛び石 Tobiishi
  (use tobiishi-seal), answering the retired seed's recommendations or re-reading the pool (use
  nemawashi-refine, the Principal PM's), picking the next seed (use nemawashi-pick), or an instance
  seed (by hand).
  Trigger phrases: "retire the seed", "retire this nemawashi", "the seed is walked", "file the seed in
  trail", "nemawashi-retire". Not "this idea is dead" / "drop this seed" — those are nemawashi-drop's.
license: MIT
metadata:
  version: "1.1.3"
  category: journey
  risk: safe
  created: "2026-09-24"
---

# Nemawashi Retire

## Purpose

**File a walked seed in `trail/`, and nothing else.** A project's 根回し Nemawashi seed is walked when
every item of its checklist is ticked. This skill proves that, proves nothing is left open under it,
and moves it. It reads no recommendation in the seed's folder, re-reads no candidate in `unpicked/`,
and names two next moves — the Principal PM's `nemawashi-refine`, which does both, and the PM's pick
after it — **it makes no judgment**, so it runs unattended.

**Retire, don't close, don't seal, don't drop.** The verbs are `<CORE>/docs/michi_agari.md`
§ Quick reference's. `trail/` is the record of ideas that were walked; a killed idea goes to
`nemawashi-drop`, one that will come back to `nemawashi-unpick`.

**Shared mechanics.** How a journey artifact changes folder, how its commit is built, and the
`## Picked seeds` line are `<CORE>/docs/journey_move.md`. This file names the
section it leans on at each step rather than restating it.

## Posture

**Scrum Master only.** Run in a `scrum-master:` session or as the `scrum-master` subagent — the skill
launcher starts it as the latter (`launcher.md`). Invoked from anywhere else, halt at once, say the
posture is wrong, and name the way in. The seat's contract is
`<CORE>/roles/loaders/scrum_master_global.md`. The gate is there because the run moves and commits with
nobody answering — `<CORE>/doctrine/setup/authoring_layers.md` § *A skill that acts unattended gates to
its seat*.

## Input

**The project.** The seed is the single active item at `system/projects/<project>/journey/nemawashi/`'s
root; an invocation may also name its slug. Resolution is `<CORE>/docs/journey_move.md` § *Resolving the
target*, with `<nema>` = that folder. A candidate in `unpicked/` is refused — it was never picked, so
it was never walked.

**Project level only.** Anything under `system/nemawashi/` is refused — say an instance seed is retired
by hand (`<CORE>/docs/journey_move.md` § *The two levels, and what exists at each*) and stop.

## Workflow

### Step 1 — Gate the posture, then resolve the seed

Check the posture (§ *Posture*) and halt there rather than proceeding. Refuse an instance seed.
Resolve per the shared file: exactly one item at `<nema>`'s root, excluding `README.md` and the
`unpicked/`, `trail/` and `drop/` subfolders — a file `<slug>.md`, or a folder `<slug>/` holding
`seed.md`. For a folder-seed every read below lands in `seed.md`. None, or more than one → stop and
name what you found.

### Step 2 — Prove the checklist is walked

**Count on the whole line, not on a line start** — a nested item is indented, and `^- \[x\]` misses it.

```bash
grep -cE '^[[:space:]]*- \[x\]' "<seed>"   # ticked
grep -nE '^[[:space:]]*- \[ \]' "<seed>"   # open, with line numbers
```

| The count says | Then |
|---|---|
| At least one ticked, none open | Walked — proceed |
| Open items remain | **Halt**, quoting each open item. Resolving them, `nemawashi-drop` (killed) and `nemawashi-unpick` (coming back) are other runs' |
| No checklist at all | **Halt**, saying the seed carries no checklist, so this run cannot prove it walked. Whether it was walked or killed is not a count; whoever knows re-invokes this skill saying it was walked, or runs `nemawashi-drop` |

A re-invocation that states the no-checklist seed was walked proceeds — the statement is the caller's,
and this run records it in the commit body. **Never infer it.** A launched run has nobody to say it, so
it halts with the reason in its log.

### Step 3 — Prove nothing open would be stranded

`<journey>` is `<nema>`'s parent:

```bash
ls "<journey>/shukuba/"    # a station .md at the root is open; trail/ and parked/ are not stations
ls "<journey>/tobiishi/"   # a change-unit folder at the root is open; trail/ and drop/ are not
```

An open station or change unit halts the run, named; closing it is `shukuba-retire`'s or
`tobiishi-seal`'s, setting it down `shukuba-park`'s or `tobiishi-drop`'s. No open station also fixes
the directional in Step 5: `Agari:`, never `Shukuba:`.

### Step 4 — Move the seed and remove its picked line

```bash
mkdir -p "<nema>/trail"
git mv "<nema>/<slug>" "<nema>/trail/<slug>"          # folder-seed
git mv "<nema>/<slug>.md" "<nema>/trail/<slug>.md"    # file-seed
```

Per `<CORE>/docs/journey_move.md` § *Ensure the destination exists* and § *Move whole — and the one edit
that is allowed*. The seed moves whole, with one exception: where `seed.md` (or the file-seed) states
its own present state — *picked*, *active*, *being walked* — the move has just made that false, so
correct that statement and nothing else, **after** the `git mv`, at the new path. A seed that makes no
such claim moves with no content change.

Then delete the line naming `<project> · nemawashi · <slug>` from `## Picked seeds` in
`system/contexts/CONTEXT_PPM.md`, and nothing else — `<CORE>/docs/journey_move.md` § *The Principal PM's
picked seeds*. No line there → nothing to remove, and say so in Step 6.

### Step 5 — Commit, in one commit

Per `<CORE>/docs/journey_move.md` § *The commit*: the rename declared with `--staged` naming both halves
(for a folder-seed, the old and new path of every file it holds), `--add` for the context file only
when a line was removed, `--add` for the seed's new path only when Step 4 corrected it, no `--skill`.

```bash
python3 "<CORE>/tools/commit_builder.py" --repo . commit \
  --staged "<nema>/<slug>.md" "<nema>/trail/<slug>.md" \
  --add system/contexts/CONTEXT_PPM.md \
  --subject "retire: nemawashi/<slug> → trail/" \
  --actor scrum-master \
  --directional "Agari: <project> — progress: <the seed's idea>, walked, retired to trail" \
  --surface "Claude Code" --co-authored-by "<your model> <noreply@anthropic.com>"
```

A caller with no posture — which Step 1 already refused — never reaches here, so `--actor scrum-master`
is the only identity. Then eyeball `git show --stat`: renames, plus one deleted line in
`CONTEXT_PPM.md` when one was removed, and content on the seed only when Step 4 corrected it.

### Step 6 — Check the pointers, then report

Run `python3 "<CORE>/tools/check_journey_links.py" --repo .` and handle what it names per
`<CORE>/docs/journey_move.md` § *After the move, say which pointers it broke* — it never undoes the move.

State plainly: which seed moved to `trail/`, whether its line left `## Picked seeds`, and what the
pointer check named. Then say the seedbed root is empty, so **the retired seed is owed to the
Principal PM** — `<CORE>/launchers/skill/launcher.sh nemawashi-refine <project> <seed>`
(`<CORE>/roles/loaders/principal_pm_global.md` § *Retiring a finished seed*) — and the pick to the PM
after it. Naming them is the whole hand-off: this run does not answer the seed, pick, offer to, or
read the pool.

---

## Outputs

| File / effect | Produced when |
|---|---|
| The seed moved whole to `nemawashi/trail/` — a falsified present-state claim corrected, if it has one — and its `## Picked seeds` line deleted, in one commit | Success (Steps 4–5) |
| The same move, with no context edit | Success, when no picked line was there |
| A stated summary (no file) naming the move, the line, the pointer check, the refine owed and the pick after it | Always on success (Step 6) |
| No change; a halt saying the posture is wrong | Invoked outside the Scrum Master seat (Step 1) |
| No change; a refusal naming the hand move | An instance seed (Step 1) |
| No change; a halt naming what was found | No seed, more than one, or a candidate in `unpicked/` (Step 1) |
| No change; a halt quoting the open items | The checklist is not fully walked (Step 2) |
| No change; a halt saying the seed has no checklist | No checklist and no caller statement that it was walked (Step 2) |
| No change; a halt naming what is open | A station or a change unit is still open (Step 3) |

---

## Critical Rules

- **The Scrum Master's, and it halts elsewhere.** The run moves and commits unattended.
- **Project level only.** An instance seed is retired by hand.
- **Mechanical.** No report file, no reading of the seed's folder for asks, no keep-or-drop over the pool,
  no next move beyond naming the refine owed and the pick after it. Anything that needs a judgment is
  `nemawashi-refine`'s.
- **`trail/` only for a seed walked to the end.** An open item halts the run; a killed seed is
  `nemawashi-drop`'s, a paused one `nemawashi-unpick`'s. Filing either in `trail/` claims a walk that
  did not happen.
- **Never strand live work.** An open station or change unit halts the run.
- **One fact, one commit.** The move and the picked line's removal are one commit, the only one this
  skill makes. The seed's content is never edited, except a present-state claim the move falsified
  (Step 4).
- **The shared mechanic is shared.** *How* the move is made is
  `<CORE>/docs/journey_move.md`. A second copy is a copy free to drift.
