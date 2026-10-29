---
name: guide-to-prompt
description: Decide what to ask, then write it. Pick one client domain and task type, one of the eight Axis 1 objectives, a forward-facing committed call and the prompt shape that supplies the rubric's 25 or more criteria; then write prompt.txt, one plain-text paragraph under 1,000 characters, question first, one to three files named, rounding once at the end, gated by voice-check.py. The best prompts on file are in references/examples.md. Use at the start of every build, before stumping designs the ladder, and whenever a prompt is written or edited.
---

# Choosing what to ask, and writing it

The prompt is a person asking for help with a job they understand: the question first, the files wanted back, each
unit beside its figure, rounding once at the end, in one paragraph under 1,000 characters. It says nothing a solver
could use that the files do not also carry, and nothing about who is asking. Read `references/examples.md` (the best
prompts on file, with where each stump hides) before drafting, and `references/exemplars.md` (the client's 49 measured
tasks) for the depth the client pays for.

## 1. The pairing

**One domain, one task type.** From the client taxonomy (`references/domains/README.md`): the domain whose
decision-maker owns the call, one task type in it (the card's `subdomain`); the task type is where the Layer 2 pitfall
comes from, and it must serve the objective in the taxonomy (the guard and `precut.py` refuse one that does not).
**Swap test:** put another field's nouns in the call sentence; if it reads the same, the domain is a backdrop. Write
the field's own deciding analysis, and why the swap breaks it, into the card's `domain_test` and the design note's
`## Three rules` (`stumping` 1.1).

**One objective of eight**, or the task is rejected on the tag ("Comparative analysis" is not one).

**Data Extraction & Conformation is the most closed objective in the corpus, and the pincer is measured.**
Only six task types in the taxonomy carry ETL, and 66 cards sit across five live cells (8, 7, 11, 7 and 6),
the sixth having been enumerated closed. Read across all 68 drivers with lineage and every ETL driver on file
is one of five moves: complete a record the process could not make; re-grain or re-key onto the decision's
unit; re-time onto the decision's calendar; recover a per-case input a second file pins; split a total between
two causes. The pincer is why cells close as enumerations rather than thinning out: a conformation call's
decisive step reduces to a correction, and a correction's input is either PRESENT in the records (rule
application, measured at 0.000000 bins and the same graded bin 24 of 24), ABSENT (Gate B, the golden 285.24
bins from anything computable), or SAMPLED (a model of the measurement, measured at 10.9 to 15.3 times the
step's worth across a sevenfold dial with 0 of 7 settings passing). The middle case these skills bless, an
arithmetic-closed per-case input that is neither a filed column nor an exact count of shipped rows, needs the
forcing file to pin a structure, an order, an opportunity count, an overlap or a condition, and in an
administrative-record world those are identity resolution, grain and time semantics, which rule 3 bars from
deciding a call. So an ETL draw names which of those five its forcing file pins and says why reading it
correctly is not sufficient, before any world is drawn.

**A seed's own header tag is not evidence that its pairing is legal.** A seed can name a domain and an objective that no task type in that domain serves, and the pairing is then undrawable however good the world is: seed AD28 pairs Economics with Anomaly Detection, and the eight task types of `economics-econometrics` serve EC, OS, F, RC and DD and none of them AD. Read the domain's own task-type codes in `references/domains/README.md` before anything else in the draw, because the guard and `precut.py` refuse the pairing at the card and a draw that reaches a measured ladder first has spent a session on a build that could never register. Where the seed's objective is the lane's, the domain moves and the world is redrawn; where the world is the point, the objective its task type does serve is the honest tag, and that moves the number to another lane.

| Objective | The decision turns on | Native shapes |
|---|---|---|
| **Forecasting & Predictive Modeling** (most wanted, the tiebreak) | a future value the supplied history pins down | 02, 13; 04, 06 over an open window |
| Root-Cause Analysis | the driver of a move, rivals ruled out on evidence | 12, 18; 09 for a fall |
| Anomaly Detection & Diagnostics | a real event separated from an artifact | 17; 08 for breaches |
| Experiment & Causal Analysis | a causal claim, designed or observational with confounders | 11, 07 |
| Descriptive & Distribution Analysis | how a population is composed or a metric distributed, not why it moved | 14, and nine more default here |
| Data Extraction & Conformation (ETL) | messy multi-source inputs reconciled into one contract-conforming dataset | 03, 15 |
| Opportunity Sizing & Decision Support | a sized opportunity built from the addressable pool to what can be realised, driving the call | none; fails if retaggable Forecasting or Descriptive unchanged |
| Data Quality Monitoring & Alerting | the health of the data or its pipeline, with a monitoring or alerting call | none; fails if retaggable Anomaly Detection or Forecasting unchanged |

The committed call faces forward by default (a figure booked, ordered or staffed for a window not yet closed); a
retrospective call needs its reason in the design note. Facing forward does not change the tag: retag as Forecasting
only when the answer is a predicted value the history pins. Write the pairing into the design note's `## Draw`, then
`guard.py recent` and `coverage` before choosing and `guard.py check` on the card (`fingerprint`).

## 2. The shape, before the ladder

The 25 criteria come from the structure of the answer, never from stacked asks: one repeated unit times its count
(10 to 20), doubled by a second figure per unit, plus the call, runner-up, gap and flip (3 to 4), a chart with named
parts (5 to 7) and the files (1 to 3). Under 25 means a denser structure. Pick from `references/shapes/README.md`,
which carries each shape's arithmetic and the seam where it turns hard rather than long; write the sum into the
design note.

| # | Shape: criteria from | # | Shape: criteria from |
|---|---|---|---|
| 01 | Ranked list under a cap: each candidate | 10 | Scorecard: each metric-threshold check (1 file) |
| 02 | Forecast across periods: each period | 11 | Before and after with a control: each unit's effects |
| 03 | Bridge between totals: each reconciling item | 12 | Drill-down to one leaf: each level's piece |
| 04 | Setting one dial: each allowed setting | 13 | Scenarios and the flip point: each cell, the flip |
| 05 | Allocation to a fixed total: each bucket | 14 | Cuts of a distribution: each cut per segment |
| 06 | Schedule under capacity: each finish period | 15 | Fields to one schema: each field's source and transform |
| 07 | Grid of cells: each cell | 16 | Indicators into one score: each indicator |
| 08 | Rule replayed on history: each period's cells | 17 | Periods around a change point: each period (1 file) |
| 09 | Funnel of stages: each stage's volume, rate, cost | 18 | Hypotheses versus evidence: each cell |

## 3. Writing prompt.txt

Write it last, against the golden. Context, question, files, rounding, in one paragraph. **The ten rules:**

1. **Lead with the question**, a direct question in the first two sentences.
2. **Cut who and why:** no names, titles, sign-offs, meetings or readers of the file.
3. **Test every fact before cutting it:** a send date, extract date, cut-over or stop rule that bounds the answer stays.
4. **Keep every ask exactly:** file names, columns, periods, units and rounding word for word.
5. **Do not change meaning while smoothing:** "in cents" is not "dollars and cents"; "whether any, and if so how many" is not "how many".
6. **One continuous paragraph**, list items joined by commas and semicolons, no "Then" or "Last".
7. **Merge and shorten;** each rounding rule once, at the end, naming the figures it governs.
8. **Ask, do not specify:** "what is", "put it in", "also give me", never "X is the file, one row per".
9. **Drop claims made only to be rejected.** An opinion arguing the wrong answer is cut.
10. **Run the 10/10 check last:** does the answer turn on real analysis, or only on a stated procedure or a field
    read correctly? If the latter, the build is not ready, whatever the prompt says.

**May say:** the question, with the candidate set and the hold on the same footing ("or none this cycle") where
relevant; the forcing fact once (window, date, cut-over, stop rule); each file by name and extension with its content
as a person states it ("one stacked bar per district, each high segment labelled with its count"); the standard the
call runs on only where the pack lacks it; a generic threat to validity ("participation was voluntary").

**Never says:** anything that fixes the basis, window, convention or population; the deciding metric, eligibility rule
or fee schedule; an input file name; a standard by acronym; a method hint ("compare A against B"); a trap word (clean,
unduplicated, reconcile, attribution, mix, standardise, grain); two metrics named as valid; a warning that a view
might mislead; a **presupposition**, an ask that only parses if a subset is non-empty or a move happened ("how many
and what they cost", "the sites where it fell"), which the client's prompt review fails as a leak: make "none" a
grammatical answer ("whether any and, if so, how many and what they cost") with every figure, unit and rounding kept,
while a fact the requester knows before any analysis stays (`reduce-house-fixes` H23).

**Budget.** 1,000 characters is about 150 to 170 words; the client's paid-out prompts ran a median 227 words at 21.6
a sentence and a maximum of 334, each still carrying the full unit. Compress per sentence, never by deleting a
requirement: one sentence with a list in it per file; cut every reason but one motive; rounding once; no role,
meeting or pack inventory; ask rather than specify. Never cut the repeated unit, the call, runner-up, gap or flip, a
chart's named parts, a unit, a derived figure's rounding, or the forcing fact. After each pass walk the figure list,
recount the criteria and rerun the gate.

**Variety.** Take the question's form from the decision (a count asks how many, a pick which, a gate whether, an amount
how much, a date when); the batch report flags a form above a third of the window, and a window shipping one format
or pairing reads as a template.

**The call and the asks.** The call is one quotable sentence with its unit. Every ask is a component, qualifier
(sensitivity, flip, reconciliation) or audit trail of it; an ask a person could act on with the call unmade is a
second decision and a first-pass rejection (`reduce-house-fixes` H18). Each ask passes six tests: a named use,
provenance independent of the criteria count, the right genre for its file, the stakeholder's vocabulary, asymmetry
across the set, nothing the organisation already knows. An entity plus an aggregate names its grain. A failing ask is
re-cut or folded, never deleted. The asks are designed in `supplemental-stumping`.

## 4. The gate

```
python3 .claude/skills/guide-to-prompt/references/voice-check.py taskNN            # exit 1 on any FAIL
python3 .claude/skills/guide-to-prompt/references/voice-check.py --file <draft> --task taskNN
python3 .claude/skills/guide-to-prompt/references/voice-check.py                   # batch report
```

It fails on: not `prompt.txt`; any backtick, hash, pipe, bracket, bullet, label-colon line, or emphasis outside a file
name; a line break; no question mark in the first two sentences; 1,000 characters or more; an em or en dash; a persona
from the card's `world.people`, a title, sign-off, board vote or reader; a sentence opening Then, Next, First, Second,
Last, Finally, After that; an LLM tell (leverage, robust, comprehensive, seamless, delve, ensure, note that, in order
to, furthermore, stakeholders); two attributed opinions; rounding outside the last sentence; zero or more than three
files. `leak.py` sweep 11 and `precut.py` run the same gate. A failing draft is not done.

## Checklist

- [ ] Domain, task type, objective and `domain_test` fixed; shape arithmetic at 25 or more before any file exists
- [ ] The call is one quotable sentence; every ask passes H18 and the six tests; `voice-check.py taskNN` exits 0
- [ ] No ask presupposes what the data holds: every ask about a subset still reads with "none" as its answer
