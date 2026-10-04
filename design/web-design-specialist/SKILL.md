---
name: web-design-specialist
description: Modern, accessible, and conversion-optimized web design direction, UX
  guidance, and design system development. Use when asked to improve a website's design,
  create a component library, audit for accessibility (WCAG), redesign a landing page
  for conversion, build a design system, give UX feedback on a layout, or improve
  mobile responsiveness.
allowed-tools:
- Read
- Write
- Bash
- Grep
- Glob
metadata:
  author: Daryl Lundy
  version: 2.0.0
  category: design
  tags:
  - web-design
  - ux
  - ui
  - accessibility
  - wcag
  - design-system
  - conversion-optimization
  - responsive
---

# Web Design Specialist

## Activation criteria
- User language explicitly matches trigger phrases such as `improve the design`, `accessibility audit`, `WCAG`.
- The requested work fits this skill's lane: Design audits, accessibility (WCAG), landing page conversion, design systems, UX feedback.
- The request needs this domain's specific workflow, checks, or deliverable shape rather than a neighboring specialist.

## First actions
1. Identify: is this a new design, a redesign, or an audit of existing design?
2. For audits: `Read` existing CSS/Tailwind files to understand current design tokens (colors, typography, spacing)
3. Confirm: target device priority (mobile-first vs desktop), accessibility requirements (WCAG AA or AAA)

## Decision rules
- Mobile-first by default — design for 375px first, then scale up
- Accessibility is non-negotiable: color contrast ≥4.5:1 for body text, ≥3:1 for large text; all interactive elements keyboard accessible
- For conversion optimization: above-the-fold CTA, trust signals, social proof placement

## Output contract
- Design direction: annotated wireframe or component spec (text-based if no design tool available)
- Accessibility: WCAG AA compliance noted for any color or interaction recommendations
- For design systems: token names in CSS custom properties format

## Constraints
- NEVER trade away accessibility or readability for visual novelty.
- NEVER treat implementation detail decisions as part of this skill when the work should be handed to frontend-specialist.
- Scope boundary: final frontend code changes belong to the relevant implementation specialist unless explicitly combined.

## Reference
- `references/full-guide.md`: UX best practices, conversion optimization patterns, accessibility standards, design system structure, responsive design patterns
