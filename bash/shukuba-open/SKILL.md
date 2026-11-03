---
name: shukuba-open
description: >-
  PM-posture skill that opens the next 宿場 Shukuba station for a project — the model writes the
  station for the next unticked item on the active seed's route, in the shukuba template's shape, and
  a script decides whether that station may be opened before it lands at the shukuba root in one
  commit. A station of that seed parked for that item is taken up again instead, its reached-when
  unchanged. Halts outside a pm session or the pm subagent. Use when a project has an active seed and
  no open station — "open the next station", "open the shukuba", "start the next leg",
  "shukuba-open". Do not use for picking or un-picking a seed (nemawashi-pick, nemawashi-unpick),
  cutting or re-cutting the route (stations-from-seed, shukuba-refine), opening a change unit
  (tobiishi-open), closing or parking a station (shukuba-retire, shukuba-park), or the instance router
  under system/shukuba/.
license: MIT
metadata:
  author: Eyal Golan
  version: "1.4.0"
  created: "2026-09-15"
  category: journey
  tags: shukuba, open, pm, journey
  risk: safe
---

# shukuba-open

**The template owns the station; the code owns validity.** The station is written from
`<CORE>/templates/journey-templates/shukuba_template.md`, whose comment block is the whole method for
what a station carries and how its reached-when is written. `scripts/open.py` refuses any station that
may not be opened, and puts it in place. This file only runs the two in order.

## Posture

**PM only.** Run in a `pm:` session or as the `pm` subagent; anywhere else, halt, say the posture is
wrong, and name the way in. The station commits with nobody asked, so the seat is the check.

## Input

**The project** — `system/projects/<project>/`. If none is named, ask. Project journeys only.

**Where the product's code runs.** If seeing what the product does today means running any of its
code — a check, its command, an import — run it in a disposable copy: a fresh clone at the commit you
are reading (`git clone --quiet <repo> <scratch> && git -C <scratch> checkout --quiet <sha>`), never
the product's main checkout. Running it there leaves files behind — a Python `__pycache__/`, a build
directory — and the chain halts this run for every entry it finds there that was not there at launch
(`<CORE>/roles/CROSS_ROLE.md` § *Every seat — a run leaves the product's main checkout as it found
it*). Run the checks from a subshell, never `cd` your own shell into the copy, and remove the copy when you have read the result, in a command of its own run from outside it. Reading the code needs no copy.

## Workflow

Run everything from the instance root. `OPEN=<CORE>/../skills/pm/.claude/skills/shukuba-open/scripts/open.py`.

### 1 — Can a station open?

```bash
python3 "$OPEN" --root . --project <project> check
```

It prints the active seed and the next unticked item on its route — `Item:`, `Slug:` and `Line:` —
or `REFUSED: <reason>` and exits 1. On a refusal, report the reason and stop.

**A `Parked:` line means the station already exists.** Go to step 3b and write nothing: a parked
station is taken up again against the bar it was opened against (the template's comment block). Read
that bar first under the comment block's *AND SO IT CAN BE MET WHERE THE STATION STANDS*; where it
fails, stop as step 2 does, and take nothing up.

### 2 — Write

Read the active seed, the project's `agari.md`, and the template with its comment block. Write the
station for the item step 1 named, in the template's shape, to a file **outside the repository** (the
scratchpad or `$TMPDIR`) — nothing else is written.

**Where the item cannot be given a reached-when a fresh session could check, write nothing.** Report
why and stop: "A station you cannot check against the world is not a station"
(`<CORE>/roles/loaders/pm_global.md`, the posture above § *What you own*), and the fix is the route, not the bar.
The same holds where the item's reached-when needs work that a later station lands, or that no
station on the route does — the comment block's *AND SO IT CAN BE MET WHERE THE STATION STANDS*.
Write nothing rather than a narrower bar. Name the gate, the clause, and the station that lands the
work or that none does, and the re-cut owed: `stations-from-seed`'s before any unit of this seed has
landed, `shukuba-refine`'s after one has.

### 3a — May it be opened?

```bash
python3 "$OPEN" --root . --project <project> apply --station <station file>
```

It re-checks step 1, then refuses unless the station's `*Item` line names the item number, the seed
as its triple and the slug, and the station carries `## What it is`, `## Reached when` and
`## Guardrail`, each once and none empty or left as the template's placeholder. On success it writes
the station to `journey/shukuba/<today>_<slug>.md` and prints that path. On a refusal, report the
reason and stop — nothing was written.

### 3b — Take it up

```bash
python3 "$OPEN" --root . --project <project> take-up
```

It re-checks step 1, moves the parked station whole back to `journey/shukuba/`, and prints its old
and new paths.

### 4 — Commit

Per `<CORE>/doctrine/governance/commit_via_builder.md`. The body is `Item <n> on <seed>: <line>`, and a
route line carries backticks, so write it to a file outside the repository and pass it as
`--body "$(cat <body file>)"`. A written station:

```bash
python3 "<CORE>/tools/commit_builder.py" --repo . commit \
  --add "<station path>" \
  --subject "open shukuba: <YYYY-MM-DD>_<slug>" --body "$(cat <body file>)" \
  --actor pm --skill shukuba-open \
  --directional "Shukuba: <YYYY-MM-DD>_<slug> — progress: opened from item <n> of <seed>" \
  --surface "Claude Code" --co-authored-by "<your model> <noreply@anthropic.com>"
```

A station taken up is a move, so its commit is `<CORE>/docs/journey_move.md` § The commit's — both halves
in `--staged`, no `--skill`:

```bash
python3 "<CORE>/tools/commit_builder.py" --repo . commit \
  --staged "<old path>" "<new path>" \
  --subject "open shukuba: <YYYY-MM-DD>_<slug>, taken up from parked/" --body "$(cat <body file>)" \
  --actor pm \
  --directional "Shukuba: <YYYY-MM-DD>_<slug> — progress: taken up from parked/" \
  --surface "Claude Code" --co-authored-by "<your model> <noreply@anthropic.com>"
```

Then do what `<CORE>/docs/journey_move.md` § After the move, say which pointers it broke says.

### 5 — Report

The station opened or taken up, its reached-when, and the next move: `tobiishi-open`. On a stop, what
stopped it and, for a bar that cannot be met where it stands, the re-cut owed.
