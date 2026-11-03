---
name: nemawashi-drop
description: |
  Drop a killed 根回し Nemawashi idea and leave the seedbed as it is behind it. The **Principal PM**'s —
  it halts outside that seat, because killing an idea is a route decision. Moves the seed — a
  file, or a folder holding `seed.md` — whole into the sibling `nemawashi/drop/`, restoring nothing.
  Takes a **candidate from `unpicked/`**
  ruled out before it was ever picked — the one origin no other journey skill accepts — and also the
  active idea from the seedbed root, whose line it also removes from the Principal PM's
  `## Picked seeds`. It moves the seed; it does not pick one, and it works identically at both levels.
  Park-don't-strike: the seed is relocated, never struck through, never marked dead in place. The why
  goes in the commit body, never into the file.
  Use when: an idea is being killed for good — ruled out, superseded, answered by another route, or
  abandoned before it was ever picked — and you want it moved to `drop/`.
  Do not use for: an idea that **ripened into work** — a project seed walked to the end (use
  nemawashi-retire), or an instance idea-seed cut into project seeds (moved to `trail/` by hand) —
  `trail/` is the record of ideas that ripened; an idea being set down to be **picked up again** (use
  nemawashi-unpick — that returns the seed to `unpicked/`), a 宿場 Shukuba station (use shukuba-park or
  shukuba-retire), a 飛び石 Tobiishi (use tobiishi-seal), or picking the next idea (the PM's own call).
  Trigger phrases: "drop this seed", "this idea is dead", "kill this candidate", "we are not doing
  this", "rule this one out", "this seed is superseded for good", "nemawashi-drop".
license: MIT
metadata:
  version: "3.6.2"
  category: journey
  risk: safe
  created: "2026-09-04"
---

# Nemawashi Drop

## Purpose

**Drop a killed idea, and leave the seedbed as it is behind it.** A 根回し Nemawashi seed is killed when
the work it proposed turns out to be wrong, another route already answered its question, or it is simply
not going to be done. The seed goes whole into `nemawashi/drop/`, and nothing else moves.

**It restores nothing; it does not pick one.** Picking the next active idea is the PM's own call
(`<CORE>/docs/michi_agari.md` § "How we work", step 1) and is out of scope here.

**Drop, don't retire, don't park, don't seal.** The verbs are kept straight in
`<CORE>/docs/michi_agari.md` § Quick reference, which owns the distinction and the reason for it:
you **seal** a 飛び石 Tobiishi, **close** a station, **retire** a finished idea, and **drop** a killed
one. `nemawashi-retire` is the near neighbour and the easy mistake — it files a seed in `trail/`, which
is the record of ideas that **ripened into work** — walked to the end, or cut into the seeds that will
walk it.

**The seed survives at a resolvable path, and the pointers at it break anyway.** Moving rather than
deleting means the file is still there to be read, and its folder tells the reader the idea was killed.
It does **not** mean the citations survive: a seed's path spells its position, so every pointer aimed at
where this file used to be is now dead (`<CORE>/docs/journey_move.md` § After the move, say which pointers
it broke). Step 5 finds them, and they are repaired.

**Shared mechanics.** The move itself — how a journey artifact changes folder, and how that commit is
built — lives in `<CORE>/docs/journey_move.md`. Read it; this file names the section it is
leaning on at each step rather than restating any of it.

## Posture

**Principal PM only.** Run in a `principal-pm:` session or as the `principal-pm` subagent. Invoked
from anywhere else, halt at once, say the posture is wrong, and name the way in. The seat's contract is
`<CORE>/roles/loaders/principal_pm_global.md`, and the gate is what makes this skill that seat's
(§ *Skills toolbox (reminder)* there names it).

**The gate is here because a kill is a route decision** — the owner's call, 2026-09-12. (The retire,
gated to this seat by the same call, moved to the Scrum Master on 2026-09-24.) An idea ruled out is one the program will not walk, which is the shape of the route rather
than the walking of it, and § *Non-responsibilities (boundaries)* in the seat's contract draws that
line. `nemawashi-unpick` is the sibling that stays the PM's: setting an idea down decides nothing
about the route.

## Input

**One skill invokes this one: `nemawashi-refine`**, the Principal PM's answer to a retired seed, which
drops a candidate its re-read of the pool rules out. Its invocation says the kill and gives the reason
its method wrote, which closes both halves of Step 1A. Otherwise a person or a queue launches it with
`<CORE>/launchers/skill/launcher.sh nemawashi-drop <project> <slug> "<reason>"` (`launcher.md`). That
command carries both halves of Step 1A: the prompt says the kill, and the reason is the caller's decided
words. A launched run takes
a project seed only; an instance seed is dropped from a `principal-pm:` session.

The invocation names **the seed**: a path to the file, or enough to identify one (the project — omit for
instance-level — and the slug).

**Two origins, and this skill is the only journey move that accepts the second.**

| origin | the seed is | `<seed>` resolves to |
|---|---|---|
| the seedbed **root** | the active idea | `<nema>/<slug>.md` |
| **`unpicked/`** | a candidate — never picked, so it has no checklist to have walked and no station | `<nema>/unpicked/<slug>.md` |

`<nema>` is the nemawashi folder root, either `system/projects/<project>/journey/nemawashi/` or the
instance `system/nemawashi/`. **`<seed>` is the seed's current path**, and every command below is
written against `<seed>` rather than against a fixed form, because the two origins do not share one.

**A seed already in `trail/`, `drop/` or a station folder is not an input here.** Repairing a
mis-aimed retire — a seed filed in `trail/` that was really killed — is a correction to a record rather
than a drop, and no skill owns it; say so and stop rather than moving it a second time.

## Workflow

### Step 1 — Resolve the seed, then close three questions before touching anything

Resolve per `<CORE>/docs/journey_move.md` § Resolving the target, **with one condition of this skill's
relaxed and the rest held.** That section requires the target sit at the journey part's root and not in
a subfolder, because it was written for four siblings that all move root → subfolder. This skill is the
first whose source may itself be a subfolder, so **for a drop, `unpicked/` is an accepted origin** and
the root-only condition does not apply to it. Everything else in that section still binds — the file
exists, the journey part is a nemawashi folder, exactly one item matches, and `trail/`, `drop/` and the
station folders remain refused.

**A. The kill has to be said, and so does the reason.** A drop proceeds on an explicit answer: this idea
is being killed, and why. All three seedbed exits start the same way — the seed leaves where it was — so
only the caller's words distinguish them, and a skill that infers the verb from the gesture picks one at
random.

The two halves close separately, and both are owed:

- **The kill.** A caller who says the idea is dead, is being killed, ruled out, superseded for good, or not going
  to be done **has closed this half** — that is what the trigger phrases in this skill's own description
  are. Naming the skill or a path and nothing more has **not**: "drop this seed" identifies which skill
  to run, not that the run should happen.
- **The reason.** Never assumed, and **never composed from the seed** — the checklist says what was
  walked, the prose says what was proposed, and neither says what was decided. If the caller said the
  idea is dead but not why, **stop and ask for the why alone.** The reason is not a formality here: by
  Step 3 the file is not edited and the folder says only *killed*, so the commit body is the only place
  it survives, and a sentence nobody decided is unappealable once written.

If the answer is really one of the other two, this skill is not it:

- **finished** — a project seed whose checklist was walked to the end: the **retire**, which
  files it in `trail/`, the record of ideas that ripened into work. Or an instance idea-seed that
  `seeds-from-idea` cut into project seeds: moved to `trail/` by hand. Stop and name which.
- **parked** — set down now, to be picked up again later. **`nemawashi-unpick`**: it moves the seed to
  `unpicked/`, joining the candidate pool, checklist intact. Stop and name it.

Do not soften a refusal into a drop because the caller seems to want one — if the answer is *finished*
or *parked*, the other skill is the answer even when this one is already invoked.

**B. Read the checklist, if the seed has one.** The unchecked branch does not gate; the ticked one does.

- **Unchecked items remain, or there is no checklist** → the normal shape of a killed idea. **Proceed.**
  This is where this skill differs from `nemawashi-retire`, whose gate stops exactly here. An unwalked
  route is what being killed *looks like*, so stopping on it would treat the skill's own subject as an
  anomaly — and a candidate, which never had a checklist at all, could never clear such a gate.
- **Every item is ticked** → **stop and ask.** A fully walked idea is what *finished* means, so a drop
  is probably a mis-aimed retire. It may still be a genuine kill — an idea can be walked to the end and
  then ruled out on what the walk found — but that is worth one sentence before the record says it was
  killed rather than completed.

**C. If the seed is the active idea, check its station.** Root origin only; a candidate in `unpicked/`
never had one.

Read `<journey>/shukuba/`. **If a station is open on this idea, stop.** The fix is an order, never a
bundled move and never a silent one: **`shukuba-park` first, in its own commit** — the PM's to run, so
it is named and handed to that seat — then this. Dropping
the seed first leaves a station standing over an idea that is dead, and nothing in the station says so —
the same state `nemawashi-unpick` forbids for the strictly milder case of an idea only being set down.
`nemawashi-retire` holds the same gate, and meets it far less often: it runs right after the last
station closed, whereas a kill lands mid-walk by nature.

### Step 2 — Ensure the drop bin exists

```bash
mkdir -p "<nema>/drop"
```

Per `<CORE>/docs/journey_move.md` § Ensure the destination exists. `drop/` is a `[create]` directory stub in
the manifest (`<CORE>/doctrine/setup/kensaiapp_structure.md` §1 and §2), so it is usually there already;
a seedbed stamped before the bin existed is the case this line covers.

### Step 3 — Move the seed into the drop bin

```bash
git mv "<seed>" "<nema>/drop/<slug>.md"
```

**A folder-seed moves the same way, whole:** `git mv "<seed>" "<nema>/drop/<slug>"` — `<seed>` is then
the folder's own current path, and the destination is the folder, carrying `seed.md` and every
`<unit-key>_report.md` / `<unit-key>_recommendations.md` inside it in one `git mv`.

`<seed>` is whichever origin Step 1 resolved — the root form or the `unpicked/` form. The destination is
the same either way: a dropped candidate and a dropped active idea are the same record.

Per `<CORE>/docs/journey_move.md` § Move whole. **Nothing in the seed is edited** — not a heading, not a
verdict line, not a note to a future reader (`seed.md`, for a folder-seed). A seed's own currency marker
("Picked active …") is not corrected either: a dropped active idea genuinely was the active one right up
to this commit, so the record is true as it stands.

**If the kill needs the disproof written down** — what was believed, what was tried, what the outcome
falsified — that is a different need from this move, and this skill does not grow to meet it. A drop
relocates a seed and writes nothing into it; a skill that started writing verdicts into the file would be a
different skill with a different name. Say that plainly, name no destination you cannot cite, and let
the caller decide where it goes.

**A dropped active idea leaves the Principal PM's context too.** Root origin, project level only. Per
`<CORE>/docs/journey_move.md` § *The Principal PM's picked seeds*: delete the line naming
`<project> · nemawashi · <slug>` from `## Picked seeds` in `system/contexts/CONTEXT_PPM.md`, and nothing
else. That file is not the seed, so the seed stays unedited. No file, section or line means nothing to
remove, and a candidate from `unpicked/` never has a line.

### Step 4 — Commit the seed's move

One commit carries the seed's rename and, when Step 3 removed one, the context line — that is the whole
of what this skill changes on disk.

`<CORE>/docs/journey_move.md` § The commit owns the recipe; read it rather than working from the sketch
below. The path arrived by `git mv` and is not edited, so **`--staged`** carries the move — plus
`--add system/contexts/CONTEXT_PPM.md` only when Step 3 removed a line — with both halves of the move named, which for an `unpicked/` origin means the `unpicked/` path, not the
root one. Naming a path the index does not carry is refused by the staged-set guard, and so is leaving
a staged path undeclared; the wrong template produces both refusals at once.

```bash
python3 "<CORE>/tools/commit_builder.py" --repo "<instance root>" commit \
  --staged "<seed>" "<nema>/drop/<slug>.md" \
  [--add system/contexts/CONTEXT_PPM.md] \
  --subject "drop: nemawashi/<slug> → drop/" \
  --body "$(cat <file>)" \
  --actor principal-pm \
  --directional "<directional>" \
  --surface "Claude Code" --co-authored-by "<your model> <noreply@anthropic.com>"
```

`<instance root>` is the directory holding `system/projects/` — the same repo Step 5 checks.

**The body goes through a file, not an inline string.** `<CORE>/doctrine/governance/commit_via_builder.md` § The call:
*"A `--body` that carries a backtick goes through a file, never inline"* — the shell runs the backtick
span as a command, the text vanishes, and the commit lands looking fine. A drop's body routinely names
the seed that superseded this one, in backticks, so this family's one always-written body is exactly
where that defect fires.

The identity flag, the both-halves-not-a-prefix rule, and the no-`--skill` rule are the shared file's. What is
specific to a **drop** is that its directional always reads **`aside:`**. A drop completes nothing —
the retire is the one journey move that does, per `<CORE>/docs/journey_move.md` § The commit, "the
reading follows the move, not the referent" — so claiming `progress:` for a kill would say the project
advanced by giving something up:

- **project** seed → `Agari: <name> — aside: <why the idea was killed>`. A station should not be open on
  this idea — Step 1C stops if one is — so `Shukuba:` does not apply. Never `Shukuba: none`, which
  doctrine retired.
- **instance** seed → `Michi: aside: <why the idea was killed>`, with no way-slug, per
  `<CORE>/doctrine/governance/commit_format.md` § Directional trailer.

**The body is the record.** It is the only place the reason survives, because the file is not edited and
the folder says only *killed*. Write the why there in a sentence someone can act on, not a label.

**Then eyeball the stat**, per the shared file. It must show **only rename(s)** — one for a file-seed,
one per file the folder held for a folder-seed — plus, when Step 3 removed it, one deleted line in
`system/contexts/CONTEXT_PPM.md`. Any other content in the stat means something was touched that should
not have been.

### Step 5 — Say which pointers the move broke

```bash
python3 "<CORE>/tools/check_journey_links.py" --repo "<instance root>"
```

Per `<CORE>/docs/journey_move.md` § After the move, say which pointers it broke, which owns both halves of
what follows and is read there rather than restated here: **what it names is repaired**, and its exit
code is information rather than a gate — a drop is never held up by a pointer somewhere else being
stale. The two do not pull against each other: the check never blocks the move, and the pointers it
names are still the finding session's to fix.

The step earns its place: a killed idea is usually one other seeds depend on, and the pointers this
breaks are the ones whose owners most need to hear that the answer is now "no".

### Step 6 — Report

State plainly:

- which seed moved to `drop/`, from which origin, and **why it was killed**;
- **the seedbed state the run left behind** — a root drop leaves the root empty with the pool unchanged;
  a candidate drop leaves the root as it was with the pool one shorter. Say which, and say how many
  candidates remain, because the two outcomes are different and the caller should not have to look;
- whether the seed's line left `## Picked seeds`, or there was none;
- the thing deliberately **not** done: no idea has been picked, no other candidate moved, and the seed
  itself is unedited;
- the broken pointers from Step 5 and what each repair was.

---

## Outputs

| File / effect | Produced when |
|---|---|
| `<seed>` (a file, or a folder holding `seed.md`) moved whole to `nemawashi/drop/<slug>` | Success (Step 3) — from the root or from `unpicked/` |
| The seed's line deleted from `## Picked seeds` in `system/contexts/CONTEXT_PPM.md`, same commit | Step 3 dropped the active idea and found the line |
| No change; a halt saying the posture is wrong | Invoked outside the Principal PM seat (§ Posture) |
| No change; a question naming the candidates | Ambiguous / not-found seed (Step 1) |
| No change; a question putting the three-way fork | The kill was not said, only implied (Step 1A) |
| No change; a question asking only for the why | The kill was said, the reason was not (Step 1A) |
| No change; a refusal naming `nemawashi-retire` | The idea was walked to the end (Step 1A) |
| No change; a refusal naming `nemawashi-unpick` | The idea is being set down to resume (Step 1A) |
| No change; a refusal naming no skill | The seed is already in `trail/`, `drop/` or a station folder (Input) |
| A question, then either outcome | Every checklist item is ticked (Step 1B) |
| No change; a stop naming `shukuba-park` and the order | A station is open on the active idea (Step 1C) |

No idea is ever picked, and no other candidate moves — those are the PM's next move and nobody's,
respectively, and neither is this skill's.

---

## Critical Rules

- **The Principal PM's, and it halts elsewhere.** Ruling an idea out decides the program's route, which
  is that seat's. A PM who wants an idea killed says so and hands it up.
- **`drop/` only for an idea that is dead.** Not slow, not blocked, not waiting on something. An idea
  that may come back goes to `nemawashi-unpick`; one that was walked to the end goes to
  `nemawashi-retire`. The folder is a claim about what happened, and it is the only claim the record
  makes.
- **The kill is said and the reason is given; neither is inferred.** Being pointed at a path is not a
  decision, and the seed's own text is not a source for the why.
- **An unwalked checklist is not a problem to solve.** It is what a killed idea looks like. This skill
  does not ask the caller to resolve the items, and it does not tick them.
- **Never orphan an open station.** Step 1C stops when a station is still open on the idea being
  dropped. The fix is an order — `shukuba-park` first, its own commit, then this.
- **The seed is never edited.** The commit is the seed's rename — one path for a file-seed or one per
  file a folder-seed holds — plus, for a dropped active idea, its line leaving `## Picked seeds`. Park-don't-strike: no strike-through, no
  `## KILLED` heading, no closing note. The commit body carries the why.
- **One fact, one commit.** The seed's move is one commit. A station park that had to happen first is
  `shukuba-park`'s own, separate commit — never fold the two together, since they carry different
  directional trailers and a bundled commit cannot be reverted in pieces.
- **One procedure, both levels.** This skill does exactly the same thing at project level and at
  instance level — move the seed to `drop/`, touch nothing else but a project seed's picked line. There is no restore, so there is
  nothing to degrade or branch on by level.
- **The pointer check never gates the move, and what it names is still repaired.** It runs after; the
  exit code is information, never a gate on the drop you were asked to make, and a pointer it names is
  the finding session's to fix — `<CORE>/doctrine/governance/found_while_walking.md` § *A broken
  journey pointer is repaired, and the triple is what stops it breaking*, clause 1 with no exception.
- **The shared mechanic is shared.** Everything about *how* the move and its commit are made lives in
  `<CORE>/docs/journey_move.md`. Read it there; a second copy is a copy free to drift.
