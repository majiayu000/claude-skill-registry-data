---
name: nextjs-app-router-typescript
description: Complete Next.js development framework with App Router, TypeScript, and modern patterns. Provides comprehensive assistance for building Next.js applications with the latest features, TypeScript integration, server components, client components, data fetching, and deployment. Use when users ask to build Next.js applications, implement routing, create components, or develop React applications with the latest Next.js features.
---

# Next.js App Router with TypeScript - Complete Development Framework

## Overview

This skill provides comprehensive assistance for Next.js development with the App Router, TypeScript, and modern patterns. It covers project setup, routing, components, data fetching, API routes, styling, and deployment using best practices with the latest Next.js features.

## What This Skill Does
- Creates Next.js project structures with App Router and TypeScript
- Implements routing with the App Router (app directory)
- Creates server and client components with proper patterns
- Sets up TypeScript with Next.js best practices
- Implements data fetching strategies (server-side, client-side, static)
- Creates API routes with Next.js
- Provides styling solutions (CSS Modules, Tailwind, etc.)
- Follows Next.js performance optimization patterns
- Implements SEO and metadata best practices

## What This Skill Does NOT Do
- Create backend APIs (Node.js servers, databases)
- Manage infrastructure (Docker, Kubernetes, cloud deployment)
- Handle specific business logic beyond Next.js patterns
- Provide complete application code without user requirements

---

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing structure, patterns, conventions to integrate with |
| **Conversation** | User's specific Next.js requirements, routing needs, styling preferences |
| **Skill References** | Next.js documentation patterns, best practices, App Router conventions |
| **User Guidelines** | Project-specific conventions, team standards, deployment requirements |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

---

## Required Clarifications

Ask about USER'S context (not domain knowledge):

1. **App type**: "Is this a static site, dynamic site, or hybrid application?"
2. **Styling**: "Which styling approach do you prefer (Tailwind, CSS Modules, Styled Components)?"
3. **Data fetching**: "Will you need server-side rendering, static generation, or client-side fetching?"
4. **Deployment**: "Where do you plan to deploy the application (Vercel, Netlify, custom server)?"

---

## Workflow

1. Set up Next.js project with App Router and TypeScript
2. Create project structure with proper directory organization
3. Implement routing with the App Router
4. Create server and client components with appropriate patterns
5. Set up data fetching strategies
6. Implement API routes if needed
7. Add styling and UI components
8. Prepare for deployment

---

## Project Setup with TypeScript

### Installation
```bash
# Create a new Next.js project with TypeScript
npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir

# Or manually:
npm create next-app@latest my-app
cd my-app
npm install typescript @types/react @types/node
```

### Recommended Project Structure
```
my-nextjs-app/
├── src/
│   ├── app/                    # App Router (Next.js 13+)
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Home page
│   │   ├── error.tsx           # Global error boundary
│   │   ├── loading.tsx         # Global loading UI
│   │   ├── not-found.tsx       # Global not found page
│   │   ├── globals.css         # Global styles
│   │   ├── api/                # API routes
│   │   │   └── [...nextauth]/ # Example API route
│   │   ├── dashboard/          # Nested route
│   │   │   ├── page.tsx
│   │   │   ├── layout.tsx
│   │   │   └── loading.tsx
│   │   └── blog/               # Dynamic route
│   │       ├── page.tsx
│   │       ├── [slug]/         # Dynamic segment
│   │       │   └── page.tsx
│   │       └── layout.tsx
│   ├── components/             # Reusable components
│   │   ├── ui/                 # UI components
│   │   │   ├── button.tsx
│   │   │   └── card.tsx
│   │   └── navigation/
│   │       └── navbar.tsx
│   ├── lib/                    # Utilities and helpers
│   │   └── utils.ts
│   ├── hooks/                  # Custom React hooks
│   │   └── use-media-query.ts
│   ├── types/                  # TypeScript types
│   │   └── index.ts
│   └── styles/                 # Styling files
│       └── globals.css
├── public/                     # Static assets
├── next.config.js              # Next.js configuration
├── tailwind.config.js          # Tailwind configuration
├── tsconfig.json               # TypeScript configuration
├── package.json
└── README.md
```

### TypeScript Configuration (tsconfig.json)
```json
{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

### Next.js Configuration (next.config.js)
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true, // Enable App Router
  },
  images: {
    domains: ['example.com'], // Add image domains for optimization
  },
  // Optional: Export as static HTML
  // output: 'export', // Uncomment for static export
}

module.exports = nextConfig
```

---

## App Router Patterns

### Root Layout (src/app/layout.tsx)
```tsx
import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { ReactNode } from 'react'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Create Next App',
  description: 'Generated by create next app',
}

export default function RootLayout({
  children,
}: {
  children: ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div id="root">{children}</div>
      </body>
    </html>
  )
}
```

### Home Page (src/app/page.tsx)
```tsx
import Link from 'next/link'
import { Suspense } from 'react'

// Server Component
export default async function HomePage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <main className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-6">
          Welcome to Next.js App Router
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-3">App Router</h2>
            <p className="text-gray-600 mb-4">
              The new App Router provides enhanced routing capabilities with nested layouts and server components.
            </p>
            <Link
              href="/dashboard"
              className="inline-block bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md transition-colors"
            >
              Go to Dashboard
            </Link>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-3">TypeScript</h2>
            <p className="text-gray-600 mb-4">
              Full TypeScript support with type-safe routing and components.
            </p>
            <Link
              href="/blog"
              className="inline-block bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-md transition-colors"
            >
              View Blog
            </Link>
          </div>
        </div>
      </main>
    </div>
  )
}
```

### Nested Layout (src/app/dashboard/layout.tsx)
```tsx
import { ReactNode } from 'react'
import Sidebar from '@/components/navigation/sidebar'
import Header from '@/components/navigation/header'

export default function DashboardLayout({
  children,
}: {
  children: ReactNode
}) {
  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        <main className="flex-1 overflow-y-auto p-6">
          {children}
        </main>
      </div>
    </div>
  )
}
```

### Dynamic Route (src/app/blog/[slug]/page.tsx)
```tsx
import { notFound } from 'next/navigation'
import { Metadata } from 'next'

// Dynamic params
type Props = {
  params: { slug: string }
}

// Generate metadata for SEO
export async function generateMetadata({
  params
}: Props): Promise<Metadata> {
  const post = await getPost(params.slug)

  if (!post) {
    return {}
  }

  return {
    title: post.title,
    description: post.excerpt,
  }
}

// Fetch data for the page
async function getPost(slug: string) {
  // Simulate API call
  const res = await fetch(`https://jsonplaceholder.typicode.com/posts/${slug}`)
  if (!res.ok) return null
  return res.json()
}

export default async function BlogPostPage({
  params
}: Props) {
  const post = await getPost(params.slug)

  if (!post) {
    notFound()
  }

  return (
    <article className="max-w-3xl mx-auto px-4 py-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">{post.title}</h1>
        <div className="text-gray-500 text-sm">
          By {post.userId} • {new Date().toLocaleDateString()}
        </div>
      </header>

      <div className="prose max-w-none">
        <p className="text-lg text-gray-700 mb-6">{post.body}</p>
      </div>
    </article>
  )
}
```

---

## Server and Client Components

### Server Component Example
```tsx
// app/components/user-profile-server.tsx
import { getUser } from '@/lib/user-service'

// Server Component - runs on the server
export default async function UserProfileServer({
  userId
}: {
  userId: string
}) {
  const user = await getUser(userId)

  if (!user) {
    return <div>User not found</div>
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-3">{user.name}</h2>
      <p className="text-gray-600">{user.email}</p>
      <p className="text-gray-500 text-sm mt-2">Member since {user.createdAt}</p>
    </div>
  )
}
```

### Client Component Example
```tsx
// app/components/user-profile-client.tsx
'use client'

import { useState, useEffect } from 'react'

// Client Component - runs in the browser
export default function UserProfileClient({
  userId
}: {
  userId: string
}) {
  const [user, setUser] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchUser() {
      try {
        const response = await fetch(`/api/users/${userId}`)
        const userData = await response.json()
        setUser(userData)
      } catch (error) {
        console.error('Error fetching user:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchUser()
  }, [userId])

  if (loading) {
    return <div>Loading...</div>
  }

  if (!user) {
    return <div>User not found</div>
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-3">{user.name}</h2>
      <p className="text-gray-600">{user.email}</p>
      <p className="text-gray-500 text-sm mt-2">Member since {user.createdAt}</p>
    </div>
  )
}
```

### Using Components in Pages
```tsx
// app/dashboard/page.tsx
import UserProfileServer from '@/components/user-profile-server'
import UserProfileClient from '@/components/user-profile-client'

export default function DashboardPage() {
  return (
    <div className="space-y-8">
      <h1 className="text-2xl font-bold">Dashboard</h1>

      {/* Server Component - data fetched on the server */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h2 className="text-lg font-semibold mb-3">Server Component</h2>
          <UserProfileServer userId="123" />
        </div>

        <div>
          <h2 className="text-lg font-semibold mb-3">Client Component</h2>
          <UserProfileClient userId="123" />
        </div>
      </div>
    </div>
  )
}
```

---

## Data Fetching Patterns

### Server-Side Data Fetching
```tsx
// app/data-fetching-example/page.tsx
import { Suspense } from 'react'

// Server component that fetches data
async function PostsList() {
  // Data fetching happens on the server
  const res = await fetch('https://jsonplaceholder.typicode.com/posts?_limit=10')
  const posts = await res.json()

  return (
    <div className="space-y-4">
      {posts.map((post: any) => (
        <div key={post.id} className="bg-white p-4 rounded-lg shadow">
          <h3 className="font-semibold">{post.title}</h3>
          <p className="text-gray-600 text-sm mt-2">{post.body}</p>
        </div>
      ))}
    </div>
  )
}

// Client component that fetches data
'use client'
import { useState, useEffect } from 'react'

function ClientPostsList() {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchPosts() {
      const res = await fetch('/api/posts')
      const data = await res.json()
      setPosts(data)
      setLoading(false)
    }

    fetchPosts()
  }, [])

  if (loading) return <div>Loading posts...</div>

  return (
    <div className="space-y-4">
      {posts.map((post: any) => (
        <div key={post.id} className="bg-white p-4 rounded-lg shadow">
          <h3 className="font-semibold">{post.title}</h3>
          <p className="text-gray-600 text-sm mt-2">{post.body}</p>
        </div>
      ))}
    </div>
  )
}

export default function DataFetchingPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">Data Fetching Examples</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div>
          <h2 className="text-xl font-semibold mb-4">Server Component (RSC)</h2>
          <Suspense fallback={<div>Loading server posts...</div>}>
            <PostsList />
          </Suspense>
        </div>

        <div>
          <h2 className="text-xl font-semibold mb-4">Client Component</h2>
          <ClientPostsList />
        </div>
      </div>
    </div>
  )
}
```

### Streaming with Suspense
```tsx
// app/streaming-example/page.tsx
import { Suspense } from 'react'

async function ProductList() {
  // Simulate slow data fetching
  await new Promise(resolve => setTimeout(resolve, 2000))

  const res = await fetch('https://fakestoreapi.com/products?limit=6')
  const products = await res.json()

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {products.map((product: any) => (
        <div key={product.id} className="border rounded-lg p-4">
          <img
            src={product.image}
            alt={product.title}
            className="w-full h-48 object-contain mb-4"
          />
          <h3 className="font-semibold">{product.title}</h3>
          <p className="text-gray-600">${product.price}</p>
        </div>
      ))}
    </div>
  )
}

async function Reviews() {
  // Simulate slow data fetching
  await new Promise(resolve => setTimeout(resolve, 1000))

  const res = await fetch('https://jsonplaceholder.typicode.com/comments?_limit=5')
  const reviews = await res.json()

  return (
    <div className="space-y-3">
      {reviews.map((review: any) => (
        <div key={review.id} className="bg-gray-50 p-3 rounded">
          <p className="text-sm">{review.body}</p>
          <p className="text-xs text-gray-500 mt-1">by {review.email}</p>
        </div>
      ))}
    </div>
  )
}

export default function StreamingPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">Streaming Example</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div>
          <h2 className="text-lg font-semibold mb-3">Products</h2>
          <Suspense fallback={<div>Loading products...</div>}>
            <ProductList />
          </Suspense>
        </div>

        <div>
          <h2 className="text-lg font-semibold mb-3">Reviews</h2>
          <Suspense fallback={<div>Loading reviews...</div>}>
            <Reviews />
          </Suspense>
        </div>
      </div>
    </div>
  )
}
```

---

## API Routes

### Basic API Route
```typescript
// app/api/users/route.ts
import { NextRequest } from 'next/server'

export async function GET(request: NextRequest) {
  // Get search params
  const searchParams = request.nextUrl.searchParams
  const page = searchParams.get('page')
  const limit = searchParams.get('limit')

  // Simulate API call
  const users = [
    { id: 1, name: 'John Doe', email: 'john@example.com' },
    { id: 2, name: 'Jane Smith', email: 'jane@example.com' },
  ]

  return Response.json({ users, page, limit })
}

export async function POST(request: NextRequest) {
  const body = await request.json()

  // Validate input
  if (!body.name || !body.email) {
    return Response.json(
      { error: 'Name and email are required' },
      { status: 400 }
    )
  }

  // Process the request
  const newUser = {
    id: Date.now(),
    name: body.name,
    email: body.email,
  }

  return Response.json({ user: newUser }, { status: 201 })
}
```

### Dynamic API Route
```typescript
// app/api/users/[id]/route.ts
import { NextRequest } from 'next/server'

// GET /api/users/123
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const { id } = params

  // Simulate fetching user by ID
  const user = {
    id,
    name: 'John Doe',
    email: 'john@example.com',
    createdAt: new Date().toISOString(),
  }

  if (!user) {
    return Response.json({ error: 'User not found' }, { status: 404 })
  }

  return Response.json({ user })
}

// PUT /api/users/123
export async function PUT(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const { id } = params
  const body = await request.json()

  // Simulate updating user
  const updatedUser = {
    id,
    ...body,
    updatedAt: new Date().toISOString(),
  }

  return Response.json({ user: updatedUser })
}

// DELETE /api/users/123
export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const { id } = params

  // Simulate deleting user
  // In real app: await deleteUser(id)

  return Response.json({ message: 'User deleted successfully' })
}
```

---

## Styling Patterns

### CSS Modules Example
```css
/* components/ui/button.module.css */
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.375rem;
  font-weight: 500;
  transition: all 0.2s ease-in-out;
}

.button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.primary {
  background-color: #3b82f6;
  color: white;
  padding: 0.5rem 1rem;
}

.secondary {
  background-color: transparent;
  color: #3b82f6;
  border: 1px solid #3b82f6;
  padding: 0.5rem 1rem;
}

.large {
  padding: 0.75rem 1.5rem;
  font-size: 1.125rem;
}
```

```tsx
// components/ui/button.tsx
import styles from './button.module.css'
import { ReactNode } from 'react'

type ButtonVariant = 'primary' | 'secondary'
type ButtonSize = 'default' | 'large'

interface ButtonProps {
  children: ReactNode
  variant?: ButtonVariant
  size?: ButtonSize
  onClick?: () => void
  type?: 'button' | 'submit' | 'reset'
  disabled?: boolean
}

export default function Button({
  children,
  variant = 'primary',
  size = 'default',
  onClick,
  type = 'button',
  disabled = false,
}: ButtonProps) {
  const buttonClasses = [
    styles.button,
    styles[variant],
    size === 'large' && styles.large,
    disabled && 'opacity-50 cursor-not-allowed',
  ].filter(Boolean).join(' ')

  return (
    <button
      type={type}
      className={buttonClasses}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  )
}
```

### Tailwind CSS with TypeScript
```tsx
// components/ui/card.tsx
import { ReactNode } from 'react'

interface CardProps {
  children: ReactNode
  className?: string
  title?: string
  description?: string
}

export default function Card({
  children,
  className = '',
  title,
  description,
}: CardProps) {
  return (
    <div className={`bg-white rounded-xl shadow-md overflow-hidden ${className}`}>
      {(title || description) && (
        <div className="border-b border-gray-200 p-6">
          {title && (
            <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
          )}
          {description && (
            <p className="mt-1 text-sm text-gray-500">{description}</p>
          )}
        </div>
      )}
      <div className="p-6">
        {children}
      </div>
    </div>
  )
}
```

### Global Styles (src/app/globals.css)
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --foreground-rgb: 0, 0, 0;
  --background-start-rgb: 214, 219, 220;
  --background-end-rgb: 255, 255, 255;
}

@media (prefers-color-scheme: dark) {
  :root {
    --foreground-rgb: 255, 255, 255;
    --background-start-rgb: 0, 0, 0;
    --background-end-rgb: 0, 0, 0;
  }
}

body {
  color: rgb(var(--foreground-rgb));
  background: linear-gradient(
      to bottom,
      transparent,
      rgb(var(--background-end-rgb))
    )
    rgb(var(--background-start-rgb));
}

@layer utilities {
  .text-balance {
    text-wrap: balance;
  }
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #c5c5c5;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
```

---

## SEO and Metadata

### Dynamic Metadata
```tsx
// app/blog/[slug]/page.tsx
import { Metadata } from 'next'

type Props = {
  params: { slug: string }
}

// Generate metadata dynamically
export async function generateMetadata({
  params
}: Props): Promise<Metadata> {
  const post = await getPost(params.slug)

  if (!post) {
    return {}
  }

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      type: 'article',
      publishedTime: post.publishedAt,
      authors: [post.author],
    },
    twitter: {
      card: 'summary_large_image',
      title: post.title,
      description: post.excerpt,
    },
  }
}

async function getPost(slug: string) {
  // Fetch post data
  const res = await fetch(`https://api.example.com/posts/${slug}`)
  if (!res.ok) return null
  return res.json()
}

export default async function BlogPost({
  params
}: Props) {
  const post = await getPost(params.slug)

  if (!post) {
    return <div>Post not found</div>
  }

  return (
    <article>
      <h1>{post.title}</h1>
      <div>{post.content}</div>
    </article>
  )
}
```

### Sitemap Generation
```typescript
// app/sitemap.ts
import { MetadataRoute } from 'next'

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    {
      url: 'https://example.com',
      lastModified: new Date(),
      changeFrequency: 'yearly',
      priority: 1,
    },
    {
      url: 'https://example.com/about',
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.8,
    },
    {
      url: 'https://example.com/blog',
      lastModified: new Date(),
      changeFrequency: 'weekly',
      priority: 0.5,
    },
  ]
}
```

### Robots.txt
```typescript
// app/robots.ts
import { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: '*',
      allow: '/',
      disallow: '/private/',
    },
    sitemap: 'https://example.com/sitemap.xml',
  }
}
```

---

## Performance Optimization

### Image Optimization
```tsx
// components/ui/image.tsx
import Image from 'next/image'
import { useState } from 'react'

interface OptimizedImageProps {
  src: string
  alt: string
  width: number
  height: number
  className?: string
  priority?: boolean
}

export default function OptimizedImage({
  src,
  alt,
  width,
  height,
  className = '',
  priority = false,
}: OptimizedImageProps) {
  const [isLoading, setIsLoading] = useState(true)

  return (
    <div className={`relative overflow-hidden ${isLoading ? 'bg-gray-200' : ''}`}>
      <Image
        src={src}
        alt={alt}
        width={width}
        height={height}
        className={`transition-opacity duration-300 ${isLoading ? 'opacity-0' : 'opacity-100'} ${className}`}
        priority={priority}
        onLoadingComplete={() => setIsLoading(false)}
        placeholder="blur"
        blurDataURL="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k=" // Base64 placeholder
      />
    </div>
  )
}
```

### Link Prefetching
```tsx
// components/navigation/link.tsx
'use client'

import NextLink from 'next/link'
import { ReactNode } from 'react'

interface LinkProps {
  href: string
  children: ReactNode
  className?: string
  prefetch?: boolean
}

export default function Link({
  href,
  children,
  className = '',
  prefetch = true
}: LinkProps) {
  return (
    <NextLink
      href={href}
      className={className}
      prefetch={prefetch}
    >
      {children}
    </NextLink>
  )
}
```

### Component Lazy Loading
```tsx
// components/lazy-component.tsx
'use client'

import { Suspense, lazy } from 'react'

const HeavyComponent = lazy(() => import('./heavy-component'))

export default function LazyComponent() {
  return (
    <Suspense fallback={<div>Loading heavy component...</div>}>
      <HeavyComponent />
    </Suspense>
  )
}
```

---

## Error Handling

### Global Error Boundary
```tsx
// app/error.tsx
'use client'

import { useEffect } from 'react'

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    // Log the error to an error reporting service
    console.error(error)
  }, [error])

  return (
    <html>
      <body>
        <div className="min-h-screen flex items-center justify-center bg-red-50">
          <div className="text-center p-8 bg-white rounded-lg shadow-lg">
            <h2 className="text-2xl font-bold text-red-600 mb-4">
              Something went wrong!
            </h2>
            <p className="text-gray-600 mb-6">
              {error.message || 'An unexpected error occurred'}
            </p>
            <button
              onClick={() => reset()}
              className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md transition-colors"
            >
              Try again
            </button>
          </div>
        </div>
      </body>
    </html>
  )
}
```

### Not Found Page
```tsx
// app/not-found.tsx
export default function NotFound() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-center p-8 bg-white rounded-lg shadow-lg">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          404 - Page Not Found
        </h2>
        <p className="text-gray-600 mb-6">
          The page you are looking for might have been removed, had its name changed, or is temporarily unavailable.
        </p>
        <a
          href="/"
          className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md transition-colors"
        >
          Go back home
        </a>
      </div>
    </div>
  )
}
```

---

## Testing Patterns

### Jest and React Testing Library Setup
```json
// package.json
{
  "devDependencies": {
    "@testing-library/jest-dom": "^5.16.5",
    "@testing-library/react": "^13.4.0",
    "@testing-library/user-event": "^14.4.3",
    "@types/jest": "^29.5.0",
    "jest": "^29.5.0",
    "jest-environment-jsdom": "^29.5.0"
  }
}
```

```javascript
// jest.config.js
const nextJest = require('next/jest')

const createJestConfig = nextJest({
  // Provide the path to your Next.js app to load next.config.js and .env files in your test environment
  dir: './',
})

// Add any custom config to be passed to Jest
const customJestConfig = {
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  testEnvironment: 'jest-environment-jsdom',
}

// createJestConfig is exported in this way to ensure that next/jest can load the Next.js configuration, which is async
module.exports = createJestConfig(customJestConfig)
```

```javascript
// jest.setup.js
import '@testing-library/jest-dom'
```

### Component Testing Example
```tsx
// components/ui/button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react'
import Button from './button'

describe('Button', () => {
  it('renders with correct text', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn()
    render(<Button onClick={handleClick}>Click me</Button>)

    fireEvent.click(screen.getByText('Click me'))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click me</Button>)
    expect(screen.getByText('Click me')).toBeDisabled()
  })
})
```

### API Route Testing
```typescript
// __tests__/api/users.test.ts
import { NextRequest } from 'next/server'
import { GET } from '@/app/api/users/route'

describe('Users API', () => {
  it('should return users list', async () => {
    const request = new NextRequest('http://localhost:3000/api/users', {
      method: 'GET',
    })

    const response = await GET(request)
    const data = await response.json()

    expect(response.status).toBe(200)
    expect(Array.isArray(data.users)).toBe(true)
  })
})
```

---

## Deployment Configuration

### Vercel Configuration
```json
// vercel.json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/next"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/$1"
    }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-XSS-Protection",
          "value": "1; mode=block"
        }
      ]
    }
  ]
}
```

### Docker Configuration
```dockerfile
# Dockerfile
FROM node:18-alpine AS base

# Install dependencies only when needed
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Install dependencies based on the preferred package manager
COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* ./
RUN \
  if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
  elif [ -f package-lock.json ]; then npm ci; \
  elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm i --frozen-lockfile; \
  else echo "Lockfile not found." && exit 1; \
  fi

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED 1

RUN \
  if [ -f yarn.lock ]; then yarn run build; \
  elif [ -f package-lock.json ]; then npm run build; \
  elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm run build; \
  else echo "Lockfile not found." && exit 1; \
  fi

# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public

# Set the correct permission for prerender cache
RUN mkdir .next
RUN chown nextjs:nodejs .next

# Automatically leverage output traces to reduce image size
# https://nextjs.org/docs/advanced-features/output-file-tracing
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000

CMD ["node", "server.js"]
```

### Environment Configuration
```typescript
// lib/config.ts
export const config = {
  api: {
    baseUrl: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:3000/api',
  },
  auth: {
    jwtSecret: process.env.JWT_SECRET || 'fallback-secret',
    sessionMaxAge: parseInt(process.env.SESSION_MAX_AGE || '86400'), // 24 hours
  },
  features: {
    analytics: process.env.NEXT_PUBLIC_ANALYTICS_ENABLED === 'true',
    debug: process.env.NODE_ENV === 'development',
  },
} as const
```

---

## Best Practices

### Component Composition Pattern
```tsx
// components/ui/card.tsx
import { ReactNode } from 'react'

interface CardProps {
  children: ReactNode
  className?: string
}

interface CardHeaderProps {
  children: ReactNode
  className?: string
}

interface CardTitleProps {
  children: ReactNode
  className?: string
}

interface CardDescriptionProps {
  children: ReactNode
  className?: string
}

interface CardContentProps {
  children: ReactNode
  className?: string
}

interface CardFooterProps {
  children: ReactNode
  className?: string
}

export function Card({ children, className = '' }: CardProps) {
  return (
    <div className={`bg-white rounded-lg shadow ${className}`}>
      {children}
    </div>
  )
}

export function CardHeader({ children, className = '' }: CardHeaderProps) {
  return (
    <div className={`p-6 border-b border-gray-200 ${className}`}>
      {children}
    </div>
  )
}

export function CardTitle({ children, className = '' }: CardTitleProps) {
  return (
    <h3 className={`text-lg font-semibold text-gray-900 ${className}`}>
      {children}
    </h3>
  )
}

export function CardDescription({ children, className = '' }: CardDescriptionProps) {
  return (
    <p className={`text-sm text-gray-500 mt-1 ${className}`}>
      {children}
    </p>
  )
}

export function CardContent({ children, className = '' }: CardContentProps) {
  return <div className={`p-6 ${className}`}>{children}</div>
}

export function CardFooter({ children, className = '' }: CardFooterProps) {
  return (
    <div className={`p-6 border-t border-gray-200 ${className}`}>
      {children}
    </div>
  )
}

// Usage
export default function ExampleCard() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>User Profile</CardTitle>
        <CardDescription>Manage your account settings</CardDescription>
      </CardHeader>
      <CardContent>
        <p>Card content goes here</p>
      </CardContent>
      <CardFooter>
        <button>Save Changes</button>
      </CardFooter>
    </Card>
  )
}
```

### Custom Hooks
```typescript
// hooks/use-media-query.ts
import { useState, useEffect } from 'react'

export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false)

  useEffect(() => {
    const media = window.matchMedia(query)
    if (media.matches !== matches) {
      setMatches(media.matches)
    }
    const listener = () => setMatches(media.matches)
    media.addEventListener('change', listener)
    return () => media.removeEventListener('change', listener)
  }, [matches, query])

  return matches
}

// hooks/use-scroll-direction.ts
import { useState, useEffect } from 'react'

export function useScrollDirection() {
  const [scrollDirection, setScrollDirection] = useState<'up' | 'down' | null>(null)

  useEffect(() => {
    let lastScrollY = window.pageYOffset

    const updateScrollDirection = () => {
      const scrollY = window.pageYOffset
      const direction = scrollY > lastScrollY ? 'down' : 'up'
      if (direction !== scrollDirection && (scrollY - lastScrollY > 10 || scrollY - lastScrollY < -10)) {
        setScrollDirection(direction)
      }
      lastScrollY = scrollY > 0 ? scrollY : 0
    }

    window.addEventListener('scroll', updateScrollDirection)
    return () => window.removeEventListener('scroll', updateScrollDirection)
  }, [scrollDirection])

  return scrollDirection
}
```

### Type Safety Patterns
```typescript
// types/index.ts
export interface User {
  id: string
  name: string
  email: string
  avatar?: string
  createdAt: string
  updatedAt?: string
}

export interface Post {
  id: string
  title: string
  content: string
  excerpt?: string
  author: User
  publishedAt: string
  updatedAt?: string
  tags: string[]
  image?: string
}

export type UserRole = 'admin' | 'moderator' | 'user'

export interface ApiResponse<T> {
  data: T
  message?: string
  success: boolean
  error?: string
}

// lib/api.ts
import { ApiResponse } from '@/types'

export async function apiRequest<T>(
  endpoint: string,
  options?: RequestInit
): Promise<ApiResponse<T>> {
  try {
    const response = await fetch(`/api${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
      ...options,
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.error || 'API request failed')
    }

    return {
      success: true,
      data,
    }
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
      data: null as any,
    }
  }
}
```

---

## Using Context7 MCP Server for Documentation

When you need the latest Next.js documentation, patterns, or examples, you can use the fetch-library-docs skill:

```bash
# Use the fetch-library-docs skill to get the latest Next.js documentation
# This will provide you with the most up-to-date patterns and best practices
```

---

## Output Checklist

Before delivering, verify:
- [ ] Project structure follows recommended organization
- [ ] App Router implementation is correct
- [ ] TypeScript configuration is properly set up
- [ ] Server and client components are appropriately used
- [ ] Data fetching patterns are implemented correctly
- [ ] API routes follow Next.js conventions
- [ ] Styling solutions are consistent
- [ ] SEO and metadata are properly configured
- [ ] Performance optimizations are applied
- [ ] Error handling is comprehensive
- [ ] Testing patterns are included

---

## Reference Files

| File | When to Read |
|------|--------------|
| `references/nextjs-docs.md` | When implementing advanced Next.js features |
| `references/app-router-best-practices.md` | When configuring routing and layouts |
| `references/typescript-patterns.md` | When implementing type-safe components |
| `references/deployment-guidelines.md` | When preparing for production deployment |