---
name: advanced-tables-components
description: Comprehensive advanced table components skill for Next.js applications with TanStack Table v8, server-side operations, and Supabase integration. Use when building data-intensive tables with features like server-side pagination/sorting/filtering, column management, row selection, bulk actions, export functionality, real-time updates, and advanced filtering UI. Covers complete workflow from database design to production-ready table implementations with shadcn/ui components. Automatically triggers for data tables, admin dashboards, report views, or any complex tabular data display needs.
---

# Advanced Tables Components

Complete production-ready patterns for building feature-rich data tables in Next.js with server-side operations, advanced filtering, and optimal performance.

## Core Philosophy

**Server-First Architecture**: All heavy operations (sorting, filtering, pagination) happen on the server to handle large datasets efficiently.

**Progressive Enhancement**: Tables work without JavaScript, then enhance with client-side features for better UX.

**Type-Safe End-to-End**: Full TypeScript coverage from database to UI components.

## When to Use This Skill

Use this skill when:

- **Building data-intensive tables** with 1000+ rows requiring server-side operations
- **Creating admin dashboards** with complex filtering and bulk operations
- **Implementing report views** with export, grouping, and aggregation features
- **Developing CRUD interfaces** with inline editing and optimistic updates
- **Building real-time tables** with live data updates via subscriptions
- **Creating responsive tables** that adapt to mobile/tablet/desktop
- **Implementing data grids** with virtualization for massive datasets
- **Building analytics dashboards** with sortable, filterable metrics
- **Creating audit logs** or activity feeds with advanced search
- **Implementing inventory systems** with complex filtering needs

## Quick Decision Framework

### Table Type Selection

```
Dataset size and requirements?
├─ < 100 rows → Simple client-side table
├─ 100-1000 rows → Hybrid approach (initial server load + client operations)
├─ 1000-10000 rows → Server-side with pagination
├─ 10000+ rows → Server-side with virtualization
└─ Real-time updates → Server-side with subscriptions
```

### Feature Selection Matrix

| Feature          | Small Dataset | Medium Dataset    | Large Dataset       | Real-time         |
| ---------------- | ------------- | ----------------- | ------------------- | ----------------- |
| Pagination       | Optional      | Recommended       | Required            | Required          |
| Virtualization   | No            | Optional          | Recommended         | Recommended       |
| Server Sorting   | No            | Optional          | Required            | Required          |
| Server Filtering | No            | Recommended       | Required            | Required          |
| Row Selection    | Client        | Hybrid            | Server-aware        | Server-aware      |
| Bulk Actions     | Client        | Server            | Server (batched)    | Server (queued)   |
| Export           | Client        | Server (streamed) | Server (background) | Server (snapshot) |

## Project Setup Workflow

### 1. Install Dependencies

```bash
# Core table dependencies
npm install @tanstack/react-table@latest
npm install @tanstack/match-sorter-utils

# UI components (shadcn/ui)
npx shadcn@latest add table button input select checkbox dropdown-menu
npx shadcn@latest add command popover badge separator skeleton
npx shadcn@latest add sheet dialog tooltip calendar slider

# Additional utilities
npm install nuqs date-fns clsx tailwind-merge
npm install sonner lucide-react
npm install @dnd-kit/core @dnd-kit/sortable @dnd-kit/utilities
npm install papaparse xlsx file-saver
```

### 2. Create Project Structure

```
components/
├── data-table/
│   ├── data-table.tsx                    # Core table component
│   ├── data-table-toolbar.tsx            # Search, filters, actions
│   ├── data-table-column-header.tsx      # Sortable headers
│   ├── data-table-pagination.tsx         # Pagination controls
│   ├── data-table-view-options.tsx       # Column visibility
│   ├── data-table-faceted-filter.tsx     # Multi-select filters
│   ├── data-table-date-filter.tsx        # Date range filters
│   ├── data-table-slider-filter.tsx      # Numeric range filters
│   ├── data-table-action-bar.tsx         # Bulk action floating bar
│   ├── data-table-row-actions.tsx        # Row-level actions
│   ├── data-table-export.tsx             # Export functionality
│   └── data-table-skeleton.tsx           # Loading states
lib/
├── table/
│   ├── hooks.ts                          # useDataTable, useTableState
│   ├── utils.ts                          # Table utilities
│   ├── filters.ts                        # Filter functions
│   ├── export.ts                         # Export utilities
│   └── types.ts                          # TypeScript definitions
```

## Implementation Workflow

### Step 1: Define Table Requirements

Before implementing, answer these questions:

1. **Dataset Size**: How many rows will the table display? (determines server vs client operations)
2. **Features Needed**: Which features from the matrix above are required?
3. **Data Source**: Supabase table or custom API endpoint?
4. **Update Frequency**: Static, periodic refresh, or real-time?
5. **User Interactions**: Read-only, inline editing, or bulk operations?

### Step 2: Set Up Data Layer

Based on the requirements, implement the appropriate data fetching pattern:

- **Server-Side Tables (1000+ rows)**: Use `references/core-patterns.md` Pattern 2: Data Fetching with Supabase
- **Real-Time Tables**: Use `references/advanced-features.md` Pattern 7: Real-time Updates
- **Client-Side Tables (<100 rows)**: Fetch all data once and use TanStack Table's built-in features

### Step 3: Create Column Definitions

Define table columns with appropriate features:

- Use `references/core-patterns.md` Pattern 3: Advanced Column Configuration
- Configure filter types (text, select, date range, slider)
- Add sortable headers where needed
- Include selection column for bulk actions
- Add actions column for row-level operations

### Step 4: Implement Core Table Component

Build the main table component:

- Use `references/core-patterns.md` Pattern 1: Server-Side Data Table hook
- Implement URL-based state management for filters/sorting/pagination
- Add loading states and error handling
- Include empty state UI

### Step 5: Add Filtering & Actions

Enhance the table with user interactions:

- **Advanced Filtering**: Use `references/filtering-actions.md` Pattern 4: Advanced Filtering UI
- **Bulk Actions**: Use `references/filtering-actions.md` Pattern 5: Action Bar for Bulk Operations
- **Export**: Use `references/filtering-actions.md` Pattern 6: Export Functionality

### Step 6: Optimize Performance

Apply performance optimizations:

- **For large datasets**: Use `references/advanced-features.md` Virtual Scrolling pattern
- **For expensive renders**: Follow `references/performance-best-practices.md` React Optimization
- **For database queries**: Apply `references/performance-best-practices.md` Query Optimization

### Step 7: Add Optional Features

Based on requirements, add additional features:

- **Inline Editing**: `references/advanced-features.md` Pattern 8: Inline Editing
- **Column Resizing**: `references/advanced-features.md` Column Resizing and Reordering
- **Real-time Updates**: `references/advanced-features.md` Pattern 7: Real-time Updates with Supabase

## Best Practices

### DO:

- ✅ Use server-side operations for datasets > 1000 rows
- ✅ Implement proper loading states with skeletons
- ✅ Add keyboard navigation (arrow keys, tab, enter)
- ✅ Provide clear empty states with actions
- ✅ Use optimistic updates for better perceived performance
- ✅ Implement proper error boundaries and fallbacks
- ✅ Add accessibility attributes (aria-labels, roles)
- ✅ Cache filter/sort preferences in localStorage
- ✅ Use debouncing for search inputs (300ms)
- ✅ Implement progressive enhancement
- ✅ Add analytics tracking for user interactions
- ✅ Use virtualization for datasets > 10,000 rows

### DON'T:

- ❌ Load entire datasets into memory
- ❌ Perform complex calculations in render
- ❌ Use index as key for dynamic rows
- ❌ Forget to handle loading/error states
- ❌ Implement filtering/sorting on client for large datasets
- ❌ Block UI during bulk operations
- ❌ Forget to cleanup subscriptions
- ❌ Use synchronous operations for data mutations

## Accessibility Checklist

- [ ] Table has proper ARIA labels
- [ ] Sortable columns indicate sort direction
- [ ] Filter inputs have labels and descriptions
- [ ] Keyboard navigation works (Tab, Arrow keys)
- [ ] Screen reader announces row selection
- [ ] Loading states are announced
- [ ] Error messages are accessible
- [ ] Color contrast meets WCAG standards
- [ ] Focus indicators are visible
- [ ] Bulk actions are keyboard accessible

## Resources

This skill includes detailed reference documentation for implementation patterns:

### references/core-patterns.md
Core implementation patterns including:
- Server-side data table hooks with URL state management
- Data fetching with Supabase including filtering, sorting, and pagination
- Advanced column configuration with different filter types

### references/filtering-actions.md
Advanced filtering and action patterns including:
- Advanced filtering UI with multiple filter types
- Action bar for bulk operations with floating UI
- Export functionality for CSV, XLSX, and JSON formats

### references/advanced-features.md
Advanced table features including:
- Virtual scrolling for large datasets
- Column resizing and reordering
- Inline editing with optimistic updates
- Real-time updates with Supabase subscriptions

### references/performance-best-practices.md
Performance optimization and best practices including:
- Database query optimization with indexes
- React optimization with memoization
- Testing strategies
- Migration guides
- Troubleshooting common issues

---

To implement a data table, start by determining the dataset size and required features using the Quick Decision Framework, then follow the Implementation Workflow step by step, referencing the appropriate patterns from the references/ files as needed.
