---
name: red
description: Run only the Red phase of one Predictive TDD cycle — activate exactly one behavior and reach a behavioral Red with a stated prediction. Invoke when the user asks for /red, for the next Red step, or wants to drive Red-Green-Refactor one phase at a time instead of letting the full cycle run.
---

# Red — one phase, manually driven

> **This is a manual phase control, not a separate method.** It runs step 1 and
> step 2 of the predictive cycle and then stops. Use it when you want to steer
> Red-Green-Refactor yourself instead of invoking the whole `exact-coding`
> workflow. The method lives in one place; this skill only selects which part of
> it to execute now.

## What to read

1. `.opencode/skills/predictive-tdd/SKILL.md` — sections **Core rules**,
   **1. Activate one behavior** and **2. Reach behavioral Red**. Those are
   binding as written.
2. The matching profile under `.opencode/skills/predictive-tdd/stacks/` for
   inactive-test syntax and the commands to run.
3. `.opencode/skills/exact-coding-shared/human-in-the-loop.md` for the Red checkpoint and the prediction-mismatch rule.

If no ordered test list exists yet, say so and offer `test-list` first. Do not
invent a list as a side effect of this phase.

## What to do

Execute exactly those two steps of the cycle, then stop:

- activate one behavior from the test list,
- predict the narrowest test's outcome, failure category, and message or values,
- run it and compare prediction with reality,
- add only enough scaffold to reach a behavioral failure, re-predicting each time.

## Where to stop

Stop at the Red checkpoint from `.opencode/skills/exact-coding-shared/human-in-the-loop.md` and report the active behavior, the
prediction, the actual result, and why this failure is the intended behavioral
Red. Do not write production behavior, and do not continue into Green — even
when the Autonomy Level would not stop there. The human invoked a single phase;
that invocation is the checkpoint.

If the activated test already passes, confirm that prediction, record that no
production change is needed, and stop. Do not manufacture a failure.

On a prediction mismatch, follow **Prediction mismatch** in the Predictive TDD
skill and stop there.
