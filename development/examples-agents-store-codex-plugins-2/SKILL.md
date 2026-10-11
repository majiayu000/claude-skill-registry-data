---
name: examples
description: Next.js development scenario walkthroughs and code patterns. This skill should be used when the user asks for "Next.js examples", "Next.js project walkthrough", "how to build a dashboard in Next.js", "Next.js e-commerce example", "Next.js code patterns", or needs end-to-end implementation guidance for common Next.js application types.
---

# Next.js Examples & Scenario Walkthroughs

Quick reference for common Next.js development patterns with links to detailed scenario walkthroughs.

## Available Scenarios

| Scenario | Type | Key Patterns | File |
|----------|------|-------------|------|
| Dashboard App | Authenticated SaaS | Layouts, auth proxy, streaming, Server Actions | [dashboard-app.md](references/scenarios/dashboard-app.md) |
| E-Commerce Storefront | Public catalog | ISR, search params, client state, image optimization | [ecommerce-storefront.md](references/scenarios/ecommerce-storefront.md) |

## Quick Reference Patterns

### Pattern 1: Authenticated Layout with Sidebar

```
app/
├── layout.tsx              # Public layout (minimal)
├── page.tsx                # Landing page
├── login/page.tsx          # Login form
├── (dashboard)/
│   ├── layout.tsx          # Auth check + sidebar + nav
│   ├── page.tsx            # Dashboard home
│   ├── settings/page.tsx   # User settings
│   └── analytics/page.tsx  # Analytics page
└── proxy.ts                # Redirect unauthenticated to /login
```

### Pattern 2: CRUD with Server Actions

```tsx
// 1. Define actions
'use server'
export async function createItem(formData: FormData) { /* ... */ revalidatePath('/items') }
export async function updateItem(id: string, formData: FormData) { /* ... */ revalidatePath('/items') }
export async function deleteItem(id: string) { /* ... */ revalidatePath('/items') }

// 2. List page (Server Component)
export default async function ItemsPage() {
  const items = await getItems()
  return <ItemList items={items} />
}

// 3. Form (Client Component with useActionState)
'use client'
export function CreateItemForm() {
  const [state, action, pending] = useActionState(createItem, null)
  return <form action={action}>...</form>
}
```

### Pattern 3: Search with URL State

```tsx
// app/search/page.tsx — Server Component
export default async function SearchPage({
  searchParams,
}: {
  searchParams: Promise<{ q?: string; page?: string }>
}) {
  const { q, page } = await searchParams
  const results = await search(q, Number(page) || 1)
  return (
    <div>
      <SearchInput defaultValue={q} />
      <SearchResults results={results} />
      <Pagination currentPage={Number(page) || 1} />
    </div>
  )
}

// app/search/search-input.tsx — Client Component
'use client'
import { useRouter, useSearchParams } from 'next/navigation'

export function SearchInput({ defaultValue }: { defaultValue?: string }) {
  const router = useRouter()
  const searchParams = useSearchParams()

  function handleSearch(term: string) {
    const params = new URLSearchParams(searchParams.toString())
    if (term) params.set('q', term)
    else params.delete('q')
    params.delete('page')
    router.push(`/search?${params.toString()}`)
  }

  return <input defaultValue={defaultValue} onChange={(e) => handleSearch(e.target.value)} />
}
```

### Pattern 4: Data Table with Streaming

```tsx
import { Suspense } from 'react'

export default function OrdersPage() {
  return (
    <div>
      <h1>Orders</h1>
      <Suspense fallback={<TableSkeleton />}>
        <OrdersTable />
      </Suspense>
    </div>
  )
}

async function OrdersTable() {
  const orders = await getOrders()  // Slow query — streams in
  return (
    <table>
      <thead><tr><th>ID</th><th>Customer</th><th>Total</th><th>Status</th></tr></thead>
      <tbody>
        {orders.map(order => (
          <tr key={order.id}>
            <td>{order.id}</td>
            <td>{order.customer}</td>
            <td>${order.total}</td>
            <td>{order.status}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
```

### Pattern 5: API Route with Validation

```ts
// app/api/posts/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { z } from 'zod'

const createPostSchema = z.object({
  title: z.string().min(1).max(200),
  content: z.string().min(1),
  published: z.boolean().default(false),
})

export async function POST(request: NextRequest) {
  const body = await request.json()
  const result = createPostSchema.safeParse(body)

  if (!result.success) {
    return NextResponse.json({ errors: result.error.flatten() }, { status: 400 })
  }

  const post = await db.post.create({ data: result.data })
  return NextResponse.json(post, { status: 201 })
}
```

## Conventions

- All examples use TypeScript and the App Router
- Server Components are the default — `'use client'` is only added when needed
- Data fetching happens in Server Components, not Client Components
- Server Actions handle mutations, not API routes (unless building a public API)
- All examples follow the file structure conventions from the `app-router-patterns` skill