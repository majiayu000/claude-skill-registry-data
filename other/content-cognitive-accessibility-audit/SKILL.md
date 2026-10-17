---
name: content-cognitive-accessibility-audit
description: Audits web interface content and task flows for cognitive accessibility, including clarity, terminology, predictable controls, memory burden, errors, sequencing, timeouts, distractions, repeated entry, authentication, help, and progress preservation. Use when the user asks for a content-clarity, plain-language, cognitive-load, cognitive-accessibility, COGA-informed, error-comprehension, or recognition-versus-recall review of pages, forms, flows, prototypes, screenshots, or source.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository or artifact access; running-interface access improves behavioral verification but is not required.
metadata:
  category: frontend-a11y
  task_type: review
  audience: accessibility-auditors-content-designers-and-product-teams
  tags:
    - accessibility
    - cognitive-accessibility
    - content-design
    - plain-language
    - wcag
    - coga
    - usability
    - forms
  status: draft
  side_effects: none
---

# Content and Cognitive Accessibility Audit

## Purpose

Audit interface content and end-to-end tasks for barriers involving comprehension, attention, memory, learning, and executive function. Produce evidence-based findings without rewriting content, and distinguish applicable WCAG findings from broader cognitive-accessibility recommendations.

This skill is independently usable. When an audit orchestrator supplies scope, target IDs, evidence, or a finding contract, preserve that context and return compatible specialist findings rather than replanning the whole audit.

## When to use this skill

Use this skill when:

- The user wants content clarity, plain-language, cognitive-load, or cognitive-accessibility reviewed.
- Pages, forms, authentication, support, errors, time limits, or multi-step tasks may create comprehension or memory barriers.
- Screenshots, prototypes, source, a running interface, content inventories, or existing audit evidence need a focused cognitive-accessibility pass.
- A broader accessibility audit needs a specialist review of content, task comprehension, recognition, memory, attention, and recovery.
- WCAG findings must be separated from supplemental cognitive-accessibility guidance.

Do not use this skill when:

- The request is only to rewrite, localize, or market content.
- The main question is semantic markup, keyboard behavior, focus management, responsive layout, media alternatives, or screen-reader announcements and a narrower specialist is available.
- The user requests a conformance certification, legal opinion, diagnosis, or claim about every person with a cognitive disability.
- No interface, content, flow, or evidence is available to inspect.

## Operating rules

- Review only. Do not edit files, rewrite passages, or replace interface copy.
- If implementation is explicitly requested, keep the audit distinct and provide a separately labeled proposed rewrite or implementation handoff. Do not present draft wording as an applied fix.
- Do not claim WCAG conformance or legal compliance.
- Do not treat every cognitive-accessibility concern as a WCAG failure. W3C cognitive-accessibility guidance is supplemental unless a supported WCAG success criterion also applies.
- Do not map a criterion from topic similarity alone. Confirm the criterion's normative conditions, requested WCAG version, target conformance level, exceptions, and available evidence.
- Do not use readability scores, word length, sentence length, or automated checks as sole proof that content is understandable.
- Do not infer a pass from missing evidence. Record `needs-validation` when the artifact cannot expose the relevant behavior.
- Do not assume a screenshot proves task sequencing, timeout behavior, data preservation, repeated entry, authentication burden, or error recovery.
- Describe functional barriers and affected tasks without stereotyping, diagnosing users, or treating cognitive disabilities as one uniform experience.
- Base severity on user and task impact, not the WCAG conformance level.

## Inputs to inspect

Start with the smallest evidence set that represents the requested tasks:

- Audit brief, target WCAG version and level, scope, audiences, supported languages, and critical tasks.
- Page, route, component, form, content, and state inventories.
- Representative user flows, requirements, acceptance criteria, step diagrams, and recovery paths.
- Visible headings, labels, instructions, helper text, abbreviations, terms, controls, errors, confirmations, warnings, and support content.
- Relevant templates, components, validation rules, state management, session handling, timeout logic, persistence, and authentication code.
- Running states for first use, returning use, invalid input, partial completion, cancellation, timeout, session expiry, re-authentication, and recovery.
- Screenshots, recordings, prototypes, design specifications, content guidelines, terminology lists, and localization variants.
- Existing audit reports, analytics, support themes, usability research, and task-based testing evidence.

Do not read an entire repository when representative routes, shared components, content sources, and task states establish the relevant patterns.

## Evidence model

Record the target, state, role, environment, method, and evidence location for each observation.

| Evidence | Supports | Important limitation |
|---|---|---|
| Content or source | Exact wording, structure, labels, validation rules, intended sequence, persistence logic | Does not prove rendered context, actual task behavior, or comprehension |
| Screenshot | Visible hierarchy, wording, apparent controls, distractions, and captured state | Does not prove semantics, transitions, timeouts, recovery, or uncaptured states |
| Prototype | Intended steps, labels, feedback, and interaction concepts | Does not prove production behavior or data preservation |
| Running interface | Reproducible tasks, errors, time pressure, repeated entry, authentication, recovery, and progress preservation | Supports only the tested roles, data, routes, states, and environments |
| Automated or readability tool | Repeatable indicators and candidate passages | Does not establish comprehension, cognitive accessibility, or WCAG failure by itself |
| Expert review | Pattern-based risks and standards analysis | Does not substitute for lived experience or prove that representative users understand the content |
| Task-based user research | Observed comprehension, strategies, errors, recovery, and completion for participants and tasks | Does not establish universal outcomes or WCAG conformance |

Use direct observations for `confirmed` findings. Use `provisional` when the evidence is persuasive but incomplete, and `needs-validation` when a stronger method or missing state is required.

## Audit coverage

Inspect each in-scope task across the following areas.

| Area | Inspect for |
|---|---|
| Headings and instructions | Descriptive page and section headings; instructions at the point of need; clear prerequisites, order, expected input, consequences, and completion conditions |
| Terminology and language | One term per concept; familiar and literal words; explained uncommon terms and abbreviations; manageable syntax; no unnecessary jargon, idioms, nested clauses, double negatives, or unexplained implications |
| Predictable controls | Familiar control patterns; consistent names, appearance, placement, and outcomes; no unexpected context change; destructive or consequential actions clearly distinguished |
| Memory burden and recognition | Needed information remains available; choices and examples support recognition; users are not forced to memorize values, calculate mentally, recall prior steps, or reconstruct lost context |
| Errors and recovery | The error, affected field or step, cause when known, and correction are understandable; valid data remains; users can review, undo, cancel, or recover without starting over |
| Task sequencing | The purpose and sequence are apparent; steps are manageable; current, completed, and remaining work is visible; dependencies and important choices are retained |
| Timeouts and progress | Time limits are disclosed and adjustable when required; warnings are actionable; drafts, input, position, and context survive interruption, timeout, and re-authentication where feasible |
| Repeated data entry | Information already supplied in the same process is auto-populated or selectable unless a documented exception applies |
| Authentication burden | Password managers, paste, autofill, and accessible alternatives are supported; users are not unnecessarily required to recall, transcribe, or solve cognitive-function tests |
| Distractions and interruptions | Moving, flashing, auto-updating, promotional, modal, notification, and audio content does not compete with the primary task without user control |
| Help and support | Contextual and human help are discoverable, understandable, consistently located when repeated, usable without abandoning progress, and appropriate to the task's risk |
| Recognition instead of recall | Labels, visible choices, summaries, examples, history, saved preferences, and retained context let users recognize what to do and what they previously chose |

## Workflow

1. **Confirm the audit frame.**
   - Record the target, user decision, in-scope tasks, roles, locales, platforms, states, and evidence.
   - Record the requested WCAG version and conformance level. If unspecified, report criterion mappings as candidates to verify, not as a conformance determination.
   - Preserve any target IDs, exclusions, severity rules, and output contract supplied by an orchestrator.

2. **Select a representative sample.**
   - Include critical and frequent tasks plus distinct content types, forms, authentication paths, error states, time-limited steps, and recovery flows.
   - Include shared terminology and controls wherever inconsistent reuse could create a cross-interface burden.
   - State what was not reviewed and when the sample should expand.

3. **Walk each task from orientation through recovery.**
   - Identify how a user knows the task purpose, prerequisites, current location, next action, outcome, and available help.
   - Exercise first use, partial completion, invalid input, interruption, return, timeout, session expiry, cancellation, and successful completion when available.
   - Record the exact point where comprehension, attention, memory, or recognition demands increase.

4. **Audit headings and instructions.**
   - Check whether headings and labels describe their topic or purpose and expose a usable structure.
   - Check whether instructions are complete, ordered, colocated with the action, and available after errors.
   - Distinguish missing or unclear helpful guidance from a specific programmatic-structure or input-instruction failure.

5. **Audit terminology and language.**
   - Compare labels, navigation, help, errors, and confirmations for consistent terms and meanings.
   - Identify unexplained abbreviations, unusual words, jargon, idioms, ambiguous references, dense clauses, double negatives, and implied steps.
   - Use audience, task risk, and context to evaluate complexity. Treat readability metrics only as prompts for manual review.

6. **Audit predictability and recognition.**
   - Compare controls with the same function across routes and states.
   - Check whether labels, signifiers, and consequences let users recognize actions without learning an undocumented pattern.
   - Record unexpected changes of context or inconsistent identification separately from broader familiarity concerns.

7. **Audit memory and task burden.**
   - Track every value, rule, code, choice, calculation, or prior instruction the user must remember.
   - Check repeated entry, multi-step context, progress indicators, review screens, saved drafts, back navigation, and return paths.
   - Prefer visible choices, retained summaries, examples, and selectable prior data over unaided recall.

8. **Audit errors, time pressure, and authentication.**
   - Trigger representative errors and verify that users can identify, understand, correct, and recover from them.
   - Inspect warnings, extension controls, data loss, session expiry, and re-authentication continuation.
   - Test password-manager, paste, autofill, one-time-code, alternative authentication, and cognitive-function-test behavior when in scope.

9. **Audit distractions, help, and support.**
   - Identify interruptions or competing content that can displace attention or hide the primary task.
   - Check whether users can pause, dismiss, defer, or control nonessential changes.
   - Verify that help is discoverable at the point of difficulty and can be used without losing entered information or task position.

10. **Classify each issue.**
    - Put an issue in `Applicable WCAG findings` only when the evidence supports a criterion within the named audit scope.
    - Put COGA-informed, plain-language, familiarity, memory, attention, support, or usability improvements without a supported in-scope WCAG failure in `Broader cognitive-accessibility recommendations`.
    - Put plausible issues that require another state, runtime behavior, or participant evidence in `Needs validation`.
    - Keep one finding when several frameworks describe the same target behavior and root cause.

11. **Write findings using the shared contract.**
    - Include every required field defined below.
    - Cite exact wording or a short excerpt only when necessary; otherwise reference the route, component, step, field, state, screenshot, or source location.
    - Make the recommendation outcome-focused. Do not silently rewrite the content.

12. **Define verification and coverage limits.**
    - Give a reproducible retest method and expected result for each finding.
    - Use task-based comprehension testing with representative users when expert inspection cannot verify understanding.
    - Report untested tasks, states, roles, locales, environments, and evidence limitations.

## WCAG mapping boundary

Use the requested WCAG version as authoritative. The following WCAG 2.2 criteria are common candidates, not automatic mappings and not an exhaustive checklist:

| Concern | Candidate criteria | Mapping boundary |
|---|---|---|
| Structure, sequence, headings, and input instructions | 1.3.1, 1.3.2, 2.4.6, 2.4.10, 3.3.2 | A helpful heading or step indicator is not always required; map only when the criterion's structural, descriptive, sequence, or input conditions apply |
| Unusual words, abbreviations, and reading complexity | 3.1.3, 3.1.4, 3.1.5 | These are Level AAA criteria with specific conditions; general plain-language opportunities are broader recommendations |
| Predictable controls and navigation | 3.2.1, 3.2.2, 3.2.3, 3.2.4 | Familiarity alone is insufficient; verify unexpected context changes or inconsistent navigation or identification |
| Errors and assistance | 3.3.1 through 3.3.6 | Match the observed error, instruction, suggestion, prevention, or contextual-help behavior to the exact criterion and level |
| Time limits and preserved progress | 2.2.1, 2.2.5, 2.2.6 | Verify the type of limit, exception, warning, data loss, re-authentication, and requested conformance level |
| Moving, audio, or auto-updating distractions | 1.4.2, 2.2.2 | General visual busyness is broader guidance unless the content meets the criterion's specific conditions |
| Consistent help | 3.2.6 | This criterion does not require help to exist; it governs the relative order of qualifying help mechanisms when repeated |
| Repeated entry | 3.3.7 | Verify the same process, information already provided, available reuse, and normative exceptions |
| Authentication and recall | 3.3.8, 3.3.9 | Verify whether a cognitive-function test is required and whether an allowed method, assistance, or exception is available |

If a supported criterion is above the requested conformance level, label it as an out-of-scope WCAG advisory rather than an in-scope failure. For supplemental cognitive-accessibility guidance, name the guidance source or design objective without placing a WCAG success criterion in `framework_mappings`.

## Finding contract

Give every finding a stable ID and include:

| Field | Requirement |
|---|---|
| `id` | Stable unique identifier such as `CCA-001` |
| `classification` | `applicable-wcag`, `broader-cognitive-recommendation`, or `needs-validation` |
| `target` | Route, component, content item, flow, step, state, role, locale, and environment as applicable |
| `affected_task` | The concrete user goal and point in the task that is blocked, slowed, or made uncertain |
| `evidence` | Evidence type, method, reference, environment, and reproducible observation |
| `user_impact` | Affected functional needs, consequence, frequency or breadth when known, and available workaround |
| `status` | `confirmed`, `provisional`, `needs-validation`, `not-reproduced`, `resolved`, or `accepted-risk` |
| `severity` | `critical`, `high`, `medium`, `low`, or `advisory`, based on user and task impact |
| `confidence` | `high`, `medium`, or `low`, with the reason and missing evidence |
| `framework_mappings` | Supported WCAG criteria with version, level, and rationale, or supplemental guidance with no implied WCAG failure |
| `recommendation` | Outcome-focused remediation guidance, constraints, and responsible surface; no unrequested rewrite |
| `verification` | Retest steps, expected result, method, environment, and evidence required to close |

Optional fields are `source_skill`, `related_ids`, and `root_cause`. Treat `accepted-risk` as a documented product decision, not an auditor decision.

## Output format

Return:

```md
## Audit summary

- Target and in-scope tasks:
- Evidence reviewed:
- WCAG version and level:
- Overall task impact:
- Coverage limitations:
- Conformance disclaimer:

## Applicable WCAG findings

### CCA-001 — Finding title

- Classification:
- Target:
- Affected task:
- Evidence:
- User impact:
- Status:
- Severity:
- Confidence:
- Framework mappings:
- Recommendation:
- Verification:

## Broader cognitive-accessibility recommendations

[Repeat the complete finding structure. Keep WCAG mappings empty unless noting an explicitly out-of-scope advisory.]

## Needs validation

[Repeat the complete finding structure and name the evidence needed.]

## Coverage and strengths

- Verified strengths:
- Untested tasks, states, roles, locales, and environments:
- Recommended next evidence:
```

Omit empty finding sections, but never omit coverage limitations. Report strengths only when directly verified; do not treat them as a conformance statement.

## Quality bar

The task is complete only when:

- Every requested topic was tested, ruled out as not applicable, or listed as not verifiable.
- Findings connect exact evidence to an affected task and concrete user impact.
- Every finding includes the full shared contract, including recommendation and verification.
- Applicable WCAG findings are separated from supplemental cognitive-accessibility recommendations.
- WCAG mappings include criterion rationale and respect the requested version and conformance level.
- Complex language and comprehension claims do not rely only on formulas or auditor preference.
- Runtime-dependent conclusions are based on exercised states or marked for validation.
- Severity, confidence, status, and conformance level remain distinct.
- Duplicate symptoms with the same target behavior and root cause are normalized.
- No content was rewritten or file modified during the review.
- Coverage gaps and evidence limitations are explicit.

## Edge cases

- **Screenshots only:** Review visible wording, hierarchy, terminology, controls, and distractions. Mark behavior, data persistence, repeated entry, authentication, timeout, and recovery as not verifiable.
- **Source only:** Review content and intended logic, then identify runtime states needed to confirm actual behavior and user-visible context.
- **Prototype only:** Review intended content and sequence while separating design intent from production behavior.
- **No named WCAG version or level:** State the assumption or provide candidate mappings for verification; do not invent a conformance target.
- **Highly specialized language:** Evaluate whether terminology is necessary for the audience and whether definitions, examples, summaries, or alternate explanations are available; do not demand oversimplification that changes meaning.
- **Multiple locales:** Audit each materially different translation and reading direction; do not infer clarity or abbreviation handling from the source language.
- **Security-sensitive authentication:** Preserve legitimate security constraints while checking allowed assistance, alternatives, and exceptions. Do not recommend weakening security.
- **Legal, health, financial, or safety tasks:** Raise severity when misunderstanding can cause serious harm and require domain review of any proposed wording.
- **No user research:** Report expert-review findings and hypotheses honestly. Do not claim representative comprehension.
- **Existing orchestrator package:** Preserve its scope, IDs, evidence references, and exclusions; return specialist findings only.

## Related skills

- `inclusive-interface-audit-orchestrator`
- `wcag-audit-scope-planner`
- `accessibility-validation-planner`
- `interface-state-coverage-review`
- `user-flow-planner`
- `user-recovery-flow-planner`
- `microcopy-polish`
