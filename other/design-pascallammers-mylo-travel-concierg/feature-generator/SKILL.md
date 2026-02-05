---
name: feature-generator
description: Generate full-stack features with Goca backend and React frontend. Use when creating new features, adding CRUD operations, or scaffolding new pages.
allowed-tools: Read, Edit, Write, Bash, Glob, Grep
---

# Feature Generator

Create complete full-stack features following Clean Architecture with Goca.

## Feature Structure

### Backend (Go with Goca)

1. **Entity** in `backend/internal/domain/` → `goca make entity`
2. **Repository** in `backend/internal/repository/` → `goca make repository`
3. **UseCase** in `backend/internal/usecase/` → `goca make usecase`
4. **Handler** in `backend/internal/handler/` → `goca make handler`

### Frontend (React)

1. **Server Component** for initial loading (no flicker)
2. **Client Component** for interactivity
3. **Generated API hooks** via Orval
4. **UI components** with shadcn/ui

## Quick Start: New Feature with Goca

```bash
cd backend

# Komplettes Feature generieren
goca feature Product --fields "name:string,price:float64,stock:int"

# Or individual layers
goca make entity Product
goca make repository Product
goca make usecase Product
goca make handler Product

# Generate API Client
cd ..
make api
```

## Entity Registry (AutoMigrate)

After `goca feature`, the new entity must be registered in `backend/internal/domain/registry.go`:

```go
// internal/domain/registry.go
func AllEntities() []interface{} {
    return []interface{}{
        &UserStats{},
        &Product{},  // ← Add new entity here!
    }
}
```

This is the **ONLY** place where new entities need to be registered!

## Complete Workflow

```bash
# 1. Generate feature
cd backend
goca feature Product --fields "name:string,price:float64,stock:int"

# 2. Add entity to registry
# backend/internal/domain/registry.go → add &Product{}

# 3. Generate API
cd ..
make api

# 4. Restart backend (migration runs automatically)
make dev-backend
```

## Server-Side Data Loading Pattern (HydrationBoundary)

### Step 1: Server Component with prefetchQuery

```tsx
// app/(protected)/products/page.tsx (Server Component)
import { dehydrate, HydrationBoundary } from "@tanstack/react-query"
import { cookies } from "next/headers"
import { redirect } from "next/navigation"
import { getGetProductsQueryKey, getProducts } from "@/api/endpoints/products/products"
import { getQueryClient } from "@/lib/get-query-client"
import { getSession } from "@/lib/auth-server"
import { ProductList } from "./product-list"

export default async function ProductsPage() {
  // 1. Check session
  const session = await getSession()
  if (!session) redirect("/login")

  // 2. Cookies for auth
  const cookieStore = await cookies()
  const cookieHeader = cookieStore.getAll().map((c) => `${c.name}=${c.value}`).join("; ")

  // 3. Prefetch with Orval function
  const queryClient = getQueryClient()
  await queryClient.prefetchQuery({
    queryKey: getGetProductsQueryKey(),
    queryFn: () => getProducts({ headers: { Cookie: cookieHeader }, cache: "no-store" }),
  })

  // 4. Wrap with HydrationBoundary
  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <div className="container py-8">
        <h1 className="text-2xl font-bold mb-4">Products</h1>
        <ProductList />
      </div>
    </HydrationBoundary>
  )
}
```

### Step 2: Client Component (no initialData needed!)

```tsx
// app/(protected)/products/product-list.tsx
"use client"

import { useGetProducts } from "@/api/endpoints/products/products"
import { useSSE } from "@/hooks/use-sse"

export function ProductList() {
  useSSE() // Real-time Updates

  // Data is already hydrated - no initialData needed!
  const { data: productsResponse } = useGetProducts()

  const products = productsResponse?.status === 200 ? productsResponse.data : null

  return (
    <div className="grid gap-4">
      {products?.map(product => (
        <div key={product.id}>{product.name} - {product.price}€</div>
      ))}
    </div>
  )
}
```

## Backend Handler mit Swagger

```go
// internal/handler/product.go

// GetProducts godoc
// @Summary List all products
// @Description Get all products for the authenticated user
// @Tags products
// @Accept json
// @Produce json
// @Success 200 {array} ProductResponse
// @Failure 401 {object} ErrorResponse
// @Security BearerAuth
// @Router /products [get]
func (h *ProductHandler) GetProducts(w http.ResponseWriter, r *http.Request) {
    // Implementation
}
```

## After Backend Changes

```bash
# Always run after handler changes:
make api
```

## Conventions

### File Naming

- Go: `snake_case.go`
- React Pages: `page.tsx` in route folder
- Client Components: `kebab-case.tsx`

### Route Protection

- Public: `frontend/src/app/`
- Protected: `frontend/src/app/(protected)/`
- Auth: `frontend/src/app/(auth)/`

### No Skeleton/Flicker

- Server Component loads data before rendering
- Client Component receives `initialData`
- React Query takes over for updates
- SSE for real-time sync
