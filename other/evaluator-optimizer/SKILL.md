---
name: evaluator-optimizer
description: >
  Generate a solution, evaluate it against explicit pass/fail criteria,
  refine using the feedback, repeat until it passes or a round cap is hit.
  Use for tasks with a clear, checkable bar and demonstrable value from
  iteration — a bug fix that must pass a test suite, code that must satisfy a
  lint/style rubric, a document that must meet stated requirements. Distinct
  from advisor-checkpoint (one strategic consult before committing) — this is
  a convergence loop against a concrete standard.
---

# Evaluator-Optimizer

Generate → evaluate against explicit criteria → refine with the feedback →
repeat until it passes or a round cap is hit. Use it when two things are both
true: there's a **clear bar** (tests, a lint rule, a stated requirement — not
"make it better") and refinement **demonstrably helps** (a model can act on
concrete feedback better than it produced the first draft blind). If either
is missing — no checkable criteria, or one attempt is already as good as five
— skip the loop; it just burns rounds for no gain.

This is a different shape from `advisor-checkpoint`: that skill is one
strategic consult before you commit to an approach. This is a loop that
converges *one artifact* against a bar you can actually check.

## Prefer an objective check over an opinion

Whenever the task has one, run the real check — a test suite, `go
vet`/`swiftlint`/a build — rather than asking a model to judge. A test result
is ground truth; a model's opinion about whether code "looks correct" is not.
Reserve a model-as-evaluator for criteria that genuinely can't be
mechanically checked (architecture quality, whether a document actually
answers the stated question, prose clarity).

## The loop

1. **Generate.** Produce a candidate against the task.
2. **Evaluate.** Run the objective check, or — if there isn't one — dispatch
   an evaluation only against explicit criteria you state up front (not "is
   this good," but "does it satisfy: correctness, no new lint violations,
   handles the empty-input case"). The evaluator's job is to grade, not to
   fix — keep the roles separated so the feedback is a clean signal, not a
   silent rewrite.
3. **Refine.** If it fails, feed the concrete failure (the test output, the
   lint error, the evaluator's specific complaint) back into the next
   generation — not "try again," but "this failed because X."
4. **Repeat**, capped at 3-5 rounds. If it hasn't converged by then, stop and
   surface the failure rather than keep spinning — a persistent failure after
   several rounds usually means the criteria are wrong, the task is
   underspecified, or the approach needs to change, not that round 6 will
   suddenly pass.

## In an interactive session

The build/test/fix cycle you already run is this loop with an objective
evaluator. Make it explicit when the criteria are less obvious than
"tests pass" — e.g., state the acceptance bar before generating, so the
evaluation step (yours or a dispatched `Agent` call) has something concrete
to check against instead of re-deriving what "done" means each round.

For a single session converging toward one checkable condition, `/goal
<condition>` is the native version of this loop — it re-evaluates the
condition after every turn and keeps the session going until it holds,
without hand-rolling the round-and-check bookkeeping yourself. Reach for it
when the loop lives entirely in one conversation; reach for the Workflow
script below when you need custom evaluator logic, multiple candidates, or
the loop spans more than this one session.

## In a Workflow script

```js
const CRITERIA = 'Correctness, no new lint violations, handles empty input.'
let candidate = await agent(`Implement <task>. Must satisfy: ${CRITERIA}`)

for (let round = 0; round < 4; round++) {
  const verdict = await agent(
    `Evaluate ONLY — do not fix. Criteria: ${CRITERIA}\n\nCandidate:\n${candidate}\n\n` +
    `Reply PASS, or FAIL with the specific failure.`,
    { label: `evaluate-r${round}` }
  )
  if (verdict.includes('PASS')) break
  candidate = await agent(
    `Refine to fix this specific failure (keep everything else): ${verdict}\n\nCandidate:\n${candidate}`,
    { label: `refine-r${round}` }
  )
}
```

Don't confuse this with the workflow tool's loop-until-dry / loop-until-count
patterns — those accumulate a growing set of findings across rounds
(discovery). This converges a single artifact toward a fixed bar
(refinement). Reach for whichever matches what the round is actually doing.
