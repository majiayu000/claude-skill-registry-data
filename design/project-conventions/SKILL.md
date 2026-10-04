---
name: project-conventions
description: Project-specific conventions for the Arch Systems monorepo. Load before any implementation or review task in this codebase. Enforces monorepo, Next.js App Router, Supabase, and light-only macOS design system rules.
user-invocable: false
disable-model-invocation: false
---

# Arch Systems Project Conventions

## Monorepo

- Package manager: pnpm 9.12.0+
- Workspace protocol: all internal deps use `"workspace:*"`
- Path alias in portal: `~/*` maps to `apps/portal/*`, `@/*` also maps to `apps/portal/*`
- Run commands from root unless testing: `pnpm dev` (portal only), `pnpm build`, `pnpm lint`

## Next.js / React

- App Router only — `app/` directory, `next/link`, `next/navigation`
- Server Components by default. Only add `'use client'` for interactivity (useState, useEffect, event handlers, browser APIs)
- Data fetching in Server Components; pass data to Client Components via props
- Loading states: `loading.tsx`. Error boundaries: `error.tsx`

## Supabase

- All interactions through `@repo/supabase` — NEVER import from `@supabase/supabase-js` directly
- Server: `createServerSupabaseClient()` from `@repo/supabase/server`
- Client: `createClient()` from `@repo/supabase/client`
- Middleware: `createMiddlewareClient()` from `@repo/supabase/middleware`
- RLS must be enabled on every new table
- Service role keys must never appear in client-side code or `NEXT_PUBLIC_*` vars

## Design System (Light-only, macOS Sonoma)

- **Theme**: Light-only. Dark mode does not exist. `#f5f5f7` page background, `#ffffff` card surfaces.
- **Glass pattern**: `bg-white/70 backdrop-blur-xl border border-black/[0.08]` for elevated surfaces.
- **Shadows**: Forbidden: raw `shadow-sm/md/lg`, raw `box-shadow` CSS. Use named tokens only: `shadow-diffusion-sm/md/lg/xl`, `shadow-card`, `shadow-card-hover`, `shadow-elevated`, `shadow-window`.
- **Borders**: `rgba(0, 0, 0, 0.06)` subtle, `rgba(0, 0, 0, 0.12)` default, `rgba(0, 0, 0, 0.2)` emphasis.
- **Accent**: `#007aff` macOS system blue (`--accent-blue`). Never use green accents.
- **Text**: `#1d1d1f` heading, `#3a3a3c` body, `#6e6e73` secondary, `#a1a1a6` muted.
- **Typography**: Inter + Outfit for UI, JetBrains Mono for tabular data. `font-weight: 400` default, `500` for nav/buttons. Never `700`/`bold`.
- **Class merging**: Always use `cn()` from `@repo/ui/lib/utils` — never `clsx` or `tailwind-merge` directly.
- **Animation**: Only `opacity`, `transform`, `background-color`, `border-color`, `color`. Never layout properties. Easing `cubic-bezier(0.16, 1, 0.3, 1)`.
- **Forbidden patterns**: `shadow-*` Tailwind tokens, `font-semibold`, `font-bold`, dark-specific hex colors (`#171717`, `#363636`, `#fafafa`), `border-emerald-*`, `text-emerald-*`.

## UI Components

- Import from `@repo/ui`, never direct shadcn paths
- Add new shadcn components via `pnpm ui` (runs in `@repo/ui` package)
- Component files: PascalCase (`Button.tsx`). Utility files: camelCase (`formatDate.ts`)

### Shared Components (@repo/ui)

- `GlassCard` — Card container with glass styling (`bg-white/70 backdrop-blur-xl border border-black/[0.08] shadow-card`)
- `DepartmentLayout` — Sidebar + content layout for department pages
- `KPI` / `KPICard` — Summary metric cards with color variants (`default`, `green`, `amber`, `red`, `blue`)
- `KPIGrid` — Responsive grid layout for KPI cards (2, 3, or 4 columns)
- `PageHeader` — Title + date header used across all department tab pages
- `ShiftToggle` — Day/night shift selector with `getCurrentShift()` helper
- `FormFields` — `FormInput`, `FormSelect`, `FormTextarea`, `SubmitButton` with consistent glass styling
- `Input` — Styled text input
- `SecondaryButton` — Secondary action button

### Shared Utilities (apps/portal/lib)

- `getDepartmentContext(params)` — Server component helper that validates department, fetches dept ID from Supabase, returns `{ dept, deptId, supabase, today }`. Calls `notFound()` on invalid departments.
- `requireDepartment(slug, allowed)` — Guards tabs to specific departments. Calls `notFound()` if department not in allowed list.

## Testing

- Unit tests: Jest with `ts-jest`, files: `<name>.test.ts` or `<name>.test.tsx`
- Mock `@repo/supabase`, never `@supabase/supabase-js`
- E2E: Playwright, files: `e2e/<name>.spec.ts`, baseURL `http://localhost:3000`
