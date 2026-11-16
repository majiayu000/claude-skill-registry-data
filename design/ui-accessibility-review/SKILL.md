---
name: ui-accessibility-review
description: Audit a web interface for accessibility and interaction quality. Use when reviewing forms, navigation, dialogs, keyboard behavior, visual states, or overall UX.
---

# UI Accessibility Review

Evaluate the rendered experience and code semantics together.

1. Check semantic HTML, accessible names, labels, roles, headings, landmarks, and meaningful alternative text.
2. Verify keyboard-only operation, logical focus order, visible focus, focus trapping/restoration, and escape behavior for overlays.
3. Review form labels, instructions, validation, error announcement, autocomplete, and recovery paths.
4. Check contrast, zoom/reflow, text sizing, reduced motion, touch target size, and status messages.
5. Ensure dynamic content and asynchronous state changes are announced appropriately without excessive noise.
6. Test with available accessibility tooling and at least one manual keyboard/screen-reader-oriented pass when possible.
7. Report reproducible failures with element, user impact, and a specific fix.

Do not assert WCAG conformance from a quick automated scan. State the guideline level and scope only when formally evaluated. Preserve visual design intent while ensuring the interaction remains usable.
