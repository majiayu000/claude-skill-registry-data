---
name: fix-web-accessibility
description:
  Audit and fix HTML accessibility issues including ARIA labels, keyboard navigation, focus management, color contrast,
  and form errors. Use when adding interactive controls, forms, dialogs, or reviewing WCAG 2.2 compliance of code. For
  design-stage audits of mockups or screenshots without code, use accessibility-review when available.
---

# Fix Web Accessibility

Fix accessibility issues.

## how to use

- `/fix-web-accessibility` Apply these constraints to any UI work in this conversation.

- `/fix-web-accessibility <file>` Review the file against all rules below and report:
  - violations (quote the exact line or snippet)
  - why it matters (one short sentence)
  - a concrete fix (code-level suggestion)

Do not rewrite large parts of the UI. Prefer minimal, targeted fixes.

## standards and conformance target

- target [WCAG 2.2 Level AA](https://www.w3.org/TR/WCAG22/#conformance-reqs) by default, while honoring explicit project
  conformance requirements; AA covers both Level A and Level AA success criteria
- use the [WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/) to check applicable criteria and their
  exceptions; the rules below are a focused checklist, not a complete conformance audit
- include relevant WCAG 2.2 additions: obscured focus (2.4.11), alternatives to dragging (2.5.7), pointer target size
  (2.5.8), consistent help placement (3.2.6), repeated data entry (3.3.7), and accessible authentication (3.3.8)
- use [ARIA APG patterns](https://www.w3.org/WAI/ARIA/apg/patterns/) for widget semantics, keyboard interaction, states,
  and focus management; preserve native HTML behavior where it provides the needed interaction
- APG is [informative implementation guidance](https://www.w3.org/WAI/ARIA/apg/about/introduction/), and its examples
  require integration and testing; following a pattern alone does not establish WCAG conformance
- conformance applies to full pages and complete processes; a component review or passing automated scan cannot
  establish that the entire product conforms

## when to apply

Reference these guidelines when:

- adding or changing buttons, links, inputs, menus, dialogs, tabs, dropdowns
- building forms, validation, error states, helper text
- implementing keyboard shortcuts or custom interactions
- working on focus states, focus trapping, or modal behavior
- rendering icon-only controls
- adding hover-only interactions or hidden content

## rule categories by priority

These priorities are triage hints. Assess actual user impact and distinguish priority from WCAG conformance level.

| priority | category            | impact      |
| -------- | ------------------- | ----------- |
| 1        | accessible names    | critical    |
| 2        | keyboard access     | critical    |
| 3        | focus and dialogs   | critical    |
| 4        | semantics           | high        |
| 5        | forms and errors    | high        |
| 6        | announcements       | medium-high |
| 7        | contrast and states | medium      |
| 8        | media and motion    | low-medium  |
| 9        | tool boundaries     | critical    |

## quick reference

### 1. accessible names (critical)

- every interactive control must have an accessible name
- icon-only buttons must have aria-label or aria-labelledby
- every input, select, and textarea must be labeled
- links must have meaningful text (no “click here”)
- decorative icons must be aria-hidden

### 2. keyboard access (critical)

- do not use div or span as buttons without full keyboard support
- make every interaction operable by keyboard; use Tab between components and pattern-specific navigation within
  composite widgets, following [APG keyboard conventions](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/)
- focus must be visible for keyboard users
- do not use tabindex greater than 0
- Escape must close dialogs or overlays when applicable

### 3. focus and dialogs (critical)

- modals must trap focus while open
- restore focus to the trigger on close
- set initial focus inside dialogs
- opening a dialog should not scroll the page unexpectedly

### 4. semantics (high)

- prefer native elements (button, a, input) over role-based hacks
- if a role is used, required aria attributes must be present
- lists must use ul or ol with li
- do not skip heading levels
- tables must use th for headers when applicable

### 5. forms and errors (high)

- errors must be linked to fields using aria-describedby
- required fields must be announced
- invalid fields must set aria-invalid
- helper text must be associated with inputs
- disabled submit actions must explain why

### 6. announcements (medium-high)

- critical form errors should use aria-live
- loading states should use aria-busy or status text
- toasts must not be the only way to convey critical information
- expose expanded state through native semantics or aria-expanded; apply aria-controls according to the chosen pattern,
  since it is optional for the [disclosure pattern](https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/)

### 7. contrast and states (medium)

- ensure sufficient contrast for text and icons
- hover-only interactions must have keyboard equivalents
- disabled states must not rely on color alone
- do not remove focus outlines without a visible replacement

### 8. media and motion (low-medium)

- images must have correct alt text (meaningful or empty)
- videos with speech should provide captions when relevant
- respect prefers-reduced-motion for non-essential motion
- avoid autoplaying media with sound

### 9. tool boundaries (critical)

- prefer minimal changes, do not refactor unrelated code
- do not add aria when native semantics already solve the problem
- do not migrate UI libraries unless requested

## common fixes

```html
<!-- icon-only button: add aria-label -->
<!-- before -->
<button><svg>...</svg></button>
<!-- after -->
<button aria-label="Close"><svg aria-hidden="true">...</svg></button>

<!-- div as button: use native element -->
<!-- before -->
<div onclick="save()">Save</div>
<!-- after -->
<button onclick="save()">Save</button>

<!-- form error: link with aria-describedby -->
<!-- before -->
<input id="email" /> <span>Invalid email</span>
<!-- after -->
<input id="email" aria-describedby="email-err" aria-invalid="true" /> <span id="email-err">Invalid email</span>
```

## review guidance

- fix critical issues first (names, keyboard, focus, tool boundaries)
- prefer native HTML before adding aria
- quote the exact snippet, state the failure, propose a small fix
- for complex widgets (menu, dialog, combobox), prefer established accessible primitives over custom behavior
- cite the success criterion and level for verified WCAG failures; identify APG recommendations and other best practices
  separately
- combine automated checks with manual keyboard, focus, zoom/reflow, and relevant screen-reader testing;
  [WAI evaluation guidance](https://www.w3.org/WAI/test-evaluate/tools/selecting/) explains the limits of automation.
  Report the tested scope, remaining issues, and checks that could not be performed
