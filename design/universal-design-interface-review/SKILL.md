---
name: universal-design-interface-review
description: Reviews digital interfaces for exclusion risks using the seven Universal Design principles. Use when the user asks for a Universal Design review, inclusive interface review, cross-ability usability review, exclusion-risk audit, or an evidence-based assessment across input methods, devices, environments, preferences, experience levels, and temporary or situational limitations.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: ui-ux-polish
  task_type: review
  audience: product-designers-ux-researchers-and-frontend-developers
  tags:
    - universal-design
    - inclusive-design
    - interface-review
    - usability
    - exclusion-risks
    - framework-mapping
  status: draft
  side_effects: none
---

# Universal Design Interface Review

## Purpose

Review a digital interface through the seven Universal Design principles and identify evidence-backed exclusion risks in real tasks and contexts.

Treat Universal Design as a design-review framework, not a conformance standard. Keep any relationship to WCAG or another framework in a separate mapping attached to the finding. Never relabel a Universal Design finding as a WCAG failure.

## When to use this skill

Use this skill when:

- The user asks for a Universal Design, inclusive interface, or exclusion-risk review.
- A design, prototype, screenshot set, component, product flow, or implemented interface must work across varied abilities and contexts.
- The team wants to examine alternatives across keyboard, pointer, touch, voice, switch, or assistive-technology use.
- The interface must adapt across devices, viewport sizes, orientations, zoom levels, environments, preferences, or experience levels.
- A usability review needs to include temporary and situational limitations rather than only permanent disability categories.
- `inclusive-interface-audit-orchestrator` requests a Universal Design review using its shared finding contract.

Do not use this skill when:

- The user asks only for a WCAG conformance audit or legal compliance determination.
- The task is limited to visual style, branding, or aesthetic preference.
- The request is to implement fixes rather than review an interface.
- There is no interface, user flow, prototype, screenshot, specification, or implementation evidence to inspect.

## Inputs to inspect

Inspect the smallest useful evidence set:

- The target interface, component, or flow and its primary tasks
- Screenshots, prototypes, recordings, or design specifications
- Relevant templates, components, styles, state logic, and responsive behavior
- Labels, instructions, errors, confirmations, status messages, and help content
- Keyboard, pointer, touch, gesture, voice, switch, and assistive-technology interaction behavior when available
- Loading, empty, validation, permission, interruption, timeout, destructive, and recovery states
- Tests, stories, fixtures, acceptance criteria, issue reports, and supplied research
- Known device, browser, viewport, zoom, language, environmental, or organizational constraints

Do not infer dynamic behavior from a static screenshot. Mark unsupported claims as `not-verifiable` and state the evidence needed.

## Review boundaries

- Review the quality and inclusiveness of task completion, not only whether a control technically exists.
- Describe the exclusion mechanism and task consequence. Do not treat a diagnosis or demographic label as evidence by itself.
- Do not assume one access need, input method, device, or preference represents all users in that category.
- Do not require every interface to support every conceivable mode. Judge alternatives by the task, risk, platform, and available evidence.
- Keep findings at the smallest actionable level. Do not turn one local issue into a claim about the entire product.
- Produce review findings and recommendations only. Do not edit files, run mutating commands, or make remote changes.

## Context coverage

Consider relevant variation across these dimensions:

| Dimension | Examples to test or reason about |
|---|---|
| Abilities and access needs | Vision, hearing, motor or dexterity, speech, cognition, attention, memory, literacy, and combinations of needs |
| Input methods | Keyboard, pointer, touch, stylus, voice, switch, screen reader, magnification, and other assistive technology |
| Devices and layouts | Phone, tablet, laptop, desktop, constrained panel, large display, portrait, landscape, browser zoom, and text enlargement |
| Environments | Glare, low light, noise, quiet spaces, vibration or movement, limited privacy, interruptions, and unreliable connectivity |
| Preferences | Text size, contrast, color, motion, language, content density, notification, modality, and pacing preferences |
| Experience levels | First-time, occasional, returning, expert, low domain familiarity, low technical familiarity, and unfamiliar conventions |
| Temporary or situational limitations | Injury, fatigue, stress, time pressure, occupied hands, muted audio, broken hardware, poor lighting, or low bandwidth |

Use the dimensions to discover plausible exclusion mechanisms, not to generate a finding for every cell. Record which contexts were examined and which remain unknown.

## Universal Design principles

### 1. Equitable use

Check whether people can complete the same core task with comparable dignity, privacy, safety, quality, and independence.

Look for:

- A primary path available only to one input method, sensory channel, device, or ability
- Separate alternatives that are incomplete, delayed, stigmatizing, or lower quality
- Help, safety, privacy, or productivity features unavailable to some users
- Personalization or assistive modes that expose unnecessary personal information

### 2. Flexibility in use

Check whether the interface supports reasonable variation in method, pace, sequence, preference, and expertise.

Look for:

- Drag, hover, gesture, speech, audio, precision, or shortcut-only actions
- Strict timing or one-way flows without pause, back, cancel, save, or resume
- Settings that cannot adapt to user preference or context
- Novice and expert needs forced into one inefficient or confusing path
- Orientation, handedness, or device assumptions that are not necessary to the task

### 3. Simple and intuitive use

Check whether the task is understandable regardless of experience, concentration, language fluency, or domain familiarity.

Look for:

- Unclear purpose, first action, step order, system state, or completion state
- Unexplained jargon, ambiguous labels, hidden dependencies, or unfamiliar conventions
- Excessive memory, inference, reading, or decision burden
- Instructions separated from the control or moment where they are needed
- Inconsistent patterns that make prior learning unreliable

### 4. Perceptible information

Check whether essential content, structure, instructions, state, and feedback can be perceived in relevant sensory and environmental conditions.

Look for:

- Meaning conveyed only by color, sound, position, shape, motion, or transient display
- Important text or controls obscured by contrast, scale, density, truncation, or overlays
- Status, errors, or changes unavailable through assistive technology
- Media or instructions without an effective alternative modality
- Feedback that disappears too quickly or becomes unusable in noise, glare, low light, zoom, or magnification

### 5. Tolerance for error

Check whether the interface prevents avoidable harm and supports recovery from mistakes, interruptions, and uncertain outcomes.

Look for:

- Destructive or high-cost actions that are easy to trigger accidentally
- Validation that arrives too late, loses data, or does not explain recovery
- Missing undo, edit, retry, cancel, restore, or confirmation where consequences warrant it
- Duplicate activation, timeout, interrupted flow, expired session, or stale-state risks
- Error messages that blame users or leave them without a viable next action

### 6. Low physical effort

Check whether the task avoids unnecessary force, precision, repetition, duration, reach, or sustained posture.

Look for:

- Repeated traversal, typing, scrolling, activation, or mode switching
- Small, crowded, distant, moving, or precision-dependent controls
- Long press, hold, drag, multi-touch, or dwell requirements without alternatives
- Controls that are difficult to reach one-handed or with limited dexterity
- Workflows that cannot preserve progress or reduce repeated effort

### 7. Size and space for approach and use

Apply this principle when spatial arrangement meaningfully affects digital use.

Check:

- Target size and spacing across pointer, touch, stylus, tremor, and magnification use
- Reflow at narrow viewports, browser zoom, text enlargement, and different orientations
- Obstruction from virtual keyboards, browser chrome, safe areas, fixed controls, dialogs, captions, or assistive-technology overlays
- Whether controls remain visible, reachable, associated with their content, and operable without precision
- Whether the layout assumes a particular posture, viewing distance, hand position, or screen size without necessity

Mark this principle `not-applicable` when the supplied digital evidence has no meaningful spatial interaction. Explain the reason instead of forcing a finding.

## Workflow

1. Define the review scope.

   Record the target, primary users or contexts, critical tasks, included surfaces, excluded surfaces, available evidence, and evidence limitations.

2. Map task completion.

   For each critical task, identify entry, required information, actions, state changes, success, failure, interruption, and recovery. Prioritize tasks with high consequence or no practical alternative.

3. Build a relevant context sample.

   Select plausible combinations across abilities, input methods, devices, environments, preferences, experience levels, and temporary or situational limitations. Explain why each selected context matters to the task.

4. Trace alternative interaction paths.

   Compare how the same task works across relevant inputs, sensory channels, layouts, pacing needs, and expertise levels. Note differences in outcome quality, independence, privacy, time, error exposure, and recovery.

5. Review all seven principles.

   Assess each principle as `supported-finding`, `no-supported-finding`, `not-verifiable`, or `not-applicable`. Support the result with finding IDs, direct evidence, or an explicit evidence limit.

6. Record exclusion risks.

   Create a finding only when evidence shows or reasonably supports a specific barrier, disadvantage, avoidable burden, or elevated error risk. Separate observed behavior from inference and assign confidence.

7. Map affected users or contexts.

   Name the access need or context and explain the mechanism. Include relevant combinations, such as touch use while zoomed, keyboard use in a dense flow, muted audio during an interruption, or first-time use under time pressure.

8. Describe task impact.

   State the affected task step and consequence: blocked completion, loss of independence, reduced privacy, increased error likelihood, missed information, added time, fatigue, confusion, or reliance on assistance.

9. Recommend the smallest effective response.

   Describe the outcome and behavior the design should provide. Include an equivalent method, clearer communication, reduced effort, safer recovery, or spatial adaptation where relevant. Avoid prescribing implementation details unsupported by the evidence.

10. Keep framework mappings separate.

    Leave `finding_type` as `universal-design`. Add the primary and any secondary Universal Design principles to `framework_mappings`. If evidence also supports a relationship to WCAG or another framework, add a separate mapping entry with its own reference and rationale. Do not call the Universal Design finding a standards failure, violation, or non-conformance.

11. Provide verification guidance.

    Specify retest steps, expected result, method, environment, and evidence needed to close the finding. Include representative manual checks and automated checks only when they can test the stated risk.

12. Check completeness and deduplicate.

    Merge findings with the same target behavior, root cause, and user impact. Preserve all valid principle and framework mappings. Keep distinct findings separate when they require different recommendations or verification.

## Finding contract

Read `inclusive-interface-audit-orchestrator` before reviewing when it is available, and use its current contract, severity model, terminology, and deduplication rules. If it is unavailable, disclose that limitation and use the embedded contract below. Keep the snake-case field names so findings can be normalized and synthesized without translation.

Each finding must include:

- **`id`:** Stable unique identifier such as `UDI-01`
- **`finding_type`:** Always `universal-design`
- **`title`:** Concise description of the exclusion mechanism
- **`target`:** Route, component, flow, state, role, environment, and occurrence as applicable
- **`evidence`:** Evidence type, method, reference, environment, and reproducible observation
- **`user_impact`:** Affected users or contexts, blocked or impaired task, consequence, workaround, and whether independent completion remains possible
- **`status`:** `confirmed`, `provisional`, `needs-validation`, `not-reproduced`, `resolved`, or `accepted-risk`
- **`severity`:** `critical`, `high`, `medium`, `low`, or `advisory`, based on user and task impact
- **`confidence`:** `high`, `medium`, or `low`, with the reason and missing evidence
- **`framework_mappings`:** One primary Universal Design principle, any justified secondary principles, and zero or more separately justified WCAG or other framework references
- **`recommendation`:** Outcome-focused response, constraints, and responsible surface
- **`verification`:** Retest steps, expected result, method, environment, and evidence required to close

Include `source_skill: universal-design-interface-review` for traceability. Add `related_ids` and `root_cause` when they help synthesis.

Use status conservatively:

- `confirmed` — reproduced or directly supported by evidence capable of establishing the behavior
- `provisional` — evidence strongly supports the finding, but an important runtime, environment, or population check remains
- `needs-validation` — the risk is plausible but current evidence cannot establish the behavior
- `not-reproduced` — a defined reproduction attempt did not show the reported behavior
- `resolved` — a prior finding passed the specified retest
- `accepted-risk` — an authorized product decision accepted the documented risk; an auditor must not assign this unilaterally

Severity means:

- `critical` — blocks a critical task, creates serious harm, or removes any practical independent path
- `high` — causes major exclusion or burden in an important task, though a difficult workaround may exist
- `medium` — creates recurring confusion, effort, disadvantage, or error exposure without blocking the task
- `low` — creates limited friction or a localized inclusive-design improvement
- `advisory` — records a supported inclusive-design opportunity without a demonstrated user-impact defect

Base severity on user impact, task criticality, breadth, workaround quality, persistence, and harm. Do not use a WCAG conformance level as severity.

## Framework separation rules

- Keep `finding_type: universal-design` even when the same evidence may relate to WCAG.
- Record each Universal Design principle as its own entry in `framework_mappings`, with one marked `primary` and any others marked `secondary`.
- Add a WCAG reference only when the criterion and evidence have a defensible relationship.
- Describe the mapping as `related`; do not use it to declare conformance or non-conformance.
- Put a possible WCAG relationship that lacks criterion-level evidence in coverage gaps for dedicated validation, not in `framework_mappings`.
- Preserve the provenance of a WCAG mapping inherited from a dedicated accessibility review.
- Do not attach a WCAG mapping merely because a finding affects disabled people.
- Do not convert broad usability concerns into accessibility violations.
- Recommend a dedicated WCAG audit when a standards determination is required.

Use this mapping shape:

```md
framework_mappings:
  - framework: Universal Design
    reference: <principle>
    relationship: primary | secondary
    rationale: <how the principle relates to the evidence and impact>
  - framework: WCAG
    reference: <success criterion or guidance>
    relationship: related
    rationale: <why the evidence may be relevant>
    provenance: <criterion-level evidence or source review>
```

## Output format

Return:

```md
## Universal Design interface review

### Scope and evidence

- Target:
- Critical tasks:
- Contexts considered:
- Evidence inspected:
- Evidence limitations:
- Not reviewed:

### Summary

Briefly state the strongest inclusive qualities, the most consequential exclusion risks, and the recommended next action.

### Principle coverage

| Universal Design principle | Tasks, states, and contexts assessed | Result | Evidence or finding IDs |
|---|---|---|---|
| Equitable use |  |  |  |
| Flexibility in use |  |  |  |
| Simple and intuitive use |  |  |  |
| Perceptible information |  |  |  |
| Tolerance for error |  |  |  |
| Low physical effort |  |  |  |
| Size and space for approach and use |  |  |  |

Use: supported-finding, no-supported-finding, not-verifiable, or not-applicable.

### Findings

#### UDI-01: <title>

- id: UDI-01
- finding_type: universal-design
- source_skill: universal-design-interface-review
- title:
- target:
  - surface:
  - flow, task, or state:
  - role, environment, and occurrence:
- evidence:
  - type:
  - method:
  - reference:
  - environment:
  - reproducible observation:
- user_impact:
  - affected users or contexts:
  - blocked or impaired task:
  - consequence:
  - workaround:
  - independent completion:
- status:
- severity:
- confidence:
  - level:
  - reason:
  - missing evidence:
- framework_mappings:
  - framework: Universal Design
    reference:
    relationship: primary
    rationale:
  - framework: Universal Design
    reference:
    relationship: secondary
    rationale:
  - framework: WCAG
    reference:
    relationship: related
    rationale:
    provenance:
- recommendation:
  - outcome:
  - constraints:
  - responsible surface:
- verification:
  - retest steps:
  - expected result:
  - method and environment:
  - closure evidence:
- root_cause:
- related_ids:

### Evidence-backed strengths

- ...

### Coverage gaps and unknowns

- ...

### Recommended verification

1. ...
```

Remove unused optional mappings and traceability fields rather than leaving empty placeholders. A reported Universal Design finding should normally have at least one Universal Design principle mapping.

If there are no supported findings, say so and retain the evidence limitations and verification guidance. Do not manufacture issues to fill every principle.

## Quality bar

The task is complete only when:

- All seven principles receive a coverage result with evidence, finding IDs, or an explicit `not-verifiable` or `not-applicable` reason.
- Findings are tied to actual tasks and evidence rather than generic checklist advice.
- Relevant variation across all seven context dimensions is considered.
- Affected users or contexts include the exclusion mechanism, not only a group label.
- Each finding follows every required field in the orchestrator contract and includes affected users or contexts, task impact, a focused recommendation, and reproducible verification guidance.
- Universal Design findings retain `finding_type: universal-design`.
- WCAG and other framework relationships are recorded separately and do not become compliance claims.
- Unknown behavior and evidence limits are visible.
- Duplicate symptoms with one underlying cause are consolidated.
- The review remains side-effect free.

## Edge cases

- For screenshots, review visible information and spatial risks; mark interaction, timing, focus, announcement, and recovery behavior `not-verifiable`.
- For prototypes, distinguish designed behavior from implemented behavior.
- For early concepts, report design risks and questions rather than implementation defects.
- For native platform controls, account for reliable platform behavior before recommending custom alternatives.
- For specialized professional tools, preserve efficient expert paths while checking whether necessary learning support and alternatives exist.
- For safety, health, finance, identity, or destructive flows, raise the severity of exclusion that can cause harm, irreversible action, or loss of privacy.
- For conflicting needs, document the tension and recommend user control or an adaptable alternative instead of declaring one universal presentation.
- For responsive interfaces, test meaningful combinations of viewport, zoom, orientation, text size, and virtual-keyboard presence rather than treating mobile and desktop as two fixed layouts.
- If user research or telemetry is supplied, use it as evidence without treating absence of reports as proof that exclusion does not exist.

## Related skills

- `inclusive-interface-audit-orchestrator` — shared orchestration parent when available
- `interface-state-coverage-review`
- `responsive-behavior-planner`
- `accessibility-validation-planner`
- `user-flow-planner`
