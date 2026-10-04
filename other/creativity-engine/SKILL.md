---
name: creativity-engine
description: Use when a defined problem needs diverse ideas, cross-domain combinations, and cheap experiments instead of a single untested answer.
metadata:
  version: "8.1.0"
  updated: "2026-08-18"
  profile: "one-shot"
  assumes: "A problem, target user, and at least one meaningful constraint can be stated."
  conflicts_with: "Unbounded brainstorming, novelty without utility, or treating generated ideas as validated opportunities."
---

# Creativity Engine

<skill_contract>
  <input>Defined problem, target user, desired change, constraints, prior attempts, and experiment budget.</input>
  <output>Three non-equivalent options with scored mechanisms and falsifiable minimum experiments.</output>
  <done>Each selected option has a hypothesis, smallest artifact, participant, threshold, budget, stop rule, and failure learning.</done>
  <non_goals>Unbounded brainstorming, novelty without utility, polished prose before diversity, or presenting ideas as validated demand.</non_goals>

Create option value by combining mechanisms, constraints, and analogies, then convert the strongest options into minimum experiments.

## Usage Template

Provide: problem, target user, desired change, constraints, existing attempts, and experiment budget. Optional: domains or concepts to combine.

## Workflow

<intake>

Rewrite the request as `For [user], change [state] under [constraints], measured by [signal]`. Extract reusable building blocks: actors, assets, mechanisms, channels, incentives, and constraints.

</intake>

<unknowns_gate>

If no user, problem, or constraint is available, return `NEEDS_INPUT` with one discriminating probe. Treat market demand, technical feasibility, and user behavior as testable unknowns, not assumptions to hide.

</unknowns_gate>

<execute>

1. Generate 10-20 combinations across at least three mechanisms or domains.
2. Include inversion, subtraction, constraint removal, and one distant analogy.
3. Cluster duplicates by underlying mechanism, not wording.
4. Score survivors on expected value, test difficulty, distinctiveness, reversibility, and evidence gap.
5. Select three non-equivalent options.
6. For each, define a minimum experiment: hypothesis, smallest artifact, target participant, success threshold, budget, stop rule, and learning captured on failure.

Do not optimize prose before option diversity. A useful failed experiment is better than an impressive concept with no falsifier.

</execute>

<evaluate>

Check that the top three differ in mechanism, fit constraints, expose their largest unknown, and can be tested cheaply. Remove ideas that are only features, slogans, or unsupported scale claims. Recombine once if all finalists share the same failure mode.

</evaluate>

## Failure Protocol

- `NEEDS_INPUT`: the problem frame lacks a user or constraint.
- `INSUFFICIENT_EVIDENCE`: ranking depends on unavailable market or technical facts; mark provisional and probe.
- `VERIFY_FAILED`: finalists are duplicates or have no falsifiable test; regenerate around different mechanisms.
- `BUDGET_STOP`: no experiment fits the budget; return the cheapest information-gathering action.

## Output Contract

Return `status`, `result` (idea clusters and top-three experiments), `evidence` (inputs and scoring basis), `unknowns`, and `next_action`.

## Edge Cases

- The requester supplies a favored solution: include it as one candidate, then generate alternatives from different mechanisms before ranking.
- The domain is regulated or safety-critical: make approval and compliance discovery part of the experiment; do not test on live users without authorization.

## Success Metrics

- At least three materially different mechanisms survive evaluation.
- Every finalist has a bounded, falsifiable experiment.
- The next experiment reduces the largest decision-relevant unknown.

## Quality Gates

- [ ] Problem, user, constraint, and signal are explicit.
- [ ] Idea count and diversity thresholds are met.
- [ ] Rankings state assumptions and evidence gaps.
- [ ] Experiments include threshold, budget, and stop rule.

</skill_contract>
