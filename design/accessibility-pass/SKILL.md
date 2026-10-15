---
name: accessibility-pass
description: Run a hands-on accessibility pass on a web page or component - keyboard walk, focus visibility, names and roles, live announcements, reduced motion, contrast and zoom - verifying each check in a real browser rather than by reading code. Use before shipping UI, or when asked to check or fix accessibility.
---

# /accessibility-pass

Every check below says **how to verify it**. Reading the code is not verification; use a real browser (Playwright, or the browser tools you have) and observe.

## 1. Keyboard walk

- Load the page, click nothing, and press Tab repeatedly from the top. Record each focused element: `document.activeElement` tag, role and accessible name.
- **Pass when:** every interactive element is reached, in reading order, and nothing that isn't interactive takes focus. No focus trap except inside an open dialog.
- Operate every control with the keyboard only: Enter and Space on buttons, arrows in tabs, radios, sliders, menus and listboxes, Escape to close anything that opens.
- **Composite widgets** (tabs, menus, listboxes, grids) should be one Tab stop with arrow keys inside (roving tabindex or `aria-activedescendant`).
- **Pass when** closing a popover, dialog or menu returns focus to the control that opened it, and deleting or moving an item leaves focus somewhere sensible, not on `<body>`.

## 2. Focus is visible

- For each focused element, take a screenshot or check computed styles. There must be a visible indicator with at least 3:1 contrast against its surroundings.
- Use `:focus-visible`, so mouse clicks don't leave rings but keyboard focus always shows.
- **Pass when** you can always tell where focus is from a screenshot alone.

## 3. Names, roles and states

- Query the accessibility tree (Playwright's `page.accessibility.snapshot()` or `getByRole` lookups).
- **Pass when:**
  - every control has a role and a name that says what it does ("Delete Q3 roadmap", not "button" or "×")
  - icon-only buttons have `aria-label`
  - toggles expose `aria-pressed` or `aria-checked`, and disclosures `aria-expanded`
  - the current page or step is marked with `aria-current`
  - inputs have real `<label>`s, and errors are tied to them with `aria-describedby`
- Images: decorative ones have `alt=""`; meaningful ones say what matters in them.
- Headings form an outline (one `h1`, no skipped levels for structure), and landmarks exist (`header`, `nav`, `main`, `footer`).

## 4. Changes are announced

- Anything that changes without a page load (a save, a toast, a filter count, an upload finishing, an error) must reach a screen reader.
- **Verify** by finding the live region (`role="status"` or `aria-live="polite"`, or `role="alert"` for errors) and checking that its text changes when the event happens.
- The text should make sense on its own: "3 edits not saved", not "Error".

## 5. Motion

- Emulate `prefers-reduced-motion: reduce` (Playwright: `reducedMotion: "reduce"` on the context) and reload.
- **Pass when:**
  - large movement, parallax, autoplay and looping animation stop or become fades
  - nothing depends on motion to be understood (a state shown only by an animation needs a static equivalent)
  - timers that expire (toasts, undo windows) can be paused by hover or focus, or extended
- If the component takes a `motion="reduced"` prop, check both paths.

## 6. Contrast, zoom and text

- Check text contrast from computed colours: 4.5:1 for body text, 3:1 for large text (24px, or 18.66px bold) and for UI boundaries and icons that carry meaning.
- **Colour is never the only signal:** errors say so in words, and statuses have a label or icon.
- Zoom to 200% (or set the viewport to 640px wide at DPR 2). **Pass when** nothing is cut off or overlapping, and there's no horizontal scroll for text content.
- Set a 24×24px minimum for touch targets, or give smaller targets enough spacing.

## 7. Report

For each failure: what it is, where it is, how you verified it, and the fix. Group by severity:

- **Blocks use:** can't reach or operate something.
- **Hard to use:** confusing names, lost focus, missing announcements.
- **Polish.**

Fix what you can, then re-run the checks that failed and say so.
