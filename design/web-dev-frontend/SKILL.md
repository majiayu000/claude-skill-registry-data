---
name: web-dev-frontend
description: "Web frontend in TypeScript with React, Vue, or Svelte: components, hooks, state management, styling and design tokens, accessibility, browser APIs, performance. Use when building or changing components, pages, forms, or UI state, theming, or any *.tsx, *.vue, *.svelte, or frontend/** file."
license: MIT
metadata:
  display-name: "Web Frontend"
  version: "1.1"
  platforms: "claude-code codex"
  tags: "frontend typescript react ui"
---

# Web dev - frontend

## Type discipline
- TypeScript strict mode is non-negotiable. No `any`, no `// @ts-ignore`, no `as unknown as T` to silence the compiler. If a type is wrong, fix the type - don't cast around it.
- Prefer `unknown` over `any` at boundaries; narrow with type guards or zod.
- Use `readonly` for arrays/objects that must not mutate. Use `as const` for literal narrowing.
- Discriminated unions over optional-everywhere objects. A `Result<T, E>` or `{ status: 'idle' | 'loading' | 'success' | 'error' }` beats five booleans.
- Validate every API/network/localStorage/URL boundary with zod. Inferred TS types come from the schema, not the other way around.

## Component design
- Components are functions. No classes unless wrapping a third-party imperative API.
- One responsibility per component. Splitting a 200-line component is almost always an improvement.
- Props interfaces named `<Component>Props`. Keep them small - if a component needs 12 props, it's two components.
- Avoid prop drilling past 2 levels. Lift to context, a store, or composition (children/render-props).
- `key` on lists must be a stable id from the data, never the array index unless the list is immutable and append-only.

## Atomic design (when working in a design system)
- **Atoms** = single-element primitives (Button, Input, Chip).
- **Molecules** = compositions of atoms with one job (FormField = Label + Input + error).
- **Organisms** = page-level building blocks with business meaning (DashboardHeader, ReportPanel).
- Shared components belong in atoms/molecules; app-specific compositions stay as organisms in the consuming app.
- Theme via CSS custom properties (e.g. `--ui-accent`), not hardcoded Tailwind palette classes - apps re-theme by overriding the variables.

## Hooks (React) / composables (Vue)
- Effects describe synchronization, not lifecycle. If you reach for `useEffect` to "do something on mount," ask whether it should be an event handler instead.
- Every effect needs a complete dependency array. Don't suppress the lint rule - fix the dep.
- Custom hooks/composables for any logic shared by ≥2 components. Name them `use<Thing>`.
- Don't fetch in `useEffect` for new code - use the framework's data layer (TanStack Query, SWR, RSC, Vue Query, SvelteKit `load`).

## State management
- Local state first. Lift only when ≥2 components need it.
- Server state ≠ client state. Don't put fetched data in Redux/Zustand - use a query cache.
- Forms: react-hook-form / vee-validate / felte. Don't roll your own.
- URL is state. Filters, tabs, pagination, modals belong in the URL when shareable/back-button-able.

## Styling
- Match the project's existing styling system (Tailwind, CSS Modules, vanilla-extract, styled-components). Don't introduce a second one.
- No inline styles for anything dynamic enough to deserve a class.
- Design tokens (spacing, color, radii) come from the system - never hand-tuned hex values for "primary."
- Dark mode via `class="dark"` toggle + CSS-variable swap is the most portable approach across frameworks.

## Accessibility (non-optional)
- Every interactive element is keyboard-reachable and has a visible focus ring.
- `<button>` for actions, `<a>` for navigation. Never `<div onClick>`.
- Form inputs have associated `<label>`s. `aria-label` is a fallback, not a default.
- Images have `alt`. Decorative images get `alt=""`.
- Color contrast meets WCAG AA. Don't convey state with color alone.
- Modals: `role="dialog"`, `aria-modal="true"`, focus trap, Escape to close, return focus to trigger.
- Menus: `role="menu"`, `aria-haspopup`, `aria-expanded`, arrow-key navigation.
- Run axe / Lighthouse on changed pages before declaring done.

## Performance
- Measure before optimizing. `React DevTools Profiler`, `performance.mark`, Lighthouse.
- Avoid `useMemo`/`useCallback` cargo-culting - they cost more than they save for cheap computations.
- Lazy-load routes and heavy components (`React.lazy`, dynamic `import()`).
- Images: correct dimensions, `loading="lazy"` below the fold, modern formats (AVIF/WebP).
- Bundle size: check the diff in `dist/` after adding a dependency. A 300KB date library for one `format()` call is not acceptable.

## API consumption
- Centralize the fetch wrapper. Auth, error mapping, base URL, and retry policy live in one place.
- Don't expose raw `Response` objects to components - return typed data or throw a typed error.
- Cancel in-flight requests on unmount (`AbortController`) for searches and live filters.
- Optimistic updates only when undo is cheap and visible.

## Testing the UI
- Component tests with React Testing Library / Vue Testing Library - query by accessible role/label, not test-ids.
- E2E for critical flows only (see `e2e-qa` skill).
- Visual regressions: only if the project already has a snapshot tool wired up.

## Verification before declaring done
Start the dev server, exercise the feature in a browser, check the golden path AND error states. Type-check passing is not feature-correctness.
