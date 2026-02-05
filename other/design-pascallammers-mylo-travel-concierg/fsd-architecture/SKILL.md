---
name: fsd-architecture
description: Feature-Sliced Design architecture for frontend. Use when creating new features, slices, or understanding the FSD layer structure.
allowed-tools: Read, Edit, Write, Glob, Grep
---

# Feature-Sliced Design (FSD) Architecture

The frontend uses Feature-Sliced Design. This skill documentation helps you understand the architecture and correctly create new features.

## Layer Hierarchy (STRICT)

```
app/        → widgets, features, entities, shared
widgets/    → features, entities, shared
features/   → entities, shared
entities/   → shared
shared/     → (only external libs)
```

**Import direction: ONLY downward!**

## Project Structure

```
frontend/src/
├── app/                        # Next.js App Router (outside FSD)
│
├── widgets/                    # Composite UI Blocks
│   └── header/
│       ├── ui/
│       │   ├── header.tsx
│       │   └── mode-toggle.tsx
│       └── index.ts            # Public API
│
├── features/                   # User Interactions / Use Cases
│   ├── auth/
│   │   ├── ui/
│   │   │   ├── login-form.tsx
│   │   │   └── register-form.tsx
│   │   ├── model/
│   │   │   └── use-auth-sync.ts
│   │   └── index.ts
│   └── stats/
│       ├── ui/
│       │   └── stats-grid.tsx
│       ├── model/
│       │   └── use-sse.ts
│       └── index.ts
│
├── entities/                   # Business Objects
│   └── user/
│       ├── ui/
│       │   └── user-info.tsx
│       ├── model/
│       │   └── types.ts
│       └── index.ts
│
└── shared/                     # Reusable Code
    ├── ui/                     # shadcn/ui components
    ├── api/                    # Orval-generated
    │   ├── endpoints/
    │   ├── models/
    │   └── custom-fetch.ts
    ├── lib/
    │   ├── auth-client/        # Client-safe Auth
    │   ├── auth-server/        # Server-only Auth
    │   ├── query-client.ts
    │   └── utils.ts
    └── config/
        ├── providers.tsx
        └── theme-provider.tsx
```

## TypeScript Path Aliases

```tsx
// Always use layer aliases:
import { Button } from "@shared/ui/button"
import { useAuthSync } from "@features/auth"
import { SessionUser } from "@entities/user"
import { Header } from "@widgets/header"
```

## Slice Segments

Each slice can have these segments:

| Segment | Purpose | Example |
|---------|---------|---------|
| `ui/` | React Components | `login-form.tsx` |
| `model/` | Hooks, State, Types | `use-auth-sync.ts` |
| `api/` | API Calls (rare, mostly in shared) | `user-api.ts` |
| `lib/` | Utilities for the slice | `validation.ts` |

## Public API Pattern (IMPORTANT!)

**Every slice MUST have an `index.ts`:**

```tsx
// features/auth/index.ts
export { LoginForm } from "./ui/login-form"
export { RegisterForm } from "./ui/register-form"
export { useAuthSync, broadcastSignOut } from "./model/use-auth-sync"
```

**Always import via index.ts:**

```tsx
// ✅ Correct
import { LoginForm } from "@features/auth"

// ❌ Wrong (Public API Sidestep)
import { LoginForm } from "@features/auth/ui/login-form"
```

## Creating a New Feature

### 1. Create folder structure

```bash
mkdir -p src/features/<name>/ui
mkdir -p src/features/<name>/model  # if hooks/state needed
```

### 2. Create UI Component

```tsx
// src/features/<name>/ui/<name>-form.tsx
"use client"

import { Button } from "@shared/ui/button"
import { Card } from "@shared/ui/card"

export function NameForm() {
  return (
    <Card>
      <Button>Action</Button>
    </Card>
  )
}
```

### 3. Create Model/Hook (optional)

```tsx
// src/features/<name>/model/use-<name>.ts
"use client"

import { useQueryClient } from "@tanstack/react-query"
import { useCallback } from "react"

export function useName() {
  const queryClient = useQueryClient()
  // ...
  return { /* ... */ }
}
```

### 4. Create Public API

```tsx
// src/features/<name>/index.ts
export { NameForm } from "./ui/name-form"
export { useName } from "./model/use-name"
```

### 5. Use in App

```tsx
// app/(protected)/page.tsx
import { NameForm } from "@features/<name>"

export default function Page() {
  return <NameForm />
}
```

## Creating a New Entity

```tsx
// src/entities/<name>/model/types.ts
export interface Product {
  id: string
  name: string
  price: number
}

// src/entities/<name>/ui/product-card.tsx
"use client"

import type { Product } from "../model/types"
import { Card } from "@shared/ui/card"

export function ProductCard({ product }: { product: Product }) {
  return <Card>{product.name}</Card>
}

// src/entities/<name>/index.ts
export type { Product } from "./model/types"
export { ProductCard } from "./ui/product-card"
```

## Import Rules

```tsx
// ✅ ALLOWED
// In app/:
import { Header } from "@widgets/header"
import { LoginForm } from "@features/auth"
import { SessionUser } from "@entities/user"
import { Button } from "@shared/ui/button"

// In widgets/:
import { useAuthSync } from "@features/auth"
import { SessionUser } from "@entities/user"
import { Button } from "@shared/ui/button"

// In features/:
import { SessionUser } from "@entities/user"
import { Button } from "@shared/ui/button"

// In entities/:
import { Button } from "@shared/ui/button"

// ❌ FORBIDDEN
// In shared/ NEVER import features/!
// In entities/ NEVER import features/!
// In features/ NEVER import other features/!
```

## Steiger Linting

FSD rules are automatically checked:

```bash
# Integrated in lint
bun run lint

# Only Steiger
bunx steiger src
```

### Common Steiger Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `no-public-api-sidestep` | Direct import instead of via index.ts | Import via index.ts |
| `insignificant-slice` | Slice has only 1 reference | Use more or move to widget/higher layer |
| `forbidden-imports` | Import from higher layer | Fix import direction |

## Server vs Client Components

```tsx
// Server Component (no "use client")
// → Can only import shared/, no hooks

// Client Component
"use client"
// → Can use hooks, but NEVER server-only code
```

### Auth Separation

```tsx
// In Client Components:
import { signIn, signOut } from "@shared/lib/auth-client"

// In Server Components:
import { getSession } from "@shared/lib/auth-server"
```

## Summary

1. **Respect layers**: Only import downward
2. **Public API**: Always export/import via index.ts
3. **Segments**: ui/, model/, api/, lib/ as needed
4. **Aliases**: @shared/, @entities/, @features/, @widgets/
5. **Linting**: `bun run lint` checks FSD rules
