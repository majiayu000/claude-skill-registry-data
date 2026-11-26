---
name: green
description: Run only the Green phase of one Predictive TDD cycle — make the smallest production change that satisfies the active failing test, with a stated prediction before the check. Invoke when the user asks for /green, for the next Green step, or wants to drive Red-Green-Refactor one phase at a time instead of letting the full cycle run.
---

# Green — one phase, manually driven

> **This is a manual phase control, not a separate method.** It runs step 3 of
> the predictive cycle and then stops. Use it when you want to steer
> Red-Green-Refactor yourself instead of invoking the whole `exact-coding`
> workflow. The method lives in one place; this skill only selects which part of
> it to execute now.

## What to read

1. `.cursor/skills/predictive-tdd/SKILL.md` — sections **Core rules** and
   **3. Reach Green minimally**. Those are binding as written.
2. The matching profile under `.cursor/skills/predictive-tdd/stacks/` for the
   commands to run.
3. `.cursor/skills/exact-coding-shared/human-in-the-loop.md` for the prediction-mismatch rule.

## What to do

Confirm there is an active behavioral Red to satisfy. If the suite is already
green, say so and stop — there is nothing for this phase to do; offer `red` or
`refactor` instead.

Then execute exactly step 3 of the cycle:

- make the smallest production change likely to pass the active test, without
  anticipating inactive examples — hardcoded values and narrow conditionals are
  valid intermediate steps,
- predict the focused test's outcome, including expected pass/fail and todo
  counts where the stack reports them,
- run it and compare prediction with reality.

## Where to stop

Stop after the active test is green. Report the change, the prediction, and the
actual result. Do not refactor, and do not start the next behavior — even
though Green has no default checkpoint in `.cursor/skills/exact-coding-shared/human-in-the-loop.md`. The human invoked a single
phase; that invocation is the checkpoint.

On a prediction mismatch, follow **Prediction mismatch** in the Predictive TDD
skill and stop there. Never change production behavior merely to make an
unexplained failure disappear.
