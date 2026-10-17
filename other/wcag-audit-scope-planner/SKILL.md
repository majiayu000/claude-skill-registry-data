---
name: wcag-audit-scope-planner
description: Defines a bounded, evidence-aware WCAG accessibility audit scope before testing begins. Use when a user asks to scope a WCAG audit, select a WCAG version and conformance level, inventory audit surfaces and user flows, choose a representative sample, define browser and assistive-technology coverage, assign test methods and specialist auditors, or document exclusions and evidence limitations. Produces a planning artifact only; it does not perform the audit or claim conformance.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: frontend-a11y
  task_type: planner
  audience: accessibility-leads-qa-teams-and-product-owners
  tags:
    - accessibility
    - wcag
    - audit-planning
    - scope
    - representative-sampling
    - assistive-technology
    - test-matrix
    - evidence
  status: draft
  side_effects: none
---

# WCAG Audit Scope Planner

## Purpose

Define what a WCAG accessibility audit will and will not evaluate before testing starts. Produce a traceable scope covering the standards target, interface inventory, representative sample, environments, test methods, evidence boundaries, exclusions, and required specialist skills.

This skill prepares an audit. It does not run tests, issue findings, certify accessibility, or conclude that a product conforms to WCAG.

## When to use this skill

Use this skill when:

- A team needs a written WCAG audit scope before internal testing, vendor engagement, release review, procurement, or remediation planning.
- The audit target spans multiple routes, templates, components, roles, states, devices, or user flows.
- Time or access constraints require representative sampling rather than exhaustive testing.
- Browser, device, input-method, or assistive-technology coverage must be agreed before execution.
- Audit work must be divided among accessibility specialists without leaving gaps or duplicating effort.
- An `inclusive-interface-audit-orchestrator` needs a bounded intake package for routing specialist audit work.
- A previous audit scope must be revised after product, platform, standards, or support-matrix changes.

Do not use this skill when:

- Testing is already underway and the user needs findings, defect analysis, remediation, or retesting.
- The user asks for a complete accessibility audit or a WCAG conformance determination.
- The request is for legal advice, certification, or an accessibility conformance report.
- A fixed scope already exists and the user only needs a detailed validation checklist; use an accessibility validation planning skill instead.
- The user asks to make implementation changes.

## Inputs to inspect

Start with the smallest available set that can establish the audit boundary:

- Audit objective, commissioning brief, statement of work, release gate, procurement requirement, or internal accessibility policy.
- Required WCAG version, conformance level, jurisdictional overlay, contractual criteria, and evaluation date.
- Sitemap, route manifest, navigation model, page inventory, content types, templates, design-system catalog, component stories, and embedded surfaces.
- Primary and secondary user flows, essential transactions, user roles, authentication boundaries, permissions, and recovery paths.
- Designs, prototypes, source structure, test environments, feature flags, locales, themes, breakpoints, and known interface states.
- Supported browser, operating-system, device, input-method, and assistive-technology policies.
- Product analytics, support data, usage research, risk registers, prior audit reports, known defects, and change history when available.
- Existing automated checks, source tests, end-to-end tests, manual QA scripts, and accessibility documentation.
- Test accounts, test data, environment access, third-party integrations, production-only behavior, and security or privacy constraints.

If an input is unavailable, record the gap and its effect on scope confidence. Do not invent product support or audit requirements.

## Planning rules

- State the exact target WCAG version and conformance level. Do not silently assume either one.
- Keep legal, contractual, policy, and WCAG requirements distinct even when they overlap.
- Treat representative sampling as risk-based coverage, not proof that untested surfaces conform.
- Trace each selected sample to the routes, templates, components, states, roles, or flows it represents.
- Define an expansion trigger for every sampled group so repeated failures, implementation differences, or contradictory evidence enlarge the sample.
- Separate exclusions from blocked or unavailable evidence. An area is not out of scope merely because it is difficult to access.
- Select environment combinations for a documented reason. Do not promise every possible browser, device, input, and assistive-technology permutation.
- Assign named specialist skills only when they are available. Otherwise assign the required capability to a qualified human or equivalent workflow.
- Preserve the `inclusive-interface-audit-orchestrator` evidence model and shared finding contract when it is the downstream coordinator.
- Phrase unresolved matters as decisions, assumptions, risks, or evidence gaps. Never convert them into pass results.

## Workflow

1. **Establish the audit objective and standards target.**
   - Record why the audit is being commissioned, who will use the result, and what decision it is expected to support.
   - State the exact WCAG version, target conformance level, evaluation date, and any additional policy, legal, or contractual requirements.
   - Clarify whether the request concerns a whole product, a bounded release, selected journeys, a design system, a component set, or another defined surface.
   - If the version or level is undecided, make it a blocking scope decision and explain what the choice changes. A recommendation may be offered, but it must not be presented as an agreed target.

2. **Build the interface inventory.**
   - List pages and routes, route families, templates, content types, components, embedded experiences, and platform-specific surfaces.
   - Identify primary, secondary, failure, interruption, and recovery flows, including every step in essential transactions.
   - Include relevant user roles, permission levels, authenticated and unauthenticated experiences, locales, themes, and feature-flag variants.
   - Inventory meaningful states such as default, hover, focus, active, selected, expanded, collapsed, disabled, loading, empty, validation, error, success, timeout, offline, and session expiry.
   - Give inventory items stable identifiers so later sample, test, and evidence tables can refer to them unambiguously.

3. **Classify coverage as exhaustive or sampled.**
   - Mark essential processes and unique high-risk behavior for exhaustive coverage when practical.
   - Group repeated routes by shared template, component composition, content structure, interaction model, and technical implementation.
   - Do not group items merely because their screenshots look similar.
   - Record the known population size for each group when available and label unknown inventory completeness as a limitation.

4. **Choose a representative sample.**
   - Include at least one instance of each common page or template type in scope.
   - Include all steps and outcome states of each selected essential process; do not sample only the entry page.
   - Include high-risk patterns such as complex forms, custom widgets, dialogs, menus, data tables, drag-and-drop, media, authentication, payments, asynchronous updates, and error recovery when present.
   - Cover materially different layouts, content densities, roles, locales, themes, breakpoints, third-party integrations, and dynamic states.
   - Use analytics, usage research, defect history, change risk, and technical uniqueness when available, but do not let traffic alone exclude low-volume essential tasks.
   - For every sample item, record the selection rationale, represented inventory IDs, required states, known coverage gaps, and conditions that require sample expansion.
   - State explicitly that results from sampled items cannot establish conformance for untested content.

5. **Define the environment and input matrix.**
   - Start from documented product support, contractual commitments, actual user evidence, and available test infrastructure.
   - Specify operating system, browser and relevant version policy, device class, viewport or display mode, and any required platform settings.
   - Cover applicable input methods such as keyboard-only, pointer, touch, speech input, switch access, stylus, or device-specific controls.
   - Select purposeful assistive-technology and browser combinations for desktop and mobile, including screen readers and any required magnification, voice-control, forced-colors, or platform accessibility settings.
   - Record the purpose of each combination, the surfaces it covers, and any unsupported, unavailable, or unverified combinations.
   - Avoid a combinatorial matrix with no risk rationale; identify baseline combinations and targeted exception combinations instead.

6. **Allocate test methods.**
   - Define automated checks, including the routes, components, states, rules, configuration, and scan limitations.
   - Define source inspection for semantic HTML, accessible names, ARIA, relationships, DOM and reading order, forms, errors, dynamic updates, and generated markup.
   - Define keyboard testing for reachability, operability, expected widget patterns, focus order, focus visibility, focus containment, restoration, shortcuts, and non-pointer alternatives.
   - Define responsive and display testing for zoom, text resize, reflow, orientation, spacing, overflow, responsive state changes, target sizing, forced colors, and user preferences.
   - Define screen-reader testing for structure, navigation, names, descriptions, roles, states, values, forms, errors, status announcements, dialogs, tables, and route changes.
   - Define other manual checks that automation cannot establish, including contrast in context, color-independent meaning, timing, flashing, motion, media alternatives, instructions, error recovery, content clarity, and task completion.
   - For each test area, identify the inventory or sample IDs, preconditions, method, expected evidence, owner or specialist, and known limitations.

7. **Determine required specialist audit skills.**
   - Classify each capability as `required`, `conditional`, or `not required`, with a scope-based rationale.
   - Consider these specialist capabilities:
     - semantic HTML, accessible names, ARIA, forms, errors, and source inspection
     - keyboard interaction and focus management
     - screen-reader navigation and announcements
     - responsive layout, zoom, reflow, text spacing, and orientation
     - contrast, non-color cues, forced colors, and visual-state perception
     - motion, animation, flashing, time limits, and reduced-motion behavior
     - mobile, touch, gesture, target-size, and device accessibility
     - media alternatives, documents, canvas, charts, maps, or other specialized content
     - cognitive load, instructions, language, consistency, and error recovery
     - automated scanning, source tooling, and test automation
     - WCAG criterion mapping, evidence review, and final report quality control
   - When discovered and applicable, evaluate these sibling specialists before selecting a broader audit skill:
     - `semantic-structure-accessibility-audit` for document structure, native semantics, ARIA, accessible names, labels, relationships, lists, and tables
     - `keyboard-focus-accessibility-audit` for keyboard operation, focus order, focus visibility, focus movement, composite patterns, shortcuts, and non-pointer alternatives
     - `forms-errors-accessibility-audit` for labels, instructions, required and invalid states, validation, submission feedback, announcements, and recovery
     - `visual-responsive-accessibility-audit` for contrast, non-color cues, zoom, reflow, text spacing, orientation, target sizing, forced colors, and responsive behavior
     - `content-cognitive-accessibility-audit` for instructions, language clarity, consistency, cognitive load, error prevention, recovery, and time-dependent content
   - Treat these names as candidates, not mandatory dependencies. If a skill is unavailable or its declared scope does not fit, assign the capability to another discovered specialist or a qualified human.
   - Name the specialist skill, tool-assisted workflow, or qualified human role that will own each required capability.
   - For each assignment, record the exact skill or capability name, selection reason, target sample, priority, prerequisites, evidence method, deliverable, dependencies, evidence limitations, and explicit exclusions.
   - Record plausible specialists that are not selected, why they are excluded, and what scope change would make them relevant.
   - When `inclusive-interface-audit-orchestrator` is available, use the scope matrices as its workstream inputs. When it is unavailable, use the same assignment table as the standalone execution plan.

8. **Document evidence requirements and limitations.**
   - Build an evidence ledger that identifies each source, target and version, availability, what it can support, what it cannot establish, and any access prerequisite.
   - Define acceptable evidence for each method, such as reproducible steps, source references, tool output, screenshots, recordings, environment details, assistive-technology notes, or linked defects.
   - Record unavailable source code, incomplete inventories, inaccessible environments, missing accounts, unstable test data, production-only behavior, unsupported tools, and untested combinations.
   - Distinguish `excluded by agreement`, `blocked`, `not available`, `not applicable`, and `deferred`; these statuses have different audit implications.
   - For every excluded or limited area, state the reason, affected coverage, risk, decision owner, and follow-up needed.
   - Include a standing limitation that defects may exist outside the selected sample and that automated results cannot establish WCAG conformance.

9. **Check scope readiness and prepare the handoff.**
   - Confirm that the standards target, inventory, sampling rationale, environment matrix, test-method matrix, evidence rules, specialist assignments, exclusions, and open decisions are internally consistent.
   - Identify prerequisites such as test accounts, data, environments, devices, assistive technologies, source access, and named owners.
   - If `inclusive-interface-audit-orchestrator` will coordinate execution, reference its shared finding contract rather than creating a competing result schema.
   - If the plan will be executed independently, require downstream findings to retain at least a stable ID, precise target, evidence and environment, user impact, status, confidence, applicable standards mapping, recommendation, and verification method.
   - Mark the plan `ready`, `ready with open items`, or `not ready`, based on whether testing can begin without creating material coverage ambiguity.
   - Hand off the scope package to the orchestrator, audit lead, or specialist owners without beginning the audit.

## Output format

Return the plan using this structure:

```md
# WCAG audit scope

## Audit objective and standards target

- Product or release:
- Audit objective:
- Intended decision:
- WCAG version:
- Conformance level:
- Additional requirements:
- Evaluation date:
- Scope owner:
- Downstream finding contract:

## Evidence ledger

| Evidence ID | Type | Target and version | Available | Supports | Cannot establish | Access prerequisite |
|---|---|---|---|---|---|---|

## Coverage inventory

| ID | Surface type | Route, template, component, state, or flow | Variants and dependencies | Coverage mode |
|---|---|---|---|---|

## Representative sample

| Sample ID | Inventory represented | Required states or flow steps | Selection rationale | Known gap | Expansion trigger |
|---|---|---|---|---|---|

## Environment and input matrix

| ID | OS and device | Browser policy | Input or assistive technology | Purpose | Limitation |
|---|---|---|---|---|---|

## Test-method matrix

| Area | Inventory or sample IDs | Method and preconditions | Evidence required | Owner or specialist | Limitation |
|---|---|---|---|---|---|

## Specialist assignments

| Order | Capability | Requirement | Named skill or role | Target sample | Priority | Prerequisites and dependencies | Evidence and limitations | Deliverable and exclusions |
|---|---|---|---|---|---|---|---|---|

## Excluded specialists

| Skill or capability | Why not selected | Reconsider when |
|---|---|---|

## Exclusions and evidence limitations

| Area | Status | Reason | Coverage and risk impact | Decision owner | Follow-up |
|---|---|---|---|---|---|

## Prerequisites and open decisions

- ...

## Scope readiness

- Status: ready / ready with open items / not ready
- Conditions before testing:
- Sampling caveat: Results cannot establish conformance for untested content.
- Conformance statement: No conformance conclusion is made by this planning artifact.
```

Keep the plan proportional to the product and audit risk. A single component may need short matrices; a multi-role service or essential transaction needs route, state, environment, evidence, and specialist traceability.

## Quality bar

The task is complete only when:

- The exact target WCAG version and conformance level are stated or clearly marked as unresolved blockers.
- Pages, routes, components, templates, states, roles, and user flows are inventoried at a useful level of detail.
- Exhaustive and representative coverage are distinguished.
- Every sampled item has a rationale, traceable representation, required states, and a known-gap statement.
- Every sampled group has an expansion trigger.
- Supported browsers, devices, input methods, and assistive technologies are defined with selection rationales.
- Automated, source, keyboard, responsive, screen-reader, and other manual test coverage is explicit.
- The evidence ledger distinguishes what each source supports from what it cannot establish.
- Evidence requirements, unavailable evidence, excluded areas, decision owners, and risk impacts are recorded.
- Required specialist capabilities and their handoffs are assigned without assuming unavailable named skills.
- Plausible but unselected specialists have a reason and reconsideration trigger.
- The output can feed `inclusive-interface-audit-orchestrator` but remains executable as a standalone scope and assignment plan.
- The result contains no audit findings, pass/fail results, certification language, or WCAG conformance claim.

## Edge cases

- **No reliable inventory:** Scope discovery as a prerequisite and label sampling confidence as low until the population is known.
- **No agreed WCAG target:** Keep version and level as a blocking decision; do not let test execution imply a target.
- **Single component:** Include host-page context, compositions, responsive containers, states, and consumer responsibilities.
- **Design system:** Sample primitives, complex composites, documented variants, themes, and representative consumer compositions separately.
- **Single-page application:** Include client-side route changes, loading, focus, title, history, announcement, error, and offline states.
- **Essential transaction:** Include every step, alternate path, error, interruption, timeout, confirmation, and recovery outcome.
- **Authenticated or role-based product:** Include materially different roles and permissions; do not infer one role from another.
- **Third-party or embedded content:** Record ownership and control boundaries, but retain the user-facing risk in scope unless exclusion is explicitly approved.
- **Native mobile or non-web surface:** Separate it from the WCAG web scope and assign an appropriate platform-specific accessibility standard and specialist.
- **Document or media-heavy product:** Add specialist sampling for PDFs, office documents, captions, transcripts, audio description, and media-player controls.
- **Unavailable assistive technology:** Record the coverage gap and substitute only when the substitute answers the same risk; otherwise defer the claim.
- **Very small budget or timeline:** Reduce breadth transparently through risk-based sampling, but do not hide omitted essential processes or high-risk patterns.

## Related skills

- `inclusive-interface-audit-orchestrator`
- `accessibility-validation-planner`
- `semantic-structure-accessibility-audit`
- `keyboard-focus-accessibility-audit`
- `forms-errors-accessibility-audit`
- `visual-responsive-accessibility-audit`
- `content-cognitive-accessibility-audit`
- `a11y-audit-fix`
- `keyboard-pattern-verifier`
- `screen-reader-announcement-audit`
- `responsive-layout-qa`
- `motion-accessibility-review`
- `wcag-evidence-mapper`
