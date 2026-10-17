---
name: keyboard-focus-accessibility-audit
description: Audits keyboard operability and focus behavior in websites, applications, and reusable components using source inspection and manual keyboard testing. Use when a user asks for a keyboard accessibility audit, tab-order review, visible-focus review, focus-management check, dialog or overlay keyboard review, custom-widget keyboard check, shortcut assessment, or investigation of pointer-only interactions.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access and, for runtime confirmation, access to a running interface in a keyboard-capable browser.
metadata:
  category: frontend-a11y
  task_type: review
  audience: frontend-developers-accessibility-reviewers-and-qa-teams
  tags:
    - accessibility
    - keyboard
    - focus
    - focus-management
    - wcag
    - dialogs
    - custom-controls
    - manual-testing
  status: draft
  side_effects: none
---

# Keyboard and Focus Accessibility Audit

## Purpose

Audit whether people can reach, understand, operate, and leave interactive web content with a keyboard, and whether focus remains visible and predictable throughout the interaction. Produce evidence-based findings, separate source-confirmed defects from behavior that requires a running interface, and map confirmed findings to applicable WCAG success criteria without claiming complete conformance.

## When to use this skill

Use this skill when:

- A website, web application, component library, design-system primitive, or embedded widget needs a keyboard and focus review.
- A user reports an unreachable control, illogical tab order, lost focus, invisible focus, keyboard trap, broken dialog, unexpected focus movement, or pointer-only action.
- A custom control or composite widget needs its activation and navigation keys checked against its documented interaction pattern.
- A release review needs focused evidence about keyboard operability, focus management, shortcuts, overlays, or disabled behavior.
- Both implementation evidence and realistic manual keyboard evidence need to be reconciled in one audit.

Do not use this skill when:

- The request is for a complete accessibility or WCAG conformance audit.
- The primary task is to review landmarks, headings, lists, tables, document reading order, or other semantic-document structure.
- The primary task is general visual design, typography, color-system, responsive-layout, or art-direction review.
- The user wants an accessibility test plan rather than findings from an existing implementation; use `accessibility-validation-planner`.
- The user wants fixes applied. This skill reports findings and recommendations only.

## Scope boundaries and routing

Keep the main audit limited to keyboard operability and focus behavior.

- Route semantic-document structure findings, including landmark, heading, list, table, reading-order, and general accessible-name issues, to `semantic-structure-accessibility-audit`.
- Route general visual accessibility findings, including contrast outside focus indicators, typography, zoom, reflow, target size, and responsive presentation, to `visual-responsive-accessibility-audit`. Keep focus-indicator visibility, focus appearance, and focus obscuration here because they directly affect keyboard use.
- Route general art-direction concerns that are not accessibility findings to `layout-art-direction`.
- Route live-region, announcement, and screen-reader behavior to the applicable specialist unless the issue is inseparable from a keyboard failure in the same custom control.
- Route content, motion, and pointer-quality issues that do not affect keyboard parity to their corresponding specialists.
- Record routed observations separately. Do not inflate this audit's finding count with out-of-scope issues.

When the skill is invoked by `inclusive-interface-audit-orchestrator`, use the orchestrator's shared finding contract, severity scale, status values, identifiers, and deduplication rules exactly. Do not rename fields or create a parallel schema.

## Inputs to inspect

Start with the smallest set that represents the target interaction:

- Audit scope, critical user tasks, supported platforms, target WCAG version and level, and acceptance criteria.
- HTML, templates, JSX, Vue, Svelte, or other component source that creates interactive elements.
- JavaScript or TypeScript for event handling, focus movement, routing, portals, overlays, shortcuts, and disabled behavior.
- CSS affecting `outline`, `box-shadow`, borders, `:focus`, `:focus-visible`, visibility, clipping, stacking, sticky or fixed content, forced colors, and scrolling.
- Dialog, popover, disclosure, menu, listbox, tabs, tree, grid, toolbar, combobox, carousel, drag-and-drop, and other interaction primitives.
- Component stories, demos, integration examples, keyboard documentation, and design-system usage guidance.
- Unit, component, browser, and accessibility tests that exercise keyboard or focus behavior.
- A running interface with representative data, permissions, responsive states, and error states when available.
- The authoritative WCAG version named by the user and the relevant native HTML or WAI-ARIA Authoring Practices pattern for each custom widget.

Do not infer behavior from a component name or ARIA role alone. Inspect the implementation and, when the claim concerns user-observable behavior, reproduce it in a running interface.

## Shared finding contract

If `inclusive-interface-audit-orchestrator` is available, read its shared finding contract before reviewing the target. Every finding must preserve these exact required fields:

| Field | Required content |
|---|---|
| `id` | Stable unique identifier |
| `target` | Route, component, flow, state, role, environment, and occurrence as applicable |
| `evidence` | Evidence type, method, reference, environment, and reproducible observation |
| `user_impact` | Affected users, blocked or impaired task, consequence, and workaround |
| `status` | `confirmed`, `provisional`, `needs-validation`, `not-reproduced`, `resolved`, or `accepted-risk` |
| `severity` | `critical`, `high`, `medium`, `low`, or `advisory`, based on user and task impact |
| `confidence` | `high`, `medium`, or `low`, with the reason and missing evidence |
| `framework_mappings` | Zero or more valid WCAG criteria or other requested-framework mappings, each with rationale |
| `recommendation` | Outcome-focused remediation guidance, constraints, and responsible surface |
| `verification` | Retest steps, expected result, method, environment, and evidence required to close |

Use `source_skill: keyboard-focus-accessibility-audit` for traceability when the contract allows optional fields. Use `related_ids` and `root_cause` only when supported by evidence. Base severity on user impact, task criticality, breadth, workaround quality, persistence, and harm; never use WCAG level as severity.

Do not assign `resolved` without successful retest evidence. Do not assign `accepted-risk`; that status requires a documented product decision.

## Evidence and confirmation model

### Source-verifiable evidence

Source review can confirm facts such as:

- A click handler is attached to a non-focusable element with no keyboard equivalent.
- A custom control lacks the code needed for its documented activation or navigation keys.
- Positive `tabindex` values impose an authored tab sequence.
- Focus is explicitly moved, restored, removed, or redirected by a specific code path.
- A global printable-character shortcut lacks turn-off, remapping, or focus scoping.
- CSS removes the user-agent focus indicator with no authored replacement in the inspected styles.
- An `aria-disabled` control still executes its action, or a visually disabled custom control remains active in its event handler.
- Pointer events, drag events, hover, long press, or gesture handlers have no discoverable non-pointer action path in the inspected implementation.

Use file paths, symbols, selectors, and line numbers when available. A deterministic source defect may have `status: confirmed` when the source itself proves the failure. Do not use source alone to claim that a full rendered interaction works.

### Runtime and manual-keyboard evidence

A running interface and manual keyboard testing are required to confirm:

- The actual forward and reverse tab sequence in rendered, conditional, responsive, virtualized, or portal-based content.
- Whether all controls and task outcomes are reachable and operable without a pointer.
- Whether the focus indicator is perceptible, clipped, covered, scrolled out of view, or obscured in each relevant state.
- Initial focus, focus containment, nested-overlay behavior, focus restoration, and fallback focus when the invoker no longer exists.
- Whether focus becomes trapped, escapes a modal, moves unexpectedly, disappears after DOM updates, or lands in hidden or inert content.
- Actual behavior of activation keys, arrow keys, `Home`, `End`, `Page Up`, `Page Down`, `Escape`, and application shortcuts.
- Keyboard behavior under validation errors, loading, deletion, route changes, responsive layouts, zoom, forced-colors settings, and delayed updates.
- Whether a pointer-only interaction has a complete keyboard-equivalent path, not merely a keyboard-reachable trigger.

Record browser, operating system, viewport, relevant preference settings, start state, exact keystrokes, expected result, and actual result. Use real key input; programmatic `.focus()`, synthetic events, DOM-order inspection, screenshots, and automated scanners do not replace manual keyboard testing.

### Status rules

- Use `confirmed` when direct source evidence proves the defect or the behavior was reproduced using the method required for that claim.
- Use `provisional` when the available evidence strongly supports a finding but one material layer or state remains unverified. Name the gap.
- Use `needs-validation` when source or limited runtime evidence indicates a credible risk but the user-observable failure has not been reproduced. Put it in the manual-verification queue, not the confirmed-findings section.
- Use `not-reproduced` when an explicit test did not demonstrate a reported issue. Record the exact tested scope and do not treat this as a pass beyond that scope.
- Keep routed observations outside the keyboard finding set unless the orchestrator asks for a normalized handoff record.

Absence of evidence is not evidence of accessible behavior.

## Audit coverage

### Keyboard access and task completion

- Traverse the interface with `Tab` and `Shift+Tab` without using a pointer.
- Complete each critical task using keyboard input alone, including opening, changing, submitting, canceling, retrying, and recovering.
- Check controls revealed by hover, pointer proximity, context menus, drag handles, canvas regions, maps, charts, swipe gestures, and long press.
- Distinguish reaching a control from completing its function.
- Check that keyboard handling does not require precise timing or key-repeat speed.

### Logical tab order

- Compare the rendered focus sequence with the task, reading, and visual sequence.
- Check forward and reverse navigation at state boundaries and after content is inserted, removed, reordered, or collapsed.
- Investigate positive `tabindex`, CSS visual reordering, portals, shadow roots, iframes, virtualization, and focusable off-screen or hidden content.
- For composite widgets, verify the intended single tab stop or documented entry point and the internal navigation model.
- Do not report DOM order or positive `tabindex` as a WCAG failure without demonstrating the resulting meaning or operability problem.

### Visible focus and focus appearance

- Check every focusable state for a visible focus indicator.
- Check indicator continuity across backgrounds, selected or active states, validation states, forced-colors settings, zoom, and responsive layouts when relevant.
- Check that sticky headers, cookie banners, drawers, toasts, overlays, clipping, and scroll containers do not entirely obscure the focused component.
- Measure indicator area and contrast only when the target includes the applicable WCAG level; otherwise report the observed visibility issue without implying an untested measurement.
- Keep general color and visual-system critique outside this audit.

### Focus movement and restoration

- Identify every code path that moves focus and the user need it serves.
- Verify initial focus after opening dialogs, menus, popovers, editing modes, error summaries, and route-level views.
- Check behavior after submit, cancel, close, delete, undo, async completion, validation failure, and DOM replacement.
- Restore focus to the invoking control when it still exists and remains the logical next location.
- When the invoker is removed or disabled, require a documented, predictable fallback aligned with the next task.
- Flag focus changes on mere focus or input when they unexpectedly change context.

### Focus traps, dialogs, and overlays

- Confirm that a modal receives focus on open, contains the intended tab sequence, prevents interaction with the background, offers a keyboard-operable close or cancel action, and restores or redirects focus logically on close.
- Confirm that `Tab` and `Shift+Tab` cycle within an active modal without creating an inescapable trap.
- Confirm that non-modal content does not trap focus.
- Test nested dialogs, stacked popovers, drawers, menus, tooltips, and overlays so `Escape` affects only the current layer unless the documented design says otherwise.
- Check outside-click dismissal for an equivalent keyboard method.
- Do not map every dialog-pattern deviation automatically to WCAG. Demonstrate the resulting keyboard, focus-order, context-change, or programmatic-state failure.

### Custom controls and composite widgets

- Prefer native controls where they supply the required semantics and keyboard behavior.
- For custom buttons and links, verify focusability, `Enter` and `Space` behavior as applicable, event timing, scroll suppression, and protection against double activation.
- For composites such as menus, tabs, radio groups, listboxes, trees, grids, treegrids, toolbars, sliders, spinbuttons, and comboboxes, identify the intended pattern before testing.
- Verify entry and exit with `Tab`, internal arrow-key behavior, orientation, wrapping rules, `Home` and `End` behavior, type-ahead, selection versus focus, and disabled-item navigation as the selected pattern defines.
- Verify roving `tabindex` or `aria-activedescendant` state through initialization, item insertion, deletion, filtering, and rerendering.
- Treat WAI-ARIA Authoring Practices as pattern guidance, not as a WCAG success criterion by itself.

### Keyboard shortcuts and Escape behavior

- Inventory local, page-level, and global shortcuts, including undocumented single-character keys.
- Check conflicts with browser, operating-system, assistive-technology, text-entry, and international keyboard commands.
- For printable-character shortcuts, verify turn-off, remapping with a non-printable modifier, or activation only while the relevant component has focus.
- Verify that shortcuts do not fire while users type in inputs, textareas, editors, or other text-entry contexts unless explicitly intended.
- Check shortcut discoverability and state-dependent availability, routing documentation concerns to the appropriate content specialist.
- Test `Escape` for dialogs, popovers, menus, editing modes, drag modes, and temporary states. Do not assume `Escape` is mandatory for every component; compare with the selected native or ARIA pattern and product contract.

### Activation keys and disabled states

- Verify native and custom activation with the keys expected for the element or pattern.
- Check `keydown` versus `keyup`, repeated keys, default scrolling, event propagation, and duplicate click synthesis.
- Verify that native `disabled`, `aria-disabled`, read-only, unavailable, and pending states have intentional focus and activation behavior.
- Ensure disabled custom controls suppress every activation path, not only pointer clicks.
- Do not assume disabled elements must always be removed from composite-widget navigation; compare with the selected pattern and document the rationale.

### Pointer-only interactions

- Inventory functionality triggered only by click position, hover, drag, swipe, pinch, drawing, double-click, context menu, or long press.
- Require a keyboard path that reaches the same outcome, including ordering, resizing, revealing actions, selecting ranges, and completing or canceling drag operations.
- For path-dependent functionality, distinguish a genuine essential-path exception from an implementation that could expose an endpoint-based alternative.
- Route pointer target-size and general gesture-quality findings elsewhere unless they also block keyboard parity.

## Workflow

1. **Define scope and evidence limits.**
   - List target pages, components, states, critical tasks, supported platforms, and excluded areas.
   - Record whether source, a running interface, or both are available.
   - Use the WCAG version and level supplied by the orchestrator or user. For a standalone audit with no stated target, disclose WCAG 2.2 Levels A and AA as the technical mapping baseline and treat AAA as advisory, not as a conformance target.

2. **Load authoritative expectations.**
   - Read `inclusive-interface-audit-orchestrator` first when it is available and retain its exact finding contract.
   - Identify the native HTML behavior, product contract, or WAI-ARIA Authoring Practices pattern that applies to each custom widget.
   - Treat WCAG as normative for success-criterion mapping and pattern guides as implementation guidance.

3. **Inventory interaction surfaces and states.**
   - Enumerate native controls, custom controls, composites, overlays, shortcuts, pointer gestures, focus-moving code paths, and disabled states.
   - Include default, expanded, collapsed, selected, editing, loading, empty, error, success, permission, and responsive variants that change interaction.
   - Prioritize critical task paths and high-risk primitives.

4. **Inspect source evidence.**
   - Trace focusability, event handlers, default-event cancellation, focus calls, restoration targets, portal or inert behavior, roving focus, shortcut scope, and pointer-only handlers.
   - Inspect focus styling and author-created layers that can obscure focus.
   - Record exact evidence and create manual-verification hypotheses for behavior source cannot prove.

5. **Run the manual keyboard pass.**
   - Reset to a known start state for each scenario.
   - Use the keyboard only and record exact keys, expected behavior, actual behavior, and recovery.
   - Test forward and reverse navigation, critical-task completion, focus visibility, overlays, custom widgets, shortcuts, disabled states, and pointer parity.
   - Repeat stateful or timing-sensitive scenarios enough to distinguish deterministic defects from intermittent behavior.

6. **Reconcile source and runtime evidence.**
   - Link reproduced behavior to the responsible source when possible.
   - Use `needs-validation` for untested source risks.
   - Record environment-specific or intermittent behavior honestly.
   - Deduplicate symptoms that share one cause without hiding distinct user impacts.

7. **Map confirmed findings to standards.**
   - Map only when evidence satisfies the conditions of the criterion.
   - Include criterion number, name, level, target WCAG version, and a one-sentence applicability rationale.
   - Use the smallest applicable set; do not attach every keyboard-related criterion to every finding.
   - Label pattern deviations separately from WCAG mappings.

8. **Route out-of-scope evidence.**
   - Send semantic-document observations to `semantic-structure-accessibility-audit`.
   - Send general visual and responsive accessibility observations to `visual-responsive-accessibility-audit`.
   - Preserve evidence and location so the receiving specialist can evaluate the observation without repeating discovery.

9. **Report coverage and limitations.**
   - List tested and untested tasks, states, components, browsers, settings, and input conditions.
   - Report verified checks as scoped observations, not proof of page-level or product-level conformance.
   - End with prioritized retest steps for confirmed findings and a separate `needs-validation` queue.

## WCAG mapping guardrails

Consider these WCAG 2.2 criteria when the evidence fits:

| Criterion | Level | Apply when confirmed evidence shows |
|---|---:|---|
| 1.4.11 Non-text Contrast | AA | An authored focus or component-state indicator lacks required contrast against adjacent colors. |
| 1.4.13 Content on Hover or Focus | AA | Additional content triggered by hover or focus is not dismissible, hoverable, or persistent as required. |
| 2.1.1 Keyboard | A | Functionality cannot be operated through a keyboard interface, subject to the essential path-dependent exception. |
| 2.1.2 No Keyboard Trap | A | Focus enters content but cannot leave using a keyboard, or a nonstandard exit is required and not explained. |
| 2.1.3 Keyboard (No Exception) | AAA | Functionality is not keyboard operable under a AAA target. Path-dependent functionality that is excepted by 2.1.1 prevents conformance to this criterion rather than creating a required keyboard implementation. |
| 2.1.4 Character Key Shortcuts | A | A printable-character shortcut lacks an allowed turn-off, remap, or focus-only mechanism. |
| 2.4.3 Focus Order | A | Focus order does not preserve meaning and operability. |
| 2.4.7 Focus Visible | AA | A keyboard-operable interface lacks a mode with a visible keyboard focus indicator. |
| 2.4.11 Focus Not Obscured (Minimum) | AA | Author-created content entirely hides the component receiving keyboard focus. |
| 2.4.12 Focus Not Obscured (Enhanced) | AAA | Any part of the focused component is hidden by author-created content under a AAA target. |
| 2.4.13 Focus Appearance | AAA | An authored keyboard focus indicator fails the specified area or focused/unfocused contrast requirement under a AAA target. |
| 2.5.1 Pointer Gestures | A | Multipoint or path-based pointer functionality lacks a qualifying simple single-pointer alternative. Keyboard operability alone does not satisfy this criterion. |
| 2.5.2 Pointer Cancellation | A | A single-pointer action lacks the required cancellation, abort, undo, or essential down-event behavior. Route here only when pointer parity is in scope. |
| 2.5.7 Dragging Movements | AA | Functionality using drag lacks a non-dragging single-pointer alternative; a keyboard alternative alone does not automatically satisfy this criterion. |
| 3.2.1 On Focus | A | Receiving focus initiates an unexpected change of context. |
| 3.2.2 On Input | A | Changing a control setting initiates an unannounced change of context. |
| 4.1.2 Name, Role, Value | A | A custom control's programmatic role, state, value, or change notification is defective and directly intertwined with the audited interaction. Coordinate with `semantic-structure-accessibility-audit`. |

These are candidate mappings, not an automatic checklist. Other criteria may apply when evidence supports them. Pattern guidance such as expected dialog focus restoration or arrow-key behavior can identify a real usability defect without necessarily establishing a WCAG failure.

Never claim:

- Complete WCAG conformance from this specialist audit.
- A criterion passes because no issue was found in untested states.
- An automated scan proves tab order, visible focus, focus restoration, focus containment, shortcut safety, or task completion.
- A code pattern violates WCAG without connecting it to the criterion's user-observable conditions.

## Output format

When orchestrated, return every finding using the exact shared finding contract from `inclusive-interface-audit-orchestrator`.

For standalone use, preserve the same contract with this structure:

```md
## Audit scope and evidence

- Target:
- Critical tasks and states:
- Source inspected:
- Runtime environment:
- WCAG reference:
- Out of scope:
- Untested:

## Confirmed and provisional findings

### KFA-001 — Concise finding title

- id: KFA-001
- target:
- evidence:
  - Type and method:
  - Source reference:
  - Environment and start state:
  - Keystrokes:
  - Expected:
  - Actual:
- user_impact:
- status: confirmed | provisional
- severity: critical | high | medium | low | advisory
- confidence: high | medium | low — reason and missing evidence
- framework_mappings:
  - WCAG 2.2 X.X.X Name (Level): applicability rationale
  - Pattern guidance, if relevant:
- recommendation:
- verification:
  - Retest steps:
  - Expected result:
  - Method and environment:
  - Closure evidence:
- source_skill: keyboard-focus-accessibility-audit
- related_ids:
- root_cause:

## Needs-validation queue

[Use the same finding contract with `status: needs-validation`; include the exact manual steps and evidence required.]

## Not reproduced

[Use the same finding contract with `status: not-reproduced` and bound the result to the tested environment and state.]

## Verified checks

- Scoped observations that were actually tested. Do not label these as complete conformance.

## Specialist handoffs

| Destination skill or capability | Observation | Evidence and target | Why routed |
|---|---|---|---|

## Limitations

- Untested environments, states, data, timing, assistive-technology combinations, or third-party surfaces.
- This keyboard and focus audit does not establish complete accessibility or WCAG conformance.
```

If no confirmed findings exist, say so and still return the `needs-validation` queue, verified checks, specialist handoffs, and limitations. Do not turn unverified risks into findings to avoid an empty report.

## Quality bar

The task is complete only when:

- Scope, critical tasks, environments, evidence sources, and exclusions are explicit.
- Keyboard access, tab order, focus visibility and appearance, focus movement, restoration, traps, dialogs, overlays, custom controls, composite widgets, shortcuts, `Escape`, activation keys, disabled states, and pointer-only interactions are considered where relevant.
- Every confirmed finding cites reproducible runtime evidence or deterministic source evidence appropriate to the claim.
- Runtime-dependent claims are not marked `confirmed` from source inspection alone.
- `needs-validation` records include exact steps, expected behavior, and evidence required.
- Every finding preserves the orchestrator's required contract fields and allowed values.
- WCAG mappings include the criterion, level, version, and evidence-specific rationale.
- Pattern guidance is not misrepresented as a WCAG success criterion.
- Semantic-document and general visual-design findings are routed outside the main audit.
- Verified checks are bounded to the states and environments actually tested.
- The result states that it does not establish complete conformance.
- No product files, remote systems, or external records are changed.

## Edge cases

- **No running interface:** Complete the source pass, report only deterministic source defects as `confirmed`, and use `needs-validation` for rendered behavior.
- **No source access:** Report only behavior reproduced in the running interface and avoid speculating about root causes.
- **Single-page applications:** Test route changes, history navigation, async view replacement, loading boundaries, and fallback focus when the prior element disappears.
- **Portals, shadow DOM, and iframes:** Test focus transitions across boundaries in both directions and identify which context owns restoration.
- **Virtualized content:** Test whether focus survives recycling, filtering, scrolling, and item deletion.
- **Nested overlays:** Test focus containment, `Escape` propagation, restoration, and background inertness one layer at a time.
- **Destructive dialogs:** Verify that initial focus and restoration support the safest logical action; do not impose a universal first-control rule.
- **Mobile or touch-first UI:** Test an external keyboard when keyboard support is in scope; route touch exploration and screen-reader gestures to the relevant specialist.
- **Third-party widgets:** Separate behavior the product can configure from upstream defects and document the integration boundary.
- **International layouts and input methods:** Avoid assuming US-keyboard character positions, and test shortcut conflicts with composition and text entry.
- **Platform-native wrappers:** Use the platform's keyboard conventions and accessibility APIs instead of applying web patterns mechanically.

## Related skills

- `inclusive-interface-audit-orchestrator`
- `semantic-structure-accessibility-audit`
- `visual-responsive-accessibility-audit`
- `accessibility-validation-planner`
- `interface-state-coverage-review`
- `layout-art-direction`
