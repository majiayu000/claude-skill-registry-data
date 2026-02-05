---
name: nextjs-16-async-apis
description: Guide for Next.js 16 fully async APIs. Covers cookies(), headers(), params, and searchParams patterns that must be awaited. Use when accessing server context in Server Components, Route Handlers, or Proxy functions. Essential for Next.js 16 compliance.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Next.js 16: Fully Async APIs

## Overview

In Next.js 16, all dynamic APIs that rely on runtime information are now **fully asynchronous**. This is a breaking change from previous versions where synchronous access was temporarily allowed. The following APIs must now be accessed asynchronously:

- `cookies()` function
- `headers()` function
- `params` in layout.js, page.js, route.js
- `searchParams` in page.js (using React's `use` hook)

## When to Use This Skill

Use this skill when:
- Accessing cookies or headers in Server Components
- Handling request parameters in Next.js 16
- Working with dynamic route parameters
- Implementing authentication or request processing
- Building Route Handlers that access request context

## Next.js 16 Async Patterns

### Accessing Cookies Async

```typescript
// ❌ BEFORE (Next.js 14 and earlier)
import { cookies } from 'next/headers'

const cookieStore = cookies()
const token = cookieStore.get('auth-token')

// ❌ BEFORE (Next.js 15 - temporary sync access)
import { cookies } from 'next/headers'

const cookieStore = cookies() // Returns Promise in Next.js 15
const token = cookieStore.get('auth-token') // Still worked with temp sync access

// ✅ AFTER (Next.js 16 - fully async)
import { cookies } from 'next/headers'

const cookieStore = await cookies() // Now requires await
const token = cookieStore.get('auth-token')
```

### Accessing Headers Async

```typescript
// ❌ BEFORE (Next.js 14 and earlier)
import { headers } from 'next/headers'

const headersList = headers()
const userAgent = headersList.get('user-agent')

// ❌ BEFORE (Next.js 15 - temporary sync access)
import { headers } from 'next/headers'

const headersList = headers() // Returns Promise in Next.js 15
const userAgent = headersList.get('user-agent')

// ✅ AFTER (Next.js 16 - fully async)
import { headers } from 'next/headers'

const headersList = await headers() // Now requires await
const userAgent = headersList.get('user-agent')
```

## Route Handlers with Async APIs

```typescript
// app/api/users/route.ts
import { cookies, headers } from 'next/headers'

export async function GET(request: Request, { params }: { params: Promise<{ id: string }> }) {
  // ✅ Next.js 16: params must be awaited
  const { id } = await params
  
  // ✅ Next.js 16: cookies must be awaited
  const cookieStore = await cookies()
  const authCookie = cookieStore.get('auth-token')
  
  // ✅ Next.js 16: headers must be awaited
  const headersList = await headers()
  const userAgent = headersList.get('user-agent')
  
  return Response.json({ 
    userId: id, 
    userAgent,
    auth: !!authCookie 
  })
}
```

## Page Components with Async Params and SearchParams

```typescript
// app/[slug]/page.tsx
import { use } from 'react'

export default function Page(props: {
  params: Promise<{ slug: string }>
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>
}) {
  // ✅ Next.js 16: Use React's 'use' hook to unwrap promises
  const params = use(props.params)
  const searchParams = use(props.searchParams)
  
  const slug = params.slug
  const query = searchParams.query
  
  return (
    <div>
      <h1>Page: {slug}</h1>
      {query && <p>Query: {query}</p>}
    </div>
  )
}
```

## Layout Components with Async Params

```typescript
// app/[category]/layout.tsx
import { use } from 'react'

export default function CategoryLayout(props: {
  params: Promise<{ category: string }>
  children: React.ReactNode
}) {
  // ✅ Next.js 16: Use React's 'use' hook to unwrap params
  const params = use(props.params)
  const category = params.category
  
  return (
    <div>
      <h2>Category: {category}</h2>
      {props.children}
    </div>
  )
}
```

## Authentication Pattern with Async Cookies

```typescript
// lib/auth.ts
import { cookies } from 'next/headers'
import { jwtVerify } from 'jose'

export async function getCurrentUser() {
  // ✅ Next.js 16: cookies must be awaited
  const cookieStore = await cookies()
  const token = cookieStore.get('auth-token')?.value
  
  if (!token) {
    return null
  }
  
  try {
    // Verify JWT token
    const verified = await jwtVerify(
      token, 
      new TextEncoder().encode(process.env.JWT_SECRET)
    )
    return verified.payload
  } catch (error) {
    return null
  }
}
```

## Server Action with Async Headers

```typescript
// app/actions.ts
'use server'

import { headers } from 'next/headers'
import { revalidatePath } from 'next/cache'

export async function logUserAction(action: string) {
  // ✅ Next.js 16: headers must be awaited in server actions
  const headersList = await headers()
  const userAgent = headersList.get('user-agent')
  const ip = headersList.get('x-forwarded-for') || 'unknown'
  
  // Log the action with user info
  console.log(`Action: ${action}, IP: ${ip}, User Agent: ${userAgent}`)
  
  // Revalidate relevant paths
  revalidatePath('/')
}
```

## Error Handling with Async APIs

```typescript
// app/[id]/page.tsx
import { use } from 'react'

export default function ProductPage(props: {
  params: Promise<{ id: string }>
}) {
  try {
    // ✅ Next.js 16: Use React's 'use' hook
    const params = use(props.params)
    const id = params.id
    
    // Fetch product data using the ID
    return <ProductDetail id={id} />
  } catch (error) {
    // Handle errors appropriately
    return <div>Error loading product</div>
  }
}
```

## Key Changes Summary

| API | Next.js 15 | Next.js 16 |
|-----|------------|------------|
| `cookies()` | Returns Promise, sync access temporarily allowed | Returns Promise, `await` required |
| `headers()` | Returns Promise, sync access temporarily allowed | Returns Promise, `await` required |
| `params` | Parameter is Promise, awaited in function | Parameter is Promise, unwrapped with `use` hook in components |
| `searchParams` | Parameter is Promise, awaited in function | Parameter is Promise, unwrapped with `use` hook in components |

## Migration Checklist

When migrating to Next.js 16:

- [ ] Update all cookie access: `cookies()` → `await cookies()`
- [ ] Update all header access: `headers()` → `await headers()`
- [ ] Update page components to use React's `use()` hook for params and searchParams
- [ ] Update layout components to use React's `use()` hook for params
- [ ] Update route handlers to await params
- [ ] Test authentication flows that use cookies
- [ ] Verify all server actions that access request context

These patterns are critical for Next.js 16 compliance and will prevent runtime errors related to asynchronous API access.