---
name: nextjs-development
description: Next.js 14+ development with App Router, React Server Components, Server Actions, client components, streaming SSR, metadata API, parallel routes, intercepting routes, TypeScript best practices, TanStack Query for data fetching, Zustand state management, shadcn/ui components, Tailwind CSS styling, authentication patterns, API routes, middleware, error handling, performance optimization, SEO, and production deployment strategies.
---

# Next.js Development Skill

## Purpose

Build modern, high-performance web applications with Next.js 14+ using App Router, React Server Components, and cutting-edge patterns.

## When to Use This Skill

Auto-activates when working with:
- Next.js application development
- App Router (app directory)
- React Server Components (RSC)
- Server Actions
- Client Components
- API Routes
- Middleware
- Authentication
- Performance optimization

## Core Concepts

### 1. App Router Architecture
```
app/
├── layout.tsx              # Root layout (Server Component)
├── page.tsx                # Home page (Server Component)
├── loading.tsx             # Loading UI
├── error.tsx               # Error boundary
├── not-found.tsx           # 404 page
├── (auth)/                 # Route group (doesn't affect URL)
│   ├── login/
│   └── register/
├── dashboard/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── @analytics/         # Parallel route
│   └── @team/              # Parallel route
└── api/                    # API routes
    └── users/
        └── route.ts
```

### 2. Server vs Client Components
- **Server Components**: Default, data fetching, no JS sent to client
- **Client Components**: 'use client', interactivity, hooks, browser APIs

## Quick Start Examples

### Server Component with Data Fetching

```typescript
// app/users/page.tsx (Server Component)
import { Suspense } from 'react'

interface User {
  id: string
  name: string
  email: string
}

async function getUsers(): Promise<User[]> {
  // Fetch directly in Server Component
  const res = await fetch('https://api.example.com/users', {
    next: { revalidate: 60 } // ISR: revalidate every 60 seconds
  })

  if (!res.ok) throw new Error('Failed to fetch users')
  return res.json()
}

export default async function UsersPage() {
  const users = await getUsers()

  return (
    <div>
      <h1>Users</h1>
      <Suspense fallback={<UserListSkeleton />}>
        <UserList users={users} />
      </Suspense>
    </div>
  )
}

// Streaming with Suspense
function UserList({ users }: { users: User[] }) {
  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}
```

### Client Component with Interactivity

```typescript
// components/user-form.tsx
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

export function UserForm() {
  const [name, setName] = useState('')
  const [loading, setLoading] = useState(false)
  const router = useRouter()

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)

    try {
      const res = await fetch('/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name })
      })

      if (res.ok) {
        router.push('/users')
        router.refresh() // Revalidate server components
      }
    } catch (error) {
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        disabled={loading}
      />
      <button type="submit" disabled={loading}>
        {loading ? 'Creating...' : 'Create User'}
      </button>
    </form>
  )
}
```

### Server Actions (Form Mutations)

```typescript
// app/actions.ts
'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'
import { z } from 'zod'

const createUserSchema = z.object({
  name: z.string().min(2),
  email: z.string().email()
})

export async function createUser(formData: FormData) {
  // Validate input
  const validatedFields = createUserSchema.safeParse({
    name: formData.get('name'),
    email: formData.get('email')
  })

  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
    }
  }

  const { name, email } = validatedFields.data

  try {
    // Database mutation
    await db.user.create({
      data: { name, email }
    })
  } catch (error) {
    return {
      message: 'Failed to create user'
    }
  }

  // Revalidate cache
  revalidatePath('/users')

  // Redirect
  redirect('/users')
}

// app/users/new/page.tsx
import { createUser } from '@/app/actions'

export default function NewUserPage() {
  return (
    <form action={createUser}>
      <input name="name" type="text" required />
      <input name="email" type="email" required />
      <button type="submit">Create</button>
    </form>
  )
}
```

### API Route Handlers

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { z } from 'zod'

const userSchema = z.object({
  name: z.string().min(2),
  email: z.string().email()
})

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const page = parseInt(searchParams.get('page') || '1')
  const limit = parseInt(searchParams.get('limit') || '10')

  const users = await db.user.findMany({
    skip: (page - 1) * limit,
    take: limit
  })

  return NextResponse.json({ users, page, limit })
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const validatedData = userSchema.parse(body)

    const user = await db.user.create({
      data: validatedData
    })

    return NextResponse.json(user, { status: 201 })
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Validation failed', details: error.errors },
        { status: 400 }
      )
    }

    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}
```

### Middleware (Authentication)

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { getToken } from 'next-auth/jwt'

export async function middleware(request: NextRequest) {
  const token = await getToken({ req: request })

  // Protected routes
  if (request.nextUrl.pathname.startsWith('/dashboard')) {
    if (!token) {
      return NextResponse.redirect(new URL('/login', request.url))
    }
  }

  // Admin-only routes
  if (request.nextUrl.pathname.startsWith('/admin')) {
    if (!token || token.role !== 'admin') {
      return NextResponse.redirect(new URL('/', request.url))
    }
  }

  // Add custom headers
  const response = NextResponse.next()
  response.headers.set('x-user-id', token?.sub || '')

  return response
}

export const config = {
  matcher: ['/dashboard/:path*', '/admin/:path*']
}
```

### Data Fetching with TanStack Query (Client)

```typescript
// hooks/use-users.ts
'use client'

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

interface User {
  id: string
  name: string
  email: string
}

export function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: async () => {
      const res = await fetch('/api/users')
      if (!res.ok) throw new Error('Failed to fetch users')
      return res.json() as Promise<User[]>
    },
    staleTime: 60000, // 1 minute
  })
}

export function useCreateUser() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (user: Omit<User, 'id'>) => {
      const res = await fetch('/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(user),
      })
      if (!res.ok) throw new Error('Failed to create user')
      return res.json()
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] })
    },
  })
}
```

### Parallel Routes & Layouts

```typescript
// app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
  analytics,
  team
}: {
  children: React.ReactNode
  analytics: React.ReactNode
  team: React.ReactNode
}) {
  return (
    <div className="grid grid-cols-3 gap-4">
      <div className="col-span-2">{children}</div>
      <div>
        <div className="mb-4">{analytics}</div>
        <div>{team}</div>
      </div>
    </div>
  )
}
```

### Error Handling

```typescript
// app/error.tsx
'use client'

import { useEffect } from 'react'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    console.error(error)
  }, [error])

  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  )
}

// app/not-found.tsx
export default function NotFound() {
  return (
    <div>
      <h2>Not Found</h2>
      <p>Could not find requested resource</p>
    </div>
  )
}
```

## Resource Files

### [resources/server-components.md](resources/server-components.md)
- RSC patterns
- Data fetching strategies
- Streaming and Suspense
- Server vs Client tradeoffs

### [resources/server-actions.md](resources/server-actions.md)
- Form mutations
- Optimistic updates
- Validation patterns
- Error handling

### [resources/authentication.md](resources/authentication.md)
- NextAuth.js setup
- Protected routes
- Session management
- OAuth integration

### [resources/performance-optimization.md](resources/performance-optimization.md)
- Image optimization
- Font optimization
- Code splitting
- Caching strategies

### [resources/seo-metadata.md](resources/seo-metadata.md)
- Metadata API
- OpenGraph tags
- Dynamic metadata
- Sitemap generation

## Best Practices

- Use Server Components by default
- Fetch data as close to where it's needed
- Use Server Actions for mutations
- Implement proper error boundaries
- Optimize images with next/image
- Use dynamic imports for code splitting
- Implement proper TypeScript types
- Use middleware for auth/routing
- Cache API responses appropriately
- Monitor Core Web Vitals
- Use streaming for better UX
- Implement proper SEO metadata

## Common Patterns

### Loading States
```typescript
// app/users/loading.tsx
export default function Loading() {
  return <UserListSkeleton />
}
```

### Revalidation
```typescript
// Revalidate on-demand
revalidatePath('/users')
revalidateTag('users')

// Time-based revalidation
fetch('...', { next: { revalidate: 60 } })

// No caching
fetch('...', { cache: 'no-store' })
```

---

**Status**: Production-Ready
**Last Updated**: 2025-11-04
**Next.js Version**: 14+
