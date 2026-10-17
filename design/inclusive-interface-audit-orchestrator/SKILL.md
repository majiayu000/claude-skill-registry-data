---
name: inclusive-interface-audit-orchestrator
description: Creates a tailored, evidence-aware audit plan for websites, web applications, pages, component libraries, prototypes, screenshots, source code, and existing audits across WCAG accessibility, Universal Design, usability heuristics, and Norman interaction principles. Use when the user asks for a comprehensive accessibility and UX audit, inclusive-design assessment, WCAG and usability review, or selection and sequencing of the right specialist audit skills for the content and interactions present.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository or artifact access. If skill discovery or automatic chaining is unavailable, return a capability-based, ready-to-use invocation plan.
metadata:
  category: project-planning
  task_type: planner
  audience: accessibility-ux-and-product-audit-leads
  tags:
    - accessibility
    - wcag
    - universal-design
    - usability
    - interaction-design
    - audit-planning
    - orchestration
    - manual-testing
  status: draft
  side_effects: none
---

# Inclusive Interface Audit Orchestrator

## Purpose

Create a proportional, evidence-aware plan for auditing an interface across accessibility, Universal Design, usability heuristics, and interaction design. Inventory the target, choose only relevant specialist skills, define representative samples and manual tests, order the work, and establish one finding contract for final synthesis.

This is a router and planner. It does not perform the complete audit, modify the target, or claim WCAG conformance.

## When to use this skill

Use this skill when:

- The user asks for a comprehensive accessibility, inclusive-design, usability, or interaction-design audit plan.
- A website, application, page, component library, prototype, screenshot set, repository, or existing audit needs several complementary review methods.
- The available evidence must be assessed before deciding which audit specialists can produce valid conclusions.
- The user wants applicable specialist skills selected, scoped, prioritized, sequenced, and given consistent reporting requirements.
- A large or varied target needs representative sampling rather than an unbounded review of every route and state.
- The execution environment cannot automatically chain skills and needs portable, ready-to-paste specialist invocations.

Do not use this skill when:

- The user wants one narrow audit that an existing specialist skill already covers.
- The user asks for direct remediation or implementation rather than an audit plan.
- The task is to certify legal compliance or issue a conformance claim.
- There is no interface target or evidence from which a meaningful plan can be derived.

## Operating rules

- Do not claim WCAG conformance or legal compliance.
- Do not treat an automated scan as a complete accessibility audit.
- Do not select every available specialist by default. Select a skill only when a target pattern, risk, requested framework, or evidence gap justifies it.
- Do not describe a usability heuristic, Universal Design concern, or Norman interaction issue as a WCAG failure without a valid success-criterion mapping and supporting evidence.
- Do not report one underlying problem as separate findings under several frameworks. Preserve multiple valid mappings on one normalized finding.
- Do not assume screenshots can establish keyboard behavior, focus order, semantics, accessible names, dynamic announcements, or assistive-technology behavior.
- Do not infer passing behavior from absent evidence. Use `not-verifiable` or plan a stronger evidence method.
- Prefer specialist skills with review-only or planning-only side effects. This plan does not authorize fixes, publishing, account changes, or other mutations.

## Inputs to inspect

Start with the smallest evidence set that establishes scope and risk:

- User request, audit goals, target audience, business-critical tasks, release stage, and explicit standards or policies.
- URLs, route lists, sitemaps, page templates, feature lists, component inventories, design-system documentation, or Storybook stories.
- Product requirements, user stories, acceptance criteria, user-flow diagrams, role and permission definitions, and supported environments.
- Relevant HTML, templates, components, styles, scripts, routing, validation, state management, tests, fixtures, and accessibility documentation.
- Running pages or builds, including required authentication, test accounts, sample data, feature flags, and environment constraints.
- Screenshots, recordings, wireframes, prototypes, design specifications, content inventories, and responsive variants.
- Existing automated reports, manual audit findings, accessibility statements, defect backlogs, support reports, research, or user-testing evidence.
- Available skill names and descriptions, including their inputs, outputs, side effects, and evidence requirements.

Do not read an entire repository when route definitions, component indexes, stories, and representative implementations can establish the initial inventory.

## Evidence model

Record each evidence source and its limits before selecting specialists.

| Evidence type | Can support | Cannot establish alone |
|---|---|---|
| Source-only | Intended semantics, component structure, event handling, code paths, design tokens, test coverage | Computed accessibility tree, actual focus order, browser behavior, visual rendering, assistive-technology output |
| Screenshot-only | Visible content, hierarchy, apparent contrast, spacing, layout, labels, and captured states | Semantics, accessible names, keyboard operation, focus movement, hidden states, announcements, timing, task completion |
| Prototype | Intended flows, labels, layout variants, transitions, and some interaction concepts | Production semantics, robust keyboard behavior, real loading or error behavior, browser and assistive-technology compatibility |
| Running page | Rendered structure, interaction behavior, computed accessibility data, responsive behavior, and reproducible states | Untested routes, roles, data conditions, environments, or assistive-technology combinations |
| Automated tool | Rules implemented by that tool, repeated checks, and machine-recorded violations | Complete accessibility, task usability, interaction quality, correct reading experience, or conformance |
| Manual interaction | Keyboard, pointer, touch, zoom, reflow, focus, timing, recovery, and task behavior that was actually exercised | Behavior outside the tested sample, setup, browser, role, data, or state |
| Assistive-technology test | Experienced output and operation for the tested browser, platform, assistive technology, settings, task, and state | Universal behavior across assistive technologies or users |
| User testing | Observed task performance, comprehension, strategies, and barriers for participating users | Universal conclusions, untested populations, or WCAG conformance |
| Existing audit | Prior findings, methods, scope, and potential regression targets | Current behavior unless the audit is recent, reproducible, and supported by retained evidence |

Treat combined evidence as stronger only when the sources address each other's limitations. Record environment, date, target version, state, method, and evidence location when available.

## Workflow

1. **Frame the audit request.**
   - Identify the target, audit goal, requested frameworks, decision the audit must support, and planning horizon.
   - Record in-scope and out-of-scope properties, routes, components, roles, locales, devices, and third-party content.
   - Identify any named WCAG version, conformance level, organizational policy, or product standard. If unspecified, record it as an open decision rather than inventing one.
   - State that the output is an audit plan, not findings or a conformance determination.

2. **Build an evidence ledger.**
   - Classify every available input with the evidence model.
   - Record access prerequisites, freshness, completeness, environments, and known limitations.
   - Mark evidence needed to validate claims that the current inputs cannot support.
   - Separate observed facts, claims from prior reports, and assumptions.

3. **Inventory the interface surface.**
   - Group pages by template, purpose, content type, and interaction complexity.
   - Inventory reusable components, layout regions, navigation systems, forms, content modules, overlays, and design-system primitives.
   - Identify roles, permissions, authentication states, locales, breakpoints, input methods, and supported platforms that change behavior.
   - Preserve traceable target identifiers such as route, story, component, flow, or screenshot ID.

4. **Map important flows and states.**
   - Identify critical, frequent, high-risk, and recovery-sensitive user tasks.
   - Include entry, success, cancellation, abandonment, validation, loading, empty, offline, timeout, permission-denied, session-expired, partial-success, and error-recovery paths when relevant.
   - Include default, hover, focus, active, selected, expanded, disabled, read-only, busy, and dynamically updated states where they materially change the experience.
   - Prioritize flows involving identity, money, health, safety, legal commitments, destructive actions, private data, or irreversible outcomes.

5. **Detect audit-relevant patterns.**
   - Check for forms, validation, search, authentication, account recovery, and multi-step transactions.
   - Check for dialogs, popovers, menus, disclosures, tabs, accordions, carousels, tooltips, custom controls, and client-side navigation.
   - Check for site and in-page navigation, breadcrumbs, skip mechanisms, repeated blocks, landmarks, headings, and orientation cues.
   - Check for audio, video, captions, transcripts, autoplay, time limits, flashing, animation, parallax, and other motion.
   - Check for simple and complex tables, grids, charts, maps, diagrams, canvas, and other data visualizations.
   - Check for drag-and-drop, drawing, path gestures, swipe, hover-only behavior, precision input, keyboard shortcuts, and device-motion input.
   - Check for asynchronous loading, live updates, notifications, toasts, status messages, optimistic updates, infinite scroll, and route changes.
   - Check for responsive reflow, zoom, text resize, orientation, touch targets, virtual keyboards, localization, bidirectional text, and content expansion.
   - Record each pattern as `present`, `absent`, `suspected`, or `not-verifiable`, with its evidence source.

6. **Define a representative sample.**
   - Include every critical user flow and unique high-risk pattern.
   - Select at least one representative of each materially different page template, component family, content type, role, and interaction model.
   - Include shared site-wide surfaces such as header, navigation, search, footer, authentication, and notifications when present.
   - Include representative success, failure, loading, empty, permission, and recovery states.
   - Include supported viewport, zoom, input, locale, and user-preference conditions in proportion to risk.
   - Document why each sample represents a wider set and list the untested remainder.
   - Define expansion triggers: increase the sample when implementations differ, repeated failures appear, a component is inconsistently composed, or evidence contradicts the assumed template.

7. **Discover and select specialist skills.**
   - Inspect available skill metadata before naming specialists.
   - Select the narrowest skill that covers the required capability and accepts the available or planned evidence.
   - Use a broader review skill only for cross-cutting coverage or when no narrower specialist exists.
   - Avoid chaining one router into another unless it adds a distinct inventory, sampling, or synthesis capability.
   - If no exact skill exists, name the required capability and provide a self-contained work package; do not invent an installed skill name.
   - Record excluded but plausible skills and why they are not applicable.

   Consider these capability areas only when triggered:

   | Capability | Select when | Typical evidence dependency |
   |---|---|---|
   | WCAG accessibility baseline | WCAG or accessibility is in scope | Combined source, running-page, automated, and manual evidence |
   | Semantics and content structure | Documents, headings, landmarks, forms, tables, or custom controls are present | Source plus rendered or accessibility-tree inspection |
   | Keyboard and focus | Any interactive control, overlay, composite widget, shortcut, drag action, or client-side navigation is present | Running page and manual keyboard testing |
   | Screen reader and announcements | Forms, dialogs, dynamic updates, status messages, data structures, or route changes are present | Running page and named assistive-technology combinations |
   | Forms, authentication, and recovery | Input, validation, identity, session, transaction, or destructive flows are present | Running states, rules, test data, and manual task completion |
   | Navigation and orientation | Multiple routes, repeated regions, deep content, or complex information architecture are present | Route inventory, source, running page, and task paths |
   | Responsive, zoom, and touch | Responsive layouts, dense controls, mobile use, or embedded contexts are present | Running page across representative sizes and settings |
   | Motion, media, and timing | Animation, autoplay, time limits, audio, video, flashing, or gesture feedback is present | Running behavior, media assets, preferences, and manual tests |
   | Tables and data visualization | Complex data, grids, charts, maps, or canvas content is present | Source, rendered structures, alternative data access, keyboard and assistive-technology tests |
   | Drag, gesture, and custom input | Pointer path, precision, drawing, swipe, or device input is required | Running page with alternative-input testing |
   | Interface states and recovery | Async, offline, validation, permission, error, or interrupted states exist | State inventory, fixtures, running states, and flow evidence |
   | Universal Design and persona coverage | Diverse abilities, contexts, roles, environments, or equitable-use questions are in scope | Product context, representative scenarios, interface evidence, and research when available |
   | Usability heuristics | Task clarity, consistency, feedback, error prevention, efficiency, or help is in scope | Representative flows and observable interface behavior |
   | Norman interaction principles | Discoverability, feedback, conceptual models, signifiers, mapping, constraints, or recovery need review | Interactive flows, state transitions, labels, controls, and user expectations |
   | User testing | Consequential tasks or unresolved usability hypotheses justify participant evidence | Stable testable target, ethical recruitment, accessible protocol, and representative tasks |

   One specialist may cover several capabilities. Do not create duplicate work merely to assign one skill per framework.

8. **Scope every selected specialist.**
   - For each specialist, record the exact skill name when available, selection reason, target sample, priority, prerequisites, evidence method, deliverable, dependencies, and evidence limitations.
   - State which framework or capability gap the specialist covers.
   - Give each specialist explicit exclusions to prevent scope creep and duplicate findings.
   - Require output in the shared finding contract or include a normalization step.

9. **Order the audit work.**
   - Start with scope confirmation, target inventory, environment access, and evidence preparation.
   - Schedule safe automated and source-based checks early to identify patterns and prepare manual tests, never as a completion gate by themselves.
   - Establish broad structural and task-flow baselines before narrow interaction or assistive-technology passes.
   - Schedule keyboard, focus, responsive, motion, media, data, and announcement specialists after their required states and fixtures are available.
   - Schedule heuristic, Universal Design, and Norman reviews against the same representative tasks and states used by accessibility specialists.
   - Schedule user testing only when the target, tasks, participant plan, consent, accommodations, and evidence handling are ready.
   - Finish with normalization, deduplication, gap review, fix-verification planning, and synthesis.
   - Mark work that may proceed in parallel and name the shared evidence or decisions that must remain stable.

10. **Define manual-testing requirements.**
    - Require keyboard-only task completion and focus inspection for interactive samples.
    - Define representative screen-reader, browser, platform, and input combinations from supported environments and risk; do not demand every possible combination.
    - Include zoom, text resize, reflow, orientation, forced-colors or high-contrast settings, reduced motion, touch, and target-size checks when applicable.
    - Require testers to exercise relevant errors, loading, empty, permission, authentication, timeout, cancellation, and recovery states.
    - Define setup data, accounts, permissions, fixtures, expected outcomes, evidence capture, and cleanup.
    - Separate expert manual review, assistive-technology testing, and participant user testing. Do not use one as a substitute for another.

11. **Establish the shared finding contract.**
    - Require every specialist finding to contain:

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

    - Allow `source_skill`, `related_ids`, and `root_cause` as optional traceability fields.
    - Base severity on user impact, task criticality, breadth, workaround quality, persistence, and harm. Do not use WCAG conformance level as severity.
    - Map WCAG only when the observed issue and evidence support a specific criterion. Leave the WCAG mapping empty for heuristic-only findings.
    - Treat `accepted-risk` as a documented product decision, not an auditor's unilateral status.

12. **Define synthesis and validation.**
    - Merge findings that share the same target behavior, root cause, and user impact; retain all valid framework mappings and occurrences.
    - Keep separate findings when similar symptoms have different causes, fixes, or verification methods.
    - Reconcile severity and confidence from the strongest reproducible evidence, documenting unresolved disagreement.
    - Separate confirmed findings, hypotheses requiring stronger evidence, and coverage gaps.
    - Summarize affected tasks and cross-cutting root causes before framework counts.
    - Define targeted retests, regression checks, owners, and closure evidence for future remediation.
    - Report untested pages, states, roles, environments, and populations. Never turn representative sampling into a conformance claim.

13. **Return a portable invocation plan.**
    - Do not imply that specialist audits have run.
    - When skills are available, use their exact discovered names.
    - When skill discovery or chaining is unavailable, use capability labels and include a ready-to-paste prompt containing the target, sample, evidence, exclusions, finding contract, expected output, dependencies, and limitations.
    - If the environment can chain skills and the user later authorizes execution, preserve the same phases, dependencies, shared contract, and synthesis gates.

## Output format

Return the plan using this structure:

```md
## Audit brief

- Target and decision:
- Requested frameworks:
- In scope:
- Out of scope:
- Standards and assumptions:
- Conformance disclaimer:

## Evidence ledger

| Evidence ID | Type | Target/version | Available | Supports | Limitations | Access prerequisite |
|---|---|---|---|---|---|---|

## Interface and risk inventory

| Target ID | Page, component, flow, or state | Patterns | Criticality | Evidence | Audit implications |
|---|---|---|---|---|---|

## Representative sample

| Sample ID | Target and states | Represents | Selection reason | Methods required | Expansion trigger |
|---|---|---|---|---|---|

## Specialist audit plan

| Order | Skill or capability | Why selected | Targets | Priority | Dependencies | Evidence and limitations | Deliverable |
|---|---|---|---|---|---|---|---|

## Manual-testing matrix

| Task or pattern | Method and environment | States | Setup | Expected evidence | Limitation |
|---|---|---|---|---|---|

## Sequence and checkpoints

1. ...

## Shared finding contract

[Repeat the required fields, allowed values, severity basis, and mapping rules.]

## Portable invocation plan

### Invocation 1 — Skill or capability

- Run after:
- Target and sample:
- Inputs:
- Ready-to-paste prompt:
- Expected output:
- Evidence limitation:

## Synthesis and validation plan

- Normalization and deduplication:
- Framework mapping review:
- Coverage-gap review:
- Retest and regression approach:
- Final synthesis sections:

## Excluded specialists

| Skill or capability | Why not selected | Reconsider when |
|---|---|---|

## Open questions and prerequisites

- ...
```

Keep small targets concise. For large systems, summarize the plan in the main response and place the detailed sample and invocation matrices in a separate portable artifact when the environment supports it.

## Quality bar

The task is complete only when:

- The target, decision, requested frameworks, scope, assumptions, and exclusions are explicit.
- Pages, components, content types, states, roles, patterns, and critical flows are inventoried in proportion to the target.
- Every selected specialist has a specific reason, target, priority, dependency, deliverable, evidence method, and limitation.
- Plausible but irrelevant specialists are excluded rather than run automatically.
- The representative sample covers critical flows and unique high-risk patterns and includes documented expansion triggers.
- Automated, source-only, screenshot-only, running-page, manual, assistive-technology, and user-testing evidence are distinguished.
- Manual tests include setup, environment, states, expected evidence, and limitations.
- The shared finding contract contains every required field and keeps severity, confidence, status, and framework mappings distinct.
- Synthesis rules prevent duplicate findings across WCAG, Universal Design, usability, and Norman lenses.
- The output includes a portable invocation plan and never implies that specialist audits were executed.
- No conformance, legal-compliance, or complete-audit claim is made.

## Edge cases

- **Screenshots only:** Plan visual and content reviews that the evidence supports. Mark semantics, keyboard, focus, dynamic behavior, and assistive-technology conclusions as not verifiable and request a running target or source.
- **Source only:** Plan static inspection and test review, then identify runtime checks needed for computed semantics, focus, layout, timing, and assistive technology.
- **Prototype only:** Review intended flows and interaction concepts while separating design intent from production accessibility and resilience.
- **Existing audit only:** Normalize prior findings into the shared contract, assess scope and freshness, and plan reproduction before treating them as current.
- **No skill catalog:** Use capability labels and portable prompts. Do not fabricate skill availability.
- **Restricted or authenticated target:** List access, test-account, safe-data, permission, and environment prerequisites. Do not bypass access controls.
- **Large or heterogeneous system:** Use stratified samples by template, pattern, role, and criticality, with expansion triggers and an explicit untested inventory.
- **Component library:** Sample primitives, variants, states, compositions, documentation, and consumer responsibilities separately.
- **Third-party content:** Distinguish owned remediation from vendor risk, replacement, wrapping, fallback, and acceptance decisions.
- **No participant research:** Record the user-testing gap. Do not present expert heuristic review as evidence of lived user experience.
- **Conflicting specialist findings:** Preserve the evidence trail, reconcile target and root cause, and keep unresolved disagreement visible.
- **Multiple locales or roles:** Include materially different content, reading direction, permissions, task paths, and error states in the sampling strategy.

## Related skills

- `accessibility-validation-planner`
- `interface-state-coverage-review`
- `user-flow-planner`
- `edge-case-test-planner`
- `user-recovery-flow-planner`
- `responsive-behavior-planner`
- `motion-behavior-planner`
- `progressive-enhancement-planner`
