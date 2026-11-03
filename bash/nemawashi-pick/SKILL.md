---
name: nemawashi-pick
description: >-
  PM-posture skill that picks the next 根回し Nemawashi seed for a project — the model chooses one
  seed from the candidate pool, and a script decides whether that choice may be made before the
  seed moves `unpicked/` → the seedbed root in one commit, which also appends the pick to the
  instance's Principal PM context when it has one. Halts outside a pm session or the pm subagent.
  Use when a project has no active seed and the next one has to be chosen — "pick the next seed",
  "what should we work next", "pick a nemawashi", "nemawashi-pick". Do not use for un-picking
  (nemawashi-unpick), cutting seeds (seeds-from-idea, seeds-from-product-docs), splitting the picked
  seed into stations (stations-from-seed), retiring or dropping a seed (nemawashi-retire,
  nemawashi-drop), or the instance seedbed under system/nemawashi/.
license: MIT
metadata:
  author: Eyal Golan
  version: "1.7.0"
  created: "2026-09-14"
  category: journey
  tags: nemawashi, pick, pm, journey
  risk: safe
---

# nemawashi-pick

**The prompt owns judgment; the code owns validity.** `prompts/thin.md` chooses the seed.
`scripts/pick.py` refuses any pick that may not be made, and makes the move. This file only runs
the two in order.

## Posture

**PM only.** Run in a `pm:` session or as the `pm` subagent; anywhere else, halt, say the posture is
wrong, and name the way in. The move commits with nobody asked, so the seat is the check.

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

Run everything from the instance root. `PICK=<CORE>/../skills/pm/.claude/skills/nemawashi-pick/scripts/pick.py`.

### 1 — Can a pick happen?

```bash
python3 "$PICK" --root . --project <project> check
```

It prints the pool, or `REFUSED: <reason>` and exits 1. On a refusal, report the reason and stop.

### 2 — Choose

Read `prompts/thin.md` and do what it says. Write the answer to a record file **outside the
repository** (the scratchpad or `$TMPDIR`) — nothing else is written:

```
Seed: <seed name, as the pool lists it>
Condition: none

<why it is the best next move>
```

`Condition:` carries `none`, or the condition that prevents starting it.

### 3 — May it be picked?

```bash
python3 "$PICK" --root . --project <project> apply --record <record file>
```

It re-checks step 1, then refuses unless the record names exactly one seed, that seed is in
`unpicked/` and in neither `trail/` nor `drop/`, its checklist is not fully walked, the condition is
`none`, and the paths a pick writes — this project's `journey/` and
`system/contexts/CONTEXT_PPM.md` — are still clean. Another project's edit elsewhere in the shared
checkout does not refuse it. On success it moves the seed and prints its old and new paths.
On a refusal, report the reason and stop — nothing was moved.

It then appends the pick to `## Picked seeds` in `system/contexts/CONTEXT_PPM.md`, the Principal
PM's view of the seeds picked across every project, and prints that path third. Several projects
hold a picked seed at once, so the line is only appended and no other line is touched. The move that
takes the seed off its root removes it (`<CORE>/docs/journey_move.md` § *The Principal PM's
picked seeds*). An instance with no such file or section prints
`no PPM context — skipped` third instead, and the pick stands.

### 4 — Commit

Per `<CORE>/doctrine/governance/commit_via_builder.md`. Drop `--add` when step 3 printed the skip line:

```bash
python3 "<CORE>/tools/commit_builder.py" --repo . commit \
  --staged "<old path>" "<new path>" --add "<context path>" \
  --subject "pick: <seed>" --body "$(cat <record file>)" \
  --actor pm --skill nemawashi-pick --prompt nemawashi-pick/thin \
  --directional "Agari: <project> — progress: <seed> is the active seed" \
  --surface "Claude Code" --co-authored-by "<your model> <noreply@anthropic.com>"
```

### 5 — Report

The seed picked, why, and the next move: `stations-from-seed`.
