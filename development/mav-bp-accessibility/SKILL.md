---
name: mav-bp-accessibility
description: Accessibility conventions for projects with user-facing interfaces. Covers WCAG 2.1 AA compliance, semantic HTML, keyboard navigation, colour contrast, screen reader support, and automated a11y testing. Applied when building or reviewing user-facing web or mobile applications.
user-invocable: false
disable-model-invocation: true
---

# Accessibility Standards

Ensure user-facing interfaces are usable by everyone, including people who rely on assistive technology.

## Maverick's Rules

- **WCAG 2.2 AA is the baseline, not the ceiling** — all user-facing interfaces must meet it.
- **Scope**: web and mobile UIs only. Does NOT apply to CLIs, REST/GraphQL APIs, backend services, batch jobs/workers/daemons, or internal build tools. If the project has no user-facing interface, skip this skill entirely.
- **Semantic HTML first** — native elements before ARIA. No ARIA is better than bad ARIA; never override native semantics; any custom ARIA widget must implement its full keyboard interaction pattern.
- **Automated accessibility testing must run in CI** (axe-core, Lighthouse CI, pa11y, eslint-plugin-jsx-a11y — whatever fits the stack). Automated tools catch only ~30% of issues; they are necessary but not sufficient.
- **Manual verification is required** for what automation misses: keyboard-only operation of the whole page (Tab/Shift+Tab/Enter/Space/Escape/arrows, no traps outside modals), screen reader announcement of labels, errors, and dynamic content, and focus management in modals and SPA route changes (trap in dialog, restore to trigger on close).
- **Zoom and reflow**: content usable at 200% zoom; no horizontal scrolling at 320px viewport width.
- **Auto-playing media is prohibited** — playback must be user-initiated.
- **Focus indicators**: never `outline: none` without a `:focus-visible` replacement; indicators need at least 3:1 contrast against the surrounding background.
- **Never use colour alone** to convey state — pair it with text, an icon, or a pattern.

## Project Implementation Lookup

Check for `docs/maverick/skills/accessibility/SKILL.md`. If present, read it and follow it — it wins on specifics (library, config, conventions). If missing, proceed with these standards and note the gap in your summary.

## Detecting Accessibility Issues in Code Review

When reviewing code for user-facing interfaces, flag these patterns:

| Pattern | Issue | Fix |
| ------- | ----- | --- |
| `<div onclick="...">` | Non-semantic interactive element | Use `<button>` or `<a>` |
| `outline: none` without replacement | Invisible focus indicator | Add `focus-visible` style |
| `<img>` without `alt` attribute | Missing text alternative | Add descriptive `alt` or `alt=""` for decorative |
| `<input>` without associated `<label>` | Unlabelled form field | Add `<label for="...">` |
| Colour alone indicates state | Inaccessible to colour-blind users | Add icon, text, or pattern |
| `tabindex` value > 0 | Breaks natural tab order | Use `tabindex="0"` or `-1` only |
| `aria-hidden="true"` on focusable element | Hidden but still keyboard-reachable | Remove from tab order or remove `aria-hidden` |
| Auto-playing video or audio | Disruptive, not user-initiated | Require explicit play action |
| Placeholder used as label | Label disappears on input, poor contrast | Add a visible `<label>` |
| Missing `lang` attribute on `<html>` | Screen reader uses wrong language | Add `<html lang="en">` (or appropriate language) |
| Custom widget without keyboard handling | Inoperable for keyboard users | Implement full keyboard interaction pattern |
| Error shown only by colour change | Screen readers cannot detect colour | Add text message and `aria-describedby` |

<!-- maverick-plugin-version: 4.0.2-dev -->
