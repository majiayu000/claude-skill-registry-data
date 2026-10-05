---
name: react-architect
version: 1.0.0
description: React 19 standards — TypeScript strict, feature-based components, hooks-first composition, TanStack Query for server state, zustand for cross-tree client state, Suspense + ErrorBoundary at every async boundary, Radix for a11y. Use when writing or reviewing React components, hooks, or client-side state.
---

# React Architecture

Targets **React 19** with **TypeScript strict**. Component library defaults to Radix primitives + Tailwind (covered deeply in [ui-ux-architect](../../frontend/ui-ux-architect/SKILL.md)). When this skill applies to Next.js apps, server-side concerns live in [nextjs-architect](../nextjs-architect/SKILL.md). See [STACK.md](STACK.md) for pinned dependencies.

## 1. TypeScript posture — strict, always

`tsconfig.json` baseline in [RECIPES.md § `tsconfig.json` — strict baseline](RECIPES.md#tsconfigjson--strict-baseline).

- **No `any`.** Use `unknown` for truly untyped boundaries, then narrow.
- **No type assertions (`as`)** except at validated I/O boundaries (after a Zod parse, etc.).
- **`noUncheckedIndexedAccess`** is on — `arr[0]` is `T | undefined`, you handle the undefined. Catches a whole class of runtime crashes.
- **`exactOptionalPropertyTypes`** distinguishes `{x?: string}` from `{x: string | undefined}`. Pick the right one per use case.
- **Discriminated unions over enum + cast.** `type Status = {kind: "loading"} | {kind: "ok"; data: T} | {kind: "err"; msg: string}`.

## 2. Project structure — feature-based

Mirrors [fastapi-architect](../fastapi-architect/SKILL.md#1-project-structure--feature-based) and [gin-architect](../gin-architect/SKILL.md#1-project-structure--feature-based) — same shape, different language. One folder per bounded feature. Full tree in [RECIPES § Feature-based project structure](RECIPES.md#feature-based-project-structure).

- **A feature folder owns its UI, hooks, types, schemas, and API queries.** Cross-feature reuse moves to `src/components/`.
- **`schemas.ts` per feature** — Zod schemas for every request body and response shape. Parse at the API boundary; throw on parse failure.
- **`index.ts` exports the public surface** of each feature. Importing from `features/users/components/UserList` is cheating; import from `features/users` and re-export deliberately.

## 3. Components

### Function components only

- **No class components.** Hooks cover every legitimate case.
- **One component per file.** File name matches the component name (`UserList.tsx` exports `UserList`).
- **Default export sparingly.** Named exports compose better with refactors and IDE tooling.

### Naming + structure

Skeleton: [RECIPES.md § Component skeleton — `Props` type + loading/error guard](RECIPES.md#component-skeleton--props-type--loadingerror-guard).

- **`Props` type colocated**, named `<Component>Props`.
- **Loading / error / empty states are real components**, not inline ternaries with cryptic JSX. Per [ui-ux-architect](../../frontend/ui-ux-architect/SKILL.md).
- **`aria-*` attributes** when the role isn't implicit. Per [ui-ux-architect](../../frontend/ui-ux-architect/SKILL.md).
- **Event handlers passed as props**, not constructed inside the component (which would change identity every render and break `memo`).

### Composition over configuration

Reach for the composition shape first; a 20-prop `<DataTable>` is a smell. Comparison: [RECIPES.md § Compound vs. configuration component shape](RECIPES.md#compound-vs-configuration-component-shape).

- **Compound components** export sub-components on the main one (`Tabs.List`, `Tabs.Tab`, `Tabs.Panel`).
- **`children` is the most underused prop.** When in doubt, accept children.
- **Render props / function-as-child** for advanced cases where parent needs the child's state. Use sparingly — usually a custom hook is cleaner.

### Memoization, sparingly

- **Don't `memo` everything.** React 19's compiler handles most cases. Profile before memoizing.
- **`useMemo` / `useCallback` justified only when:**
  - The memoized value is itself expensive to compute, *or*
  - It's passed to a memoized child and identity matters.
- **The wrong reason** to add `memo`: "to feel safe". Often actively counterproductive (memoize an object that always changes → worse than not memoizing).

## 4. Hooks

### Built-in hooks

Full table of when to use each (`useState`, `useReducer`, `useContext`, `useEffect`, `useLayoutEffect`, `useId`, `useTransition`, `useDeferredValue`, `use`) in [RECIPES § Built-in hooks reference](RECIPES.md#built-in-hooks-reference). Key rule: **`useEffect` is for synchronization with non-React systems, not for fetching** — TanStack Query handles fetching.

### Custom hooks

- **Encapsulate stateful behavior** that's reused or that doesn't fit in a component. `useUser(id)`, `useDebounce(value, ms)`, `useEscapeKey(handler)`.
- **Name starts with `use`** — React's lint depends on it.
- **One responsibility per hook.** `useUserAndPostsAndPreferences` is three hooks.
- **Custom hooks compose other hooks** freely. No reason to inline what could be `useUser(id)`.

### Don't fetch in `useEffect`

- **Server state lives in TanStack Query**, not `useState` + `useEffect`. The fetch-in-effect pattern is correct for ~zero apps.
- The query handles loading, error, retry, dedup, caching, refetch on focus, invalidation — none of which you want to reimplement.

## 5. State management — three layers

| Layer | What | Tool |
|---|---|---|
| **Server state** | Anything fetched from the API — users, orders, etc. | **TanStack Query** |
| **Local state** | Component-internal — open/closed, form draft, hover | `useState` / `useReducer` |
| **Client global state** | Cross-tree, mutable, doesn't fit Context (perf or shape) | **zustand** when justified |

### TanStack Query for server state

- **Query keys are arrays, hierarchically structured.** `["users", { filter, sort, cursor }]`. Drives invalidation patterns.
- **Define query keys + fetchers per feature** in `features/<feature>/api.ts`.
- **Stale time tuned per resource** — `staleTime: 1000 * 60` is a reasonable default; reference data can go higher.
- **`refetchOnWindowFocus: true`** as default. Modern app expectation.
- **Optimistic updates** for mutations that the user will see succeed in 99% of cases (likes, votes, simple edits). Roll back on error. The query lib supports this directly with `onMutate` + `onError` rollback.
- **Don't put server data in zustand.** Caching, dedup, and freshness already live in TanStack Query; duplicating them is a recipe for inconsistency.

### Context for cross-tree static-ish state

- **Auth context, theme context, locale context** — read by many components, changes rarely.
- **Stable provider value** — wrap in `useMemo` so consumers don't re-render on every parent render. Or split into one provider for the value and one for the dispatcher.

### zustand for the rest

- **When Context performance is a problem** (many consumers re-render on every change), zustand selectors fix it.
- **When state has a non-trivial reducer shape** with several actions, zustand's set/get is cleaner than `useReducer` + Context.
- **Don't reach for it preemptively.** Most apps go years without needing it.

Skeleton: [RECIPES.md § Zustand store — focused, single-purpose](RECIPES.md#zustand-store--focused-single-purpose).

## 6. Suspense + ErrorBoundary

React 19's recommendation is: **every async boundary has a Suspense + ErrorBoundary above it.** Skeleton: [RECIPES.md § Suspense + ErrorBoundary at a route](RECIPES.md#suspense--errorboundary-at-a-route).

- **`<Suspense>` for loading**, `<ErrorBoundary>` for errors. The two together replace per-component `if (isPending) ... if (isError) ...` ladders.
- **TanStack Query supports Suspense mode** (`useSuspenseQuery`) — pairs cleanly with the boundary pattern.
- **Granularity matters.** A single big Suspense for the whole page means one slow query blocks everything. A Suspense per logical region means each fills in as ready.

## 7. Forms

- **Controlled inputs** for everything user-typed. `useState` per field for simple forms; `react-hook-form` (default for non-trivial) for complex forms with cross-field validation.
- **Zod schemas validate** on submit (and optionally on blur for inline feedback). Same schema feeds the API request type.
- **Native HTML form semantics** — `<form>`, `<label htmlFor>`, `<input required>`. Browser validation is free and accessible.
- **Submit returns a `Promise`** — disable the submit button while pending, show inline error on failure.

## 8. Routing — when Next.js isn't in play

- **TanStack Router** is the modern type-safe choice for non-Next React SPAs.
- **React Router** is the established option; v7+ is solid.
- **App Router for Next.js apps** — see [nextjs-architect](../nextjs-architect/SKILL.md).

Route components live in `src/routes/` (or framework-specific path); they orchestrate features but don't contain business logic — that's in feature folders.

## 9. Styling

- **Tailwind CSS** as the default — utility-first, no runtime cost, pairs with Radix primitives.
- **CSS modules** for genuinely custom one-off styles.
- **No CSS-in-JS** with runtime cost (styled-components, emotion) in 2026 — server-render + zero-runtime alternatives (`vanilla-extract`, Tailwind) cover the use cases at lower cost.
- **Design tokens** centralized — see [ui-ux-architect](../../frontend/ui-ux-architect/SKILL.md).

## 10. Testing

- **Vitest** for unit + component tests. Faster than Jest, ESM-native.
- **React Testing Library** for component tests — queries by role/label/text, not by CSS selector or implementation detail. Aligns with [tdd](../../workflows/tdd/SKILL.md) "test through the public interface."
- **Playwright** for end-to-end browser tests. Headless on CI, headed for debugging.
- **`axe-core` for accessibility tests** in unit + e2e — see [ui-ux-architect](../../frontend/ui-ux-architect/SKILL.md).
- **Test what users do**, not what implementation does. `screen.getByRole("button", { name: /submit/i })` over `container.querySelector("[data-testid=submit]")`.

## 11. Performance

- **React 19 compiler** does most memoization automatically. Don't fight it with manual `memo`.
- **Code-split at route boundaries** with `lazy()` + `<Suspense>`. Avoid lazy-loading components that render on every page.
- **Virtualize long lists** (`@tanstack/react-virtual`) — anything > 100 rows.
- **Image discipline** — `<img loading="lazy">`, explicit `width`/`height` to prevent layout shift, modern formats (WebP/AVIF). Next's `<Image>` handles this; non-Next apps use the same primitives manually.
- **Profile with React DevTools profiler** before optimizing.

## 12. Cross-skill ties

- [nextjs-architect](../nextjs-architect/SKILL.md) — Next-specific server-side concerns (RSC, server actions, app router) live there; this skill covers client React universally.
- [ui-ux-architect](../../frontend/ui-ux-architect/SKILL.md) — accessibility, component primitives (Radix), design tokens, loading/error/empty state design.
- [rest-api-architect](../../protocols/rest-api-architect/SKILL.md) — API contracts the frontend consumes. `snake_case` ↔ `camelCase` translation happens at the boundary if needed.
- [fastapi-architect](../fastapi-architect/SKILL.md) / [gin-architect](../gin-architect/SKILL.md) / [nethttp-architect](../nethttp-architect/SKILL.md) — backend counterparts; feature-folder structure mirrors them.
- [tdd](../../workflows/tdd/SKILL.md) — RTL "test through public interface" maps to TDD's "interface is the test surface".
- [logic-cleaner](../../refactoring/logic-cleaner/SKILL.md) / [code-design-refactor](../../refactoring/code-design-refactor/SKILL.md) — apply to React the same way as any other code; React's structure doesn't exempt it.
