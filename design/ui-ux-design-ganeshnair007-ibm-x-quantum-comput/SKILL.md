---
name: ui-ux-design
description: Design responsive, accessible, consistent, and modern user interfaces with coherent visual hierarchy.
---

# UI/UX Design

## Design Standards
- **Coherent Typography & Spacing:** Use systematic Tailwind scale or design tokens. Avoid random pixel overrides.
- **State Completeness:** Every view must provide designed treatments for:
  1. `Loading` (skeleton or inline spinner, avoiding layout shifts)
  2. `Empty` (instructional guidance or call-to-action)
  3. `Success` (subtle toast or confirmation feedback)
  4. `Error` (actionable recovery hints with error codes)
  5. `Unauthorized` (clear permission barrier with escalation path)
- **Accessibility (WCAG 2.1 AA):**
  - Minimum 4.5:1 contrast for body text; 3:1 for large text.
  - Full keyboard navigation with visible focus rings.
  - Proper ARIA landmarks, roles, and accessible names.
- **Restraint:** Avoid gimmicky animations, excessive neon gradients, or decorative widgets that obscure data.
