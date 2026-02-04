---
name: nextjs-data-table-page
description: Create Next.js data table pages with SSR initial load, SWR caching, and server-response-based UI updates. Use when asked to create a new data table page, entity management page, CRUD table, or admin list view. Generates page.tsx (SSR), table components, columns, context, actions, and API routes following a proven architecture with centralized reusable data-table component.
---

# Next.js Data Table Page Generator

Create production-ready data table pages with:
- **SSR initial data loading** for fast first paint
- **Flexible data fetching** - Simple state or SWR based on needs
- **URL-based state** for filters/pagination via `nuqs`
- **Centralized data-table** from `@/components/data-table`
- **Type-safe columns** with TanStack Table
- **Context-based actions** for CRUD operations

## Data Fetching Strategy

**Before generating, determine the appropriate strategy:**

### Decision Question
**Does this table's data change without user action?**

| Answer | Strategy | Use When |
|--------|----------|----------|
| **No** | A: Simple Fetching (Default) | Settings, admin CRUD, most entity tables |
| **Yes** | B: SWR Fetching | Dashboards, multi-user editing, live monitoring |

### Strategy A: Simple Fetching (Recommended for CRUD Tables)
- Use `useState` for local data management
- Update state from server mutation responses
- No automatic revalidation
- Lower complexity, no SWR dependency
- **See:** [nextjs/references/simple-fetching-pattern.md](../nextjs/references/simple-fetching-pattern.md)

### Strategy B: SWR Fetching (Requires Justification)
- Use `useSWR` with documented justification
- Configure appropriate revalidation triggers
- For dashboards and multi-user scenarios
- **See:** [nextjs/references/swr-fetching-pattern.md](../nextjs/references/swr-fetching-pattern.md)

**Decision framework:** [nextjs/references/data-fetching-strategy.md](../nextjs/references/data-fetching-strategy.md)

## Architecture Overview

```
app/(pages)/[section]/[entity]/
├── page.tsx                          # SSR entry point
├── context/
│   └── [entity]-actions-context.tsx  # Actions provider
└── _components/
    ├── table/
    │   ├── [entity]-table.tsx        # Main client wrapper (SWR)
    │   ├── [entity]-table-body.tsx   # DataTable + columns
    │   ├── [entity]-table-columns.tsx# Column definitions
    │   ├── [entity]-table-controller.tsx # Toolbar/bulk actions
    │   └── [entity]-table-actions.tsx # Bulk action hooks
    ├── actions/
    │   ├── add-[entity]-button.tsx   # Add button + sheet
    │   └── actions-menu.tsx          # Row action menu
    ├── modal/
    │   ├── add-[entity]-sheet.tsx    # Create form
    │   ├── edit-[entity]-sheet.tsx   # Edit form
    │   └── view-[entity]-sheet.tsx   # View details
    └── sidebar/
        └── status-panel.tsx          # Stats sidebar

app/api/[section]/[entity]/
├── route.ts                          # GET (list) + POST (create)
├── [entityId]/
│   ├── route.ts                      # PUT (update)
│   └── status/route.ts               # PUT (status toggle)
└── status/route.ts                   # POST (bulk status)
```

## Quick Start

1. **Gather requirements**: Entity name, fields, API endpoints, actions needed
2. **Generate files** in order: types → API routes → page → table → columns → context → actions
3. **Verify** data-table component exists at `@/components/data-table`

## File Generation Order

### 1. Types (if not existing)
Define response types in `@/lib/types/api/[entity].ts`. See [references/types-pattern.md](references/types-pattern.md).

### 2. API Routes
Create Next.js API routes that proxy to backend. See [references/api-routes-pattern.md](references/api-routes-pattern.md).

### 3. SSR Page (`page.tsx`)
```tsx
import { auth } from "@/lib/auth/server-auth";
import { get[Entity]s } from "@/lib/actions/[entity].actions";
import { redirect } from "next/navigation";
import [Entity]Table from "./_components/table/[entity]-table";

export default async function [Entity]Page({
  searchParams,
}: {
  searchParams: Promise<{
    is_active?: string;
    search?: string;
    page?: string;
    limit?: string;
  }>;
}) {
  const session = await auth();
  if (!session?.accessToken) redirect("/login");

  const params = await searchParams;
  const pageNumber = Number(params.page) || 1;
  const limitNumber = Number(params.limit) || 10;
  const skip = (pageNumber - 1) * limitNumber;

  const data = await get[Entity]s(limitNumber, skip, {
    is_active: params.is_active,
    search: params.search,
  });

  return <[Entity]Table initialData={data} />;
}
```

### 4. Main Table Component
See [references/table-component-pattern.md](references/table-component-pattern.md) for the full pattern with:
- SWR setup with `fallbackData: initialData`
- Action handlers that return server responses
- `updateItems()` function for cache mutation
- `ActionsProvider` wrapper

### 5. Table Body + Columns
See [references/columns-pattern.md](references/columns-pattern.md) for:
- Column definitions with `updatingIds` loading states
- Selection column with checkbox
- Status toggle with confirmation
- Actions column placeholder

### 6. Context + Actions
See [references/context-pattern.md](references/context-pattern.md) for:
- Context provider setup
- Bulk action hooks
- Error handling patterns

### 7. Edit/Add Sheets
See [references/edit-sheet-pattern.md](references/edit-sheet-pattern.md) for:
- Fetch-then-open pattern (load complete entity before opening sheet)
- Row actions with loading states
- Edit sheet component structure
- Form handling with server response updates

## Core Principles

### Server Response Updates (NOT Optimistic)

Both strategies use server responses to update the UI:

```tsx
// ✅ CORRECT: Use server response
const { data: updated } = await fetchClient.put(`/api/entity/${id}`, body);
updateItems([updated]); // Update local state with server data

// ❌ WRONG: Optimistic update
const optimistic = { ...current, ...changes };
setData({ items: [...items.filter(i => i.id !== id), optimistic] });
```

### Strategy A: Simple State Management (Default)
```tsx
// No SWR - use React state
const [data, setData] = useState<Response>(initialData);

const updateItems = (serverResponse: Item[]) => {
  setData(current => {
    const responseMap = new Map(serverResponse.map(i => [i.id, i]));
    return {
      ...current,
      items: current.items.map(item =>
        responseMap.has(item.id) ? responseMap.get(item.id)! : item
      ),
    };
  });
};
```

### Strategy B: SWR Configuration (When Justified)
```tsx
/**
 * SWR JUSTIFICATION:
 * - Reason: [Document why revalidation is needed]
 * - Trigger: [Interval / Focus / Manual]
 */
const { data, mutate } = useSWR<Response>(apiUrl, fetcher, {
  fallbackData: initialData ?? undefined,
  keepPreviousData: true,
  revalidateOnMount: false,
  revalidateIfStale: true,
  revalidateOnFocus: false,  // Set true only if justified
  revalidateOnReconnect: false,
});
```

### URL-Based State
```tsx
// Use nuqs for URL params (auto-triggers SWR refetch)
const [page, setPage] = useQueryState("page", parseAsInteger.withDefault(1));
const [filter] = useQueryState("filter");

// Build API URL from params
const params = new URLSearchParams();
params.append("skip", ((page - 1) * limit).toString());
if (filter) params.append("search", filter);
const apiUrl = `/api/entity?${params.toString()}`;
```

### Cache Update Pattern
```tsx
const updateItems = async (serverResponse: EntityResponse[]) => {
  const currentData = data;
  if (!currentData) return;

  const responseMap = new Map(serverResponse.map(item => [item.id, item]));
  const updatedList = currentData.items.map(item =>
    responseMap.has(item.id) ? responseMap.get(item.id)! : item
  );

  await mutate(
    { ...currentData, items: updatedList },
    { revalidate: false }
  );
};
```

## Required Dependencies

Ensure project has:
- `nuqs` - URL state management
- `@tanstack/react-table` - Table primitives
- `@/components/data-table` - Reusable table components (must exist)
- `swr` - Only if using Strategy B (SWR fetching)

## Checklist

- [ ] Data fetching strategy selected (A or B)
- [ ] Types defined for entity and response
- [ ] API routes created (GET, POST, PUT, bulk status)
- [ ] SSR page fetches initial data
- [ ] Main table uses selected strategy:
  - Strategy A: `useState` with initialData
  - Strategy B: `useSWR` with fallbackData + justification comment
- [ ] Actions return server response (not optimistic)
- [ ] Columns show loading state via updatingIds
- [ ] Context provides actions to children
- [ ] Bulk actions use hook pattern
- [ ] URL params drive filtering/pagination
- [ ] Edit sheets use fetch-then-open pattern (not row.original)
