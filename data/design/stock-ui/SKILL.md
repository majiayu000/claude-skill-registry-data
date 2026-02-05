---
name: stock-ui
description: Stock analysis UI frontend. React + TypeScript with Tailwind CSS, shadcn/ui, Recharts. Use for React components, API integration, routing, state management, styling, charts visualization.
---

# Stock Insights UI Skill

A comprehensive React frontend for stock analysis featuring real-time data visualization, financial projections, and comparative analytics.

## Tech Stack

- **Framework**: React 19 + React Router 7 (file-based routing)
- **Language**: TypeScript 5.8
- **State Management**: Zustand (with devtools)
- **UI Components**: shadcn/ui (Radix UI primitives)
- **Styling**: Tailwind CSS 4.1
- **Charts**: Recharts 2.15
- **Authentication**: Clerk
- **Build Tool**: Vite 6
- **Icons**: Lucide React, Tabler Icons

## Project Structure

```
app/
├── routes/              # Page components (React Router 7 file-based)
│   ├── home.tsx        # Landing page
│   ├── search.tsx      # Stock metrics search
│   ├── compare.tsx     # Multi-stock comparison
│   ├── charts.tsx      # Financial charts visualization
│   ├── projections.tsx # Stock price projections calculator
│   └── financials.tsx  # Financial statements viewer
├── components/         # Reusable React components
│   ├── charts/        # Chart-specific components
│   ├── homepage/      # Landing page sections
│   ├── dashboard/     # Dashboard layout components
│   └── ui/            # shadcn/ui base components
├── store/             # Zustand state management
│   └── stockStore.ts  # Global app state
├── hooks/             # Custom React hooks
│   ├── useAuthenticatedFetch.ts  # Clerk auth wrapper
│   └── use-mobile.ts             # Responsive breakpoint
├── lib/               # Utility functions
│   └── utils.ts       # cn() for Tailwind class merging
├── constants/         # Static data
│   └── homeModules.ts # Feature module definitions
├── root.tsx           # Root layout with Clerk provider
└── routes.ts          # Route configuration
```

## Key Directories

- `app/routes/` - Page-level components with route handlers (loaders, actions)
- `app/components/ui/` - Base UI primitives from shadcn/ui (Button, Card, Input, etc.)
- `app/components/charts/` - Recharts wrappers (RevenueChart, EPSChart, MarginChart)
- `app/components/homepage/` - Marketing page sections (navbar, pricing, features)
- `app/store/` - Zustand store with centralized state for metrics, charts, financials
- `app/hooks/` - Reusable hooks including authenticated API calls
- `docs/` - Comprehensive UI specifications and implementation guides

## Common Tasks

### Creating Components

Components follow shadcn/ui patterns using Radix primitives and Tailwind CSS. Create functional components with TypeScript interfaces for props. Use the `cn()` utility from `lib/utils.ts` to merge Tailwind classes conditionally.

**Example pattern:**
```tsx
interface MyComponentProps {
  title: string;
  onAction: () => void;
}

export function MyComponent({ title, onAction }: MyComponentProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <Button onClick={onAction}>Action</Button>
      </CardContent>
    </Card>
  );
}
```

See `references/components.md` for detailed component hierarchy and examples.

### Making API Calls

All API calls use the `useAuthenticatedFetch` hook which wraps requests with Clerk authentication tokens. The Zustand store provides centralized fetch actions with caching for `/metrics`, `/charts`, `/financials`, and `/projections` endpoints.

**Pattern:**
```tsx
const { authenticatedFetch } = useAuthenticatedFetch();
const actions = useStockActions();

// Use store action (recommended - includes caching)
await actions.fetchCharts('AAPL', 'quarterly', authenticatedFetch);

// Or direct fetch (for custom endpoints)
const response = await authenticatedFetch(`${apiUrl}/custom`);
```

See `references/api-client.md` for complete API integration patterns and endpoint documentation.

### Adding Routes

Routes use React Router 7's file-based routing. Create a new file in `app/routes/` and register it in `routes.ts`. Each route can export `loader` (server-side data fetching), `action` (form handling), and default component.

**Steps:**
1. Create `app/routes/my-route.tsx`
2. Export default component and optional `loader`/`action`
3. Add to `routes.ts`: `route("my-route", "routes/my-route.tsx")`

See `references/routing.md` for routing patterns and protected routes.

### Styling Components

Styling uses Tailwind CSS 4.1 with utility classes. Follow mobile-first responsive design patterns. Use the `cn()` utility to conditionally merge classes. shadcn/ui components accept `className` prop for customization.

**Common patterns:**
- Spacing: `p-4`, `px-6`, `py-2`, `space-y-4`, `gap-2`
- Layout: `flex`, `grid`, `max-w-7xl`, `mx-auto`, `container`
- Colors: `bg-blue-500`, `text-gray-700`, `border-gray-200`
- Responsive: `sm:text-lg`, `md:grid-cols-2`, `lg:max-w-4xl`
- States: `hover:bg-gray-100`, `focus:ring-2`, `disabled:opacity-50`

See `references/styling.md` for Tailwind configuration and design tokens.

### Building Charts

Charts use Recharts library with custom wrappers in `app/components/charts/`. Follow existing patterns for bar charts (Revenue, EPS, Operating Income) and line charts (Margins, Cash Flow). All charts support quarterly and TTM (trailing twelve months) modes.

**Chart structure:**
```tsx
<ResponsiveContainer width="100%" height={400}>
  <BarChart data={chartData}>
    <CartesianGrid strokeDasharray="3 3" />
    <XAxis dataKey="quarter" />
    <YAxis />
    <Tooltip />
    <Bar dataKey="value" fill="#F59E0B" />
  </BarChart>
</ResponsiveContainer>
```

Charts receive data from Zustand store's `charts` state, populated by `/charts?ticker={symbol}&mode={quarterly|ttm}` endpoint.

See `references/components.md` for chart component details and data structures.

### State Management

Global state uses Zustand store (`app/store/stockStore.ts`) with separate slices for each feature:
- `globalTicker` - Current selected stock symbol
- `stockInfo` - Price, market cap, shares outstanding
- `search` - Metrics search results
- `compare` - Multi-stock comparison data
- `charts` - Chart data (revenue, EPS, margins, cash flows)
- `projections` - Base data and calculated projections
- `financials` - Historical and estimated financial statements

**Usage:**
```tsx
// Access state
const chartsState = useChartsState();
const stockInfo = useStockInfo();
const actions = useStockActions();

// Update state
actions.setGlobalTicker('AAPL');
await actions.fetchCharts('AAPL', 'quarterly', authenticatedFetch);
```

See `references/state-management.md` for complete store structure and patterns.

## API Endpoints

All endpoints require Clerk authentication via Bearer token:

- `GET /metrics?ticker={symbol}` - Stock metrics (PE ratios, growth rates, margins)
- `GET /charts?ticker={symbol}&mode={quarterly|ttm}` - Chart data (revenue, EPS, margins, cash flows)
- `GET /financials?ticker={symbol}` - Financial statements (historical + estimates)
- `GET /projections?ticker={symbol}` - Base data for projections (revenue, net income, EPS)
- `GET /stock-info?ticker={symbol}` - Current stock info (price, market cap, shares)

Base URL: `import.meta.env.VITE_API_BASE_URL`

## Development Commands

```bash
npm run dev        # Start dev server (port 5173)
npm run build      # Build for production
npm run start      # Serve production build
npm run typecheck  # Run TypeScript type checking
```

## Environment Variables

Create `.env` file:
```
VITE_API_BASE_URL=http://localhost:8000  # FastAPI backend
VITE_ENV=local                            # Environment (local/production)
CLERK_PUBLISHABLE_KEY=pk_test_...        # Clerk public key
CLERK_SECRET_KEY=sk_test_...             # Clerk secret key
```

## Key Features

1. **Search** - Find stocks and view key metrics (PE ratios, growth rates, margins)
2. **Compare** - Side-by-side comparison of up to 3 stocks
3. **Charts** - Interactive financial charts with quarterly/TTM toggle
4. **Projections** - Calculate future stock prices with custom growth inputs
5. **Financials** - View historical and estimated financial statements

## Design Patterns

- **Component Composition**: Build complex UIs from small, reusable components
- **Custom Hooks**: Extract logic into reusable hooks (useAuthenticatedFetch)
- **Centralized State**: Zustand store for global state, local useState for UI state
- **Type Safety**: TypeScript interfaces for all props, state, and API responses
- **Error Boundaries**: Route-level error handling with ErrorBoundary exports
- **Loading States**: Skeleton components and loading indicators for async operations
- **Caching**: Store-level caching for API responses to reduce backend load
- **Responsive Design**: Mobile-first Tailwind utilities with breakpoints

## Reference Documentation

- **components.md** - Complete component hierarchy and props interfaces
- **api-client.md** - API integration patterns and authentication
- **routing.md** - React Router 7 setup and route configuration
- **state-management.md** - Zustand store structure and usage patterns
- **styling.md** - Tailwind configuration and design tokens

## Additional Resources

- `docs/ui/` - Detailed UI implementation guides for each page
- `docs/prd.md` - Product requirements and feature specifications
- `docs/activity.md` - Development activity log with implementation notes

