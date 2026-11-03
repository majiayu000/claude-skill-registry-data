---
name: nemawashi-unpick
description: |
  Un-pick the active 根回し Nemawashi idea, leaving the project with no idea active. The **PM**'s — it
  halts outside a pm session or the pm subagent. Un-picking moves the
  seed itself — root → `unpicked/`, rejoining the candidate pool — and leaves the root **empty**. No other
  candidate moves; the pool's shape is otherwise unaffected. The checklist is left exactly as it is, ticks
  and all, so the route survives intact for a re-pick. The seed's line leaves the Principal PM's
  `## Picked seeds` in the same commit. It un-picks one; it picks none. Project-level
  only — this skill serves project journeys; the instance seedbed's pick is made and undone by hand.
  Use when: the active idea is being paused, deprioritised, blocked, or superseded for now — including to clear the
  slot for different work — and it should stay in the candidate pool.
  Do not use for: an idea that ripened into work — its checklist fully walked, or cut into the seeds
  that will walk it (use nemawashi-retire — that files it in `trail/` and restores nothing), an idea being **killed** — ruled out, superseded for good, or not going to be
  done (use nemawashi-drop — that files it in `drop/`, because the candidate pool is for ideas that may
  still be picked), a 宿場 Shukuba station (use shukuba-park — a station really does move, to
  its own `parked/`), a 飛び石 Tobiishi (use tobiishi-seal), or picking the next idea (nemawashi-pick).
  Trigger phrases: "unpick this idea", "un-pick the active seed", "set this nemawashi down", "no idea
  should be active", "this idea isn't finished but I need the slot", "nemawashi-unpick".
license: MIT
metadata:
  version: "4.3.4"
  category: journey
  risk: safe
  created: "2026-08-03"
---

# Nemawashi Unpick

## Purpose

**Undo a pick.** A 根回し Nemawashi seed becomes active *by election*: a pick lifts it out of `unpicked/`
to the root, alone; no other candidate moves. Un-picking runs that backwards — the seed itself moves back,
root → `unpicked/`, rejoining the pool, and the root is left **empty**.

```
A active:      root = {A}          unpicked = {B, C}
un-pick A:     root = {}           unpicked = {A, B, C}
```

**The seed moves, and that is the whole point.** What made it active was its solitude at the root — an
occupied root names the active idea, an empty root names none — and un-picking ends that the only way it
can: by moving the seed out. Leaving it at the root while touching nothing else would leave the root
occupied, which is exactly the active shape the un-pick exists to end.

**`unpicked/` is the candidate pool, not a parking lot** — `<CORE>/docs/journey_move.md` § The seedbed's
`unpicked/` is the candidate pool owns the invariant: that folder holds any number of seeds at any time,
whether or not an idea is active. Its count is never a function of the pick. That is why this skill's
on-disk operation is the seed's own move — plus its picked line leaving the Principal PM's context — not
a restore of anything else.

**End state is an empty root and a pool one seed larger.** The empty root is unambiguous — a reader
checks the root first, never the pool's contents, to tell whether an idea is active. A half-walked idea
is told apart from a fresh candidate by its **content** — its ticked checklist items — not by which
folder it sits in.

**Un-pick, don't retire, don't drop, don't close, don't seal.** The verbs are kept straight in
`<CORE>/docs/michi_agari.md` § Quick reference. `nemawashi-retire` retires an idea **walked to the end**
— it moves the seed to `trail/` and restores nothing, because that idea is done with. `nemawashi-drop`
drops a **killed** one to `drop/`; an abandoned idea is its case, not `nemawashi-retire`'s, which refuses it. Here the idea is neither — it is coming back.
`shukuba-park` parks a station; `shukuba-retire` closes a reached one; `tobiishi-seal` seals a change unit.

**It un-picks one; it picks none.** Choosing the next active idea is the PM's own call
(`<CORE>/docs/michi_agari.md` § "How we work", step 1) and is out of scope. This skill leaves the pool
open and stops.

**Project-level only.** The instance seedbed does have a pick, per `<CORE>/docs/journey_move.md` § The two
levels, and what exists at each — but it is made and undone **by hand**, not by this skill
(`system/nemawashi/README.md` § "Pick one → see only it"). An invocation pointing at `system/nemawashi/`
stops, saying an instance seed's moves are a hand's. Do not move anything into or out of `unpicked/`
yourself.

**Shared mechanics.** The move itself — how a journey artifact changes folder and how that commit is
built — lives in `<CORE>/docs/journey_move.md`. Read it; this file names the section it is
leaning on at each step rather than restating any of it. The two gates in Step 1 are this skill's own.

## Posture

**PM only.** Run in a `pm:` session or as the `pm` subagent. Invoked from anywhere else, halt at once,
say the posture is wrong, and name the way in. The seat's contract is `<CORE>/roles/loaders/pm_global.md`,
which gives this move to the PM: a seed set down unfinished stays the PM's.

**The gate is the owner's call, 2026-09-17.** Setting an idea down frees the project's slot, and what
occupies that slot is the PM's traverse, so the move belongs to the seat that walks it.

## Input

The invocation names **the seed**: a path to
the file, or enough to identify one (the project and the slug, or the project alone, since a
project's active seed is the single item at its seedbed root). It also carries **the reason** the
seed is set down, which the commit body records. Resolution is
`<CORE>/docs/journey_move.md` § Resolving the target; the journey part here is
`system/projects/<project>/journey/nemawashi/`.

Sitting **alone** at that folder's root is what "active" means, so the shared file's
root-not-a-subfolder condition is the operative one: a file already in `unpicked/` is a candidate with no
pick to undo, a file in `trail/` ripened into work, and a file in `drop/` was killed.

Run by `shukuba-refine` when its route moves free the slot, from the same PM seat. Launched unattended
by `<CORE>/launchers/skill/launcher.sh nemawashi-unpick <project> "<reason>"`, from this skill's
`launcher.md`. There nobody can answer, so a question this skill would ask is the run's report —
`<CORE>/docs/journey_move.md` § *Ask, don't guess*.

## Workflow

### Step 1 — Resolve the seed, and run both gates

Resolve per the shared file, with `<nema>` = `system/projects/<project>/journey/nemawashi`, and add this
skill's own condition: the seed must be **the active one** — the single item at that root (a file, or a
folder holding `seed.md`), excluding `README.md` and the `unpicked/` and `trail/` subfolders. If the root
holds no item, **no idea is active** and there is nothing to un-pick — stop and say so.

If the path resolves to the instance seedbed, stop per *Project-level only* above.

**The reason has to be given.** It is **never composed from the seed** — the checklist says what was
walked, the prose says what was proposed, and neither says why the idea is being set down. If the
invocation carries no reason, **stop and ask for the reason alone**, before anything moves. The commit
body is the only place it survives.

**Gate A — is it actually unfinished?** Read the checklist.

- **Unchecked items remain** — the route is unwalked. This skill is right. Proceed.
- **Every item ticked** — the idea is **finished**, and that is `nemawashi-retire`'s, the Scrum Master's. **Stop and say
  so.** Both skills move the seed off the root — the difference is only where it lands: this skill returns
  it to the candidate pool, `nemawashi-retire` files it in `trail/` — so leaving a finished idea in the
  pool means a later pick re-walks a route already walked.
- **No checklist at all** — a project seed that never grew one. Nothing to gate on; proceed, and say so
  in the report.

**Gate B — is a station still open on this idea?** Check `system/projects/<project>/journey/shukuba/` for
a station file at its root.

If one is there, **stop and ask.** A station is opened *from the active seed's checklist*
(`<CORE>/docs/michi_agari.md` § "How we work", step 2), so an open station with no active idea behind it
is orphaned — it names a leg of a route nobody is walking, and the project reads as having active work
whose idea has been set down. The resolution is an order, not a merge: **`shukuba-park` parks the station
first**, in its own commit, and then this skill runs. Say that when you ask, so the owner can answer
"yes, do both" rather than having to work out the sequence.

An empty station slot — including one `shukuba-park` just emptied — passes this gate silently.

### Step 2 — Move the seed to the candidate pool

Per `<CORE>/docs/journey_move.md` § The pick and the un-pick. **This is the operation** — everything else in
this skill is a gate, a correction, or the commit.

Un-picking ends the active idea by moving the seed itself, root → `unpicked/`. No other item moves — the
candidate pool's shape is otherwise unchanged; it gains exactly this one seed.

```bash
git mv "<nema>/<seed>.md" "<nema>/unpicked/<seed>.md"
```

**A folder-seed moves the same way, whole:** `git mv "<nema>/<seed>" "<nema>/unpicked/<seed>"` — one
`git mv` of the folder carries `seed.md` and every `<unit-key>_report.md` /
`<unit-key>_recommendations.md` inside it.

**This step runs before Step 3, unconditionally** — see the ordering rule there.

**Then take the seed's line out of the Principal PM's context.** Per `<CORE>/docs/journey_move.md` § *The
Principal PM's picked seeds*: delete the line naming `<project> · nemawashi · <seed>` from
`## Picked seeds` in `system/contexts/CONTEXT_PPM.md`, and nothing else. No file, section or line
means nothing to remove.

### Step 3 — Make the seed honest where it stands

Per `<CORE>/docs/journey_move.md` § Move whole — and the one edit that is allowed. This is the only place the
seed's content changes, and a seed is the artifact most likely to need it: being picked is something that
happened *to it*, and a seed records it — a line reading "Picked active <date>", a status header, a
"currently walking" note. Those claims are false the moment the idea stops being active. For a
folder-seed the currency marker lives in `seed.md`, and that is the one file this step ever edits.

Correct exactly those claims of present state, and nothing else:

- **Do** correct a picked/active/current marker so it records what is now true — picked on its date,
  un-picked on this one, back in the candidate pool.
- **Do not** touch forward-looking prose. A seed is written in anticipation ("when this is picked, the
  first station will…"), which reads correctly for a candidate again.
- **Do not** touch the checklist — see Step 4.
- **Do not** add a set-down note, a reason, or a summary. The reason is the commit body's.

If the seed makes no claim about its own currency, nothing is edited, and that is the correct outcome
rather than a missed step.

**Move first, then edit — Step 2 before Step 3, always.** The shared file warns that `git mv` stages a
rename against a file's **old committed content**, so an edit made *before* the move is staged nowhere
and is dropped from the commit silently. This skill both moves the seed (Step 2) and may edit it (Step 3)
— exactly the shape the hazard describes, now that the seed is no longer left untouched at the root. Run
Step 2 first, unconditionally; only then correct the seed's currency marker at its new path in
`unpicked/`.

### Step 4 — Leave the checklist exactly as it is

Every item keeps its current mark. Unchecked items stay `[ ]`; items ticked by stations already closed
stay `[x]`, because those stations really were reached and their record in `shukuba/trail/` says so.

Nothing is added: no parked marker, no "set down here" line, no pointer. The checklist **is** the idea's
route, and it has to survive intact for a re-pick to mean anything — it is also the only thing that
distinguishes this half-walked idea from a fresh candidate, now that the layout does not. A marker on an
unchecked item risks a later reader treating it as handled, which is the failure un-picking exists to
avoid. Appending to a checklist line is also the bloat the shared file forbids.

### Step 5 — Commit, then report

One commit carries the seed's rename, its content correction only if Step 3 found something, and its
picked line's removal only if Step 2 found one. Per
`<CORE>/docs/journey_move.md` § The commit:

```bash
python3 "<CORE>/tools/commit_builder.py" --repo . commit \
  --staged "<nema>/<seed>.md" "<nema>/unpicked/<seed>.md" \
  --add "<nema>/unpicked/<seed>.md" system/contexts/CONTEXT_PPM.md \
  --subject "unpick nemawashi: <slug> — seed returned to the candidate pool, root empty" \
  --body "$(cat <file>)" \
  --actor pm \
  --directional "<directional>" \
  --surface "Claude Code" --co-authored-by "<your model> <noreply@anthropic.com>"
```

- The `--staged` list names **both halves of the seed's move**: its old path and its new path in
  `unpicked/`. **A folder-seed names two paths per file it holds** — the old and the new path of each —
  rather than the folder prefix. The `--add` names the seed at its **new** path (`seed.md` inside the
  folder, for a folder-seed), dropped when Step 3 changed nothing, and
  `system/contexts/CONTEXT_PPM.md`, dropped when Step 2 removed no line.
- **The body is the reason the seed is set down**, as the invocation gave it, and goes through a file
  per `<CORE>/doctrine/governance/commit_via_builder.md` § The call. It is never composed from the seed.
- **The directional is `aside:`.** Un-picking does not advance the product. Gate B has already required
  the station slot to be empty, so it resolves past `Shukuba:` to **`Agari: <project> — aside: …`**
  against `system/projects/<project>/agari.md`. Never `Shukuba: none`.
- **The seed's move is always the commit.** The seed itself always moves when this skill completes —
  there is no path where Step 2 runs and nothing is committed.

Then check `git show --stat` per the shared file. Expect rename(s) — one for a file-seed, one per file
the folder held for a folder-seed — content in `seed.md` only if Step 3 corrected it, and one deleted
line in `system/contexts/CONTEXT_PPM.md` only if Step 2 removed one.

**Report** plainly: which seed was un-picked, why it was set down rather than retired, how many unchecked
items its checklist still carries, whether a currency marker was corrected, and whether its line left
`## Picked seeds` or there was none. Then name the state the
project is in: **the root is empty, the candidate pool holds N seeds including this one, and none has
been picked.** Picking the next one is the PM's move, not this one's.

---

## Outputs

| File / effect | Produced when |
|---|---|
| The seed (a file, or a folder holding `seed.md`) moved whole `nemawashi/<seed>` → `nemawashi/unpicked/<seed>`, one commit | Success (Step 2) |
| A currency-marker correction inside the seed at its new path, same commit | Step 3 found a falsified self-description |
| The seed's line deleted from `## Picked seeds` in `system/contexts/CONTEXT_PPM.md`, same commit | Step 2 found the line |
| No change; a halt saying the posture is wrong | Invoked outside the PM seat (§ Posture) |
| No change; a pointer to `nemawashi-retire` | The checklist is fully walked (Gate A) |
| No change; a question naming the open station and the order | A station is still open on this idea (Gate B) |
| No change; a question naming what was found | Ambiguous / not-found / not-active seed (Step 1) |
| No change; a question asking for the reason alone | The invocation carries no reason (Step 1) |

The seed moves exactly once on every completed run; no other candidate ever moves; the checklist is never
modified; and no idea is ever picked, in any path.

---

## Critical Rules

- **The PM's, and it halts elsewhere.** A seat that is not the PM names the un-pick as owed and hands
  it to the PM rather than running it.
- **The reason is given, never composed.** It is the commit body. With no reason in the invocation,
  ask for it alone before anything moves.
- **The seed moves; nothing else does.** Root → `unpicked/`, rejoining the candidate pool. No other
  candidate is touched, and the pool's existing contents are unaffected. The one other edit is the
  seed's own line leaving the Principal PM's `## Picked seeds`.
- **Verify unfinished; don't assume it.** A fully-ticked checklist means the retire. Gate A is
  checked, and a finished idea stops the run.
- **Never orphan an open station.** Gate B stops when a station is still open on this idea. The fix is an
  order — `shukuba-park` first, its own commit, then this — never a bundled move and never a silent one.
- **Leave the checklist intact.** Unchecked stays `[ ]`, ticked stays `[x]`, nothing is added to any line.
  With the layout no longer distinguishing a half-walked idea from a fresh candidate, the checklist is the
  only thing that does.
- **Un-pick, don't pick.** The root ends up empty. Do not pick a replacement, do not leave a candidate
  specially placed, do not rank them. Picking is the PM's call.
- **Project-level only.** The instance seedbed's pick is undone by hand, not by this skill. Stop and say
  so rather than touching `system/nemawashi/unpicked/` yourself.
- **One fact, one commit.** The idea's un-pick is one commit. A station's parking is `shukuba-park`'s
  own. Never bundle them: they carry different scopes, and a bundled commit cannot be reverted in pieces.
- **Move first, then edit.** Step 2's `git mv` runs before Step 3's correction, always — reversing the
  order silently drops the content edit from the commit.
- **The shared mechanic is shared.** Everything about *how* the move and its commit are made lives in
  `<CORE>/docs/journey_move.md`. Read it there; a second copy is a copy free to drift.
