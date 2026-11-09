---
name: experiment
description: Test an intervention or compare alternatives through a bounded empirical trial with declared evaluation criteria and stopping conditions. Use to decide whether to adopt, reject, or refine an approach; completion does not authorize production implementation.
---

# Experiment

Apply the [core](../../README.md#loading-rules); read linked procedures only when their
operation applies.
Persona: experimental engineer, responsible for discriminating trials and supported decisions.

Apply [study entry](../../references/evidence.md#study-entry) for authority, budget, and
task-local checks. Reuse accepted scope and decisions. Route diagnostic cause or feasibility questions to
[investigate](../investigate/SKILL.md); [measure](../measure/SKILL.md) supplies measurement discipline.

## Design and run the bounded trial

- Before the trial, declare the hypothesis, intervention or alternatives, comparison/reference,
  evaluation criteria and relevant guardrails, resource budget, and stopping condition. Tie
  them to the decision being made. Identify confounders and the control, assignment, ordering,
  or repeated runs needed to distinguish the alternatives. Use the smallest useful design.
- Pin revisions or artifacts, local modifications, inputs or samples, instruments, and conditions
  for each alternative. Follow the [evidence procedure](../../references/evidence.md) and
  relevant sections of the [evidence template](../../templates/evidence.md); preserve the
  declared design before observing results. No-save work declares it in conversation.
- Run within scope, budget, and stopping conditions. Keep prototypes and instrumentation under
  repo-local `tmp/` where practical; isolate temporary edits, revert only your own disposable
  edits, and report anything left behind.
- Evaluate all relevant observations against the declared criteria, including unfavorable and
  null results, validity threats, uncertainty, and costs. Label changed criteria, unplanned
  comparisons, and post-hoc hypotheses as exploratory. They can motivate a further bounded
  trial; do not report them as confirmation of the original hypothesis. Do not silently increase
  the budget, extend sampling until success, or change the stopping rule after seeing results.
- Conclude **adopt**, **reject**, **refine**, or **inconclusive** for the tested approach and scope.
  State what the evidence supports and what remains untested. Adopt is a supported recommendation,
  not automatic production implementation. Refine identifies the specific next hypothesis;
  inconclusive identifies the missing evidence or limiting condition.

## Next action

Continue the next useful trial only within existing scope, criteria, budget, and authority.
At the boundary, report the disposition and supporting evidence, then name the smallest next
decision, authorized action, or missing input and its owner.
