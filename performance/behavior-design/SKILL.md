---
name: behavior-design
description: Use when a goal must be converted into a repeatable behavior, cue, SOP, review cadence, and identity-aligned reinforcement.
metadata:
  version: "8.1.0"
  updated: "2026-08-18"
  profile: "stateful"
  assumes: "The actor, desired outcome, and operating context can be observed or probed."
  conflicts_with: "Coercive behavior design, vague motivation advice, or unmeasured habit claims."
---

# Behavior Design

<skill_contract>
  <input>Actor, desired outcome, current behavior, context, constraints, baseline evidence, and review horizon.</input>
  <output>An agency-preserving HAS behavior system with cues, effort levels, SOP, measures, recovery, and review cadence.</output>
  <done>The target behavior is observable, runnable on a low-motivation day, evidenced, and assigned one review owner.</done>
  <non_goals>Coercion, unsupported identity claims, vague motivation advice, or optimizing lagging outcomes without behaviors.</non_goals>

Convert an outcome into the smallest observable behavior system that can survive low-motivation days. Preserve agency; optimize the environment before blaming the actor.

## Usage Template

Provide: desired outcome, actor, context, current behavior, constraints, review horizon, and available evidence. Optional: failed attempts and environmental cues.

## Workflow

<intake>

1. Restate the outcome as an observable change, not an identity label.
2. Establish baseline frequency, friction, trigger context, and hard constraints.
3. Separate controllable behavior from lagging outcome.
4. Set one review horizon and one owner.

</intake>

<unknowns_gate>

Classify unknowns as known, probeable, testable, or blocked. If actor, target behavior, or safety boundary is absent, return `NEEDS_INPUT` with one minimal question. A reversible assumption is allowed only when labeled and paired with a same-cycle test.

</unknowns_gate>

<execute>

Build the HAS sequence:

1. **H1 Goal:** translate the outcome into one leading behavior and one lagging measure.
2. **H2 Habit:** define anchor, cue, location, and three effort levels: minimum (about 2 minutes), normal, and stretch.
3. **H3 SOP:** write `trigger -> action -> evidence -> recovery -> stop` so a missed run has a next move.
4. **H4 Review:** select a cadence; compare planned versus observed behavior and change one variable only.
5. **H5 Identity:** use evidence-based reinforcement: “I am becoming X because I repeatedly did Y,” never unsupported affirmation.

Reduce friction before adding motivation. Prefer defaults, visible cues, prepared tools, and short feedback latency. Keep the minimum behavior useful rather than ceremonial.

</execute>

<evaluate>

Check that the behavior is observable, starts in a named context, fits the minimum effort budget, produces evidence, and has a recovery path. Reject plans that depend on constant willpower, hide coercion, or measure only outcomes. If the check fails, revise the highest-friction element once and re-evaluate.

</evaluate>

<state_contract>

Persist `{run_id, status, attempt, budget, evidence, unknowns, last_error, next_action}` plus baseline, current H1-H5 design, review date, and revision history. Update atomically after each review; never overwrite prior observations.

</state_contract>

## Failure Protocol

- `NEEDS_INPUT`: a target, actor, or boundary is missing; ask one narrow probe.
- `INSUFFICIENT_EVIDENCE`: baseline is unknown; run a short observation period before optimizing.
- `VERIFY_FAILED`: the behavior is not observable, feasible, or linked to the outcome; revise one variable.
- `BUDGET_STOP`: the review horizon or effort budget is exhausted; preserve state and report the next experiment.

## Output Contract

Return `status`, `result` (H1-H5 plan), `evidence` (baseline and measures), `unknowns`, and `next_action` (owner plus review date).

## Edge Cases

- Motivation is near zero: keep the cue and reduce the action to a useful minimum; do not expand the reward system.
- Repeated misses occur despite compliance: treat the goal-behavior link as unverified and test a different leading behavior.

## Success Metrics

- One named cue reliably starts one observable minimum behavior.
- Execution evidence is captured at the chosen cadence.
- Reviews change the system using observed friction, not self-judgment.

## Quality Gates

- [ ] Outcome, leading behavior, and lagging measure are distinct.
- [ ] Minimum action, recovery path, owner, and review date exist.
- [ ] The design preserves agency and has no coercive mechanism.
- [ ] Completion claims use observed behavior evidence.

</skill_contract>
