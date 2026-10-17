---
name: accessibility-validation-planner
description: Plans accessibility validation for web interfaces across semantic structure, keyboard operation, focus management, screen-reader behavior, zoom and reflow, contrast, reduced motion, and automated checks. Use when a user asks for an accessibility QA plan, WCAG-style validation checklist, a11y test strategy, manual and automated accessibility coverage, or pre-release accessibility verification for pages, components, flows, prototypes, or design-system work.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: frontend-a11y
  task_type: planner
  audience: frontend-developers-and-qa-teams
  tags:
    - accessibility
    - wcag
    - semantic-html
    - keyboard
    - focus-management
    - screen-reader
    - contrast
    - reduced-motion
    - automated-testing
  status: draft
  side_effects: none
---

# Accessibility Validation Planner

## Purpose

Create a practical accessibility validation plan for a web interface before release or handoff. Cover manual checks, assistive-technology checks, responsive and user-preference checks, automated tooling, evidence to collect, and clear pass/fail criteria without pretending that automated scans prove full accessibility.

## When to use this skill

Use this skill when:

- The user asks for an accessibility test plan, QA checklist, validation plan, or WCAG-style review plan.
- A page, component, form, navigation pattern, modal, menu, data view, checkout flow, onboarding flow, or design-system primitive needs accessibility verification.
- The task involves semantic HTML, accessible names, ARIA usage, keyboard support, focus order, focus trapping or return, announcements, screen-reader behavior, zoom, reflow, contrast, reduced motion, or automated scans.
- A team needs to decide what to test manually, what to test with assistive technologies, and what to delegate to automated tools.
- The user wants pre-release accessibility coverage rather than direct implementation changes.

Do not use this skill when:

- The user only asks for a code fix and already has a specific failing accessibility issue.
- The request is primarily visual polish, animation design, or responsive layout planning without accessibility validation.
- The user needs a legal compliance opinion; provide technical validation planning, not legal advice.
- The task is a full implemented-code audit with findings rather than a plan; use or create a review-focused accessibility skill instead.

## Inputs to inspect

Start with the smallest relevant set:

- Product brief, user stories, acceptance criteria, design files, or QA scope.
- Target pages, routes, flows, components, states, and supported browsers/devices.
- HTML/templates/components that define landmarks, headings, controls, labels, tables, dialogs, menus, forms, and error handling.
- CSS that affects visibility, focus indicators, color, layout order, zoom behavior, motion, forced-colors behavior, or responsive reflow.
- JavaScript that manages focus, disclosure, keyboard events, route changes, validation, async status, live regions, or announcements.
- Existing tests, Storybook stories, Playwright/Cypress suites, axe integrations, lint rules, and accessibility documentation.
- Known user preferences or platform requirements, including reduced motion, high contrast or forced colors, text resizing, localization, and input method constraints.

If no repository or implementation exists, build the plan from the supplied interface description and label assumptions explicitly.

## Workflow

1. **Define validation scope.**
   - List the pages, components, user flows, states, and breakpoints in scope.
   - Identify critical tasks and high-risk UI patterns such as forms, dialogs, menus, carousels, drag-and-drop, data tables, custom controls, toasts, and route transitions.
   - State target standards or expectations, such as WCAG-oriented internal criteria, design-system rules, or release-blocking accessibility requirements.

2. **Inventory interaction and content states.**
   - Include default, hover, focus, active, selected, disabled, loading, empty, validation, error, success, expanded, collapsed, authenticated, unauthenticated, and permission-denied states when relevant.
   - Include dynamic updates, async status changes, client-side navigation, overlays, and interrupted or failed operations.
   - Separate essential task states from nice-to-have polish states.

3. **Plan semantic and structural checks.**
   - Verify landmarks, headings, lists, tables, forms, labels, instructions, errors, relationships, document title, language, and reading order.
   - Prefer native HTML semantics before ARIA; flag custom controls that need role, name, state, value, and relationship verification.
   - Include checks for hidden content, duplicated names, inaccessible icons, ambiguous links or buttons, invalid nesting, and content order that differs from visual order.

4. **Plan keyboard and input checks.**
   - Define the expected tab order, shortcut behavior, arrow-key behavior, Escape behavior, activation keys, and non-pointer alternatives.
   - Verify that every task can be completed with keyboard alone and without timing traps.
   - Include checks for custom widgets against expected keyboard patterns, while avoiding unsupported shortcuts that conflict with assistive technologies or browsers.

5. **Plan focus behavior checks.**
   - Define initial focus, visible focus indicators, focus order, focus containment, focus restoration, skip links, route-change focus, error focus, and focus behavior after async updates.
   - Test focus visibility at normal mode, high contrast or forced colors, zoom, and responsive breakpoints.
   - Flag unexpected focus movement, focus loss, hidden focused elements, and focus traps without an exit.

6. **Plan screen-reader and announcement checks.**
   - Choose representative assistive-technology and browser combinations appropriate to the project.
   - Define what must be perceivable through browse/reading mode and what must work in forms/application interaction mode.
   - Check accessible names, descriptions, role/state/value, error announcements, live-region announcements, loading updates, dialog context, table navigation, and route or page changes.
   - Avoid requiring every screen reader to announce identical phrasing; validate that equivalent information and control state are conveyed.

7. **Plan display, perception, and preference checks.**
   - Validate contrast for text, icons, graphical controls, focus indicators, and state indicators.
   - Include zoom, text resizing, reflow, orientation, responsive layout, truncation, spacing, and content overlap checks.
   - Include reduced motion, paused or disabled animation, flashing, autoplay, parallax, transitions, and scroll-linked effects.
   - Include color-independent communication for errors, status, selected states, required fields, charts, and badges.

8. **Plan automated and static checks.**
   - Select appropriate tools such as accessibility linters, HTML validators, axe-based browser checks, component tests, end-to-end scans, contrast tooling, and visual regression checks for focus and reflow.
   - State what each tool can catch and what must remain manual.
   - Add automation at stable checkpoints: component stories, route smoke tests, CI, pull-request checks, and release validation.
   - Prevent false confidence by recording known tool blind spots, ignored rules, and manual follow-up for violations.

9. **Prioritize checks and assign evidence.**
   - Mark blockers, high-priority risks, medium-priority issues, and advisory checks.
   - Assign each check to a role or validation surface, such as developer, QA, design, content, or release owner.
   - Define required evidence: screenshots, short recordings, test output, screen-reader notes, keyboard path notes, browser/device matrix, or linked defects.

10. **Create the execution sequence and acceptance gates.**
    - Start with semantics and keyboard basics before advanced assistive-technology passes.
    - Run automated checks early and repeatedly, but reserve manual verification for final release gates.
    - Include retest rules for fixes, regressions, design changes, dependency upgrades, and content changes.
    - End with a release recommendation format that distinguishes pass, pass with accepted risk, and block.

## Output format

Return the plan using this structure:

```md
## Scope and assumptions

- Interface or flow: ...
- In scope: ...
- Out of scope: ...
- Assumptions and standards: ...

## Validation matrix

| Area | Checks | Method | Evidence | Priority |
|---|---|---|---|---|
| Semantics and structure | ... | ... | ... | ... |
| Keyboard and input | ... | ... | ... | ... |
| Focus behavior | ... | ... | ... | ... |
| Screen reader behavior | ... | ... | ... | ... |
| Zoom, reflow, and display preferences | ... | ... | ... | ... |
| Contrast and non-color cues | ... | ... | ... | ... |
| Motion and time-based behavior | ... | ... | ... | ... |
| Automated checks | ... | ... | ... | ... |

## Assistive technology and browser matrix

| Platform | Browser | Assistive tech or setting | Purpose |
|---|---|---|---|

## Execution sequence

1. ...

## Release gates

- Blockers: ...
- Pass with accepted risk: ...
- Retest requirements: ...

## Open questions

- ...
```

Keep the plan proportional to the risk and scope. For a small component, produce a concise matrix. For a critical flow, include state coverage, assistive-technology combinations, owners, and release gates.

## Quality bar

The task is complete only when:

- The validation scope and assumptions are explicit.
- Semantic, keyboard, focus, screen-reader, zoom/reflow, contrast, motion, and automated checks are all considered.
- The plan separates automated coverage from manual and assistive-technology verification.
- Each check has a method, evidence expectation, and priority.
- Critical user tasks and high-risk UI states are covered before lower-risk polish.
- Release gates distinguish blockers from accepted risks and follow-up items.
- The output remains a validation plan and does not modify product files unless the user separately asks for implementation.

## Edge cases

- **No implementation yet:** Plan against wireframes, states, and intended semantics; add implementation-dependent checks as open questions.
- **Design-system component:** Validate the primitive, documented variants, composition examples, and consumer responsibilities separately.
- **Custom widgets:** Require native alternatives or documented keyboard, role, state, name, and announcement expectations before approval.
- **Single-page apps:** Include route-change title, focus, announcement, loading, and history behavior.
- **Data visualization:** Include text alternatives, table or data access, color-independent encodings, keyboard access, and zoom behavior.
- **Localization:** Include language changes, text expansion, bidirectional layout, translated labels, and reading order.
- **Mobile and touch:** Include screen-reader touch exploration, target size, orientation changes, virtual keyboard behavior, and non-hover alternatives.
- **Known inaccessible third-party content:** Identify whether the team can replace, wrap, document, or accept the risk; do not hide the risk behind automated scan results.

## Related skills

- `progressive-enhancement-planner`
- `interface-state-coverage-review`
- `responsive-behavior-planner`
- `motion-behavior-planner`
- `edge-case-test-planner`
