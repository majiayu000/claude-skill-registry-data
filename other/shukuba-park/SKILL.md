---
name: shukuba-park
description: |
  Park an unreached 宿場 Shukuba station and free the slot. Moves the station file into the sibling
  `shukuba/parked/`, where it waits until someone opens it again, and leaves the 根回し Nemawashi seed's
  checklist item **unticked**. The **PM**'s — it halts outside a pm session or the pm subagent. Asks
  nothing — the freed slot is shukuba-open's and the idea's un-pick is nemawashi-unpick's — so it runs
  unattended.
  Park-don't-strike: the station is relocated, never struck through, never marked done-in-place.
  Project-level only. The instance's `system/shukuba/` is a router station with one destination,
  `trail/`, and no `parked/` at all.
  Use when: a station is being set down before its reached-when is met — the work is paused, deprioritised,
  blocked, or superseded, or the slot is wanted for different work — and it should stay available to take
  up again.
  Do not use for: a station whose reached-when **is** met (use shukuba-retire — that closes it to `trail/`
  and ticks the seed), the idea behind it (use nemawashi-unpick — that moves the seed itself to
  `unpicked/` and leaves the root empty), an unsealed 飛び石 Tobiishi being set down (use tobiishi-drop — that moves it to
  `tobiishi/drop/`), a finished one (use tobiishi-seal), or an instance-level item
  under `system/` (the instance router has no `parked/` to move a station into).
  Trigger phrases: "park the station", "park this shukuba", "set this station down", "shelve the station",
  "the station isn't reached but I need the slot", "shukuba-park".
license: MIT
metadata:
  version: "3.6.0"
  category: journey
  risk: safe
  created: "2026-08-03"
---

# Shukuba Park

## Purpose

**Set down a station that was not reached, without claiming it was.** A 宿場 Shukuba is one leg of the
active 根回し Nemawashi idea's route, and exactly one is active at a time. Sometimes that leg is stopped
part-way — blocked, deprioritised, superseded, or simply not the work the slot is wanted for now. The
station has to leave the slot, but nothing about it is finished.

**`parked/` is where it goes, and `trail/` would be wrong.** Each project's `journey/shukuba/README.md`
(stamped from `<CORE>/templates/journey_shukuba_template.md`) reserves the trail for **reached**
stations — it is the record of stations whose reached-when was met. Filing an unreached station there
makes that record claim a walk that never happened, and because the record is read by looking at which
folder things are in, a note inside the file does not correct it. `parked/` says the opposite and says it
by name: this one is waiting.

**Park, don't close, don't retire, don't seal.** The verbs are kept straight in
`<CORE>/docs/michi_agari.md` § Quick reference. This skill parks a station. `shukuba-retire` closes a
reached one; `nemawashi-unpick` un-picks the idea; `nemawashi-retire` retires a finished idea;
`tobiishi-seal` seals a change unit.

**The seed's checklist item is not touched.** This is the whole reason parking is its own operation
rather than a flag on the close — see *Leave the item unticked* in Critical Rules.

**Project-level only** — the instance's `system/shukuba/` is a router station, per `<CORE>/docs/journey_move.md`
§ The two levels, and what exists at each: it has one destination, `trail/`, and **no `parked/` at all**
(`system/shukuba/README.md` § Lifecycle). There is no slot to free and nowhere to park it into. An
invocation pointing anywhere under `system/` that is not `system/projects/<project>/journey/shukuba/`
stops with `nemawashi-unpick` named for a project seed, and the Michi named as the instance's only
direction.

**Shared mechanics.** The move itself — how a journey artifact changes folder, and how that commit is
built — lives in `<CORE>/docs/journey_move.md`. Read it; this file names the section it is
leaning on at each step rather than restating any of it.

## Posture

**PM only.** Run in a `pm:` session or as the `pm` subagent. Invoked from anywhere else, halt at once,
say the posture is wrong, and name the way in. The seat's contract is `<CORE>/roles/loaders/pm_global.md`,
which gives this move to the PM: a station set down unreached frees the slot the PM's traverse fills,
the same reason `nemawashi-unpick` is the PM's — the owner's call, 2026-10-03.

## Input

The invocation names **the station**: a path to the
file, or enough to identify one (the project and the slug). Resolution is
`<CORE>/docs/journey_move.md` § Resolving the target; the journey part here is
`system/projects/<project>/journey/shukuba/`.

Run by `shukuba-refine` as one of its moves. `shukuba-retire`, which is the Scrum Master's, names it as
owed when the station it was asked to close is not actually reached — it does not run it.

## Workflow

### Step 1 — Resolve the station, and confirm it is genuinely unreached

Resolve per the shared file, with `<shukuba>` = `system/projects/<project>/journey/shukuba`. If it
resolves to an instance-level item instead, stop per *Project-level only* above.

**Then read the station's reached-when and check it against the world.** This is the gate that decides
which skill the caller wants, and it is checked rather than assumed.

**Where a check runs.** When checking the world means running the product's own checks — a test
suite, a harness, a script under the product's `checks/` — run them in a disposable copy of the
product — a fresh clone at the commit under test (`git clone --quiet <repo> <scratch> && git -C <scratch> checkout --quiet <sha>`), never `git archive`,
which drops the history a product's checks may read — never in the product's main checkout, and
leave that checkout as you found it. Run the checks from a subshell, never `cd` your own shell into the
copy, and remove the copy when you have read the result, in a command of its own run from outside it
(`<CORE>/roles/CROSS_ROLE.md` § *Every seat — a run leaves the product's main checkout as it found
it*). A chain halts the step that leaves it dirtier.

The two outcomes:

- **Not met** — any part of the reached-when is unsatisfied. This skill is right. Proceed.
- **Met** — the station was reached, so it is closed, not parked. **Run `shukuba-retire` on it, as the
  PM**, and stop: that skill moves it to `trail/`, ticks its item and commits, and this skill parks
  nothing. The boy-scout rule — the station is already in your hands, so the close is not left owed
  (`shukuba-retire` § Posture states this as its one exception for the PM — the owner's call, 2026-10-03). Parking a reached station loses the record of a completed walk just as surely as filing an
  unreached one in `trail/` fabricates one; the error simply points the other way.
- **Cannot be told from the files** — the reached-when turns on something you cannot observe. **Stop and
  report**: park nothing, and name the part of the reached-when you could not judge and why. Do not
  ask — the run may have nobody to answer — and do not infer it from how much of the station "looks
  done."

A station may also be parked while *technically* reachable — the owner simply wants the slot for other
work. That is a legitimate park and needs no special handling, but say plainly in the report that the
reached-when was not met, so nobody later reads the parked file as unfinished-and-blocked when it was
unfinished-and-deprioritised.

### Step 2 — Ensure `parked/` exists

```bash
mkdir -p "<shukuba>/parked"
```

Per `<CORE>/docs/journey_move.md` § Ensure the destination exists.

### Step 3 — Move the station into `parked/`

```bash
git mv "<shukuba>/<YYYY-MM-DD>_<slug>.md" "<shukuba>/parked/<YYYY-MM-DD>_<slug>.md"
```

### Step 4 — Make the file honest where it sits

Per `<CORE>/docs/journey_move.md` § Move whole — and the one edit that is allowed. Applied here: a station
usually describes the work rather than its own currency, so **most stations move whole with no content
change at all**, and that is the expected outcome — not a step you skipped.

Correct only a claim of present currency the move just falsified — a header saying the station is
*active*, *current*, or *being walked now*. A partly-walked station's own notes about progress are
**not** such a claim; they are a true record of what was done and they are what makes the file worth
taking up again. Leave them, and leave the reached-when exactly as written — a station taken up again is
walked against the same bar it was opened against.

Add nothing: no set-down note, no reason, no pointer. The reason is the commit body's.

**Order matters** — the move is Step 3 and the edit is Step 4, not the reverse, per *Move first, then
edit* in the shared file.

### Step 5 — Leave the Nemawashi alone

The station was opened from one unchecked item on the active seed's checklist. That item **stays
`[ ]`**, and the seed file is **not opened, not edited, and not part of this commit**.

This is the structural difference from `shukuba-retire`, which ticks it — and the reason parking could
not be a flag on that skill. A tick says the item is walked. It is not. And the cost is asymmetric: a
wrongly-ticked item means no station is ever opened from it again, the work reads done, and nothing
anywhere records that it was not walked. There is no cheap way back from that, whereas an item left
unticked simply remains what it is — the next thing to take up.

No parked-marker is added to the line either. `[ ]` is already the true statement about that item, and
the parked station is self-describing where it sits: it names the seed item it came from, so the record
is complete without touching the seed. Appending anything to a checklist line is also the bloat the
shared file forbids.

### Step 6 — Commit

One commit, carrying the station's rename and — only if Step 4 found something — its content
correction. Per `<CORE>/docs/journey_move.md` § The commit:

```bash
python3 "<CORE>/tools/commit_builder.py" --repo . commit \
  --staged "<shukuba>/<YYYY-MM-DD>_<slug>.md" "<shukuba>/parked/<YYYY-MM-DD>_<slug>.md" \
  --add "<shukuba>/parked/<YYYY-MM-DD>_<slug>.md" \
  --subject "park shukuba: <YYYY-MM-DD>_<slug> → parked/, unreached" \
  <--actor pm as the pm subagent | --role PM from a pm: session> \
  --directional "Shukuba: <YYYY-MM-DD>_<slug> — aside: <why it is being parked>" \
  --surface "Claude Code" --co-authored-by "<your model> <noreply@anthropic.com>"
```

The shared file owns the identity flag, the `--add`-only-if-you-edited rule (Step 4 changes nothing in the common
case, and then `--staged` alone carries the commit), no-`--skill`, and the `aside:` reading for a
set-down. What is specific here: the directional is always a **`Shukuba:`** line, resolved against the
station being parked — a station is open by definition, so it never degrades to `Agari:`.

Then check `git show --stat` per the shared file. Expect a rename, and content only if Step 4 made a
correction.

### Step 7 — Report

State plainly: which station moved to `parked/`, that its reached-when was **not** met and which part
was outstanding, whether any content correction was made, and — explicitly — that **the seed's checklist
item is still unticked**, that the seed is still the active idea, and that the station slot is now
**empty**.

The empty slot is the journey standing still on purpose. Say so, so the caller knows that is the state
they are in rather than discovering it later. Say it and stop: what to put in the slot, and whether the
idea is set down too, are the owner's — see Critical Rules.

---

## Outputs

| File / effect | Produced when |
|---|---|
| `shukuba/<YYYY-MM-DD>_<slug>.md` moved to `shukuba/parked/<YYYY-MM-DD>_<slug>.md`, one commit | Success (Steps 3–6) |
| A currency-marker correction inside the moved file, same commit | Step 4 found a falsified self-description |
| Nothing parked; the station closed through `shukuba-retire`, in that skill's own commit | The reached-when **is** met (Step 1) |
| No change; a question naming the candidates | Ambiguous / not-found station (Step 1) |
| No change; a report naming the part of the reached-when that could not be judged | An unresolvable reached-when (Step 1) |
| No change; a halt saying the posture is wrong | Invoked outside the PM seat (§ Posture) |

The seed's checklist is never modified by this skill, in any path.

---

## Critical Rules

- **The PM's, and it halts elsewhere.** A seat that is not the PM names the park as owed and hands it
  to the PM rather than running it.
- **`parked/`, never `trail/`.** The trail records **reached** stations. An unreached station filed there
  fabricates a completed walk, and no note inside the file corrects it.
- **Verify unreached; don't assume it.** A reached station belongs to `shukuba-retire`, which this
  skill runs on it rather than leaving the close owed. Check the
  reached-when against the world in Step 1 and stop if it is met — the mirror-image error is just as
  destructive. Where the files cannot tell, stop and report; never ask, never guess.
- **Leave the item unticked.** The seed is not opened, not edited, not committed. No tick, no parked
  marker, no appended note. A wrong tick buries a station's worth of work with no trace and no cheap way
  back; `[ ]` is already true.
- **Project-level only.** The instance Shukuba is a router with one destination, `trail/`, and no
  `parked/`. An instance-level invocation stops with a pointer to `nemawashi-unpick` and the Michi —
  never a fabricated instance station.
- **Preserve the reached-when verbatim.** A parked station is taken up again against the bar it was
  opened against. Rewriting or relaxing it while parking silently changes what "reached" will mean.
- **One fact, one commit.** The station's parking is one commit, and it is the only one this skill
  makes. The idea's un-pick is `nemawashi-unpick`'s own. Never bundle them: they carry different scopes,
  and a bundled commit cannot be reverted in pieces.
- **Don't offer the next move.** Not the freed slot's next occupant, and not un-picking the idea. The
  next occupant is not even derivable here — the parked item is still the next unchecked one, so an
  offer would propose re-opening the station just parked, which `shukuba-open` takes up again as it is;
  opening something *different* changes the route first, and the route is the PM's
  (`<CORE>/roles/loaders/pm_global.md` § *What you own*, item 2). Whether
  the idea is set down too is the owner's call in the PM loop, and `nemawashi-unpick` is the PM's to run.
  An offer here is a second copy of a decided fact, and an interactive gate in a skill that must run
  inside `shukuba-refine`'s unattended moves with nobody in the room.
- **The shared mechanic is shared.** Everything about *how* the move and its commit are made lives in
  `<CORE>/docs/journey_move.md`. Read it there; a second copy is a copy free to drift.
