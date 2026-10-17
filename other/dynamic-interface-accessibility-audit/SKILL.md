---
name: dynamic-interface-accessibility-audit
description: Audits dynamic web interfaces and changing application states for accessibility, including dialogs, overlays, tabs, menus, disclosures, popovers, live regions, asynchronous feedback, SPA navigation, inserted or removed content, focus management, and exposed names, roles, properties, and states. Use when the user asks for a review of runtime accessibility, screen-reader announcements, loading or error states, client-side transitions, dynamic ARIA behavior, or focus movement and restoration.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository or artifact access; runtime and assistive-technology conclusions require access to a running target and the stated test environment.
metadata:
  category: frontend-a11y
  task_type: review
  audience: frontend-developers-accessibility-specialists-and-qa-teams
  tags:
    - accessibility
    - wcag
    - dynamic-interfaces
    - aria
    - focus-management
    - live-regions
    - screen-reader
    - spa
  status: draft
  side_effects: none
---

# Dynamic Interface Accessibility Audit

## Purpose

Audit how a web interface exposes and manages changing content, state, context, focus, and announcements. Produce evidence-bounded findings that another team can reproduce and verify without modifying the target or claiming complete WCAG conformance.

Use this skill independently or as a specialist invoked by an audit orchestrator. When orchestrated, accept the supplied scope and return findings in the shared contract below. When used alone, establish the same scope, evidence ledger, contract, and limitations without requiring any other skill.

## When to use this skill

Use this skill when:

- A web application, component library, or critical flow contains dialogs, overlays, tabs, menus, disclosures, popovers, toasts, or other changing interface regions.
- The user asks whether loading, success, empty, error, progress, validation, or asynchronous states are accessible.
- A single-page application changes routes, page titles, focus, history, or main content without a full document load.
- Content is inserted, replaced, reordered, virtualized, or removed in response to user action, polling, streaming, or background work.
- The user reports missing, stale, duplicate, delayed, interrupted, or excessively verbose screen-reader announcements.
- Source code and runtime behavior must be distinguished from results observed with named assistive technologies.

Do not use this skill when:

- The request is only for a future accessibility test plan rather than findings from existing evidence.
- The task is limited to static visual contrast, document structure, or copy with no changing interface behavior.
- The user asks for remediation and has not asked for an audit; report findings and recommendations, but do not edit product files.
- The request is for legal advice, certification, or a complete WCAG conformance determination.

## Operating rules

- Keep source inspection, browser runtime testing, and assistive-technology testing distinct.
- Do not infer actual focus, computed accessibility data, timing, or announcements from source code alone.
- Do not infer screen-reader output from a browser accessibility tree or an automated rule.
- Do not mark untested behavior as passing. Record it as a coverage gap or `needs-validation`.
- Test state transitions, not only settled end states.
- Prefer native HTML behavior. Treat WAI-ARIA Authoring Practices as pattern guidance, not as WCAG success criteria.
- Do not require identical spoken wording across assistive technologies. Require equivalent, timely, understandable information and state.
- Do not move focus merely to force an announcement. Evaluate whether the change requires focus, a status message, both, or neither.
- Keep one root problem as one finding when it causes duplicate symptoms across states or frameworks. Record separate occurrences and mappings on that finding.
- Base severity on user and task impact, not on a WCAG conformance level.

## Inputs to inspect

Start with the smallest evidence set that covers the requested flow and its state transitions:

- User request, target URL or build, route or component inventory, critical tasks, supported environments, and stated WCAG 2.2 level if any.
- Components, templates, HTML, event handlers, state management, routing, portals, focus utilities, animation or transition hooks, and DOM insertion or removal code.
- ARIA roles, names, descriptions, relationships, live-region attributes, `aria-busy`, `aria-current`, `aria-expanded`, `aria-selected`, `aria-modal`, and native element states.
- Loading, success, empty, error, offline, timeout, permission, cancellation, retry, optimistic-update, partial-success, and stale-data fixtures.
- Unit, component, end-to-end, keyboard, accessibility, and announcement tests, including ignored rules and known gaps.
- A running target with safe test data, authentication, required roles, feature flags, network controls, and reproducible state triggers.
- Browser developer tools, rendered DOM, computed accessibility tree, focus traces, DOM or live-region mutation logs, recordings, and console output.
- Named browser, operating-system, assistive-technology, version, verbosity setting, and interaction mode for each assistive-technology pass.

Do not read an entire repository when route definitions, component indexes, representative implementations, stories, and tests establish the relevant patterns.

## Evidence model

Classify each observation before making a finding.

| Evidence type | Can support | Cannot establish alone |
|---|---|---|
| Static source | Intended DOM, native elements, declared ARIA, event and focus code paths, state branches, and test coverage | Computed name or role, rendered visibility, actual focus order, timing, browser behavior, or spoken output |
| Automated or static tool | Rules that the tool implements and machine-recorded violations in the scanned state | Complete state coverage, interaction usability, correct focus behavior, announcement quality, or conformance |
| Browser runtime | Rendered DOM, computed accessibility data, actual keyboard and focus behavior, mutation order, and reproducible transitions | What an assistive technology speaks or how a user experiences untested modes and combinations |
| Assistive-technology test | Output and operation observed for the named setup, task, mode, and states | Equivalent results in untested technologies, versions, settings, browsers, platforms, or user strategies |
| Existing report or recording | Prior observations, methods, scope, and regression targets | Current behavior unless the target version and conditions match and the result is reproducible |

Record the target version, route, component, state, action, environment, method, date when relevant, and evidence reference. A source defect may be confirmed as a source defect, but claims about runtime or assistive-technology impact remain provisional until the required evidence exists.

## Workflow

1. **Frame the audit.**
   - Identify the target, critical tasks, components, routes, roles, data conditions, locales, platforms, and dynamic behaviors in scope.
   - Record supplied standards and policies. If no WCAG level is named, use WCAG 2.2 as a mapping reference without assuming a conformance target.
   - State the evidence available, access constraints, exclusions, sampling method, and the fact that the audit does not establish complete conformance.

2. **Build a transition inventory.**
   - List each meaningful trigger and the states before, during, after, and after failure or cancellation.
   - Include loading, success, empty, error, retry, timeout, offline, permission-denied, partial-success, optimistic, stale, and rapid-repeat states when applicable.
   - Record expected visible feedback, DOM change, exposed name/role/state, keyboard behavior, focus destination, restoration target, and announcement for each transition.
   - Include overlapping and interrupted transitions, repeated activation, slow responses, out-of-order responses, route back/forward, and component unmounting.

3. **Inspect static implementation evidence.**
   - Trace triggers, state machines, conditional rendering, portals, routing, live-region containers, and focus calls.
   - Check whether native semantics are available before reviewing custom ARIA.
   - Check that names, roles, values, properties, and states are present on the correct nodes and update from the same source of truth as the visual state.
   - Look for duplicate IDs, stale `aria-*` values, hidden or inert referenced nodes, inaccessible fallback states, unstable keys, node replacement, and timers or effects that can duplicate or suppress updates.
   - Review tests for initial, transition, terminal, failure, cancellation, repetition, and cleanup behavior.
   - Report what source proves and list the runtime or assistive-technology checks still required.

4. **Exercise keyboard and focus transitions at runtime.**
   - Complete each sampled task with keyboard alone.
   - Record focus before the trigger, immediately after activation, during intermediate states, after completion or failure, after dismissal, and after content removal.
   - Check logical focus order, visible focus, focus obscured by overlays or sticky content, and whether the active element remains present, visible, operable, and contextually useful.
   - Verify deliberate initial focus, containment only when the interaction requires it, escape from every state, and restoration to the invoker or another logical target when the invoker no longer exists.
   - Flag focus sent to `body`, removed nodes, hidden content, inactive layers, or arbitrary locations.

5. **Audit dialogs, overlays, and popovers.**
   - Verify the trigger's name and exposed expanded or popup state when applicable.
   - For modal dialogs, test programmatic context, accessible name, initial focus, contained tab sequence, inactive background, close mechanism, nested-dialog behavior, and restoration after every close path.
   - For non-modal dialogs and popovers, test discoverability, dismissal, outside interaction, focus behavior, and the absence of an unintended keyboard trap.
   - Test escape, submit, cancel, click-away, route change, timeout, error, and invoker removal independently.
   - For content shown on hover or focus, check dismissibility, hoverability, persistence, and access without pointer hover.

6. **Audit tabs, menus, disclosures, and composite widgets.**
   - Identify the implemented pattern from semantics and behavior; do not infer a menu merely from its visual appearance.
   - Verify accessible names, roles, relationships, orientation, disabled state, expanded state, selected state, and active panel or item.
   - Test the keyboard model appropriate to that pattern, including entry, internal navigation, activation, dismissal, and exit.
   - Check automatic versus manual tab activation under real loading latency.
   - Check that hidden panels and collapsed content do not remain unexpectedly focusable or exposed, and that reopening preserves or resets state intentionally.
   - Flag visual and programmatic states that diverge after rapid input, rerendering, or asynchronous completion.

7. **Audit feedback and asynchronous states.**
   - Trigger loading, progress, success, empty, error, retry, cancellation, and partial-result states separately.
   - Verify that visible information is also programmatically determinable where required, without making non-urgent updates unnecessarily interruptive.
   - Check loading and busy semantics, control availability, repeated submission, optimistic rollback, error recovery, and the relationship between feedback and the affected control or region.
   - Check whether new results, counts, validation feedback, and background completion are announced at the right time and remain available for review.
   - Verify that error identification and recovery guidance do not rely on color, location, focus movement, or transient speech alone.

8. **Audit SPA route changes and inserted or removed content.**
   - Test direct navigation, in-app navigation, redirects, back/forward, loading, failure, and repeated navigation to the same route.
   - Verify route-specific document titles, current-location semantics, meaningful main-region or heading updates, and intentional focus or announcement behavior.
   - Avoid duplicate orientation from simultaneous title, focus, and live-region strategies unless each conveys distinct necessary information.
   - For inserted content, verify its DOM and reading position, relationships, discoverability, focus policy, and announcement policy.
   - For removed content, verify that focus and referenced relationships move to valid logical targets and that removal or changed results are communicated when needed.
   - Test virtualized, infinite, streaming, reordered, and replaced content for stale accessibility-tree entries and lost position.

9. **Test live regions and status messages with assistive technology.**
   - Use representative supported browser and assistive-technology combinations proportional to risk.
   - Record the trigger, expected message purpose, visible text, relevant DOM mutation, actual spoken result, order, delay, interruption, and repeat behavior.
   - Test one update at a time, then rapid, repeated, overlapping, and out-of-order updates.
   - Detect silent updates, stale messages, duplicated visible and hidden copies, repeated announcements after rerender, queued obsolete results, overuse of assertive interruption, and verbose messages that conceal the actionable part.
   - Check that live-region containers and relevant attributes exist at the time required by the implementation and that updates are not defeated by hidden, replaced, or repeatedly mounted containers.
   - Distinguish a failed announcement from a failed state exposure, focus problem, unsupported combination, timing race, or test-mode mistake.

10. **Verify accessible names, roles, properties, and states.**
    - Compare the visible interface, rendered DOM, computed accessibility data, keyboard behavior, and spoken output.
    - Verify that each interactive element has a concise, distinguishable accessible name and that visible labels are represented in names when required.
    - Verify that roles match behavior and that changing values, states, and relationships remain accurate throughout every sampled transition.
    - Check for stale, contradictory, duplicate, empty, overly long, or context-free names and descriptions.
    - Do not treat syntactically valid ARIA as evidence that the control is operable or understandable.

11. **Create and map findings.**
    - Create a finding only when the evidence shows a defect, a well-supported provisional issue, or a concrete validation need.
    - Use the shared finding contract below.
    - Map only WCAG 2.2 criteria supported by the observed behavior and evidence. Include a short rationale for each mapping.
    - Keep APG deviations, usability concerns, and coverage gaps separate from WCAG failures unless a success criterion independently applies.
    - Deduplicate stale, duplicate, and excessive announcement symptoms when they share one root cause and remediation.

12. **Synthesize limits and verification.**
    - Group findings by affected task and root cause before counting criteria.
    - Separate `confirmed`, provisional, and `needs-validation` findings from passed checks and untested coverage.
    - Report every untested state, route, role, environment, technology combination, and data condition that limits conclusions.
    - Define targeted retests that reproduce the transition, name the expected result, and use the evidence method needed to close each finding.

## WCAG 2.2 mapping guidance

Use the following as common candidate mappings, not an exhaustive checklist. Confirm the criterion's applicability, target conformance level, and evidence for each finding. A pattern can fail without failing every criterion in its row, and a WCAG mapping does not establish page or product conformance.

| WCAG 2.2 criterion | Level | Consider when |
|---|---:|---|
| 1.3.1 Info and Relationships | A | Structure, labels, dialog or panel relationships, or state relationships are not programmatically determinable. |
| 1.3.2 Meaningful Sequence | A | Insertion, replacement, or visual reordering creates a programmatic reading sequence that changes meaning. |
| 1.4.13 Content on Hover or Focus | AA | A tooltip, popover, or other hover/focus content is not dismissible, hoverable, or persistent as required. |
| 2.1.1 Keyboard | A | A dynamic control, widget, update, or recovery action cannot be operated through a keyboard interface. |
| 2.1.2 No Keyboard Trap | A | Focus cannot leave a component or overlay through a standard or documented method. |
| 2.2.1 Timing Adjustable | A | A timeout or auto-dismiss behavior imposes a time limit that is not adjustable under the criterion's conditions. |
| 2.2.2 Pause, Stop, Hide | A | Auto-updating content cannot be paused, stopped, hidden, or controlled when the criterion applies. |
| 2.4.2 Page Titled | A | A client-side route does not expose a title that describes its topic or purpose. |
| 2.4.3 Focus Order | A | Programmatic focus movement or dynamic insertion produces an order that does not preserve meaning and operability. |
| 2.4.6 Headings and Labels | AA | A dynamic view, region, or control has a heading or label that does not describe its topic or purpose. |
| 2.4.7 Focus Visible | AA | Keyboard focus is not visibly identifiable in a dynamic state. |
| 2.4.11 Focus Not Obscured (Minimum) | AA | An author-created overlay or sticky region entirely hides the focused component. |
| 2.5.3 Label in Name | A | A control with a visible text label exposes a name that does not contain that visible text. |
| 3.2.1 On Focus | A | Receiving focus unexpectedly triggers a route, dialog, or other change of context. |
| 3.2.2 On Input | A | Changing a setting or input unexpectedly changes context without prior advice. |
| 3.3.1 Error Identification | A | A dynamic error is not identified or described in text. |
| 3.3.3 Error Suggestion | AA | A known correction is not suggested when the criterion applies. |
| 4.1.2 Name, Role, Value | A | A control's name or role is missing, or a user-settable value, state, or property is unavailable to user agents and assistive technologies. |
| 4.1.3 Status Messages | AA | Success, results, waiting, progress, or error information that does not receive focus is not programmatically determinable through role or properties. |

Check the normative [WCAG 2.2 Recommendation](https://www.w3.org/TR/WCAG22/) and applicable Understanding documents when a mapping is uncertain. Do not use conformance level as severity and do not claim that this focused audit covers all applicable success criteria.

## Shared finding contract

Return every finding with these required fields so the result can be merged directly by the inclusive-interface audit orchestrator:

| Field | Requirement |
|---|---|
| `id` | Stable unique identifier. |
| `target` | Route, component, flow, state, role, environment, and occurrence as applicable. |
| `evidence` | Evidence type, method, reference, environment, and reproducible observation. |
| `user_impact` | Affected users, blocked or impaired task, consequence, and workaround. |
| `status` | `confirmed`, `provisional`, `needs-validation`, `not-reproduced`, `resolved`, or `accepted-risk`. |
| `severity` | `critical`, `high`, `medium`, `low`, or `advisory`, based on user and task impact. |
| `confidence` | `high`, `medium`, or `low`, with the reason and missing evidence. |
| `framework_mappings` | Zero or more valid WCAG criteria or other supplied frameworks, each with rationale. |
| `recommendation` | Outcome-focused remediation guidance, constraints, and responsible surface. |
| `verification` | Retest steps, expected result, method, environment, and evidence required to close. |

Allow `source_skill`, `related_ids`, and `root_cause` as optional traceability fields. Set `source_skill` to `dynamic-interface-accessibility-audit` when useful. Treat `accepted-risk` as a documented product decision, not an auditor-selected disposition.

## Output format

Return:

```md
## Audit summary

- Target and version:
- Scope and sample:
- Evidence used:
- Overall outcome:
- Conformance disclaimer:

## Evidence ledger

| Evidence ID | Type | Target and state | Method and environment | Supports | Limitations |
|---|---|---|---|---|---|

## Transition coverage

| Transition ID | Trigger | Before, during, and after states | Focus expectation | Announcement expectation | Methods run | Result |
|---|---|---|---|---|---|---|

## Findings

### DIA-001 — Short title

- id:
- target:
- evidence:
- user_impact:
- status:
- severity:
- confidence:
- framework_mappings:
- recommendation:
- verification:
- source_skill: dynamic-interface-accessibility-audit
- related_ids: optional
- root_cause: optional

## Passed checks

- Include only checks directly exercised in a named state and environment.

## Coverage gaps and required validation

| Gap | Why it matters | Evidence needed | Priority |
|---|---|---|---|

## WCAG mapping summary

| Criterion | Finding IDs | Mapping rationale | Evidence limit |
|---|---|---|---|

## Retest priorities

1. ...
```

Keep a narrow component audit concise. For a multi-route application, preserve the contract and place repeated transition details in tables.

## Quality bar

The task is complete only when:

- Dialogs and overlays; tabs, menus, disclosures, and popovers; relevant state feedback; route changes; insertion and removal; asynchronous updates; focus; exposed semantics; and announcement quality are covered or explicitly marked out of scope.
- Each dynamic behavior is tested as a transition with before, intermediate, terminal, failure, and interruption states where applicable.
- Static source, automated, browser runtime, and assistive-technology evidence are labeled and never substituted for one another.
- Every finding follows the shared contract and includes reproducible evidence, user impact, confidence, and a targeted verification method.
- Stale, duplicate, missing, delayed, interrupted, and excessive announcements are considered.
- WCAG 2.2 mappings include criterion-specific rationale and never imply complete conformance.
- Passed checks are limited to the exact sampled state and environment.
- Untested states and technology combinations remain visible as coverage gaps.
- No files, accounts, or external systems are modified.

## Edge cases

- **Source only:** Report source-backed defects and intended behavior, then list runtime and assistive-technology checks required for computed semantics, focus, timing, and announcements.
- **Running target without assistive technology:** Confirm browser runtime behavior, but mark spoken-output and announcement-quality claims `needs-validation`.
- **Screenshot or design only:** Review visible state communication as provisional design evidence. Do not claim keyboard, focus, semantic, or announcement results.
- **No reproducible async state:** Use safe fixtures, network throttling, or documented test hooks only when already available. Record the state as untested rather than mutating production data.
- **Authenticated or consequential flow:** Use authorized test accounts and safe data. Do not bypass access controls or trigger irreversible actions.
- **Third-party widget:** Separate observed user impact from remediation ownership, vendor constraints, wrapper options, replacement options, and accepted-risk decisions.
- **Inconsistent assistive-technology output:** Preserve results by exact environment, check computed semantics and timing, and avoid declaring one product universally correct or broken from a single combination.
- **Transient message unavailable for replay:** Treat the inability to review important information as part of the user impact; do not rely on a recording as the user-facing solution.
- **Nested or concurrent overlays:** Test stacking, inactive layers, Escape ownership, focus containment, close order, and restoration after each layer.
- **Virtualized or streaming content:** Test position, item count where exposed, focus persistence, stale nodes, newly loaded content, and recovery when the focused item is recycled.

## Related skills

- `inclusive-interface-audit-orchestrator`
- `accessibility-validation-planner`
- `interface-state-coverage-review`
- `keyboard-focus-accessibility-audit` when available
