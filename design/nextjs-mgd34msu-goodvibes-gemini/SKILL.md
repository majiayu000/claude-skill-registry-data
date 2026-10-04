---
name: nextjs
description: Builds full-stack React applications with Next.js App Router, Server Components, Server Actions, and edge deployment. Use when creating Next.js projects, implementing routing, data fetching, caching, authentication, or deploying to Vercel.
---

# Next.js

Full-stack React framework with App Router, Server Components, Server Actions, and optimized deployment patterns.

## Quick Start

**Create new project:**
```bash
npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir
cd my-app && npm run dev
```

**Essential file structure:**
```
src/
  app/
    layout.tsx      # Root layout (required)
    page.tsx        # Home page
    globals.css     # Global styles
    api/            # Route handlers
  components/       # React components
  lib/              # Utilities
```

## App Router Fundamentals

### File Conventions

| File | Purpose |
|------|---------|
| `page.tsx` | Route UI |
| `layout.tsx` | Shared UI wrapper |
| `loading.tsx` | Loading UI (Suspense) |
| `error.tsx` | Error boundary |
| `not-found.tsx` | 404 UI |
| `route.ts` | API endpoint |

### Routing Patterns

```
app/
  page.tsx                    # /
  blog/
    page.tsx                  # /blog
    [slug]/
      page.tsx                # /blog/:slug
  (marketing)/                # Route group (no URL segment)
    about/page.tsx            # /about
  @modal/                     # Parallel route (slot)
    (.)photo/[id]/page.tsx    # Intercepting route
```

**Dynamic segments:**
```tsx
// app/blog/[slug]/page.tsx
export default async function Page({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  return <Article slug={slug} />
}
```

**Catch-all segments:**
```tsx
// app/docs/[...slug]/page.tsx - matches /docs/a, /docs/a/b, etc.
// app/docs/[[...slug]]/page.tsx - also matches /docs
```

### Layouts

```tsx
// app/layout.tsx - Root layout (required)
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
```

**Nested layout:**
```tsx
// app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="flex">
      <Sidebar />
      <main className="flex-1">{children}</main>
    </div>
  )
}
```

## Server Components

**Default behavior** - all components are Server Components unless marked with `'use client'`.

```tsx
// Server Component (default)
async function Posts() {
  const posts = await db.posts.findMany() // Direct DB access
  return (
    <ul>
      {posts.map(post => <li key={post.id}>{post.title}</li>)}
    </ul>
  )
}
```

**When to use Client Components:**
- Event handlers (onClick, onChange)
- State and lifecycle (useState, useEffect)
- Browser APIs
- Custom hooks with state

```tsx
'use client'

import { useState } from 'react'

export function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}
```

## Data Fetching

### Server Components (Recommended)

```tsx
// Direct fetch in Server Component
async function BlogPosts() {
  const res = await fetch('https://api.example.com/posts')
  const posts = await res.json()
  return <PostList posts={posts} />
}

// With ORM
async function Users() {
  const users = await prisma.user.findMany()
  return <UserList users={users} />
}
```

### Parallel Data Fetching

```tsx
export default async function Page() {
  // Start both requests simultaneously
  const postsPromise = getPosts()
  const usersPromise = getUsers()

  // Await both
  const [posts, users] = await Promise.all([postsPromise, usersPromise])

  return (
    <>
      <PostList posts={posts} />
      <UserList users={users} />
    </>
  )
}
```

### Streaming with Suspense

```tsx
import { Suspense } from 'react'

export default function Page() {
  return (
    <div>
      <h1>Dashboard</h1>
      <Suspense fallback={<Skeleton />}>
        <SlowComponent />
      </Suspense>
    </div>
  )
}
```

## Server Actions

### Basic Form

```tsx
// app/actions.ts
'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string
  const content = formData.get('content') as string

  await db.posts.create({ data: { title, content } })

  revalidatePath('/posts')
  redirect('/posts')
}
```

```tsx
// app/posts/new/page.tsx
import { createPost } from '@/app/actions'

export default function NewPostPage() {
  return (
    <form action={createPost}>
      <input name="title" required />
      <textarea name="content" required />
      <button type="submit">Create Post</button>
    </form>
  )
}
```

### With Validation

```tsx
'use server'

import { z } from 'zod'

const PostSchema = z.object({
  title: z.string().min(1).max(100),
  content: z.string().min(1),
})

export async function createPost(formData: FormData) {
  const validated = PostSchema.safeParse({
    title: formData.get('title'),
    content: formData.get('content'),
  })

  if (!validated.success) {
    return { error: validated.error.flatten().fieldErrors }
  }

  await db.posts.create({ data: validated.data })
  revalidatePath('/posts')
  redirect('/posts')
}
```

### With useActionState

```tsx
'use client'

import { useActionState } from 'react'
import { createPost } from '@/app/actions'

export function CreatePostForm() {
  const [state, action, pending] = useActionState(createPost, null)

  return (
    <form action={action}>
      <input name="title" />
      {state?.error?.title && <p>{state.error.title}</p>}
      <button disabled={pending}>
        {pending ? 'Creating...' : 'Create'}
      </button>
    </form>
  )
}
```

## Caching

### Data Cache

```tsx
// Cached by default (static)
const data = await fetch('https://api.example.com/data')

// Opt out of caching
const data = await fetch('https://api.example.com/data', {
  cache: 'no-store'
})

// Time-based revalidation
const data = await fetch('https://api.example.com/data', {
  next: { revalidate: 3600 } // 1 hour
})

// Tag-based revalidation
const data = await fetch('https://api.example.com/data', {
  next: { tags: ['posts'] }
})
```

### Revalidation

```tsx
'use server'

import { revalidatePath, revalidateTag } from 'next/cache'

export async function updatePost() {
  // Revalidate specific path
  revalidatePath('/posts')

  // Revalidate by tag
  revalidateTag('posts')

  // Revalidate layout
  revalidatePath('/posts', 'layout')
}
```

### Route Segment Config

```tsx
// Force dynamic rendering
export const dynamic = 'force-dynamic'

// Revalidate every 60 seconds
export const revalidate = 60

// Generate static params
export async function generateStaticParams() {
  const posts = await getPosts()
  return posts.map((post) => ({ slug: post.slug }))
}
```

## API Routes (Route Handlers)

```tsx
// app/api/posts/route.ts
import { NextResponse } from 'next/server'

export async function GET() {
  const posts = await db.posts.findMany()
  return NextResponse.json(posts)
}

export async function POST(request: Request) {
  const body = await request.json()
  const post = await db.posts.create({ data: body })
  return NextResponse.json(post, { status: 201 })
}
```

**Dynamic route handler:**
```tsx
// app/api/posts/[id]/route.ts
export async function GET(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params
  const post = await db.posts.findUnique({ where: { id } })

  if (!post) {
    return NextResponse.json({ error: 'Not found' }, { status: 404 })
  }

  return NextResponse.json(post)
}
```

## Middleware

```tsx
// middleware.ts (root level)
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Check auth
  const token = request.cookies.get('token')

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  // Add headers
  const response = NextResponse.next()
  response.headers.set('x-custom-header', 'value')

  return response
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/:path*'],
}
```

## Metadata & SEO

```tsx
// Static metadata
export const metadata = {
  title: 'My App',
  description: 'App description',
  openGraph: {
    title: 'My App',
    description: 'App description',
    images: ['/og.png'],
  },
}

// Dynamic metadata
export async function generateMetadata({ params }) {
  const post = await getPost(params.slug)
  return {
    title: post.title,
    description: post.excerpt,
  }
}
```

## Image Optimization

```tsx
import Image from 'next/image'

export function Avatar() {
  return (
    <Image
      src="/avatar.png"
      alt="Avatar"
      width={64}
      height={64}
      priority // Above the fold
    />
  )
}

// Remote images (configure in next.config.js)
<Image
  src="https://example.com/image.jpg"
  alt="Remote image"
  width={800}
  height={600}
/>
```

## Environment Variables

```bash
# .env.local (git ignored, local dev)
DATABASE_URL=postgresql://...
SECRET_KEY=abc123

# Public (exposed to browser)
NEXT_PUBLIC_API_URL=https://api.example.com
```

```tsx
// Server only
const dbUrl = process.env.DATABASE_URL

// Client accessible
const apiUrl = process.env.NEXT_PUBLIC_API_URL
```

## Common Patterns

### Authentication Check

```tsx
import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'

export default async function ProtectedPage() {
  const cookieStore = await cookies()
  const session = cookieStore.get('session')

  if (!session) {
    redirect('/login')
  }

  return <Dashboard />
}
```

### Error Handling

```tsx
// app/error.tsx
'use client'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  )
}
```

### Loading States

```tsx
// app/dashboard/loading.tsx
export default function Loading() {
  return <DashboardSkeleton />
}
```

## Best Practices

1. **Default to Server Components** - Only use Client Components when needed
2. **Colocate data fetching** - Fetch data in the component that needs it
3. **Use Server Actions for mutations** - Not API routes
4. **Implement proper loading states** - Use Suspense and loading.tsx
5. **Configure caching appropriately** - Don't over-cache dynamic content
6. **Use `generateStaticParams`** - For static generation of dynamic routes

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `'use client'` everywhere | Only use for interactivity |
| Fetching in layout for child data | Fetch in the page/component that needs it |
| Not awaiting `params`/`searchParams` | These are now Promises in Next.js 15 |
| Using API routes for mutations | Use Server Actions instead |
| Forgetting to revalidate cache | Call `revalidatePath`/`revalidateTag` |

## Reference Files

- [references/app-router.md](references/app-router.md) - Advanced routing patterns
- [references/caching.md](references/caching.md) - Caching strategies deep dive
- [references/server-actions.md](references/server-actions.md) - Server Actions patterns
- [references/deployment.md](references/deployment.md) - Vercel and self-hosting

## Templates

- [templates/page.tsx](templates/page.tsx) - Page component template
- [templates/layout.tsx](templates/layout.tsx) - Layout component template
- [templates/server-action.ts](templates/server-action.ts) - Server Action template
