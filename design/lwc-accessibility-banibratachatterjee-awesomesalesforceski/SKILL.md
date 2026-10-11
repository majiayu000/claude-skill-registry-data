---
name: lwc-accessibility
description: "Use when designing or reviewing Lightning Web Components for keyboard access, semantic labeling, focus management, screen-reader behavior, and WCAG-aligned UX in Salesforce. Triggers: 'lwc accessibility', 'keyboard navigation in lwc', 'screen reader labels', 'focus trap in modal'. NOT for Apex or sharing security reviews, or for purely visual SLDS styling that does not affect accessibility behavior."
category: lwc
salesforce-version: "Spring '25+'"
well-architected-pillars:
  - User Experience
  - Security
tags:
  - lwc-accessibility
  - keyboard-navigation
  - aria
  - focus-management
  - screen-reader
triggers:
  - "keyboard navigation is broken in my lwc"
  - "screen reader cannot understand this component"
  - "how should i manage focus in an lwc modal"
  - "need aria labels or alternative text in lwc"
  - "custom lwc is not accessible"
inputs:
  - "which base components, custom markup, and interactive states the component uses"
  - "whether the issue affects keyboard users, screen readers, or both"
  - "where focus should land on open, error, save, and close transitions"
outputs:
  - "accessibility review findings for semantics, labels, focus, and keyboard behavior"
  - "remediation plan for WCAG-aligned LWC interaction design"
  - "recommended component or markup changes to reduce accessibility risk"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-03-15
---

Use this skill when a Lightning Web Component looks correct visually but may fail for keyboard users or assistive technology. The highest-value move in LWC accessibility work is usually to remove custom interaction code and return to accessible base components, then handle the few remaining focus and labeling gaps deliberately.

---

## Before Starting

Gather this context before working on anything in this domain:

- Which parts of the UI are interactive: buttons, menus, tabs, dialogs, inline actions, or custom pickers?
- Is the component built mostly from `lightning-*` base components, SLDS blueprint markup, or custom HTML?
- Where should focus move after the user opens a modal, triggers validation errors, saves, or cancels?

---

## Core Concepts

Accessibility in LWC is easiest when the component stays close to platform primitives. Salesforce base components already carry keyboard behavior, labeling support, and SLDS-aligned semantics. The farther a team moves toward clickable `div` elements, custom focus logic, and manual ARIA, the more likely it is to recreate a solved problem badly.

### Base Components First

Start with a base component whenever one exists. The LWC accessibility guidance explicitly points teams toward accessible base components and SLDS blueprints because they provide tested interaction and assistive-tech support out of the box. A custom menu button or faux toggle should be a last resort, not a default pattern.

### Accessible Name Beats Visual Guesswork

Interactive elements need a clear accessible name. In practice that means real button text, a visible or hidden label on inputs, and `alternative-text` on icons that communicate meaning. ARIA should sharpen semantics where needed, but it should not be used to patch over structurally wrong markup such as a clickable `span`.

### Focus Is Part Of The Contract

Dialogs, drawers, popovers, and error states need an intentional focus plan. Users must land on the first actionable or context-setting element, remain inside a modal interaction while it is open, and return to the launcher when it closes. If focus disappears after rerender or save, the component is functionally broken for keyboard users.

### Validation Must Be Programmatic

Error text cannot live only in color or layout. Inputs need programmatic error association and clear state changes. In Salesforce UI, this usually means using the built-in validation behavior of base form components where possible, and reserving custom validation wiring for truly custom input experiences.

---

## Common Patterns

### Base-Component Replacement For Custom Click Targets

**When to use:** The component currently uses custom HTML such as a clickable `div`, icon-only action, or hand-rolled toggle.

**How it works:** Replace the interactive surface with `lightning-button`, `lightning-button-icon`, `lightning-input`, or another standard base component. Keep any remaining custom markup decorative, not interactive.

**Why not the alternative:** Adding `tabindex`, `role`, and key handlers to arbitrary markup usually creates incomplete keyboard behavior and inconsistent screen-reader output.

### Deliberate Focus Management Around Dialogs

**When to use:** The component opens a modal, quick action surface, or blocking overlay.

**How it works:** Use `LightningModal` or another supported dialog surface, set focus on meaningful content or the first actionable control, and return focus to the launch element when the interaction closes.

**Why not the alternative:** Leaving focus wherever the browser last had it makes the overlay hard to use and easy to lose.

### Accessible Composite Widget Boundary

**When to use:** A real business need requires a custom picker, listbox, or multi-step composite component.

**How it works:** Choose a known WAI-ARIA interaction pattern, document the keyboard contract, and test it with both tab order and screen-reader announcements before shipping.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Standard action, toggle, or input | Use a `lightning-*` base component | Accessible behavior is already implemented and maintained by the platform |
| Need branded layout but normal semantics | Use an SLDS blueprint with minimal custom behavior | Keeps semantics closer to supported interaction models |
| Need a modal or blocking overlay | Use `LightningModal` with an explicit focus plan | Modal semantics and dismissal behavior are easier to keep correct |
| Considering ARIA on a clickable `div` | Replace it with semantic HTML or a base component | ARIA does not fully repair incorrect structure |
| Custom composite widget is unavoidable | Implement and test a formal keyboard model | Composite controls need a documented accessibility contract |

---


## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org edition, relevant objects, and current configuration state
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Core Concepts and Common Patterns sections above
4. Validate — run the skill's checker script and verify against the Review Checklist below
5. Document — record any deviations from standard patterns and update the template if needed

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] Every interactive surface is semantic HTML or a supported base component.
- [ ] Inputs, buttons, and meaningful icons have a clear accessible name.
- [ ] Focus order matches the visible reading order and business flow.
- [ ] Modal or overlay interactions trap and restore focus intentionally.
- [ ] Validation feedback is programmatic and not color-only.
- [ ] Keyboard-only testing covers open, close, save, cancel, and error states.

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **`lightning-icon` needs deliberate text when it carries meaning** - icon-only affordances look obvious visually but become vague or silent to assistive technology without `alternative-text`.
2. **Custom HTML can regress below the platform baseline quickly** - moving away from `lightning-*` components often removes built-in keyboard and label behavior teams assumed they still had.
3. **Focus can get lost after rerender** - conditional templates, async state changes, and modal open or close transitions can strand keyboard users unless focus is restored deliberately.
4. **ARIA does not replace semantic structure** - adding roles to the wrong element can still produce confusing navigation and announcement behavior.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Accessibility review | Findings on semantic markup, labels, keyboard interaction, and focus behavior |
| Remediation plan | Concrete changes to base components, ARIA usage, and focus handling |
| Test checklist | Keyboard and screen-reader scenarios that should pass before release |

---

## Related Skills

- `lwc/lwc-modal-and-overlay` - use when the main problem is dialog choice and overlay lifecycle rather than general accessibility posture.
- `lwc/lwc-forms-and-validation` - use when the accessibility issue is mainly inside form validation and record-edit UX.
- `lwc/lwc-testing` - use alongside this skill to turn accessibility expectations into repeatable component tests.
