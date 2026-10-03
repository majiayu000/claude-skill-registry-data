---
name: triangulate
description: >-
  Apply three lenses to one problem in a fixed order — recon (what is actually
  there), debug-mantra (is what I believe actually true), ponytail (what is the
  smallest thing that works) — with an explicit rule for how much evidence to buy
  before shrinking. Use when a task tempts you toward opposite errors at once:
  over-building against a blast radius nobody measured, or shipping a confident
  one-liner into a system nobody read. Trigger on /triangulate, and on "what is the
  right amount of work here", "am I over-thinking this", "am I under-thinking this",
  "how deep should I go", "give me the balanced take", "is this a big change or a
  small one". Do NOT fire when only one lens applies: a live bug in a system you
  already understand is /debug-mantra, greenfield is /ponytail, and planning a
  change to a known system is /recon then /swe.
argument-hint: "[subject]"
---

# Triangulate

Three lenses, one problem. Ground it, falsify it, then shrink it.

Every skill this one calls ships in `skills/` beside it — `recon`, `debug-mantra`, `ponytail`,
`swe`. Nothing here depends on an external skill pack.

## Step 0a — Should this fire at all?

Route to the single skill and stop, if the task is:

| Task | Route to |
|---|---|
| A live bug in a system you already understand | [debug-mantra](../debug-mantra/SKILL.md) |
| Greenfield — nothing exists to trace | [ponytail](../ponytail/SKILL.md) |
| A change to a known system, no over-build temptation | [recon](../recon/SKILL.md), then [swe](../swe/SKILL.md) |
| A typo, comment, or formatting change | none of the three — fix it |

**Two rows match: a live bug beats a planned change.**

**If the change would introduce, move, or replace a source of truth**, do not route away — that
question is not a lens conflict, it is an authority question. Answer it before Step 1, and treat the
decision as **irreversible** there regardless of how small the diff looks.

Triangulate fires only when **at least two** lenses would fire **and pull in opposite directions on
effort**. If the change is smaller than the sentence describing it, do not classify — fix it.

## Step 0b — Does this need to exist at all?

Ponytail rung 1, in one line. If the answer is no, say so and stop.

**This may end the run only if you can quote, verbatim, one of:**

- **(a)** a statement in the request itself that removes the need, or
- **(b)** the output of one read-only command you ran *this session*.

Memory, summaries, and beliefs about the code are not held facts. If the answer needs a second
command, a file read, or any inference — proceed to Step 1.

Do not assert "we don't need this" without the number. Ponytail forbids it: *"Can't actually
measure it? You have no profiler. Don't assert 'fast enough' blind, name the assumption and the
trigger to revisit."*

## The three lenses

| Lens | Axis | Question |
|---|---|---|
| recon | the **system** | What is actually there? |
| debug-mantra | the **claim** | Is what I believe actually true? |
| ponytail | the **response** | What is the smallest thing that works? |

The only genuine conflict between them is **how much evidence to buy**. Steps 1–2 settle it.

Order after Step 0: **recon → debug-mantra → ponytail.** Ponytail runs last.

## Step 1 — Classify the decision, not the task

Two axes. One line each. Under a minute.

- **Reversible** — delete it next week and nothing else moves.
  **Irreversible** — migration, published contract, stored data shape, an API others call, or
  anything with a rollback cost.
  **A change another repo or another person has already consumed is not reversible** — reverting
  your side does not un-break theirs. Measure reversibility at the far end of the radius, not in
  your own working tree.
- **Contained** — one file, or callers you have already enumerated *and read*.
  **Crossing** — other modules, contracts, stored state, other repos, other people.

If you cannot classify an axis, it is **crossing** and **irreversible** until one lookup says
otherwise. Spend the lookup.

## Step 2 — Read the floor

| | **Contained** | **Crossing** |
|---|---|---|
| **Reversible** | **none** — ponytail alone | **recon-lite + falsify** |
| **Irreversible** | **falsify** | **full** |

Read the floor from the cell, not from a count of how many axes went the hard way.

- **none** — say `triangulate → ponytail only, <reason>` and go. No card, no ceremony.
- **recon-lite + falsify** — one recon pass for the seams (who calls this, what writes this state,
  what crosses a boundary; `file:line` or it is an Unknown), then disprove *"that is all of them."*
  The seam read is what tells you what to falsify — a falsification with nothing enumerated never
  targets dynamic dispatch or string-based references.
- **falsify** — [debug-mantra](../debug-mantra/SKILL.md) step 3 against the single belief that makes this irreversible. Run
  the **disproof** first.
- **full** — [recon](../recon/SKILL.md) fan-out, then the mantra ledger across every observation. Ponytail then
  applies to the **fix**, never to the reading.

**The floor is a floor.** Buy more evidence freely; never buy less. "I'm confident" is not a reason
to drop a floor — confidence is what debug-mantra exists to attack.

## Step 3 — Ground (recon)

Run [recon](../recon/SKILL.md) at the floor's width. Its rules carry unchanged: the graph is a lead not a citation,
every edge a decision depends on is confirmed by reading the file, and anything unverified goes in
Unknowns rather than being smoothed into the findings.

Recon's own skip list still applies here. A floor of `recon-lite` on a subsystem you traced ten
minutes ago is satisfied by what you already hold — write it down, do not re-run it.

## Step 4 — Falsify (debug-mantra)

Take the belief the plan leans on hardest — the one whose failure costs the most, not the one you
are least sure of. Then apply [debug-mantra](../debug-mantra/SKILL.md):

- What is the cleanest **disproof**? Run that first.
- Does the belief hold against **every** breadcrumb so far, or only the most recent?
- If the belief rests on a screenshot, a rendered view, or memory, it is hypothesis-zero. Look at
  the raw artifact before anything inherits its shape.
- **If the disproof kills the belief:** record it in `FALSIFY`, then re-classify at Step 1 with what
  recon learned, or stop and report. A plan leaning on a dead belief does not proceed to Step 5.

Recite the full mantra only if this is also an active debug session.

## Step 5 — Shrink (ponytail)

Now, and only now, run [ponytail](../ponytail/SKILL.md) on the *implementation*. The ladder is
unchanged: does this machinery need to exist, stdlib, native platform, existing dependency, one
line, minimum code.

Two guards that matter more here than in ponytail alone:

- Ponytail shrinks the **mechanism**, never the requirement, and never the evidence floor from
  Step 2. Trust boundaries, error handling that prevents data loss, security, accessibility, and
  operational controls stay.
- Every seam recon found is either **covered** by the shipped shape or **named** in the card as
  skipped-with-a-trigger. A silently dropped seam is not laziness; it is a bug you have not met yet.

## The card

```
SUBJECT: <the change, one line>
CELL:    <reversible|irreversible> x <contained|crossing>  ->  floor: <none|recon-lite+falsify|falsify|full>
GROUND:  <seams, file:line — or "skipped: <reason>">
FALSIFY: <the load-bearing belief; what disproved it, or what it survived>
SMALLEST:<the shape shipped> — skipped: <X>, add when <Y>
UNKNOWNS:<what would change this answer, and the one command that settles it>
```

Worked example — rename an internal utility imported across 12 modules:

```
SUBJECT: rename fmt_money() -> format_currency() across the billing package
CELL:    reversible x crossing  ->  floor: recon-lite + falsify
GROUND:  12 static imports (billing/*.py, 9 files) + 1 dynamic lookup —
         billing/registry.py:44 resolves the name from a config string
FALSIFY: belief "grep found every caller" — DEAD. registry.py:44 never appears in a
         symbol grep. Re-classified: the config key is a consumed contract -> irreversible.
SMALLEST:keep the old name as an alias for one release; migrate the config key separately
         — skipped: the hard cutover, add when the config key is confirmed unused in prod
UNKNOWNS:other repos reading the same config key — `rg 'fmt_money' ../*/config/` settles it
```

Short card in chat. If recon's output is long, the map goes to `recon-<subject>.md` and the card
cites it — long output belongs in the file.

If writing the card would take longer than making the change, the cell was reversible + contained.
Say `triangulate → ponytail only` and go. This is ponytail rung 1 applied to triangulate itself.

## Neighbors

- [recon](../recon/SKILL.md) — the ground pass, Step 3.
- [debug-mantra](../debug-mantra/SKILL.md) — the falsification pass, Step 4.
- [ponytail](../ponytail/SKILL.md) — rung 1 at Step 0b, the shrink pass at Step 5.
- [swe](../swe/SKILL.md) — grades the resulting plan; triangulate feeds its Pillar 0 and Blast.

## Provenance

Designed and QA'd through two automated `/relay-xyz` rounds against the plan doc, 2026-08-28:
round 1 DeepSeek v4 Pro (dsh → OpenRouter), round 2 Qwen 3.8 Max (CommandCode). Both returned
"Changes requested"; both were right. The threads and the full disposition table are in
[`relay-system/2026-08-28/`](https://github.com/HiQS-Labs/XYZ-forge/blob/development/relay-system/2026-08-28) —
`triangulate-r1-deepseek.md`, `triangulate-r2-qwen.md`, and `TRIANGULATE-PLAN.md`.
