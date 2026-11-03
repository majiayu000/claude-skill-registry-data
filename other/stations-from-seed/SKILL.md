---
name: stations-from-seed
description: >-
  PM-posture skill that splits the picked 根回し Nemawashi seed into the 1 to N 宿場 Shukuba stations
  that will actually be walked, rewriting that seed's own station checklist in place. The checklist a
  seed arrives with is the cutter's proposal, written by a seat that never walked the product; this is
  where it becomes the route. Requires PM posture and halts outside a pm session or the pm subagent. It
  writes only the checklist section and the divergence lines that go with it — no station file, no
  change_request.md — so the next moves stay the PM's own. Use when a seed has just been picked and its
  route has to be settled, or when a seed reached the root with no checklist at all. After a change unit
  lands, re-cutting the route against what the unit found is shukuba-refine's, not this skill's.
when_to_use: >-
  Trigger phrases — "split the seed", "split this seed into stations", "cut the seed into stations",
  "re-cut the checklist", "what stations does this seed take", "stations-from-seed". It also fires
  right after a pick, when the expectation is a route at the end of it. Do not use for picking or
  un-picking a seed (nemawashi-pick, nemawashi-unpick), opening a station
  (shukuba-open), opening or sealing a change unit (tobiishi-open, tobiishi-seal), closing
  or parking a station (shukuba-retire, shukuba-park), re-reading the route after a change unit lands
  (shukuba-refine), or cutting an idea into seeds (seeds-from-idea and seeds-from-product-docs, which
  are the Principal PM's).
license: MIT
metadata:
  author: Eyal Golan
  version: "1.6.0"
  created: "2026-09-05"
  category: journey
  tags: nemawashi, shukuba, stations, split, pm, journey
  risk: safe
---

# stations-from-seed

## Purpose

Turn the **picked seed** into the **route**. One seed sits at the project's `journey/nemawashi/` root
carrying a checklist somebody proposed; what leaves is the checklist a PM will actually walk, station
by station.

**This file is the orchestrator.** It owns the posture gate, resolving the seed, the two gates that
stop a run, the in-place rewrite, and the commit. It makes no judgment about the route itself.

**The method is `prompts/rich.md`** — the one body this file points at. Read it in full
at Step 2 and apply it. Everything about *what* the stations are and *whether* the seed can be split
lives there — its § *What a station is, and what it is not*, § *The checklist you were handed is a
proposal*, § *How one seed becomes 1 to N stations*, § *Every station carries a reached-when that can
be checked against the world*, § *The six defects, hunted by name*, § *A divergence from the proposal
is logged in the seed*, § *What you do not write* and § *When you stop*. None of it is repeated here,
and where a step below needs a judgment it names the section that makes it.

**A seed's shape** is `<CORE>/templates/journey-templates/nemawashi_template.md`, which fixes the
checklist's form and how terse a station line has to be. The prompt points at it too. Neither this file
nor the prompt restates it.

## Posture

**PM only.** Run in a `pm:` session or as the `pm` subagent. Invoked from anywhere else, halt at once,
say the posture is wrong, and name the way in. The seat's contract is
`<CORE>/roles/loaders/pm_global.md`, and the gate is what makes this skill that seat's — its
§ *Skills toolbox (reminder)* names it, and its § *Responsibilities* places this move second, between
the pick and the station-open.

The gate is about the seat, not about the session's liveness. This move is interactive with the owner
by design, and a live session invoking it is the ordinary way in.

## Input

**The project** — `system/projects/<project>/`. If none is supplied, ask which one; the PM cannot work
undirected. Everything else the run needs is resolved from there, and the prompt's § *Inputs you work
from* fixes what is read and which input wins where two disagree.

The run works in the instance it was started in. It opens no worktree and cuts no branch, so the
re-cut checklist is in the seed the moment the run ends.

**Where the product's code runs.** If seeing what the product does today means running any of its
code — a check, its command, an import — run it in a disposable copy: a fresh clone at the commit you
are reading (`git clone --quiet <repo> <scratch> && git -C <scratch> checkout --quiet <sha>`), never
the product's main checkout. Running it there leaves files behind — a Python `__pycache__/`, a build
directory — and the chain halts this run for every entry it finds there that was not there at launch
(`<CORE>/roles/CROSS_ROLE.md` § *Every seat — a run leaves the product's main checkout as it found
it*). Run the checks from a subshell, never `cd` your own shell into the copy, and remove the copy when you have read the result, in a command of its own run from outside it. Reading the code needs no copy.

## Workflow

### Step 1 — Gate, then resolve the seed

Check the posture (§ *Posture*) and halt there rather than proceeding.

Resolve `<nema>` = `system/projects/<project>/journey/nemawashi`. The picked seed is the **single item
at that root** — a file, or a folder holding `seed.md` — excluding `README.md` and the `unpicked/`,
`trail/` and `drop/` subfolders. For a folder-seed, `seed.md` is the one file this skill ever reads or
rewrites; the folder's own report/recommendation files are untouched.

**Gate A — is a seed picked at all?** If the root holds no seed item, there is nothing to split. Stop,
say so, and name the pick as the move that comes first — `nemawashi-pick`.

**Gate B — is the seed being walked?** Check `system/projects/<project>/journey/tobiishi/` for a change
unit at its root, and read the seed for an ad-hoc arc belonging to it that has not finished. If either
is open, **stop and say what is open.** A seed is not modified mid-walk — the route it is being walked
on would change underneath the session walking it. The resolution is an order rather than a merge: the
open work seals or is set down first, then this skill runs.

An empty change-unit slot passes this gate silently.

### Step 2 — Read the method, then split

Read `prompts/rich.md` in full, then
`<CORE>/templates/journey-templates/nemawashi_template.md`. Apply them. Every judgment this run makes —
what counts as a station, how many the seed becomes, where the boundaries fall, what each reached-when
claims, the order, and whether the seed can be split at all — is made there, including the four cases
that stop the run.

### Step 3 — Rewrite the checklist in place

Replace the seed's route section with the route, one line per station in the shape the template fixes.
Where the seed has no such section, add it in the template's position. **For a folder-seed, the rewrite
lands in `seed.md`** — the one file inside the folder this skill ever edits.

**The route is the section whose heading begins `## Stations`** — match that prefix, never the full
string. The template writes the long form at its `:64` and calls it `## Stations` at `:32`, and seeds
on disk carry several spellings between those two, so a full-string match reads a seed that has a route
as one that has none. `tobiishi-open`'s Step 4 keys on the same prefix, and it routes callers here.

Two rules bound the edit, and both are about what you do **not** touch:

- **An already-ticked item is never re-ordered, re-worded or un-ticked.** A `[x]` records a station
  that was really reached and whose file is in `shukuba/trail/`; the record on disk would disagree with
  the seed the moment you moved it. Re-cut only what is still `[ ]`.
- **No other section changes**, except the divergence lines the prompt's § *A divergence from the
  proposal is logged in the seed* requires. Those go in the seed's own prose, one line per departure —
  never a new section, never a table, never appended to a checklist line.

Write no station file and no `change_request.md`. Both are later moves, and the prompt's § *What you do
not write* says why.

### Step 4 — Commit

Per `<CORE>/doctrine/governance/commit_via_builder.md`, staging the seed and nothing else, with
`--skill stations-from-seed` and `--prompt stations-from-seed/rich` as this run's producing pair, and
`--role PM`. The directional is the project's — `Agari: <project> — progress: <what the route now
says>` — since settling a route advances the seed toward its terminus.

### Step 5 — Close, or stop

On a clean close, report: how many stations the seed now carries, how many it arrived with, every
divergence and its reason, and the next move — **open the first unticked station** — `shukuba-open` — and then `tobiishi-open` for the change
units that reach it.

On a stop, report the case from the prompt's § *When you stop*, commit nothing, and halt. A partial
checklist is worse than none: it reads as a settled route.

---

## Outputs

| File / effect | Produced when |
|---|---|
| The picked seed's `## Stations — dynamic checklist` rewritten, one commit | Success (Step 3) |
| Divergence lines in the seed's prose, same commit | The re-cut departed from the proposal |
| No change; the pick named as the move that comes first | The seedbed root holds no seed (Gate A) |
| No change; what is open, named | A change unit or ad-hoc arc is unfinished (Gate B) |
| No change; the stop case named | The prompt's § *When you stop* fired (Step 2) |

The seed — `seed.md` alone, for a folder-seed — is the only file this skill ever writes, and it writes
at most one commit per run.

---

## Critical Rules

- **The seed is the only file that changes** — `seed.md` alone, for a folder-seed. No station file, no
  `change_request.md`, no seed of your own in `unpicked/` — stocking the pool is the **Principal PM**'s.
- **A ticked item is history.** Never re-order, re-word or un-tick an `[x]`; its station's record is in
  `shukuba/trail/` and would contradict you.
- **Never split a seed being walked.** Gate B stops the run. The fix is an order — the open work seals
  or is set down first — never a bundled edit and never a silent one.
- **Split, don't re-cut the seed.** What the work *is* was settled by the cut and the Agari behind it.
  Re-cutting the route is this skill's; changing the subject is another seat's.
- **Every divergence is logged.** A re-cut that departs from the proposal and says nothing leaves the
  next reader unable to tell it from a careless one. The prompt makes this mandatory.
- **The method is the prompt's.** Everything about what a station is and whether the split can be made
  lives in `prompts/rich.md`. A second copy here is a copy free to drift.
