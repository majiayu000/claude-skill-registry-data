---
name: complex-widget-pattern-audit
description: Audits custom composite widgets—including comboboxes, listboxes, trees, treegrids, grids, menus, tablists, carousels, command palettes, date pickers, and mixed controls—for coherent semantics, keyboard interaction, focus, selection, active-item behavior, and announcements. Use when reviewing an implemented widget against its intended native HTML or ARIA pattern, identifying unsupported or mixed patterns, or defining the runtime and assistive-technology tests needed to verify accessibility.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository or artifact access. Runtime keyboard, accessibility-tree, and assistive-technology conclusions require a testable interface and representative environments.
metadata:
  category: frontend-a11y
  task_type: review
  audience: frontend-developers-design-system-maintainers-and-accessibility-reviewers
  tags:
    - accessibility
    - aria
    - composite-widgets
    - keyboard
    - focus-management
    - screen-reader
    - combobox
    - tree
    - menu
    - tabs
  status: draft
  side_effects: none
---

# Complex Widget Pattern Audit

## Purpose

Audit whether each custom widget implements one coherent, appropriate interaction pattern. Identify the intended pattern, prefer native HTML when it can meet the product need, compare computed semantics and actual behavior with the selected pattern, and distinguish confirmed failures from risks that require runtime or assistive-technology validation.

This is a review-only specialist. Do not modify the target, assume that adding ARIA makes a widget accessible, treat an Authoring Practices Guide example as a universal prescription, or claim complete WCAG conformance.

## When to use this skill

Use this skill when:

- A custom combobox, listbox, tree, treegrid, grid, menu, tablist, carousel, command palette, date picker, or other composite control needs accessibility review.
- A widget uses managed focus, roving `tabindex`, `aria-activedescendant`, directional navigation, selection, expansion, or dynamic announcements.
- Semantics and behavior appear to come from different patterns.
- A design-system component must be compared with its documented interaction contract.
- Source review has found a plausible widget risk that needs structured runtime or assistive-technology tests.
- An audit orchestrator assigns the complex-widget work package.

Do not use this skill when:

- Native form controls or ordinary links and buttons are the only controls in scope.
- The request concerns static data-table semantics without a composite grid interaction model; use `data-table-grid-accessibility-audit`.
- The request concerns page-wide keyboard order or focus trapping rather than a widget's internal interaction contract; use `keyboard-focus-accessibility-audit`.
- The user asks only for implementation, legal certification, or a complete accessibility audit.
- Several unrelated accessibility domains need coordination; use an audit orchestrator and assign this skill only the widget-pattern portion.

## Operating rules

- Identify the interaction contract before judging individual attributes or keys.
- Prefer native HTML when it supplies the required semantics and behavior. Do not replace a native `<select>`, disclosure, button group, link list, or other sufficient native control with ARIA solely for styling.
- Inspect native elements and computed accessibility semantics, not class names or product labels.
- Treat role, owned elements, accessible name, properties, states, focus model, keyboard behavior, selection model, and announcements as one pattern contract.
- Preserve distinctions among DOM focus, active item, visual highlight, selection, checked state, current item, expansion, and activation.
- Do not require every optional key from a reference pattern. Do require the implemented and documented key model to be complete, discoverable where necessary, and internally consistent.
- Treat WAI-ARIA Authoring Practices as informative pattern guidance and WCAG as the normative basis for any success-criterion mapping.
- Do not infer accessibility from ARIA presence, automated checks, source, or screenshots alone.
- Base severity on user impact and task criticality, not a WCAG conformance level.

## Orchestrator compatibility

When `inclusive-interface-audit-orchestrator` supplies scope, identifiers, allowed values, framework rules, deduplication decisions, or a shared finding contract, use them exactly. Do not create a competing schema.

If no orchestrator is available, remain independently usable by applying the mirrored finding contract below. Use `source_skill: complex-widget-pattern-audit` when optional traceability fields are supported.

## Inputs to inspect

Start with the smallest evidence set that establishes the widget's contract and critical states:

- Audit scope, critical tasks, supported browsers, platforms, input methods, assistive technologies, viewports, locales, and requested WCAG baseline.
- Rendered widgets, component stories, prototypes, recordings, screenshots, accessibility-tree captures, and reproducible URLs or builds.
- Widget markup, styles, event handlers, focus utilities, state management, portal or popup logic, virtualization, and component APIs.
- Product requirements and documentation for opening, closing, navigation, selection, activation, editing, filtering, escape behavior, and announcements.
- Unit, integration, keyboard, end-to-end, accessibility, and assistive-technology tests.
- Fixtures for empty, loading, error, disabled, readonly, required, invalid, filtered, selected, expanded, collapsed, virtualized, and asynchronous states.

Do not read an entire repository when representative implementations, stories, and tests establish the behavior.

## Evidence limits

| Evidence | Can support | Cannot establish alone |
|---|---|---|
| Source | Intended roles, relationships, event handling, focus logic, and state transitions | Computed semantics, actual key behavior, spoken output, or interoperability |
| Screenshot or design | Visible labels, instructions, focus styling, controls, and apparent states | Programmatic roles, focus ownership, keyboard behavior, or announcements |
| Accessibility tree | Computed name, role, state, hierarchy, and active-descendant exposure in one environment | Complete interaction, visual focus, spoken usefulness, or other environments |
| Running interface | Actual keys, focus movement, state changes, dismissal, and computed semantics | Untested browsers, assistive technologies, data, locales, or hidden states |
| Automated test | Assertions and rules actually executed | Pattern coherence, complete keyboard operation, understandable speech, or conformance |
| Assistive-technology test | Experienced navigation, context, state, and announcements for the named combination | Universal behavior across untested combinations |

Use `confirmed` only when evidence demonstrates the problem. Use `provisional` when evidence strongly indicates it but one material condition remains unverified. Use `needs-validation` for a concrete risk with explicit runtime or assistive-technology test steps. Absence of evidence is not a pass.

## Pattern classification guide

Use the current authoritative specification and pattern guidance selected for the audit. This guide identifies common decision points; it is not a substitute for inspecting the widget's documented contract.

| Intended pattern | Key classification questions |
|---|---|
| Native control | Can a native `<select>`, input, button, disclosure, link list, or grouped control meet the task without a composite widget? |
| Combobox | Is there an editable or select-only input/control with a related popup? Is the popup a listbox, grid, tree, or dialog, and do autocomplete and value-commit behavior match that choice? |
| Listbox | Is the task choosing options rather than invoking commands or navigating links? Is single- or multi-selection explicit and distinct from focus? |
| Tree | Is the content hierarchical with expandable parent items and tree-style directional navigation? |
| Grid or treegrid | Does the widget intentionally provide composite cell or row navigation? For a treegrid, are hierarchical expansion and grid navigation both coherent? |
| Menu or menubar | Are the items application commands or choices in a menu interaction, rather than site navigation, ordinary actions, or a selectable list? |
| Tablist | Does each tab control one associated tab panel, with a coherent automatic or manual activation model? |
| Carousel | Is it a content rotator composed from suitable native controls, regions, slides, and status behavior? Does rotation stop and remain stopped when users interact? |
| Command palette | Is it a dialog containing a combobox/listbox, a menu-like command surface, or another documented composition? Do not invent a single `command-palette` role. |
| Date picker | Is it a native date input or a composition such as an input/combobox plus dialog and calendar grid? Are date navigation, selection, formatting, and return focus specified? |
| Other composite | Is there one tab stop with managed internal navigation and a documented role/state model, or would ordinary controls in the page tab sequence be more appropriate? |

Treat a pattern as **unsupported** when its required semantics or interaction model is not sufficiently supported in the target browser and assistive-technology matrix, or when the implementation relies on invented roles, invalid ownership, or unavailable platform behavior. Treat a pattern as **mixed** when semantics, keyboard behavior, focus model, state model, or instructions materially follow different patterns—for example, a `menu` with listbox selection behavior or a combobox whose popup role and keyboard logic disagree.

## Workflow

1. **Frame the review.**
   - Record the target, instances, critical tasks, states, evidence, environments, exclusions, and requested standards.
   - If no WCAG version is specified, disclose WCAG 2.2 as the mapping baseline. Do not invent a conformance level.
   - Separate source-supported conclusions from runtime, accessibility-tree, and assistive-technology conclusions.

2. **Inventory widgets and representative states.**
   - List each materially different widget implementation, its product label, trigger, popup or owned content, states, and consumers.
   - Sample by implementation, configuration, and risk rather than appearance alone.
   - Include opening, closing, empty, disabled, readonly, invalid, loading, filtered, async, selection, activation, and error states where applicable.
   - Expand the sample when instances differ in roles, focus strategy, libraries, virtualization, popup rendering, or event handling.

3. **Identify the intended pattern.**
   - Infer intent from the user task, native elements, computed roles, documentation, and actual behavior; do not rely on a component name.
   - Record the primary pattern, any composed subpatterns, the reference used, required behaviors, optional behaviors adopted, and unresolved ambiguity.
   - Ask whether a simpler native control or ordinary group of native controls would satisfy the task.
   - If no coherent pattern fits, report the mismatch rather than forcing the closest role.

4. **Compare native and custom approaches.**
   - Identify the platform behavior the custom widget replaces and the product requirement that justifies replacement.
   - Compare keyboard, touch, zoom, forced-colors, mobile, form, validation, and assistive-technology consequences.
   - Recommend native HTML when it meets the requirement. When it does not, state why a custom pattern is necessary and what validation burden it creates.

5. **Audit names, roles, relationships, properties, and states.**
   - Inspect computed accessible names and roles for the container, trigger, input, popup, items, groups, panels, and supporting text.
   - Verify required ownership and relationships such as popup association, controls, labelled-by, described-by, active descendant, level, position, set size, selection, expansion, orientation, autocomplete, modal state, and invalid or disabled state as applicable.
   - Check that IDs are unique and references remain valid through portals, filtering, virtualization, rerendering, and asynchronous updates.
   - Verify state changes are programmatically exposed at the correct time and do not conflict with native semantics.
   - Flag prohibited roles, invalid states, invented semantics, redundant ARIA that changes native behavior, and hidden-but-referenced content.

6. **Audit keyboard interaction.**
   - Test entry, exit, opening, closing, traversal, boundary behavior, activation, selection, cancellation, and return to the invoking context.
   - Test `Tab`, `Shift+Tab`, arrow keys, `Home`, `End`, `Page Up`, `Page Down`, `Enter`, `Space`, `Escape`, and type-ahead only where the selected pattern defines or documents them.
   - Check modifier keys, editable text expectations, platform conventions, repeated keys, key holds, and keys at first and last items.
   - Confirm disabled items, nested controls, links, editable cells, submenus, and popup transitions do not create traps or unreachable actions.
   - Verify documented optional shortcuts do not override text editing or browser and assistive-technology commands unexpectedly.

7. **Audit focus ownership and movement.**
   - Identify whether the widget uses DOM focus, roving `tabindex`, or `aria-activedescendant`; require one coherent strategy per interaction context.
   - Verify one intended page-tab entry point for a composite unless the pattern explicitly requires otherwise.
   - For roving focus, check exactly one current item is tabbable and that rerenders do not lose it.
   - For `aria-activedescendant`, check DOM focus remains on the owning element and the referenced active item exists, is owned or validly controlled, is exposed, and is scrolled into view.
   - Test opening focus, closing focus, focus restoration, removal of the active item, filtering, async updates, virtualization, nested widgets, and unmounting.
   - Distinguish visible focus, DOM focus, accessibility focus, and active-item styling in evidence.

8. **Audit selection, activation, and active-item behavior.**
   - Define whether navigation changes only the active item, also changes selection, immediately activates content, or updates an input value.
   - Verify single- and multi-selection models, range or modifier behavior, persistent selection, deselection, and selected-item removal.
   - Check automatic versus manual tab activation, combobox value commitment, menu command invocation, tree expansion, grid edit mode, date selection, and carousel slide changes against the chosen contract.
   - Ensure visual highlight and programmatic `selected`, `checked`, `current`, or `expanded` states describe the same user-understandable state.

9. **Audit announcements and context.**
   - Verify names, roles, states, position, level, set size, selection, expansion, availability, and instructions are exposed without excessive repetition.
   - Test popup opening and closing, result counts, no-results, filtering, async loading, errors, value changes, selection, command completion, date context, and carousel rotation where users need nonvisual feedback.
   - Prefer native state-change exposure over unnecessary live regions.
   - Check live regions for existence before updates, appropriate politeness, atomicity, deduplication, stale messages, rapid-update flooding, and interruption.
   - Record exact assistive technology, browser, platform, input mode, speech settings, state, action, and heard output for announcement claims.

10. **Detect mixed and unsupported patterns.**
    - Compare the widget's role hierarchy, owned content, keyboard model, focus strategy, selection model, instructions, and announcements as one matrix.
    - Identify conflicts among implementation, documentation, automated tests, visual cues, and user expectations.
    - Check target-environment support for unusual role combinations, `aria-activedescendant` ownership, virtualization metadata, nested composites, and portal-rendered popups.
    - Do not recommend attribute patching when the root problem is a confused interaction model. Recommend selecting and implementing one coherent contract.

11. **Require proportionate runtime validation.**
    - Always require runtime keyboard testing for custom composite behavior.
    - Require accessibility-tree inspection for computed roles, names, states, hierarchy, and active-descendant exposure.
    - Require representative assistive-technology tests for announcements, complex composites, unusual compositions, unsupported-pattern risks, and any behavior not established by source.
    - Include touch and mobile assistive-technology testing when the widget is in mobile scope.
    - State exact setup, steps, expected result, environment, evidence to capture, and retest scope. Do not write “test with a screen reader” without a protocol.

12. **Produce root-cause findings.**
    - Merge symptoms that share one widget contract failure, root cause, remediation, and verification path.
    - Keep separate findings when failures have different causes, impacts, owners, or retests.
    - Separate confirmed findings, provisional findings, validation needs, not-reproduced results, and coverage gaps.
    - Map WCAG only when evidence supports the criterion. A pattern-guide deviation alone is not a WCAG failure.
    - Recommend outcomes and constraints, not copy-paste ARIA without corresponding behavior.

## Shared finding contract

Use every required field for each issue:

| Field | Requirement |
|---|---|
| `id` | Stable unique identifier |
| `target` | Route, component, widget instance, state, role, environment, and occurrence as applicable |
| `evidence` | Evidence type, method, reference, environment, and reproducible observation |
| `user_impact` | Affected users, blocked or impaired task, consequence, and workaround |
| `status` | `confirmed`, `provisional`, `needs-validation`, `not-reproduced`, `resolved`, or `accepted-risk` |
| `severity` | `critical`, `high`, `medium`, `low`, or `advisory`, based on user and task impact |
| `confidence` | `high`, `medium`, or `low`, with the reason and missing evidence |
| `framework_mappings` | Zero or more valid WCAG criteria or other requested framework mappings, each with rationale |
| `recommendation` | Outcome-focused remediation guidance, constraints, and responsible surface |
| `verification` | Retest steps, expected result, method, environment, and evidence required to close |

Allow `source_skill`, `related_ids`, and `root_cause` as optional traceability fields. Do not use WCAG level as severity. Treat `accepted-risk` as a documented product decision, not an auditor decision.

## Output format

Return:

```md
## Audit summary

- Target and scope:
- Evidence and environments:
- Widget patterns reviewed:
- Overall outcome:
- Highest-impact risks:
- Evidence limitations:

## Widget pattern inventory

| Widget ID | Target and states | Intended pattern | Native alternative | Focus model | Selection or activation model | Evidence | Pattern status |
|---|---|---|---|---|---|---|---|

Pattern status: coherent, mixed, unsupported, ambiguous, or needs-validation.

## Findings

### [ID] Finding title

- target:
- evidence:
- user_impact:
- status:
- severity:
- confidence:
- framework_mappings:
- recommendation:
- verification:
- source_skill: complex-widget-pattern-audit

## Validation queue

| Widget ID | Risk or question | Setup and state | Steps | Expected result | Environment | Evidence to capture |
|---|---|---|---|---|---|---|

## Coverage gaps

- Untested widgets, states, inputs, browsers, platforms, assistive technologies, locales, and limitations.
```

Omit empty optional traceability fields. If no issue is confirmed, report that bounded result and retain material validation needs and coverage gaps.

## Quality bar

The task is complete only when:

- Every widget has an intended pattern, composition, native-alternative decision, and pattern-status classification.
- The audit compares computed semantics and actual behavior with one explicit pattern contract.
- Names, roles, relationships, properties, states, keyboard behavior, focus, active item, selection, activation, and announcements are covered where applicable.
- Focus, active item, visual highlight, selection, checked state, current state, expansion, and activation are not conflated.
- Mixed and unsupported patterns are identified at the contract level rather than reduced to isolated ARIA edits.
- Runtime, accessibility-tree, and assistive-technology conclusions are bounded to evidence and named environments.
- Every validation need includes reproducible steps, expected results, environments, and evidence requirements.
- Findings follow the supplied or mirrored shared contract and are deduplicated by root cause.
- WCAG mappings are evidence-based, and no APG deviation is presented as an automatic conformance failure.
- Native HTML is preferred where appropriate, without claiming that native controls remove all testing needs.
- No complete-audit, universal-support, legal-compliance, or conformance claim is made.

## Edge cases

- **No running target:** Review intent and source, then mark keyboard, focus, computed semantics, and announcements as needing runtime validation.
- **Screenshot or design only:** Classify visible intent provisionally; do not claim roles, focus behavior, keyboard operation, or announcements.
- **Ambiguous pattern:** Document plausible models and the conflicting evidence. Ask the product team to choose the interaction contract before prescribing roles.
- **Pattern composition:** Audit both the outer pattern and embedded pattern, including focus handoff and escape behavior between them.
- **Virtualized items:** Verify active and selected items remain represented, references stay valid, position metadata is accurate, and offscreen movement is announced and scrolled appropriately.
- **Portal-rendered popup:** Validate relationships, ownership, reading order, focus containment, outside interaction, and dismissal in representative environments.
- **Editable content inside a composite:** Define navigation mode versus text-editing mode and prevent widget shortcuts from consuming editing keys.
- **Touch-only or mobile UI:** Do not translate desktop arrow-key expectations mechanically; test platform accessibility gestures, focus order, names, states, and equivalent operation.
- **Third-party widget:** Distinguish application configuration from vendor defects and identify wrapper, replacement, escalation, or acceptance options.
- **Conflicting reference patterns:** Use the target standard and support matrix named in scope, record the version, and treat unresolved interoperability as a validation need.

## Related skills

- `inclusive-interface-audit-orchestrator`
- `data-table-grid-accessibility-audit`
- `keyboard-focus-accessibility-audit`
- `dynamic-interface-accessibility-audit`
- `semantic-structure-accessibility-audit`
- `accessibility-validation-planner`
