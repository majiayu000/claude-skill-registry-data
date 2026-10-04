---
name: accessibility
description: Use when building UI that ships to users, when reviewing for WCAG AA compliance, when adding keyboard navigation, when ensuring screen reader support, when auditing color contrast, or when preparing a UI surface for an EU or government customer.
---

# Accessibility

## Overview

Establish WCAG AA as the baseline floor for every UI surface — *before* it ships. Output is `.forge/accessibility.md` — the semantic-HTML rules, the ARIA usage policy, keyboard navigation requirements, focus management rules, contrast policy, reduced-motion respect, and the screen-reader testing checklist. Pairs with `design-system` (which defines the visual tokens that meet contrast) and `interaction-patterns` (which defines the keyboard and focus contract).

## When to Use

- A UI surface is going to production and there's no accessibility audit
- The product ships to EU, government, healthcare, or education customers (legal requirement)
- A user reports that they can't use a feature with keyboard or screen reader
- A new component category is being added (modal, drawer, command palette) and focus management is unclear
- An existing UI is being audited and ARIA usage looks suspicious

## When NOT to Use

- Internal CLI tools or backend services with no UI
- Throwaway prototypes that will never ship
- Single one-line copy changes that don't touch interaction or structure

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "Accessibility is a nice-to-have" | It's a legal requirement in most markets (ADA in US, EAA in EU, AODA in Canada) and a usability requirement everywhere. |
| "We'll add it later" | Retrofitting a11y costs 10x building it in. Every component pattern picked without a11y becomes a refactor. |
| "Our users don't need it" | You don't know that — assistive tech use is often invisible. ~20% of users have a disability in some form. |
| "ARIA fixes everything" | ARIA overuse is worse than no ARIA. Native semantic HTML always beats `<div role="button">`. |
| "Just make the visible thing look right" | Screen readers see structure, not pixels. A visually-correct page can be unusable with VoiceOver. |
| "Color is enough to signal state" | Colorblind users can't see red-vs-green; every meaningful color needs a text or icon backup. |

## Red Flags

- A `<div onClick={...}>` instead of `<button>` (not keyboard accessible by default)
- ARIA roles applied to elements that already have native semantics (`<button role="button">` is a smell)
- `outline: none` on a focusable element with no replacement focus-visible style
- A modal that doesn't trap focus, doesn't return focus on close, or can't be closed with `Esc`
- A form `<input>` without a `<label>` (or `aria-label` for icon-only)
- Color used as the only signal for state (red = error, green = success, no icon, no text)
- An animation that violates `prefers-reduced-motion`
- A heading skipped (`<h1>` followed by `<h3>` with no `<h2>`)
- Image with no `alt` (or `alt=""` for non-decorative images)

## Core Process

### Step 1: Establish WCAG AA baseline

In `.forge/accessibility.md`, declare the conformance target (AA at minimum for most products; AAA only where regulatory). Document which assistive technologies are tested against:
- VoiceOver on macOS Safari
- VoiceOver on iOS Safari
- NVDA on Windows Firefox
- TalkBack on Android Chrome

### Step 2: Audit semantic HTML usage

The rule: **prefer native elements over ARIA every time.**

| Use | Not |
|---|---|
| `<button>` | `<div role="button">` |
| `<a href>` | `<div onClick={navigate}>` |
| `<input type="checkbox">` | `<div role="checkbox">` |
| `<dialog>` or `<div role="dialog">` *with* focus trap and labelling | `<div className="modal">` |
| `<nav>`, `<main>`, `<aside>`, `<header>`, `<footer>` | `<div>` everywhere |
| `<ul>`/`<li>` for lists | A pile of `<div>`s |

Run a structural audit: every interactive element is a native interactive element, or has a documented reason it isn't.

### Step 3: Review ARIA usage (sparingly)

The rules for ARIA:
1. **No ARIA is better than bad ARIA.** A wrong `aria-label` lies to screen readers.
2. **Use ARIA only when native semantics aren't enough** — e.g., to announce live regions (`aria-live`), to label icon-only buttons (`aria-label`), to associate hint text (`aria-describedby`), to wire combobox/listbox patterns that have no native equivalent.
3. **Never add a role that the element already has.** `<button role="button">` is a smell.
4. **Test what ARIA does** — open VoiceOver and listen, don't trust the visual inspector.

### Step 4: Verify keyboard navigation

For every interactive element and every page:
- Tab order matches visual reading order
- Every interactive element has a visible focus-visible style (2px outline, sufficient contrast)
- `Esc` closes any modal, drawer, popover, command palette
- Focus is trapped inside modals (no Tab leak to background)
- Focus returns to the trigger element when a modal closes
- Arrow keys work where they should (menus, lists, comboboxes, custom controls)
- `Enter` and `Space` both activate buttons; `Enter` activates links

Cross-reference `interaction-patterns` for the canonical keyboard contract.

### Step 5: Check color contrast

- **Body text:** 4.5:1 contrast against background (AA)
- **Large text (≥18pt or 14pt bold):** 3:1
- **Non-text UI components (icons, focus rings, borders that convey state):** 3:1
- **State conveyed by color** must also be conveyed by text or icon

Audit every token pairing in `design-system` — every text/background combination meets AA. Document the contrast ratio next to each token.

### Step 6: Verify motion respects `prefers-reduced-motion`

- Animations longer than 100ms are disabled when `prefers-reduced-motion: reduce` is set
- Parallax, autoplay, marquee, infinite carousels are off by default and require explicit user opt-in
- Essential motion (loading indicators) remains, but at minimal intensity

### Step 7: Create the screen reader testing checklist

For every UI surface before it ships:

- [ ] Tab through every focusable element in order — no missing or unreachable element
- [ ] VoiceOver reads each element with meaningful, non-redundant text
- [ ] Modals announce themselves on open and trap focus
- [ ] Form errors announce when they appear (`role="alert"` or live region)
- [ ] Loading states are announced (`aria-busy` + `aria-live="polite"`)
- [ ] Images have `alt` (decorative = empty `alt=""`)
- [ ] Headings form a valid outline (no skipped levels)

## Verification

- [ ] `.forge/accessibility.md` written with the conformance target
- [ ] Every interactive element is a native interactive element (or has documented ARIA + reason)
- [ ] No `<div onClick>` in the codebase (grep-verified)
- [ ] Every form input has a label (visible or `aria-label`)
- [ ] Contrast verified AA for every text/background token pairing
- [ ] No `outline: none` without a focus-visible replacement
- [ ] Every modal traps focus and restores it on close
- [ ] `prefers-reduced-motion` is respected (verified in a test or storybook)
- [ ] Last 3 UI PRs ran through the screen reader checklist
