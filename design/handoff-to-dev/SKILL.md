---
name: handoff-to-dev
description: Specify, map, document, validate, and package an approved UX/UI design or prototype into build-ready behavior, component, responsive, state, accessibility, analytics, QA, and acceptance contracts. Trigger on "prepare developer handoff", "hand off to engineering", "create implementation specs", "spec this design", "document component behavior", or "write acceptance criteria". Do not use while the product model is still being redesigned or invent backend contracts.
metadata:
  version: "1.1.1-main"
  argument-hint: "[approved designs, prototype, system links, and platform constraints]"
---

# Handoff to Development

Specify intent, behavior, states, constraints, and verification so implementation requires no hidden product decisions or arbitrary pixel matching.

## 1. Confirm readiness

Collect:

`Approved flow and decisions | Platforms, browsers, devices, locales, inputs | Components, tokens, code, versions | Content, data, permissions, latency, APIs | Accessibility target and test environment | Analytics, release, flags, rollout | Open decisions and owners`

Label unresolved product, data, security, privacy, or technical decisions. Do not disguise them as visual annotations.

## 2. Map the critical flow

Write:

`Entry -> Preconditions -> User action -> System response -> Branches -> Recovery -> Completion -> Return`

Include deep link, refresh, back, cancel, interruption, duplicate submission, expired session, and partial completion where relevant. Define what state is retained.

## 3. Map design to system

For every visible region identify:

`Design object | Code component | Variant | Tokens | Content/data | Event | Owner | Gap`

Synthetic example: `Address search | AddressAutocomplete | Default | semantic field tokens | Provider results | address_selected | Checkout | Timeout policy open`

Use existing component and token names. Avoid raw pixel, color, and typography values when semantic tokens or layout constraints exist. Mark new components and variants explicitly; do not silently create one-off implementations.

## 4. Specify component behavior

Read [references/implementation-contract.md](references/implementation-contract.md). Define anatomy, hierarchy, variants, states, interactions, semantics, content limits, responsiveness, and events. State intent and invariants before exact dimensions.

Use measurements for fixed or bounded values only. For flexible layouts, specify container, grid, min/max, wrapping, truncation, overflow, intrinsic sizing, aspect ratio, alignment, and priority.

Synthetic contract:

`Component: AddressAutocomplete | Intent: accelerate entry without blocking manual input | Trigger: eligible address query | Loading: retain query and announce status | Error: preserve values and expose manual entry | Invariant: selecting a suggestion never submits the form`

## 5. Cover all states

Read [references/state-and-responsive-matrix.md](references/state-and-responsive-matrix.md). Include default and consequential states across component, page, data, network, permission, and session levels.

Provide realistic fixtures for long labels, empty data, maximum values, errors, translated content, and slow responses. Do not let `happy path only` designs become an implementation requirement.

## 6. Specify accessibility

Read [references/accessibility-qa-and-acceptance.md](references/accessibility-qa-and-acceptance.md). Define:

`Control or region | Semantic element | Name, role, state, value | Relationships | Keyboard and focus | Errors and status | Contrast, target, reflow, scaling, motion, touch | Accessible alternative`

Reference relevant WCAG 2.2 criteria for requirements, but do not claim conformance from the specification alone.

## 7. Define telemetry and performance

Only include approved analytics. For each event specify:

`Event | Trigger | Properties | Object ID | Success/failure | Privacy note | Owner`

Define user-visible performance behavior: immediate acknowledgment, loading strategy, cancellation, optimistic update, timeout, retry, state preservation, and layout stability. Add numeric budgets only when product or engineering owns them.

## 8. Write acceptance criteria

Use observable Given/When/Then statements or an equally testable format. Cover behavior, data, states, responsiveness, accessibility, instrumentation, and recovery. Avoid `matches design`, `looks correct`, or `works on mobile` as acceptance criteria.

Synthetic example: `Given autocomplete is unavailable, when the user enters an address manually and submits, then checkout continues without retrying or enabling the provider.`

## 9. Produce the handoff package

For a complete input-to-output demonstration, read [references/worked-example.md](references/worked-example.md). Use it to calibrate behavior-first detail, flexible layout rules, states, and acceptance criteria; do not reuse its fictional system names or API assumptions.

### Scope and dependencies

State included flows, platforms, feature flags, system versions, dependencies, and exclusions.

### Flow contract

Provide transitions, branches, state retention, and recovery.

### Screen and component specs

Use:

`Purpose | System mapping | Anatomy | Content/data | Behavior | States | Responsive | Accessibility | Events`

### State matrix

Include ownership and required fixtures.

### Acceptance criteria

Group by feature behavior, accessibility, responsiveness, data integrity, and resilience.

### Open decisions

Use:

`Question | Why it matters | Decision owner | Blocking? | Needed by`

### Design QA plan

Name environments, viewports, content fixtures, assistive technologies, browsers, and high-risk checks. Record deviations as defects, approved tradeoffs, or design changes.

**Checkpoint:** Trace every acceptance criterion back to approved evidence and forward to component, state, and QA coverage. Revise gaps, then repeat until each Quality-bar item passes or every unresolved decision has an owner and blocking status.

## Quality bar

- critical flows expose branches and recovery, and mappings name system components and tokens;
- content ranges, consequential states, and responsive constraints define implementation behavior;
- accessibility semantics, focus behavior, QA coverage, and acceptance criteria are explicit and observable;
- unresolved decisions have owners and never masquerade as implementation detail.
