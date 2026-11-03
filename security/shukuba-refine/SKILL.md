---
name: shukuba-refine
description: >-
  PM-posture skill the PM runs, in a pm session or as the pm agent, after a change unit lands or halts. It reads what the unit left (its flow
  findings, its code-integrity report, its security report, the developer's closing commit and its `Deferred:` lines, any deferred_decisions.md, the
  corrections its plan owed to records outside its reach, and the work its spec handed on) and what moved in the product's upstream documents since the unit's seed was cut, then acts on the
  project's route with six moves (modify a seed, modify a station, park a station,
  un-pick the active seed to free the slot, raise a companion item on an upstream document, drop a
  halted unit through tobiishi-drop) and always
  leaves two files with the seed, a report and a recommendations file to the Principal PM. The report
  opens with the next moves the run leaves owed — each with its seat and the command that starts it —
  and the completion message carries them. Requires PM
  posture and halts outside a pm session or the pm subagent. It never drops or closes a seed and never
  writes a new one. Not stations-from-seed, which routes one seed before it is walked, from the seed
  alone.
when_to_use: >-
  Run by the PM once a unit has landed or halted. Trigger phrases — "shukuba-refine", "refine the route
  after the seal", "review the sealed unit", "review the halted unit". Do not use for splitting a freshly picked seed into
  stations (stations-from-seed), opening or sealing a change unit (tobiishi-open, tobiishi-seal),
  closing or parking one station on its own (shukuba-retire, shukuba-park), or cutting, retiring or
  dropping a seed (seeds-from-idea, seeds-from-product-docs, nemawashi-retire, nemawashi-drop).
license: MIT
metadata:
  author: Eyal Golan
  version: "2.11.0"
  created: "2026-09-10"
  category: journey
  tags: shukuba, nemawashi, tobiishi, review, pm, journey
  risk: safe
  depends-on: shukuba-park, nemawashi-unpick, tobiishi-drop
---

# shukuba-refine

## Purpose

After a change unit lands, read what it left and what moved upstream, and bring the project's route
back into line with the world. What leaves is a route that has been re-read — moved where it owed a
move, left where it holds — and two files with the unit's seed that say what was done, why, from
where, and what is owed next and by whom.

**This file is the orchestrator.** It owns the posture gate, resolving the unit, its station and its
seed, the hold list's mechanics, running each move through its owner, landing the two files, and the
commits. It makes no judgment about the route.

**The method is `prompts/rich.md`** — the one body this file points at. Read it in
full at Step 4 and apply it. What to read, what counts as a finding, what is held, which of the six
moves each finding owes, companion over recommendation, what is never done, what every entry
carries, and which moves are owed next all live there — its § *Inputs you work from*, § *Read the unit
before the route*, § *What you are looking for*, § *The hold list*, § *The six moves*, § *Companion
over recommendation*, § *What you never do*, § *No move is an answer*, § *Every entry carries what,
why, and where from* and § *Name what comes next*. None of it
is repeated here.

**The two files' shapes** are `<CORE>/templates/journey-templates/shukuba_refine_report_template.md` and
`<CORE>/templates/journey-templates/shukuba_refine_recommendations_template.md`. A seed's own shape,
including its folder form, is `<CORE>/templates/journey-templates/nemawashi_template.md`.

**Not `stations-from-seed`.** That skill routes one picked seed before it is walked, from the seed
alone, and writes only its checklist. This one runs after a unit lands, from what the unit left and
what moved upstream, across every seed and station of the project, and always writes its two files.

## Posture

**PM only.** Run in a `pm:` session or as the `pm` subagent. Invoked from anywhere else, halt at once,
say the posture is wrong, and name the way in — open a session with the `pm:` prefix, or run the `pm`
subagent. The seat's contract is `<CORE>/roles/loaders/pm_global.md`.

The gate is here because the run writes and commits with nobody answering
(`<CORE>/doctrine/setup/authoring_layers.md` § *A skill that acts unattended gates to its seat*). The
`pm` agent may invoke it as readily as a person in a `pm:` session; every other seat is refused here.

## Input

**The project** — `system/projects/<project>/` — and **the unit's key**. Everything else is resolved
from those two.

The key is the one the caller names. Without one, it is the unit the project's
`contexts/CONTEXT_PM.md` names: that file holds the project's current change, and `tobiishi-seal`
flips its `**Status:**` to `Sealed` when the change lands, so a sealed item there is the unit that just
landed. Take the `<YYYY-MM-DD>_<slug>` key it names when that key resolves to
`journey/tobiishi/trail/<key>/`, and say in the report that the key came from the context.

**A halted unit is found the same way.** When the context's status is `Open`, take the key it names
as a halted unit when three things hold:
- the key resolves to an open `journey/tobiishi/<key>/`;
- no walk is in flight on it, meaning neither `system/logs/chain-<project>-state.json` nor
  `system/logs/chain-change-<project>-state.json` carries that `key` with `ended` null;
- a walk has ended on it, meaning one of those files carries that `key` with `ended` set to `halted`.

Say in the report that the key came from the context. An ad-hoc merge never writes the context, so
its key is always the caller's.

**A unit already reviewed is reviewed again, in full.** A report already beside the seed for this key is
never a reason to skip the review or to stop early, and neither is a unit, a product or a chain that
has not changed since that report. The method may have changed, and a moved rule changes the verdict.
Read the unit, apply the current `prompts/rich.md`, make the moves it finds owed,
and write the two files again. The earlier ones stay in git.

**A named key** resolves in this order: `journey/tobiishi/trail/<key>/` (sealed), then the open
`journey/tobiishi/<key>/` (halted), then an ad-hoc merge. An open unit is a `journey/tobiishi/<key>/`
holding `change_request.md`, outside `trail/` and `drop/`.

**Stop and say which is missing** when there is no project, or when no key was named and the context
cannot supply one: its status is `Open` and its unit is not halted as above (it is still being
walked, so there is nothing to review yet), or it names no key, or its key resolves to neither a sealed
folder nor a halted unit. Never take the latest unit any other way.

The run works in the instance it was started in, on its current branch. It opens no worktree.

## Workflow

### Step 1 — Gate, then resolve the unit

Check the posture (§ *Posture*) and halt there rather than proceeding.

Resolve the unit by its key. It is found in one of three shapes, and the Tobiishi is the one this skill
is built for:

| | Sealed 飛び石 Tobiishi | Halted Tobiishi | Ad-hoc merge |
|---|---|---|---|
| The unit's folder | `journey/tobiishi/trail/<key>/` | `journey/tobiishi/<key>/` on `main` and on branch `<key>` | `system/projects/<project>/docs/<key>/` |
| Flow findings | `<folder>/flow_findings/<step>.md` | the same, read off branch `<key>` | not produced — state absent |
| Integrity report | `<folder>/code-integrity-report.md` | the same, read off branch `<key>` | `<folder>/code-integrity-report.md` |
| Security report | `<folder>/security-report.md` | the same, read off branch `<key>` | `<folder>/security-report.md` |
| Deferred decisions | `<folder>/deferred_decisions.md`, if any | the same, read off branch `<key>` | not produced — state absent |
| Deferred lines | the lines that **begin** `Deferred:` in the developer's closing commit (the commit the `Developer's closing commit` row resolves); when there are none, state them absent | the same, if the unit reached a closing commit | the same |
| Corrections owed | `<folder>/tl_instruction.md` § *Corrections owed while there*, if any | the same, read off branch `<key>` | not produced — state absent |
| Work handed on | `<folder>/change_spec.md` § *Out of Scope* | the same, read off branch `<key>` | not produced — state absent |
| The halt report | not produced — state absent | `halt_report.md`, from the four places `DiskReader.halt_report` looks, branch first | not produced — state absent |
| The unit's commits | `git log <M>^1..<M>^2`, where `<M>` is the `merge: <key> →` commit | `git log main..<key>` | the same as sealed |
| Developer's closing commit | the latest commit in that range whose `Role:` is `Developer` | the same | the same |

When no `merge: <key> →` commit exists, the unit's commits are those whose message names the key
(`git log --grep "<key>"`), and a closing commit with no `Role: Developer` among them is stated absent.
Every row is read. An artifact the shape does not produce, or that is not on disk, is **stated absent
in the report, never a halt**. An ad-hoc plan is free-form and carries neither of the last two
sections, so on an ad-hoc merge both are stated absent.

**Stop** only when neither the folder nor any commit naming the key exists — say what was looked for.

### Step 2 — Resolve the station and the seed

**The station.** Read the `Shukuba:` trailer on the unit's commits
(`git log --format='%(trailers:key=Shukuba,valueonly)' <range>`); a sealed unit's `seal:` commit
carries it. Its value is the station's dated stem, `<YYYY-MM-DD>_<slug>`; a commit written before
2026-09-14 may carry the bare `<slug>`, which names the stem ending in it. Where no commit carries one, the station is the one file under
`system/projects/<project>/journey/shukuba/` — root, `trail/` or `parked/` — that names the key. More
or fewer than one station → stop and name what was found.

**The seed.** The station names its seed on its item line (*"Item <n> on the active 根回し Nemawashi
`<seed-slug>`"*). Find that seed under `system/projects/<project>/journey/nemawashi/` as a file or a
folder holding `seed.md`, per `<CORE>/docs/journey_move.md` § *Resolving the target*. The
two files land with it at the root or in `unpicked/`. **If it sits in `trail/` or `drop/`, stop and
say so** — this skill never writes there, and where the record of a finished or killed seed takes a
report is not this skill's to decide.

### Step 3 — Read upstream, and build the hold list

**Upstream.** Resolve `Product path:` from `system/projects/<project>/project.md` — relative to the
instance, or absolute. Where it holds no `docs/`, there is no upstream; say so and go on. Otherwise,
in the product's own repo, list what changed under `docs/` since the seed's first commit
(`git log --diff-filter=A --follow --format=%cI -- <seed path>`, then
`git -C <product repo> log --since=<that date> --name-status -- docs/`), and list every live
`*_open_issues.md` there.

**Chain in flight.** Read `system/logs/chain-<project>-state.json`. A chain is in flight when the file
exists, its `ended` is null, its `pending` is set, and its `schema_version` is the engine's — the same
test the engine uses to refuse a second walk (`<CORE>/tools/chain.py`
`_refuse_to_overwrite_a_live_walk`). Every document on its `spine`, and that document's companion, is
held.

**Units being walked.** A change unit at `journey/tobiishi/`'s root holds the seed and station it
walks. The halted unit under review is the one exception: it holds neither its own station nor its
seed. Every other open unit still holds what it walks.

Hand the prompt the held set; what it means for each seed and station is decided there.

### Step 4 — Read the method, and decide

Read `prompts/rich.md` in full, then the two templates. Read every seed at the
seedbed root and in `unpicked/`, the open station and every station in `parked/`, and
`system/projects/<project>/agari.md`. Apply the prompt. Every judgment — what each finding owes, which
moves are made, what is held, what is recommended, and whether nothing moves — is made there.

### Step 5 — Act on the route

Make the moves in this order, so no move finds the ground changed by a later one:

1. **Modify a seed, modify a station.** Edit in place. For a folder-seed the edit lands in `seed.md`;
   for a station, in its file where it sits (root or `parked/`). A ticked `[x]` line is never changed.
   Commit these edits together through `<CORE>/doctrine/governance/commit_via_builder.md` with
   `--skill shukuba-refine --prompt shukuba-refine/rich --role PM`.
2. **Park a station.** Run `shukuba-park` on it. It verifies the reached-when itself and commits
   itself; where it refuses, record the refusal as a non-move. A station the park finds reached, the
   park closes through `shukuba-retire` (its own exception, the owner's call, 2026-10-03) — record
   that as a close, not a park. Any other station found reached is not closed here — the close is
   the **Scrum Master**'s (Step 7).
3. **Un-pick the active seed**, only to free the slot — run `nemawashi-unpick`, giving it as its
   reason why the prompt found the seed blocked. It moves the seed, so the seed's path for Step 6 is
   where it now sits.
4. **Raise companion items.** Per `<CORE>/../skills/companion/.claude/skills/companion-self-answer/SKILL.md` § *When a change
   belongs to another document*: append to the document's live companion, or open one from that
   document's own `*_open_issues_template.md`. An item raised from here goes
   in the companion's section for items raised from downstream where the template has one. Commit it
   in the product's own repo (`git rev-parse --show-toplevel` from the companion's folder), one commit
   per companion. The document is never edited.
5. **Drop the halted unit.** Run `tobiishi-drop` on it with the project, the key and the reason the
   prompt wrote. It checks, commits and closes the worktrees itself; where it refuses, record the
   refusal as a non-move. Only a halted unit is dropped — never a sealed unit or an ad-hoc merge.

Never hand-edit `CONTEXT_PM.md` or `change_request.md`, and never edit a file under `trail/` or
`drop/`.

### Step 6 — Land the two files with the seed

**A file-seed becomes a folder first.** Move it, then write:

```bash
mkdir -p "<nema>/<seed>"
git mv "<nema>/<seed>.md" "<nema>/<seed>/seed.md"
```

`<nema>` is the seed's own folder — the seedbed root or `unpicked/`. A pointer written as
`<seed>.md` still resolves once `<seed>/seed.md` exists, so nothing else changes.

Write `<nema>/<seed>/<key>_report.md` and `<nema>/<seed>/<key>_recommendations.md` from their templates
— **both, every run**. The report names every move with the SHA Step 5 produced, and opens with
`## Next moves` — every move left owed, whose it is and the command that starts it. With nothing to
recommend, the recommendations file carries the one line "Nothing to recommend." under its heading.
In both, a seed, a station or a change unit is cited by its triple, `<project> · <kind> · <name>` —
the name the folder's own for a folder-seed or a change unit, with no `.md` — never by its path, with any line after the span as `(line N)` — the report template states why, and
`<CORE>/tools/test_journey_pointers_are_triples.py` refuses a path-form pointer in a live seed folder.

Commit through `<CORE>/doctrine/governance/commit_via_builder.md`: `--staged` naming both halves of the
move when there was one, `--add` the two files, `--skill shukuba-refine --prompt shukuba-refine/rich
--role PM`. The directional follows `<CORE>/doctrine/governance/commit_format.md` § *Directional
trailer*: `Shukuba: <YYYY-MM-DD>_<slug>` when a station is open, else `Agari: <project>`; `progress:` when the route
moved, `aside:` when nothing did.

Then run `python3 "<CORE>/tools/check_journey_links.py" --repo "<instance root>"` and report what it
names, per `<CORE>/docs/journey_move.md` § *After the move, say which pointers it broke*. It never gates the run.

### Step 7 — Report

Say what moved and what was held, how many recommendations were written, and where the two files are.
Then list the report's `## Next moves` as written there — each move, whose it is, and its command — and
make none of them: a station found reached that the park did not close is the **Scrum Master**'s to close (`shukuba-retire`), the
pick is `nemawashi-pick`'s, the next change is its chain's, a walked seed's retire is the **Scrum Master**'s
(`nemawashi-retire`), and any seed's drop or cut is the Principal PM's. The completion message of an unattended run is read off that same section
(`launcher.md` § *Reporter*), so what is said here and what reaches the owner's phone are one list.

---

## Outputs

| File / effect | Produced when |
|---|---|
| `<key>_report.md` (opening with `## Next moves`) and `<key>_recommendations.md` inside the seed's folder, one commit | Every run that passes Steps 1–2 |
| A file-seed moved to `<seed>/seed.md`, same commit | The seed was a file |
| Seed and station edits, one commit | The prompt found a seed or station owed a change (Step 5.1) |
| A `shukuba-park` or `nemawashi-unpick` commit, each its own | The prompt found the move owed (Step 5.2–5.3) |
| A companion item in the product's repo, one commit per companion | A change belongs to an upstream document (Step 5.4) |
| A `tobiishi-drop` commit | A halted unit whose intake will not be walked as written — its subject no longer holds, or the route has split it into separate units (Step 5.5) |
| No change; what is missing, named | Wrong posture, no project, no key named and none sealed in `CONTEXT_PM.md`, no unit found, not exactly one station, or a seed in `trail/` or `drop/` |

---

## Critical Rules

- **Both files, every run.** A run that moves nothing still writes the report and the recommendations
  file, and "Nothing to recommend." is an answer.
- **Never drop, close or write a seed.** No `nemawashi-drop`, no retire, nothing new in
  `unpicked/`. A drop or a cut is a recommendation to the Principal PM; a retire is a `## Next moves`
  row for the Scrum Master.
- **Each move through its owner.** Park, un-pick and drop run their skills; a companion item follows
  `companion-self-answer`'s mechanism. None is re-implemented here. A reached close is never performed
  here — it is named as owed to the **Scrum Master** (Step 7), unless the park finds it and closes it
  through `shukuba-retire` itself (Step 5.2).
- **Name every next move, make none.** The report's `## Next moves` lists what the run leaves owed,
  whose it is and its command; the run performs none of them, and Step 7 repeats that list rather than
  composing its own.
- **Held means untouched.** A seed or station whose sources include a document a chain may still move,
  or that an open unit walks, is listed as held and not modified.
- **No fix, no hand-edit of a skill's file, no write to `trail/` or `drop/`.** The run routes; it does
  not patch.
- **The method is the prompt's.** Everything about what a finding owes lives in
  `prompts/rich.md`. A second copy here is a copy free to drift.
