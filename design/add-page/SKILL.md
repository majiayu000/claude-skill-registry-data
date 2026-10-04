---
name: add-page
description: Scaffold a new agent platform page with the project's standard layout, RTL Arabic, react-query data fetch, skeleton, and sidebar entry. Use when the user asks to "add a page", "create a new page", or "build a screen for X".
---

# add-page

Scaffold a new platform page that matches the existing patterns. The page must look like every other page in the app — same wrapper, same header, same skeleton, same RTL handling.

## Inputs to gather

Before scaffolding, ask (or infer) :

- **Page name** in English (e.g. `commissions`)
- **Arabic title** (e.g. `العمولات`) — required
- **Route path** (e.g. `/home/platform/commissions`)
- **Data source** — does it `useQuery` an existing API? If not, run `/add-api-route` first
- **Sidebar group** — where in `apps/web/src/components/layout/sidebar.tsx` does the link go?

## Steps

1. **Read a sibling page** for the latest pattern. Default reference: `apps/web/src/pages/platform/leads/index.tsx` (already follows the post-E2 conventions: tight tables, RTL, `PageHeader`, soft skeletons).
2. **Create the file** at `apps/web/src/pages/platform/{name}/index.tsx`. It must:
   - Import `PageHeader` from `@/components/ui/page-section-header`
   - Wrap in the standard `PAGE_WRAPPER` constant from `@/config/platform-theme`
   - Use `useQuery({ queryKey: ['/api/...'] })` from `@tanstack/react-query`
   - Render a `<Skeleton>` block from `@/components/skeletons/...` while loading
   - Default to RTL — use `ms-`/`me-`/`ps-`/`pe-`/`text-start`/`text-end` (never `ml-`/`mr-`)
   - All visible strings in Arabic — use the project's IBM Plex Sans Arabic stack
   - All colors via CSS variable tokens (`bg-card`, `text-foreground`, etc.) — never hex
3. **Register the route** in `apps/web/src/App.tsx` (or wherever the wouter `<Switch>` lives).
4. **Add the sidebar link** in `apps/web/src/components/layout/sidebar.tsx` under the right group.
5. **Run `/typecheck`** to confirm zero TS errors.
6. **Update the vault**: if the page introduces a meaningful new feature, add a note under `Aqarkom_Knowledge/Features/`. Otherwise just note it in the next session retro.

## Verification checklist

- [ ] Page renders with no console errors
- [ ] Skeleton is visible during loading (use throttle in Network tab to test)
- [ ] All strings are in Arabic
- [ ] No `ml-`/`mr-`/`pl-`/`pr-`/`text-left`/`text-right` in JSX
- [ ] No hardcoded colors
- [ ] Sidebar link works in both expanded and collapsed states
- [ ] `/typecheck` passes

## Anti-patterns

- Don't copy a page that hasn't been refactored to the post-E1 layout — start from `leads/index.tsx`
- Don't put `<CardContent>` padding on tables; use `<CardContent className="p-0">`
- Don't import lucide icons individually outside the project's icon convention
