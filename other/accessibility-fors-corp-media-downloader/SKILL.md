---
name: accessibility
description: Accessibility (a11y) practices for any UI work — web, mobile, or desktop. Use when building or reviewing user-facing screens/components, forms, navigation, color/contrast choices, or anything involving images, icons, or custom interactive widgets.
---

# Accessibility

Applies regardless of framework — the specifics below are grouped by platform, but
the underlying principle is universal: someone using a keyboard only, a screen
reader, or with low vision/color blindness should be able to do everything a mouse
user with full-color vision can do.

## Universal checklist (any platform)

- **Semantics over styling.** Use the platform's real interactive elements (button,
  link, checkbox, native list/table) instead of a styled `div`/`View` with a click
  handler. Custom widgets need explicit roles/labels to compensate for what native
  elements give you for free.
- **Everything reachable by keyboard/switch control alone**, in a logical order, with
  a visible focus indicator. Never remove a focus outline without providing an
  equally visible replacement.
- **Every non-decorative image/icon has a text alternative.** Purely decorative
  images are marked as such (empty alt, `aria-hidden`, decorative flag) so screen
  readers skip them instead of reading noise.
- **Color is never the only signal.** Error states, required fields, status
  indicators, chart series — pair color with text, icon, or pattern.
- **Contrast**: body text ≥ 4.5:1, large text/icons ≥ 3:1 (WCAG AA). Check this
  against the actual rendered color, not the design token name.
- **Forms**: every input has a programmatically associated label (not just adjacent
  text), inline errors are announced to assistive tech and tied to their field, and
  validation doesn't rely on color/shape alone.
- **Motion**: respect the user's reduced-motion preference; nothing flashes more
  than 3x/second.
- **Don't trap focus** in a modal/dialog beyond its own boundary, and return focus to
  a sensible place when it closes.

## Web (HTML/React/Vue/etc.)

- Prefer semantic HTML5 elements (`<nav>`, `<main>`, `<button>`) over ARIA on a
  `<div>` — ARIA is a patch for when semantic HTML genuinely can't express the
  widget (e.g. a combobox), not a first choice.
- One `<h1>` per page, headings in strict order (no skipping levels for style).
- Live regions (`aria-live`) for async updates a sighted user would notice visually
  (toast, inline validation, loading → loaded).
- Test with a keyboard alone (Tab/Shift+Tab/Enter/Space/Esc/arrow keys) and with the
  browser's accessibility tree inspector before calling a component done — automated
  linters (axe, eslint-plugin-jsx-a11y) catch maybe half of real issues.

## Mobile (iOS/Android)

- Set accessibility labels/hints on custom controls (`accessibilityLabel` /
  `contentDescription`); group related elements so VoiceOver/TalkBack don't read
  fragments out of context.
- Respect Dynamic Type / font-scale settings — don't hardcode text sizes that break
  layout when the user scales text up.
- Minimum touch target ~44x44pt (iOS) / 48x48dp (Android).

## Desktop (native/Electron/Tauri)

- Same keyboard-navigation and focus-order rules apply; native toolkits expose an
  accessibility tree (UIA/AX/AT-SPI) — verify custom-drawn controls actually appear
  in it, not just visually.

## When reviewing, not building

Ask the same questions a reviewer would: can this be done with keyboard only, does
every interactive element have an accessible name, does removing color leave the
state legible. Flag findings the same way `reviewer-correctness`/`reviewer-security`
do — concrete element, concrete failure, not a vague "improve accessibility."
