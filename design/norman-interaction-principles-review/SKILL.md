---
name: norman-interaction-principles-review
description: Reviews actual interfaces, components, states, and task flows using Don Norman's interaction-design principles. Use when the user asks to find discoverability, affordance, signifier, mapping, feedback, constraint, conceptual-model, execution-gap, evaluation-gap, error-prevention, or recovery problems that make possible actions, results, next steps, or system behavior unclear.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access and interface evidence such as screenshots, prototypes, recordings, or a live interface unless stated otherwise.
metadata:
  category: ui-ux-polish
  task_type: review
  audience: product-designers-frontend-developers-and-ux-researchers
  tags:
    - interaction-design
    - usability
    - norman-principles
    - discoverability
    - feedback
    - conceptual-models
    - error-recovery
  status: draft
  side_effects: none
---

# Norman Interaction Principles Review

## Purpose

Review real interface behavior through Don Norman's interaction-design principles and identify where users may misunderstand what they can do, how to do it, what happened, what will happen next, or how to recover.

Base the review on actual components, states, transitions, and task flows. Do not return a generic explanation of the principles or count the same user problem once per framework or principle.

## When to use this skill

Use this skill when:

- The user asks for a Norman-principles, interaction-design, or usability review.
- Users may not notice an available action or understand how to operate a control.
- Controls, gestures, labels, layouts, or outcomes do not appear to correspond clearly.
- A system response is delayed, ambiguous, silent, transient, or difficult to interpret.
- Users form an inaccurate model of system state, scope, causality, persistence, or next steps.
- A task has preventable mistakes, dead ends, destructive actions, uncertain outcomes, or weak recovery paths.
- A component or flow needs review across default, active, loading, success, error, disabled, empty, and recovery states.
- Another audit has found a usability problem that needs a Norman-principle interpretation without duplicating the root finding.

Do not use this skill when:

- The user wants only a general lesson or summary of Norman's work.
- No interface, flow, component, implementation, or representative evidence is available to inspect.
- The request is solely a WCAG conformance audit, visual-style critique, user-research plan, or implementation task.
- A claimed problem cannot be tied to an affected user task or observable interface evidence.

## Inputs to inspect

Inspect the smallest useful evidence set for the requested task:

- The interface, prototype, screenshots, recordings, or supplied live environment.
- The primary task, user goal, entry point, completion condition, and recovery path.
- Relevant screens, dialogs, menus, forms, notifications, navigation, and controls.
- Default, hover, focus, active, selected, expanded, disabled, loading, empty, error, success, partial-success, offline, permission, and undo states when applicable.
- Transitions before, during, and after important actions.
- Relevant page, route, component, state-management, validation, and error-handling source.
- Product requirements, acceptance criteria, design specifications, tests, support reports, or research evidence supplied with the task.
- Existing findings from other review frameworks when the review is part of a coordinated audit.

Do not infer dynamic behavior from one static screenshot. Mark behavior as not verified when the available evidence cannot show it.

## Finding contract and framework boundary

Read `inclusive-interface-audit-orchestrator` before reviewing when it is available, and use its current shared finding contract, severity model, terminology, and deduplication rules.

If the orchestrator is unavailable, disclose that limitation and use this minimum root-finding contract:

- `id`: stable unique identifier; preserve an existing root ID when enriching a prior finding
- `target`: route, component, flow, state, role, environment, and occurrence as applicable
- `evidence`: evidence type, method, reference, environment, and reproducible observation
- `user_impact`: affected users, affected task, consequence, and workaround
- `status`: `confirmed`, `provisional`, `needs-validation`, `not-reproduced`, `resolved`, or `accepted-risk`
- `severity`: `critical`, `high`, `medium`, `low`, or `advisory`, based on user and task impact
- `confidence`: `high`, `medium`, or `low`, with the reason and missing evidence
- `framework_mappings`: Norman concepts and any valid cross-framework relationships, each with rationale and provenance when inherited
- `recommendation`: outcome-focused remediation guidance, constraints, and responsible surface
- `verification`: retest steps, expected result, method, environment, and evidence required to close

Use `source_skill`, `related_ids`, and `root_cause` as optional traceability fields. Set `source_skill` to `norman-interaction-principles-review` for findings originating in this review.

Treat Norman-principle observations as interaction-design findings, not WCAG failures. A relationship to accessibility, a heuristic, or another review framework is a mapping on the same root finding. Do not create another issue or increase the issue count for that relationship.

Preserve a WCAG mapping only when a dedicated accessibility review has supplied adequate criterion-level evidence. Otherwise leave the WCAG mapping empty and record the possible relationship as a coverage gap that requires dedicated validation. Do not use WCAG conformance level as severity.

## Review model

Use the principles as diagnostic lenses, not as independent checklist quotas. Report only evidence-backed breakdowns that affect an actual task.

### Discoverability

Determine whether users can find the actions and states they need at the moment they need them. Inspect initial visibility, progressive disclosure, menus, gestures, mode changes, permissions, and whether hidden actions have learnable paths.

Do not equate permanent visibility with good discoverability. A disclosed action can remain discoverable when its trigger, location, and current availability are clear.

### Affordances

Determine whether the interface's actual and perceived action possibilities agree. Check whether users can tell what can be pressed, dragged, edited, selected, expanded, scrolled, dismissed, or manipulated.

Distinguish the underlying affordance from the signifier that communicates it. A visual cue can imply an action the system does not support, and a valid action can exist without a sufficient cue.

### Signifiers

Inspect labels, shapes, positions, icons, text, cursor changes, focus treatment, motion, grouping, and other cues that communicate where and how to act. Check whether the cue remains meaningful across input methods, states, viewports, and unfamiliar contexts.

### Mappings

Determine whether the relationship between a control, the user's action, and the resulting effect is understandable. Inspect spatial arrangement, order, direction, grouping, timing, control-to-target correspondence, and whether results appear near the action that caused them.

### Feedback

Determine whether the system communicates receipt, progress, success, failure, scope, and current state promptly and proportionately. Check whether feedback is attributable to the initiating action, persists long enough to interpret, and distinguishes pending work from completed work.

### Constraints

Determine whether physical, logical, semantic, or conventional constraints prevent invalid actions and guide valid ones. Check whether constraints explain unavailable choices, avoid premature dead ends, and do not hide actions users need to understand.

### Conceptual models

Infer the model the interface teaches about objects, relationships, permissions, modes, persistence, causality, and system boundaries. Compare that model with actual behavior across the task. Flag contradictions that make users predict the wrong outcome.

Do not assume the implementation's data model is the user's conceptual model.

### Gaps of execution and evaluation

Trace the action cycle:

1. Form a goal.
2. Form an intention.
3. Specify an action.
4. Execute the action.
5. Perceive the system state.
6. Interpret the state.
7. Compare the outcome with the goal.

An execution gap exists when the interface makes it difficult to translate a goal into an available, understandable action. An evaluation gap exists when the interface makes it difficult to perceive, interpret, or judge the result.

Locate the exact step where the gap occurs. Do not label the entire flow with a gap when one transition supplies the evidence.

### Error prevention, recovery, and understandable behavior

Review whether the interface:

- Prevents likely slips and mistaken interpretations without obstructing routine work.
- Uses appropriate defaults, previews, input boundaries, confirmations, and constraints.
- Makes destructive, irreversible, costly, or broad-scope actions clear before commitment.
- Preserves work and context after validation errors, interruptions, or failed requests.
- Supports cancel, back, retry, edit, undo, restore, or escalation when appropriate.
- Distinguishes partial success, delayed completion, stale data, conflicts, and unknown outcomes.
- Explains what happened, what remains unchanged, what the user can do next, and whether recovery is possible.
- Keeps feedback and recovery close to the affected object or action.
- Avoids exposing raw implementation details as the only explanation.

Prefer reversible actions and clear outcome visibility over unnecessary confirmation dialogs.

## Workflow

### 1. Establish scope and contract

Record:

- The interface, component, or flow under review.
- The target user and affected task.
- The entry point and observable completion condition.
- The included states, devices, input methods, and viewport conditions.
- The evidence sources and important limitations.
- Whether the shared contract came from `inclusive-interface-audit-orchestrator` or the embedded fallback.

Do not broaden a focused request into a product-wide review without evidence or authorization.

### 2. Reconstruct the task flow

Trace the primary path and relevant alternate, failure, and recovery paths.

For each meaningful step, record:

- The user's immediate goal.
- What the interface suggests is possible.
- The action the user is expected to choose.
- The user's likely prediction.
- The system response.
- How the user can tell whether the goal was achieved.
- The next action or recovery option.

Include transitions and state changes, not only static screens.

### 3. Gather direct evidence

Exercise or inspect the relevant states and actions when the supplied environment permits read-only review. Prefer evidence in this order:

1. Directly observed interface behavior.
2. Behavior supported by source and tests.
3. Documented intended behavior.
4. Reasonable inference from incomplete artifacts.

For each observation, capture:

- Artifact locator, route, component, or screen.
- Starting state and conditions.
- User action or event.
- Expected or signified behavior.
- Observed behavior.
- Resulting state.

Label inferences and unverified behavior explicitly. Do not invent user confusion, frequency, or impact that the evidence does not support.

### 4. Diagnose the breakdown

For each task step, ask:

- Can the user discover a relevant action?
- Does the interface suggest the correct possibilities?
- Do signifiers explain where and how to act?
- Does the control map clearly to its target and result?
- Does feedback make state and causality understandable?
- Do constraints guide action and prevent likely mistakes?
- Does behavior reinforce a coherent conceptual model?
- Can the user bridge execution and evaluation?
- Can the user avoid, recognize, and recover from errors?

Select the principle that best explains the root breakdown as primary. Record other principles only when they add diagnostic value.

### 5. Consolidate root findings

Group observations into one root finding when they share:

- The same underlying interaction breakdown.
- The same affected task or outcome.
- The same user consequence.
- The same practical remedy.

Split findings when the consequences or remedies are independently actionable, even if they involve the same control.

Count stable root finding IDs only. Do not count:

- Each affected screen as a new issue when one component causes the problem.
- Each Norman principle as a separate issue.
- Each persona or input method as a separate issue when the same root cause applies.
- Each cross-framework relationship as a separate issue.

### 6. Set status, severity, and confidence

Set status from the evidence state:

- `confirmed`: Reproduced with evidence sufficient for the claim.
- `provisional`: Supported by credible but incomplete evidence.
- `needs-validation`: Plausible, but the required method, state, or environment has not been tested.
- `not-reproduced`: Specifically tested under recorded conditions without reproducing the reported behavior.
- `resolved`: Retested successfully against the verification method after remediation.
- `accepted-risk`: Use only for a documented product decision, never as the reviewer's unilateral conclusion.

Set severity from affected users, task criticality, breadth, workaround quality, persistence, and potential harm:

- `critical`: Creates immediate severe harm, loss, or inability to complete a safety- or mission-critical task with no reasonable workaround.
- `high`: Blocks or corrupts a critical task, creates material risk of data loss or unintended commitment, or leaves a consequential outcome unknowable.
- `medium`: Causes likely mistakes, repeated uncertainty, substantial recovery effort, or failure in an important but recoverable task.
- `low`: Creates localized hesitation, inconsistency, or learning cost with limited task impairment.
- `advisory`: Identifies an evidence-backed improvement without current evidence of task impairment.

Set confidence to `high`, `medium`, or `low` and explain why. Name missing states, methods, or environments. Do not increase severity or confidence because several frameworks map to the same finding.

### 7. Recommend the smallest coherent correction

Tie every recommendation to the root cause and affected task. State:

- What cue, control, relationship, state, or recovery behavior should change.
- Where and when the change should appear.
- What users should be able to predict or understand afterward.
- Which existing convention or component should be preserved when appropriate.
- Any trade-off introduced by added visibility, feedback, or constraint.

Avoid vague recommendations such as `make it intuitive`, `improve affordance`, or `add feedback`.

### 8. Define a reproducible verification method

Specify:

- Starting conditions.
- User goal.
- Action sequence.
- Relevant state, input method, or viewport.
- Expected visible or perceivable response.
- Evidence that shows the user can proceed, evaluate the outcome, or recover.

Use an observed interaction check for behavior changes. For conceptual-model changes, include a task-based usability check in which participants predict the result before acting and explain the result afterward.

### 9. Map related frameworks without duplication

Add a cross-framework mapping only when the same evidence and consequence genuinely relate to another framework.

For each mapping, record:

- Framework and criterion, heuristic, or principle.
- The relationship to the root finding.
- Rationale and provenance when the mapping came from another specialist.

Keep the original root ID. Preserve valid existing mappings. Put unsupported or suspected relationships in coverage gaps rather than the validated mapping list. Do not create a second title, severity, recommendation, or issue count.

### 10. Report coverage and uncertainty

State:

- Tasks and states reviewed.
- Tasks and states not reviewed.
- Directly observed versus source-inferred behavior.
- Evidence conflicts.
- Unverified risks that need additional artifacts or testing.

Do not turn missing evidence into a confirmed finding.

## Output format

Return:

```md
## Review scope

**Interface:** ...
**Target user:** ...
**Affected task:** ...
**Evidence inspected:** ...
**States and paths reviewed:** ...
**Contract source:** inclusive-interface-audit-orchestrator | embedded fallback
**Limitations:** ...

## Task-flow assessment

| Step | User goal | Available action and signifiers | Expected model or outcome | Observed response | Gap |
|---|---|---|---|---|---|

## Root findings

### NIP-001 — Concise root problem

- **`id`:** NIP-001
- **`target`:** Route, component, flow, state, role, environment, and occurrence.
- **`evidence`:** Evidence type, method, reference, environment, starting state, action, expected or signified behavior, and reproducible observation.
- **`user_impact`:**
  - **Affected users:** ...
  - **Affected task:** Specific user goal and task step.
  - **Consequence:** What users may misunderstand, fail to do, do unintentionally, or be unable to evaluate or recover from.
  - **Workaround:** Available workaround and its cost, or `none`.
- **`status`:** confirmed | provisional | needs-validation | not-reproduced | resolved | accepted-risk
- **`severity`:** critical | high | medium | low | advisory
- **`confidence`:** high | medium | low — reason and missing evidence.
- **`framework_mappings`:**
  - **Norman:** Primary principle — rationale connecting the evidence to the affected task.
  - **Norman:** Supporting principle — rationale, when useful.
  - **Other framework:** Criterion, heuristic, or principle — rationale and provenance, when valid.
- **`recommendation`:** Smallest coherent interaction change, constraints, expected outcome, and responsible surface.
- **`verification`:** Retest setup, action, expected result, method, environment, and evidence required to close.
- **`source_skill`:** norman-interaction-principles-review
- **`root_cause`:** Optional normalized cause.
- **`related_ids`:** Optional related finding IDs.

## Norman principle coverage

| Principle or gap | Tasks and states assessed | Result | Evidence or finding IDs |
|---|---|---|---|

Use `supported-finding`, `no-supported-finding`, `not-verifiable`, or `not-applicable` in the result column. Cover discoverability, affordances, signifiers, mappings, feedback, constraints, conceptual models, execution and evaluation gaps, and error prevention, recovery, and understandable system behavior. This is a task-specific coverage record, not a generic theory checklist or one-issue-per-principle count.

## Cross-framework mapping index

| Root finding | Framework mapping | Rationale | Provenance |
|---|---|---|---|

## Evidence-backed strengths

- Cite effective interaction behavior worth preserving.

## Coverage and next verification

- Reviewed: ...
- Not reviewed: ...
- Additional evidence or testing needed: ...
```

Omit the mapping index when there are no mappings. If no root findings are supported, say so and report the reviewed scope and remaining evidence limitations.

## Quality bar

The task is complete only when:

- The review is tied to real interfaces, states, transitions, and user tasks.
- Every requested Norman principle is assessed against the scoped tasks or marked `not-verifiable` or `not-applicable` with a reason.
- Every finding identifies one root interaction problem with concrete evidence.
- Every finding satisfies the shared `id`, `target`, `evidence`, `user_impact`, `status`, `severity`, `confidence`, `framework_mappings`, `recommendation`, and `verification` contract.
- Every `user_impact` states the affected users, affected task, consequence, and workaround.
- Every `framework_mappings` list identifies the primary Norman principle with rationale and preserves valid supporting or cross-framework relationships.
- Execution and evaluation gaps are located at specific task steps.
- Recommendations make system possibilities, causality, state, outcomes, next steps, or recovery more understandable.
- Related principles and frameworks map to one root finding instead of creating duplicate issue counts.
- Norman-principle observations are not mislabeled as WCAG failures.
- Direct observations, source-supported behavior, and inference are distinguished.
- Missing evidence and unreviewed states are explicit.
- The result remains useful even when the orchestrator is unavailable.

## Edge cases

- **Static evidence only:** Review only visible signifiers, layout, apparent affordances, and documented states. Mark feedback, timing, transitions, and recovery as unverified.
- **Source without a runnable interface:** Report source-supported behavior separately from observed behavior and avoid claims about the rendered experience.
- **Prototype without real data or services:** Review the represented model and intended state changes, but identify unavailable failure and recovery evidence.
- **Hidden expert shortcuts:** Preserve efficient shortcuts while ensuring the primary path remains discoverable or learnable.
- **Intentional constraints:** Do not flag necessary safety, permission, or sequence constraints merely because they add friction; review whether their reason and release condition are understandable.
- **Destructive actions:** Prefer clear scope, preview, reversibility, and outcome feedback. Recommend confirmation only when it meaningfully prevents a consequential mistake.
- **Conflicting cues:** Treat one contradiction between label, appearance, placement, and behavior as one root finding when one correction resolves it.
- **Multiple tasks or personas:** Separate task-flow assessments, then deduplicate shared root causes.
- **Potential accessibility overlap:** Record an evidence gap or preserve a mapping from a dedicated accessibility review; do not make a new WCAG claim.

## Related skills

- `inclusive-interface-audit-orchestrator` — use when available to coordinate the shared finding contract across review frameworks.
- `interface-state-coverage-review`
- `microcopy-polish`
- `user-recovery-flow-planner`
