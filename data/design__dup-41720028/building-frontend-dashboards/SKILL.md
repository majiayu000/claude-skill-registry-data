---
name: Building Frontend Dashboards
description: Build responsive React dashboards with TypeScript, shadcn/ui, TanStack Query, and Supabase for event-studio. Use when user mentions dashboard, metrics, KPI cards, data tables, charts, analytics, admin panel, Recharts, event management UI, booking interface, financial overview, or asks to create pages with data visualization.
---

# Building Frontend Dashboards

Expert in building React dashboards for the event-studio project.

## Project Context

**Tech Stack**: React 18 + TypeScript + Vite + shadcn/ui + TanStack Query + Supabase

**Structure**:
```
src/
├── pages/Dashboard*.tsx       # Route components
├── features/[feature]/hooks/  # Custom hooks (useEvents, etc.)
├── components/ui/             # shadcn/ui components
└── integrations/supabase/     # Supabase client & types
```

**Key Patterns**:
- TanStack Query for all data fetching
- Supabase for backend (use `supabase` client from `@/integrations/supabase/client`)
- shadcn/ui components (import from `@/components/ui/`)
- Zustand for state (if needed)
- React Hook Form + Zod for forms

## Standard Dashboard Workflow

Copy this checklist and track your progress:

```
Dashboard Implementation:
- [ ] 1. Identify data requirements (tables, metrics)
- [ ] 2. Create custom hook in features/[feature]/hooks/
- [ ] 3. Build page in src/pages/Dashboard*.tsx
- [ ] 4. Add metric cards and main content
- [ ] 5. Add route in App.tsx
- [ ] 6. Test loading/error states
```

### Step 1: Identify Requirements

Ask user to clarify:
- What data to display?
- What metrics/KPIs?
- What user actions?
- Filters needed?

### Step 2: Create Custom Hook

**Pattern**: Create in `src/features/[feature]/hooks/use*.ts`

```typescript
import { useQuery } from '@tanstack/react-query';
import { supabase } from '@/integrations/supabase/client';

export function useDashboardMetrics() {
  return useQuery({
    queryKey: ['dashboard-metrics'],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('events')
        .select('*, bookings(count)');
      if (error) throw error;
      return data;
    },
  });
}
```

**For more patterns**: See `resources/query-patterns.ts`

### Step 3: Build Page Structure

**Template**:

```typescript
import Sidebar from '@/components/Sidebar';
import { Card } from '@/components/ui/card';

const DashboardNew = () => {
  const { data, isLoading, error } = useYourHook();

  if (isLoading) return <PageLoader />;
  if (error) return <ErrorAlert error={error} />;

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <main className="flex-1 p-8">
        <h1 className="text-3xl font-bold mb-6">Dashboard Title</h1>

        {/* Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          {/* MetricCard components */}
        </div>

        {/* Main Content */}
        <Card className="p-6">
          {/* DataTable or Charts */}
        </Card>
      </main>
    </div>
  );
};

export default DashboardNew;
```

### Step 4: Use Reusable Components

**Import from resources**:

```typescript
import {
  MetricCard,
  DataTable,
  StatusBadge,
  EmptyState,
  ErrorAlert
} from '../skills/frontend-dashboard/resources/component-patterns';
```

**See complete examples**: `resources/component-patterns.tsx`

## Quick Reference

### Supabase Queries

```typescript
// Simple query
const { data } = await supabase.from('events').select('*');

// With joins
const { data } = await supabase
  .from('events')
  .select('*, bookings(*), organizer:users(full_name)');

// With filters
const { data } = await supabase
  .from('events')
  .select('*')
  .eq('status', 'active')
  .gte('start_date', date);
```

**More patterns**: See `resources/supabase-patterns.ts`

### Common Components

```typescript
// Metric Card
<MetricCard
  title="Total Revenue"
  value="$125,000"
  change={12.5}
  icon={<DollarSign />}
/>

// Data Table
<DataTable
  data={events}
  columns={[
    { key: 'title', label: 'Event' },
    { key: 'status', label: 'Status', render: (v) => <StatusBadge status={v} /> }
  ]}
  onEdit={(row) => handleEdit(row)}
/>

// Empty State
<EmptyState
  title="No events yet"
  description="Get started by creating your first event"
  action={{ label: "Create Event", onClick: () => navigate('/new') }}
/>
```

### Layouts

**7 layout patterns** in `resources/layout-examples.tsx`:
- StandardDashboardLayout (sidebar + content)
- DashboardWithActionsBar (search + filters)
- TabbedDashboard (multi-tab analytics)
- SplitViewDashboard (list + detail)
- GridViewDashboard (grid/list toggle)
- ResponsiveDashboard (mobile-first)
- StickyHeaderDashboard (fixed header)

## Examples

### Example 1: Events Dashboard

**User**: "Create a dashboard page showing all events with metrics"

**Your Process**:

1. **Create hook** (`src/features/events/hooks/useEventsDashboard.ts`):
```typescript
export function useEventsDashboard() {
  return useQuery({
    queryKey: ['events-dashboard'],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('events')
        .select('*, bookings(count, total_amount.sum())')
        .order('created_at', { ascending: false });
      if (error) throw error;
      return data;
    },
  });
}
```

2. **Create page** (`src/pages/DashboardEvents.tsx`) with:
   - Header with "Create Event" button
   - 4 metric cards (total events, active events, revenue, bookings)
   - Search bar and filters
   - DataTable with events
   - Actions: edit, delete, view details

3. **Add route** in `App.tsx`:
```typescript
<Route path="/dashboard/events" element={<DashboardEvents />} />
```

### Example 2: Analytics Dashboard with Charts

**User**: "Add a revenue analytics page with charts"

**Your Response**:

1. Create `useRevenueAnalytics` hook fetching bookings with date grouping
2. Build page with:
   - Revenue metrics cards
   - Line chart (Recharts) showing revenue over time
   - Pie chart for revenue by category
3. Use Recharts components from `recharts` package
4. Add date range filter

### Example 3: Bookings Management

**User**: "Create a bookings dashboard with search and filters"

**Your Implementation**:
- Search by attendee name
- Filter by status (pending, confirmed, cancelled)
- DataTable with booking details
- Actions: view ticket, refund, send email
- Export to CSV button

## Best Practices

**Always**:
- Show loading states (skeleton or spinner)
- Handle errors with user-friendly messages
- Make responsive (use `md:`, `lg:` prefixes)
- Use TypeScript strictly (no `any`)
- Validate permissions before showing data

**Performance**:
- Implement pagination for large datasets
- Use proper TanStack Query caching (`queryKey`)
- Optimize with `React.memo` if needed

**UX**:
- Provide empty states
- Use toast notifications (from `sonner`)
- Make actions reversible
- Show success feedback

## Resources

**Complete examples and patterns**:
- `resources/component-patterns.tsx` - Reusable components (MetricCard, DataTable, etc.)
- `resources/query-patterns.ts` - TanStack Query hooks and patterns
- `resources/supabase-patterns.ts` - Supabase query examples
- `resources/layout-examples.tsx` - 7 dashboard layout templates

## Troubleshooting

**Query not refetching**: Use `invalidateQueries` in mutation `onSuccess`

**RLS blocking queries**: Check Supabase RLS policies allow the operation

**TypeScript errors**: Regenerate types with `npx supabase gen types typescript`

**Not responsive**: Use Tailwind responsive prefixes, test in dev tools
