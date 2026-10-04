---
name: route-discovery-system
description: "Filesystem auto-discovery of App Router pages into navigable index pages. Use when creating an index/listing page, adding route directories, converting hard-coded route configs to auto-discovery, or adding a route-listing display variant."
---

# Route Discovery System

Filesystem-based route auto-discovery that replaces hard-coded `config.ts` route arrays. Server Components scan directories for `page.tsx` files and render grouped navigation UIs with switchable display variants.

## Architecture

```
Server Component (RouteIndexPage)
  └─ scanRoutes() reads filesystem (server-only)
  └─ Serializes RouteDisplayData
  └─ Passes to RouteDisplaySwitcher (client)
       └─ next/dynamic loads active variant (ssr: false)
       └─ Dropdown switches between variants
```

**Key boundary:** `utils/route-discovery/index.ts` is `server-only` (filesystem access). `utils/route-discovery/shared.ts` has pure functions safe for client imports.

## File Map

| File | Role |
|------|------|
| `utils/route-discovery/index.ts` | Server-only: `scanRoutes`, `scanRoutesShallow` |
| `utils/route-discovery/shared.ts` | Client-safe: `groupRoutes`, `getRouteLabel`, `toModulePages`, `sortGroupKeys` |
| `components/ssr/RouteIndexPage.tsx` | Server Component: scans filesystem, renders page shell, passes data to switcher |
| `components/ssr/RouteHeaderData.tsx` | Server Component: auto-feeds `ModuleHeader` nav from filesystem |
| `components/ssr/route-display/types.ts` | `RouteDisplayData`, `RouteDisplayVariant`, `RouteDisplayProps` |
| `components/ssr/route-display/RouteDisplaySwitcher.tsx` | Client wrapper: variant dropdown + `next/dynamic` imports |
| `components/ssr/route-display/GroupedCardsDisplay.tsx` | Variant: grouped folder cards (default) |
| `components/ssr/route-display/DataTableDisplay.tsx` | Variant: searchable keyboard-navigable grid |
| `components/ssr/route-display/ExpandableSectionsDisplay.tsx` | Variant: collapsible accordion sections |
| `components/ssr/route-display/FlatListDisplay.tsx` | Variant: minimal filterable list |

## Usage: Index Page

Replace any hard-coded route listing with:

```tsx
import { join } from "path";
import { RouteIndexPage } from "@/components/ssr/RouteIndexPage";

export default async function MyPage() {
  return (
    <RouteIndexPage
      directory={join(process.cwd(), "app", "(authenticated)", "my-feature")}
      basePath="/my-feature"
      title="My Feature"
    />
  );
}
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `directory` | `string` | required | Absolute path to scan |
| `basePath` | `string` | required | URL prefix for links |
| `title` | `string` | — | Page heading |
| `description` | `string` | auto-generated | Subtitle text |
| `icon` | `ComponentType` | `LayoutGrid` | Lucide icon for heading |
| `shallow` | `boolean` | `false` | Scan one level only |
| `defaultVariant` | `RouteDisplayVariant` | `"grouped-cards"` | Initial display variant |
| `children` | `ReactNode` | — | Custom content above the grid |

## Usage: Layout with Auto-Header

Replace `config.ts` + `ModuleHeader` patterns:

```tsx
import { join } from "path";
import { RouteHeaderData } from "@/components/ssr/RouteHeaderData";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <RouteHeaderData
      directory={join(process.cwd(), "app", "(authenticated)", "tests", "forms")}
      moduleHome="/tests/forms"
      moduleName="Forms"
    >
      {children}
    </RouteHeaderData>
  );
}
```

## Adding a New Display Variant

1. Create `components/ssr/route-display/MyNewDisplay.tsx`:

```tsx
"use client";
import type { RouteDisplayProps } from "./types";

export default function MyNewDisplay({ data }: RouteDisplayProps) {
  const { routes, groups, sortedGroupKeys, basePath, hasGroups } = data;
  // Render using data — import from shared.ts, NOT from index.ts
  // Use Link from "next/link" for navigation
}
```

2. Add the variant key to `types.ts`:

```ts
export type RouteDisplayVariant =
  | "grouped-cards"
  | "data-table"
  | "expandable-sections"
  | "flat-list"
  | "my-new-variant";
```

3. Add the label to `VARIANT_LABELS` in `types.ts`.

4. Register in `RouteDisplaySwitcher.tsx`:

```ts
"my-new-variant": dynamic(() => import("./MyNewDisplay"), { ssr: false }),
```

## Scanner Behavior

- Recursively walks directories looking for `page.tsx` files
- Skips: `_prefixed` directories, `[dynamic]` route segments
- Groups routes by top-level directory segment
- `scanRoutesShallow` only checks immediate children (no recursion)

## Converting Existing Routes

When converting a directory from hard-coded `config.ts` to auto-discovery:

1. Replace `page.tsx` with `RouteIndexPage` usage
2. Replace `layout.tsx` with `RouteHeaderData` (if it imported from `config.ts`)
3. Delete `config.ts`
4. Keep `EntityPack` wrappers and `export const dynamic = 'force-dynamic'` if present
5. Never touch functional leaf pages — only replace listing/index pages

## Favicon Integration

`RouteIndexPage` automatically resolves the favicon for the `basePath` and threads it into the display:

- The favicon badge renders next to the page `<h1>` title (replaces the Lucide icon when a favicon exists)
- `GroupedCardsDisplay` uses the favicon color as a left-border accent on each group card
- Flat list entries show the favicon badge instead of a plain dot

No extra code needed — just pass the correct `basePath` and the system picks up the config from `navigation-links.tsx` or the system-route overrides (`/demo`, `/tests`, `/administration`).

To understand how favicons are registered and what colors/letters are already in use, see `.claude/skills/route-metadata-favicons/SKILL.md`.

---

## Pages NOT Using This System

These have custom logic and intentionally remain hand-maintained:

- `administration/page.tsx` — curated category dashboard (has `/administration/all-routes` companion)
- `dashboard/page.tsx` — iOS-style icon grid
- `tests/links/` and `tests/windows/` — master cross-directory index lists
- `demos/local-tools/page.tsx`, `demos/scraper/page.tsx` — custom functional UIs
