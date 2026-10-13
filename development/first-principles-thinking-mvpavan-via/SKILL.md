---
name: first-principles-thinking
description: Use when explicitly requested, or only when a consequential decision hinges on an unresolved foundational assumption that ordinary inspection or the active workflow cannot settle. Skip routine edits, straightforward fixes, settled implementation plans, and generic requests to think critically.
---

# First Principles Thinking

Adapted from the supplied *First Principles Thinking — The D.A.R.E. Framework*
prompt pack: Decompose, Audit, Recombine, Experiment. This is the structured
workflow for exceptional cases; the everyday operating principle does not
require loading this skill on every task.

## Activation boundary

Explicit invocation is sufficient. Otherwise, use only when all three hold:

- A decision materially affects the outcome, architecture, cost, or reversibility.
- A foundational premise is unsupported, contradicted by evidence, or implicated
  in repeated failures; changing it could change the chosen approach.
- A focused lookup, ordinary inspection, or the active debugging/design/review
  workflow cannot adequately settle that premise.

Name the decision and suspect premise in one sentence. Task size, complexity,
the words "critical thinking", and the AGENTS.md opening principle alone are
not triggers. For example, repeated evidence against a core product premise may
qualify; a typo, known bug fix, or implementation of an approved contract does not.
Use this within the active task, without starting a parallel review ceremony.

## D — Decompose

State the requested outcome and success criteria. Break the problem into its
smallest useful components and show their relationships. Stop when another split
would not improve examination. Keep decomposition separate from evaluation and
solution proposals.

If a deeper objective appears, identify it as a hypothesis. Preserve the stated
problem; ask before substituting a materially different objective. Continue work
that does not depend on that choice.

## A — Audit assumptions

Rank the premises by how much the decision depends on them. For each material
premise, record its evidence, classify it as verified fact, convention, or
unknown, and explain what removing or inverting it would change. Check evidence
against primary sources where available; an unsupported claim remains unknown.

Separate chosen requirements from empirical claims. User constraints, safety
boundaries, and approved contracts remain binding unless authorized to change;
questioning their rationale does not suspend them.

## R — Recombine facts

Build alternatives from verified components and binding constraints. Seek up to
three structurally different approaches when meaningful alternatives exist;
do not invent options to fill a quota. For each, identify its supporting facts,
the convention it challenges, and its largest failure risk. Label every new
assumption. Keep an existing solution when the evidence supports it; novelty
alone is not a benefit.

## E — Experiment against reality

For each viable approach, identify the smallest affordable test of its decisive
assumption: concrete action, observable result, rejection threshold, result that
keeps it viable, and what either result teaches. State which premise to revisit
if all approaches fail. Survival of one test is not proof of the whole solution.

Run checks already authorized by the task. Propose experiments needing new
authority; this skill grants no permission for prototypes, spending, external
messages, deployment, or destructive actions.

## Output and stopping point

Return a concise decision brief: outcome, decisive facts and assumptions,
recommendation or unresolved choice, and the cheapest discriminating test with
its pass/fail criteria. Distinguish observed results from proposed tests.

Stop when evidence supports the next authorized step, or when a specific missing
fact or owner decision prevents choosing safely. Resume the active workflow;
do not keep decomposing, generate speculative redesigns, or reopen settled
decisions without new evidence or an explicit request.
