---
name: coding-patterns
description: Use this when writing or modifying code in FOSSAPP. Provides Next.js App Router patterns, server action organization, dual Supabase client rules, TypeScript conventions, validation patterns, error handling, and naming conventions.
---

# FOSSAPP Coding Patterns

Essential patterns and conventions for writing code in FOSSAPP. Follow these patterns for all new features and modifications.

---

## Module Splitting (MANDATORY)

**Large files MUST be split** into focused, single-responsibility modules.

### Thresholds

| File Size | Action |
|-----------|--------|
| > 500 lines | Consider splitting |
| > 800 lines | **MUST split** |

### Patterns

**Server Actions** → Create subdirectory with focused modules:
```
src/lib/actions/
├── projects.ts           # Re-export (backward compat)
└── projects/             # Focused modules
    ├── index.ts          # Barrel export (NO 'use server')
    ├── project-crud-actions.ts   # Has 'use server'
    └── project-product-actions.ts
```

**Page Components** → Co-locate with page.tsx:
```
src/app/projects/[id]/
├── page.tsx              # Main (reduced to ~500 lines)
└── components/
    ├── index.ts          # Barrel export
    ├── project-overview-tab.tsx
    └── utils.tsx
```

**Complex Components** → Extract sub-components:
```
src/components/planner/
├── planner-viewer.tsx    # Main component
├── viewer-toolbar.tsx    # Extracted
└── viewer-overlays.tsx   # Extracted
```

### Key Rules

1. **Barrel exports** (`index.ts`) must NOT have `'use server'`
2. Each action file has `'use server'` at top
3. Original files become re-exports for backward compatibility
4. Use descriptive names: `*-crud-actions.ts`, `*-tab.tsx`

**Full details**: `.claude/monorepo-development-guidelines.md`

---

## Server Actions (Domain Organization)

### Structure

Organize server actions by **business domain**, not operation type:

```
src/lib/actions/
├── index.ts          # Re-exports all actions
├── validation.ts     # Shared validation utilities
├── dashboard.ts      # Stats, analytics, aggregations
├── customers.ts      # Customer CRUD
├── products.ts       # Product search, details
├── projects.ts       # Project management
└── taxonomy.ts       # Category tree operations
```

### Pattern for Domain Files

```typescript
// src/lib/actions/[domain].ts
'use server'

import { supabaseServer } from '../supabase-server'
import { validateXxx } from './validation'
import { PAGINATION } from '@/lib/constants'

// ============================================================================
// INTERFACES
// ============================================================================

export interface DomainItem {
  id: string
  name: string
}

export interface DomainListParams {
  page?: number
  pageSize?: number
  sortBy?: string
  sortOrder?: 'asc' | 'desc'
}

// ============================================================================
// SEARCH
// ============================================================================

export async function searchDomainAction(query: string): Promise<DomainItem[]> {
  try {
    const sanitizedQuery = validateSearchQuery(query)

    const { data, error } = await supabaseServer
      .schema('schema_name')
      .from('table_name')
      .select('...')
      .ilike('name', `%${sanitizedQuery}%`)
      .limit(PAGINATION.DEFAULT_SEARCH_LIMIT)

    if (error) {
      console.error('Domain search error:', error)
      return []
    }

    return data || []
  } catch (error) {
    console.error('Search domain error:', error)
    return []
  }
}
```

### Importing Actions

```typescript
// Preferred: Import from domain file directly
import { searchCustomersAction } from '@/lib/actions/customers'

// Also valid: Import from index (backward compatible)
import { searchCustomersAction } from '@/lib/actions'
```

---

## Dual Supabase Client Pattern ⚠️ CRITICAL

**NEVER mix these up!** Using the wrong client is a security vulnerability.

### Server-Side (Actions & API Routes)

```typescript
import { supabaseServer } from '@/lib/supabase-server'

export async function serverAction() {
  const { data, error } = await supabaseServer
    .from('items.product_info')
    .select('*')

  return data
}
```

**Uses:** `SUPABASE_SERVICE_ROLE_KEY` (full admin access)
**Never expose to client!**

### Client-Side (Components)

```typescript
import { supabase } from '@/lib/supabase'

export function ClientComponent() {
  const fetchData = async () => {
    const { data } = await supabase
      .from('items.product_info')
      .select('*')
    return data
  }
}
```

**Uses:** `NEXT_PUBLIC_SUPABASE_ANON_KEY` (limited permissions)

### Rule of Thumb

- **Server actions** → `supabaseServer` (service role)
- **API routes** → `supabaseServer` (service role)
- **Client components** → `supabase` (anon key)
- **When in doubt** → Use server action with `supabaseServer`

---

## Server vs Client Components

### Default: Server Components

```typescript
// No 'use client' directive = Server Component
export default function ProductPage() {
  return <div>Server-rendered content</div>
}
```

**Benefits:**
- Better performance (less JavaScript)
- SEO-friendly
- Direct database access
- Automatic code splitting

### Client Components

```typescript
'use client'

import { useState } from 'react'

export default function InteractiveComponent() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(count + 1)}>{count}</button>
}
```

**Use when you need:**
- React hooks (useState, useEffect, useContext)
- Browser APIs (localStorage, window)
- Event handlers (onClick, onChange)
- Third-party libraries requiring client context

### Composition Pattern

Keep client components small and compose them in server components:

```typescript
// app/page.tsx (Server Component)
import { InteractiveButton } from '@/components/interactive-button'

export default function Page() {
  return (
    <div>
      <h1>Server-rendered heading</h1>
      <InteractiveButton /> {/* Client component */}
    </div>
  )
}
```

---

## Validation Patterns

### Centralized Validation

All validation in `src/lib/actions/validation.ts`:

```typescript
'use server'

import { VALIDATION } from '@/lib/constants'

export function validateSearchQuery(query: string): string {
  if (!query || typeof query !== 'string') {
    throw new Error('Invalid search query')
  }

  const sanitized = query.trim().slice(0, VALIDATION.SEARCH_QUERY_MAX_LENGTH)
  if (sanitized.length === 0) {
    throw new Error('Search query cannot be empty')
  }

  return sanitized
}

export function validateUUID(id: string, fieldName: string): string {
  if (!id || !VALIDATION.UUID_REGEX.test(id)) {
    throw new Error(`Invalid ${fieldName} format`)
  }
  return id
}
```

### Usage in Actions

```typescript
import { validateSearchQuery, validateUUID } from './validation'

export async function getProductByIdAction(productId: string) {
  const sanitizedId = validateUUID(productId, 'product ID')
  // ...
}
```

---

## Constants & Configuration

All magic numbers and configuration values go in `src/lib/constants.ts`:

```typescript
export const VALIDATION = {
  SEARCH_QUERY_MAX_LENGTH: 100,
  UUID_REGEX: /^[0-9a-f]{8}-...-[0-9a-f]{12}$/i,
} as const

export const PAGINATION = {
  DEFAULT_SEARCH_LIMIT: 50,
  DEFAULT_PAGE_SIZE: 20,
  MAX_BATCH_SIZE: 1000,
} as const

export const DASHBOARD = {
  TOP_FAMILIES_LIMIT: 10,
  ACTIVE_USERS_LIMIT: 5,
} as const
```

**Usage:**
```typescript
import { PAGINATION } from '@/lib/constants'

.limit(PAGINATION.DEFAULT_SEARCH_LIMIT)  // ✅ Good
.limit(50)                               // ❌ Bad (magic number)
```

---

## Error Handling

### Standard Pattern

```typescript
export async function someAction(): Promise<ResultType> {
  try {
    const { data, error } = await supabaseServer.from('table').select('*')

    if (error) {
      // Log with context, no sensitive data
      console.error('Action name error:', {
        message: error.message,
        code: error.code
      })
      return defaultValue  // Empty array, null, or error object
    }

    return data || defaultValue
  } catch (error) {
    // Catch unexpected errors
    console.error('Action name exception:',
      error instanceof Error ? error.message : 'Unknown error'
    )
    return defaultValue
  }
}
```

### Return Patterns

| Scenario | Return Value |
|----------|--------------|
| List/Search failed | `[]` (empty array) |
| Get by ID failed | `null` |
| Stats failed | Object with zero values |
| Paginated list failed | Full result object with empty items |

---

## Naming Conventions

### Actions
```
[verb][Domain]Action
searchProductsAction
getCustomerByIdAction
listProjectsAction
getDashboardStatsAction
```

### Database Functions
```
schema.verb_noun_with_params
items.get_dashboard_stats
items.get_supplier_stats
search.search_products_with_filters
```

### Types
```
[Domain][Purpose]
ProductSearchResult    # For search/list results
ProductDetail          # For full detail view
CustomerListParams     # For list operation params
```

### Files
```
Domain files:     lowercase, singular (customers.ts, not customer.ts)
Type files:       lowercase, singular (product.ts)
Component files:  PascalCase (FilterPanel.tsx)
```

---

## shadcn/ui Component Patterns

### Adding Components

```bash
npx shadcn@latest add dialog
npx shadcn@latest add table
```

### Usage Pattern

```typescript
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export function MyComponent() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Title</CardTitle>
      </CardHeader>
      <CardContent>
        <Button variant="default">Click me</Button>
      </CardContent>
    </Card>
  )
}
```

### FossSpinner (Custom Branded Spinner)

```typescript
import { Spinner } from '@/components/ui/spinner'

// Standard usage
<Spinner size="lg" />                        // sm=20, md=32, lg=48, xl=64

// Dark backgrounds
<Spinner size="lg" variant="dark" />         // White F for dark backgrounds

// Standard placement
<div className="flex items-center justify-center flex-1">
  <Spinner size="lg" />
</div>
```

**Design Guidelines:**
- Always center spinners in main content area, not sidebars
- Use `variant="dark"` on dark backgrounds (e.g., `bg-black`)
- Use `variant="auto"` (default) for responsive dark mode

---

## Type Definitions

### Location

```
src/types/
├── product.ts    # ProductInfo, ProductSearchResult, Feature
├── search.ts     # SearchFilters, FilterDefinition, Facets
├── customer.ts   # CustomerDetail, CustomerSearchResult
└── index.ts      # Re-exports (optional)
```

### Pattern

```typescript
// src/types/domain.ts

/**
 * Lightweight type for list/search results
 */
export interface DomainSearchResult {
  id: string
  name: string
}

/**
 * Full type for detail views
 */
export interface DomainDetail extends DomainSearchResult {
  description: string
  created_at: string
}

/**
 * Params for list operations
 */
export interface DomainListParams {
  page?: number
  pageSize?: number
  sortBy?: 'name' | 'created_at'
  sortOrder?: 'asc' | 'desc'
}
```

---

## Database Query Patterns

### PostgreSQL Functions (RPC)

Use PostgreSQL functions when:
1. **Aggregation needed** - COUNT, SUM, GROUP BY operations
2. **Multiple related queries** - Batch into single call
3. **Complex joins** - Let PostgreSQL optimize
4. **Performance critical** - Avoid transferring large datasets

```typescript
const { data, error } = await supabaseServer
  .schema('schema_name')
  .rpc('function_name', {
    p_param1: value,
    p_limit: 10
  })

if (error) {
  console.error('RPC error:', error)
  return defaultValue
}

return (data || []).map((item: DBResponseType) => ({
  field1: item.column1,
  field2: Number(item.column2)  // bigint → number
}))
```

### Schema Organization

```
items.*        → Product/catalog functions
analytics.*    → User tracking, metrics
search.*       → Search/filter functions
customers.*    → Customer functions
projects.*     → Project functions
```

---

## Security Checklist

**Always:**
- ✅ Validate all inputs (regex, trim, length)
- ✅ Use parameterized queries (Supabase client)
- ✅ Limit result sets (`.limit(50)`)
- ✅ Sanitize user input before database queries
- ✅ Return generic error messages (don't expose internals)
- ✅ Use `supabaseServer` for server-side operations
- ✅ Use `supabase` for client-side operations

**Never:**
- ❌ Trust user input directly
- ❌ Concatenate SQL strings manually
- ❌ Return raw database errors to client
- ❌ Expose service role key to client
- ❌ Skip input validation
- ❌ Mix up supabase clients

---

## Quick Reference

### Adding New Features Checklist

1. **Types first**: Define interfaces in `src/types/[domain].ts`
2. **Database functions**: If aggregation needed, create migration
3. **Validation**: Add validators to `src/lib/actions/validation.ts`
4. **Action file**: Create `src/lib/actions/[domain].ts`
5. **Export**: Add to `src/lib/actions/index.ts`
6. **Constants**: Add any magic numbers to `src/lib/constants.ts`
7. **Tests**: Manual testing via dev server

### Common Patterns

**Loading States:**
```typescript
const [isLoading, setIsLoading] = useState(false)

const handleAction = async () => {
  setIsLoading(true)
  try {
    await fetchData()
  } finally {
    setIsLoading(false)
  }
}

if (isLoading) return <Spinner />
```

**Data Fetching:**
```typescript
'use client'

import { useState } from 'react'
import { searchProductsAction } from '@/lib/actions'

export function ProductSearch() {
  const [results, setResults] = useState([])

  const handleSearch = async (query: string) => {
    try {
      const data = await searchProductsAction(query)
      setResults(data)
    } catch (error) {
      console.error(error)
    }
  }

  return <Results data={results} />
}
```

---

## JSDoc Documentation (MANDATORY)

**All new code MUST include JSDoc documentation.** This improves IDE experience and AI agent comprehension.

### What Requires JSDoc

| Element | Required | Optional |
|---------|----------|----------|
| Exported functions | ✅ Always | - |
| Hooks | ✅ Always | - |
| Interfaces/Types | ✅ Always | - |
| Complex internal functions | ✅ When non-obvious | - |
| File-level module docs | ✅ For complex files | Simple files |
| Trivial getters/setters | - | ❌ Skip |

### Standard Patterns

**Functions/Hooks:**
```typescript
/**
 * Fetches products with ETIM classification and symbol assignments.
 *
 * @remarks
 * Products are joined with `etim.ec_class` to get the symbol letter.
 * Symbol numbers (A1, A2) are assigned per-area based on insertion order.
 *
 * @param areaRevisionId - The active area revision UUID
 * @returns Products grouped by type, or empty arrays on error
 *
 * @see {@link docs/features/symbol-classification.md}
 */
export async function getCaseStudyProductsAction(areaRevisionId: string) {
```

**Interfaces:**
```typescript
/**
 * A product placement on the floor plan.
 * Coordinates are stored in DWG model space (mm) for LISP export.
 */
export interface Placement {
  /** Unique placement identifier */
  id: string
  /** DWG X coordinate in model units (typically mm) */
  worldX: number
  /** DWG Y coordinate in model units (typically mm) */
  worldY: number
}
```

**File-level (for complex modules):**
```typescript
/**
 * useCoordinateTransform Hook
 *
 * Handles coordinate transformation between APS Viewer page coordinates
 * and DWG model space coordinates. Essential for marker placement and
 * LISP script export.
 *
 * @see {@link https://aps.autodesk.com/blog/parsing-line-points-viewer}
 */
```

### Key Principles

1. **"Why" not "what"** - Code shows what, docs explain why
2. **Domain terms** - Define FOSSAPP-specific terms (ETIM, symbols, tiles, placements)
3. **Cross-references** - Link related files with `@see`
4. **External APIs** - Reference Supabase, APS, ETIM docs
5. **Skip the obvious** - Don't document trivial code

### Good Examples

See `src/components/case-study-viewer/hooks/` for well-documented hook examples.

### Enhancement Prompt

For systematic JSDoc enhancement passes, use: `.claude/prompts/jsdoc-enhancement.md`

---

## See Also

- Full architecture docs: [docs/architecture/](../../docs/architecture/)
- API patterns: [docs/architecture/api-patterns.md](../../docs/architecture/api-patterns.md)
- Component guide: [docs/architecture/components.md](../../docs/architecture/components.md)
- JSDoc enhancement prompt: [.claude/prompts/jsdoc-enhancement.md](../../prompts/jsdoc-enhancement.md)
