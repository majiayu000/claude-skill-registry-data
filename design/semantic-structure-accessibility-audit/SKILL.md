---
name: semantic-structure-accessibility-audit
description: Reviews web pages, templates, and components for evidence-based accessibility issues in semantic HTML and document structure. Use when the user asks to audit headings, landmarks, page titles, document language, lists, tables, labels, relationships, meaningful sequence, reading order, link or button semantics, native elements, ARIA, accessible names, or conflicts between native semantics and ARIA.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: frontend-a11y
  task_type: review
  audience: frontend-developers-and-accessibility-reviewers
  tags:
    - accessibility
    - semantic-html
    - document-structure
    - headings
    - landmarks
    - aria
    - accessible-names
    - wcag
  status: draft
  side_effects: none
---

# Semantic Structure Accessibility Audit

## Purpose

Review semantic HTML and document structure against explicit evidence. Distinguish what the available artifacts prove from what requires rendered-DOM, accessibility-tree, assistive-technology, or human verification, and never turn a source review into a claim of complete accessibility conformance.

## When to use this skill

Use this skill when:

- The user asks for a semantic HTML, document structure, landmark, heading, reading-order, or ARIA audit.
- A page, route, template, component, or generated document needs review for programmatically determinable structure and relationships.
- The task involves page titles, document or passage language, lists, data tables, labels, accessible names, links, buttons, native semantics, or ARIA conflicts.
- An accessibility audit orchestrator routes the semantic-structure portion of a broader review to a specialist.
- The user needs evidence-backed findings rather than implementation changes.

Do not use this skill when:

- The primary task is keyboard behavior, focus management, visual presentation, contrast, responsive layout, form validation, error recovery, or dynamic-widget interaction.
- The user wants a complete accessibility audit or conformance claim from source files alone.
- The task is primarily screen-reader announcement timing, live regions, or state changes after interaction.
- The user asks to implement fixes rather than review and report them.

Route out-of-scope concerns to an available specialist skill. If no specialist is available, record a scoped handoff without expanding this audit.

## Inputs to inspect

Start with the smallest evidence set that can represent the audited surface:

- Page shells and route templates containing `<html>`, `<head>`, `<title>`, and primary content.
- HTML, JSX, TSX, Vue, Svelte, Astro, or other templates that produce headings, landmarks, lists, tables, labels, links, buttons, and ARIA.
- Reusable primitives or design-system components that wrap native elements or compute roles, labels, IDs, and relationships.
- Content data, localization files, or CMS mappings that supply titles, headings, link text, button text, labels, and language changes.
- Routing or metadata code that sets document titles and document language.
- CSS only where it can change content exposure or meaningful order, such as `display`, generated content, flex or grid reordering, visually hidden patterns, or visibility rules.
- JavaScript only where it creates, removes, replaces, hides, labels, or reorders semantic content.
- Rendered DOM snapshots, accessibility-tree output, validator results, screenshots, or manual-test notes when supplied.
- The requested WCAG version, conformance level, audited routes or states, and supported technology assumptions.

Treat screenshots as contextual evidence, not proof of programmatic semantics. Treat source as incomplete when runtime composition, conditional rendering, shadow DOM, slots, portals, localization, or third-party content can change the result.

## Scope boundaries

This skill covers:

- Heading presence, labeling, levels, hierarchy, and whether headings describe their sections.
- Landmark presence, nesting, multiplicity, and names where repeated landmarks require distinction.
- Page titles, document language, and language changes within content.
- Native list and table structure, including captions, headers, header associations, and layout-versus-data intent.
- Programmatic labels, group labels, descriptions, and ID-based relationships.
- DOM sequence and reading order when sequence affects meaning.
- Link-versus-button purpose, native interactive semantics, and programmatically determinable names.
- ARIA roles, states, properties, references, allowed usage, redundant semantics, and conflicts with native HTML.
- Accessible-name sources and precedence when evidence permits a reliable computation.

This skill does not test:

- Keyboard commands, tab order, focus visibility, trapping, restoration, or activation behavior.
- Color, contrast, typography, spacing, zoom, reflow, target size, or other visual presentation.
- End-to-end form instructions, validation, errors, recovery, or submission behavior; only semantic labels, groups, names, and relationships are in scope.
- Dynamic-widget keyboard patterns, state transitions, focus changes, or announcements; only the static semantic contract visible in the supplied evidence is in scope.

Do not ignore an out-of-scope risk. Record it under `Specialist handoffs` with the evidence that triggered the handoff and the type of review required.

## Standards baseline

- Default to WCAG 2.2 when the user does not specify another version.
- Use the version and conformance level explicitly requested by the user when provided.
- If the conformance level is unspecified, record it as an open scope decision. Map in-scope observations to their applicable WCAG 2.2 criteria and levels without inventing a conformance target.
- Treat AAA criteria as advisory unless AAA is explicitly in scope.
- Map findings only to criteria supported by the evidence. Common mappings include WCAG 2.2 Success Criteria 1.3.1, 1.3.2, 2.4.1, 2.4.2, 2.4.4, 2.4.6, 2.5.3, 3.1.1, 3.1.2, and 4.1.2.
- Do not cite WCAG 2.2 Success Criterion 4.1.1 Parsing as a current failure; it is obsolete and removed in WCAG 2.2. Map an invalid-markup issue to another applicable criterion only when its accessibility consequence is demonstrated.
- Use current authoritative HTML, ARIA in HTML, WAI-ARIA, HTML accessibility API mapping, and accessible-name computation rules when resolving native and ARIA semantics.
- Separate WCAG failures from semantic quality improvements and authoring best practices. A redundant role, skipped heading level, multiple `<h1>` elements, or non-native widget is not automatically a WCAG failure without an unmet requirement and supporting evidence.

## Evidence and classification rules

Use the shared finding contract from `inclusive-interface-audit-orchestrator`. Every issue finding must contain:

| Field | Requirement |
|---|---|
| `id` | Stable unique identifier |
| `target` | Route, component, flow, state, role, environment, and occurrence as applicable |
| `evidence` | Evidence type, method, reference, environment, and reproducible observation |
| `user_impact` | Affected users, blocked or impaired task, consequence, and workaround |
| `status` | `confirmed`, `provisional`, `needs-validation`, `not-reproduced`, `resolved`, or `accepted-risk` |
| `severity` | `critical`, `high`, `medium`, `low`, or `advisory`, based on user and task impact |
| `confidence` | `high`, `medium`, or `low`, with the reason and missing evidence |
| `framework_mappings` | Zero or more valid WCAG criteria, Universal Design principles, usability heuristics, or Norman concepts, each with rationale |
| `recommendation` | Outcome-focused remediation guidance, constraints, and responsible surface |
| `verification` | Retest steps, expected result, method, environment, and evidence required to close |

Use `source_skill`, `related_ids`, and `root_cause` when useful for traceability. Set `source_skill` to `semantic-structure-accessibility-audit`. Base severity on user impact, task criticality, breadth, workaround quality, persistence, and harm; do not derive severity from WCAG conformance level. Add a WCAG mapping only when the observed issue and evidence support a specific criterion, and leave `framework_mappings` empty for an HTML or ARIA authoring-rule issue that has no supported framework mapping.

The six required result groups are reporting classes, not replacements for the shared `status` field:

| Result group | Shared-contract treatment |
|---|---|
| Confirmed failure | Emit a finding with `status: confirmed`. Use only when evidence proves that an applicable requirement is unmet. |
| Pass | Emit a scoped coverage record, not a finding. Use `status: not-reproduced` only when retesting a previously reported finding that was not reproduced. |
| Probable issue | Emit a finding with `status: provisional`. State the evidence needed to confirm or dismiss it. |
| Manual-test requirement | Emit a test requirement. When it tracks a specific suspected barrier, also emit a finding with `status: needs-validation` and link the two IDs. |
| Not applicable | Emit a scoped coverage record with the reason the triggering condition is absent or out of scope. |
| Unavailable evidence | Emit an evidence-gap record naming the missing artifact. If a concrete suspected barrier remains, link the gap to a `provisional` or `needs-validation` finding. |

Preserve `resolved`, `accepted-risk`, and `not-reproduced` only when updating the lifecycle of an existing finding. `Accepted-risk` requires a documented product decision; an auditor must not assign it unilaterally.

Apply these evidence thresholds:

1. **Confirmed failure**
   - Cite the exact artifact, failed requirement, and user impact.
   - Do not confirm when runtime output, intended meaning, or accessible-name computation remains uncertain.

2. **Pass**
   - State the exact target, check, environment, and evidence.
   - Do not generalize a pass for one heading, route, or relationship into page-level or product-level conformance.

3. **Probable issue**
   - Use when evidence strongly suggests a defect but a missing runtime value, composition path, content state, or intent prevents confirmation.

4. **Manual-test requirement**
   - Use when correct interpretation depends on rendered order, accessibility-tree exposure, browser behavior, assistive technology, human-language judgment, or task context that source cannot settle.
   - Provide the environment, steps, expected result, and evidence to capture.

5. **Not applicable**
   - Use only when the triggering condition is demonstrably absent from the audited scope or the criterion is outside the requested version or level.

6. **Unavailable evidence**
   - Use when the check is applicable or may be applicable but required artifacts cannot be inspected.
   - Do not substitute it for a manual test: use unavailable evidence when an artifact is missing and a manual-test requirement when a human or runtime method must produce the evidence.

## Workflow

1. **Load the coordinating contract.**
   - If `inclusive-interface-audit-orchestrator` is available, read its shared finding contract before reviewing the target.
   - Preserve its identifiers, status labels, severity conventions, framework-mapping rules, and required fields.
   - If it is unavailable, use the mirrored shared contract in this skill and disclose the missing dependency.

2. **Establish the audit baseline.**
   - Record the target routes, components, states, viewport-independent content variants, and languages.
   - Default the WCAG version to 2.2 unless another version is explicit.
   - Record an unspecified conformance level as an open scope decision rather than inventing one.
   - State that the result is a semantic-structure review, not a complete accessibility conformance evaluation.
   - List keyboard, visual, form-behavior, and dynamic-widget testing as out of scope.

3. **Build an evidence map.**
   - Connect each audited route or component to its page shell, templates, semantic primitives, content sources, metadata logic, and relevant CSS or JavaScript.
   - Distinguish author source, generated source, rendered DOM, accessibility tree, tool output, and manual observation.
   - Record missing routes, states, content variants, and runtime artifacts before drawing conclusions.

4. **Inspect document metadata.**
   - Verify that each page or route has a programmatically set, descriptive title in the final document state.
   - Verify the default document language and programmatically marked language changes where applicable.
   - Treat client-side title or language updates as probable or manual-test items unless their final runtime values are evidenced.

5. **Inspect headings and landmarks.**
   - Check whether real heading and landmark semantics represent the content structure.
   - Check heading labels, hierarchy, nesting, and section relationships without treating a skipped level or multiple `<h1>` elements as an automatic failure.
   - Check one primary main-content region, appropriate landmark containment, and distinguishable names for repeated landmark types when needed.
   - Check that ARIA does not suppress, overwrite, duplicate, or misrepresent native structural semantics.

6. **Inspect lists, tables, labels, and relationships.**
   - Verify that content presented as a list uses list semantics and preserves item boundaries.
   - Distinguish data tables from layout tables. For data tables, inspect captions where needed, header cells, row/column scope, and complex header associations.
   - Verify native and ARIA labeling relationships, group names, descriptions, ownership, controls, and referenced IDs.
   - Confirm that every referenced ID exists in the relevant document or shadow-root scope and that duplicate IDs do not make a relationship ambiguous.
   - Route form instructions, validation, and error behavior to a forms specialist.

7. **Inspect meaningful sequence and reading order.**
   - Compare DOM order with the sequence needed to understand the content.
   - Inspect CSS reordering, generated content, hidden content, portals, and scripted insertion only where they may change meaning or accessibility exposure.
   - Confirm a failure only when both the required meaningful sequence and the contradictory programmatic order are evidenced.
   - Otherwise record a probable issue or a manual test with a specific reading-order procedure.

8. **Inspect link, button, and native-element semantics.**
   - Determine whether navigation uses link semantics and actions use button semantics.
   - Check native element behavior implied by the markup, including anchors without `href`, button default types where relevant to semantics, and non-interactive elements given interactive roles.
   - Prefer native HTML where it supplies the required role, state, behavior, and relationships.
   - Treat replacement of a valid, complete ARIA widget with a native element as a best-practice recommendation unless a normative failure is separately proven.
   - Route keyboard activation and interaction-pattern checks to a keyboard specialist.

9. **Inspect ARIA and accessible names.**
   - Validate role values, permitted roles, required states and properties, supported attributes, ownership, and references.
   - Detect roles or names prohibited on the native element, ARIA that conflicts with strong native semantics, and interactive semantics suppressed by `role="none"` or `role="presentation"`.
   - Compute accessible names using the applicable host-language and accessible-name rules, including precedence and name-from-author versus name-from-content behavior.
   - Check for absent, empty, duplicated, misleading, or overridden names; broken `aria-labelledby` references; and visible labels omitted from accessible names when WCAG 2.5.3 applies.
   - Require rendered accessibility-tree or assistive-technology verification when source composition cannot establish the final name, role, or relationship.

10. **Classify and route every check.**
    - Place every check in exactly one of the six required result groups.
    - Assign every issue finding a valid shared-contract status; do not use result-group labels as status values.
    - Keep confirmed failures, probable issues, and best-practice advice distinct.
    - Add specialist handoffs for keyboard behavior, visual presentation, form behavior, and dynamic widgets without reviewing those areas.
    - Record not-applicable and unavailable-evidence results so coverage gaps remain visible.

11. **Check coverage and claims.**
    - Account for every in-scope area in the coverage matrix.
    - Ensure every confirmed failure and pass has precise evidence.
    - Ensure every probable issue states the missing confirmation evidence.
    - Ensure every manual-test requirement includes steps and an expected result.
    - Use wording such as “no confirmed failures were found in the reviewed evidence,” never “fully accessible,” “WCAG compliant,” or “complete conformance,” unless a separate complete conformance evaluation supports that claim.

## Output format

Return the review using this structure:

```md
## Audit scope

- Target: ...
- Evidence reviewed: ...
- Evidence unavailable: ...
- Standard version: WCAG 2.2
- Conformance level: [requested value or not specified]
- Out of scope: keyboard behavior; visual presentation; form behavior beyond semantic labels and relationships; dynamic-widget interaction
- Conformance limitation: This source-focused semantic review does not establish complete accessibility conformance.

## Result summary

| Result group | Count |
|---|---:|
| Confirmed failure | 0 |
| Pass | 0 |
| Probable issue | 0 |
| Manual-test requirement | 0 |
| Not applicable | 0 |
| Unavailable evidence | 0 |

## Confirmed failures

| ID | Target | Evidence | User impact | Status | Severity | Confidence | Framework mappings | Recommendation | Verification | Root cause | Related IDs |
|---|---|---|---|---|---|---|---|---|---|---|---|

## Passes

| ID | Area | Target | Requirement | Evidence and environment | Coverage boundary | Confidence |
|---|---|---|---|---|---|---|

## Probable issues

| ID | Target | Evidence | User impact | Status | Severity | Confidence | Framework mappings | Recommendation | Verification | Root cause | Related IDs |
|---|---|---|---|---|---|---|---|---|---|---|---|

## Manual-test requirements

### Needs-validation findings

| ID | Target | Evidence | User impact | Status | Severity | Confidence | Framework mappings | Recommendation | Verification | Root cause | Related IDs |
|---|---|---|---|---|---|---|---|---|---|---|---|

### Coverage-only manual tests

| ID | Area | Target and environment | Evidence gap | Test procedure | Expected result | Evidence to capture | Related finding IDs |
|---|---|---|---|---|---|---|---|

## Not-applicable checks

| ID | Area | Requirement | Scope | Reason |
|---|---|---|---|---|

## Unavailable evidence

| ID | Area | Target | Missing evidence | Why it matters | How to obtain it | Related finding IDs |
|---|---|---|---|---|---|---|

## Coverage matrix

| Area | Result IDs | Evidence level | Coverage note |
|---|---|---|---|
| Page title and language | ... | ... | ... |
| Headings and landmarks | ... | ... | ... |
| Lists and tables | ... | ... | ... |
| Labels and relationships | ... | ... | ... |
| Meaningful sequence and reading order | ... | ... | ... |
| Links, buttons, and native elements | ... | ... | ... |
| ARIA and accessible names | ... | ... | ... |
| Native and ARIA conflicts | ... | ... | ... |

## Specialist handoffs

| ID | Route | Triggering evidence | Requested specialist check |
|---|---|---|---|

## Conclusion

- Highest-impact confirmed failures: ...
- Evidence gaps that limit confidence: ...
- Required retests and handoffs: ...
- Claim boundary: ...
```

Omit no result-group section. Write `None` when a section has no results so the distinction between zero findings and unreviewed evidence remains explicit.

## Quality bar

The task is complete only when:

- The requested WCAG version and level are explicit; WCAG 2.2 is the default version and an unspecified level remains an open scope decision.
- Headings, landmarks, page titles, document language, lists, tables, labels, relationships, meaningful sequence, reading order, link and button semantics, native elements, ARIA, accessible names, and native-ARIA conflicts are each accounted for.
- Every check appears in exactly one required result group, and every issue finding uses the orchestrator's exact shared fields and status values.
- Confirmed failures and passes cite precise, reviewable evidence rather than assumptions.
- Probable issues, manual tests, not-applicable checks, and unavailable evidence remain separate.
- WCAG failures are separated from specification violations, authoring best practices, and advisory improvements.
- Out-of-scope keyboard, visual, form-behavior, and dynamic-widget concerns are routed rather than silently dropped or audited here.
- The conclusion states the evidence and conformance limits and does not claim complete conformance from source review alone.
- No product files or external systems are changed.

## Edge cases

- **Framework abstraction:** Trace props, slots, spreads, and wrapper components to final semantics. Use `Unavailable evidence` when the final expansion cannot be established.
- **Client-side routes:** Review route-specific titles, language, main headings, and landmark structure. Require runtime verification for post-navigation output when source does not prove the final state.
- **Shadow DOM or portals:** Verify relationship scope and final accessibility-tree exposure; do not assume ordinary document ID resolution applies.
- **Conditional or localized content:** Review representative variants and record uninspected variants as unavailable evidence, not passes.
- **CSS visual reordering:** A difference between visual and DOM order is not automatically a failure. Determine whether the programmatic sequence changes meaning and require manual testing when intent is unclear.
- **Heading conventions:** Skipped levels or multiple `<h1>` elements require contextual review; do not report them as automatic WCAG failures.
- **Repeated landmarks:** Repeated landmark types may need names that distinguish their purpose. Judge the exposed structure, not the raw element count alone.
- **ARIA on native HTML:** Redundant ARIA is usually a quality issue; conflicting, prohibited, or misleading ARIA may be a confirmed failure when the final semantics are evidenced.
- **Custom interactive elements:** Review static name, role, state, and relationships here. Route activation keys, navigation patterns, focus, and state changes to keyboard or widget specialists.
- **Third-party embeds:** Review the integration boundary and accessible name of the embedding element. Mark inaccessible third-party internals as unavailable evidence unless they can be inspected.
- **No runtime evidence:** Report what source proves, downgrade uncertain conclusions, and add targeted manual-test requirements. Do not convert missing runtime evidence into a blanket failure.

## Related skills

- `inclusive-interface-audit-orchestrator`
- `accessibility-validation-planner`
- `progressive-enhancement-planner`
- `interface-state-coverage-review`
