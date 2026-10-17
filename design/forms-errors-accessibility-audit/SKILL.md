---
name: forms-errors-accessibility-audit
description: Audits web forms and error handling for accessible labels, instructions, required and invalid states, field groups, autocomplete, validation, submission feedback, status announcements, and recovery. Use when the user asks for a forms accessibility audit, validation or error-message review, accessible form QA, failed-submission assessment, or WCAG 2.2 mapping for forms without requesting implementation changes.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: frontend-a11y
  task_type: review
  audience: frontend-developers-accessibility-reviewers-and-qa-teams
  tags:
    - accessibility
    - forms
    - validation
    - error-handling
    - screen-reader
    - keyboard
    - autocomplete
    - recovery
    - wcag
  status: draft
  side_effects: none
---

# Forms and Errors Accessibility Audit

## Purpose

Audit forms as complete user journeys, from understanding each field through validation, submission, failure, and recovery. Produce evidence-backed findings, isolate behavior that still requires manual testing, and map relevant WCAG 2.2 criteria without claiming full conformance.

## When to use this skill

Use this skill when:

- The user asks for a forms accessibility audit, accessible validation review, or form error-handling assessment.
- A sign-up, sign-in, checkout, search, contact, settings, upload, survey, or multi-step form needs review.
- The task involves labels, instructions, required fields, field groups, input purpose, autocomplete, inline errors, error summaries, async validation, submission status, or recovery.
- The user wants confirmed code or runtime findings separated from keyboard, screen-reader, browser, or network checks that have not been performed.
- The user wants likely WCAG 2.2 mappings for form-specific issues rather than a conformance claim.

Do not use this skill when:

- The user wants implementation changes rather than a review; route the findings to an implementation-capable accessibility skill after the audit.
- The request is only for general form copywriting with no accessibility assessment.
- The task is a legal opinion or accessibility certification.
- The interface has no user-input, validation, or submission behavior in scope.

## Inputs to inspect

Start with the smallest relevant set:

- Form templates, pages, components, routes, and design-system field primitives.
- Rendered HTML or an accessibility-tree snapshot for every form state available.
- Validation schemas, client-side validation handlers, and server-error adapters.
- Submission handlers, request state, retry logic, duplicate-submission controls, and success handling.
- CSS affecting label visibility, error styling, focus, disabled states, order, or hidden content.
- Tests, stories, fixtures, screenshots, recordings, defect reports, and accessibility-tool output.
- Product requirements for required fields, supported formats, sensitive values, authentication, legal or financial transactions, and multi-step flows.
- The supported browser, device, keyboard, and assistive-technology matrix when one exists.

If only code, screenshots, or a design brief is available, audit what that evidence can establish and move all unverified behavior into manual-test requirements.

## Audit rules

- Keep the task review-only. Do not edit product files, submit real forms, create accounts, or send data unless the user separately authorizes those actions.
- Prefer native HTML form semantics. Evaluate ARIA as a supplement, not as a replacement for correct native labels, grouping, states, and controls.
- Treat a source-code issue, rendered-DOM defect, reproducible behavior, or test result as confirmed only when the evidence directly establishes it.
- Treat expected screen-reader announcements, focus behavior not exercised, browser-native validation differences, race conditions, and network recovery as manual-test requirements until tested.
- Do not convert a plausible risk into a confirmed finding. Do not hide a directly observable defect in the manual-test list.
- Cite file and line, component, rendered element, test, screenshot, or reproduction step for every confirmed finding.
- Map only criteria supported by the issue and evidence. Use wording such as “maps to,” “likely affects,” or “requires verification against.”
- When invoked by `inclusive-interface-audit-orchestrator`, use its shared finding contract and allowed values exactly.
- Never describe a partial audit, automated scan, or single assistive-technology pass as proof of full WCAG 2.2 conformance.

## Workflow

1. **Define scope and critical tasks.**
   - List each form, step, entry point, and completion outcome in scope.
   - Identify critical paths, sensitive data, irreversible actions, legal or financial commitments, authentication, time limits, and third-party controls.
   - Record available evidence, test environments, unsupported platforms, and explicit exclusions.

2. **Build a form-state inventory.**
   - Cover initial, focused, filled, valid, invalid, disabled, and read-only field states as applicable.
   - Cover client-validation failure, server-validation failure, submitting, delayed response, success, network failure, server failure, session expiry, retry, and uncertain submission outcome.
   - Include empty, partially completed, autofilled, restored, and multi-step return states.
   - Mark unavailable states as manual-test requirements instead of assuming their behavior.

3. **Audit labels and accessible names.**
   - Verify that every input, select, textarea, button, and custom control has an accurate programmatic name.
   - Verify explicit or implicit label association and unique identifiers where HTML labels are used.
   - Confirm that visible labels remain available and that placeholders are not the only labels or instructions.
   - Compare visible labels with accessible names, especially for speech-input compatibility and icon-only controls.
   - Check repeated fields, dynamically added rows, composite inputs, upload controls, search fields, and submit buttons for unique, task-specific names.
   - Flag hidden, duplicated, empty, misleading, or state-dependent names.

4. **Audit descriptions, instructions, and field groups.**
   - Verify that required formats, constraints, units, examples, password rules, and consequences are available before users need them.
   - Confirm that persistent instructions are visible and programmatically associated where the relationship matters.
   - Check that help revealed on focus or request remains keyboard-accessible, dismissible when necessary, and available long enough to use.
   - Verify `fieldset` and `legend`, native group semantics, or equivalent programmatic grouping for related radio buttons, checkboxes, dates, addresses, names, and repeated question sets.
   - Confirm that instructions do not rely only on color, position, shape, or sensory wording.
   - Check whether dynamically inserted descriptions or errors update their association with the correct field.

5. **Audit required, invalid, and input-purpose states.**
   - Verify that required status is communicated visibly and programmatically, with any symbol convention explained.
   - Confirm that optional and required conventions are consistent and do not depend on color alone.
   - Verify that invalid state is exposed when a field is actually invalid and is cleared when corrected.
   - Check that `aria-invalid`, native constraint validation, and custom validity state agree with the visible message.
   - Verify suitable HTML input types, `autocomplete` tokens, and input-purpose metadata for fields that collect information about the user.
   - Distinguish input purpose from input mechanics: `type`, `inputmode`, and `autocomplete` solve different problems.
   - Check that autocomplete is not disabled without a documented, user-centered reason.

6. **Audit error identification and correction.**
   - Verify that every detected error identifies the affected field and describes the problem in text.
   - Confirm that known correction guidance is specific, actionable, and presented without exposing sensitive information.
   - Check inline errors for visual proximity and programmatic association with their fields.
   - Check error summaries for an informative heading, a useful count or overview when appropriate, and links or controls that move focus to the affected fields.
   - Verify that error styling does not rely on color, icons, or border treatment alone.
   - Check that client and server validation use compatible field identifiers, wording, and correction paths.
   - Prevent stale, duplicate, contradictory, or premature error messages.

7. **Audit validation timing.**
   - Identify whether validation occurs on input, blur, step change, or submission and whether the timing matches the task.
   - Flag errors shown before a user has had a reasonable chance to complete a field.
   - Verify that real-time validation does not announce on every keystroke, interrupt typing, unexpectedly move focus, or create an unmanageable stream of updates.
   - Confirm that errors update or clear predictably after correction without hiding unresolved problems.
   - Check that changing a value does not cause an unexpected context change or submission.
   - Verify that native browser validation has been assessed in the supported browser matrix when it is relied upon.

8. **Audit keyboard and screen-reader behavior.**
   - Verify or require a manual test that the form can be understood, completed, reviewed, submitted, corrected, and retried with keyboard alone.
   - Check logical focus order, visible focus, Enter and Space behavior, group navigation, custom widgets, and focus visibility when sticky content or virtual keyboards are present.
   - Verify or require a manual test for how focus moves after invalid submission, step changes, success, and recoverable failure.
   - Confirm that names, descriptions, required state, invalid state, group context, errors, and button state are exposed through the accessibility API.
   - Verify dynamic error, loading, success, and failure announcements with representative supported screen-reader and browser combinations.
   - Avoid duplicate output from simultaneous focus movement, inline descriptions, error summaries, alerts, and live regions.
   - Judge equivalent access to information, not identical wording across screen readers.

9. **Audit failed-submission recovery and value preservation.**
   - Verify that failed submission explains what happened, whether data was received, and what the user can do next.
   - Confirm that user-entered values are preserved after validation, network, and server failures unless retaining a sensitive value would create a security risk.
   - Check that preserved values remain associated with the correct fields and that invalid values are not silently normalized or discarded.
   - Verify that retry, edit, return, cancel, and alternative contact or completion paths are keyboard and screen-reader accessible.
   - Check session-expiry and authentication recovery for preserved work, advance warning, re-entry burden, and return to the interrupted task.
   - Flag loops, dead ends, cleared forms, ambiguous outcomes, and focus reset to an unrelated location.

10. **Audit submission lifecycle and duplicate prevention.**
    - Verify that the submit control has a clear name and exposes submitting or unavailable state without becoming unreachable or unexplained.
    - Check that repeated activation, Enter-key submission, touch activation, latency, and retry cannot accidentally create duplicate actions.
    - Confirm that disabling a control does not strand focus, suppress necessary status, or prevent recovery after a failed request.
    - Verify that loading feedback is timely, perceivable, and programmatically available when it does not receive focus.
    - Verify that success feedback identifies the completed action and provides the next logical step.
    - Distinguish network failure, server failure, field-level rejection, authorization failure, timeout, and unknown outcome when the recovery action differs.
    - Do not force a WCAG mapping for duplicate-prevention or idempotency defects unless the affected success criterion is directly supported.

11. **Use automation proportionally.**
    - Run available linting, DOM inspection, accessibility rules, component tests, and end-to-end checks when the audit environment allows.
    - Verify automated results against the rendered control, accessible name computation, application state, and user flow.
    - Use automation to confirm detectable issues, not to infer complete keyboard, screen-reader, cognitive, or recovery behavior.
    - Record commands, tool versions, tested routes or stories, and meaningful limitations.

12. **Classify evidence and prioritize.**
    - Separate confirmed findings from manual-test requirements before drafting the result.
    - Use the orchestrator's severity vocabulary when supplied. Otherwise use `critical`, `high`, `medium`, `low`, or `advisory` based on task blockage, information loss, recovery cost, frequency, scope, workaround quality, persistence, and harm.
    - Keep status, severity, and confidence distinct. Do not use WCAG conformance level as severity.
    - Group duplicate manifestations under one root-cause finding while listing all affected controls or states.
    - Prioritize blockers to form completion and recovery before verbosity, consistency, or polish issues.

13. **Map applicable WCAG 2.2 criteria.**
    - Use the current WCAG 2.2 Recommendation or the governing copy supplied by the user.
    - Commonly consider:
      - `1.3.1 Info and Relationships` (A) for label, instruction, error, and group relationships.
      - `1.3.5 Identify Input Purpose` (AA) for programmatically identifiable inputs collecting information about the user.
      - `1.4.1 Use of Color` (A) for required, invalid, success, or status cues conveyed by color.
      - `2.1.1 Keyboard` (A), `2.4.3 Focus Order` (A), `2.4.7 Focus Visible` (AA), and `2.4.11 Focus Not Obscured (Minimum)` (AA) for form operation and focus.
      - `2.4.6 Headings and Labels` (AA) for descriptive labels and summary headings.
      - `2.5.3 Label in Name` (A) when visible control text and accessible names diverge.
      - `3.2.1 On Focus` (A) and `3.2.2 On Input` (A) for unexpected validation, submission, or context changes.
      - `3.3.1 Error Identification` (A), `3.3.2 Labels or Instructions` (A), and `3.3.3 Error Suggestion` (AA).
      - `3.3.4 Error Prevention (Legal, Financial, Data)` (AA) when applicable to consequential submissions.
      - `3.3.7 Redundant Entry` (A) when users must re-enter information already supplied in the same process.
      - `4.1.2 Name, Role, Value` (A) for control names, roles, states, properties, and values.
      - `4.1.3 Status Messages` (AA) for errors, loading, results, success, and progress presented without a change of context.
    - Consider `2.2.1 Timing Adjustable` (A), `3.2.6 Consistent Help` (A), `3.3.5 Help` (AAA), `3.3.6 Error Prevention (All)` (AAA), `3.3.8 Accessible Authentication (Minimum)` (AA), and `3.3.9 Accessible Authentication (Enhanced)` (AAA) only when the audited flow brings them into scope.
    - Do not map a criterion merely because it concerns forms. Explain the issue-to-criterion relationship and label conditional mappings.

14. **Produce the report.**
    - State scope, tested evidence, untested surfaces, and the number of confirmed findings by severity.
    - Use the orchestrator finding contract when one is present in the task context.
    - Otherwise use the portable fallback contract below.
    - End with residual risk and the minimum manual tests needed to close it.

## Output format

### Orchestrator integration

When invoked by `inclusive-interface-audit-orchestrator`, use its shared finding contract:

- Required fields: `id`, `target`, `evidence`, `user_impact`, `status`, `severity`, `confidence`, `framework_mappings`, `recommendation`, and `verification`.
- Allowed `status` values: `confirmed`, `provisional`, `needs-validation`, `not-reproduced`, `resolved`, or `accepted-risk`.
- Allowed `severity` values: `critical`, `high`, `medium`, `low`, or `advisory`.
- Allowed `confidence` values: `high`, `medium`, or `low`, with the reason and missing evidence.
- Optional traceability fields: `source_skill`, `related_ids`, and `root_cause`.
- Treat `accepted-risk` as a documented product decision, not an auditor decision.

If another caller supplies a finding schema:

- Preserve its exact field names, allowed values, identifiers, ordering, and required metadata.
- Put only evidence-backed defects in its findings collection.
- Put unperformed behavior checks in its designated manual-test, open-question, or follow-up collection.
- Add the portable fields below only when the contract permits extensions.
- Do not invent a supposed orchestrator schema or silently translate severity values.

If no schema is supplied, use the same independently portable contract:

```md
## Audit summary

- Scope: ...
- Evidence inspected: ...
- Environments exercised: ...
- Exclusions: ...
- Confirmed findings: critical ..., high ..., medium ..., low ...
- Conformance note: This scoped audit does not establish full WCAG 2.2 conformance.

## Confirmed findings

### FEA-001 — <concise issue title>

- ID: FEA-001
- Target: <route, component, flow, state, role, environment, and occurrence as applicable>
- Evidence: <type, method, reference, environment, and reproducible observation>
- User impact: <affected users, impaired or blocked task, consequence, and workaround>
- Status: confirmed
- Severity: critical | high | medium | low | advisory
- Confidence: high | medium | low — <reason and missing evidence>
- Framework mappings: <WCAG 2.2 criterion and rationale, or an empty list when no valid mapping is established>
- Recommendation: <outcome, constraints, and responsible surface>
- Verification: <retest steps, expected result, method, environment, and closure evidence>
- Source skill: forms-errors-accessibility-audit
- Related IDs: <optional>
- Root cause: <optional>

## Manual-test requirements

### MT-001 — <behavior to verify>

- Risk: ...
- Why manual testing is required: ...
- Related finding ID: <optional provisional or needs-validation record>
- Preconditions: ...
- Steps: ...
- Expected accessible behavior: ...
- Browser, device, and assistive technology: ...
- Evidence to capture: ...

## Coverage and residual risk

| Area or state | Inspected | Exercised | Result or remaining risk |
|---|---:|---:|---|
| Labels and names | ... | ... | ... |
| Instructions and groups | ... | ... | ... |
| Required and invalid states | ... | ... | ... |
| Inline and summary errors | ... | ... | ... |
| Keyboard and screen reader | ... | ... | ... |
| Submission and duplicate prevention | ... | ... | ... |
| Loading, success, network, and server states | ... | ... | ... |
| Recovery and preserved values | ... | ... | ... |

## WCAG 2.2 mapping summary

| Criterion | Confirmed finding IDs | Manual-test IDs | Mapping note |
|---|---|---|---|

## Recommended next actions

1. ...
```

Omit the confirmed-findings section only when there are no confirmed defects, and say so explicitly. Never move manual-test requirements into that section to make the report look complete.

## Quality bar

The task is complete only when:

- The audit covers labels, names, instructions, required and invalid states, groups, autocomplete, input purpose, validation, errors, submission feedback, and recovery as applicable.
- Initial, invalid, submitting, loading, success, network-failure, and server-failure states are inspected or explicitly queued for manual testing.
- Inline errors, error summaries, error identification, correction guidance, validation timing, and status announcements are assessed.
- Keyboard and screen-reader behavior is either exercised with recorded evidence or kept in manual-test requirements.
- Failed-submission recovery, preserved values, session or retry behavior, and duplicate-submission risks are addressed.
- Every confirmed finding includes specific evidence, user impact, an actionable recommendation, a defensible WCAG mapping or explicit absence of one, and a retest.
- Every finding keeps target, status, severity, confidence, framework mappings, recommendation, and verification distinct.
- Manual-test requirements include executable steps and expected accessible behavior.
- Any supplied orchestrator finding contract is followed without making the skill dependent on that orchestrator.
- The report states scope and limitations and makes no unsupported full-conformance claim.
- No product files or external systems are changed.

## Edge cases

- **Native browser validation:** Test representative supported browsers and assistive technologies; built-in messages, focus behavior, localization, and styling differ.
- **Server-rendered postback:** Check whether errors, focus, values, and document context survive the new response.
- **Single-page application:** Check route or step transitions, async DOM replacement, stale live regions, and focus restoration.
- **Multi-step form:** Audit step names, progress, backward navigation, saved values, cross-step errors, review, and final confirmation.
- **Sensitive fields:** Balance value preservation with security; do not recommend retaining secrets merely for convenience.
- **Authentication:** Include password-manager support, paste, accessible authentication, timeout, re-authentication, and recovery only when in scope.
- **Composite date, address, payment, or name controls:** Check group context, field order, locale, input purpose, and error specificity for each part.
- **Dynamic or repeated fields:** Check unique labels, stable identifiers, announced additions or removals, focus placement, and error targeting.
- **Third-party widgets:** Separate defects observable in the integration from behavior that requires vendor or live-environment verification.
- **Localization:** Check translated labels and errors, text expansion, right-to-left order, grammar in dynamic messages, and locale-specific formats.
- **No runnable interface:** Report static findings and provide manual tests; do not predict focus or announcement behavior.
- **No defects found:** Report tested coverage and residual risk rather than declaring the form accessible or conformant.

## Related skills

- `inclusive-interface-audit-orchestrator`
- `accessibility-validation-planner`
- `interface-state-coverage-review`
- `user-recovery-flow-planner`
- `edge-case-test-planner`
- `microcopy-polish`
