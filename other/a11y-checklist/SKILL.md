---
name: a11y-checklist
description: WCAG 2.2 AA quick reference — semantics, keyboard, names, states, contrast, motion, errors. Use when building or reviewing UI components.
---

# Accessibility checklist (WCAG 2.2 AA)

Use this as a walk-through, top to bottom. If you can't answer "yes" or "N/A" for a line, fix it.

## Semantics
- [ ] The element matches the intent. `<button>` for actions. `<a>` for navigation. Lists use `<ul>`/`<ol>`. Landmarks use `<main>`/`<nav>`/`<header>`/`<footer>`/`<aside>`.
- [ ] Headings form a valid outline — one `<h1>`, no skipped levels.
- [ ] Forms have `<label>`s (or `aria-labelledby`). Placeholder is not a label.

## Keyboard
- [ ] Every interactive element is reachable by `Tab`.
- [ ] Focus order matches visual order.
- [ ] No focus traps. Modals trap focus only while open and restore on close.
- [ ] Focus is visible (outline, ring, or theme equivalent). Don't remove `:focus-visible` without replacement.
- [ ] Keyboard shortcuts don't collide with screen-reader virtual cursor.

## Names & descriptions
- [ ] Every interactive control has an accessible name. Icon-only buttons: `aria-label`.
- [ ] Images: meaningful `alt`; decorative `alt=""`.
- [ ] Form errors are programmatically associated via `aria-describedby`.

## States
- [ ] `aria-expanded`, `aria-selected`, `aria-pressed`, `aria-checked`, `aria-invalid` reflect the current state and update as it changes.
- [ ] Loading states have `aria-busy` or a live region announcement.
- [ ] Async status changes are announced in a `role="status"` or `role="alert"` live region (use `alert` sparingly — it's interruptive).

## Contrast
- [ ] Normal text ≥ 4.5:1 vs background.
- [ ] Large text (≥ 18pt or 14pt bold) ≥ 3:1.
- [ ] UI components (form borders, focus rings, icon glyphs) ≥ 3:1.
- [ ] Don't rely on color alone to convey meaning — error state must have an icon or text too.

## Motion
- [ ] Respect `prefers-reduced-motion`. No auto-animating carousels, parallax, or transitions without the opt-out.
- [ ] Videos under 5s ok; longer needs pause/stop controls.
- [ ] No flashing over 3 times per second in any region larger than ~25% of the viewport.

## Structure & navigation
- [ ] Page has a `<main>` landmark and a sensible `lang` on `<html>`.
- [ ] Skip-to-content link at the top (or equivalent landmark structure).
- [ ] Page title is descriptive and unique per route.

## Errors & status
- [ ] Inline errors say *what* was wrong and *how to fix* ("Email must include an @").
- [ ] Errors appear near the input, are announced to AT, and don't rely solely on color.
- [ ] Required fields are marked both visually and programmatically (`aria-required` or `required`).

## Testing
- [ ] Keyboard-only pass: unplug the mouse, try the flow.
- [ ] Screen-reader pass (VoiceOver / NVDA) on critical flows.
- [ ] axe or similar linter in CI — treat findings as bugs, not noise.

## Smells
- `role="button"` on a `<div>` — use `<button>` instead
- `aria-hidden` on interactive content — almost always wrong
- Tabindex > 0 — almost always wrong
- "Click here" link text — unhelpful out of context

## Success criteria quick map
Common SCs you'll cite: 1.1.1 (non-text alt), 1.3.1 (info and relationships), 1.4.3 (contrast), 2.1.1 (keyboard), 2.4.3 (focus order), 2.4.7 (focus visible), 3.3.1 (error identification), 4.1.2 (name, role, value), 4.1.3 (status messages).
