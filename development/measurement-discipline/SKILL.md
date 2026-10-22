---
name: measurement-discipline
description: "Measurement discipline for claims that rest on data. Use when deciding on an experiment result, setting a threshold (閾値) or guard, choosing an observation period (観察期間) or when to open a gate, comparing a candidate with production (本番比較), or when an automated gate rejects outputs you trust."
user-invocable: true
origin: shimo4228
replaces: five contemplative-agent feedback memories (one-run-not-evidence / gate-on-evidence-not-calendar / saturated-guard-is-worse-than-none / no-numeric-caps / relevance-distribution, promoted 2026-08-25) + three speed-design memories (converting n into days / enforce-first / label-once, promoted 2026-09-26 from contemplative-agent RFC-0047) + one production-comparison memory (the lab arm mirrors production's mechanism, promoted 2026-09-26 from the confound in contemplative-agent RFC-0046)
---

# Measurement Discipline

Before accepting a measured claim, first ask under what conditions that measurement holds. Nine
principles, each drawn from a failure in practice (the sources are measurements in the author's
Contemplative Agent project, `shimo4228/contemplative-agent`; the principles themselves break the same way in any repo).

## 1. One success is not evidence

Do not say "it worked" after one smoke run and commit. In a stochastic system (LLMs, external I/O,
timing-dependent code), one run is one sample from a distribution. **Before making the claim, decide
how many runs, under which conditions, would let you say it** — if you cannot decide, weaken the
claim to "it can work".
(Source: the 2026-06 correction, after a single observed run of a follow fix was nearly reported as "fixed")

## 2. Gate on observations, not the calendar

Do not make the "move to the next stage" condition of a staged or partial rollout a date or a
duration. **Estimate the required number of observations in advance, and move on when those
observations have accumulated.** A calendar gate fires even with zero observations; an observation
gate stops when there is no data — and stopping is correct.
(Source: the enforcement decision for a shadow instrument was cut by the number of verdicts, not by "in two weeks")

How to set the observation count and open the gate:

- **Derive n from the pre-registered question** (for the precision of a rate, the binomial 95% CI
  half-width ≈ 1/√n; ±6 pt needs 300). "Once enough has accumulated" is not an n
- **Convert n into days using the arrival rate and write it in the ledger** (`resume condition: 300
  answered rows (60–105 rows/day, 3–5 days after the switch)`). Measure the arrival rate at every
  reading and update it as a range — an observation-count condition with no expected date has
  nothing to check against
- **Open the gate on the day n is reached. A weekly ritual is not a clock** — a gate that opens only
  at a ritual makes you wait many times longer than n requires (Source: contemplative-agent relevance
  shadow; at 60–105 rows a day, a question needing n = 300 had a clock of "4 Saturdays or 1,000
  rows". Read 2026-09-26)
- **If n is not reached within a short cap (default 14 days), decide instead of extending** — retire,
  or shrink the question to lower n. The longer you wait, the longer it sleeps in the ledger

## 3. A guard firing 0% or 100% of the time is a design error

When you place a suspicion field, a warning, or a check, **measure its firing rate on real data**. A
guard that never fires leads readers to read "checked, no problem" (worse than none), and a guard
that always fires gets skipped. If you have no data to calibrate it, output the raw reading instead
of a guard.
(Source: contemplative-agent ADR-0082, where readers aggregated an `observed` field that was permanently 0 and drew the opposite conclusion)

## 4. Do not use a numeric cap as a quality filter

A `max_N`-style cap controls quantity; it does not judge quality. Cutting at "top N" silently discards
good items ranked N+1 and below and silently passes bad items within the top N. To cut on quality,
build a judge on a quality axis; use a cap only when you want to cut quantity — the moment you mix
the two, both guarantees vanish.

## 5. Do not describe a distribution from the scores of what passed

Data left downstream of a filter is already selection-biased. "The mean of what passed is high" does
not prove the filter works (you have not looked at the rejects). Discuss distributions, calibration
and thresholds only on **the full pre-filter population**, or at least with a sample of the rejected
side attached.

## 6. Switch reversible changes first, then observe

A change that only alters which already-permitted action is taken, whose **error direction is on the
shrinking side** (fewer outward effects; misses can be picked up later), and whose subsequent verdicts
can be reverted by removing a setting, goes enforce-first — switch over, run the old path alongside
for n rows, record both on the same row (paired), and decide keep / kill on the day n is reached. The
kill switch is the absence of the setting. Pay for an observation-only waiting stage only for changes
whose error direction is on the expanding side, that change the form of what goes out, that widen the
I/O surface, or that cannot be reverted. Paired runs can compare only verdicts on the same input —
side effects that have already happened change the later input set, so "the history of running on
the old path alone" is never available. Compare the error direction, not a blanket declaration of
reversibility.
(Source: contemplative-agent relevance gate; would-be gate rate 0.22–0.39 vs live 0.58 = shrinking side, so enforce-first. Read 2026-09-26)

## 7. Buy expensive judgments once; make repeated measurement deterministic and $0

Freeze ceiling-model or human labels once (in the main tree, not a worktree — deleting a worktree has
lost the row data in practice), and run later measurement with cheap scorers (temperature 0,
logprobs, golden comparison). A metric that does not run on every PR cannot act as a ratchet.
**Measure reproducibility instead of assuming it** — run the same set twice, take the run-to-run
difference as the noise floor, and place the ratchet line and the neighborhood of any threshold
outside it (even temperature-0 logprobs gave run-to-run argmax agreement 0.913, max |Δp| 0.26 —
contemplative-agent S31, gemma4:e4b, 2026-09-26). **Freeze labels with the judgment's inputs (prompt,
model, the value layer it references) pinned in a manifest, and expire them when an input changes**
(relabel or ack) — so that a legitimate change in inputs is not read as a regression.
(Source: contemplative-agent's `evals/` pinned assets + `check_staleness.py`; the row-data loss in contemplative-agent RFC-0045, 2026-09-25)

## 8. A lab arm compared against production mirrors production's mechanism

Design a measurement that claims a candidate is "better than production" only after **listing the
differences between candidate and production in a table** (the text shown in the input, the form of
the question, how the answer is read, temperature, the definitions the judge uses). Measure one
difference. If there are two or more, keep arms that change one condition at a time (a ladder) on the
same sample, and read which condition carries the difference from the paired differences. Align the
judge's (ceiling model, external judge) question and definitions with production's as well — if you
do not, that is not a measurement but a choice of definition, and you pre-register it as the author's
decision in the packet and the RFC (not in a script docstring — a buried definition becomes the
judge's ground truth, and fixes get built on top of it).
(Source: contemplative-agent RFC-0045 → RFC-0046. A candidate with identity only / a 4-level scale /
logprobs was compared against production with identity + axioms / a 0–1 scale / generated numbers, and
the judge also scored with identity only — enforce was designed on evidence where three conditions
and the definition were confounded, and the owner's review sent it back to a ladder. 2026-09-26)

## 9. Before fitting outputs to a gate, test the gate against trusted labels

When an automatic judging gate (an LLM or judge model + a threshold) rejects outputs that a trusted
judgment (the author, a bench judge) passes, **measure the gate's own discriminative power** before
reshaping the outputs to pass it. Collect judged outputs so that both passes and fails are included
(from several versions), replay the gate with the same input assembly as production, and save the
raw scores. Look at the acceptance rate on the pass side and on the fail side, the precision of the
accepted set compared with the overall pass rate, and the AUROC of the scores. A gate whose
accepted-set precision does not exceed the overall pass rate is noise, and fixes fitted to it optimize
for noise. Compare proposed thresholds, question wordings and scopes offline on the saved scores
before taking them live. If no proposal can be distinguished from chance, take the check out of
gating, record its score as a label, and give the property to a trusted mechanism (the prompt, a
self-check, a separate judgment). If the gate was placed for a specific failure, also confirm that it
actually catches inputs synthesized with that failure.
(Source: claim_fidelity in the author's jev-research-pipeline project. It accepted 24 of 120 passes
and 10 of 31 fails; precision 0.71 fell below the overall 0.79, AUROC 0.42–0.68. Synthesized subject
swaps scored 0.46–0.54 under a threshold of 0.6 and passed straight through. 2026-10-01 to 02: the
gate was removed and kept only as a record, and the template dropouts in production sections were
resolved)

## How to use

In design or review, name one applicable principle and ask with it ("This is principle 3 — on what
data did you calibrate this guard's firing rate?"). Do not walk through every principle each time.

## Expiry conditions

- Retire when the substrate starts raising these questions on its own at design time (Scaffold Dissolution)
- If a measurement a principle came from is refuted, delete that principle (the principles are rules of thumb, not axioms)
