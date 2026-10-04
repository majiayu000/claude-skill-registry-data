---
name: a11y-audit
description: "Accessibility audit of a page or flow: axe-core, Lighthouse, and a WCAG 2.2 AA manual checklist, severity-ranked with fixes. Use for an a11y audit, WCAG conformance, screen reader or keyboard testing, or contrast ratios. Building accessible components belongs to web-dev-frontend."
license: MIT
metadata:
  display-name: "Accessibility Audit"
  version: "1.1"
  platforms: "claude-code codex"
  tags: "accessibility wcag audit testing"
---

# Accessibility audit

This is a dedicated *audit pass* over a page or flow - distinct from building accessible components (that's `web-dev-frontend`). You are measuring conformance against WCAG 2.2 AA and producing a findings list, not shipping the fixes.

## Automated first pass (necessary, not sufficient)

- Run **axe-core** (`@axe-core/cli`, or `@axe-core/playwright` inside an E2E test) on each page/state.
- Run **Lighthouse** accessibility category for a second opinion and a score.
- Automated tools catch roughly a third of issues. **Never stop here** - keyboard, focus, and screen-reader problems mostly don't show up automatically.

## Manual checklist (WCAG 2.2 AA)

- **Keyboard:** every interactive element is reachable and operable by keyboard; focus order is logical; focus ring is visible; no keyboard traps; `Esc` closes overlays.
- **Screen reader:** run VoiceOver / NVDA through the flow. Every control announces a **name, role, and state**. Landmarks (`main`, `nav`, `header`) are present.
- **Structure:** exactly one `<h1>`; headings don't skip levels; lists are real lists; semantic landmarks over `<div>` soup.
- **Forms:** every input has a programmatic `<label>` (not just a placeholder); errors are associated (`aria-describedby`) and announced; required state conveyed non-visually.
- **Contrast:** body text ≥ 4.5:1, large text ≥ 3:1, UI components/graphics ≥ 3:1. Never convey meaning by colour alone.
- **Images & media:** meaningful `alt`, or `alt=""` for decorative; captions/transcripts for audio/video.
- **Dynamic content:** async updates announced via `aria-live`; modals trap focus and return it to the trigger on close; `prefers-reduced-motion` respected.
- **Zoom & reflow:** 200% zoom loses no content/function; at 320px width there's no horizontal scroll (reflow).
- **Target size (2.2):** interactive targets ≥ 24×24 CSS px (or have adequate spacing).

## Static review (no browser)

When reviewing a diff rather than a running page - no axe-core, no Lighthouse, no screen reader - check what the markup and styles can tell you without executing them, and say plainly that this is a static pass, not a substitute for the automated and manual passes above:

- Semantic elements and ARIA roles/attributes are present and correctly paired (a `role="button"` div also gets a keyboard handler and `tabindex`).
- Every form control's label, in the markup, either wraps it or matches its `for`/`id`.
- Interactive elements are real buttons/links/inputs, not a `<div onClick>`.
- Colour tokens against the design system's own contrast pairs, where the values are visible in the diff.
- `alt` text is present and isn't the filename.

## Reporting findings

Rank by user impact:

- **Blocker** - an assistive-tech user cannot complete the task (unlabeled submit, keyboard trap, invisible focus).
- **Serious** - major barrier with a workaround (poor contrast on key text, missing headings).
- **Moderate / Minor** - friction or best-practice gaps.

For each finding give: the **WCAG success criterion** (e.g. 1.4.3, 2.4.7, 2.5.8), the **location** (page + element/selector), the **user impact**, and the **specific fix**.

## What this skill is *not*

- Not the fix step - hand remediation to `web-dev-frontend`, which owns building accessible components.
- Not a substitute for real AT testing - the manual pass with an actual screen reader is where the real findings come from.
