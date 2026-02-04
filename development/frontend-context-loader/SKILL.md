---
name: frontend-context-loader
description: "Load the minimal Cookmate frontend context fast. Use only for frontend tasks to avoid repeated discovery: Next.js app structure, shared layouts, modules, and UI patterns."
---
# Frontend Context Loader (Cookmate)

Goal: cut token/time spent rediscovering the web app. Load these in order, skim only what’s needed.

## Quick sequence
1) App entry/layouts: `apps/web/src/app/layout.tsx`, `apps/web/src/app/(app)/layout.tsx`, main pages under `apps/web/src/app/(app)/**`, `apps/web/src/app/page.tsx` (redirect).
2) Layout/navigation patterns: `apps/web/src/shared/layouts/app/*` (AppShell, Topbar, BottomNav, navigation.ts).
3) Providers: `apps/web/src/shared/providers/query-provider.tsx`.
4) Modules: `apps/web/src/modules/**` (Recipes, RecipeDetail, Search, NewRecipes, etc.) — check domain/application/ui and seeds.
5) UI/shared: `apps/web/src/shared/ui/**` and `apps/web/src/shared/lib/**` for utilities/primitives; `tailwind.config.ts`, `SHADCN_THEME.css` if theme matters.

## Fast commands
- List files quickly: `rg --files apps/web/src/app`, `rg --files apps/web/src/modules`
- Search patterns: `rg "RecipesView" apps/web/src`, `rg "AppShell" apps/web/src`
- Preview: `sed -n '1,160p' path`

## Notes
- Navigation uses `navigation.ts` with `useSelectedLayoutSegments`; ignore segment groups `(...)`.
- Default UI pattern: AppShell with Topbar (desktop) + BottomNav (mobile), background radial accent.
