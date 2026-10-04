---
name: audit-skeleton
description: Audit every page to ensure it has a layout-accurate skeleton loading state using useMinLoadTime, matching the page's actual structure (cards, grids, tables, charts, sidebars). Use after adding pages, before /complete-session, and during UX audits.
---

# audit-skeleton

Every page must show a skeleton loading state that **mirrors its actual layout** — not a generic spinner or empty div. Users should see the page's structure (metric cards, tables, charts, sidebars) shimmer into place so the transition to real content feels seamless.

## What a compliant page looks like

```tsx
import { useMinLoadTime } from "@/hooks/useMinLoadTime";
import { SomePageSkeleton } from "@/components/skeletons/page-skeletons";
import { PAGE_WRAPPER } from "@/config/platform-theme";
import PageHeader from "@/components/ui/page-header";

export default function SomePage() {
  const showSkeleton = useMinLoadTime();
  const { data, isLoading } = useQuery({ queryKey: ['/api/...'] });

  if (isLoading || showSkeleton) {
    return (
      <div className={PAGE_WRAPPER}>
        <PageHeader title="عنوان الصفحة" />
        <SomePageSkeleton />
      </div>
    );
  }

  return (
    <div className={PAGE_WRAPPER}>
      <PageHeader title="عنوان الصفحة" />
      {/* actual content */}
    </div>
  );
}
```

## Requirements for a skeleton to "match the layout"

A skeleton is **layout-accurate** when:

1. **Same grid structure** — if the page uses `GRID_METRICS` (4 cols), the skeleton renders 4 skeleton cards in the same grid
2. **Same card count & shape** — metric rows, chart areas, list items have matching skeleton counterparts
3. **Same sidebar/main split** — if the page is `lg:grid-cols-3` with a sidebar, the skeleton replicates that split
4. **Same toolbar/filter bar** — search inputs, tab triggers, view toggles get skeleton placeholders
5. **Same table structure** — header row + N body rows with matching column count
6. **Wrapped in `animate-pulse`** — the top-level skeleton div must include `animate-pulse`
7. **Uses design tokens** — `border-border`, `bg-card`, `rounded-2xl` (never hardcoded colors)

## Steps

1. **Inventory all pages**. Collect every file under `apps/web/src/pages/platform/`, `apps/web/src/pages/admin/`, and `apps/web/src/pages/client/` that exports a default component.

2. **Check each page for the skeleton pattern**. For each page grep/read for:
   - `useMinLoadTime` import — **required**
   - A skeleton component import from `@/components/skeletons/` — **required**
   - The loading guard: `if (isLoading || showSkeleton)` returning the skeleton — **required**

3. **Flag missing skeletons**. Pages that fail any check above go into the "Missing skeleton" list.

4. **Audit skeleton accuracy**. For each page that _does_ have a skeleton:
   - Read the page's **loaded state** JSX and note its layout structure (grids, cards, tables, charts, sidebar splits)
   - Read the **skeleton component** and compare it to the loaded layout
   - Flag mismatches: e.g. page has 5 metric cards but skeleton shows 4, page has a sidebar but skeleton is single-column, page has tabs but skeleton omits them

5. **Report** a table with columns:
   | Page | Status | Skeleton component | Issues |
   |------|--------|--------------------|--------|
   | leads | OK | LeadsSkeleton | — |
   | inbox | MISSING | — | No useMinLoadTime, no skeleton |
   | dashboard | MISMATCH | DashboardSkeleton | Skeleton missing the quick-actions row |

6. **Fix missing skeletons** — for each missing page:
   - Analyze the page layout
   - Create a skeleton component in `apps/web/src/components/skeletons/page-skeletons.tsx` that matches the layout
   - Wire it into the page with `useMinLoadTime`
   - Use the shared building blocks (`SkeletonCard`, `SkeletonMetricRow`, `SkeletonChartArea`, `SkeletonListItem`) where possible

7. **Fix mismatched skeletons** — update the skeleton component to match the current page layout.

8. **Run `/typecheck`** to confirm zero TS errors after all changes.

## Shared skeleton building blocks (in page-skeletons.tsx)

| Block | Use for |
|-------|---------|
| `SkeletonCard` | Single metric/stat card |
| `SkeletonMetricRow` | Row of 2-5 metric cards in `GRID_METRICS` |
| `SkeletonChartArea` | Chart container with title placeholder |
| `SkeletonListItem` | Avatar + text + badge row in a list |

If none of these fit, create a page-specific skeleton function (e.g. `InboxSkeleton`) using the same `Skeleton` primitive and `animate-pulse` pattern.

## Verification checklist

- [ ] Every page under `pages/platform/`, `pages/admin/`, `pages/client/` has a skeleton
- [ ] Every skeleton uses `useMinLoadTime` (min 2000ms)
- [ ] Every skeleton mirrors the page's grid/card/table/sidebar structure
- [ ] All skeletons use `animate-pulse` at the top level
- [ ] All skeletons use design tokens (`border-border`, `bg-card`, `rounded-2xl`) — no hardcoded colors
- [ ] All skeletons use RTL-safe classes (`ms-`, `me-`, `ps-`, `pe-`, `border-s`, `border-e`)
- [ ] `/typecheck` passes

## Anti-patterns

- Don't use a generic spinner (`<Spinner />`) as a page loading state — always use a structural skeleton
- Don't use the Suspense fallback as the skeleton — Suspense fallback is a minimal empty div; the real skeleton lives inside the page component
- Don't create a "one-size-fits-all" skeleton — each page type needs its own skeleton that matches its layout
- Don't show skeleton for less than 2s — use `useMinLoadTime(2000)` to prevent flash
- Don't put the skeleton outside `PAGE_WRAPPER` — it must be inside the same wrapper as the loaded content so spacing is consistent
