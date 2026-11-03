---
name: seeds-from-idea
description: >-
  Principal PM-posture skill that cuts an idea — something said in passing, a note, or a seed that
  someone else set down — into 根回し Nemawashi seeds, each one walkable on its own, each with an
  owning project and its own station checklist, written into that project's candidate pool. Requires
  Principal PM posture and halts outside a principal-pm session or the principal-pm subagent. It opens no
  worktree and no branch — it writes and commits in the instance it was started in, so the seeds
  are in the pool the moment the run ends. The cut itself never
  interviews — when it meets something the repository cannot settle it
  commits what it has written, names the case, and halts there, so a re-run folds that work instead of
  cutting the idea again from nothing. Use when an idea needs cutting into seeds, when a discussion or
  a note should become seeded work, or when an unstructured ask has to end up as seeds a PM can pick.
when_to_use: >-
  Trigger phrases — "cut this idea into seeds", "cut the idea", "seed this", "turn this into nemawashi
  seeds", "seeds-from-idea". It also fires when an idea arrives with no structure and the
  expectation is seeds at the end of it, including when the thing to be cut is itself a seed. Do not
  use for picking a seed or walking one (the PM's), un-picking, parking or retiring a journey item
  (nemawashi-unpick, nemawashi-retire, shukuba-park, shukuba-retire), sealing a change unit
  (tobiishi-seal), or authoring a product document (the definition family and product-fdr).
license: MIT
metadata:
  author: Eyal Golan
  version: "3.0.2"
  created: "2026-08-30"
  category: journey
  tags: nemawashi, seeds, idea, principal-pm, journey
  risk: safe
---

# seeds-from-idea

## Purpose

Cut one **idea** into 根回し Nemawashi seeds. The idea arrives as a **brief** — the words of whoever
asked, quoted with where they were said, and the evidence beside them, each checkable
(`templates/brief.md`). What leaves is a set of seed files a PM can pick and walk without ever meeting
the idea.

**This file is the orchestrator.** It owns the posture gate, the brief and who writes it, the method
this cut applies, and the moves that are an *idea-seed*'s alone. Everything a cut does around the cut — where the run works,
the folder and the file name each seed gets, the trace-back line every seed
carries, what a run may move in a seedbed, the commit, and the shape of a close and of a stop — is
`<CORE>/prompts/principal_pm_cut_seeds_run.md`, shared with every other cutter and not restated here.

**The method is `prompts/rich.md`** — the one body this file points at. Read it in full at Step 2
and apply it. That lens extends `<CORE>/prompts/principal_pm_cut_seeds.md`, which holds everything
about *what* to cut and *whether* to cut: its § *What an idea is, and what it is not*, § *Ground every
claim before you cut*, § *Sweep the seedbeds before you write one*, § *One idea becomes 1 to N seeds*,
§ *Every seed gets an owning project*, § *The Michi is checked on every seed, and a seed says which Way
it serves*, § *When a routing seed is earned*, § *You do not interview* and § *When you stop*. Read
it too, as the lens directs. The lens tightens three of those for an idea cut — how many seeds, when a
routing seed is planted, and which inputs may ground a seed — and holds the output to
`seeds-from-product-docs`'s bar: the ask quoted, four kinds of seed, its ordering, the security flag, a
close that accounts for the whole ask, and a stop on an unsettled input. Where the two disagree, the
lens governs. None of either is repeated here, and where a step below needs a judgment it names the section
that makes it.

**A seed's shape** is the template `<CORE>/templates/journey-templates/nemawashi_template.md`, which
fixes its sections, its checklist and how terse it has to be. The base prompt points at it too. Neither
this file nor either prompt restates it.

## Posture

**Principal PM only.** Run in a `principal-pm:` session or as the `principal-pm` subagent. Invoked
from anywhere else, halt at once, say the posture is wrong, and name the way in. The seat's contract
is `<CORE>/roles/loaders/principal_pm_global.md`, and the gate is what makes this skill that seat's
(§ *Skills toolbox (reminder)* there names it).

The gate is about the seat, not about the session's liveness. A live session invoking this skill is
the ordinary way in; the base prompt's § *You do not interview* draws that line and it is not redrawn here.

## The run's shape

`<CORE>/prompts/principal_pm_cut_seeds_run.md` is the run's shape. Read it; this file adds only what is
below.

## Writing the brief in a session

**The session drafts the brief and the owner confirms it** — the owner's call, 2026-10-24. Write it
from `templates/brief.md`, by the rules in `<CORE>/templates/brief_template.md`'s DRAFTING ONE IN A
SESSION block, which `ad-hoc-plan` drafts by too. The base prompt's § *You do not interview* binds from the
confirmation on.

`nemawashi-refine` writes its brief itself, inside its own run, and nobody confirms it: its
`## The ask` quotes the recommendation it is answering, at its lines, which the quote check holds it to.

## The cut's report

**This cut writes one file the shared file's § *Where a seed lands, and under what name* otherwise
forbids** ("no report file"), and its § *Close, or stop* reports a stop "in the run's closing message
rather than in a new file"; this cut reports a stop in both. The file is
`<the brief's stem, with _brief replaced by _report>.md`, beside the brief, in the shape of
`templates/report.md`. The owner's call, 2026-10-24. The reason is the unattended path: a cut started
inside `nemawashi-refine` has no one reading its closing message, and refine reads this file instead
to record what the cut did. It is written on every run, a stop included, and committed with the brief —
except on a Step 1 stop, where nothing is committed: the brief is wrong and is fixed first, and the
report is left beside it for the caller to read. The closing message still says what it says; the file
is what lasts.

## What this run may move that a cut in general may not

The shared file grants a cutter no move on its own input. This one has two, because its input is
itself a seed and the instance seedbed is this seat's alone.

**The idea-seed the run is cutting.** The sweep finds it, and that is not the duplicate stop — the
base prompt's § *Sweep the seedbeds before you write one* says so and passes the move here. **Both
directions are open on it**: an un-pick, root → `unpicked/`, and a pick, `unpicked/` → root — one file
and nothing else either way, per `<CORE>/docs/journey_move.md` § *The pick and the un-pick*.
A root holds one active idea at a time, so a pick into an occupied root un-picks that occupant
first. **The run may pick the idea-seed** — the owner's call, 2026-08-30 — because the
instance seedbed is this seat's alone and no PM can reach it. At instance level every one of these
moves is this seat's own hand, since the project-level pick and un-pick skills do not serve that
seedbed.

**Both of those moves now land immediately**, since this run has no branch to hold them
(§ *Where the run works* in the shared file). The 2026-08-30 permission was granted when a move sat
on a branch the owner had still to land, so it cost nothing to make and nothing to undo. It costs
both now. Make the move where the cut leaves the seed's position plainly false, and where it does
not, leave the seed alone and say in the report which move you did not make.

**Retiring the idea-seed is not the run's.** It waits on the cut being approved — not on the run, and
not on the merge — the owner's call, 2026-08-30. The default is to leave the seed where it is, and to
move it only where the cut has made its position false.

**Where it goes when that day comes is `trail/`, moved by hand** — an instance idea-seed's moves are a hand's (`<CORE>/docs/journey_move.md`
§ *The two levels, and what exists at each*). A cut idea-seed
ripened into work, which is what `trail/` records — `<CORE>/templates/nemawashi_template.md` states the
criterion and `<CORE>/docs/michi_agari.md` § Quick reference keeps it apart from `drop/`. It is not a
drop: a dropped idea was ruled out, and this one produced the seeds. Say so to whoever is owed the
move; the run itself still does not make it.

## Workflow

### Step 1 — Gate, then resolve the idea

Check the posture (§ *Posture*) and halt there rather than proceeding. Open no worktree and cut no
branch: this run works in the instance it was started in, per the shared file's § *Where the run
works*.

**The idea arrives as a brief** — one file in the shape of `templates/brief.md`, beside this file,
at `system/projects/<project>/docs/seeds-from-idea/<YYYY-MM-DD>_<slug>_brief.md`, or at
`docs/seeds-from-idea/` in the instance root when the owning project is the instance or is left to the
cut. The brief is the cut's whole input: what it does not say, the cut does not know. Where the
invocation hands you a path, read that file. Where it hands you none, § *Writing the brief in a
session* says who writes it.

**Check its quotes before anything else is read:**

    python3 <CORE>/tools/check_brief_quotes.py <brief> --root "$(git rev-parse --show-toplevel)"

It prints one line per citation whose quote is not at its lines, and ends with a count on stderr of
the citations it checked and the ones it skipped as unresolvable. **Any line it prints stops the run**,
and so does a skipped citation naming a file in this instance — the root was wrong, and nothing was
checked. Only a citation into another repository, such as an external product, may stay skipped. A
brief whose `## The ask` is empty or `none` stops the run the same way — there is nothing to cut. On
such a stop, commit nothing and report it as § *The cut's report* says.

Resolve the brief's sources to what the seeds will cite, in the form the base prompt's § *Every seed
traces back to the idea it came from* gives for each kind of source — a journey artifact, any other
file, or conversation. Resolve them against that instance, for the reason the shared file gives. The
brief itself is cited too, by its path, so the seed's walker can open the input the cut read.

**The moves this cut has on its input seed land immediately**, since there is no branch holding them
back. The shared file's § *What the run may move, and what it does not* is what that costs, and its
rule — move only where you are certain, otherwise write the seed and report the move you did not
make — binds the two moves in § *What this run may move that a cut in general may not* above.

### Step 2 — Read the method, then cut

Read `prompts/rich.md` in full, then `<CORE>/prompts/principal_pm_cut_seeds.md` in full as the lens
directs, then `<CORE>/templates/journey-templates/nemawashi_template.md`. Apply them. Every judgment
the cut makes — does a claim survive contact with the repository, how many seeds there are and where
the lines between them fall, who owns each one, is a routing seed earned, can the cut be made at all
— is made there, and where the lens and the base disagree, the lens governs.

### Step 3 — Write the seeds

One file per seed, at the path and under the name the shared file fixes, in the shape the template
fixes, each carrying its trace-back line.

### Step 4 — Make the moves, if any

Only the ones the shared file allows, plus the two § *What this run may move that a cut in general may
not* adds.

### Step 5 — Commit

As the shared file directs, with `--skill seeds-from-idea` and
`--prompt seeds-from-idea/rich` as this run's producing pair. **The brief and the report go in the
commit of the scope the brief sits under** — a project's when it is in that project's `docs/`, the
instance's when it is at the root — so the input is on record beside what it became. Where the seeds
span scopes, every other scope's commit names the brief by its path in its body. The owner's call,
2026-10-24.

### Step 6 — Close, or stop

As the shared file directs, and also in the report file § *The cut's report* names. One thing is this
cut's own on a clean close: retiring the idea-seed waits on the cut being approved (§ *What this run may
move that a cut in general may not*), so the report says nothing about having retired it.
