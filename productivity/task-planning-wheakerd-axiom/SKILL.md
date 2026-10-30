---
name: task-planning
description: Create or revise an actionable task plan from the user's current requirements. Use when the user explicitly requests a task or implementation plan, or asks to remove, replace, merge, reorder, or narrow items in an existing plan. Keep retained decisions, dependencies, and acceptance criteria consistent with the current scope. Do not use for scheduled automations, progress reports, ordinary chat corrections, plan execution, or specialized planning already owned by another Axiom route. An explicit task-planning invocation may refine that plan's presentation while preserving its owner's constraints and authority.
---

# Task Planning

Produce a self-contained plan that describes the work currently requested.
Treat the plan as the current agreement about the work. Size its detail to the
task and preserve the user's preferred format when it remains useful.

Defaults you may adapt, saying so: plan structure and detail, question count, and the order of the final checks. Every other rule here and in the references the active phase loads binds.

## Select The Planning Phase

- Use the request and the existing artifact to identify planning; a visible host plan-mode indicator is not required.
- A request to formulate or revise a plan authorizes that planning work. Execution, scheduling, creating another host task, and saving a file require their own applicable user intent. Carry forward authority already granted; do not add a confirmation gate merely because a plan was produced.
- Specialized Axiom workflows retain their domain and authorization rules. Select their owner for specialized planning. When explicitly invoked to refine such a plan, apply this skill to its presentation and consistency without replacing those rules or resolving a material workflow choice for the user, unless the user explicitly delegated that choice and every alternative is reversible and already authorized; then state the choice and why before acting. An offered option authorizes no persistent system change, external or remote-state change, deletion, credential use, or material cost.
- Read `references/scope-revisions.md` when a revision removes, replaces, or restores scope, or when dependency and constraint treatment is uncertain.

## Establish The Current Requirements

1. Read the latest request, the relevant existing plan, and enough task context
   to identify the requested outcome. Inspect source material only as needed
   to make the plan concrete.
2. Preserve user requirements and still-valid decisions. Distinguish explicit
   constraints from assistant suggestions, assumptions, and historical
   discussion; a suggestion in an earlier draft is not a user requirement.
3. Apply the user's changes at the scope they identify. If an item number,
   target, or dependency is materially ambiguous, ask one focused question and
   continue independent planning work. Clear deletions need no reconfirmation.
4. Use the latest user choice for the affected scope. Removing an item from
   this plan does not create a permanent ban on that item. A later request may
   restore it within the user's current authority.

## Build Or Revise The Plan

- For a new plan, describe the requested outcome, necessary steps, relevant
  dependencies, and observable acceptance criteria. Add assumptions only when
  they affect a decision. Scale the structure to the work; a small task may
  need only a few steps.
- For a revision, preserve unaffected goals, decisions, and useful detail.
  Apply the requested change and repair the affected structure instead of
  redesigning unrelated parts of the plan.
- Remove canceled or superseded scope wherever it contributes work: goals,
  steps, deliverables, dependencies, acceptance criteria, examples, and open
  questions. Renumber and repair references after the change.
- Write the remaining plan affirmatively around its current work. Do not
  carry canceled items into non-goals, exclusion lists, repeated disclaimers,
  or explanations of how they will not be implemented. Their removal alone
  is not a reason to mention them in the new plan.
- Keep an explicit, still-effective constraint when it affects current work,
  such as local-only data handling or a fixed budget. Place it once where it
  informs implementation or acceptance. User-requested scope statements and
  applicable domain requirements remain valid reasons to state a boundary.
- If removing an item makes a retained goal infeasible, identify the concrete
  dependency and resolve the affected choice. Do not silently restore removed
  work, promise an impossible result, or turn the canceled feature into a
  continuing task.

## Deliver The Current Plan

By default, return the updated plan as a complete artifact that can be read
without the edit history. If the user requests only a changed section, a diff,
or a change summary, provide that format and repair any affected references.
Keep requested revision history separate from the plan body.

Before returning the plan, check:

1. Every task and acceptance criterion serves a current requirement or a
   necessary, supported dependency.
2. Removed and superseded work has no remaining implementation obligation or
   incidental exclusion narrative.
3. Retained goals, explicit constraints, and unaffected decisions are intact.
4. Steps, dependencies, references, and acceptance criteria agree.
5. Material uncertainty is visible at the affected decision; the plan adds no
   unnecessary approval round or execution authority.

These are checks of the plan artifact. They do not prove implementation,
execution, or that a future host session will follow the skill.
