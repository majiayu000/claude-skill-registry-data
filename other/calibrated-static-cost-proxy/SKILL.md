---
name: calibrated-static-cost-proxy
description: "Compute the judged cost inside the artefact generator from structure alone (charged ops weighted by the firing rate of their enclosing conditions), calibrate it against the official judge once per design, and use it for all inner-loop decisions. Use when a judge run costs minutes or more and individual levers are worth less than about 1% each, in any benchmark-optimization campaign where a generator builds the artefact (circuits, prover constraints, gas, proof size)."
---

Paths such as `scripts/...`, `references/...` and `assets/...` are relative to this skill's folder.

# Pi-mal-Duume (calibrated-static-cost-proxy)

A **static proxy** is a count the generator prints with every build: the expected judged cost, computed from the
artefact's structure with no simulation. **Calibrated** means it was compared with the judge on the same artefact
and the gap is on record. Inner-loop decisions use the proxy; the judge confirms once per submission candidate.

## Use it / leave it

- Use when a judge run costs minutes or more and levers are worth less than about 1% each.
- Do not report the proxy as the score.
- Leave it when cost depends on data in ways the generator cannot weight (input-dependent loops with no known
  distribution). Then use an exact replica (`exact-evaluator-replica`).

## Inputs

- A generator that knows the nesting of every conditional block it emits.
- One judge (or exact replica) run per calibration.

## Procedure

1. **Put a counter in the builder.** Each charged op adds its weight. Inside a block conditioned on a measurement
   outcome, or on any runtime condition, the weight is multiplied by that condition's firing rate, per nesting
   level. Use 1/2 for a balanced random outcome. Use the measured firing rate for any condition known not to be
   balanced. `scripts/proxy_counter.py` holds a 20-line `StaticCost` class (`push(rate)`, `pop()`,
   `charge(n, section)`) to copy or port.
   Done when every site that emits a charged op goes through the counter.

2. **Print it with every build, after all post-passes,** next to the emitted count and per named section. A
   post-pass that removes or adds charged ops after the counter ran makes the figure wrong; either count after the
   pass or make the pass update the counter.
   Done when the build prints one line with emitted count and expected cost, and the per-section costs sum to the
   total.

3. **Calibrate.** Run the judge on the same artefact and record proxy, judge and gap in `assets/calibration.tsv`
   with the artefact hash and evaluator commit. Worked example, five pairs from one campaign: 0.06% and 0.04%;
   about 10 units in 3 million, twice; and 1.5% on the first build with a spliced foreign module (static
   4,929,726.5 against 4,854,904.726). Recalibrate when a new kind of conditional block or any foreign module is
   introduced.
   Done when the latest row's gap is recorded and `proxy_counter.py check calibration.tsv --lever <smallest lever>`
   exits 0.

4. **Decide with the proxy, confirm with the judge.** Keep lever tables in proxy units at a reduced test scale. Run
   the judge or replica once per submission candidate and add the pair to the calibration file.
   Done when each accepted lever has a proxy delta and the candidate has a judge figure.

5. **Per-call costs for library routines.** A gate-level or unit test prints expected cost per call for each
   routine. A lever is then priced as (calls) x (per-call delta) before it is built.
   Done when the routine table exists and its sum over call counts matches the section totals.

6. **State the unit and scale of every proxy figure.** For example "per division at the walk's gate test, test cap
   593, which corresponds to 825 at full scale". Two proxy figures taken at different caps or scales are not
   comparable.
   Done when no proxy number in a note or table lacks a unit and a scale.

## Checks that say it worked

- The proxy-to-judge gap is recorded and is below the size of the smallest lever being decided.
- The sum of per-section costs equals the total.
- A lever accepted on the proxy moved the judge figure by about the predicted delta at the next confirmation.

## Failure modes

- **Unbalanced conditions.** A repair block that fires on 5% of samples, weighted at 1/2, overstates its cost
  tenfold. Measure the rate once on a sample and pass it to `push`.
- **Post-passes that run after the counter.**
- **Comparing proxy figures taken at different caps or scales.**
- **Drift after splicing foreign ops.** The 1.5% case above is larger than most single levers. Recalibrate after
  every import (see `fit-probe-and-splice`).
- **A proxy that drifts unnoticed.** Every judge run is a free calibration point; record all of them.

## Bundled files

- `scripts/proxy_counter.py`: the `StaticCost` class and `check <calibration.tsv> [--lever SIZE]`, which prints
  each gap and exits 1 when the latest gap is not below the lever size. `--selftest` compares the counter with a
  simulated judge on a random block tree and shows the unbalanced-condition error.
- `assets/calibration.tsv`: header and one example row. Columns: artefact hash, proxy, judge, relative gap, date,
  evaluator commit, note.

## Transfer

- Provers: constraint or cell counts against measured prover time or memory.
- Gas: a static gas estimate against measured receipts.
- Proof benchmarks: a term-size estimate against the checker's measured size or time.

## Evidence this pays

Citation key: `N:<id8>:<line>` is a public submission note of the source campaign (solver BitWonka, ecdsa.fail)
by id prefix. Numbers are quoted; none was recomputed for this skill.

- One row's four build steps were chosen on "expected" figures and confirmed twice by the judge: 5,010,346 expected
  against 5,007,345.518, and 4,920,208 against 4,918,479.342 (N:954016db:34-37).
- The weighting rule, 1/2 per nesting level of a measurement-conditioned block: N:954016db:39-41. The build line
  that prints it: N:954016db:126-128.
- Further pairs: N:2d167363:17, 25, 33, 35. The 1.5% drift: N:29c85603, section 4.
- Lever tables in proxy units at a test cap: N:390668eb:27-44. Per-call routine costs: N:29c85603:124.
- The calibration rests on five quoted pairs from three notes.
