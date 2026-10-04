---
name: frontend-accessibility
description: Design, implement, and audit accessible frontend interfaces. Use when prompts mention accessibility, WCAG, ARIA, keyboard navigation, screen readers, focus states, semantic HTML, contrast, forms, inclusive UI, or the old accessibility/frontend-a11y skills.
---

# Frontend Accessibility

Use this skill to make frontend work accessible without turning every task into a full compliance report.

## Routing

- For concise product/accessibility framing, read `references/accessibility.md`.
- For implementation details, keyboard patterns, ARIA rules, forms, focus, testing, and common frontend pitfalls, read `references/frontend-a11y.md`.
- For small UI fixes, apply the checklist below before loading a reference.

## Checklist

1. Prefer native HTML controls before ARIA.
2. Make every interactive element keyboard reachable and operable.
3. Preserve visible focus states with sufficient contrast.
4. Use labels, names, descriptions, and status announcements where behavior is not obvious.
5. Verify no nested interactive controls, click-only controls, or focus traps.
6. Check color contrast, reduced motion, hit area size, error messaging, and responsive order.
7. Test at least keyboard tab flow and one assistive-technology-friendly DOM inspection.

## Output

When reporting work, mention the accessibility behavior changed and the verification performed.

