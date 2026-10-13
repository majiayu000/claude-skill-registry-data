---
name: ui-component-library
description: Reusable UI component patterns for React, Vue, and vanilla JavaScript. Includes advanced components beyond basic libraries (shadcn/ui, MUI), complex interactions, and production-ready code patterns. Use when building custom component libraries or implementing sophisticated UI components. Also triggers on compound components, headless hooks, render props, virtualized lists, drag and drop, command palette, autocomplete, rich text editor, file upload component, or any request for advanced React component patterns beyond what shadcn provides out of the box. Even if someone says "build me a custom component" — use this skill.
metadata:
  version: "1.0.0"
allowed-tools: "Bash, Read, Write, Glob"
---

<essential_principles>

### 1. Accessibility Is Architecture, Not Decoration

Every component starts with the correct semantic HTML element, keyboard navigation, ARIA attributes, and focus management. These are designed in at the API level, not bolted on after.

### 2. Composition Over Configuration

Prefer compound component patterns (`Tabs.Trigger`, `Tabs.Content`) over monolithic prop-heavy components. Let consumers compose behavior rather than configuring it through dozens of props.

### 3. Separate Behavior from Styling

Use headless hooks (`useDropdown`, `useModal`) to encapsulate behavior. Consumers apply their own styles. This makes components portable across design systems.

### 4. Performance by Default

Memoize expensive computations, virtualize long lists, use event delegation, and lazy-load off-screen content. Don't wait for performance problems to optimize.

</essential_principles>

<intake>

| User Says | Route To |
|-----------|----------|
| "Build a component" / "custom component" / "component API" | `workflows/build-component.md`, then `references/component-patterns.md` |
| "Virtualized table" / "infinite scroll" / "data grid" / "chart" | `references/component-catalog.md` → Data Display |
| "Drag and drop" / "modal" / "tooltip" / "command palette" / "file upload" | `references/component-catalog.md` → Interactive |
| "Autocomplete" / "multi-select" / "date picker" / "form component" | `references/component-catalog.md` → Forms |
| "Split panes" / "masonry" / "carousel" / "virtualized list" | `references/component-catalog.md` → Layout |
| "Testing components" / "performance" / "memoization" | `references/testing-performance.md` |
| "Compound components" / "headless" / "render props" / "advanced pattern" | `references/component-patterns.md` |

</intake>

<component_checklist>

Before building any component, verify:

**Functionality:**
- [ ] States defined (default, hover, focus, active, selected, disabled, loading, error)
- [ ] Props API designed (required/optional, types, defaults)
- [ ] Events/callbacks defined
- [ ] Edge cases handled (empty, loading, error states)

**Accessibility:**
- [ ] Keyboard navigation (arrow keys, Tab, Enter, Escape)
- [ ] ARIA attributes (role, aria-label, aria-describedby, aria-expanded)
- [ ] Focus management (trap in modals, restore on close)
- [ ] Screen reader announcements (live regions for dynamic content)

**Performance:**
- [ ] Virtualization (for lists over 100 items)
- [ ] Lazy loading (defer off-screen content)
- [ ] Memoization (prevent unnecessary re-renders)
- [ ] Event delegation (reduce listener count)

**Styling:**
- [ ] Scoped styles (CSS Modules, Tailwind+CVA, or CSS-in-JS)
- [ ] Theme tokens consumed (never raw color/spacing values)
- [ ] Responsive (mobile-first breakpoints)
- [ ] Dark mode support

</component_checklist>

<quality_gates>

Before releasing any component:

- [ ] TypeScript types exported
- [ ] Accessibility tested (keyboard + screen reader)
- [ ] Unit tests pass (over 80% coverage)
- [ ] Visual regression baseline established — Vizzly (`npx vizzly tdd`), Chromatic, or Percy
- [ ] Performance profiled (React DevTools Profiler)
- [ ] Documentation complete (props, examples, a11y notes)
- [ ] Storybook story created (all variants and states)
- [ ] Dark mode verified
- [ ] Mobile responsive (tested 320px–1920px)
- [ ] No console errors or warnings

</quality_gates>

<reference_index>

| Workflow | Purpose | When to Read |
|----------|---------|--------------|
| `workflows/build-component.md` | Step-by-step: design API → scaffold → implement → test → document | Creating any new component |

| Reference | Purpose | When to Read |
|-----------|---------|--------------|
| `references/component-patterns.md` | CVA anatomy, compound components, headless hooks, render props | Designing component architecture |
| `references/component-catalog.md` | Advanced component implementations by category (data, interactive, forms, layout) | Building a specific complex component |
| `references/testing-performance.md` | Unit tests, a11y tests, memoization, virtualization, styling options | Testing and optimizing components |

| Script | Purpose | When to Run |
|--------|---------|-------------|
| `scripts/a11y-check.js` | Static accessibility analysis of a component file (ARIA, keyboard, semantic HTML) | After implementing, before PR |

| Asset | Purpose | When to Use |
|-------|---------|-------------|
| `assets/component-template.tsx` | Production-ready component starter with CVA variants, forwardRef, ARIA, loading state | Starting any new component |

</reference_index>

## CLAIMS

- [GENERATED] Compound component pattern (`Tabs.Trigger`, `Tabs.Content`) is superior to monolithic prop APIs for complex components because it preserves composition and avoids prop explosion
- [GENERATED] Headless hooks separate behavior from styling, enabling the same interaction logic across multiple visual implementations — the pattern used by Radix UI, Headless UI, and React Aria
- [SOURCED] Virtualizing lists >100 items: react-virtual and @tanstack/virtual are the current standard — not React's built-in — because React doesn't provide virtualization

## GAPS / BLINDSPOTS / UNKNOWN-UNKNOWNS

- RSC (React Server Components) compatibility constraints on client components are evolving — some patterns here require `"use client"` directives
- Web Components / custom elements not covered — valid cross-framework alternative
- Testing library recommendations may shift as Vitest matures relative to Jest
