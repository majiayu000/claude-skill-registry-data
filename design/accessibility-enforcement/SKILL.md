---
name: accessibility-enforcement
description: Enforce WCAG 2.2 AA on every UI change. Audit focus order, keyboard traps, ARIA correctness, color contrast, focus visibility, and color-never-alone rules. Use when building or reviewing any UI component, running a design review, or preparing a regulated-customer release.
---

# Skill: Accessibility Enforcement (WCAG 2.2 AA)

Accessibility is not optional for Concept2Cure's regulatory customers (FDA, EMA, PMDA, Health Canada, enterprise pharma). Many of them require WCAG 2.2 AA conformance in procurement. Every shipped component must meet this bar.

## Activation

This skill activates when:

- Building, editing, or reviewing any React component in `client/src/`
- Running `design-review` or `design-flow`
- Preparing a release or a regulated-customer deliverable
- Touching focus management, form fields, modal/dialog behavior, tables, or chat UI

## Hard Rules (WCAG 2.2 AA — NON-NEGOTIABLE)

1. **Keyboard-first**. Every interactive element MUST be reachable and operable with keyboard alone (`Tab`, `Shift+Tab`, `Enter`, `Space`, arrows where semantic). No mouse-only controls.
2. **Focus visible**. Every focusable element MUST show a focus ring. Default: `focus-visible:ring-2 focus-visible:ring-stone-400`. Do NOT remove outlines without a replacement indicator.
3. **Focus order matches visual order**. Tab order must follow reading order. No `tabIndex` > 0. Use DOM order to control flow.
4. **No keyboard traps**. Users must be able to move focus out of any widget (including custom chat composers, modals, editors) with `Tab` or `Escape`.
5. **Contrast ratios (normal text ≥ 4.5:1, large text ≥ 3:1, UI components ≥ 3:1)**. Verify every text-on-surface pairing in the stone palette. `text-stone-400 on bg-white` is typically insufficient for body text — use `text-stone-600` or darker.
6. **Color is never the sole signal**. Status, errors, required fields, and state changes MUST also use text, icon, pattern, or shape — not color alone. `<WorkspaceStatusBadge>` is correct; a bare colored dot is not.
7. **Semantic HTML first**. Use `<button>`, `<nav>`, `<main>`, `<dialog>`, `<table>` with `<th scope>` before reaching for `role="..."`. Only add ARIA when semantics cannot be expressed natively.
8. **Accessible names**. Every button, input, icon-only control, and image MUST have an accessible name — `aria-label`, `aria-labelledby`, visible text, or `<label htmlFor>`. Decorative icons use `aria-hidden="true"`.
9. **Live regions for dynamic content**. Toasts, inline error messages, streaming chat tokens, and async status changes MUST announce via `role="status"` / `role="alert"` / `aria-live`. The `statesV2` components already handle this — use them.
10. **Reduced motion**. Any animation > 200ms or with parallax/transform MUST respect `prefers-reduced-motion: reduce` and fall back to a static state.
11. **Touch targets ≥ 44×44 px** (WCAG 2.2 SC 2.5.8) on touch surfaces. Desktop chat and editor are exempt; mobile overlays and portal are not.
12. **Form errors are associated**. Field errors use `aria-describedby` pointing to the error element, and `aria-invalid="true"` on the field. `<FormField>` does this automatically — use it.

## Before Shipping a Component, Verify

- Can I `Tab` to every interactive element in order?
- Does every focus stop show a visible ring?
- Can I dismiss modals/panels with `Escape`?
- Do inputs have labels (visible or `aria-label`)?
- Are error messages announced (role="alert" or inside a live region)?
- Are icon-only buttons named?
- Would a screen reader understand the page structure (`<h1>`–`<h6>` hierarchy, landmarks)?
- Does every color-coded signal also have a text/icon companion?

## Forbidden Patterns

| Forbidden | Use Instead |
| --- | --- |
| `<div onClick={...}>` for a button | `<Button>` from the governed registry |
| `outline: none` / `focus:outline-none` without replacement | `focus-visible:ring-2 focus-visible:ring-stone-400` |
| `tabIndex={5}` to control order | Fix DOM order; use `tabIndex={0}` / `-1` only |
| Color-only error indication | Text + icon + color |
| Icon-only button with no `aria-label` | Add `aria-label="Close"` etc. |
| `<img>` without `alt` | `alt="..."` or `alt=""` (decorative) |
| Toast using bare `console.log` or `alert()` | `useToast()` (provides `role="status"`) |
| Modal without focus trap + `Escape` | Use governed `<Dialog>` (Radix) — already correct |
| Animated transitions ignoring reduced-motion | Wrap in `@media (prefers-reduced-motion: no-preference)` or use `motion-safe:` |

## Tooling

- **Unit/integration**: `@testing-library/react` + `jest-axe` for automated violations
- **E2E**: Playwright has `axe-playwright` — wire into `design-review` runs
- **Manual**: Tab through the page; use VoiceOver (Mac) or NVDA (Windows) for at least the critical flows (login, chat, document editor, submission workflow)

## Completion Gate

A UI change is NOT complete until:

- Axe checks pass (or known-acceptable exceptions are documented)
- Keyboard-only pass completed
- Focus ring visible on every new interactive element
- Every new icon-only control has an accessible name
- Color contrast checked on every new text-on-surface pairing

Flag any accessibility regression to the user explicitly — do not silently ship.
