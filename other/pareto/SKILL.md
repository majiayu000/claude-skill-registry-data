---
name: pareto
description: >
  Processes the user's request through the Pareto Principle. It ranks the causes that generate
  most of the outcome, spends roughly a fifth of the effort on the interventions that address them,
  and reports what that effort bought. This skill is user-only: it runs only when the user invokes
  /pareto [request]. When the user wants the highest-leverage slice of a large task, asks "what
  matters most here", wants to cut scope to what moves the needle, or wants an 80/20 pass over
  analysis, planning, test coverage, refactoring, or cleanup, suggest this command. Do not use it for
  work whose value depends on being complete, such as a security fix, a compliance change, a
  migration, or a specific reported bug.
argument-hint: "[request to process]"
disable-model-invocation: true
---

# Pareto

A small subset of causes produces most of the outcome. Find that subset, spend about a fifth of the effort against it, and show the cut, so the user can argue with it.

Estimate roughly throughout. "80/20" is shorthand for "expect lumpiness", and not a ratio to hit. The two percentages do not have to pair, so a fifth of the effort can buy 95% of the outcome, or 40%. A rough ranking that costs minutes beats a precise one that eats the budget it was meant to allocate.

## When this is the wrong tool

Some work is worth doing only in full: a security fix, a compliance change, a migration, or a specific reported bug. 80% of a data migration is a corrupted database. Say that the request is not a Pareto candidate, then do the work in full, or ask the user.

When you decline the framing, decline its shape too. Give a checklist to finish, and not a ranked list that the reader can stop partway down. On completeness-critical work, the skipped item is the one that matters.

Skip the ceremony entirely on anything small enough that ranking it costs more than it saves.

## Stage 1: rank the causes

Rank causes, and not tasks. Work items sorted by payoff are only a to-do list. Asking "what is generating most of this?" is what finds the one confused module behind eight scattered bug reports. Weight the causes by cost or severity rather than by raw counts, so that a rare catastrophe does not sit buried under a constant nuisance.

Rank on effect size alone. What a fix costs plays no part yet. When "that is expensive" suppresses a cause here, it buries the finding that the user most needs. This stage produces a ranking, and not a shortlist, so that stage 2 can still reach into the tail.

Use whatever signal is already visible: error rates, coverage gaps, file churn, or the shape of the request. When no signal exists, rank from priors, and label that in a clause. An unlabeled guess reads as measurement.

**When the causes are evenly spread**, say so before you spend anything. Five independent bug fixes are five bug fixes. Name the flatness, and let the user choose between funding the whole job and taking an arbitrary slice.

## Stage 2: spend a fifth of the effort

Cost the interventions against the top causes. Work down by outcome per unit of effort, until you have spent roughly a fifth of the effort of the full job, then stop. Effort is the budget, and outcome is what you observe and report. The reverse rule, which is to keep going until most of the outcome is covered, authorizes spending whatever it takes.

Both stages earn their place. Ranking causes while you ignore cost recommends a rewrite every time. Ranking interventions without first finding the causes drifts to cheap triviality, which is eight one-line fixes that leave the generator untouched.

**Spend the budget on the work, and not on deciding what the work is.** The deliverable is the change that the user asked for. Buy measurement only when it is cheap and decisive. That means a check that redirects the whole effort, and not a survey that produces a plan. When the honest answer is that the budget buys diagnosis and no improvement, say so plainly as a trade-off. Do not hand over an investigation as though it were the work.

**An unaffordable root cause is a finding, and not a skip.** When the biggest cause needs work that swamps the budget, name it with its price. Write it as "Most of these failures trace to the retry logic, and fixing it properly is about three days". That is the one thing that the user cannot get from the diff.

Sweep up the near-free wins from the tail while you are in there. Keep them incidental to the vital few, and do not let them become the work.

Correctness is not optional weight. A slice that leaves the build broken, or a migration half-applied, has negative value, so whatever keeps the work coherent belongs inside the budget.

## Two shapes of request

**Analysis, planning, and review**: the budget caps the depth of the investigation. Lead with the top causes at full depth, compress the tail, and name what you did not examine. An analysis that hides its own shallowness is worse than a slower one.

**Actual work, such as coverage, refactoring, cleanup, and fixes**: the budget caps the changes you make. Do the subset, leave the rest untouched rather than half-applied, and report the line that you drew.

## Report the cut

Write a few sentences, and not a section per bullet:

- **The vital few causes**, and how you ranked them.
- **What the budget bought**: the rough share of effort spent against the rough share of outcome gained, reported as observations rather than as the prediction of the principle. Skip any number that you cannot estimate honestly.
- **What is left**, grouped, with minor items separated from unaffordable ones. The second group is the user's next funding decision.
