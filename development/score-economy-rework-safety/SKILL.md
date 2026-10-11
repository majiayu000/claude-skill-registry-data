---
name: score-economy-rework-safety
description: "Use when rewards feel wrong relative to each other, before shipping an XP or score formula change users earned against, when acting on an economy audit, or when stored scores need restating. Also when a game/fitness rebalance may silently inflate currency, levels or a leaderboard, or before mutation-testing uncommitted economy work."
---

# Score-economy rework, safely

Any change to a reward formula users have already earned against (XP, strength
score, currency): an owner's "X gives less than Y" complaint, or findings from
`game-economy-ground-truth-audit`. Kotlin/Room examples come from `D:/Monarch`.

## Ordering and magnitude are separate problems

"X gives less than Y" is an **ordering** defect. The trap is fixing it with scale
constants tuned on invented examples: you ship correct ordering plus a 2-3x
inflation nobody asked for, and the level curve, titles and any leaderboard move
with it.

- **Ordering** comes from the structural terms (per-item difficulty weight,
  unit conversion, volume taper). Prove these with mutation tests.
- **Magnitude** comes from the scale constants (per-unit rate, flat per-item
  base). Calibrate these against real data and an in-app reference reward.

## 1. Fixtures: the ground-truth dump and the owner's data

Start from the ground-truth dump (`game-economy-ground-truth-audit`): what the
shipping code pays per catalogue entry, plus reference rows. Check every
before/after table and scout claim ("tier V pays tier III rates") against it;
delete the throwaway test and TSV before finishing.

Invented scenarios will not tell you whether a change inflates. The owner's
reported session is the only honest fixture, and in practice it reproduces the
complaint exactly. On Android with a debuggable build, back up **before**
installing anything (`exec-out`, never `adb shell`: the CRLF corruption and the
size check are in `android-package-rename-data-carryover`):

```bash
adb exec-out run-as <pkg> cat databases/<db> > backup/<db>
# repeat for -wal and -shm: sqlite replays the WAL when all three sit together
```

Rebuild the actual rows as a test fixture. Re-pull at the end and diff row
counts plus the headline totals: that diff is your evidence the verification did
not cost the owner data. Expect benign drift from background sync (a health-data
row appearing) — identify it, do not wave it away.

## 2. Anchor the ordinary case, bound the top

Pick a representative *ordinary* unit of activity — the median case, not the one
being complained about — and tune the scale constants so its reward is
unchanged. That makes the change a redistribution rather than inflation, and it
is a sentence you can defend:

> "4x8 pull-ups + 3x10 dips + 3x12 leg raises scored 273 before and 278 now."

Then find a reward the codebase already prices deliberately and check you have
not overtaken it. Comments like *"Skills are milestones, not sets: reward scales
hard with tier"* are a stated product rule; a repeatable action out-earning a
once-per-lifetime milestone violates it.

Sweep candidates in one throwaway test rather than guessing:

```kotlin
for ((base, per) in listOf(8 to 1.5, 6 to 1.0, 5 to 0.8, 4 to 0.7)) {
    println("%4d %4.2f | %8d %8d %8d %9d".format(
        base, per, total(realHard, base, per), total(beginner, base, per),
        total(exploitFarm, base, per), total(anchor, base, per)))
}
```

Print the reference rewards under the table so the choice is legible. Include
an **exploit row** (the thing being farmed at maximum volume) and confirm it
collapses.

Read the printed output from the JUnit XML — `system-out` is captured there
without touching Gradle logging config:

```python
re.search(r'<system-out><!\[CDATA\[(.*?)\]\]></system-out>', s, re.S).group(1)
```
Non-ASCII output is XML-escaped inside CDATA (emoji arrive as
`]]>&#x1f7e9;<![CDATA[`); substitute it back before judging the layout.

## 3. Reuse the difficulty table the project already has

Before inventing a difficulty or intensity table, find the one the project
already keeps for another purpose (`game-economy-ground-truth-audit` lists where
they hide). Never add a second: a rival table drifts. If a rival already exists,
delete it and check the deleted helper for remaining callers.

Two traps when reusing it:

- **Names that price a modifier into the tier.** "Weighted Pull-up" sits at
  the top tier *because of the +25 kg in its standard*. If the formula also
  multiplies by logged kilos, that plate is paid for twice. Override those
  names to their unloaded parent and let the real load do the work.
- **Modifier strings that duplicate a numeric field.** A `weighted` tag next
  to a `weightKg` column is the same double count. Give such tags a factor of
  1.0 and say why in a comment.

Anything unlisted must fall back to a default, or a user-created item mints
reward by naming.

## 4. Wrong-unit values

A value typed into the wrong field (seconds in a reps field) is one bug per
consumer: reward, strength scores, lifetime totals, any "N reps" summary.
Enumerate and fix consumers with `unit-overloaded-column-migration`. While
calibrating, also:

- Record every consumer you do not fix as a costed decision.
- Detect the unit from the project's own source of truth (a claim standard, a
  declared metric), not a new hand-kept list. When you infer from text, check
  the inference against **every** row and print the diff — a regex like
  `\d+\s*s\b` matching anywhere reads "5 negatives, each 5s" as a hold. Anchor
  it to the first figure instead.

## 5. Phase it, and commit before you mutate

1. Fix clean defects (no economy impact) first.
2. Economy changes need the owner's yes: show the before/after payout table on
   their own data and name the existing primitive you will reuse.
3. A change to any stored score needs a history decision (section 7).

Each phase is one commit, made **before** mutation-proving it. Mutations edit
real source and revert it; a `git checkout -- <file>` revert destroys every
uncommitted phase that touched that file (three agents' work was lost this way,
at high rebuild cost), and `git checkout` from the index or HEAD is lossy for
staged-vs-worktree changes. So revert with `git checkout -- <file>` against a
COMMITTED state — never a `.bak` copy, which a cleanup `rm` can delete mid-run.
When one file carries several phases (e.g. `Repository`), split the diff by hunk
(`git apply --cached` with per-phase hunk subsets) so commits stay thematic.

## 6. Prove ordering by mutation, not by assertion

Each structural term gets a mutation that removes it; the ordering test must
fail:

| mutation | expected failures |
|---|---|
| difficulty weight -> 1.0 | ordering + headline comparison |
| unit conversion removed | unit tests |
| volume taper -> identity | headline comparison |

Write the headline test as the owner's exact comparison, with both totals in the
failure message. Stale-XML and line-anchored mutation mechanics:
`gradle-mutation-proof-regression-test`.

## 7. History: banked rewards stay, comparative scores restate once

Whether stored figures move is the owner's call: leaving them makes new records
incomparable with old ones, and recomputing them restates history. First check
whether a recompute-from-stored-inputs path already exists.

- **Banked progression (XP, levels) is never recomputed.** Past awards were
  earned under the old rule; rewriting them can demote a level and destroy
  trust in the number. Say so in the code comment and in the report.
- **A stored comparative score (a strength index, a leaderboard's lifetime sum)
  is restated exactly once per formula change** — old and new formulas mixed in
  one ranking make it meaningless. Use a version marker: bump the Room version,
  the migration adds the column at 0, and code compares it to a
  `SCORING_VERSION` constant and rescores once. SQL cannot express scoring, so
  the marker is consumed in Kotlin.

Verified 2026-09-24 in `D:/Monarch`: `Repository.ensureSeeded` restates strength
scores once under `StrengthIndex.SCORING_VERSION`; `rescoreStrengthScores` never
touches banked XP.

## 8. Restatement tests (instrumented)

- Prove the rescore-all runs: plant sentinel scores, reset the marker, run the
  seed/launch path, assert scores match a freshly computed `sessionScore` and
  lifetime equals the fresh sum.
- Prove it runs ONCE: with the marker stamped, planted wrong scores must survive.
- Re-read the profile row before stamping the version — stamping a pre-rescore
  copy silently writes the stale lifetime total back over the fresh sum (a real
  bug this caught).
- Beware the vacuous guard: a test whose database holds nothing to repair
  short-circuits before the code under test runs. Add a control row that forces
  the path.

## 9. Honesty invariants worth pinning

- An unearned progress line must never report `current == target` (rounding can
  claim a title complete).
- Distance/duration work: missing time pays 0; never fabricate a pace.
- One pace/intensity model (section 3).

## Reporting

Lead with the before/after table on the owner's **own** data, then the anchor
sentence, then the bounded-top sentence, then the history decision (what was
restated, what was left). If you re-tuned mid-flight, say so and say why —
discovering your first pass inflated 2.4x and correcting it is the strongest
evidence the calibration is real.
