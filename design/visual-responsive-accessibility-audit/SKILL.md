---
name: visual-responsive-accessibility-audit
description: Audits the visual presentation and responsive behavior of web interfaces for accessibility barriers. Use when a user asks to review screenshots, pages, components, or flows for text and non-text contrast, color-only communication, text resize, browser zoom, reflow, orientation, text spacing, hover or focus content, focus visibility or obscuring, target size, responsive order, clipping, overlap, horizontal scrolling, forced colors, or high-contrast behavior, with evidence-aware WCAG 2.2 mapping.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access and can use screenshots, source files, or a running browser when available.
metadata:
  category: frontend-a11y
  task_type: review
  audience: accessibility-auditors-frontend-developers-and-qa-teams
  tags:
    - accessibility
    - wcag
    - visual-accessibility
    - responsive-design
    - contrast
    - zoom
    - reflow
    - focus-visibility
    - target-size
    - forced-colors
  status: draft
  side_effects: none
---

# Visual Responsive Accessibility Audit

## Purpose

Audit an implemented or represented web interface for accessibility barriers in visual presentation and responsive behavior. Separate what screenshots can establish from what requires source inspection, a running browser, interaction, or measurement. Map supported findings to applicable WCAG 2.2 criteria without turning design preferences, incomplete evidence, or a sampled review into accessibility failures or a conformance claim.

This is a review-only skill. Do not modify product files, install tools, or mutate external systems.

## When to use this skill

Use this skill when:

- The user asks for a visual accessibility, responsive accessibility, zoom, reflow, contrast, or target-size audit.
- Screenshots, designs, source files, a component story, or a running page need evidence-aware accessibility review.
- The task covers text or non-text contrast, non-color cues, text resize, browser zoom, orientation, text spacing, hover or focus content, focus presentation, responsive order, overflow, or high-contrast modes.
- A broader inclusive-interface audit needs a specialist visual and responsive workstream that follows the shared finding contract.
- The user wants findings and verification guidance rather than implementation changes.

Do not use this skill when:

- The request is a complete accessibility audit; route semantics, forms, keyboard behavior, screen-reader output, media, motion, and cognitive concerns to appropriate specialist reviews.
- The user only wants aesthetic critique, art direction, responsive design planning, or subjective visual polish.
- The task asks for legal advice, certification, or a WCAG conformance declaration.
- The user asks to implement fixes. Perform this review first, then use a change-oriented skill only under a separate implementation scope.
- The available evidence cannot show the target at all. Request the smallest useful artifact instead of returning a generic checklist as audit findings.

## Scope boundaries and coordination

Keep the primary audit limited to visual presentation and responsive behavior.

- In standalone use, include focus visibility and focus obscuring because both have visual and layout-dependent requirements.
- When `keyboard-focus-accessibility-audit` is also assigned, let that specialist own keyboard reachability, order, management, trapping, and the primary focus-behavior finding. Contribute responsive, zoom, sticky-layout, contrast, and measurement evidence to the same shared finding, or agree on one owner based on root cause.
- Route document structure, programmatic relationships, and accessible-name issues to a semantic specialist unless they are needed only to explain a responsive-order finding.
- Route screen-reader output, announcements, keyboard widget patterns, motion, media alternatives, and cognitive or content concerns to their applicable specialists.
- Route aesthetic composition and responsive design planning without an evidenced accessibility barrier to the relevant UI/UX skill.
- Deduplicate cross-specialist findings by target behavior, root cause, user impact, remediation, and verification method.

## Inputs to inspect

Start with the smallest relevant set:

- Audit target, routes, components, tasks, states, breakpoints, themes, locales, roles, and exclusions.
- Required accessibility standard and conformance level. If none is supplied, state that WCAG 2.2 Level A and AA are the working mapping baseline, not an agreed conformance target.
- Screenshots or recordings with viewport size, browser zoom, device pixel ratio, theme, state, and capture date when known.
- A running page, component explorer, preview build, or local fixture when runtime testing is permitted.
- HTML, templates, components, CSS, SVG, design tokens, media queries, container queries, responsive utilities, and tests relevant to the target.
- Browser, operating-system, device, input, orientation, forced-colors, and high-contrast support expectations.
- Existing audit reports, known defects, exception decisions, and design-system requirements.

Record missing inputs and the claims they prevent. Do not infer runtime behavior, dimensions, computed colors, DOM order, or platform-mode behavior from an unlabeled screenshot.

## Evidence rules

Classify every piece of evidence before drawing a conclusion:

| Evidence type | What it can support | Main limitation |
|---|---|---|
| `screenshot` | Visible clipping, overlap, truncation, apparent order, captured focus state, visible non-color cues, and other facts in that exact image | Does not establish interaction behavior, DOM or focus order, CSS-pixel dimensions, computed contrast, hidden states, zoom response, or behavior outside the captured viewport |
| `source` | Authored colors, layout constraints, media rules, ordering, focus styles, orientation locks, forced-colors rules, and test intent | Does not prove the computed or interactive result in a supported browser |
| `runtime` | Reproducible behavior in a named browser, viewport, state, input method, zoom level, orientation, or platform mode | Applies only to the tested environment and occurrence |
| `measurement` | Contrast ratios, CSS-pixel target dimensions, viewport dimensions, focus-indicator metrics, and other quantified results | Requires a named method, relevant states, and correct handling of exceptions |
| `coverage-gap` | A test or environment that remains unavailable | Supports no pass or failure conclusion |

Use these rules:

- A screenshot may confirm a visible symptom in its captured state. It does not confirm that a WCAG threshold failed when that conclusion requires interaction, computed styles, CSS-pixel dimensions, or measurement.
- Label an apparent low-contrast pairing as `provisional` until measured. Do not estimate a ratio by eye.
- Label untested zoom, reflow, text-spacing, hover, focus, orientation, target-size, responsive-order, and forced-colors behavior `needs-validation`.
- Use `confirmed` only when the observation is reproducible and the evidence is sufficient for the claim.
- Keep `severity`, `confidence`, `status`, and WCAG conformance level separate.
- Do not convert “not tested,” “not visible,” or “not reproduced” into “pass.”

## Workflow

1. **Define scope and evidence boundaries.**
   - Record the target, critical tasks, states, viewports, themes, locales, environments, standards baseline, and exclusions.
   - Inventory the supplied evidence by type and identify required runtime or measurement access.
   - State whether the review is exhaustive or sampled. Never generalize a sampled result to untested surfaces.

2. **Inventory visual and responsive states.**
   - Include default, hover, focus, active, selected, disabled, expanded, validation, error, success, loading, sticky, overlay, and modal states when relevant.
   - Include narrow and wide viewports, intermediate widths near content-driven layout changes, portrait and landscape, increased text, zoom, forced colors, and supported themes.
   - Test content stressors such as long words, long labels, translated text, large values, validation messages, dense tables, and user-generated content when they are in scope.

3. **Triage screenshot observations.**
   - Record only visible facts tied to an image, viewport, theme, and state.
   - Note apparent contrast risks, color-only cues, clipping, overlap, truncation, unexpected visual order, visible scrollbars, small-looking controls, and captured focus treatment.
   - Move every claim that requires interaction or a threshold into runtime or measurement follow-up.
   - Do not treat density, font taste, whitespace, alignment, brand color choice, or aesthetic hierarchy as an accessibility failure without an evidenced barrier or applicable requirement.

4. **Test text and non-text contrast.**
   - Measure rendered foreground and adjacent background colors for normal text, large text, placeholder text when it conveys information, links, errors, icons, control boundaries, selected states, chart marks, and author-styled focus indicators.
   - Check every materially different state and background, including gradients, images, overlays, translucency, themes, and disabled styling when the component is not exempt as inactive.
   - Apply the WCAG 2.2 Level AA thresholds: at least 4.5:1 for normal text, 3:1 for large-scale text, and 3:1 for visual information required to identify active controls, states, or meaningful graphics.
   - Record the measured ratio, sampled colors, text size and weight when relevant, state, adjacent color, method, and any applicable exception.
   - Review images of text under 1.4.5 when authored text could provide the same presentation. Do not mistake logos or essential presentations for automatic failures.

5. **Test color-independent communication.**
   - Inspect errors, status, required fields, selection, links within text, chart series, badges, availability, and interactive states.
   - Verify that color is not the only visual means of conveying information, action, response, or distinction.
   - Accept text, shape, pattern, iconography with an understandable meaning, underline, position plus explicit labeling, or another perceptible visual cue when it conveys equivalent information.
   - Do not claim that an accessible name alone satisfies a visual non-color requirement; 1.4.1 concerns visual perception. Map sensory-only instructions to 1.3.3 only when the evidence supports that separate issue.

6. **Test text resize, browser zoom, and reflow separately.**
   - Test text resize up to 200% without loss of content or functionality for WCAG 2.2 1.4.4.
   - Exercise browser zoom at representative intermediate levels and the reflow threshold. For vertically scrolling content, test at a width equivalent to 320 CSS pixels; a 1280 CSS-pixel-wide starting viewport at 400% zoom is one equivalent setup.
   - Record both zoom percentage and resulting CSS viewport dimensions. Browser zoom is a test method, not a standalone WCAG criterion.
   - At each step, inspect clipped or overlapping text, hidden controls, truncated instructions, inaccessible off-screen content, sticky-region collisions, and horizontal scrolling.
   - Under 1.4.10, allow two-dimensional scrolling for content that genuinely requires a two-dimensional layout for usage or meaning, such as some maps, diagrams, data tables, and tool-based interfaces. Limit the exception to that content, not the whole page.

7. **Test responsive adaptation, orientation, and order.**
   - Rotate or emulate portrait and landscape and complete relevant operations in both. Treat a single-orientation restriction as a failure only when that orientation is not essential.
   - Resize continuously enough to catch failures between named breakpoints.
   - Compare visual order with DOM reading order and keyboard focus order when sequence affects meaning or operation.
   - Use 1.3.2 for a programmatically determinable reading-sequence failure and 2.4.3 for a focus-order failure. A visually rearranged layout is not a failure by itself when meaning and operability remain intact.
   - Check that responsive hiding, duplication, reparenting, and off-canvas patterns do not remove necessary information or create conflicting occurrences.

8. **Test text spacing overrides.**
   - Apply, without changing other style properties, line height of at least 1.5 times the font size, paragraph spacing of at least 2 times the font size, letter spacing of at least 0.12 times the font size, and word spacing of at least 0.16 times the font size.
   - Check for clipped, overlapped, truncated, hidden, or functionally unusable content.
   - Account for languages and scripts that do not use one or more of these properties.
   - Do not report that the authored design must use these values; 1.4.12 tests whether user overrides cause loss.

9. **Test content shown on hover or focus.**
   - Exercise custom tooltips, submenus, previews, validation help, and other author-controlled additional content with both pointer hover and keyboard focus where applicable.
   - Verify that applicable content is dismissible without moving hover or focus, hoverable when pointer-triggered, and persistent until the trigger is removed, the user dismisses it, or the information becomes invalid.
   - Test at zoomed and narrow layouts where additional content is more likely to cover other content.
   - Do not apply 1.4.13 to unmodified user-agent presentation or to content that does not meet the criterion's trigger conditions.

10. **Test focus visibility and obscuring.**
    - Navigate the running interface with a keyboard through every relevant control and state.
    - Confirm a visible focus indicator exists in a mode of operation covered by 2.4.7. Measure author-styled indicator contrast under 1.4.11 when applicable.
    - Check focus against sticky headers, sticky footers, cookie notices, drawers, popovers, dialogs, virtual keyboards, and scroll containers at default and zoomed layouts.
    - Map a component entirely hidden by author-created content to 2.4.11. Evaluate the stricter 2.4.12 and focus-indicator size and contrast requirements in 2.4.13 only when Level AAA is in scope.
    - A screenshot of a captured focus state can support that occurrence, but it cannot establish keyboard reachability, the full focus sequence, or all obscuring conditions.

11. **Measure pointer target size.**
    - Measure the actual clickable or tappable target in CSS pixels, not only the visible icon or glyph.
    - Test compact and responsive states separately because hit areas and spacing may change.
    - Evaluate WCAG 2.2 2.5.8 against the 24 by 24 CSS-pixel minimum and its spacing, equivalent-control, inline, user-agent-control, and essential-presentation exceptions.
    - Evaluate 2.5.5's 44 by 44 CSS-pixel target only when Level AAA is in scope.
    - Record dimensions, adjacent targets, spacing or exception geometry, input context, state, and measurement method.

12. **Test forced colors and high-contrast modes where relevant.**
    - Use a supported browser and operating-system mode rather than simulating the result from a normal-mode screenshot.
    - Check text, icons, control boundaries, selected and invalid states, custom focus indicators, links, charts, background images, and content revealed by hover or focus.
    - Inspect whether author colors are replaced, whether system colors or forced-color adjustments preserve meaning, and whether transparent borders or background-only cues disappear.
    - Treat forced colors or high contrast as a test environment, not a standalone WCAG success criterion. Map only the evidenced underlying barrier, such as color-only meaning, missing required non-text contrast, or invisible keyboard focus.
    - If the platform mode is unavailable, record a coverage gap rather than a pass.

13. **Normalize, map, and prioritize findings.**
    - Use the shared finding contract below for every confirmed or provisional finding.
    - Base severity on user impact, task criticality, breadth, workaround quality, persistence, and harm. Never derive severity from Level A, AA, or AAA.
    - Add a WCAG mapping only when the observed behavior and evidence satisfy the mapping rationale. Otherwise leave `framework_mappings` empty and name the candidate criterion in `verification`.
    - Merge repeated occurrences with the same behavior, root cause, impact, and remediation; preserve affected targets and states. Keep separate issues when causes, fixes, or retests differ.
    - Report strengths or passes only for explicitly tested targets, states, methods, and environments.

14. **Close with coverage and verification limits.**
    - List untested viewports, states, themes, locales, orientations, zoom levels, platform modes, and environments.
    - Separate confirmed findings, provisional findings, needs-validation items, not-reproduced items, and coverage gaps.
    - State that the result is a bounded technical audit, not legal advice, certification, or proof of whole-product WCAG conformance.

## WCAG 2.2 mapping guide

Use this as a routing guide, not as a substitute for criterion-specific evidence:

| Audit concern | Common applicable WCAG 2.2 criteria |
|---|---|
| Color-only meaning or sensory-only instructions | 1.4.1 Use of Color (A); 1.3.3 Sensory Characteristics (A) when separately supported |
| Text contrast and images of text | 1.4.3 Contrast (Minimum) (AA); 1.4.5 Images of Text (AA); 1.4.6 Contrast (Enhanced) (AAA) and 1.4.9 Images of Text (No Exception) (AAA) only when in scope |
| Additional block-of-text presentation requirements | 1.4.8 Visual Presentation (AAA) only when in scope; do not use it to label general layout preferences |
| Control, state, graphic, or applicable focus-indicator contrast | 1.4.11 Non-text Contrast (AA) |
| Text resize | 1.4.4 Resize Text (AA) |
| Reflow, clipping, overlap, or two-dimensional scrolling at the criterion threshold | 1.4.10 Reflow (AA) |
| Orientation restriction | 1.3.4 Orientation (AA) |
| Responsive reading or focus order | 1.3.2 Meaningful Sequence (A); 2.4.3 Focus Order (A) |
| User text-spacing overrides | 1.4.12 Text Spacing (AA) |
| Additional content triggered by hover or focus | 1.4.13 Content on Hover or Focus (AA) |
| Visible or obscured keyboard focus | 2.4.7 Focus Visible (AA); 2.4.11 Focus Not Obscured (Minimum) (AA); 2.4.12 Focus Not Obscured (Enhanced) (AAA) and 2.4.13 Focus Appearance (AAA) only when in scope |
| Pointer target size | 2.5.8 Target Size (Minimum) (AA); 2.5.5 Target Size (Enhanced) (AAA) only when in scope |
| Forced-colors or high-contrast failure | No criterion solely for the mode; map the supported underlying barrier |

Clipping, overlap, truncation, horizontal scrolling, browser zoom, forced colors, and high-contrast modes are observations or test conditions, not automatic WCAG mappings. Connect them to a criterion only after checking its scope, threshold, exceptions, and user impact.

## Shared finding contract

Include every required field:

| Field | Requirement |
|---|---|
| `id` | Stable unique identifier, using `VR-A11Y-###` when no project convention exists |
| `target` | Route, component, flow, state, role, environment, and occurrence as applicable |
| `evidence` | Evidence type, method, reference, environment, and reproducible observation |
| `user_impact` | Affected users, blocked or impaired task, consequence, and workaround |
| `status` | `confirmed`, `provisional`, `needs-validation`, `not-reproduced`, `resolved`, or `accepted-risk` |
| `severity` | `critical`, `high`, `medium`, `low`, or `advisory`, based on user and task impact |
| `confidence` | `high`, `medium`, or `low`, with the reason and missing evidence |
| `framework_mappings` | Zero or more valid WCAG criteria or other requested framework mappings, each with rationale |
| `recommendation` | Outcome-focused remediation guidance, constraints, and responsible surface |
| `verification` | Retest steps, expected result, method, environment, and evidence required to close |

Optional traceability fields are `source_skill`, `related_ids`, and `root_cause`. Use `source_skill: visual-responsive-accessibility-audit` when an orchestrator will combine specialist results. Treat `accepted-risk` as a documented product decision, never an auditor's unilateral conclusion.

## Output format

Return the audit using this structure:

```md
## Audit summary

- Target and scope:
- Evidence reviewed:
- Standards baseline:
- Tested environments and states:
- Overall result:
- Conformance disclaimer:

## Evidence ledger

| Evidence ID | Type | Target and state | Environment or dimensions | Supports | Limitation |
|---|---|---|---|---|---|

## Findings

### VR-A11Y-001 — Concise finding title

- target:
- evidence:
- user_impact:
- status:
- severity:
- confidence:
- framework_mappings:
- recommendation:
- verification:
- source_skill: visual-responsive-accessibility-audit
- related_ids: optional
- root_cause: optional

## Screenshot observations requiring runtime or measurement

| Observation | Screenshot evidence | Why it is not yet a confirmed failure | Required test or measurement | Candidate criterion, if any |
|---|---|---|---|---|

## Tested passes

| Area | Target, state, and environment | Method | Result boundary |
|---|---|---|---|

## Coverage gaps and remaining validation

| Area | Status | Missing evidence or environment | Claim prevented | Next step |
|---|---|---|---|---|
```

Omit empty optional fields and sections, but always include the audit summary, findings or an explicit no-confirmed-findings statement, screenshot/runtime distinction, and coverage gaps. Do not return a generic compliance score.

## Quality bar

The task is complete only when:

- Scope, standards baseline, supplied evidence, tested environments, states, and limitations are explicit.
- Text and non-text contrast, color-independent communication, text resize, browser zoom, reflow, orientation, text spacing, hover or focus content, focus visibility and obscuring, target size, responsive order, clipping, overlap, horizontal scrolling, and relevant forced-colors or high-contrast behavior are tested or marked not applicable or not validated with a reason.
- Screenshot observations are separated from findings that require runtime behavior or measurement.
- Each confirmed failure has reproducible evidence sufficient for its claim.
- Contrast ratios, CSS-pixel dimensions, viewport sizes, zoom levels, states, and applicable exceptions are recorded when relevant.
- Every finding follows the shared contract, and severity, confidence, status, and framework mappings remain distinct.
- WCAG 2.2 mappings include criterion number, name, level, and a finding-specific rationale.
- Level AAA criteria are applied only when the audit target includes them or the result clearly labels them as advisory.
- Subjective visual preferences are not reported as accessibility failures.
- Forced-colors and high-contrast checks are not misrepresented as their own WCAG criteria.
- Untested and not-reproduced areas are not reported as passes.
- The final result makes no legal, certification, or whole-product conformance claim.
- No product files or external systems are changed.

## Edge cases

- **Screenshots only:** Confirm visible facts only. Put contrast thresholds, target dimensions, focus sequences, hover behavior, zoom, reflow, orientation, responsive DOM order, and platform modes into required validation unless reliable measurement metadata is supplied.
- **Source only:** Report source-supported risks as provisional and identify the running-browser result needed for confirmation.
- **Prototype or design file:** Review specified presentation and responsive intent, but do not claim production behavior, DOM order, input behavior, or platform-mode support.
- **Unlabeled screenshot:** Record the missing viewport, scale, zoom, theme, and state metadata and avoid CSS-pixel or whole-layout conclusions.
- **Two-dimensional content:** Evaluate the reflow exception at the smallest component boundary that requires two-dimensional layout; do not exempt surrounding navigation, instructions, or controls.
- **Data visualization:** Review meaningful graphical contrast and non-color encodings, then route text alternatives, data access, and interaction semantics to appropriate specialist audits.
- **Native or unmodified user-agent control:** Check the relevant WCAG exception before treating author-independent appearance or target size as a failure.
- **Target-size exception:** Document the exact exception and supporting geometry or equivalent control. “Looks close enough” is not evidence.
- **Multiple themes or brands:** Test each materially different token combination or record untested themes as coverage gaps.
- **Localization:** Test content expansion and relevant writing systems; do not apply Latin-script spacing assumptions where the properties do not exist.
- **Forced colors unavailable:** Inspect source for risks if useful, but keep runtime behavior `needs-validation`.
- **Third-party content:** Report the user-facing barrier and ownership boundary separately; do not erase the finding because remediation depends on a vendor.

## Related skills

- `inclusive-interface-audit-orchestrator`
- `wcag-audit-scope-planner`
- `accessibility-validation-planner`
- `keyboard-focus-accessibility-audit`
