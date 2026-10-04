---
name: ideate
description: >-
  Structured idea generation for a project or a blank-slate problem — ideas
  worth pursuing, not the first one that sticks. Grounds in the current repo
  (AGENTS.md/README) or a freeform problem, then diverges across named lenses
  (adjacent user, removed constraint, inversion, and more) so a run yields
  range, not ten variations of one idea. Fights premature convergence —
  nothing judged until the divergence quota is met — then verdicts each idea
  EXPLORE/PARK/DROP, where DROP is cheap. EXPLORE items become seeds for
  priorart (is it novel?) or feature (build it); verdicts persist in
  out/ideate/tracker.md so repeat runs open with what's new. Keyless. Use to
  generate, brainstorm, or explore ideas or new directions for a project or
  problem — e.g. "/ideate", "/ideate <topic>", "brainstorm features for X".
  For whether an idea already exists use priorart; for competitor features
  use scout; for choosing between named options use verdict.
---

# ideate — diverge before you converge

`/ideate` — generate ideas for THIS repo (reads its AGENTS.md/README)
`/ideate <topic|problem>` — generate ideas for an arbitrary problem, no repo needed

Answer one question: **what could this become that isn't obvious yet — and
which of those directions actually deserves effort?** Both halves matter. A
session that only sprays ideas is a whiteboard; one that judges before it
has range is just the first idea wearing a verdict. The deliverable is a
short list of directions each carrying its own reason to live or die.

The enemy the whole skill is built against is **premature convergence** —
latching onto the first plausible idea and spending the session polishing
it. Every step below exists to hold divergence open long enough to be worth
converging on.

## Step 0 — Frame the ground

You cannot diverge from nothing; fix a starting point first.

- **With a repo** (`/ideate` alone): read `AGENTS.md` (the map skill writes
  it), `README`, and the top-reacted open issues. Distill the project's
  **job in one sentence** and its **differentiation axis** — the thing it
  does that alternatives don't, which every later verdict is judged against.
- **With a topic** (`/ideate <problem>`): restate the problem in one
  sentence and name the **user** and the **constraint that hurts most**.
  Missing pieces are assumptions — state them, don't invent facts.
- Read `out/ideate/tracker.md` if it exists: ideas already generated,
  verdicts already made. A DROPped idea isn't re-raised unless something
  changed; repeat runs open with **"Since last ideate"** — what's new in the
  repo or problem since.

**Completion criterion:** job, user, and differentiation/constraint written
down before any idea is generated.

## Step 1 — Diverge (judgment forbidden here)

Generate ideas by working the **lenses** in
[`references/lenses.md`](references/lenses.md) — do not freehand a flat list,
which is how every session collapses into variations of one idea. Take each
lens in turn and force at least one idea from it, even a weak one; range
comes from the lenses being different, not from trying harder on one.

Hard rule: **no evaluating, ranking, or "but that won't work" until the
quota is met** — aim for at least two ideas per lens worked. Judging mid-
divergence is premature convergence by another name; a bad idea from an
unworked lens is worth more here than a safe idea restated.

**Completion criterion:** every applicable lens worked, quota met, ideas
captured verbatim — no pruning yet.

## Step 2 — Cluster and sharpen

Now converge, but only halfway. Group the raw ideas into clusters of the
same underlying bet; within each cluster keep the sharpest single statement
and fold the rest into it. Kill exact duplicates. For each survivor write
one line: **what changes for the user if this exists.** An idea whose
user-impact line can't be written is a DROP waiting to happen — surface that
now, not after building.

**Completion criterion:** a deduplicated list, each survivor with a one-line
user impact.

## Step 3 — Verdict each survivor

Every surviving idea gets exactly one label, with a reason:

- **EXPLORE** — worth real effort next. Must clear two bars: it advances the
  differentiation axis (or genuinely relieves the worst constraint), and its
  effort is justified by that impact. "It sounds cool" clears neither.
- **PARK** — plausible but not now; record the trigger that would revive it.
- **DROP** — off-axis, redundant, or impact doesn't pay for effort. DROP is
  the cheap default; a session that EXPLOREs everything has judged nothing.

Hand off cleanly: each **EXPLORE** is a ready **seed** — route it to
`priorart` (does it already exist before you build?) or straight to
`feature` (build it). Name the handoff in the verdict.

**Completion criterion:** every survivor labeled EXPLORE / PARK / DROP with a
reason, and every EXPLORE names its next skill.

## Step 4 — Persist

Append the run to `out/ideate/tracker.md`: date, the frame (job + axis), and
every idea with its verdict and reason — including DROPs, so they aren't
re-raised next run. This is the memory that lets the next `/ideate` open with
"Since last ideate" instead of regenerating the same list.

**Completion criterion:** tracker written; run reproducible from it.
