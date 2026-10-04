---
name: accessibility
description: This skill should be used when building or reviewing UI for accessibility — keyboard navigation, screen readers, ARIA, color contrast, focus states, accessible forms, or WCAG compliance. Trigger phrases include "make it accessible", "a11y", "accessibility", "WCAG", "ARIA", "keyboard navigation", "screen reader", "color contrast", "focus states", "accessible form", "is this compliant", "EAA", "ADA". It targets WCAG 2.2 AA with concrete component rules and an axe-core test step.
---

# Accessibility

This skill makes interfaces usable by everyone — keyboard-only users, screen-reader users, low-vision users — and meets the legal bar (the EU Accessibility Act and ADA Title II both reference WCAG). Accessibility is not a nice-to-have; it's increasingly a legal requirement and always a larger addressable market.

Analogy: a curb cut was built for wheelchairs, but everyone with a stroller, suitcase, or bike uses it. Accessible UI is the same — built for those who need it, better for everyone.

## Dependencies

This skill is stronger when **Vercel's `web-design-guidelines` skill** (part of `vercel-labs/agent-skills`, ~27k⭐) is installed — it ships the ARIA/focus/keyboard checklist. Delegate the checklist to it when present; always pair with the axe-core test step below, which catches runtime violations a static checklist can't. **Never block on a missing dependency** — the rules below are the embedded fallback.

## The target

**WCAG 2.2 Level AA** — the bar referenced by the EU EAA, ADA Title II, and Section 508. Automated tools catch only ~30-40% of issues, so combine automated tests with manual checks.

## Discovery (max 3 questions, only if unknown)

1. Are you building new components or auditing existing UI?
2. Any specific complaint (keyboard trap, unreadable contrast, screen reader silent)?
3. Is there a CI pipeline where an a11y test could run?

## Step 1 — Semantic HTML first

Use native elements before ARIA: `<button>`, `<nav>`, `<main>`, `<label>`, `<a>`. **"No ARIA is better than bad ARIA"** — reach for ARIA only when no native element fits. Maintain a logical heading hierarchy (one `<h1>`, no skipped levels) and add a "skip to content" link.

## Step 2 — Keyboard & focus

- **Every interactive element reachable and operable by keyboard alone** (Tab / Shift-Tab / Enter / Space / Esc). Test by unplugging the mouse.
- **Never remove focus outlines without a replacement.** Style `:focus-visible` instead of `outline: none`.
- No keyboard traps — focus must be able to leave any widget (modals: trap *within* while open, release on close).

## Step 3 — Forms

- Every input has a programmatically associated `<label>` (or `aria-label`).
- Link errors with `aria-describedby` + set `aria-invalid` on the field.
- Don't rely on color alone to signal errors — add text/icon.

## Step 4 — Color & targets

- Contrast **≥ 4.5:1** for normal text, **≥ 3:1** for large text and UI components/focus indicators.
- Touch targets **≥ 24×24px** (WCAG 2.2 SC 2.5.8); 44×44px recommended for primary actions.

## Step 5 — Dynamic content & motion

- Announce async updates (toasts, validation, loading) with an `aria-live="polite"` region.
- Honor `prefers-reduced-motion` — gate non-essential animation behind it (also a WCAG 2.3.3 requirement). Coordinate with the `ui-design` motion settings.

## Step 6 — Test it

- Add `jest-axe` and assert per component: `expect(await axe(container)).toHaveNoViolations()`. Run it in CI.
- Manually test one full flow with a real screen reader (VoiceOver on macOS, NVDA on Windows) — automated tools can't judge whether the announced experience makes sense.

## Output

Deliver: the accessible components (semantic markup, labels, focus handling), the contrast/target fixes, an `aria-live` region for dynamic status, and a `jest-axe` test wired into CI.

## Reference

w3c/wcag (WCAG 2.2), dequelabs/axe-core (~7k⭐), nickcolley/jest-axe, vercel-labs/agent-skills `web-design-guidelines`.
