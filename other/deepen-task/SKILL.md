---
name: deepen-task
description: Reframe a task or rewrite a prompt for greater rigor when asked for a deeper approach, expert methods, or more ambitious use of AI. Identify missing expert work, primary evidence, concrete methods, and independent validation. Use altitude and range only where they improve the user's goal. For reviewing an existing implementation plan, see plan-review-loop; for unclear marketing copy, see marketing-clarity.
---

# Deepen Task

Turn a surface-level request into an executable brief with stronger evidence,
methods, and checks. Improve the substance of the work without automatically
adding deliverables, length, or complexity.

## Establish the task boundary

Read the supplied prompt and relevant context. Identify the intended outcome,
requested artifact, audience, constraints, available inputs, and what counts
as success. Preserve explicit choices about format, tools, time, and budget.
Ask only when an unresolved detail would materially change the brief;
otherwise state a reasonable assumption.

Match the deliverable to the request. When the user asks to improve a
prompt or reframe a task, return a diagnosis and rewritten prompt. When
they ask for deeper analysis, a better artifact, or execution, apply the
method and produce that work; do not stop at a prompt rewrite. Reframing
alone does not authorize implementation, new data access, installations,
purchases, ongoing monitoring, or external actions.

## Choose where ambition helps

Use depth by default. Consider the other lenses only when they address a
specific weakness in the request; do not force all four into every task.

| Lens | Useful question | Boundary |
|------|-----------------|----------|
| Speed | Can existing work be done with less delay or repetition? | A faster workflow may already satisfy the request; do not add analysis for its own sake. |
| Altitude | What decision or outcome is this artifact supposed to enable? | Keep a required artifact. Offer a different workflow as an option, without silently substituting it. |
| Depth | Which underlying evidence or professional technique would materially improve this result? | Prefer the smallest method that resolves the important uncertainty. |
| Range | Could a method from another field expose a blind spot? | Name the contribution and how it will be checked; avoid a cast of imaginary experts. |

Altitude is especially useful when a task is a proxy for a decision. For
creative work, respect the desired experience or artifact as an end in
itself rather than inventing a business outcome.

## Diagnose before rewriting

Answer these four questions concretely for this task:

1. **Missing expert work.** What would a strong practitioner investigate or
   produce that the request omits? Name the consequential omission and why
   it matters, rather than adopting an expert persona or vocabulary.
2. **Primary evidence.** What is the closest useful source to the underlying
   reality: original text, events, measurements, code, interviews, or visual
   references? Separate evidence already available from evidence to request.
   Raw material is valuable when it resolves uncertainty; do not demand an
   entire dataset when a relevant sample or existing artifact suffices.
3. **Methods and instruments.** Name a specific operation, its input, and
   its output. Choose a tool for the operation, not for its prestige. Check
   availability before claiming it can be used; express unavailable tooling
   as a requirement or provide a workable alternative.
4. **Independent check.** What observable evidence could contradict the
   result, beyond the authoring model's confidence or the user's approval?
   Specify the check, comparator, and acceptance criterion where justified.
   Examples include held-out observations, a reproduction, a relevant
   benchmark, a source comparison, or a task-based audience evaluation.
   Another model's agreement can help review but is not ground truth.

Challenge the most important assumption. Distinguish a hypothesis from a
finding and correlation from causation. For creative or interpretive work,
separate factual/source checks from judgments of taste; no single metric
proves artistic quality.

When a target seems difficult, identify the limiting assumption and a
bounded experiment. A stretch goal can guide exploration, but do not call
an unmeasured target feasible or keep retrying without new evidence. For
stalled work, isolate the uncertain step into smaller questions with
checkable intermediate outputs.

## Write the executable prompt

Return a short explanation of the material changes, then a self-contained
prompt the user can paste into a fresh session when a rewrite is requested.
For an execution request, use these elements to guide the work rather
than adding an unsolicited prompt artifact. Include:

- The outcome and requested deliverable, with the original constraints.
- The evidence to inspect, identifying supplied inputs and missing inputs.
- The consequential expert work and specific methods it requires.
- How to challenge the key assumption and verify the result independently.
- How to report uncertainty, evidence gaps, and a stopping condition suited
  to the task's time, budget, and risk.

Use only the elements that matter; do not turn this into a mandatory long
template. Keep optional changes in scope separate from the main prompt.
If the original request is already rigorous, say so and make only the
changes that improve execution. For a simple constrained request, a short
rewrite or no rewrite can be the right result.

Mark proposed checks as proposed. Claim a result is verified only after
the check has actually run and its output supports the claim. If essential
evidence is unavailable, name the gap and provide the best bounded next
step instead of fabricating a conclusion.

For worked examples, routing boundaries, and the source analysis, read
[references/examples-and-source.md](references/examples-and-source.md) when
calibrating an unfamiliar task or explaining the method's origin.

## Attribution

Adapted from Felix Rieseberg's
[How to be more ambitious: A tutorial for humans with models](https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/)
(13 October 2026), surfaced by
[CG's X post](https://x.com/cgtwts/status/2110571916973207906).
The source proposes four ambition lenses; this skill adds an executable
brief workflow and explicit limits on scope and validation claims.
