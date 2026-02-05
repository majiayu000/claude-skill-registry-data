---
name: nextjs-workflow
description: Next.js framework workflow guidelines. Activate when working with Next.js projects, next.config, app router, or Next.js-specific patterns.
location: user
---

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

# Next.js Workflow

## Tool Grid

| Task | Tool | Command |
|------|------|---------|
| Run dev | Next.js | `npm run dev` |
| Build | Next.js | `npm run build` |
| Turbopack | Next.js | `next dev --turbo` |
| Test | Vitest | `vitest` |
| E2E | Playwright | `playwright test` |
| Lint | ESLint + next | `next lint` |

---

## App Router

App Router MUST be used for all new Next.js projects. Pages Router SHOULD only be used for legacy compatibility.

### Directory Structure

```
app/
├── layout.tsx          # Root layout (REQUIRED)
├── page.tsx            # Home page
├── loading.tsx         # Loading UI
├── error.tsx           # Error boundary
├── not-found.tsx       # 404 page
├── globals.css         # Global styles
├── (group)/            # Route groups (no URL segment)
│   └── page.tsx
├── api/                # API routes
│   └── route.ts
└── [slug]/             # Dynamic routes
    └── page.tsx
```

### Route Groups

Route groups `(groupName)` SHOULD be used to:
- Organize routes without affecting URL structure
- Apply different layouts to route subsets
- Split application into logical sections

---

## Server Components

Server Components are the DEFAULT. Client Components MUST be explicitly marked.

### When to Use Server Components (Default)

- Data fetching
- Accessing backend resources directly
- Keeping sensitive data on server (tokens, API keys)
- Large dependencies that SHOULD stay server-side

### When to Use Client Components

Client Components MUST be marked with `'use client'` directive at the top of the file.

Use Client Components for:
- Interactivity (onClick, onChange, etc.)
- React hooks (useState, useEffect, useContext)
- Browser-only APIs (localStorage, window)
- Custom hooks with state or effects

```tsx
'use client'

import { useState } from 'react'

export function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(count + 1)}>{count}</button>
}
```

### Component Composition Pattern

Server Components MAY import Client Components. Client Components MUST NOT import Server Components directly but MAY accept them as props.

```tsx
// ServerComponent.tsx (Server Component - default)
import { ClientWrapper } from './ClientWrapper'
import { ServerChild } from './ServerChild'

export function ServerComponent() {
  return (
    <ClientWrapper>
      <ServerChild />  {/* Passed as children prop */}
    </ClientWrapper>
  )
}
```

---

## File-Based Routing

### Special Files

| File | Purpose | Required |
|------|---------|----------|
| `layout.tsx` | Shared UI for segment and children | Root only |
| `page.tsx` | Unique UI for route | Yes for route |
| `loading.tsx` | Loading UI with Suspense | OPTIONAL |
| `error.tsx` | Error boundary | OPTIONAL |
| `not-found.tsx` | 404 UI | OPTIONAL |
| `route.ts` | API endpoint | OPTIONAL |
| `template.tsx` | Re-rendered layout | OPTIONAL |
| `default.tsx` | Parallel route fallback | OPTIONAL |

### Dynamic Routes

```
app/
├── blog/
│   ├── [slug]/page.tsx        # /blog/:slug
│   └── [...slug]/page.tsx     # /blog/* (catch-all)
├── shop/
│   └── [[...slug]]/page.tsx   # /shop or /shop/* (optional catch-all)
```

### Parallel Routes

Parallel routes SHOULD be used for complex layouts with independent navigation.

```
app/
├── @modal/
│   └── login/page.tsx
├── @sidebar/
│   └── page.tsx
└── layout.tsx  # Receives modal and sidebar as props
```

### Intercepting Routes

```
app/
├── feed/
│   └── (..)photo/[id]/page.tsx  # Intercepts /photo/[id]
└── photo/
    └── [id]/page.tsx
```

---

## Partial Prerendering (PPR)

PPR SHOULD be enabled for pages with static shells and dynamic content.

### Configuration

```ts
// next.config.ts
const nextConfig = {
  experimental: {
    ppr: 'incremental',
  },
}
```

### Usage

```tsx
// app/page.tsx
export const experimental_ppr = true

export default function Page() {
  return (
    <main>
      <StaticHeader />         {/* Prerendered */}
      <Suspense fallback={<Skeleton />}>
        <DynamicContent />     {/* Streamed */}
      </Suspense>
    </main>
  )
}
```

---

## Server Actions

Server Actions MUST be used for form handling and data mutations.

### Inline Server Actions

```tsx
// app/page.tsx
export default function Page() {
  async function createItem(formData: FormData) {
    'use server'
    const name = formData.get('name')
    // Database operation
    revalidatePath('/')
  }

  return (
    <form action={createItem}>
      <input name="name" />
      <button type="submit">Create</button>
    </form>
  )
}
```

### Separate Action Files

Actions MAY be defined in separate files for reuse.

```ts
// app/actions.ts
'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'

export async function createItem(formData: FormData) {
  // Validation
  // Database operation
  revalidatePath('/items')
  redirect('/items')
}
```

### Client Component Usage

```tsx
'use client'

import { useFormStatus } from 'react-dom'
import { createItem } from './actions'

function SubmitButton() {
  const { pending } = useFormStatus()
  return <button disabled={pending}>{pending ? 'Creating...' : 'Create'}</button>
}

export function CreateForm() {
  return (
    <form action={createItem}>
      <input name="name" />
      <SubmitButton />
    </form>
  )
}
```

---

## Data Fetching

### Request Deduplication

Next.js automatically deduplicates fetch requests. The same URL SHOULD be fetched in multiple components without concern.

```tsx
// Both components fetch the same data - automatically deduplicated
async function Header() {
  const user = await fetch('/api/user').then(r => r.json())
  return <div>{user.name}</div>
}

async function Sidebar() {
  const user = await fetch('/api/user').then(r => r.json())
  return <div>{user.email}</div>
}
```

### Caching Options

```tsx
// Default: cached indefinitely (static)
fetch('https://api.example.com/data')

// Revalidate every 60 seconds
fetch('https://api.example.com/data', { next: { revalidate: 60 } })

// No caching (dynamic)
fetch('https://api.example.com/data', { cache: 'no-store' })

// Revalidate on-demand with tags
fetch('https://api.example.com/data', { next: { tags: ['posts'] } })
```

### On-Demand Revalidation

```ts
// app/actions.ts
'use server'

import { revalidatePath, revalidateTag } from 'next/cache'

export async function updatePost() {
  // Update database
  revalidateTag('posts')      // Revalidate by tag
  revalidatePath('/blog')     // Revalidate by path
}
```

---

## Image Optimization

`next/image` MUST be used for all images.

### Basic Usage

```tsx
import Image from 'next/image'

export function Avatar() {
  return (
    <Image
      src="/avatar.jpg"
      alt="User avatar"
      width={64}
      height={64}
      priority  // For LCP images
    />
  )
}
```

### Responsive Images

```tsx
<Image
  src="/hero.jpg"
  alt="Hero image"
  fill
  sizes="(max-width: 768px) 100vw, 50vw"
  style={{ objectFit: 'cover' }}
/>
```

### Remote Images

Remote domains MUST be configured in `next.config.ts`:

```ts
// next.config.ts
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'cdn.example.com',
        pathname: '/images/**',
      },
    ],
  },
}
```

---

## Font Optimization

`next/font` SHOULD be used for optimal font loading.

### Google Fonts

```tsx
// app/layout.tsx
import { Inter, Roboto_Mono } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
})

const robotoMono = Roboto_Mono({
  subsets: ['latin'],
  variable: '--font-roboto-mono',
  display: 'swap',
})

export default function RootLayout({ children }) {
  return (
    <html className={`${inter.variable} ${robotoMono.variable}`}>
      <body>{children}</body>
    </html>
  )
}
```

### Local Fonts

```tsx
import localFont from 'next/font/local'

const myFont = localFont({
  src: './fonts/MyFont.woff2',
  display: 'swap',
})
```

---

## Metadata API

### Static Metadata

```tsx
// app/page.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Page Title',
  description: 'Page description',
  openGraph: {
    title: 'OG Title',
    description: 'OG Description',
    images: ['/og-image.jpg'],
  },
}
```

### Dynamic Metadata

```tsx
// app/blog/[slug]/page.tsx
import type { Metadata } from 'next'

type Props = { params: Promise<{ slug: string }> }

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params
  const post = await getPost(slug)

  return {
    title: post.title,
    description: post.excerpt,
  }
}
```

### Template Pattern

```tsx
// app/layout.tsx
export const metadata: Metadata = {
  title: {
    template: '%s | My Site',
    default: 'My Site',
  },
}

// app/about/page.tsx
export const metadata: Metadata = {
  title: 'About',  // Results in "About | My Site"
}
```

---

## Middleware

Middleware MUST be placed at `middleware.ts` in the project root.

### Basic Middleware

```ts
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Check auth
  const token = request.cookies.get('token')

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/:path*'],
}
```

### Headers and Rewrites

```ts
export function middleware(request: NextRequest) {
  const response = NextResponse.next()

  // Add headers
  response.headers.set('x-custom-header', 'value')

  // Rewrite (internal redirect)
  if (request.nextUrl.pathname === '/old-path') {
    return NextResponse.rewrite(new URL('/new-path', request.url))
  }

  return response
}
```

---

## Environment Variables

### Naming Convention

| Prefix | Availability | Example |
|--------|--------------|---------|
| None | Server only | `DATABASE_URL` |
| `NEXT_PUBLIC_` | Client + Server | `NEXT_PUBLIC_API_URL` |

### Usage

```tsx
// Server Component or API Route
const dbUrl = process.env.DATABASE_URL

// Client Component (MUST have NEXT_PUBLIC_ prefix)
const apiUrl = process.env.NEXT_PUBLIC_API_URL
```

### Validation

Environment variables SHOULD be validated at build time:

```ts
// lib/env.ts
import { z } from 'zod'

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  NEXT_PUBLIC_API_URL: z.string().url(),
})

export const env = envSchema.parse(process.env)
```

---

## TypeScript Configuration

### Required tsconfig.json Settings

```json
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

---

## Common Patterns

### Loading States

```tsx
// app/dashboard/loading.tsx
export default function Loading() {
  return <div className="animate-pulse">Loading...</div>
}
```

### Error Boundaries

```tsx
// app/dashboard/error.tsx
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

### Not Found

```tsx
// app/not-found.tsx
import Link from 'next/link'

export default function NotFound() {
  return (
    <div>
      <h2>Not Found</h2>
      <Link href="/">Return Home</Link>
    </div>
  )
}
```

### Programmatic Not Found

```tsx
import { notFound } from 'next/navigation'

async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const item = await getItem(id)

  if (!item) {
    notFound()
  }

  return <div>{item.name}</div>
}
```
