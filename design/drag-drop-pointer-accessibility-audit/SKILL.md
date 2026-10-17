---
name: drag-drop-pointer-accessibility-audit
description: Audits web interfaces that use drag and drop, swipe, pinch, path-based gestures, hover, small targets, pointer-specific controls, or device motion. Use when a user asks to review pointer accessibility, drag-and-drop accessibility, touch or gesture alternatives, target size, hover-only content, reordering, pointer cancellation, or WCAG 2.2 pointer-input criteria without requesting implementation changes.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository or artifact access; runtime confirmation benefits from a running interface on representative pointer, touch, keyboard, and assistive-technology configurations.
metadata:
  category: frontend-a11y
  task_type: review
  audience: frontend-developers-accessibility-reviewers-and-qa-teams
  tags:
    - accessibility
    - wcag
    - pointer
    - drag-and-drop
    - gestures
    - touch
    - target-size
    - keyboard
    - universal-design
  status: draft
  side_effects: none
---

# Drag, Drop, Gesture, and Pointer Accessibility Audit

## Purpose

Audit whether pointer, touch, gesture, and motion interactions let people discover, operate, cancel, confirm, and recover from a task without unnecessary precision, force, timing, or device-specific capability. Produce evidence-based technical accessibility findings and separately labeled Universal Design concerns. Do not claim complete WCAG conformance.

## When to use this skill

Use this skill when:

- A website, application, component, canvas, map, editor, game-like control, or design-system primitive uses drag and drop, sorting, resizing, drawing, swipe, pinch, long press, path gestures, hover, pointer capture, or device motion.
- A user reports accidental activation, an unreachable drag handle, a small or crowded control, hover-only content, unreliable reordering, unclear drag instructions, lost focus, or absent confirmation after a pointer action.
- A release review needs focused evidence about WCAG 2.2 pointer input criteria, target size, touch interaction, or alternatives to precision-dependent controls.
- An inclusive audit needs to assess low physical effort, flexibility in use, and tolerance for error for a pointer-driven task.

Do not use this skill when:

- The request is a complete accessibility or legal conformance audit.
- The primary question is keyboard navigation or focus management without a pointer, gesture, or motion interaction in scope; use `keyboard-focus-accessibility-audit`.
- The primary question is general contrast, zoom, responsive layout, or visual design outside pointer-target and hover behavior; use `visual-responsive-accessibility-audit`.
- The user asks to implement or remediate the issue rather than review it.

## Scope boundaries and orchestration

Keep the main audit limited to pointer, touch, gesture, motion, hover, target-size, and their complete alternative task paths.

- Route semantics and general accessible-name defects to `semantic-structure-accessibility-audit`, while retaining a `2.5.3 Label in Name` mapping when a pointer control's visible label is not contained in its accessible name.
- Route broader keyboard and focus findings to `keyboard-focus-accessibility-audit`; retain keyboard findings here only when they are required to establish an alternative to the audited pointer task.
- Route general visual presentation and responsive issues to `visual-responsive-accessibility-audit`; retain target-size geometry and hover/focus-content behavior here.
- Route dynamic announcement and state-management defects to `dynamic-interface-accessibility-audit` when they are broader than the pointer task. Keep task-specific reorder, completion, cancellation, and error-recovery feedback in scope.
- Route broader cognitive clarity or recovery concerns to `content-cognitive-accessibility-audit` when they are not specific to the interaction.

When invoked by `inclusive-interface-audit-orchestrator`, use its supplied scope, IDs, severity scale, status values, framework-mapping rules, deduplication decisions, and shared finding contract exactly. Do not create a parallel schema.

When that orchestrator is unavailable, remain independently usable by using the mirrored contract in this skill and `source_skill: drag-drop-pointer-accessibility-audit`.

## Inputs to inspect

Start with the smallest evidence set that represents the interaction and its alternatives:

- Audit scope, critical tasks, supported platforms, input methods, WCAG version and level, and product acceptance criteria.
- Representative routes, components, stories, demos, prototypes, recordings, screenshots, and defect reports.
- HTML, templates, component code, and JavaScript or TypeScript handling pointer, mouse, touch, drag, click, keyboard, motion, and cancellation events.
- CSS affecting target dimensions, spacing, hit areas, hover and focus states, overlays, dragging affordances, `touch-action`, pointer capture, and disabled states.
- Accessible names, visible labels, descriptions, instructions, status messages, live regions, roles, values, and state exposed by custom controls.
- Reorder, resize, drawing, selection, deletion, upload, save, cancellation, undo, and error paths, including loading and interrupted states.
- Tests and test fixtures for pointer, touch, keyboard, accessibility tree, screen reader, and responsive conditions.
- A running interface with representative data and supported devices or emulation when available.

Do not infer runtime behavior from a screenshot or static source alone. Record the missing method as `needs-validation`.

## Evidence and audit rules

- Review task completion, not merely whether an event handler or alternate button exists. An alternative must provide the same essential outcome with comparable information, control, and recovery.
- Use a real or accurately emulated pointer/touch environment for runtime claims. Record browser, operating system, input device, viewport, zoom, touch-assistive settings, and start state when relevant.
- Treat source-only observations as `confirmed` only when the source deterministically establishes the defect. Treat actual target geometry, touch behavior, focus movement, accessibility-tree exposure, and announcements as runtime or assistive-technology checks until tested.
- Test the complete lifecycle: discovery, instruction, initiation, operation, cancellation, success or failure feedback, focus outcome, and recovery.
- Do not treat keyboard access as a substitute for a required simple single-pointer alternative under WCAG 2.5.1 or 2.5.7. Keyboard access remains an important independent requirement and Universal Design alternative.
- Do not treat a native control, an exception, or an essential interaction as a failure without checking the criterion's conditions. Record the exact rationale and evidence.
- Map WCAG only when the observed behavior and evidence support that criterion. Keep APG guidance, browser defects, product quality, and Universal Design observations separate from conformance findings.
- Do not change product files, execute destructive test actions, submit production data, or mutate external systems.

## Audit coverage

For every in-scope interaction, record its task, trigger, required precision or path, feedback, committed outcome, alternative paths, cancellation path, and recovery path.

| Area | Inspect for |
|---|---|
| Gesture alternatives | A simple single-pointer alternative for multipoint or path-based gestures; usable choices for swipe, pinch, rotation, tracing, drawing, and multi-finger actions |
| Dragging and reordering | A non-dragging single-pointer path, a complete keyboard path, discoverable drag/reorder instructions, boundary behavior, and movement confirmation |
| Pointer cancellation | Up-event activation or an available abort, undo, or reversal; no irreversible or costly action merely from pointer down unless essential |
| Targets and spacing | Measured CSS-pixel target size, gaps and overlap, hit-area alignment, nearby destructive controls, device scaling, magnification, and applicable exceptions |
| Labels and instructions | Visible action words contained in accessible names; label, handle, source, destination, constraints, and outcome instructions available at the point of use |
| Hover and proximity | Information, controls, and previews available without hover where needed; hover/focus content is dismissible, hoverable, persistent, and keyboard reachable when WCAG 1.4.13 applies |
| Device motion | An alternate control method, an accidental-activation disablement mechanism, clear state and calibration feedback, and recovery from unavailable sensor access |
| Focus and state | Logical focus before, during, after, and on cancellation of a pointer operation; state, selection, position, success, failure, and undo status exposed in more than color or movement |
| Error recovery | Invalid drop destinations, rejected reorders, interrupted drags, failed saves, collisions, duplicate actions, lost connection, and uncertain completion leave users with an understandable next step |
| Universal Design | Flexibility across inputs; low precision, force, reach, repetition, and sustained action; tolerance for error; and adequate space for touch, stylus, tremor, magnification, and one-handed use |

## Workflow

1. **Define scope and evidence.**
   - Record target IDs, critical tasks, consequential actions, supported browsers and devices, requested WCAG baseline, available artifacts, and exclusions.
   - Mark each source, screenshot, prototype, automated result, runtime observation, and assistive-technology test with its limits.
   - Preserve any orchestrator-provided identifiers, evidence references, and exclusions.

2. **Inventory pointer-dependent behaviors.**
   - List every action activated by pointer down, click, hover, drag, long press, swipe, pinch, rotation, trace, drawing, canvas coordinate, pressure, tilt, device orientation, shake, or other motion.
   - Include visible and hidden controls: drag handles, hover toolbars, context actions, resize grips, maps, sliders, sortable lists, uploads, carousels, gesture navigation, and native-wrapper controls.
   - Note whether the behavior is optional enhancement, required functionality, or a high-consequence action.

3. **Map each task through recovery.**
   - For each critical interaction, record entry, instruction, initiation, required movement or precision, valid and invalid destinations, success, cancellation, error, undo, and return paths.
   - Identify what changes while the user is holding, dragging, or moving: focus, selection, visual state, accessible state, data order, and persistence.
   - Test or request the behavior after interruption, viewport change, scroll, device rotation, pointer loss, slow network, save failure, and rerendering when relevant.

4. **Test single-pointer alternatives.**
   - For each multipoint or path-based gesture, verify a simple single-pointer alternative completes the same function without requiring a specific path or simultaneous contacts.
   - For each dragging operation, verify a non-dragging single-pointer method such as select then choose destination, move up/down controls, menu action, or explicit destination control.
   - Judge alternatives by outcome, availability, clarity, and recoverability. Do not require an identical gesture or visual effect.
   - Evaluate essential exceptions narrowly and document why no non-gesture or non-drag alternative can achieve the function.

5. **Test complete keyboard alternatives.**
   - Complete each task with keyboard alone, including choosing an item, selecting a destination or increment, committing, cancelling, receiving feedback, and continuing from the resulting state.
   - Check focus order, visible focus, instructions, activation keys, movement commands, `Escape` or another documented cancellation mechanism, and focus restoration after cancel, reorder, delete, or failure.
   - Verify that keyboard operation does not depend on a pointer-created hover state or on knowing screen coordinates.

6. **Test cancellation and down-event behavior.**
   - Trigger each single-pointer action then move away, release elsewhere, cancel, or undo as the interface permits.
   - Confirm that an action occurs on the up event, can be aborted or reversed, or is essential when it occurs on down. Treat accidental activation and high-consequence actions with proportionate rigor.
   - Check pointer capture, scrolling, context loss, delayed response, repeated input, and component unmounting for stranded or duplicated actions.

7. **Measure targets, spacing, and physical effort.**
   - Measure the authored target's CSS-pixel bounding box, effective hit area, overlap, and spacing at relevant breakpoints and zoom levels. Record the method and state.
   - Check WCAG 2.5.8's 24 by 24 CSS-pixel minimum and its exceptions before reporting a failure. Consider WCAG 2.5.5's 44 by 44 CSS-pixel enhanced target only for an AAA target or as an advisory goal.
   - Test dense controls, adjacent destructive actions, small drag handles, resize grips, hover-only controls, and moving targets with touch, stylus, magnification, tremor, and one-handed use in mind.
   - Report unnecessary precision, sustained hold, repeated repositioning, reach, force, and fatigue as Universal Design or usability concerns unless the evidence supports a WCAG criterion.

8. **Audit labels, instructions, and hover access.**
   - Compare visible labels with computed accessible names, especially voice-control-relevant action words such as “Move,” “Delete,” “Drag,” “Resize,” and “Save.”
   - Make source item, destination, constraints, keyboard commands, cancellation, and confirmation discoverable before and during the interaction. Do not rely only on a cursor shape, animation, color, spatial position, or learned gesture.
   - Test hover-revealed information and controls by keyboard focus and touch. When additional content is triggered by hover or focus, test dismissal, pointer movement into the content, persistence, and availability long enough to use.

9. **Audit motion, feedback, and recovery.**
   - For device-motion input, verify an alternative input method and a way to disable accidental motion activation. Test denied permission, unavailable sensors, calibration failure, and unexpected motion.
   - Verify current position, selected item, valid destination, reorder result, rejected action, save state, and undo availability through more than animation, color, or position alone.
   - Test concise screen-reader status communication when focus does not adequately convey reorder or completion state. Avoid duplicate announcements from simultaneous focus movement and live-region output.
   - Test invalid drop, blocked movement, server rejection, timeout, cancellation, undo, retry, and uncertain persistence. Ensure progress and a usable focus target survive when feasible.

10. **Assess Universal Design without inflating WCAG claims.**
    - Evaluate Equitable use, Flexibility in use, Tolerance for error, Low physical effort, and Size and space for approach and use where relevant.
    - State the concrete burden: added time, precision, force, reach, fatigue, accidental activation, reduced independence, or loss of recovery.
    - Record a Universal Design finding or advisory separately when the concern is supported but does not meet a WCAG success criterion's conditions.

11. **Classify, map, and deduplicate.**
    - Separate confirmed findings, provisional findings, needs-validation items, not-reproduced reports, scoped passes, and coverage gaps.
    - Merge occurrences sharing one target behavior, root cause, user impact, recommendation, and verification method; preserve all affected controls and valid mappings.
    - Assign severity from user impact, task criticality, breadth, workaround quality, persistence, and harm, not WCAG level.

## WCAG 2.2 applicability guide

Use this as a mapping aid, not as an automatic failure checklist.

| Criterion | Level | Apply when confirmed evidence shows |
|---|---:|---|
| 1.4.13 Content on Hover or Focus | AA | Additional author-controlled content triggered by hover or focus cannot be dismissed, hovered, or kept persistent as required. |
| 2.1.1 Keyboard | A | Required functionality, including an alternative path, cannot be completed through a keyboard interface and no applicable exception applies. |
| 2.4.3 Focus Order | A | Focus movement after a pointer task, cancellation, reorder, or state update prevents meaning or operation. |
| 2.4.7 Focus Visible | AA | A keyboard-operable alternative lacks a visible focus indicator. |
| 2.4.11 Focus Not Obscured (Minimum) | AA | Author-created content fully hides the focused component in the alternative path. |
| 2.5.1 Pointer Gestures | A | Multipoint or path-based pointer functionality lacks a simple single-pointer alternative and is not essential. Keyboard access alone does not satisfy this criterion. |
| 2.5.2 Pointer Cancellation | A | A single-pointer action lacks up-event activation, abort, reversal or undo, or an essential down-event rationale. |
| 2.5.3 Label in Name | A | A visible text label for a pointer-operable control is not contained in its accessible name. |
| 2.5.4 Motion Actuation | A | Device-motion functionality has no alternative user-interface method, or accidental motion activation cannot be disabled when the criterion applies. |
| 2.5.5 Target Size (Enhanced) | AAA | Pointer targets fail the 44 by 44 CSS-pixel enhanced size under an explicitly scoped AAA review and no exception applies. |
| 2.5.7 Dragging Movements | AA | Functionality requiring dragging lacks a non-dragging single-pointer alternative and is not essential. Keyboard access alone does not satisfy this criterion. |
| 2.5.8 Target Size (Minimum) | AA | A pointer target is smaller than 24 by 24 CSS pixels and no spacing, equivalent-control, inline, user-agent, or essential exception applies. |
| 3.3.2 Labels or Instructions | A | Necessary instructions for a pointer-dependent input, destination, constraint, or correction are absent. |
| 4.1.2 Name, Role, Value | A | A custom pointer control's role, name, value, or exposed state prevents operation or understanding. |
| 4.1.3 Status Messages | AA | A completed reorder, movement, saved state, or error requires programmatic status communication and it is absent or ineffective. |

Do not map a small target, confusing gesture, hover-only convenience, missing reorder animation, or extra physical effort to WCAG automatically. Map only the supported criterion and list remaining concerns as Universal Design, usability, or a validation requirement.

## Shared finding contract

When orchestrated, return every finding in the exact contract supplied by `inclusive-interface-audit-orchestrator`.

For standalone use, every issue finding must contain:

| Field | Requirement |
|---|---|
| `id` | Stable unique identifier, such as `DDP-001` |
| `target` | Route, component, task, state, control, input mode, environment, and occurrence as applicable |
| `evidence` | Evidence type, method, reference, environment, and reproducible observation |
| `user_impact` | Affected users or contexts, impaired task, consequence, and available workaround |
| `status` | `confirmed`, `provisional`, `needs-validation`, `not-reproduced`, `resolved`, or `accepted-risk` |
| `severity` | `critical`, `high`, `medium`, `low`, or `advisory`, based on impact rather than WCAG level |
| `confidence` | `high`, `medium`, or `low`, including reason and missing evidence |
| `framework_mappings` | Zero or more justified WCAG, Universal Design, or other requested-framework mappings, each with rationale |
| `recommendation` | Outcome-focused remediation guidance, constraints, and responsible surface |
| `verification` | Retest steps, expected result, method, environment, and closure evidence |

Optional traceability fields are `source_skill`, `related_ids`, and `root_cause`. Use `source_skill: drag-drop-pointer-accessibility-audit`.

Treat `accepted-risk` only as a documented product decision. An auditor must not assign it unilaterally.

## Output format

When orchestrated, return the orchestrator's exact output structure. For standalone use, return:

```md
## Pointer interaction audit

### Scope and evidence

- Target and critical tasks:
- Pointer, touch, gesture, motion, and keyboard paths reviewed:
- WCAG baseline and assumptions:
- Evidence and environments:
- Out of scope and untested:

### Coverage ledger

| Target and task | Interaction and alternatives | States tested | Evidence | Result | Remaining validation |
|---|---|---|---|---|---|

### Confirmed and provisional findings

#### DDP-001 — Concise finding title

- id: DDP-001
- target:
- evidence:
- user_impact:
- status:
- severity:
- confidence:
- framework_mappings:
  - WCAG 2.2 X.X.X Name (Level): applicability rationale
  - Universal Design — <principle>: related burden and rationale
- recommendation:
- verification:
- source_skill: drag-drop-pointer-accessibility-audit
- related_ids: optional
- root_cause: optional

### Needs validation

[Use the same finding contract. Include exact device, input method, task, expected behavior, and evidence required.]

### Scoped passes

| Check | Target, state, and environment | Method | Result boundary |
|---|---|---|---|

### Specialist handoffs

| Destination skill or capability | Observation | Evidence and target | Why routed |
|---|---|---|---|

### Coverage gaps and limitations

- ...

### Recommended remediation order

1. ...
```

If no failure is confirmed, say so for the reviewed sample. Do not describe that result as whole-product accessibility, WCAG conformance, certification, or legal compliance.

## Quality bar

The task is complete only when:

- Each in-scope pointer, hover, gesture, drag, motion, and precision-dependent interaction is inventoried or explicitly excluded.
- Single-pointer alternatives, keyboard alternatives, cancellation, target size and spacing, label-in-name relationships, hover access, motion alternatives, instructions, reorder announcements, focus behavior, state confirmation, and error recovery are tested or assigned an evidence-specific validation step.
- Dragging and path or multipoint gesture alternatives are judged against their distinct WCAG requirements; keyboard access is not misrepresented as satisfying the required single-pointer alternative.
- Target geometry, state, breakpoint, zoom, test method, and any claimed exception are recorded for target-size findings.
- Findings distinguish confirmed WCAG mappings, pattern guidance, Universal Design concerns, and unverified risks.
- Every finding follows the shared contract and includes actionable remediation and reproducible verification.
- Scoped passes and not-reproduced reports remain bounded to the tested target, state, device, input method, and environment.
- The result makes no whole-product conformance or legal-compliance claim, and no product or external system is changed.

## Edge cases

- **Essential interaction:** Do not assume a drawing, path, game, signature, map, or pressure-sensitive task is essential. Document the functional reason and evaluate every non-essential surrounding action separately.
- **Native drag and drop:** Test the actual product interaction; browser-native behavior or the presence of draggable markup does not establish accessible alternatives, instructions, or status feedback.
- **Touch screen without hover:** Ensure critical information and controls exposed on hover have a non-hover access path. Do not assume a long press is an equivalent unless it is discoverable and usable.
- **Canvas, maps, and custom editors:** Inspect coordinate-dependent actions, keyboard and simple-pointer alternatives, announced positions and outcomes, zoom, panning, hit testing, and error recovery rather than relying on DOM semantics alone.
- **Virtualized or auto-sorted lists:** Test reorder confirmation, persistence, focus, announcements, and undo across scrolling, filtering, refresh, save failure, and rerendering.
- **Third-party component:** Report the user-facing barrier and configuration or ownership boundary separately; do not discard the finding because a vendor owns the base control.
- **Screenshot-only review:** Report visible target density, labels, instructions, and hover affordances only. Mark target measurement, event timing, alternatives, focus, announcements, and recovery as `needs-validation` unless evidence establishes them.
- **Source-only review:** Confirm deterministic code defects, but require runtime validation for rendered hit areas, gesture recognition, browser cancellation behavior, computed names, focus, and spoken feedback.
- **Voice control:** A visible label that is absent from the accessible name can block voice-command matching; test representative commands when an appropriate environment is available.
- **Reduced dexterity or situational use:** Treat precision, force, fatigue, occupied hands, tremor, injury, magnification, and one-handed use as context for Universal Design assessment, not assumptions about any individual user.

## Related skills

- `inclusive-interface-audit-orchestrator`
- `keyboard-focus-accessibility-audit`
- `visual-responsive-accessibility-audit`
- `dynamic-interface-accessibility-audit`
- `semantic-structure-accessibility-audit`
- `universal-design-interface-review`
