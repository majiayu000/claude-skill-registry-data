---
name: worldcrafter-route-creator
description: Scaffold Next.js App Router routes for simple pages without forms or complex logic. Use when user needs "create a page", "add route", "add about/contact/terms page", "create API endpoint", "add layout", or mentions SSE/webhooks. Generates page, layout, loading, error, and not-found files with boilerplate. Best for static content, read-only pages, and API endpoints (REST, SSE, webhooks). Do NOT use for forms with validation (use worldcrafter-feature-builder), complete features with database (use worldcrafter-feature-builder), database-only changes (use worldcrafter-database-setup), or comprehensive testing (use worldcrafter-test-generator).
---

# WorldCrafter Route Creator

**Version:** 2.0.0
**Last Updated:** 2025-01-15

This skill provides tools and templates for scaffolding Next.js App Router routes with all necessary files and boilerplate code.

## Skill Metadata

**Related Skills:**
- `worldcrafter-feature-builder` - Use instead for complete features with forms and validation
- `worldcrafter-auth-guard` - Use to protect routes after creation
- `worldcrafter-test-generator` - Use to add tests for created routes

**Example Use Cases:**
- "Create an about us page" → Generates page.tsx with static content, loading.tsx, and error.tsx at /about
- "Add an API endpoint for users" → Creates route.ts with GET/POST handlers at /api/users
- "Create a dashboard layout" → Generates layout.tsx with navigation and shared UI for /dashboard routes
- "Add a dynamic product page" → Creates /products/[id]/page.tsx with dynamic route handling

## When to Use This Skill

Use this skill when:
- Creating new pages/routes in the application
- Setting up route groups or nested routes
- Creating API routes (Route Handlers)
- Adding layouts for route segments
- Setting up protected/authenticated routes
- Creating dynamic routes with parameters
- Adding loading states and error boundaries

## Next.js App Router Overview

WorldCrafter uses Next.js 15+ App Router with these file conventions:

- **`page.tsx`** - UI for a route (makes route publicly accessible)
- **`layout.tsx`** - Shared UI for segment and children
- **`loading.tsx`** - Loading UI (Suspense boundary)
- **`error.tsx`** - Error UI (Error boundary)
- **`not-found.tsx`** - 404 UI for not found errors
- **`route.ts`** - API endpoint (Route Handler)

## Route Scaffolding Process

### Phase 1: Plan Route Structure

**Consider:**
- Route path (e.g., `/worlds/[slug]`, `/api/upload`, `/api/sse/activity`)
- Is it a page or API route?
- Does it need authentication?
- Does it need a custom layout?
- What loading/error states are needed?

**WorldCrafter Route Reference**: See `references/worldcrafter-routes.md` for complete application route tree with all patterns:
- World management routes (`/worlds/[slug]/*`)
- Entity routes (characters, locations, events, items, factions)
- Visualization routes (graph, map, timeline, wiki)
- API routes (upload, export, MCP, SSE, webhooks)
- Auth routes (login, signup, reset-password)
- Marketing routes (landing, about, pricing)

### Phase 2: Scaffold Route

**Automated Scaffolding:**

```bash
python .claude/skills/worldcrafter-route-creator/scripts/scaffold_route.py <route-path>
```

**Examples:**
```bash
# Basic page route
python scaffold_route.py dashboard

# Nested route
python scaffold_route.py dashboard/settings

# Dynamic route
python scaffold_route.py posts/[id]

# Route group
python scaffold_route.py (marketing)/about

# API route
python scaffold_route.py api/users --api
```

This creates:
- `src/app/<route-path>/page.tsx` (or `route.ts` for API)
- `src/app/<route-path>/loading.tsx`
- `src/app/<route-path>/error.tsx`
- Optional: `layout.tsx`, `not-found.tsx`

**Manual Approach:**
Copy templates from `assets/templates/` and customize.

### Phase 3: Customize Route Files

#### Page Component (`page.tsx`)

```typescript
export default function DashboardPage() {
  return (
    <div className="container mx-auto py-8">
      <h1 className="text-3xl font-bold">Dashboard</h1>
      {/* Page content */}
    </div>
  )
}
```

**Server Component Features:**
- Async data fetching
- Direct database access
- No client-side JavaScript by default

**Client Component Features:**
- Add `"use client"` directive
- Interactive elements
- Hooks (useState, useEffect, etc.)

#### Layout (`layout.tsx`)

```typescript
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="dashboard-layout">
      <nav>{/* Navigation */}</nav>
      <main>{children}</main>
    </div>
  )
}
```

**Layout Features:**
- Shared UI across routes
- Preserved state on navigation
- Can be nested
- Cannot access route parameters (use page)

#### Loading State (`loading.tsx`)

```typescript
export default function Loading() {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="h-12 w-12 animate-spin rounded-full border-4 border-muted border-t-primary" />
    </div>
  )
}
```

**Features:**
- Instant loading state
- Wrapped in Suspense automatically
- Streamed from server

#### Error Boundary (`error.tsx`)

```typescript
'use client'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center">
      <h2 className="text-2xl font-bold">Something went wrong!</h2>
      <button onClick={reset}>Try again</button>
    </div>
  )
}
```

**Features:**
- Must be Client Component
- Catches errors in children
- Provides reset function
- Can be nested

#### API Route (`route.ts`)

```typescript
import { NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

export async function GET() {
  const data = await prisma.model.findMany()
  return NextResponse.json(data)
}

export async function POST(request: Request) {
  const body = await request.json()
  const result = await prisma.model.create({ data: body })
  return NextResponse.json(result)
}
```

**Supported Methods**: GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS

### Phase 4: Add Metadata

```typescript
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Dashboard',
  description: 'User dashboard page'
}

export default function DashboardPage() {
  // ...
}
```

**Dynamic Metadata:**
```typescript
export async function generateMetadata({ params }): Promise<Metadata> {
  const post = await getPost(params.id)
  return {
    title: post.title,
    description: post.excerpt
  }
}
```

## WorldCrafter API Route Patterns

WorldCrafter uses several specialized API route patterns. See `references/worldcrafter-routes.md` for complete implementations.

### File Upload to Supabase Storage

```typescript
// src/app/api/upload/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { createClient } from '@/lib/supabase/server'

export async function POST(request: NextRequest) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  const formData = await request.formData()
  const file = formData.get('file') as File

  const { data, error } = await supabase.storage
    .from('uploads')
    .upload(`${user.id}/${file.name}`, file)

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }

  return NextResponse.json({ url: data.path })
}
```

### Server-Sent Events (SSE) for Real-Time Updates

```typescript
// src/app/api/sse/activity/route.ts
import { NextRequest } from 'next/server'
import { createClient } from '@/lib/supabase/server'

export async function GET(request: NextRequest) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return new Response('Unauthorized', { status: 401 })
  }

  const stream = new ReadableStream({
    async start(controller) {
      const encoder = new TextEncoder()

      controller.enqueue(encoder.encode(`data: ${JSON.stringify({ type: 'connected' })}\n\n`))

      const channel = supabase
        .channel('activity')
        .on('postgres_changes', {
          event: '*',
          schema: 'public',
          table: 'activities',
          filter: `user_id=eq.${user.id}`
        }, (payload) => {
          controller.enqueue(encoder.encode(`data: ${JSON.stringify(payload)}\n\n`))
        })
        .subscribe()

      request.signal.addEventListener('abort', () => {
        channel.unsubscribe()
        controller.close()
      })
    }
  })

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive'
    }
  })
}
```

### MCP Server (JSON-RPC 2.0)

```typescript
// src/app/api/mcp/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { createClient } from '@/lib/supabase/server'
import { prisma } from '@/lib/prisma'

interface JsonRpcRequest {
  jsonrpc: '2.0'
  method: string
  params?: unknown
  id: string | number
}

export async function POST(request: NextRequest) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return NextResponse.json({
      jsonrpc: '2.0',
      error: { code: -32001, message: 'Unauthorized' },
      id: null
    }, { status: 401 })
  }

  const rpcRequest: JsonRpcRequest = await request.json()

  try {
    const result = await handleMcpMethod(rpcRequest.method, rpcRequest.params, user.id)
    return NextResponse.json({
      jsonrpc: '2.0',
      result,
      id: rpcRequest.id
    })
  } catch (error) {
    return NextResponse.json({
      jsonrpc: '2.0',
      error: {
        code: -32603,
        message: error instanceof Error ? error.message : 'Internal error'
      },
      id: rpcRequest.id
    }, { status: 500 })
  }
}
```

### Webhook Handler (with Signature Verification)

```typescript
// src/app/api/webhooks/stripe/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { headers } from 'next/headers'
import Stripe from 'stripe'

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2024-11-20.acacia'
})

export async function POST(request: NextRequest) {
  const body = await request.text()
  const signature = (await headers()).get('stripe-signature')!

  let event: Stripe.Event

  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    )
  } catch (err) {
    return NextResponse.json({ error: 'Invalid signature' }, { status: 400 })
  }

  // Handle event types
  switch (event.type) {
    case 'checkout.session.completed':
      // Handle successful checkout
      break
    case 'customer.subscription.deleted':
      // Handle subscription cancellation
      break
  }

  return NextResponse.json({ received: true })
}
```

### Background Job (Export)

```typescript
// src/app/api/export/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { createClient } from '@/lib/supabase/server'
import { prisma } from '@/lib/prisma'

export async function POST(request: NextRequest) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  const { worldId } = await request.json()

  // Create export job
  const job = await prisma.exportJob.create({
    data: {
      userId: user.id,
      worldId,
      status: 'pending'
    }
  })

  // Trigger background processing
  // await queueExportJob(job.id)

  return NextResponse.json({ jobId: job.id })
}
```

## Common Route Patterns

### Basic Page Route

```
src/app/
└── about/
    ├── page.tsx       # /about
    ├── loading.tsx
    └── error.tsx
```

### Nested Routes

```
src/app/
└── dashboard/
    ├── page.tsx           # /dashboard
    ├── layout.tsx
    ├── settings/
    │   └── page.tsx       # /dashboard/settings
    └── profile/
        └── page.tsx       # /dashboard/profile
```

### Dynamic Routes

```
src/app/
└── posts/
    ├── page.tsx           # /posts
    └── [id]/
        ├── page.tsx       # /posts/123
        ├── edit/
        │   └── page.tsx   # /posts/123/edit
        └── not-found.tsx
```

**Access Parameters:**
```typescript
export default function PostPage({ params }: { params: { id: string } }) {
  return <div>Post ID: {params.id}</div>
}
```

### WorldCrafter World Management Routes

```
src/app/
└── worlds/
    ├── page.tsx                        # /worlds - List all user's worlds
    ├── new/
    │   └── page.tsx                    # /worlds/new - Create world
    └── [slug]/
        ├── page.tsx                    # /worlds/:slug - Dashboard
        ├── settings/
        │   └── page.tsx                # /worlds/:slug/settings
        ├── characters/
        │   ├── page.tsx                # /worlds/:slug/characters - List
        │   ├── new/
        │   │   └── page.tsx            # /worlds/:slug/characters/new
        │   └── [id]/
        │       ├── page.tsx            # /worlds/:slug/characters/:id - Detail
        │       └── edit/
        │           └── page.tsx        # /worlds/:slug/characters/:id/edit
        ├── graph/
        │   └── page.tsx                # /worlds/:slug/graph - Visualization
        ├── map/
        │   └── page.tsx                # /worlds/:slug/map - Interactive map
        └── timeline/
            └── page.tsx                # /worlds/:slug/timeline - Events timeline
```

**Pattern Features:**
- World slug for human-readable URLs
- Nested entity routes (characters, locations, events, items, factions)
- Consistent CRUD pattern (list, new, [id], [id]/edit)
- Visualization routes (graph, map, timeline)
- All routes protected (auth required)
- World ownership verified in layout

### Catch-All Routes

```
src/app/
└── docs/
    └── [...slug]/
        └── page.tsx       # /docs/a, /docs/a/b, /docs/a/b/c
```

**Optional Catch-All:**
```
└── [[...slug]]/           # Matches /docs too
```

**WorldCrafter Wiki Example:**
```
src/app/
└── worlds/
    └── [slug]/
        └── wiki/
            ├── page.tsx                # /worlds/:slug/wiki - Home
            └── [pageSlug]/
                └── page.tsx            # /worlds/:slug/wiki/:pageSlug
```

### Route Groups

```
src/app/
├── (auth)/                # Auth route group (not in URL)
│   ├── layout.tsx         # Auth-specific layout
│   ├── login/
│   │   └── page.tsx       # /login
│   ├── signup/
│   │   └── page.tsx       # /signup
│   └── reset-password/
│       └── page.tsx       # /reset-password
└── (marketing)/           # Marketing route group (not in URL)
    ├── layout.tsx         # Marketing layout
    ├── page.tsx           # / (landing)
    ├── about/
    │   └── page.tsx       # /about
    └── pricing/
        └── page.tsx       # /pricing
```

**WorldCrafter Use Cases:**
- Different layouts for auth vs marketing pages
- Organize routes logically without affecting URLs
- Share navigation and styling within groups
- Separate public and authenticated sections

### Parallel Routes

```
src/app/
└── dashboard/
    ├── @analytics/
    │   └── page.tsx
    ├── @team/
    │   └── page.tsx
    └── page.tsx
```

**Layout:**
```typescript
export default function Layout({
  children,
  analytics,
  team,
}: {
  children: React.ReactNode
  analytics: React.ReactNode
  team: React.ReactNode
}) {
  return (
    <>
      {children}
      {analytics}
      {team}
    </>
  )
}
```

### Intercepting Routes

```
src/app/
├── feed/
│   └── page.tsx
├── photo/
│   └── [id]/
│       └── page.tsx       # /photo/123
└── @modal/
    └── (.)photo/
        └── [id]/
            └── page.tsx   # Intercepts /photo/123
```

### API Routes

```
src/app/
└── api/
    ├── upload/
    │   └── route.ts           # POST /api/upload - File upload
    ├── export/
    │   └── route.ts           # POST /api/export - Background job
    ├── mcp/
    │   └── route.ts           # POST /api/mcp - MCP server (JSON-RPC)
    ├── sse/
    │   └── activity/
    │       └── route.ts       # GET /api/sse/activity - Server-Sent Events
    └── webhooks/
        └── stripe/
            └── route.ts       # POST /api/webhooks/stripe - Stripe webhook
```

**WorldCrafter API Patterns:**
- File upload to Supabase Storage
- Background job creation (export)
- MCP server with JSON-RPC 2.0
- Server-Sent Events for real-time updates
- Webhook handlers with signature verification

## Authentication Patterns

### Protected Page Route

```typescript
import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'

export default async function ProtectedPage() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    redirect('/login')
  }

  return <div>Protected content for {user.email}</div>
}
```

### Protected API Route

```typescript
import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export async function GET() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  // Fetch user-specific data
  const data = await prisma.data.findMany({
    where: { userId: user.id }
  })

  return NextResponse.json(data)
}
```

### Protected Layout

```typescript
import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    redirect('/login')
  }

  return (
    <div className="dashboard-layout">
      {children}
    </div>
  )
}
```

## Data Fetching Patterns

### Server Component (Recommended)

```typescript
import { prisma } from '@/lib/prisma'

export default async function PostsPage() {
  const posts = await prisma.post.findMany()

  return (
    <div>
      {posts.map(post => (
        <article key={post.id}>{post.title}</article>
      ))}
    </div>
  )
}
```

### Parallel Data Fetching

```typescript
async function getData() {
  const [users, posts] = await Promise.all([
    prisma.user.findMany(),
    prisma.post.findMany()
  ])

  return { users, posts }
}

export default async function Page() {
  const { users, posts } = await getData()
  // ...
}
```

### Sequential Data Fetching

```typescript
export default async function Page({ params }: { params: { id: string } }) {
  const user = await prisma.user.findUnique({
    where: { id: params.id }
  })

  // Waits for user before fetching posts
  const posts = await prisma.post.findMany({
    where: { authorId: user.id }
  })

  return <div>{/* ... */}</div>
}
```

## Reference Files

- `references/worldcrafter-routes.md` - Complete WorldCrafter route tree with all API patterns
- `references/related-skills.md` - How this skill works with other WorldCrafter skills
- `assets/templates/` - All route file templates

**Key patterns in worldcrafter-routes.md:**
- World management structure (`/worlds/[slug]/*`)
- Entity CRUD patterns (characters, locations, events, items, factions)
- API routes (file upload, background jobs, MCP server, SSE, webhooks)
- Auth route group patterns
- Nested layouts and route groups
- Dynamic route parameter handling

## Skill Orchestration

This skill is best for creating simple pages and routes. For complete features with forms, use worldcrafter-feature-builder instead.

### Common Workflows

**Simple Static Pages:**
1. **worldcrafter-route-creator** (this skill) - Create page structure
2. Add content and styling
3. Optionally use **worldcrafter-test-generator** to add tests

**API Endpoints:**
1. **worldcrafter-route-creator** (this skill) - Create route.ts with handlers
2. Add business logic and database operations
3. Optionally use **worldcrafter-auth-guard** to protect endpoints

**Protected Pages:**
1. **worldcrafter-route-creator** (this skill) - Create page structure
2. **worldcrafter-auth-guard** - Add authentication checks

**Dynamic Routes:**
1. **worldcrafter-route-creator** (this skill) - Create [id]/page.tsx structure
2. Add data fetching and rendering logic
3. Add not-found.tsx for invalid IDs

### When Claude Should Use Multiple Skills

Claude will orchestrate route-creator with other skills when:
- User wants a simple page that later needs protection (route-creator → auth-guard)
- User wants to create API endpoints (route-creator → auth-guard for protection)
- User wants static pages with comprehensive tests (route-creator → test-generator)

**Example orchestration:**
```
User: "Create an about page and a contact page"

Claude's workflow:
1. worldcrafter-route-creator (this skill):
   - Create /about page with loading and error states
   - Create /contact page with loading and error states
```

**Alternative - Complete Feature:**
```
User: "Create a contact form"

Claude's workflow (DO NOT use route-creator):
1. worldcrafter-feature-builder (use instead):
   - Creates /contact route with form
   - Adds validation schema
   - Creates Server Action
   - Includes tests
```

### Skill Selection Guidance

**Choose this skill when:**
- User wants "simple page", "about page", "static content"
- User mentions "API endpoint" or "route handler"
- User wants layouts or route structure only
- No forms or validation needed

**Choose worldcrafter-feature-builder instead when:**
- User mentions "form", "submit", "validation", "feature"
- User wants complete functionality with database
- User wants CRUD operations
- User wants comprehensive implementation

**Use this skill for:**
- Static content pages (about, terms, privacy)
- API endpoints (Route Handlers)
- Layouts and route groups
- Simple read-only pages
- Dynamic routes without forms

**Do NOT use this skill for:**
- Forms with validation (use feature-builder)
- Complete features (use feature-builder)
- Database operations (use database-setup or feature-builder)

## Route Scaffolding Script Reference

```bash
# Basic route
python scaffold_route.py dashboard

# With layout
python scaffold_route.py dashboard --with-layout

# API route
python scaffold_route.py api/users --api

# Dynamic route
python scaffold_route.py posts/[id]

# Protected route
python scaffold_route.py dashboard --protected
```

## Troubleshooting

### Route Not Found

- Ensure `page.tsx` exists in route folder
- Check file naming (lowercase, no typos)
- Verify folder structure matches URL

### Layout Not Applied

- Layout must be named `layout.tsx`
- Layout applies to children only
- Check layout is in correct folder

### Loading State Not Showing

- Add `loading.tsx` in route folder
- Ensure page has async operations
- Check Suspense boundaries

### Error Boundary Not Catching

- Error boundary must be Client Component (`'use client'`)
- Only catches errors in children
- Add error.tsx at appropriate level

## Best Practices

1. **Use Server Components by default** - Add `'use client'` only when needed
2. **Colocate files** - Keep components/utilities with routes
3. **Use layouts for shared UI** - Navigation, headers, footers
4. **Add loading states** - Improve perceived performance
5. **Handle errors gracefully** - Provide reset functionality
6. **Protect sensitive routes** - Check auth in server components
7. **Optimize metadata** - Use generateMetadata for dynamic content
8. **Use route groups** - Organize routes without affecting URLs

## Success Criteria

A complete route setup includes:
- ✅ Page component created
- ✅ Loading state added
- ✅ Error boundary added
- ✅ Layout (if shared UI needed)
- ✅ Metadata configured
- ✅ Authentication check (if protected)
- ✅ Not-found page (for dynamic routes)
- ✅ Route accessible at correct URL
