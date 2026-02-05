---
name: nextjs-app-development
description: Build Next.js applications with App Router and Pages Router, including Server Components, Server Actions, data fetching, and routing. Use when building Next.js apps, implementing SSR/SSG, or creating API routes.
---

# Next.js App Development Specialist

Specialized in building Next.js applications using both App Router (Next.js 13+) and Pages Router.

## When to Use This Skill

- Building Next.js applications with App Router or Pages Router
- Implementing Server Components and Client Components
- Creating layouts, pages, and special files
- Implementing Server Actions for data mutations
- Setting up data fetching strategies (SSR, SSG, ISR)
- Creating API routes and Route Handlers
- Implementing dynamic routing

## Core Principles

- **Server First**: Prefer Server Components for better performance
- **Client When Needed**: Use Client Components for interactivity
- **Data Fetching**: Choose appropriate strategy (SSR, SSG, ISR)
- **File-System Routing**: Leverage Next.js routing conventions
- **Type Safety**: Use TypeScript for params, searchParams, etc.
- **Progressive Enhancement**: Build with JavaScript optional when possible

## App Router (Next.js 13+)

### Directory Structure

```
app/
├── layout.tsx          # Root layout
├── page.tsx            # Home page (/)
├── loading.tsx         # Loading UI
├── error.tsx           # Error UI
├── not-found.tsx       # 404 UI
├── (marketing)/        # Route group (doesn't affect URL)
│   ├── layout.tsx
│   ├── about/
│   │   └── page.tsx    # /about
│   └── pricing/
│       └── page.tsx    # /pricing
├── dashboard/
│   ├── layout.tsx
│   ├── page.tsx        # /dashboard
│   └── settings/
│       └── page.tsx    # /dashboard/settings
├── blog/
│   ├── page.tsx        # /blog
│   └── [slug]/
│       └── page.tsx    # /blog/:slug
└── api/
    └── users/
        └── route.ts    # API route
```

### Server Components vs Client Components

```typescript
// Server Component (default)
// Runs on server, no JavaScript sent to client
export default async function UserList() {
  // WHY: Fetch data directly in component on server
  const users = await fetchUsers()

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}

// Client Component (opt-in with 'use client')
'use client'

import { useState } from 'react'

export default function Counter() {
  // WHY: Needs client-side state and interactivity
  const [count, setCount] = useState(0)

  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  )
}

// Composition: Server Component with Client Component children
export default async function Page() {
  const users = await fetchUsers()

  return (
    <div>
      <h1>Users</h1>
      {/* Server Component */}
      <UserList users={users} />
      {/* Client Component for interactivity */}
      <AddUserForm />
    </div>
  )
}
```

### Layouts

```typescript
// app/layout.tsx - Root Layout (required)
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'My App',
  description: 'My awesome app',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <header>Header</header>
        <main>{children}</main>
        <footer>Footer</footer>
      </body>
    </html>
  )
}

// app/dashboard/layout.tsx - Nested Layout
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="dashboard">
      <aside>Sidebar</aside>
      <div>{children}</div>
    </div>
  )
}
```

### Pages with Type-Safe Params

```typescript
// app/blog/[slug]/page.tsx
interface PageProps {
  params: { slug: string }
  searchParams: { [key: string]: string | string[] | undefined }
}

export default async function BlogPost({ params, searchParams }: PageProps) {
  const { slug } = params
  const post = await fetchPost(slug)

  return (
    <article>
      <h1>{post.title}</h1>
      <div>{post.content}</div>
    </article>
  )
}

// Generate static params for SSG
export async function generateStaticParams() {
  const posts = await fetchAllPosts()

  return posts.map(post => ({
    slug: post.slug,
  }))
}

// Generate metadata
export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const post = await fetchPost(params.slug)

  return {
    title: post.title,
    description: post.excerpt,
  }
}
```

### Data Fetching

```typescript
// Default: Cache enabled (SSG-like)
async function getUsers() {
  const res = await fetch('https://api.example.com/users')
  return res.json()
}

// Revalidate every 60 seconds (ISR)
async function getUsers() {
  const res = await fetch('https://api.example.com/users', {
    next: { revalidate: 60 },
  })
  return res.json()
}

// No cache (SSR-like)
async function getUsers() {
  const res = await fetch('https://api.example.com/users', {
    cache: 'no-store',
  })
  return res.json()
}

// Opt out of caching for entire route
export const dynamic = 'force-dynamic'
export const revalidate = 0

export default async function Page() {
  const users = await getUsers()
  return <div>...</div>
}
```

### Server Actions

```typescript
// app/actions.ts
'use server'

import { revalidatePath } from 'next/cache'

export async function createUser(formData: FormData) {
  const name = formData.get('name') as string
  const email = formData.get('email') as string

  // Validate
  if (!name || !email) {
    return { error: 'Name and email are required' }
  }

  // Create user
  await db.users.create({ name, email })

  // WHY: Revalidate to show updated data
  revalidatePath('/users')

  return { success: true }
}

export async function deleteUser(userId: string) {
  await db.users.delete(userId)
  revalidatePath('/users')
}

// app/users/create-form.tsx
'use client'

import { createUser } from './actions'

export function CreateUserForm() {
  return (
    <form action={createUser}>
      <input name="name" type="text" required />
      <input name="email" type="email" required />
      <button type="submit">Create User</button>
    </form>
  )
}

// With useFormStatus
'use client'

import { useFormStatus } from 'react-dom'

function SubmitButton() {
  const { pending } = useFormStatus()

  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Creating...' : 'Create User'}
    </button>
  )
}
```

### Route Handlers (API Routes)

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server'

// GET /api/users
export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const query = searchParams.get('query')

  const users = await db.users.findMany({
    where: query ? { name: { contains: query } } : {},
  })

  return NextResponse.json(users)
}

// POST /api/users
export async function POST(request: NextRequest) {
  const body = await request.json()

  const user = await db.users.create({
    data: {
      name: body.name,
      email: body.email,
    },
  })

  return NextResponse.json(user, { status: 201 })
}

// app/api/users/[id]/route.ts
interface RouteContext {
  params: { id: string }
}

// GET /api/users/:id
export async function GET(request: NextRequest, { params }: RouteContext) {
  const user = await db.users.findUnique({
    where: { id: params.id },
  })

  if (!user) {
    return NextResponse.json({ error: 'User not found' }, { status: 404 })
  }

  return NextResponse.json(user)
}

// DELETE /api/users/:id
export async function DELETE(request: NextRequest, { params }: RouteContext) {
  await db.users.delete({
    where: { id: params.id },
  })

  return new NextResponse(null, { status: 204 })
}
```

### Special Files

```typescript
// app/loading.tsx - Loading UI
export default function Loading() {
  return <div>Loading...</div>
}

// app/error.tsx - Error UI
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

// app/not-found.tsx - 404 UI
export default function NotFound() {
  return (
    <div>
      <h2>Not Found</h2>
      <p>Could not find requested resource</p>
    </div>
  )
}
```

## Pages Router (Legacy, Still Supported)

### Directory Structure

```
pages/
├── _app.tsx            # Custom App
├── _document.tsx       # Custom Document
├── index.tsx           # Home page (/)
├── about.tsx           # /about
├── blog/
│   ├── index.tsx       # /blog
│   └── [slug].tsx      # /blog/:slug
└── api/
    └── users.ts        # API route
```

### Page Component

```typescript
// pages/index.tsx
import type { NextPage } from 'next'

const Home: NextPage = () => {
  return (
    <div>
      <h1>Welcome</h1>
    </div>
  )
}

export default Home
```

### getServerSideProps (SSR)

```typescript
// pages/users.tsx
import type { GetServerSideProps, NextPage } from 'next'

interface Props {
  users: User[]
}

const UsersPage: NextPage<Props> = ({ users }) => {
  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}

// WHY: Fetch data on every request (SSR)
export const getServerSideProps: GetServerSideProps<Props> = async (context) => {
  // Access query params
  const { query } = context

  const users = await fetchUsers()

  return {
    props: {
      users,
    },
  }
}

export default UsersPage

// Redirect example
export const getServerSideProps: GetServerSideProps = async (context) => {
  const session = await getSession(context)

  if (!session) {
    return {
      redirect: {
        destination: '/login',
        permanent: false,
      },
    }
  }

  return {
    props: { session },
  }
}

// Not found example
export const getServerSideProps: GetServerSideProps = async (context) => {
  const user = await fetchUser(context.params?.id as string)

  if (!user) {
    return {
      notFound: true,
    }
  }

  return {
    props: { user },
  }
}
```

### getStaticProps (SSG)

```typescript
// pages/about.tsx
import type { GetStaticProps, NextPage } from 'next'

interface Props {
  data: Data
}

const AboutPage: NextPage<Props> = ({ data }) => {
  return <div>{data.content}</div>
}

// WHY: Generate page at build time (SSG)
export const getStaticProps: GetStaticProps<Props> = async () => {
  const data = await fetchAboutData()

  return {
    props: {
      data,
    },
    revalidate: 60, // ISR: Revalidate every 60 seconds
  }
}

export default AboutPage
```

### getStaticPaths (SSG with Dynamic Routes)

```typescript
// pages/blog/[slug].tsx
import type { GetStaticPaths, GetStaticProps, NextPage } from 'next'

interface Props {
  post: Post
}

const BlogPost: NextPage<Props> = ({ post }) => {
  return (
    <article>
      <h1>{post.title}</h1>
      <div>{post.content}</div>
    </article>
  )
}

// WHY: Define which paths to pre-render at build time
export const getStaticPaths: GetStaticPaths = async () => {
  const posts = await fetchAllPosts()

  return {
    paths: posts.map(post => ({
      params: { slug: post.slug },
    })),
    fallback: 'blocking', // or false or true
  }
}

export const getStaticProps: GetStaticProps<Props> = async (context) => {
  const slug = context.params?.slug as string
  const post = await fetchPost(slug)

  if (!post) {
    return {
      notFound: true,
    }
  }

  return {
    props: { post },
    revalidate: 60,
  }
}

export default BlogPost
```

### API Routes (Pages Router)

```typescript
// pages/api/users.ts
import type { NextApiRequest, NextApiResponse } from 'next'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method === 'GET') {
    const users = await db.users.findMany()
    return res.status(200).json(users)
  }

  if (req.method === 'POST') {
    const { name, email } = req.body

    if (!name || !email) {
      return res.status(400).json({ error: 'Name and email required' })
    }

    const user = await db.users.create({
      data: { name, email },
    })

    return res.status(201).json(user)
  }

  return res.status(405).json({ error: 'Method not allowed' })
}

// pages/api/users/[id].ts
export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const { id } = req.query

  if (req.method === 'GET') {
    const user = await db.users.findUnique({
      where: { id: id as string },
    })

    if (!user) {
      return res.status(404).json({ error: 'User not found' })
    }

    return res.status(200).json(user)
  }

  if (req.method === 'DELETE') {
    await db.users.delete({
      where: { id: id as string },
    })

    return res.status(204).end()
  }

  return res.status(405).json({ error: 'Method not allowed' })
}
```

### Custom _app and _document

```typescript
// pages/_app.tsx
import type { AppProps } from 'next/app'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const queryClient = new QueryClient()

export default function App({ Component, pageProps }: AppProps) {
  return (
    <QueryClientProvider client={queryClient}>
      <Component {...pageProps} />
    </QueryClientProvider>
  )
}

// pages/_document.tsx
import { Html, Head, Main, NextScript } from 'next/document'

export default function Document() {
  return (
    <Html lang="en">
      <Head />
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  )
}
```

## Tools to Use

- `Read`: Read existing Next.js pages and components
- `Write`: Create new pages and routes
- `Edit`: Modify existing code
- `Bash`: Run Next.js dev server and build

### Bash Commands

```bash
# Development
npm run dev

# Build
npm run build

# Start production server
npm run start

# Type checking
tsc --noEmit

# Linting
eslint . --ext .ts,.tsx
```

## Workflow

1. **Plan Routes**: Design URL structure and routing
2. **Choose Router**: Decide between App Router and Pages Router
3. **Write Tests**: Test page rendering and data fetching
4. **Implement Pages**: Create page components
5. **Add Data Fetching**: Implement SSR/SSG/ISR as needed
6. **Test Integration**: Ensure pages work end-to-end
7. **Optimize**: Check build output and performance
8. **Commit**: Create atomic commit

## Related Skills

- `react-component-development`: For component implementation
- `react-state-management`: For state management
- `nextjs-optimization`: For performance optimization
- `vitest-react-testing`: For testing
- `playwright-testing`: For E2E testing

## Coding Standards

See [React Coding Standards](../_shared/react-coding-standards.md)

## TDD Workflow

Follow [Frontend TDD Workflow](../_shared/frontend-tdd-workflow.md)

## Key Reminders

- **App Router**: Prefer Server Components, use Client Components when needed
- **Pages Router**: Choose appropriate data fetching method (SSR/SSG/ISR)
- Use TypeScript for type-safe params and props
- Implement proper loading and error states
- Use Server Actions for data mutations in App Router
- Leverage file-system routing conventions
- Set appropriate cache and revalidation strategies
- Generate metadata for SEO
- Use Route Handlers (App Router) or API Routes (Pages Router) for backend logic
- Test both client and server behavior
- Write comments explaining WHY, not WHAT
