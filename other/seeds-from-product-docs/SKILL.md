---
name: seeds-from-product-docs
description: >-
  Principal PM-posture skill that cuts a product's settled documents — its SDD, FDR, ADR records and
  NFDR — into 根回し Nemawashi seeds, each walkable on its own, each with its own station checklist,
  written into the owning project's candidate pool. The second of that seat's two cutters, beside
  seeds-from-idea; this one starts from a document set already designed, ordered and locked, and
  draws out the work nobody has drawn yet. Four kinds come out — work on the product, a
  document the product's own records name and nobody wrote, a change asked of a definition-tier
  document through its open-issues companion, and a project that has to exist first. Requires
  Principal PM posture and halts outside a principal-pm session or the principal-pm subagent. It
  opens no worktree and no branch — it writes and commits in the instance it was started in, so the
  seeds are in the pool the moment the run ends. The cut never
  interviews — meeting something the repository cannot settle, it commits what it has, names the
  case and halts.
when_to_use: >-
  Trigger phrases — "cut seeds from the docs", "cut the product's documents", "seed this product",
  "the SDD is settled, cut it", "draw the work out of the design", "seeds-from-product-docs". It also
  fires when a product's definition chain has just settled and seeds are expected at the end of it,
  and on a later re-cut once earlier seeds have been walked. Do not use for cutting an idea or a
  stray seed (seeds-from-idea), picking or walking a seed (the PM's), un-picking, parking or retiring
  a journey item, sealing a change unit (tobiishi-seal), or authoring a product document.
license: MIT
metadata:
  author: Eyal Golan
  version: "2.6.0"
  created: "2026-09-02"
  category: journey
  tags: nemawashi, seeds, product-documents, sdd, principal-pm, journey
  risk: safe
---

# seeds-from-product-docs

## Purpose

Cut a product's **settled documents** into 根回し Nemawashi seeds. What arrives is a document set that
has already been argued to settlement — designed, ordered, locked and bound — and what leaves is a set
of seed files a PM can pick and walk without reading any of it.

**This file is the orchestrator.** It owns the posture gate, how the run resolves the product and the
project that owns it, and the ordered steps. Everything a cut does *around* the cut — where the run
works, the folder and the file name each seed gets, the trace-back line every
seed carries, what a run may move in a seedbed, the commit, and the shape of a close and of a stop —
is `<CORE>/prompts/principal_pm_cut_seeds_run.md`, shared with the seat's other cutter and not restated
here.

**The method is `prompts/rich.md`** — the one body this file points
at. Read it in full at Step 3 and apply it. Everything about *what* to cut and *whether* to cut lives
there: its § *Inputs — four you draw from, five you read against*, § *What the Agari and the Michi are doing here*,
§ *Four kinds of seed*, § *Every seed traces back to the documents it was drawn from*, § *Before you
cut — the skeleton is not yours*, § *Priority and incremental slicing*, § *What the SDD's order and
its slice→seed map bind you to*, § *Sweep the product's own seedbed, in all three positions* and
§ *What this lens decides, and what it does not*. That lens extends
`<CORE>/prompts/principal_pm_cut_seeds.md`, which holds the grounding pass, the sweep's three
outcomes, the Michi check every seed passes and names the Way for, the four stops, the no-interview
rule and the re-run fold — read it too, as the lens directs. None of it is repeated here.

**A seed's shape** is the template `<CORE>/templates/journey-templates/nemawashi_template.md`, which
fixes its sections, its checklist and how terse it has to be. The lens points at it too. Neither this
file nor the lens restates it.

## Posture

**Principal PM only.** Run in a `principal-pm:` session or as the `principal-pm` subagent. Invoked
from anywhere else, halt at once, say the posture is wrong, and name the way in. The seat's contract
is `<CORE>/roles/loaders/principal_pm_global.md`, and the gate is what makes this skill that seat's
(§ *Skills toolbox (reminder)* there names it).

The gate is about the seat, not about the session's liveness. A live session invoking this skill is
the ordinary way in; the lens's no-interview rule draws that line and it is not redrawn here.

## The run's shape

`<CORE>/prompts/principal_pm_cut_seeds_run.md` is the run's shape. Read it; this file adds only what is
below.

**One move it grants that this cut never makes:** the shared file leaves a cutter's moves on its own
input to the skill. This one has none — its input is a set of product documents, which the cut reads
and never writes. A run that finds itself editing a document it drew from has taken the upstream
kind's work and skipped the companion it belongs on (the lens's § *Four kinds of seed*).

## What this run is given, and how it resolves it

**The invocation names a product, or the project that owns it, or a satellite-qualified pair.** All
three resolve to the same two things, and the run needs both:

- **The project** — `system/projects/<project>/`, whose `agari.md` is the cut's filter and its routing
  key, and whose `journey/nemawashi/` is the seedbed the seeds land in and the one the sweep reads.
- **The product** — the path `system/projects/<project>/project.md` names, which is where the
  documents are. It may sit inside the instance or outside it, so read it from `project.md` rather
  than assuming either.

Resolve both **against the instance the run was started in**, for the reason the shared file gives.
Then check the product path holds what the lens draws from, on the lens's own terms — which documents those are, what counts
as settled, and what the owner may rule instead are its § *Inputs — four you draw from, five you read
against*. Halt where it says to halt.

**When the invocation names no product at all**, or names one that resolves to two projects, say what
you found and stop. Picking which product to cut is not this run's call.

## Workflow

### Step 1 — Gate

Check the posture (§ *Posture*) and halt there rather than proceeding. Open no worktree and cut no
branch: this run works in the instance it was started in, and its seeds are in the pool the moment it
commits — the shared file's § *Where the run works*.

### Step 2 — Resolve the product and its project

Per § *What this run is given, and how it resolves it*, including the settled-input check. Halt there
rather than cutting against a shape that is about to move.

### Step 3 — Read the method, then cut

Read `prompts/rich.md` in full, then the sibling lens it extends
and `<CORE>/templates/journey-templates/nemawashi_template.md`. Apply them. Every judgment the cut
makes — which document a candidate is drawn from, whether the Agari lets it through, which of the four
kinds it is, what is worth landing first, how much of the draw this cut takes, and whether the cut can
be made at all — is made there. One thing the lens fixes is not a judgment: **every run checks every FDR rule,
ADR binding and NFDR obligation against the product before it orders anything**, whatever the SDD's
slices yield — the lens's § *Inputs — four you draw from, five you read against*.

### Step 4 — Write the seeds

One file per seed, at the path and under the name the shared file fixes, in the shape the template
fixes, each carrying its trace-back line — whose fixed opening is the shared file's and whose content
is the lens's § *Every seed traces back to the documents it was drawn from*.

**An upstream-kind seed owes a second write**: the item on the owing document's own
`*_open_issues.md` companion, in that companion's item shape, recording that this seat raised it. The
seed alone is not the raise. Both are this run's, by hand — the lens says so.

**Write no station**, and pick nothing this cut produced. Opening a station and picking a seed are the
PM's moves, which is the whole reason a cut writes into a pool.

### Step 5 — Make the moves, if any

Only the ones the shared file allows. This cut has none of its own (§ *The run's shape*).

### Step 6 — Commit

As the shared file directs, with `--skill seeds-from-product-docs` and
`--prompt seeds-from-product-docs/rich` as this run's producing pair.

### Step 7 — Close, or stop

As the shared file directs. Two things are this cut's own on a clean close:

- **Say what you did not cut.** A document set is rarely cut exhaustively in one pass, so the report
  names which parts of the draw are still uncut and what would make them ready — the lens's
  § *Priority and incremental slicing*. It covers all four documents: the SDD's slices left, and
  what the four-document pass found in the FDR, the ADR records and the NFDR and did not cut, or
  that it found nothing there. A list that names slices only is not this account.
- **Say which upstream items you raised**, by companion path and item, so the owner knows which
  definition documents are now owed a re-run.
