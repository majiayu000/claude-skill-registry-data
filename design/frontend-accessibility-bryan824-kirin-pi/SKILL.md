---
name: frontend-accessibility
description: "When building or reviewing an interface that people must operate without relying on sight, a mouse, or unrestricted motion — use native-first accessible interface craft."
---

# Frontend Accessibility

The platform is the component library: begin with the native behavior people
already depend on, then add only the semantics and interaction the interface
truly changes.

Resist: visual-only completion, custom controls that recreate browser behavior,
and ARIA used to disguise a semantic mismatch.

- Choose native landmarks, controls, labels, and validation before roles or
  scripted keyboard behavior; make every control's visible purpose present in
  its accessible name.
- Let DOM order carry focus. Give every pointer operation a keyboard path and a
  visible focus state; when an overlay changes context, contain its focus and
  restore it to the invoking control.
- Make forms recoverable: visible labels, useful input semantics, field-linked
  errors, and an announced failure or status at the right scope. Keep live
  regions stable before they need to speak.
- Treat screen-reader output, target usability, zoom/reflow, and reduced-motion
  behavior as interaction requirements, not finishing checks. Preserve a
  usable non-motion completion path and do not couple correctness to a visual
  animation ending.
- Read [edge cases](REFERENCE.md) when a native/default choice is unclear;
  test the actual assistive and input paths the product supports.

When `frontend-design` is installed, use its
[shared review contract](../frontend-design/references/REVIEW.md). Otherwise report
focused accessibility findings, exact evidence, user impact and verification gaps
directly. Review-only requests stay read-only; do not install siblings or duplicate
the full review schema.
