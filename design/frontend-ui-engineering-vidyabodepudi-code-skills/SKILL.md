---
name: frontend-ui-engineering
description: >
  Frontend-specific engineering practices including component architecture,
  state management, accessibility, responsiveness, and performance. Use
  when building UI components, pages, or interactive interfaces.
version: 1.0.0
permissions:
  - fs.read
  - fs.write
  - shell.exec
  - browser.inspect
triggers:
  - context: "building UI components"
  - context: "frontend development"
  - context: "building a web page"
  - command: "/build"
platforms:
  - claude-code
  - cursor
  - gemini-cli
  - copilot
  - codex
  - opencode
  - windsurf
  - kiro
dependencies:
  - test-driven-development@^1.0.0
model_variants:
  claude:
    enforcement_style: "human-partner collaborative"
  gemini:
    enforcement_style: "structured-checklist"
  gpt:
    enforcement_style: "directive-imperative"
author: codehands-core
signed: true
tier: 2
---

## Overview

Frontend engineering requires balancing visual fidelity, accessibility, performance, and maintainability. This skill covers component design, state management, responsive layouts, and the practices that differentiate production UIs from prototypes.

## When to Use

- When building any UI component, page, or interactive element
- When styling or layout work is involved
- When managing client-side state
- NOT for API-only or CLI work

## Process

### 1. Component Design

- **Single responsibility per component** — one purpose, one reason to change
- **Props down, events up** — data flows down, actions flow up
- **Composition over configuration** — small composable components over mega-components with 20+ props
- **Controlled vs. uncontrolled** — make the choice explicit, don't mix

### 2. State Management

- **Local state first** — component state for UI state (open/closed, selected tab)
- **Lift state when needed** — only when siblings need to share state
- **Global state is last resort** — for truly global concerns (user session, theme, locale)
- **Derived state is computed** — never store what you can compute from existing state

### 3. Accessibility (Non-Negotiable)

- Semantic HTML first (`<button>`, `<nav>`, `<main>` — not `<div onclick>`)
- All interactive elements keyboard accessible
- All images have alt text
- Color contrast ≥ 4.5:1 for normal text, 3:1 for large text
- Focus management for dynamic content (modals, dropdowns)
- Reference: `references/accessibility-checklist.md`

### 4. Responsive Design

- Mobile-first approach (min-width breakpoints)
- Test at: 320px, 768px, 1024px, 1440px minimum
- No horizontal scrolling on any viewport
- Touch targets ≥ 44x44px on mobile
- Images: srcset + sizes for responsive loading

### 5. Performance

- Code split at route boundaries
- Lazy load below-the-fold content
- Images in WebP/AVIF with fallbacks
- Explicit width/height on images (prevent CLS)
- Minimize re-renders (memoization where measured beneficial)
- Reference: `references/performance-checklist.md`

### 6. Testing UI

- **Component tests** — Render, interact, assert behavior (not markup structure)
- **Visual regression** — Snapshot sparingly, only for stable, critical visuals
- **Accessibility tests** — Automated (axe-core) + manual keyboard walkthrough
- **Integration tests** — User flows crossing component boundaries

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Accessibility can be added later" | Retrofitting accessibility is 10x harder than building it in. Semantic HTML costs nothing extra. Do it now. |
| "It works on my screen" | Your screen is one of thousands of viewport sizes. Test at 320px minimum. |
| "That's just a div with an onClick" | A `<div>` with onClick is invisible to screen readers, not keyboard accessible, and has no button semantics. Use `<button>`. |
| "Users don't use keyboard navigation" | ~15% of users rely on non-mouse navigation (disability, power users, testing). It's also a legal requirement. |

## Red Flags

- `<div onClick>` instead of `<button>` for interactive elements
- No alt text on images
- No responsive testing
- Inline styles for layout (should use CSS system)
- Global state for component-local concerns
- No component tests

## Verification

- [ ] Components have single responsibility
- [ ] State management follows local → lifted → global progression
- [ ] Accessibility checklist passed (keyboard, alt text, contrast, semantics)
- [ ] Responsive at 320px, 768px, 1024px, 1440px
- [ ] Performance: no unnecessary re-renders, images optimized
- [ ] Component tests verify behavior, not markup

## See Also

- `codehands:browser-testing-with-devtools` — Visual verification via DevTools
- `references/accessibility-checklist.md` — WCAG 2.2 AA checklist
- `references/performance-checklist.md` — Frontend performance checklist
