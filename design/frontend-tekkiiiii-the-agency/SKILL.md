---
name: frontend
description: |
  Build high-quality, production-grade frontend interfaces, components, and web UIs — from landing pages and dashboards to React components and full design systems. Implements a design-first workflow: visual hierarchy and typography before code, reusable component architecture, performance optimization, and WCAG 2.1 AA accessibility baseline.
  Purpose: Delivers frontend work that looks polished, is maintainable, and scales — not just functional but production-ready.
  When to trigger: (1) "Build a website," "create a landing page," "make a dashboard," or "build a UI," (2) "Write a React component" or "add a UI feature to our app," (3) "Improve the look and feel" or "design polish" on an existing interface, (4) "Set up a design system" or "add consistent styling," (5) "Make it responsive" or "mobile-friendly," (6) "Fix accessibility issues" — low contrast, missing ARIA labels, keyboard navigation, (7) "Add animations" or "make it feel smooth."
  Key capabilities: Design system checklist (spacing, color, typography, interactive states), component patterns for layout, forms, and empty/loading states, React+TypeScript best practices, lazy loading, bundle size optimization, mobile-first responsive breakpoints, and semantic HTML with ARIA.
  Ideal user/context: Frontend engineers, designers who code, or anyone who wants UI work done right — not just assembled.
  Also for: Marketing sites needing conversion-focused layouts, design system audits, accessibility remediation, and animations for product onboarding flows.
---

## Relationship with `ui-ux-pro-max`

When both `ui-ux-pro-max` and `frontend` could apply:
- `ui-ux-pro-max` **leads** on visual/interface decisions, design systems, color, typography, layout
- `frontend` **handles** component-level code quality, React patterns, state management, performance, accessibility implementation

Do not duplicate design decisions — implement what ui-ux-pro-max specifies.

# Frontend Design Skill

## Core Principles
- **Design-first thinking**: Consider visual hierarchy, spacing, and typography before writing code
- **Component architecture**: Build reusable, composable components
- **Performance**: Lazy load, minimize bundle size, optimize images
- **Accessibility**: WCAG 2.1 AA as baseline — semantic HTML, ARIA labels, keyboard navigation

## Stack Defaults (adjust to user's context)
- React + TypeScript
- Tailwind CSS for utility-first styling
- Framer Motion for animations
- Lucide React for icons

## Design System Checklist
- Consistent spacing scale (4px base unit)
- Limited color palette (primary, secondary, neutral, semantic)
- Typography scale (display, heading, body, caption)
- Interactive states for all clickable elements (hover, active, focus, disabled)

## Component Patterns

### Layout
```jsx
// Always use semantic HTML
<main>, <section>, <article>, <nav>, <aside>, <header>, <footer>
// Grid for 2D layouts, Flexbox for 1D
```

### Forms
- Label every input
- Show validation inline, immediately after interaction
- Clear error states with helpful messages

### Loading & Empty States
- Skeleton screens over spinners for content
- Always design the empty state — don't leave blank white space

## Code Quality
- Extract magic numbers to named constants
- Keep components under 200 lines — split if larger
- Co-locate styles with components
- Write self-documenting prop names

## Responsive Design
- Mobile-first: start with smallest viewport
- Breakpoints: sm (640), md (768), lg (1024), xl (1280)
- Test at 375px (iPhone SE) and 1440px (desktop)