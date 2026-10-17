---
name: data-table-grid-accessibility-audit
description: Audits static data tables, sortable tables, interactive ARIA grids, virtualized data, filtering, selection, row and column actions, result updates, and responsive alternatives for accessibility. Use when the user asks to review table purpose, captions, header associations, sorting state, grid keyboard interaction, focus management, selection, virtualization, changed-result announcements, or empty and loading states against WCAG.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository or artifact access. Runtime keyboard, responsive, accessibility-tree, and screen-reader conclusions require a testable interface and representative environments.
metadata:
  category: frontend-a11y
  task_type: review
  audience: frontend-developers-design-system-maintainers-and-accessibility-reviewers
  tags:
    - accessibility
    - wcag
    - data-tables
    - aria-grid
    - keyboard
    - screen-reader
    - virtualization
    - responsive-design
    - sorting
    - selection
  status: draft
  side_effects: none
---

# Data Table and Grid Accessibility Audit

## Purpose

Audit whether people can understand and operate tabular data across static tables, sortable tables, interactive grids, virtualized collections, and responsive variants. Select the native table or ARIA grid expectations that match the implemented interaction model, distinguish confirmed defects from checks that need runtime or assistive-technology evidence, and map only supported findings to applicable WCAG criteria.

This is a review-only specialist. Do not modify the target, claim complete WCAG conformance, or treat an ARIA Authoring Practices Guide pattern deviation as an automatic WCAG failure.

## When to use this skill

Use this skill when:

- A page or component presents data in rows and columns.
- A table supports sorting, filtering, pagination, selection, expansion, editing, or row and column actions.
- A custom `grid` or `treegrid` needs semantic, keyboard, focus, or selection review.
- Data is virtualized, lazy-loaded, infinitely scrolled, or only partly present in the DOM.
- A responsive table becomes scrollable, hides columns, or changes to cards, lists, or another narrow-screen presentation.
- Loading, empty, filtered, refreshed, or changed-result states need accessibility review.
- An audit orchestrator assigns the tables-and-data-grids work package.

Do not use this skill when:

- The target is a layout table with no data relationships; route the underlying layout and reading-order issues to the applicable semantic or responsive specialist.
- The primary target is a chart, map, canvas visualization, or spreadsheet file rather than an HTML or ARIA table-like interface.
- The request is only to implement fixes, certify legal compliance, or establish complete WCAG conformance.
- A broader audit needs several unrelated accessibility domains; use an orchestrator and select this skill for the tabular-data portion.

## Operating rules

- Prefer native HTML table semantics for static tabular data, including sortable tables whose sort controls are ordinary buttons in header cells.
- Do not recommend `role="grid"` merely because a table contains links, buttons, checkboxes, menus, filters, or sortable columns. A native table may contain interactive controls, and those controls remain ordinary page tab stops.
- Treat an ARIA grid as a composite widget. Once `grid` or `treegrid` is used, require a coherent focus-management and directional-navigation model rather than table-style document browsing alone.
- Do not add keyboard behavior to a static table container. Test the normal keyboard behavior of controls inside it.
- Prefer native `<table>`, `<caption>`, `<th>`, and `<td>` elements when they express the structure. Treat ARIA table roles as a fallback whose browser and assistive-technology support requires manual validation.
- Preserve the distinction between focus, selection, checked state, expanded state, edit mode, and sort state. Do not infer one state from visual styling for another.
- Treat WAI-ARIA Authoring Practices as informative interaction guidance and WCAG as the normative basis for success-criterion mappings.
- Base severity on user and task impact, not WCAG conformance level.
- Do not infer accessible behavior from source or screenshots alone. Bound every conclusion to the evidence actually inspected.

## Orchestrator compatibility

When `inclusive-interface-audit-orchestrator` invokes this skill, use its scope, identifiers, severity scale, allowed status values, framework-mapping rules, deduplication decisions, and shared finding contract exactly. Do not create a parallel schema.

If the orchestrator is unavailable, remain independently usable by applying the mirrored contract in this skill. Use `source_skill: data-table-grid-accessibility-audit` when optional traceability fields are supported.

## Inputs to inspect

Start with the smallest evidence set that establishes the table model, states, and critical tasks:

- Audit scope, critical tasks, target WCAG version and level, supported browsers, platforms, input methods, assistive technologies, viewports, zoom levels, roles, locales, and data conditions.
- Rendered pages, component stories, prototypes, screenshots, recordings, accessibility-tree captures, and reproducible URLs or builds.
- Table, grid, cell, header, filter, sort, pagination, virtualization, selection, action-menu, and responsive-renderer source.
- Relevant HTML templates, CSS, event handlers, focus utilities, state management, data adapters, and component-library APIs.
- Unit, integration, accessibility, keyboard, end-to-end, and assistive-technology test evidence.
- Fixtures for dense, sparse, empty, loading, error, filtered, selected, expanded, edited, paginated, and virtualized states.
- Product requirements for sort precedence, selection persistence, hidden columns, row identity, bulk actions, edit behavior, and expected announcements.

Do not read the entire repository when representative implementations, stories, fixtures, and tests can establish the behavior.

## Evidence limits

| Evidence type | Can support | Cannot establish alone |
|---|---|---|
| Source | Intended elements, roles, attributes, event handling, focus logic, and virtualization metadata | Computed roles and names, actual key behavior, announcement output, visual reflow, or interoperability |
| Screenshot or design | Visible captions, labels, indicators, density, truncation, apparent states, and responsive intent | Header associations, DOM order, keyboard operation, programmatic states, focus movement, or announcements |
| Accessibility tree | Computed roles, names, states, row and column metadata, and exposed hierarchy in one environment | Complete keyboard operation, visual behavior, other environments, or understandable spoken output |
| Running interface | Reproducible interaction, focus movement, visual states, responsive changes, and computed semantics | Untested data sizes, roles, breakpoints, browsers, assistive technologies, or hidden states |
| Automated test or scanner | Assertions and rules actually executed | Correct table comprehension, complete grid interaction, spoken context, or WCAG conformance |
| Screen-reader test | Experienced reading, navigation, state, position, and announcement behavior for the named combination | Universal assistive-technology behavior or untested states and data |

Use `confirmed` only when evidence demonstrates the failure. Use `provisional` when evidence strongly indicates a defect but one material condition remains unverified. Use `needs-validation` for a concrete risk requiring runtime or assistive-technology testing. Absence of evidence is not a pass.

## Native table versus ARIA grid decision

Classify each target before applying interaction expectations.

| Model | Typical characteristics | Expected keyboard model |
|---|---|---|
| Native data table | Static row-column relationships; may include links, buttons, checkboxes, sort buttons, or menus | Document or table reading commands belong to assistive technology; only embedded controls enter the page tab sequence |
| Sortable native table | Native table with one or more header controls that reorder data | `Tab` reaches each sort control; its native activation keys operate it; the table container does not acquire arrow-key navigation |
| ARIA table | Static tabular structure built without native table elements | No composite-widget keyboard model; focus only interactive descendants; require strong interoperability justification and testing |
| ARIA data grid | Composite tabular widget with managed cell navigation, selection, editing, or spreadsheet-like operation | One managed entry point; arrow keys move within the grid; `Home`, `End`, and other documented grid commands work consistently |
| Treegrid | Hierarchical interactive rows with grid navigation and expand/collapse behavior | Apply the selected treegrid pattern in addition to grid navigation, state, and focus expectations |

If the semantics and behavior disagree, report the mismatch and its user impact. Do not solve a broken grid only by removing its role unless the resulting native-table model supports every required interaction and content relationship.

## Workflow

1. **Frame the review.**
   - Record the target, user tasks, table instances, data volumes, roles, states, environments, evidence, exclusions, and requested WCAG baseline.
   - If no WCAG version is named, disclose WCAG 2.2 as the mapping baseline. If no conformance level is named, keep it as an open scope decision rather than inventing one.
   - Identify whether source, runtime, responsive, keyboard, and screen-reader testing are available.

2. **Inventory table-like surfaces and states.**
   - List every materially different native table, ARIA table, grid, treegrid, responsive alternative, and virtualized implementation in scope.
   - Include default, sorted, multi-sorted, filtered, paginated, selected, expanded, editing, loading, empty, error, refreshed, and permission-limited states when present.
   - Sample by implementation and risk, not only by visual appearance. Expand the sample when similar tables use different markup, libraries, state models, or responsive renderers.

3. **Classify the interaction model.**
   - Inspect native elements and computed roles rather than class names or product labels such as “data grid.”
   - Determine whether the interface behaves as a document structure, a table containing controls, a composite grid, or a treegrid.
   - Record the chosen reference model and any mismatch among semantics, documented behavior, and actual interaction.

4. **Audit table purpose and orientation.**
   - Check for a concise, programmatically associated caption or equivalent accessible name that identifies the table when surrounding context is insufficient.
   - Distinguish a table name from longer instructions or descriptions. Avoid repeating the same text as both caption and summary.
   - Verify that users can discover sorting, filtering, selection, editing, scrolling, hidden-column, and action behavior without relying only on position, color, icons, or hover.
   - Check whether multiple similar tables have names that distinguish their purpose.

5. **Audit headers and relationships.**
   - Verify genuine header cells use `<th>` or the appropriate `columnheader` or `rowheader` role.
   - For simple native tables, verify `scope="col"` and `scope="row"` where it improves reliable association; do not require redundant attributes when the native algorithm is unambiguous and supported.
   - For grouped, irregular, or multi-level native headers, verify each data cell can be associated with every required header. Use an appropriate combination of structural grouping, `scope`, or explicit `headers` and unique `id` references.
   - Check row and column spans, blank header cells, repeated header rows, nested tables, sticky clones, hidden columns, and DOM reordering for broken or misleading associations.
   - Verify visual header text, accessible names, sort controls, and the exposed row and column structure remain consistent.

6. **Audit sorting and filtering.**
   - Verify each sortable header exposes a clear control name and current state. Apply `aria-sort` only to the header currently controlling sort as appropriate; represent ascending, descending, or other order accurately.
   - For multi-column sorting, document the interaction and precedence in accessible text because `aria-sort` alone does not express multiple sort keys or their priority.
   - Verify activation works by keyboard and does not move focus unpredictably when rows reorder or refresh.
   - Check filter labels, instructions, clear/reset controls, submitted versus live filtering, removable tokens, result counts, and recovery from zero results.
   - Ensure visual icons, text, programmatic state, and actual data order agree.

7. **Audit native-table keyboard behavior and actions.**
   - Follow the page tab sequence through sort controls, cell links, row-selection checkboxes, action buttons, menus, pagination, and related controls.
   - Verify native controls retain their expected activation, menu, checkbox, and form behavior.
   - Check that repeated row actions have names or descriptions that include enough row context without becoming excessively verbose.
   - Verify keyboard users can reach, open, operate, dismiss, and leave row or column action UI, and that focus returns to a logical surviving target after close, delete, refresh, or pagination.
   - Flag an excessively long tab sequence as an efficiency concern, but do not prescribe a grid unless the product can implement and support the complete composite-widget contract.

8. **Audit ARIA grid keyboard interaction and focus.**
   - Verify the grid has one managed page-tab stop and a stable focus target using roving `tabindex` or `aria-activedescendant`.
   - Verify arrow keys move predictably among cells. Test `Home` and `End`, and when supported, `Control` + `Home`, `Control` + `End`, `Page Up`, and `Page Down`.
   - Check boundary behavior, disabled or hidden cells, merged cells, pinned rows or columns, scrolling, pagination, and dynamically loaded edges.
   - Verify focus lands on the cell or single contained widget that provides the most understandable spoken result.
   - For editable cells or cells with multiple or arrow-key-dependent widgets, verify a discoverable transition between navigation and edit/action modes, including reliable exit and focus restoration.
   - Ensure grid navigation does not consume keys while focus is operating an inner control that needs them.
   - Verify focus remains visible, unobscured, logically ordered, and recoverable after sorting, filtering, insertion, deletion, virtualization, or rerendering.

9. **Audit selection and bulk actions.**
   - Identify whether selection applies to rows, columns, cells, visible results, the current page, or the complete filtered data set.
   - Verify selection is programmatically exposed on the selected object, commonly with `aria-selected` for grid rows or cells or native checkbox state for explicit table selection.
   - When an ARIA grid permits multiple selected items, verify `aria-multiselectable="true"` is present on the grid and the selection model matches it.
   - Keep keyboard focus and selection visually and programmatically distinct.
   - Test single, multiple, range, select-all, clear-all, and persistence behavior across filtering, sorting, pagination, virtualization, and data refresh.
   - Verify selection counts and bulk-action availability are perceivable, and confirm destructive or consequential actions identify the affected scope.
   - Compare optional grid selection shortcuts with the documented product model; report APG deviations separately unless they cause a supported WCAG failure.

10. **Audit row and column actions.**
    - Check action names, row or column context, disabled state, menu state, confirmation, cancellation, and post-action feedback.
    - Verify actions are not available only on hover or through pointer gestures.
    - Check column hiding, resizing, reordering, pinning, grouping, and context menus for keyboard alternatives and updated structural metadata.
    - Verify focus and selection survive non-destructive actions and move predictably when the focused row or column is removed.

11. **Audit virtualized and partial data.**
    - Verify exposed total row and column counts represent the logical data set when known, and that row and column indices represent logical positions rather than recycled DOM positions.
    - Check `aria-rowcount`, `aria-colcount`, `aria-rowindex`, and `aria-colindex` where ARIA semantics require them; do not add redundant ARIA that conflicts with complete native table structure.
    - Verify off-screen recycling does not duplicate IDs, stale accessible names, selected states, indices, or action context.
    - Test directional navigation, jumps, page movement, search results, live loading, focus retention, and announcements across virtualization boundaries.
    - Verify a focused or active cell is not removed without a deterministic replacement and that assistive technology can discover newly rendered content.
    - Require manual screen-reader testing for virtualized grids and for any table whose logical structure is only partly represented in the DOM.

12. **Audit responsive behavior.**
    - Test narrow viewports, browser zoom, text enlargement, reflow, orientation changes, and content expansion using representative dense and long data.
    - For horizontal scrolling, verify the scroll region is discoverable and keyboard operable, focus is not clipped, and sticky headers or columns do not obscure content.
    - For hidden columns, verify essential information and action context remain available and users can discover or restore omitted data.
    - For card, list, disclosure, or transposed alternatives, verify every record retains its labels, values, reading sequence, actions, selection, and state without depending on visual alignment.
    - Check that CSS display changes, cloned markup, or alternate renderers do not remove native table semantics or create duplicate accessible content.
    - Do not require all tables to transform into cards; accept scrolling, prioritization, or another approach when information and operation remain available.

13. **Audit announcements and non-default states.**
    - Test initial and subsequent loading, delayed loading, partial loading, refresh, errors, no data, no filter matches, permission limits, and stale-data states.
    - Verify the interface distinguishes “no records exist” from “no records match these filters” and offers appropriate recovery.
    - Check whether changed result counts, completed filtering, asynchronous sorting, page changes, selection totals, saved edits, and bulk-action outcomes are announced when the change is not otherwise conveyed by focus or context.
    - Prefer concise status messages that do not move focus or repeatedly announce every keystroke. Do not add live regions for changes already communicated adequately.
    - Verify any programmatic busy state, including `aria-busy` where applicable, matches actual availability and that loading text does not conceal still-operable controls or strand focus.

14. **Run manual keyboard and screen-reader tests.**
    - Complete representative tasks with keyboard alone in every interactive model.
    - Test at least one representative supported screen-reader, browser, and platform combination for native header reading, sort state, action context, result announcements, selection, grid position, navigation and edit modes, virtualization, and responsive alternatives.
    - Record the exact environment, data state, commands, spoken or braille output, expected result, and limitation.
    - Mark screen-reader testing as required, completed, blocked, or out of scope. Never silently omit it.

15. **Map and normalize findings.**
    - Connect each finding to an observed user impact and the narrowest applicable WCAG criterion.
    - Keep APG pattern deviations, HTML or ARIA specification issues, usability concerns, and WCAG failures distinct.
    - Merge symptoms with the same root cause, target behavior, remediation, and verification method. Preserve separate occurrences and all valid mappings.
    - Return every finding in the shared contract and separate confirmed findings, items needing validation, not-reproduced checks, coverage gaps, and passes observed only in the tested sample.

## WCAG 2.2 applicability guide

Consider these criteria only when the evidence fits:

| Criterion | Level | Typical application |
|---|---:|---|
| 1.3.1 Info and Relationships | A | Table purpose, headers, cell associations, roles, row and column structure, selection or sort state conveyed only visually |
| 1.3.2 Meaningful Sequence | A | Responsive transformations, reordered DOM, cards, or virtualized rendering create an incorrect reading sequence |
| 1.4.3 Contrast (Minimum) | AA | Table text, placeholder text, or state labels lack required text contrast |
| 1.4.10 Reflow | AA | Data or controls require two-dimensional scrolling at the criterion's viewport conditions without an applicable exception |
| 1.4.11 Non-text Contrast | AA | Focus, selection, boundaries needed to identify controls, or state indicators lack required contrast |
| 2.1.1 Keyboard | A | Sorting, filtering, selection, editing, scrolling, navigation, or actions cannot be completed by keyboard |
| 2.1.2 No Keyboard Trap | A | Focus cannot leave a grid, edit mode, scroll region, menu, or action UI |
| 2.4.3 Focus Order | A | Focus moves in an order that breaks table or grid meaning and operation |
| 2.4.6 Headings and Labels | AA | Table, filter, action, or control labels do not describe topic or purpose |
| 2.4.7 Focus Visible | AA | The keyboard focus indicator is not visible |
| 2.4.11 Focus Not Obscured (Minimum) | AA | Sticky headers, columns, overlays, or scrolling fully hide the focused component |
| 2.5.3 Label in Name | A | A visible action or filter label is absent from its accessible name |
| 2.5.8 Target Size (Minimum) | AA | Small sort, filter, selection, resize, or row-action targets fail the criterion and no exception applies |
| 3.3.2 Labels or Instructions | A | Filter, edit, selection, or grid-operation inputs lack necessary labels or instructions |
| 4.1.2 Name, Role, Value | A | Table or grid roles, names, values, states, focusability, sort, selection, expansion, or edit state are missing or incorrect |
| 4.1.3 Status Messages | AA | Result, loading, sort, filter, selection, edit, or action outcomes need programmatic status communication without moving focus |

This table is a routing aid, not an automatic checklist. Other criteria may apply when supported by the target and evidence. Do not map a grid arrow-key convention to WCAG 2.1.1 unless the missing behavior prevents keyboard operation or access to functionality; document pattern inconsistency separately when it remains operable.

## Shared finding contract

Every issue finding must contain:

| Field | Requirement |
|---|---|
| `id` | Stable unique identifier |
| `target` | Route, component, table or grid, row or column, state, role, environment, and occurrence as applicable |
| `evidence` | Evidence type, method, reference, environment, and reproducible observation |
| `user_impact` | Affected users, blocked or impaired task, consequence, and workaround |
| `status` | `confirmed`, `provisional`, `needs-validation`, `not-reproduced`, `resolved`, or `accepted-risk` |
| `severity` | `critical`, `high`, `medium`, `low`, or `advisory`, based on user and task impact |
| `confidence` | `high`, `medium`, or `low`, with the reason and missing evidence |
| `framework_mappings` | Zero or more valid WCAG criteria or other requested-framework mappings, each with rationale |
| `recommendation` | Outcome-focused remediation guidance, constraints, and responsible surface |
| `verification` | Retest steps, expected result, method, environment, and evidence required to close |

Allow `source_skill`, `related_ids`, and `root_cause` as optional traceability fields. Treat `accepted-risk` as a documented product decision, not an auditor-selected shortcut.

## Output format

When orchestrated, return findings using the orchestrator's exact structure. For standalone use, return:

```md
## Audit summary

- Target and scope:
- Table models reviewed:
- Standards and assumptions:
- Evidence and environments:
- Screen-reader testing: required | completed | blocked | out of scope
- Overall result and limitations:

## Coverage ledger

| Target | Model | States and tasks | Evidence | Result | Remaining validation |
|---|---|---|---|---|---|

## Confirmed and provisional findings

### DTG-001 — Finding title

- target:
- evidence:
- user_impact:
- status:
- severity:
- confidence:
- framework_mappings:
- recommendation:
- verification:
- source_skill: data-table-grid-accessibility-audit

## Needs validation

[Use the same finding contract. Include exact keyboard, responsive, accessibility-tree, or screen-reader steps and the required environment.]

## Not reproduced

[Use the same finding contract and bind the result to the tested target, data, state, and environment.]

## Manual test record

| Task | Environment | Data and state | Commands | Expected result | Observed result | Evidence reference |
|---|---|---|---|---|---|---|

## WCAG applicability ledger

| Criterion | Applicable | Findings | Rationale or exclusion |
|---|---|---|---|

## Coverage gaps and limitations

- ...

## Recommended remediation order

1. ...
```

If no failure is confirmed, state that no failures were confirmed in the reviewed sample. Do not say the target is fully accessible, WCAG compliant, or conformant.

## Quality bar

The task is complete only when:

- Every in-scope surface is classified as a native table, sortable native table, ARIA table, grid, or treegrid before interaction expectations are applied.
- Captions or names, headers, associations, sort state, keyboard behavior, focus, selection, row and column actions, virtualization, responsive behavior, announcements, and loading and empty states are reviewed or explicitly marked not applicable.
- Static tables are not assigned composite-grid keyboard expectations, and grids are not assessed only as static tables.
- Complex headers and responsive alternatives are evaluated from actual relationships and reading behavior, not visual appearance alone.
- Virtualized content includes logical count, index, focus-retention, recycling, and newly rendered content checks.
- Manual screen-reader testing is explicitly flagged and recorded for representative supported environments.
- Every finding contains the shared contract fields, evidence, user impact, actionable remediation, and reproducible verification.
- WCAG mappings are evidence-specific and separate from APG guidance, specification issues, and usability recommendations.
- Confirmed findings, validation needs, not-reproduced checks, coverage gaps, and observed passes remain distinct.
- The result makes no complete-conformance, certification, or legal-compliance claim.

## Edge cases

- **Layout table:** Confirm whether relationships are genuinely tabular before preserving table semantics; route visual layout and reading-order issues separately.
- **One-column or one-row data:** Do not remove table semantics solely because the structure is small when row-column relationships still aid understanding.
- **Interactive controls in cells:** Keep native table behavior unless a supported composite interaction model is intentionally required.
- **Multiple sort keys:** Supplement `aria-sort` with accessible precedence and direction information; do not invent unsupported ARIA values.
- **Merged or irregular cells:** Test actual header association and reading behavior; a visually plausible layout is insufficient.
- **Expandable rows:** Verify expansion state, control relationship, revealed-content reading order, focus behavior, and whether nested content still belongs in the table model.
- **Sticky or cloned headers:** Check duplicate semantics, IDs, tab stops, names, and focus obscuration.
- **Server-side pagination:** Clarify whether counts, positions, selection, and select-all apply to the page or full result set.
- **Unknown totals:** Do not fabricate row counts. Document what is known and test how loading boundaries are conveyed.
- **Live financial, operational, or monitoring data:** Balance timely announcements against interruption; test batching, pause controls, stale-data cues, and user-selected update frequency where applicable.
- **Mobile screen reader:** Do not assume desktop grid commands transfer to touch exploration. Test the supported mobile combination or disclose the gap.
- **Third-party grid library:** Separate library defaults, product configuration, wrapper behavior, and owned remediation responsibility.
- **Screenshots only:** Review visible purpose, labels, indicators, density, and responsive intent; mark semantics, keyboard, focus, and announcements as not verifiable.
- **Source only:** Report source-confirmed defects and define runtime and screen-reader validation for computed semantics and behavior.

## Related skills

- `inclusive-interface-audit-orchestrator`
- `semantic-structure-accessibility-audit`
- `keyboard-focus-accessibility-audit`
- `dynamic-interface-accessibility-audit`
- `visual-responsive-accessibility-audit`
- `accessibility-validation-planner`
- `wcag-audit-scope-planner`
