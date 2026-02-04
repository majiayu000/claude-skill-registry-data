---
name: frontend-dev
description: Astro + React islands with TanStack (Query, Form, Table) and Tailwind CSS. Use for frontend UI development, components, data fetching, forms, and styling.
---

# Frontend Development

**Activation:** Astro, React, TanStack, Query, Form, Table, Tailwind, component, island, page, UI

> **CRITICAL: Container-First Execution**
>
> **NEVER** run Node/pnpm commands directly on the host. Always use Docker:
> ```bash
> # WRONG - will fail with Volta error
> pnpm lint
> pnpm tsc --noEmit
>
> # RIGHT - use Docker
> docker compose exec frontend pnpm lint
> docker compose exec frontend pnpm check
> ```
> See `.claude/rules/container-execution.md` for full details.

> **CRITICAL:** This project uses **SSG (Static Site Generation) + nginx** architecture.
> See **AGENTS.md § Frontend Architecture Principles** for the authoritative documentation.
>
> Key points:
> - **NO SSR** - Never use `output: 'server'` in astro.config.mjs
> - Dynamic routes use **client-side routing** - React island reads URL, fetches via API
> - Production is **nginx + static files only** - no Node.js runtime

## Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Framework | Astro | Static pages, file-based routing |
| Islands | React 19 | Interactive components |
| Data | TanStack Query | Server state, caching |
| Forms | TanStack Form | Type-safe form handling |
| Tables | TanStack Table | Headless data tables |
| Styling | Tailwind CSS | Utility-first CSS |

## Architecture

```
frontend/src/
├── pages/              # Astro pages (routing)
├── layouts/            # Page layouts
├── components/         # React islands
│   ├── ui/            # Reusable UI components
│   └── features/      # Feature-specific components
├── lib/               # Utilities
│   ├── api.ts         # API client + TanStack Query
│   └── hooks/         # Custom hooks
└── styles/            # Global styles
```

## Design Principles

This is a **professional tool for musicians and audio engineers**:

1. **Clean & Functional** - Prioritize usability over novelty
2. **Aesthetically Pleasing** - Well-proportioned, consistent spacing
3. **Professional Polish** - Subtle shadows, smooth transitions
4. **Content-First** - UI supports the workflow, doesn't distract

### Visual Guidelines

```css
/* Color palette: Neutral with accent */
--color-bg: #ffffff;
--color-surface: #f8fafc;
--color-border: #e2e8f0;
--color-text: #1e293b;
--color-muted: #64748b;
--color-accent: #3b82f6;      /* Blue for actions */
--color-success: #22c55e;
--color-error: #ef4444;

/* Spacing: Consistent scale */
/* Use Tailwind: p-2, p-4, p-6, gap-4, gap-6 */

/* Shadows: Subtle depth */
/* shadow-sm for cards, shadow-md for modals */

/* Transitions: Smooth, not flashy */
/* transition-colors duration-150 */
```

## Astro Pages

### Static Pages (Standard)

```astro
---
// src/pages/browse.astro
import Layout from '../layouts/Layout.astro';
import BrowseContent from '../components/browse/BrowseContent';
---

<Layout title="Browse Shootouts">
  <BrowseContent client:load />
</Layout>
```

### Dynamic Routes (Client-Side)

For routes like `/shootout/{id}`, create a shell page that handles ALL IDs:

```astro
---
// src/pages/shootout/index.astro
// This single file handles /shootout/123, /shootout/abc, etc.
import Layout from '../../layouts/Layout.astro';
import ShootoutDetail from '../../components/shootout/ShootoutDetail';
---

<Layout title="Shootout">
  <ShootoutDetail client:load />
</Layout>
```

The React component reads the URL and fetches data:

```tsx
// components/shootout/ShootoutDetail.tsx
export function ShootoutDetail() {
  const shootoutId = window.location.pathname.split('/shootout/')[1];
  const { data, isLoading, error } = useQuery({
    queryKey: ['shootout', shootoutId],
    queryFn: () => fetchShootout(shootoutId),
    enabled: !!shootoutId,
  });
  // ...render based on data
}
```

### Hydration Directives

```astro
<!-- Immediate: Above fold, needs interactivity -->
<PipelineBuilder client:load />

<!-- Visible: Below fold, load when scrolled to -->
<ShootoutList client:visible />

<!-- Idle: Low priority, load when browser idle -->
<Analytics client:idle />
```

## TanStack Query

### Setup

```typescript
// src/lib/api.ts
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 1,
    },
  },
});

const API_BASE = import.meta.env.PUBLIC_API_URL;

export async function fetchJSON<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, { credentials: 'include' });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}
```

### Queries

```typescript
// src/lib/hooks/useShootouts.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { fetchJSON } from '../api';

export function useShootouts() {
  return useQuery({
    queryKey: ['shootouts'],
    queryFn: () => fetchJSON<Shootout[]>('/shootouts'),
  });
}

export function useShootout(id: number) {
  return useQuery({
    queryKey: ['shootouts', id],
    queryFn: () => fetchJSON<Shootout>(`/shootouts/${id}`),
    enabled: !!id,
  });
}

export function useCreateShootout() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: ShootoutCreate) =>
      fetch('/api/shootouts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
        credentials: 'include',
      }).then(res => res.json()),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['shootouts'] });
    },
  });
}
```

### In Components

```tsx
export function ShootoutList({ userId }: { userId: number }) {
  const { data: shootouts, isLoading, error } = useShootouts();

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message="Failed to load shootouts" />;

  return (
    <ul className="divide-y divide-gray-200">
      {shootouts?.map(shootout => (
        <ShootoutItem key={shootout.id} shootout={shootout} />
      ))}
    </ul>
  );
}
```

## TanStack Form

```tsx
import { useForm } from '@tanstack/react-form';

interface ShootoutFormData {
  title: string;
  description: string;
}

export function CreateShootoutForm({ onSubmit }: { onSubmit: (data: ShootoutFormData) => void }) {
  const form = useForm({
    defaultValues: { title: '', description: '' },
    onSubmit: async ({ value }) => {
      onSubmit(value);
    },
  });

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        form.handleSubmit();
      }}
      className="space-y-4"
    >
      <form.Field
        name="title"
        validators={{
          onChange: ({ value }) =>
            value.length < 3 ? 'Title must be at least 3 characters' : undefined,
        }}
      >
        {(field) => (
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Title
            </label>
            <input
              type="text"
              value={field.state.value}
              onChange={(e) => field.handleChange(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm
                         focus:border-blue-500 focus:ring-blue-500"
            />
            {field.state.meta.errors && (
              <p className="mt-1 text-sm text-red-600">{field.state.meta.errors}</p>
            )}
          </div>
        )}
      </form.Field>

      <button
        type="submit"
        disabled={!form.state.canSubmit}
        className="px-4 py-2 bg-blue-600 text-white rounded-md
                   hover:bg-blue-700 disabled:opacity-50 transition-colors"
      >
        Create Shootout
      </button>
    </form>
  );
}
```

## TanStack Table

```tsx
import { useReactTable, getCoreRowModel, flexRender } from '@tanstack/react-table';

const columns = [
  { accessorKey: 'title', header: 'Title' },
  { accessorKey: 'status', header: 'Status' },
  { accessorKey: 'createdAt', header: 'Created',
    cell: ({ getValue }) => new Date(getValue()).toLocaleDateString() },
];

export function ShootoutsTable({ data }: { data: Shootout[] }) {
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <table className="min-w-full divide-y divide-gray-200">
      <thead className="bg-gray-50">
        {table.getHeaderGroups().map(headerGroup => (
          <tr key={headerGroup.id}>
            {headerGroup.headers.map(header => (
              <th key={header.id} className="px-6 py-3 text-left text-xs font-medium
                                             text-gray-500 uppercase tracking-wider">
                {flexRender(header.column.columnDef.header, header.getContext())}
              </th>
            ))}
          </tr>
        ))}
      </thead>
      <tbody className="bg-white divide-y divide-gray-200">
        {table.getRowModel().rows.map(row => (
          <tr key={row.id} className="hover:bg-gray-50">
            {row.getVisibleCells().map(cell => (
              <td key={cell.id} className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {flexRender(cell.column.columnDef.cell, cell.getContext())}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

## UI Components

### Button

```tsx
const variants = {
  primary: 'bg-blue-600 text-white hover:bg-blue-700',
  secondary: 'bg-gray-100 text-gray-900 hover:bg-gray-200',
  danger: 'bg-red-600 text-white hover:bg-red-700',
};

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: keyof typeof variants;
}

export function Button({ variant = 'primary', className, ...props }: ButtonProps) {
  return (
    <button
      className={`px-4 py-2 rounded-md font-medium transition-colors
                  disabled:opacity-50 ${variants[variant]} ${className}`}
      {...props}
    />
  );
}
```

### Card

```tsx
export function Card({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={`bg-white rounded-lg border border-gray-200 shadow-sm ${className}`}>
      {children}
    </div>
  );
}

export function CardHeader({ children }: { children: React.ReactNode }) {
  return <div className="px-6 py-4 border-b border-gray-200">{children}</div>;
}

export function CardContent({ children }: { children: React.ReactNode }) {
  return <div className="px-6 py-4">{children}</div>;
}
```

## Accessibility (WCAG 2.1 AA)

- Color contrast: 4.5:1 for text, 3:1 for UI
- Focus indicators: `focus:ring-2 focus:ring-blue-500`
- Keyboard navigation: All interactive elements focusable
- Labels: All form inputs have labels
- Alt text: All images have descriptive alt

## MCP Tools for Development

### Development (Chrome DevTools)

Use Chrome DevTools MCP for interactive debugging during development:

```
mcp__chrome-devtools__navigate          - Navigate to page
mcp__chrome-devtools__get_console_logs  - Check for errors
mcp__chrome-devtools__get_computed_style - Debug CSS issues
mcp__chrome-devtools__get_element_info   - Inspect layout/box model
mcp__chrome-devtools__get_network_logs   - Debug API calls
```

**Best for:** CSS debugging, real-time iteration, network inspection, performance profiling.

### PR Verification (Playwright)

Use Playwright MCP for automated verification before PR:

```
mcp__playwright__browser_navigate       - Navigate to page
mcp__playwright__browser_console_messages - Check console errors
mcp__playwright__browser_network_requests - Verify API success
mcp__playwright__browser_take_screenshot  - Capture proof
```

**Best for:** Screenshot evidence, automated checks, PR verification.

See `chrome-devtools` and `playwright` skills for full documentation.

## Quality Commands

```bash
docker compose exec frontend pnpm lint
docker compose exec frontend pnpm tsc --noEmit
docker compose exec frontend pnpm build
```

## Resources

See `resources/` for:
- `tanstack-patterns.md` - Advanced TanStack patterns
- `component-library.md` - Full UI component set
