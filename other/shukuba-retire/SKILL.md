---
name: shukuba-retire
description: |
  Scrum Master-posture skill that closes a reached 宿場 Shukuba station — halts outside a scrum-master
  session or the scrum-master subagent, with one exception: shukuba-park, run by the PM, closes a
  station it finds already reached through this skill.
  Close a reached 宿場 Shukuba station. Moves the station file whole into the sibling `shukuba/trail/`,
  ticks the item it was opened from on the active 根回し Nemawashi seed (`[ ]` → `[x]`), commits both in
  one commit, and reports whether unchecked items remain. Asks nothing — the next station is shukuba-open's
  and the seed's retire is nemawashi-retire's — so it runs unattended. Where the item it ticked was the
  last one, it says that retire is owed, and does nothing further.
  Park-don't-strike: the station is relocated, never struck through, never marked done-in-place.
  Project-level only. The instance router station under `system/shukuba/` is never walked — its
  cross-project reached-when is met in the contributing projects' own journeys, no seed checklist item
  stands behind it to tick, and its file moves to `trail/` by hand.
  Use when: a station's reached-when is met and you want it closed.
  Do not use for: a station being set down **unreached** (use shukuba-park — that moves it to `parked/`
  and leaves the seed's item unticked), a 飛び石 Tobiishi (use tobiishi-seal — that seals +
  merges), a finished 根回し Nemawashi idea (use nemawashi-retire), or the instance router station under
  `system/shukuba/` (never walked — no seed item to tick; its file moves to `trail/` by hand).
  Trigger phrases: "close this shukuba", "retire this station", "the station is reached", "shukuba-retire".
license: MIT
metadata:
  version: "2.13.0"
  category: journey
  risk: safe
  created: "2026-07-30"
---

# Shukuba Retire

## Purpose

**Close a reached station, and say where that leaves the journey.** A 宿場 Shukuba is one leg of the
active 根回し Nemawashi idea's route; when its reached-when is met, two things are true at once — the
station is finished, and the seed's checklist item it came from is done. This skill does both: the
archive move and the tick. A third thing is true and is only *reported* — the journey is now standing at
the next item, or at none.

**What comes next is not this skill's.** Which station opens next, whether it is walked, and whether the
idea retires are the owner's calls in the loop — `<CORE>/docs/michi_agari.md` § *How we work*, step 4,
and `<CORE>/roles/loaders/pm_global.md` §§ *Responsibilities* 6-8 and *Hand-off triggers*. The
station-open in particular is its own move, made by `shukuba-open` (`pm_global.md` § *Skills toolbox
(reminder)*). A close that asked those questions
stated a second copy of a fact that already has an owner, and made the skill unusable from any caller
with nobody in the room.

**Close, don't seal, don't retire the idea.** The verbs are kept straight in
`<CORE>/docs/michi_agari.md` § Quick reference: you **seal** a 飛び石 Tobiishi, **close** a station, and
**retire** a finished idea. This skill closes. `tobiishi-seal` seals; `nemawashi-retire` retires.

**`trail/` is the record of stations reached** — and only of those. A station being set down *unreached*
is a different operation with a different destination: `shukuba-park`, which moves it to
`shukuba/parked/` and leaves the seed's item unticked. See Step 1's gate.

**Project-level only** — the instance has its own 宿場 Shukuba (`system/shukuba/`), but it is a **router**,
not a walked station, per `<CORE>/docs/journey_move.md` § The two levels: it coordinates several projects
pushing on one shared thing and is never crossed by Tobiishi. Its cross-project reached-when is met when
every contributing project has reached its own station on the shared thing, which is not this skill's to
verify, and no Nemawashi checklist item stands behind it to tick. Its file is moved to `trail/` by
hand, not by this skill (`system/shukuba/README.md` § Lifecycle). An invocation pointing anywhere under
`system/` that is not `system/projects/<project>/journey/shukuba/` stops, saying an instance seed's moves are
made by hand, and names the Michi as the instance's only direction.

**Shared mechanics.** The move itself — how a journey artifact changes folder, and how that commit is
built — lives in `<CORE>/docs/journey_move.md`. Read it; this file names the section it is
leaning on at each step rather than restating any of it. The tick in Step 4 is this skill's own.

## Posture

**Scrum Master only.** Run in a `scrum-master:` session or as the `scrum-master` subagent. Invoked from
anywhere else, halt at once, say the posture is wrong, and name the way in. The seat's contract is
`<CORE>/roles/loaders/scrum_master_global.md`. The gate is there because the run moves, ticks and commits
with nobody answering — `<CORE>/doctrine/setup/authoring_layers.md` § *A skill that acts unattended gates
to its seat*.

**One exception: the PM, from inside its own park.** When `shukuba-park`, running in the PM seat, finds
the station it was asked to set down already reached, it closes the station through this skill rather
than leaving the close owed — the boy-scout rule, applied to a station already in the PM's hands — the owner's call, 2026-10-03.
That is the only way in for the PM. A `pm:` session or `pm` subagent invoking this skill directly, or any
other PM skill, halts like every other seat. The Scrum Master still owns the close; the exception
removes a hand-off, not the seat.

## Input

The invocation names **the project**, and may name **the station**: its dated stem
(`<YYYY-MM-DD>_<slug>`), or a path to the file. With no station named, the close acts on the one
station at the project's shukuba root — a root holds one at most. The journey part here is
`system/projects/<project>/journey/shukuba/`.

## Workflow

### Step 1 — Resolve the station and confirm it's closable

Run everything from the instance root.
`RETIRE=<CORE>/../skills/scrum-master/.claude/skills/shukuba-retire/scripts/retire.py`.

```bash
python3 "$RETIRE" --root . --project <project> resolve [--station <YYYY-MM-DD>_<slug>]
```

Pass `--station` when the invocation names one — for a path, its file name. The script prints the
station's path from the instance root, and it makes the checks `<CORE>/docs/journey_move.md`
§ Resolving the target asks for: it refuses a root holding more than one station, named or not — a
root holds one, and a close never picks one of two — a root holding none when no station is named,
and a named station that is not open at the root — already in `trail/`, in `parked/`, or absent. **A refusal stops the run: report it as printed and change nothing.** The station
is the path the script printed, with `<shukuba>` its folder. Do not list the folder yourself to find
the station or to second-guess the answer — a listing the run chose is what this step replaces, and
on 2026-10-13 one cut off by `| head` was read as an empty root. An invocation pointing anywhere under
`system/` that is not a project's shukuba stops per *Project-level only* above.

**Then confirm the station was actually reached.** Read its reached-when and check it against the world.
If any part is unsatisfied, **stop and name `shukuba-park`**, the PM's to run — that skill moves the station to
`shukuba/parked/` and leaves the seed's item unticked, which is what an unfinished leg needs. Closing it
here instead would do both halves of the damage at once: `trail/` would claim a walk that never happened,
and Step 4's tick would mark the item done so no station is ever opened from it again. If the reached-when
turns on something you cannot observe, ask rather than inferring it from how much of the station looks
done.

**Where a check runs.** When checking the world means running the product's own checks — a test
suite, a harness, a script under the product's `checks/` — run them in a disposable copy of the
product — a fresh clone at the commit under test (`git clone --quiet <repo> <scratch> && git -C <scratch> checkout --quiet <sha>`), never `git archive`,
which drops the history a product's checks may read — never in the product's main checkout, and
leave that checkout as you found it. Run the checks from a subshell, never `cd` your own shell into the
copy, and remove the copy when you have read the result, in a command of its own run from outside it
(`<CORE>/roles/CROSS_ROLE.md` § *Every seat — a run leaves the product's main checkout as it found
it*). A chain halts the step that leaves it dirtier.

### Step 2 — Ensure the trail exists

```bash
mkdir -p "<shukuba>/trail"
```

Per `<CORE>/docs/journey_move.md` § Ensure the destination exists.

### Step 3 — Move the station into the trail

```bash
git mv "<shukuba>/<YYYY-MM-DD>_<slug>.md" "<shukuba>/trail/<YYYY-MM-DD>_<slug>.md"
```

Per `<CORE>/docs/journey_move.md` § Move whole. A reached station has no self-description for the move to
falsify — it is going where a finished station belongs — so the shared file's one permitted edit does not
arise here, and the file moves with no content change at all. The outcome goes in the **commit body**
(Step 5), which is what the trail's record is read alongside.

### Step 4 — Tick the Nemawashi

The station was opened from one unchecked item on the active seed's checklist. Check it off.

**Find the active seed.** It is the single item at the sibling
`system/projects/<project>/journey/nemawashi/` — a file, or a folder holding `seed.md` — at that
folder's **root**, excluding `README.md` and excluding the `unpicked/` and `trail/` subfolders. (One
active idea at a time; the other candidates sit in `unpicked/`.) If the root holds no item, or more than
one, **stop and ask** — the seedbed is in a state this skill must not guess at. For a folder-seed, every
read and the tick below both land in `seed.md`.

**A seed carrying no checklist has nothing to tick — proceed.** Roughly a third of the seeds on disk
are that shape: an idea written as one bounded defect never grows a route, and there is no item for a
station to have been opened from. Skip the rest of this step and go to Step 5, whose commit then
carries the station's rename alone. Say in the commit body that no item was ticked and why, so the
trail does not read as a tick that went missing.

**Match the item.** The station file names the seed item it was opened from — a worked example opens
*"Item 3 of the active 根回し Nemawashi `YYYY-MM-DD_a-seed-name`"*. Read the station (you still have
it from Step 1) and match that to exactly one **unchecked** (`- [ ]`) entry on the seed's checklist.

**Tick it, and only tick it.**

```
- [ ] Build the kensaiapp-spawn skill …     →     - [x] Build the kensaiapp-spawn skill …
```

Two brackets change. Nothing else about the line changes, and nothing is appended to it — per
*Don't bloat the journey* in the shared file.

**If the item cannot be matched to exactly one unchecked entry, stop and ask** — name the unchecked
entries and let the owner say which. A wrong tick silently buries a station's worth of work: the item
reads done, no station will ever be opened from it again, and nothing anywhere records that it wasn't
walked. There is no cheap way back from it, which is why guessing is not allowed here.

### Step 5 — Commit both paths, in one commit

One commit carries **two paths**: the station's *rename* (Step 3) and the *edited seed* (Step 4— for a
folder-seed, `seed.md` inside it). They are one fact — this station is closed — so they are one commit.

`<CORE>/docs/journey_move.md` § The commit owns the recipe; read it rather than working from the sketch below.
The two declarations differ:

- the **rename** is already in the index, so it is declared with **`--staged`**, naming **both halves**;
- the **edited seed** is an ordinary modification, so it rides **`--add`** — the seed's own path for a
  file-seed, `<nemawashi>/<seed>/seed.md` for a folder-seed.

**When the seed has no checklist there is no `--add` and no second path** — the commit carries the
rename alone, and the subject drops the tick clause. Step 4 sends you here directly.

```bash
python3 "<CORE>/tools/commit_builder.py" --repo . commit \
  --staged "<shukuba>/<YYYY-MM-DD>_<slug>.md" "<shukuba>/trail/<YYYY-MM-DD>_<slug>.md" \
  --add "<nemawashi>/<seed>.md" \
  --subject "close shukuba: <YYYY-MM-DD>_<slug> → trail/, item <n> ticked" \
  --actor scrum-master \
  --directional "Shukuba: <YYYY-MM-DD>_<slug> — progress: reached, closed to trail" \
  --surface "Claude Code" --co-authored-by "<your model> <noreply@anthropic.com>"
```

When `shukuba-park` runs this skill from the PM seat (§ Posture), the identity flag is that
seat's own — the PM's agent type, or `--role PM` from a `pm:` session — never the Scrum Master's.

**With no checklist**, the `--add` line goes and the subject drops its tick clause —
`close shukuba: <YYYY-MM-DD>_<slug> → trail/`.

The identity flag and the no-`--skill` rule are the shared file's. What is specific to a **close**:

- **`--directional` is always a `Shukuba:` line, and always `progress:`.** A close is project-scoped and
  it advances the station it names, so it resolves against the station just closed. The shared file's
  `Agari:` fallback does not apply — a station is open by definition here — and `aside:` belongs to
  `shukuba-park`, not to a close. See `<CORE>/doctrine/governance/commit_format.md` § Directional
  trailer.

**Then eyeball the stat**, per the shared file. With a checklist it must show **both** a rename **and**
an insertion/deletion pair for the seed (`seed.md` alone, for a folder-seed): the rename alone means the
tick did not land. With no checklist the rename alone is the correct and complete result. The seed and
the station are different journey items, so the shared file's move-then-edit trap does not fire from
Step 3/Step 4 order — but the stat is still the only place a missing tick shows. If it is missing,
re-`--add` the seed and commit before going on.

### Step 6 — Report

State plainly what happened: which station moved to `trail/`, and which checklist item was ticked (or
that the seed carries no checklist, so nothing was).

Then state **where the journey now stands** — the one fact Step 4 already computed and the caller cannot
get anywhere cheaper:

- **Unchecked items remain** — say how many, and quote the next one. The station slot is now empty, and
  the next station is `shukuba-open`'s (`<CORE>/roles/loaders/pm_global.md` § *Responsibilities* 3).
- **None remain** — say so, and say that **the retire is owed — `nemawashi-retire`**. The seed's whole
  checklist is walked, so this is where the walked seed leaves the walk. **Naming it is the whole of the hand-off**: this run does not perform the
  retire, does not offer to, and does not invoke `nemawashi-retire`. Say it only here, on the branch
  where no item remains; a seed with route left is not owed to anybody.
- **The seed carries no checklist** (Step 4's proceed) — say that, and say nothing about what the seed's
  state implies. There is no route to be part-way along, so "how many remain" has no answer here, and
  inventing one would read as a finished route.

Reporting that is not asking it. **Do not offer to open the next station, to walk it, or to retire the
seed** — see Critical Rules. An empty slot is the journey standing still, and the caller should know
that is the state they are in; what to do about it is theirs.

---

## Outputs

| File / effect | Produced when |
|---|---|
| `shukuba/<YYYY-MM-DD>_<slug>.md` moved to `shukuba/trail/<YYYY-MM-DD>_<slug>.md` + the seed's item ticked, in one commit | Success (Steps 3–5), when the seed carries a checklist |
| the same move, rename only, no tick | Success, when the seed carries no checklist (Step 4) |
| A report naming how many checklist items remain unchecked, and the next one | Always (Step 6) |
| No change; the script's refusal, reported as printed | No station open at the root, more than one, or the named one not open there (Step 1) |
| No change; a question naming the candidates | Unmatchable item (Step 4) |
| No change; a halt saying the posture is wrong | Invoked outside the Scrum Master seat and not from the PM's park (§ Posture) |

---

## Critical Rules

- **The Scrum Master's, and the PM's only from inside its park.** Any other seat, or the PM by any other
  route, names the close as owed and hands it to the Scrum Master.
- **The station is the one `retire.py resolve` prints.** Never one found by a listing of your own;
  a refusal from the script ends the run with nothing changed.
- **`trail/` only for a station that was reached.** Verify the reached-when in Step 1; an unreached
  station goes to `shukuba-park`, not here. Closing one anyway fabricates a completed walk *and* ticks
  its item away — both halves of the damage in one commit.
- **Project-level only.** The instance Shukuba is a router, never walked — its cross-project reached-when
  is not this skill's to verify, and no seed item stands behind it to tick. An instance-level
  invocation stops with a pointer to the router's hand move
  (`system/shukuba/README.md`) and the Michi — never a fabricated instance station.
- **Tick exactly one item, or ask — unless the seed has no checklist, which is a proceed.** The tick is `[ ]` → `[x]` on one matched unchecked entry. If it can't
  be matched to exactly one, ask. A wrong tick loses a station's work with no trace.
- **A tick is a tick.** Two brackets — no appended paragraph, no "done — see commit abc123". The
  don't-bloat rule this serves is the shared file's; a checklist line is where the temptation to break it
  actually lands.
- **One fact, one commit.** The close (rename + tick) is one commit, and it is the only one this skill
  makes. A newly opened station is `shukuba-open`'s commit; a seed retire is its own. Never
  bundle them: each carries its own directional trailer, and a bundled one cannot be reverted in pieces.
- **Don't offer the next move.** Not the next station, not walking it, not retiring the seed. Each is
  already owned — the station-open by `shukuba-open` (`<CORE>/roles/loaders/pm_global.md` § *Responsibilities* 3),
  the rest by the loop in `<CORE>/docs/michi_agari.md:144-149` — so an offer here is a second copy of a
  decided fact, and an interactive gate in a skill that must run from a delegate or a launcher with
  nobody in the room. Report where the journey stands; stop there.
- **`Shukuba: … progress:` always.** A close advances the station it names, so the directional never
  degrades to `Agari:` and never reads `aside:`.
- **The shared mechanic is shared.** Everything about *how* the move and its commit are made lives in
  `<CORE>/docs/journey_move.md`. Read it there; a second copy is a copy free to drift.
- **The seed's retire is `nemawashi-retire`'s.** This run never
  performs the retire and never offers it — and it must not re-implement that move or its
  unfinished-checklist gate. A second copy of that logic is a copy free to drift. What it does owe is
  one sentence, and only when no checklist item remains: the retire is owed — `nemawashi-retire`
  (Step 6). Saying it on any other branch invents an obligation.
