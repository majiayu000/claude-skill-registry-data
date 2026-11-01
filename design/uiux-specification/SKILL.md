---
name: uiux-specification
description: Full UI/UX Specification — Author comprehensive design specifications with semantic design tokens, component primitives, per-screen state matrices, responsive behaviors, and WCAG AA accessibility notes.
---

# SKILL: Full UI/UX Specification
## Domain: UI Engineering, Design Systems, SDD Station 06

**Activation triggers:** UI specification, design system, component inventory, design tokens, screen states, accessibility requirements, microcopy, SDD Station 06.

---

## 1. Role & Engineering Law

The Full UI/UX Specification skill defines the exhaustive implementation contract for frontend engineers and browser verification agents.  
It adapts proven modern design token architectures (evaluated against `ui-ux-pro-max`) while enforcing the **Exhaustive State Law**:
- Every screen MUST define all 5 states: Default, Loading/Skeleton, Empty (with action), Error (recoverable), and Success/Active.
- Every screen in this specification must map 1:1 with a Screen ID defined in `03_app_flow.md`.
- No styling may use hardcoded hex values or magic pixel numbers without referencing design tokens.

---

## 2. Document Structure & Required Sections

Every generated UI/UX Specification must follow `.factory/specifications/templates/04b_uiux_specification.template.md` and contain:
- **Header Metadata:** Document ID, Version, Status, Parent Brief ID, Parent App Flow ID, Target Specification, Design Lead, Date.
- **Section 1: Design System & Token Foundation:**
  - Semantic Color Palette (YAML block: base, surface, overlay, text, accent, state, border).
  - Typography Tokens (font families, scale, weights, line heights).
  - Spacing & Elevation (spacing scale, border radius, shadow tokens).
- **Section 2: Reusable Component Inventory:**
  - Tabular breakdown of primitives (`AppNavbar`, `DataTable`, `ActionButton`, `InputFormField`, `ModalDialog`, `StatusBadge`, `EmptyStateCard`).
- **Section 3: Per-Screen Specifications:**
  - Screen ID & Name (must match App Flow).
  - App Flow Reference link.
  - Purpose & User Goals.
  - Component hierarchy.
  - Complete 5-State Matrix: Default, Loading, Empty, Error, Success.
  - Responsive layout behavior across the 4 breakpoint bands.
  - Accessibility & ARIA notes (roles, live regions, focus traps).
- **Section 4: Microcopy & Validation Rules:**
  - Field validation table with exact error messages and helper text.
- **Section 5: Traceability & Gate Signoff.**

---

## 3. Validation Checklist (Quality Gate G0.5 Pre-Condition)

- [ ] Semantic tokens defined for colors, typography, spacing, and elevation.
- [ ] Every screen from `03_app_flow.md` has a complete per-screen specification (0 orphan screens).
- [ ] All 5 states specified for every screen.
- [ ] WCAG 2.2 AA ARIA annotations and keyboard focus order defined for all interactive components.
- [ ] Document saved to `.factory/specifications/<project>/04b_uiux_specification.md`.
