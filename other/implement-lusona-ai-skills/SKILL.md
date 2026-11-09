---
name: implement
description: Implement an authorized bounded change with adaptive planning, explicit TDD, and verification. Also use for explicit planning-only requests, which end with a proposed approach and do not authorize implementation.
---

# Implement

Apply the [core](../../README.md#loading-rules); read linked procedures only when their
operation applies.
Persona: implementation engineer, responsible for necessary decomposition, completing
authorized work, and verifying the agreed outcome.

Reuse the owning record. At entry, and again when scope grows, decide whether the change
requires independent review under
[Review and communication](../../README.md#review-and-communication). Direct work without a
spec may use [notes](../../templates/notes.md); [retention](../../references/retention.md)
states when a spec and queue row are required.
If creating a spec, use relevant sections of the [change record](../../templates/spec.md) at
`docs/lusona/specs/<change-id>.md` under [naming](../../references/naming.md).
A clear authorized request does not require Specify first.
Maintain existing separate plans in place; do not migrate records or create a companion plan by default.

## Assess the agreement and current evidence

- Inspect the working tree, relevant code, callers, and tests. When using or creating a spec,
  apply the [queue rules](../../references/queue.md). Read acceptance criteria, constraints,
  explicit TDD and its source, completion conditions, applicable ADRs, and existing evidence.
  Reuse settled decisions. For a linked visual reference, apply
  [visuals](../../references/visuals.md).
- Resolve missing behavior or scope through [specify](../specify/SKILL.md),
  consequential technical decisions through [architect](../architect/SKILL.md), and empirical
  uncertainty through [investigate](../investigate/SKILL.md) when needed.
- Apply the [TDD rules](../../references/tdd.md).
- Choose planning depth from dependencies, uncertainty, coordination, and recovery needs,
  including a long run whose earlier context will be summarized before it finishes.
  Straightforward work needs an outcome and checks, not a manufactured task list. Add an
  optional execution section when sequencing helps. Detail the next useful increment; expand
  later tasks only to resolve dependencies or meet an explicit planning request.
- When tasks are useful, give each an observable outcome, scope, dependencies, and completion
  checks linked to criteria without repeating requirements. Confirm existing paths and commands;
  label proposals and unverified commands, and resolve command uncertainty before relying on a
  check. Establish consumed/produced interfaces, ownership,
  and mutable verification resources before dependent or concurrent work.
- Establish verification and recovery before authorized persistent-data or deployment operations,
  including migration ordering when needed.
- Before execution, check that scoped acceptance criteria have planned or existing verification
  and the next increment has expected results and no blocking ambiguity. Fix routine omissions
  inline without adding an approval gate. Revise the approach as evidence changes within authority.
- For planning-only work, report the proposed execution section, assumptions, unresolved decisions,
  verification approach, and concrete next action.

## Implement and check bounded increments

- Maintain lifecycle state under the [queue rules](../../references/queue.md).
- Follow the recorded TDD sequence in coherent bounded increments through observable interfaces,
  with red/green evidence for test-first behaviors.
- Investigate uncertainty before escalating a decision.
- Run agreed and applicable repository checks. Judge status and output against defined expected
  results, including explicitly required error behavior; an arbitrary nonzero exit is not success.
  Report environmental blockers.
- Inspect each increment's evidence and choose the next action from remaining criteria or
  uncertainty; revisit clarification, design, or investigation when evidence requires it,
  preserving accepted constraints and authority. Inspect the final diff for defects, unintended changes, and unnecessary complexity.
- Evaluate success against agreed behavior, not task completion. Record human acceptance only
  when given.
- Record results, check and review evidence, limitations, and the current handoff in the owning
  change record under [retention](../../references/retention.md); the coordinator applies
  [closeout](../../references/closeout.md) before removing a Done row.

## Commit verified increments

Complete the selected TDD sequence and required verification, then apply the
[commit procedure](../../references/commits.md), subject to user and repository restrictions.

## Next action

Continue the next authorized increment. At the authorized boundary, report behavior,
consequential decisions, evidence, and remaining uncertainty, and name any required review,
acceptance, delivery, or blocker with its inputs. Recommend [refactor](../refactor/SKILL.md)
only for a concrete structural problem.
