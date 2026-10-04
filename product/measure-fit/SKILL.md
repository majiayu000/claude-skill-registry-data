---
name: measure-fit
description: This skill should be used when the user wants to set up measurement or judge whether they've built something people want — "how do I measure product/market fit?", "set up my metrics / conversion funnel / cohorts", "am I at product/market fit?", "run the Sean Ellis test", "what should my key metric be?", "track retention/activation", "which engine of growth?", or validating the customer lifecycle (acquisition → activation → retention → revenue → referral). It defines the value metrics, reads funnels and cohorts honestly, and applies the fit benchmarks. Writes to .lean/metrics/. Use for the "verify quantitatively" stage. For designing a single experiment, use run-experiment.
version: 0.1.0
---

# Measure product/market fit

Define a metric for "have I built something people want?", then steer toward it. You work as the **Analyst** guide role (`../../reference/roles.md`) — evidence-minded and honest, especially about the difference between progress and vanity. Read `references/product-market-fit.md` before judging fit.

## When to use

The user needs to set up measurement, interpret their funnel/cohorts, or get an honest read on product/market fit. This is the *verify quantitatively* stage and the validate-the-lifecycle work that precedes it. For a single assumption test, use `run-experiment`; for the qualitative MVP interviews, `customer-interview` (mvp).

## Core stance

- **Retention is the macro that matters.** Revenue is the *first* form of validation; retention is the *ultimate* one. People can pay for something they don't use (forgot to cancel, someone else pays); they don't *keep using* something they don't want. Judge "people want it" primarily on retention.
- **Cohorts over funnel snapshots.** A single funnel hides what changed; weekly cohorts (group users by join week) show whether last week's change actually moved the needle and handle traffic fluctuations correctly.
- **Validate the lifecycle micro before scaling macro.** Get ~80% of hand-qualified early adopters through the full cycle (acquisition → activation → retention → revenue → referral) before chasing volume. Scaling before early traction is waste.
- **Vanity vs. value metrics.** Total signups and page views go up while the business goes nowhere. Track activation and retention.

## Procedure

1. **Load context.** Read `.lean/PROGRESS.md` (stage), `.lean/canvas.md` (Key Metrics block), and any prior `.lean/metrics/` files.
2. **Define the value metrics & key metric.** Map the customer lifecycle to AARRR (Acquisition, Activation, Retention, Revenue, Referral; see `references/product-market-fit.md`). Pick the single key metric for the current question — usually **retention** as the macro, with activation as the supporting micro.
3. **Set up measurement.** Specify the conversion funnel and **weekly cohort report** (functionally — what events, grouped how — independent of the analytics tool). For early stage, this can be a manual sheet.
4. **Validate the lifecycle (micro).** Walk the funnel for hand-qualified early adopters; find the leakiest bucket, fix it, reach out to users who dropped. Target ~80% through the full cycle.
5. **Judge fit honestly.** Apply the benchmarks: the **Sean Ellis test** ("how would you feel if you could no longer use this?" — ≥**40% "very disappointed"** signals early traction) and the **40% retention month-over-month** proxy. State whether the evidence supports fit, with the numbers — don't flatter.
6. **Pick the engine of growth (when approaching fit).** Sticky (retention) / viral (referral) / paid (margins; LTV > 3×CAC). Focus on one; declare the key metric and target, and align the next experiments to it (route to `run-experiment`).
7. **Write** `.lean/metrics/<YYYY-MM-DD>-<label>.md`: the funnel/cohort read, the fit verdict against benchmarks, and the recommended next move. Update `.lean/PROGRESS.md`; if fit signal is real, advance the Stage to Scale.

## Output

`.lean/metrics/...` — defined value metrics, a funnel/cohort read, an honest fit verdict (Sean Ellis %, retention %), and a recommended engine of growth + next experiment. Update Stage in PROGRESS.md when warranted.

## Related

- `run-experiment` — the experiments that move the chosen metric.
- `customer-interview` (mvp) — the qualitative half of validation.
- `investor-pitch` — consumes these numbers; raising is best *after* fit.
- `references/product-market-fit.md` — AARRR, Sean Ellis test, retention macro, engines of growth.
