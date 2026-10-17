---
name: refactor
description: Run only the Refactor phase of one Predictive TDD cycle — review the green code against the Four Rules of Simple Design, apply the domain-responsibility review, and run the mandatory domain-boundary trial. Invoke when the user asks for /refactor, for the next Refactor step, or wants to drive Red-Green-Refactor one phase at a time instead of letting the full cycle run.
---

# Refactor — one phase, manually driven

> **This is a manual phase control, not a separate method.** It runs step 4 of
> the predictive cycle and then stops. Use it when you want to steer
> Red-Green-Refactor yourself instead of invoking the whole `exact-coding`
> workflow. The method lives in one place; this skill only selects which part of
> it to execute now.
>
> For a measured cleanup pass over the whole finished tree rather than one green
> step, use `end-refactor` instead.

## What to read

1. `.claude/skills/predictive-tdd/SKILL.md` — section **4. Inspect and
   refactor**, including **Domain responsibility review** and the **Mandatory
   domain-boundary trial**. That section is binding as written, with its
   before/after records.
2. The matching profile under `.claude/skills/predictive-tdd/stacks/` for
   language- and framework-specific application guidance only.
3. `.claude/skills/exact-coding-shared/human-in-the-loop.md` for the Refactor checkpoint and the prediction-mismatch rule.

## What to do

First verify the behavior tests are green and say so. Refactoring on red is not
permitted by the Core rules; if anything fails, stop and offer `green` instead.

Then execute exactly step 4 of the cycle as written in the Predictive TDD
skill: the Four Rules review in order, the domain-responsibility review, and the
domain-boundary trial with its recorded `Domain responsibility` /
`Independent change axes` / `Boundary candidate` and `Boundary outcome` /
`Semantic change` / `Fewest Elements check` blocks. Analysis alone is not the
attempt — when a credible seam exists, try the structural change and keep or undo
it on the evidence.

Make at most one refactoring at a time and predict and run the smallest relevant
check after each.

Both refactor profiles ship in this tree. If the human named the isolated profile, delegate the review through the Agent tool with `subagent_type: refactor` and verify Green before applying the checkpoint yourself; otherwise refactor inline in this context.

## Where to stop

Stop at the Refactor checkpoint from `.claude/skills/exact-coding-shared/human-in-the-loop.md` — including when no change improved
the code. Report the Four Rules decision, the boundary record, any change made,
and the passing gates. Do not close the cycle by activating the next behavior —
the human invoked a single phase; that invocation is the checkpoint, and they
drive the next behavior with `red`.

On a prediction mismatch, follow **Prediction mismatch** in the Predictive TDD
skill and stop there.
