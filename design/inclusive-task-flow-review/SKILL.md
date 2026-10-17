---
name: inclusive-task-flow-review
description: Reviews complete user journeys for accessibility, usability, resilience, cognitive load, and exclusion risks. Use when the user asks to assess registration, login, checkout, booking, search and filtering, file upload, onboarding, account recovery, multi-step forms, destructive actions, or another end-to-end task across entry, decisions, interruptions, errors, recovery, completion, confirmation, and return paths.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with access to relevant product artifacts or a running interface. Specialist skill discovery and automatic chaining are optional.
metadata:
  category: ui-ux-polish
  task_type: review
  audience: product-designers-ux-reviewers-and-frontend-teams
  tags:
    - inclusive-design
    - user-flows
    - accessibility
    - usability
    - resilience
    - cognitive-load
    - error-recovery
    - exclusion-risk
  status: draft
  side_effects: none
---

# Inclusive Task Flow Review

## Purpose

Review whether a complete user journey remains understandable, operable, recoverable, and equitable from entry through return. Examine transitions and dependencies between steps—not only individual screens—across accessibility, usability, resilience, cognitive load, and exclusion risk.

This is a journey-level review. It does not modify the target, replace component-level audits, certify conformance, or treat absent evidence as passing behavior.

## When to use this skill

Use this skill when:

- The user wants an end-to-end review of registration, login, checkout, booking, search and filtering, file upload, onboarding, account recovery, a multi-step form, a destructive action, or a comparable task.
- A flow must be inspected across entry conditions, steps, decisions, interruptions, errors, recovery, completion, confirmation, and return paths.
- A task may exclude people because of access requirements, input assumptions, time pressure, identity checks, payment methods, language, device capabilities, or recovery design.
- The user wants journey-level findings synthesized across keyboard, touch, zoom, assistive technology, slow connections, interrupted sessions, or cognitive demand where evidence supports those conclusions.
- An existing journey, prototype, implementation, test suite, support history, or audit needs a proportional inclusive-design review.

Do not use this skill when:

- The user wants a component-level accessibility audit, WCAG conformance assessment, or legal certification.
- The request is only to design a new flow; use a flow-planning skill instead.
- The task concerns one isolated state, control, motion behavior, or copy string and an appropriate specialist skill covers it.
- There is no identifiable task, user goal, or journey evidence to review.

## Operating rules

- Review the whole task before optimizing an individual screen or component.
- Distinguish observed behavior, documented requirements, user-research evidence, and inference.
- Test or report only the input modes, environments, interruption conditions, and assistive technologies that the evidence supports.
- Never infer keyboard, touch, zoom, semantic, announcement, or recovery behavior from screenshots alone.
- Do not equate expert review with evidence from disabled users or other affected populations.
- Do not claim WCAG conformance or legal compliance.
- Keep journey-level findings here. Route detailed technical diagnosis to the narrowest applicable specialist without duplicating its audit.
- Do not modify files, product data, accounts, bookings, orders, payments, or other state. Use test environments and reversible test data when runtime inspection is authorized.

## Inputs to inspect

Start with the smallest set that can establish the task and its variants:

- User goal, success definition, business criticality, known audiences, supported environments, and scope boundaries.
- Flow diagrams, requirements, user stories, acceptance criteria, service blueprints, prototypes, screenshots, recordings, or research findings.
- Entry routes, navigation, deep links, prerequisite communications, eligibility rules, account and permission requirements, and supported alternatives.
- Relevant pages, forms, dialogs, messages, source files, route definitions, state management, validation rules, tests, fixtures, and analytics or support evidence.
- Running interfaces with safe test accounts, representative data, supported browsers, devices, input modes, zoom settings, and assistive technologies.
- Loading, empty, offline, timeout, validation, permission-denied, duplicate-submission, session-expired, partial-success, cancellation, and completion states.
- Downstream artifacts such as emails, receipts, reference numbers, saved progress, account history, and routes back into or away from the task.

Do not read an entire repository when route definitions, representative implementations, tests, and task-specific artifacts are sufficient.

## Evidence limits

Use the available evidence proportionally:

| Evidence | Can support | Cannot establish alone |
|---|---|---|
| Requirements or flow diagram | Intended steps, rules, branches, and outcomes | Implemented behavior or real user success |
| Screenshot | Visible hierarchy, wording, apparent state, and layout | Focus, semantics, announcements, hidden branches, or task completion |
| Prototype | Intended sequence, decisions, labels, and some interactions | Production robustness, actual accessibility, networking, or persistence |
| Source and tests | Implemented paths, validation, persistence logic, and expected behavior | Rendered experience or untested platform behavior |
| Running interface | Reproducible behavior in the tested state and environment | Untested roles, data, platforms, or interruption conditions |
| Assistive-technology test | Output and operation for the named combination and task | Behavior across all assistive technologies or users |
| User research or support evidence | Experienced barriers, strategies, and consequences in its sample | Universal conclusions or unobserved populations |

Record the target version, role, data state, environment, method, and evidence limitation when available. Mark unsupported questions as coverage gaps rather than pass or fail.

## Workflow

1. **Frame the task and review boundary.**
   - State the user's goal, starting point, completion condition, criticality, and consequence of failure.
   - Define in-scope roles, variants, channels, devices, locales, and downstream outcomes.
   - Identify prerequisites such as an account, email access, phone number, identity evidence, payment method, file type, permission, or prior knowledge.
   - Record exclusions, assumptions, and unavailable evidence.

2. **Map the complete journey.**
   - Trace entry conditions and ways users discover, start, resume, or return to the task.
   - Enumerate task steps, system transitions, user decisions, optional paths, dependencies, and points of no return.
   - Include interruptions, validation failures, connectivity loss, timeouts, expired sessions, duplicate actions, partial completion, cancellation, and abandonment.
   - Trace recovery, completion, confirmation, proof of outcome, next steps, and return paths.
   - Label branches and states with stable identifiers so findings can cite them.

3. **Identify affected users and exclusion assumptions.**
   - Ask who cannot enter, understand, operate, complete, recover, or verify the task under the current rules.
   - Inspect assumptions about vision, hearing, dexterity, speech, memory, literacy, language, identity documents, credit, address, device ownership, connectivity, privacy, or access to another channel.
   - Check whether alternatives are genuinely equivalent in cost, time, dignity, privacy, and outcome.
   - Use research evidence when available; otherwise label affected-user analysis as a reasoned hypothesis requiring validation.

4. **Review every journey phase.**
   - **Entry:** Is the task findable, expected, and available without hidden or circular prerequisites?
   - **Orientation:** Does the user understand purpose, requirements, duration, progress, cost, consequences, and available help before committing?
   - **Steps:** Are instructions, labels, sequencing, defaults, dependencies, and progress cues understandable and consistent?
   - **Decisions:** Are choices distinguishable, consequences disclosed before action, and safe defaults used?
   - **Interruptions:** Can the user pause, navigate away, reauthenticate, change device, or recover from a lost connection without unnecessary loss?
   - **Errors:** Are problems detected at a useful time, associated with their cause, explained plainly, and correctable without redoing unrelated work?
   - **Recovery:** Are undo, retry, alternative routes, support, saved progress, and escalation paths available and trustworthy?
   - **Completion:** Is success unambiguous, accurate, and protected from duplicate or uncertain submission?
   - **Confirmation:** Does the user receive durable proof, reference details, consequences, and ways to correct or challenge the outcome?
   - **Return:** Can the user revisit status, resume work, reverse a reversible action, repeat the task, or continue to the next logical destination?

5. **Evaluate interaction conditions where evidence allows.**
   - Complete representative paths using keyboard-only operation and inspect focus continuity across steps, errors, overlays, and route changes.
   - Exercise touch without relying on hover, precision, multi-pointer gestures, or a single orientation.
   - Inspect zoom, text resize, reflow, virtual-keyboard obstruction, content expansion, and loss of context at representative supported sizes.
   - Use named assistive-technology and browser combinations for semantics, control purpose, reading order, instructions, errors, status updates, and confirmation.
   - Avoid demanding every possible combination. Select conditions based on supported environments, user risk, and materially different interaction models.
   - Route component-specific failures discovered in this pass to specialist review.

6. **Stress resilience and continuity.**
   - Use slow or unstable connections, delayed responses, offline transitions, refreshes, back/forward navigation, and repeated activation where safe and relevant.
   - Check whether progress, inputs, uploads, selections, and transaction state survive interruption appropriately.
   - Inspect stale data, concurrent changes, expired authentication, dependency failures, and uncertain outcomes.
   - Verify that retries are idempotent where the task could create duplicate accounts, payments, bookings, uploads, or destructive effects.
   - Check that failure messages preserve entered data and give an actionable, truthful next step.

7. **Review cognitive demand and error tolerance.**
   - Inspect the amount of information, memory, calculation, context switching, time pressure, and unfamiliar terminology required at each step.
   - Check whether instructions remain available when needed and whether users must remember data from another page, device, or message.
   - Look for inconsistent control placement, surprise requirements, ambiguous progress, premature validation, coercive urgency, or repeated entry.
   - Prefer recognition, preview, confirmation, reversible action, and progressive disclosure where they reduce task risk.
   - Distinguish inconvenience from barriers that prevent completion, create harm, or force dependence on another person.

8. **Record journey-level findings using the shared contract.**
   - Create one finding per distinct target behavior, root cause, user impact, and verification method.
   - Merge repeated occurrences when they share a cause and remedy; list every affected step or branch.
   - Separate confirmed findings from hypotheses and coverage gaps.
   - Base severity on user impact, task criticality, breadth, workaround quality, persistence, and potential harm—not on framework labels.

9. **Route specialist follow-up without replacing it.**
   - Use exact installed skill names only after discovery. If discovery is unavailable, name the capability and provide a self-contained handoff.
   - Route field labels, instructions, grouping, autocomplete, validation, submission feedback, and form-specific recovery to `forms-errors-accessibility-audit`.
   - Route headings, landmarks, reading order, control semantics, accessible names, relationships, and ARIA conflicts to `semantic-structure-accessibility-audit`.
   - Route keyboard operation and focus behavior to `keyboard-focus-accessibility-audit`.
   - Route live updates, status messages, dialogs, route changes, and assistive-technology announcements to `dynamic-interface-accessibility-audit`.
   - Route zoom, reflow, text resize, touch targets, orientation, and forced-colors behavior to `visual-responsive-accessibility-audit`.
   - Route missing or inconsistent loading, empty, busy, error, success, and recovery states to `interface-state-coverage-review`.
   - Route framework-specific interpretation to `universal-design-interface-review` or `norman-interaction-principles-review` when the user requests that lens or the journey evidence needs detailed principle mapping.
   - Use `accessibility-validation-planner` when detailed accessibility validation must be planned rather than executed.
   - Preserve the shared finding ID, target, evidence, user impact, and known limitations in every handoff. Ask the specialist to return additions or corrections using the same finding contract.
   - Do not invoke specialists merely to restate a journey-level conclusion.

10. **Synthesize the review.**
    - Summarize whether the primary task can be entered, completed, recovered, confirmed, and revisited under the tested conditions.
    - Prioritize blockers and harmful exclusions before friction and polish.
    - Group cross-cutting root causes across steps while retaining traceable occurrences.
    - List untested branches, roles, environments, populations, and evidence needed.
    - Recommend outcome-focused changes and specialist follow-up; do not prescribe unsupported component implementation details.

## Shared finding contract

Every finding must include:

| Field | Requirement |
|---|---|
| `id` | Stable unique identifier |
| `target` | Flow, step, branch, state, role, environment, and occurrence as applicable |
| `evidence` | Evidence type, method, reference, environment, and reproducible observation |
| `user_impact` | Affected users, blocked or impaired task, consequence, and workaround |
| `status` | `confirmed`, `provisional`, `needs-validation`, `not-reproduced`, `resolved`, or `accepted-risk` |
| `severity` | `critical`, `high`, `medium`, `low`, or `advisory`, based on user and task impact |
| `confidence` | `high`, `medium`, or `low`, with the reason and missing evidence |
| `framework_mappings` | Zero or more supported WCAG criteria, Universal Design principles, usability heuristics, or Norman concepts, each with rationale |
| `recommendation` | Outcome-focused remediation guidance, constraints, and responsible surface |
| `verification` | Retest steps, expected result, method, environment, and evidence required to close |

Optional traceability fields are `source_skill`, `related_ids`, and `root_cause`.

Map WCAG only when the observed behavior and evidence support a specific success criterion. Leave `framework_mappings` empty when no defensible mapping is needed. Treat `accepted-risk` as a documented product decision, not an auditor decision.

## Output format

Return:

```md
## Review summary

- Task and outcome:
- Overall assessment:
- Highest-impact barriers:
- Evidence basis and limits:

## Journey map

| ID | Phase | User goal or action | System response | Branches and risks | Evidence |
|---|---|---|---|---|---|

## Findings

### FLOW-001 — Short title

- Target:
- Evidence:
- User impact:
- Status:
- Severity:
- Confidence:
- Framework mappings:
- Recommendation:
- Verification:
- Source skill / related IDs / root cause: [when applicable]

## Coverage by condition

| Condition | Paths or states reviewed | Result | Evidence limitation |
|---|---|---|---|

## Specialist follow-up

| Finding ID | Skill or capability | Question to validate | Required evidence | Priority |
|---|---|---|---|---|

## Coverage gaps

- Untested branches, roles, environments, populations, and evidence needed.

## Recommended changes

1. ...
```

Keep the journey map proportional. For a small linear task, a concise sequence is sufficient; for a branching or consequential task, preserve explicit step and branch identifiers.

## Quality bar

The task is complete only when:

- Entry, orientation, steps, decisions, interruptions, errors, recovery, completion, confirmation, and return paths are reviewed or explicitly marked not applicable or untested.
- Primary, alternative, failure, cancellation, interruption, and resume paths are covered in proportion to risk.
- Findings cite evidence and distinguish observed behavior from inference.
- Keyboard, touch, zoom, assistive technology, slow connection, interrupted session, and cognitive-load conditions are evaluated only where evidence allows.
- Exclusion risks identify the assumption, affected users, task consequence, workaround quality, and evidence confidence.
- Every finding follows the shared contract with severity, confidence, status, and framework mappings kept distinct.
- Journey-level root causes are synthesized without duplicating component-level specialist findings.
- Specialist handoffs are narrow, traceable, and independently usable.
- Coverage gaps and untested populations remain visible.
- No conformance, legal-compliance, or universal-user claim is made.

## Edge cases

- **Screenshot-only evidence:** Review visible sequence, hierarchy, wording, and captured states. Mark operation, semantics, announcements, persistence, and uncaptured branches as unverified.
- **Prototype-only evidence:** Review intended flow and exclusion assumptions, but separate design intent from production resilience and accessibility.
- **Source-only evidence:** Trace implemented paths and tests, then identify runtime checks needed for rendered behavior and task completion.
- **No running target:** Produce an evidence-limited review and a manual test matrix; do not imply execution.
- **One happy path only:** Review it, then report failure, interruption, recovery, cancellation, and return paths as coverage gaps.
- **Authentication or payment:** Use authorized test environments and non-production data. Do not create real charges, bookings, accounts, or identity events.
- **Destructive action:** Inspect preview, scope, confirmation, cancellation, undo, durable confirmation, and recovery from ambiguous outcomes.
- **Third-party dependency:** Distinguish owned flow design from vendor limitations and document fallback, support, substitution, or accepted-risk decisions.
- **Multiple channels:** Trace handoffs among web, app, email, SMS, phone, or in-person steps, including access and continuity assumptions.
- **No user research:** Report exclusion hypotheses as provisional and name the participant evidence needed; do not treat expert review as lived-experience validation.

## Related skills

- `inclusive-interface-audit-orchestrator`
- `interface-state-coverage-review`
- `forms-errors-accessibility-audit`
- `semantic-structure-accessibility-audit`
- `keyboard-focus-accessibility-audit`
- `dynamic-interface-accessibility-audit`
- `visual-responsive-accessibility-audit`
- `universal-design-interface-review`
- `norman-interaction-principles-review`
- `accessibility-validation-planner`
- `user-flow-planner`
- `user-recovery-flow-planner`
