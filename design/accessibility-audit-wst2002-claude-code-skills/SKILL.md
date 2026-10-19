---
name: accessibility-audit
description: Use when checking a website, web app or UI component for accessibility, WCAG or a11y compliance, screen reader or keyboard support, color contrast, ARIA usage, or fixing issues reported by axe, Lighthouse or an accessibility review.
---

# Accessibility Audit

## Overview

Check that everyone can perceive, operate and understand the interface: with a keyboard only, with a screen reader, with zoom, and with low vision. Fix issues in the components that produce them so the fix applies everywhere they are used.

## Method

1. **Automated scan** if a URL is available: `npx @axe-core/cli <url>` or Lighthouse accessibility. Automated tools find about a third of issues; treat results as a starting point.
2. **Code review** of components with the checklist below: forms, buttons, links, images, modals, menus, tabs, tables, custom widgets.
3. **Keyboard pass:** Tab through every interactive element. Focus visible, logical order, nothing unreachable, no focus traps, Escape closes overlays, focus returns to the trigger.
4. **Screen reader semantics:** every control has a role, an accessible name and its state (expanded, selected, checked, invalid).
5. **Report** with the contract below, mapped to WCAG 2.2 AA.

## Checklist

| Area | Requirement (WCAG) |
|---|---|
| Images | Informative images have meaningful `alt`; decorative ones `alt=""` (1.1.1) |
| Contrast | Text 4.5:1, large text and UI components 3:1 (1.4.3, 1.4.11) |
| Color | Information not conveyed by color alone (1.4.1) |
| Structure | One `h1`, ordered headings, landmarks (`header`, `nav`, `main`, `footer`), lists as lists (1.3.1) |
| Forms | Every input has a `<label>`; errors named in text and linked with `aria-describedby`; required marked (1.3.1, 3.3.1, 3.3.2) |
| Controls | Actions are `<button>`, navigation is `<a href>`; no clickable `div` without role, tabindex and key handlers (2.1.1, 4.1.2) |
| Focus | Visible focus indicator; never `outline: none` without a replacement (2.4.7) |
| Modals and menus | Focus moves in, is trapped while open, Escape closes, focus returns (2.1.2, 2.4.3) |
| Names | Icon-only buttons have `aria-label`; link text makes sense out of context (2.4.4, 4.1.2) |
| Motion | Respect `prefers-reduced-motion`; no auto-playing motion longer than 5 s without pause (2.2.2, 2.3.3) |
| Zoom and reflow | Usable at 200% zoom and 320 px width without horizontal scroll (1.4.4, 1.4.10) |
| Targets | Touch targets at least 24×24 px (2.5.8) |
| Language | `<html lang>` set (3.1.1) |

ARIA rule: prefer native HTML elements. Add ARIA only when no native element fits, and then implement the full keyboard behavior of that pattern.

## Output contract

```
### [Critical | Serious | Moderate | Minor] Title — WCAG <criterion>
- Where: component and file:line (and URL if relevant)
- Who is affected: keyboard users, screen reader users, low vision, etc.
- Fix: corrected markup or CSS
```

Critical = blocks a task for some users (cannot submit a form by keyboard). End with **Passed checks** and **Needs manual testing** (items that require a real screen reader session).

## Common mistakes

- `div` or `span` with `onClick` instead of a `button`.
- Placeholder text used as the only label.
- `aria-label` that contradicts the visible text.
- `role="button"` added without Enter and Space key handling.
- Claiming WCAG compliance from an automated scan alone.

---

Made by **Wageesha Tripathi** · [LinkedIn](https://www.linkedin.com/in/wst2002/) · [Email](mailto:tripathiwageesha2002@gmail.com) · [More skills](https://github.com/WST2002/claude-code-skills)
