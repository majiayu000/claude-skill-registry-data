---
name: black-box-model-extraction
description: Use when recovering the exact rules of a financial model, calculator or pricing engine you can only submit inputs to — no source access. Triggers on "reverse engineer this calculator", "clone this model", "match their numbers", "figure out what formula they use", or when our output disagrees with a reference tool and you must find out why.
---

# Black-Box Model Extraction

Recover a numeric model's exact rules by submitting inputs and reading outputs.
Done well, the result is not "close enough" — it is shekel-exact, with every
rule traceable to a recorded observation.

**Core principle: one free parameter at a time.** Isolate everything you cannot
yet derive into a single scalar, then prove the rest of the model by showing
that one scalar reproduces the whole output. Then go measure that scalar
directly.

## The loop

1. **Find the richest output channel.** Prose summaries round; charts often
   don't. Rendered pages frequently embed full series in a `<script>` block —
   hundreds of exact monthly data points instead of one rounded headline. Look
   before you settle for the headline number.
2. **Record every probe as a fixture.** Input payload + full output, on disk,
   forever. These become the regression suite. Never re-probe for something you
   already recorded.
3. **Change one variable.** Design the scenario so everything else is inert
   (zero the returns, equalise income and expenses, park a huge cash balance) so
   a difference can only mean one thing.
4. **Predict, then check.** Hypothesise a formula, compute the number it
   implies, compare to the observed value. "Consistent with" is not "verified".
5. **Write it down with the numbers that prove it.** A claim without its
   evidence rots the moment someone doubts it.

## Design the experiment so only one thing can move

The single highest-leverage habit. Examples that cracked real rules:

| Question | Scenario that answered it unambiguously |
|---|---|
| Does the return change after some event? | Fix the event date, run the *same* scenario at 5% and at 20%. Identical output ⇒ the rate is not derived from the input return. |
| Is this flag doing anything? | Two runs differing in that flag alone. Byte-identical output ⇒ it does nothing. |
| What is the tax rule on withdrawals? | A balance with a *known* cost basis and no history to invent. |
| What is this hidden fee? | Vary the stated fee 10× and see whether the effect scales. |

If a scenario has two moving parts, you will fit a plausible wrong answer.

## Isolate the unknown into one scalar

When one quantity resists derivation, do not stall and do not guess. Make it an
explicit parameter, then **fit it per scenario** — a 1-D search that minimises
disagreement with the recorded output.

Two things fall out at once:

- **Everything else gets proven.** If one free scalar reproduces a 500-point
  series to rounding, every other rule in the model is right.
- **You harvest the unknown's shape.** The fitted values across scenarios are
  data. Plot them against candidate drivers; the pattern usually names itself.

Then design a probe that measures the scalar *directly* (make the quantity the
only thing that can move) and check the measured value against the fitted one.
Agreement between two independent routes is the strongest evidence available.

## Traps that produce confident wrong answers

**The inversion inherits the forward model's assumptions.** If you recover a
hidden parameter by inverting an observable — "this taxable fraction implies a
lot of age N" — every assumption in that inversion is load-bearing. Get the
growth rate wrong and you will produce an internally consistent, arithmetically
flawless, completely false disproof. *This happened in this codebase:* a model
was "disproved" because the inversion used the accumulation rate for a period
where the system had switched to a much lower one. Before trusting a
disproof, re-derive it under each regime the system has.

**A clean cutoff is not always the rule you think.** An effect that vanishes at
a threshold may be a *different mechanism* whose output happens to be zero
there. Test with a case big enough to survive the alternative: if you think
"tax stops at 60", find a scenario with a large enough amount that a
marginal-rate rule would still bite. If it does, it was never an exemption.

**Rounded displays hide off-by-ones.** An age printed to one decimal is
ambiguous between two adjacent months. Prefer an unambiguous field (a date) and
work out whether the reported index is the last month *before* the transition
or the first one after.

**Fitting can land in a local minimum.** A max-error objective is only
piecewise smooth. Bracket with a coarse grid before refining, and sanity-check
the fitted value against the neighbouring scenarios.

**A discontinuity must not be interpolated across.** If the surface jumps,
split it into branches and interpolate within each. Smoothing over a real jump
produces answers that are wrong on both sides.

## Verify to the unit, not to the eye

Compare full series, not spot values, and report the *worst* disagreement
across every month and every series. Two numbers that agree at month 3 and
diverge at month 300 are a failing model that looks fine in a summary.

Track the difference between:
- **verified to the unit** — predicted and observed match to display precision
- **consistent with** — the data does not contradict it

Never promote the second to the first in a writeup.

## Reproducing bugs is part of the job

The reference is the spec, including where it is wrong. Expect to find:
dead code paths that crash (so there is *no* behaviour to clone — implement
from intent and label it as inference, never as parity), stale statutory
constants, and modelling choices that are simply very conservative.

Reproduce them faithfully, log each as a deviation candidate with the evidence,
and let the owner decide. Silently "fixing" one destroys parity and hides a
decision that was not yours to make.

## Be a good citizen of someone else's server

Every probe costs them compute. Reuse one session, run sequentially, sleep
between calls, and think hard about the scenario before spending a request. A
well-designed probe is worth twenty scattergun ones. Record everything so you
never pay twice for the same answer.

## Worked example in this repo

`research/zeke_retire_calc/` is a complete instance: harness (`zeke.py`,
`probe.py`), fixtures, a fitter (`fit_decumulation.py`), a direct measurement
campaign (`probe_trinity.py`), and 14 evidence notes. The engine it produced is
`backend/services/fire/`, with parity tests in `tests/backend/unit/fire/`.

Read `notes/13-fifo-lifo.md` first: it documents a wrong disproof and its
correction, which is the most useful thing in the directory.
