---
name: brokle-frontend-dev
description: Use this skill when developing Next.js/React frontend code for Brokle. Includes components, pages, hooks, API clients, stores, or any frontend features.
---

# Brokle Frontend Development

## Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| Next.js | 15.5.2 | App Router, Turbopack |
| React | 19.2.0 | UI library |
| TypeScript | 5.9.3 | Strict mode |
| Tailwind CSS | 4.1.15 | Styling |
| shadcn/ui | - | Component primitives |
| Zustand | - | Client state |
| React Query | - | Server state |
| React Hook Form | - | Forms + Zod validation |
| Vitest | - | Testing |
| pnpm | - | Package manager |

## Critical Import Rules

**Always import from feature index, never internal paths:**

```typescript
// CORRECT
import { useAuth, SignInForm } from '@/features/authentication'
import { useOrganization } from '@/features/organizations'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'
import { apiClient } from '@/lib/api/core/client'

// FORBIDDEN - internal paths
import { useAuth } from '@/features/authentication/hooks/use-auth'
import { AuthStore } from '@/features/authentication/stores/auth-store'
```

## Feature-Based Architecture

```
web/src/
├── app/                      # Next.js App Router (routing only)
│   ├── (auth)/              # Auth route group
│   └── (dashboard)/         # Dashboard routes
├── features/                # Domain features (self-contained)
│   ├── authentication/
│   ├── organizations/
│   ├── projects/
│   └── [feature]/
│       ├── components/      # Feature UI
│       ├── hooks/           # React hooks
│       ├── api/             # API functions
│       ├── stores/          # Zustand (optional)
│       ├── types/           # TypeScript types
│       └── index.ts         # Public API exports
├── components/
│   ├── ui/                 # shadcn/ui primitives
│   ├── shared/             # Cross-feature components
│   └── layout/             # App shell
├── lib/api/core/           # BrokleAPIClient
└── hooks/                  # Global hooks
```

**Rule**: Routes are thin - delegate to feature components:

```typescript
// app/(dashboard)/projects/page.tsx
import { ProjectsList } from '@/features/projects'
export default function ProjectsPage() {
  return <ProjectsList />
}
```

## State Management

| State Type | Tool | Location |
|------------|------|----------|
| Server data | React Query | Feature hooks |
| Client state | Zustand | Feature stores |
| Form state | React Hook Form + Zod | Component |
| URL state | useSearchParams() | Component |

### Server State Pattern

```typescript
// features/[feature]/hooks/use-data.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { getData, updateData } from '../api/data-api'

export function useData(id: string) {
  const queryClient = useQueryClient()

  const query = useQuery({
    queryKey: ['data', id],
    queryFn: () => getData(id),
  })

  const mutation = useMutation({
    mutationFn: updateData,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['data', id] }),
  })

  return { ...query, update: mutation.mutate }
}
```

### Client State Pattern

```typescript
// features/[feature]/stores/feature-store.ts
import { create } from 'zustand'

interface FeatureState {
  selectedId: string | null
  setSelectedId: (id: string | null) => void
}

export const useFeatureStore = create<FeatureState>((set) => ({
  selectedId: null,
  setSelectedId: (id) => set({ selectedId: id }),
}))
```

## Component Patterns

### Server Components (Default)

No directive needed. Use for static content and SEO:

```typescript
export default async function Page({ params }: { params: { id: string } }) {
  const data = await fetchData(params.id)
  return <div>{data.title}</div>
}
```

### Client Components

Add `'use client'` when needed:

```typescript
'use client'
import { useState } from 'react'

export function Interactive() {
  const [count, setCount] = useState(0)
  return <Button onClick={() => setCount(c => c + 1)}>{count}</Button>
}
```

**Use 'use client' when:**
- Event handlers (onClick, onChange)
- React hooks (useState, useEffect)
- Browser APIs (localStorage, window)

## API Client Pattern

```typescript
// features/[feature]/api/feature-api.ts
import { apiClient } from '@/lib/api/core/client'
import type { FeatureResponse, CreateFeatureRequest } from '../types'

export async function getFeature(id: string): Promise<FeatureResponse> {
  const response = await apiClient.get<FeatureResponse>(`/feature/${id}`)
  return response.data
}

export async function createFeature(data: CreateFeatureRequest): Promise<FeatureResponse> {
  const response = await apiClient.post<FeatureResponse>('/feature', data)
  return response.data
}
```

## Form Pattern

```typescript
'use client'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const schema = z.object({
  email: z.string().email(),
  name: z.string().min(2),
})

type FormData = z.infer<typeof schema>

export function MyForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  })

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Input {...register('email')} />
      {errors.email && <p className="text-destructive">{errors.email.message}</p>}
    </form>
  )
}
```

## Feature Index Pattern

```typescript
// features/[feature]/index.ts

// Hooks
export { useFeature } from './hooks/use-feature'

// Components
export { FeatureComponent } from './components/feature-component'

// Types (selective)
export type { FeatureData, FeatureConfig } from './types'

// DO NOT export stores directly - use hooks
```

## Testing

```typescript
// features/[feature]/__tests__/component.test.tsx
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { Component } from '../components/component'

describe('Component', () => {
  it('renders', () => {
    render(<Component />)
    expect(screen.getByText('Expected')).toBeInTheDocument()
  })
})
```

## Development Commands

```bash
cd web

pnpm dev          # Dev server (Turbopack)
pnpm build        # Production build
pnpm lint         # Next.js linter
pnpm format       # Prettier
pnpm test         # Vitest
pnpm test:watch   # Watch mode
```

## Supporting References

Load these files when you need detailed guidance:

| Need | Reference |
|------|-----------|
| Colors, typography, spacing, dark mode | [design-system.md](design-system.md) |
| UI components, state patterns, forms | [component-patterns.md](component-patterns.md) |
| Animations, transitions, micro-interactions | [animation-patterns.md](animation-patterns.md) |
| Complete feature example (authentication) | [feature-patterns.md](feature-patterns.md) |
| Decision trees, cheat sheets | [quick-reference.md](quick-reference.md) |

## Quick Decision Tree

**Creating new functionality?**
- Feature-specific → `features/[feature]/`
- Shared across features → `components/shared/`
- UI primitive → `components/ui/`

**Adding state?**
- Server data → React Query hook
- Client state → Zustand store
- Form → React Hook Form
- URL → useSearchParams()

**Component type?**
- Needs interactivity/hooks → `'use client'`
- Static/SEO → Server Component (default)

## Best Practices

1. **Import from feature index** - Never from internal paths
2. **Keep routes thin** - Delegate to feature components
3. **Server Components default** - Add 'use client' only when needed
4. **Type everything** - No `any` types
5. **Error boundaries** - Add per feature and route
6. **Check existing components** - `components/shared/` before creating new
