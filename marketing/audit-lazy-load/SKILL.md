---
name: audit-lazy-load
description: Audit every page to ensure it uses React.lazy() in App.tsx for code-splitting, and that the Suspense fallback delegates to the page's own skeleton. Use after adding pages, before /complete-session, and during performance audits.
---

# audit-lazy-load

Every page component must be **lazy-loaded** via `React.lazy()` in `App.tsx` so the initial bundle stays small. The Suspense fallback should be minimal (empty div) because each page handles its own skeleton internally via `useMinLoadTime`.

## Architecture

```
App.tsx
  └─ const SomePage = lazy(() => import("@/pages/platform/some-page"))
  └─ <Suspense fallback={<div className="h-full" />}>
       <SomePage />
     </Suspense>

SomePage/index.tsx (inside the lazy chunk)
  └─ useMinLoadTime() → shows SomePageSkeleton while loading
  └─ useQuery() → fetches data
  └─ renders skeleton OR real content
```

This two-layer approach means:
1. **Suspense fallback** covers the brief moment while the JS chunk downloads (minimal div)
2. **Page skeleton** covers the data-fetching phase (layout-accurate skeleton via `useMinLoadTime`)

## What's compliant

A page is compliant when:

1. It is imported in `App.tsx` via `React.lazy(() => import("@/pages/..."))` — NOT a static import
2. It is rendered inside a `Suspense` boundary (via the `withSuspense` helper or explicit `<Suspense>`)
3. Inside the page component itself, `useMinLoadTime` is called and the skeleton is shown during loading

## Exceptions (pages that MAY be statically imported)

These critical public routes are loaded eagerly because they're part of the initial landing experience:

- `Landing` (`@/pages/landing`)
- `NotFound` (`@/pages/not-found`)
- `SignupSelection`, `SignupIndividual`, `SignupCorporate`, `SignupSuccess`, `KYCSubmitted` (`@/pages/signup/*`)
- `Sidebar`, `PlatformShell`, `Header` (layout components, not pages)

Everything else — all platform pages, admin pages, client portal pages — **must** be lazy-loaded.

## Steps

1. **Read `App.tsx`** and collect:
   - All `lazy(() => import(...))` declarations → the "lazy set"
   - All static `import ... from "@/pages/..."` declarations → the "eager set"
   - All route registrations and which component they reference

2. **Inventory all page files**. Collect every `index.tsx` or named `.tsx` under:
   - `apps/web/src/pages/platform/`
   - `apps/web/src/pages/admin/`
   - `apps/web/src/pages/client/`
   - `apps/web/src/pages/marketing/`
   - `apps/web/src/pages/requests/`
   - `apps/web/src/pages/map/`
   - `apps/web/src/pages/listing/`
   - `apps/web/src/pages/blog.tsx`

3. **Cross-reference**. For each page file, check:
   - Is it in the lazy set? → OK
   - Is it in the eager set and NOT in the exceptions list? → **VIOLATION**
   - Is it not imported in App.tsx at all? → **ORPHAN** (may be a sub-component, not a page — investigate)

4. **Check Suspense wrapping**. Every lazy component must be rendered inside `<Suspense>`. In this project, the `withSuspense()` helper handles this. Verify each lazy component is either:
   - Wrapped via `withSuspense(Component)`, or
   - Inside a `platformShellRoutes` / `platformDynamicRoutes` / `platformAdditionalRoutes` array (which the `PlatformShell` renders inside Suspense)

5. **Check page-level skeleton**. For each lazy-loaded page, verify it internally uses `useMinLoadTime` + a skeleton (delegate to `/audit-skeleton` if needed).

6. **Report** a table:
   | Page file | Import type | Suspense | Page skeleton | Status |
   |-----------|-------------|----------|---------------|--------|
   | platform/leads | lazy | withSuspense | LeadsSkeleton | OK |
   | platform/inbox | static | — | — | NEEDS LAZY |
   | admin/cms | lazy | withSuspense | — | NEEDS SKELETON |

7. **Fix violations**:
   - Move static imports to `lazy(() => import(...))` declarations
   - Ensure the route uses `withSuspense` or is in a Suspense-wrapped route array
   - If the page lacks an internal skeleton, create one (follow `/audit-skeleton` steps)

8. **Run `/typecheck`** to confirm zero TS errors.

## Verification checklist

- [ ] Every non-exception page uses `React.lazy()` in App.tsx
- [ ] Every lazy component is wrapped in `<Suspense>` (via `withSuspense` or route array)
- [ ] Suspense fallbacks are minimal (`<div className="h-full" />` or `<div className="min-h-screen bg-background" />`)
- [ ] Every lazy page internally uses `useMinLoadTime` + a layout-accurate skeleton
- [ ] No orphan pages (every page file is reachable from App.tsx routes)
- [ ] `/typecheck` passes

## Anti-patterns

- Don't statically import pages that aren't in the exceptions list — this bloats the initial bundle
- Don't put a heavy skeleton in the Suspense fallback — Suspense fallback fires before the chunk loads; keep it minimal
- Don't use `React.lazy` for layout components (`Sidebar`, `Header`, `PlatformShell`) — these are needed immediately
- Don't forget to add new pages to the route config arrays — a lazy import with no route means dead code
- Don't use `loading` prop on wouter `<Route>` — the project uses Suspense + `useMinLoadTime` instead
