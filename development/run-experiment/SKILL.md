---
name: run-experiment
description: This skill should be used when the user wants to design or log an experiment to test a business-model assumption — "design an experiment to test X", "how do I validate this assumption?", "turn this into a falsifiable hypothesis", "what's the smallest test for this?", "set up a landing-page / concierge / smoke test", or "log the results of my experiment". It frames the assumption as a falsifiable hypothesis, picks a single key metric and the smallest build, and records the Build-Measure-Learn cycle to .lean/experiments/. Use it for the "systematically test your plan" step. For interviews specifically, use customer-interview; for judging product/market fit, use measure-fit.
version: 0.1.0
---

# Run an experiment

A single trip around the Build-Measure-Learn loop. This skill turns a risky assumption into a falsifiable hypothesis, designs the smallest test that produces real learning, and logs the result. You work as the **Analyst** guide role (`../../reference/roles.md`). Read `references/build-measure-learn.md` before designing.

## When to use

The user wants to test an assumption (usually the top one from `prioritize-risks`), needs help making it testable, or wants to record what an experiment taught them. Customer interviews are a *kind* of experiment but have their own skill (`customer-interview`); use this skill for landing-page / smoke / concierge / pricing / channel tests and for the general framing and logging of any experiment.

## Core stance

- **Maximize speed, learning, and focus together.** Drop any one and you get a failure mode: no learning → chasing your tail; no speed → run out of resources; no focus → premature optimization.
- **One key metric per experiment.** Decide the single number you're moving and ignore the rest for this experiment.
- **Smallest thing possible to learn.** You rarely need code. Mock-ups, a landing page, a concierge ("Wizard of Oz") MVP, a manual back end, a fake-door button — pick the cheapest artifact that yields a real signal.
- **Bold before product/market fit.** Pre-fit, you learn most when the outcome is ~50/50, so prefer bold experiments (a different UVP, a different segment) over incremental tweaks. Save micro-optimization for after fit.

## Procedure

1. **Load context.** Read `.lean/risks.md` (what's riskiest), `.lean/PROGRESS.md` (stage), and the canvas. Confirm which assumption this experiment attacks.
2. **Write a falsifiable hypothesis.** Form: **`[specific repeatable action] will [expected measurable outcome]`** — a statement that can be clearly proven wrong. Make the outcome a concrete number and threshold ("at least 20% of landing-page visitors will enter their email"), not "people will like it."
3. **Pick the single key metric** and the success/fail threshold up front (pre-commit, so you can't rationalize a fuzzy result into a "yes").
4. **Design the smallest build.** Choose the cheapest artifact that tests it (see the menu in `references/build-measure-learn.md`). Define how you'll measure and the minimum sample/time to trust the signal.
5. **Run / record.** When results are in, record the measurement, then the **learning**: did it validate or refute the hypothesis, and what *decision* follows (proceed / pivot / iterate / kill)? Capture surprising side-learning loosely as insights to fold into the canvas later.
6. **Write** `.lean/experiments/<id>.md` from `assets/experiment-template.md` (`<id>` like `E1`, `E2`). Update `.lean/PROGRESS.md` (a dated Journal line). If the result retires or moves a risk, update `.lean/risks.md`.
7. **Close the loop.** Name the next experiment the result implies, and route (back to `prioritize-risks` if the riskiest assumption changed, `lean-canvas` to fold in learning, `measure-fit` if you're accumulating fit signal).

## Output

`.lean/experiments/<id>.md` — a falsifiable hypothesis, one key metric + threshold, the build, the measurement, and the learning/decision. A clear next action.

## Related

- `prioritize-risks` — supplies the assumption to test.
- `customer-interview` — the qualitative experiment type (its own skill).
- `measure-fit` — when experiments are about overall product/market-fit signal.
- `references/build-measure-learn.md` — the loop, the smallest-build menu, hypothesis examples.
