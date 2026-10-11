---
name: game-economy-ground-truth-audit
description: "Use when asked to audit or sanity-check a game/fitness reward economy (XP, score, currency curves) across a whole catalogue, or after a fix makes a previously dead scoring path pay out. Also before judging an economy from its formulas instead of from what the code actually pays."
---

# Ground-truth economy audit

Auditing a reward economy by reading formulas produces plausible-sounding
findings that are wrong about magnitude. Auditing it by reading the **numbers
the code actually pays** produces findings with arithmetic attached, and it
finds the outliers you would never have thought to look for.

Always generate ground truth FIRST, then fan out.

## 1. Dump what the code really pays

Write a throwaway test in the project's own test source set that walks the real
catalogue through the real scoring functions and writes a TSV. Not a
reimplementation of the formula — call the shipping code.

One row per catalogue entry, with the columns an audit needs to compare:

```
name  group  category  metric  weighted  tier  intensity  sample  score  scorePerUnit  secondaryScore
```

Rules that make the dump usable:

- **Pick one realistic `sample` per metric** and state it in the row
  (`10 reps`, `60 s`, `30 min`, `5 km / 30 min`, `10 attempts`). Comparisons are
  meaningless without a stated effort.
- **Emit a `scorePerUnit` column.** Totals hide inversions; per-unit rates expose
  them instantly.
- **Append REFERENCE rows**: what an ordinary session pays, what the biggest
  single award is (e.g. a skill claim), what one level costs. Every later
  judgement is a ratio against these, and without them a number is just a number.
- **Mark columns that do not apply** to some rows. A field defaulting to `2` for
  entries that never route through it will be reported as a finding by every
  agent you dispatch unless you pre-empt it.

Then delete the test and the TSV at cleanup — it is scaffold, not coverage.

Traps: the `--tests` filter may silently match nothing even when the class
compiles; just run the whole suite. Check the file actually landed
(`glob **/dump.tsv`) — the working directory of a unit test is often the module
dir, not the repo root.

## 2. Model the extremes yourself before dispatching

Run the curve over *realistic volumes*, not the sampled one. The sample is for
comparison; the extremes are where the economy breaks.

A flat per-unit rate is the classic defect: it is calibrated to one modality and
silently applied to every other. Sweep the plausible range of each modality and
convert the worst case into the currency the player feels — levels, not points:

```python
def level(xp, cost=lambda l: 100*l):
    lv = 1
    while xp >= cost(lv): xp -= cost(lv); lv += 1
    return lv
```

"One entry mints 9 levels" is a finding. "4000 XP" is a number.

## 3. Look down the stack before proposing a new table

Before anyone proposes a per-entry intensity or difficulty table, grep for one
that already exists. Calorie/energy (MET) estimation, difficulty tiers or a skill
tree, a progression graph, a rarity enum and analytics layers frequently already
hold a calibrated value for exactly these entries, built for another purpose and
never consulted by scoring. Reusing it is one rule instead of a second
hand-maintained table that will drift.

Two parallel models of the same quantity in one package is itself the finding.

## 4. Fan out against the numbers

Dispatch read-only scouts with the TSV path in shared context and an explicit
instruction: *use these numbers, do not recompute from the formulas, do not
speculate*. Useful axes, one per agent:

- the newly-paid or least-reviewed curve family
- the **competitive** score (a leaderboard) as distinct from the personal one
- descriptive correctness per entry (group, category, metric, flags)
- the progression/claim economy against session rewards
- achievement/title reachability against the real catalogue size

Require every finding to be tagged `DEFECT` (contradicts the code's own stated
rule) or `BALANCE` (a judgement the owner owns), and to cite `path:line` or a
TSV row. List known-and-deliberate decisions in the brief so they come back
under `## NOT FINDINGS` instead of as findings.

## 5. What this reliably catches

- **Modality-blind flat rates** — one unit priced identically across activities
  whose real cost differs 10x.
- **A bonus window calibrated to one member** of the family, unreachable by the
  others and automatic for one of them.
- **A missing taper on a competitive SUM.** If the personal currency damps
  volume and the ranked one does not, the cheapest movement in the catalogue is
  the dominant strategy and it compounds without bound. Work the exploit with
  units-per-minute as the cost proxy.
- **Achievement thresholds above the catalogue ceiling** — unearnable content
  padding a denominator forever. Compare every threshold to the real count.
- **Invariants enforced only in the UI.** Grep the gate function's callers: if
  the only ones are screens, the data layer will mint the reward out of order.
- **Wholesale category mapping** where a progression axis is mistaken for a
  taxonomy axis, so mixed members land in the wrong bucket.

## 6. Do not rewrite the economy unasked

An audit's deliverable is the audit. Separate the clean defects (no numbers
anybody earned against change) from the balance calls, and present the balance
calls as costed options with the arithmetic. Check whether a recompute path
already exists before repeating a "changing this would restate history"
argument — if the code can already rescore from stored inputs, that objection
may be obsolete, and the comment asserting it is part of what you are auditing.

Acting on the findings once the owner chooses is `score-economy-rework-safety`.
