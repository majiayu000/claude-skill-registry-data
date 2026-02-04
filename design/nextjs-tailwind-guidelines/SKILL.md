---
name: nextjs-tailwind-guidelines
description: Next.js 15 + Tailwind CSS development guidelines. Modern patterns including App Router, Server/Client Components, Suspense, lazy loading, file organization, Tailwind CSS styling, performance optimization, and TypeScript best practices. Use when creating components, pages, features, styling, routing, or working with Next.js code.
---

# Next.js + Tailwind Development Guidelines

## Purpose

Comprehensive guide for modern Next.js 15 development with App Router, emphasizing Server Components, Suspense-based patterns, Tailwind CSS styling, and performance optimization.

## When to Use This Skill

- Creating new components or pages
- Building new features with App Router
- Server vs Client Component decisions
- Styling with Tailwind CSS
- Next.js routing and layouts
- Performance optimization
- Organizing frontend code
- TypeScript best practices

---

## Quick Start

### New Component Checklist

- [ ] Server Component (default) or Client Component ('use client')?
- [ ] Use TypeScript with proper prop types
- [ ] Lazy load heavy components: `lazy(() => import())`
- [ ] Wrap in `<Suspense>` for loading states
- [ ] Import alias: `@/` for src directory
- [ ] Tailwind classes with `className`
- [ ] `useCallback` for event handlers passed to children
- [ ] Default export at bottom
- [ ] No early returns with loading spinners

### New Feature Checklist

- [ ] Create `src/features/{feature}/` directory
- [ ] Subdirectories: `components/`, `hooks/`, `lib/`, `types/`
- [ ] TypeScript types in `types/`
- [ ] Route in `src/app/{feature}/page.tsx`
- [ ] Lazy load client components when needed
- [ ] Suspense boundaries for async operations
- [ ] Export public API from `index.ts`

---

## Server vs Client Components

**SERVER COMPONENTS (Default):**

- Data fetching
- Static content
- SEO-critical content
- No interactivity needed
- Zero JavaScript to client

**CLIENT COMPONENTS ('use client'):**

- useState, useEffect, useContext
- Event handlers (onClick, onChange)
- Browser APIs (localStorage, window)
- Third-party libraries requiring browser

**Key Rule:** Default to Server Components, add 'use client' only when needed

---

## Component Patterns

### Server Component

```typescript
// Server Component - No 'use client' needed
import { Suspense } from 'react';

interface Props {
  id: string;
}

async function MyServerComponent({ id }: Props) {
  // Fetch data directly in Server Component
  const data = await fetch(`https://api.example.com/data/${id}`).then(r => r.json());

  return (
    <div className="p-4 bg-white dark:bg-gray-900">
      <h1 className="text-2xl font-bold">{data.title}</h1>
    </div>
  );
}

export default MyServerComponent;
```

### Client Component

```typescript
'use client';

import { useState, useCallback } from 'react';
import { motion } from 'framer-motion';

interface Props {
  onAction?: () => void;
}

export function MyClientComponent({ onAction }: Props) {
  const [count, setCount] = useState(0);

  const handleClick = useCallback(() => {
    setCount(c => c + 1);
    onAction?.();
  }, [onAction]);

  return (
    <motion.button
      onClick={handleClick}
      className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
      whileHover={{ scale: 1.05 }}
    >
      Clicked {count} times
    </motion.button>
  );
}

export default MyClientComponent;
```

---

## Tailwind CSS Styling

### Basic Patterns

```typescript
// Utility classes
<div className="flex items-center justify-between p-4 bg-white dark:bg-gray-900">

// Responsive
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">

// Conditional classes (simple)
<div className={`base-class ${isActive ? 'active' : 'inactive'}`}>

// Conditional classes (complex) - use cn utility
import { cn } from '@/lib/utils';
<div className={cn(
  "base-class",
  isActive && "active-class",
  isLarge && "text-xl"
)}>
```

### Common Patterns

```typescript
// Card
<div className="rounded-lg border bg-card text-card-foreground shadow-sm">

// Button
<button className="inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90">

// Input
<input className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm">
```

---

## App Router Structure

```
src/
  app/
    layout.tsx         # Root layout
    page.tsx           # Home page (/)
    about/
      page.tsx         # /about
    blog/
      layout.tsx       # Blog layout
      page.tsx         # /blog
      [slug]/
        page.tsx       # /blog/[slug]
    api/
      hello/
        route.ts       # API endpoint
```

### Page Example

```typescript
// src/app/my-route/page.tsx
import { Suspense } from 'react';
import { MyFeature } from '@/features/my-feature';

// Metadata for SEO
export const metadata = {
  title: 'My Page',
  description: 'Page description',
};

export default function MyPage() {
  return (
    <div className="container mx-auto py-8">
      <Suspense fallback={<div className="animate-pulse">Loading...</div>}>
        <MyFeature />
      </Suspense>
    </div>
  );
}
```

### Layout Example

```typescript
// src/app/layout.tsx
import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'My App',
  description: 'App description',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-background font-sans antialiased">
        {children}
      </body>
    </html>
  );
}
```

---

## Data Fetching

### Server Component (Recommended)

```typescript
// Fetch directly in Server Component
async function MyComponent() {
  const data = await fetch('https://api.example.com/data', {
    next: { revalidate: 3600 } // Cache for 1 hour
  }).then(r => r.json());

  return <div>{data.title}</div>;
}
```

### Client Component (when needed)

```typescript
'use client';

import { useEffect, useState } from 'react';

export function MyClientData() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/data')
      .then(r => r.json())
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading...</div>;
  return <div>{data?.title}</div>;
}
```

---

## Performance Optimization

### Next.js Built-in

```typescript
// Image optimization
import Image from 'next/image';
<Image
  src="/hero.jpg"
  alt="Hero"
  width={800}
  height={600}
  priority // For above-fold images
/>

// Font optimization
import { Inter } from 'next/font/google';
const inter = Inter({ subsets: ['latin'] });

// Dynamic imports (lazy loading)
import dynamic from 'next/dynamic';
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <div>Loading...</div>,
  ssr: false // Disable SSR if needed
});
```

### React Optimization

```typescript
'use client';

import { useMemo, useCallback, memo } from 'react';

// useMemo for expensive computations
const filtered = useMemo(() =>
  items.filter(item => item.active).sort((a, b) => a.name.localeCompare(b.name)),
  [items]
);

// useCallback for event handlers
const handleClick = useCallback((id: string) => {
  console.log(id);
}, []);

// memo for expensive components
const ExpensiveComponent = memo(({ data }: Props) => {
  return <div>{/* Heavy rendering */}</div>;
});
```

---

## Loading & Error States

### Loading UI

```typescript
// src/app/my-route/loading.tsx
export default function Loading() {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary" />
    </div>
  );
}
```

### Error Handling

```typescript
// src/app/my-route/error.tsx
'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h2 className="text-2xl font-bold mb-4">Something went wrong!</h2>
      <button
        onClick={reset}
        className="px-4 py-2 bg-primary text-primary-foreground rounded"
      >
        Try again
      </button>
    </div>
  );
}
```

---

## File Organization

```
src/
  app/                    # Next.js App Router
    layout.tsx
    page.tsx
    globals.css

  components/             # Reusable UI components
    ui/
      button.tsx
      card.tsx
    layout/
      header.tsx
      footer.tsx

  features/               # Feature-specific code
    auth/
      components/
      hooks/
      lib/
      types/
      index.ts

  lib/                    # Shared utilities
    utils.ts

  types/                  # Global types
    index.ts
```

---

## TypeScript Best Practices

```typescript
// Explicit prop types
interface ComponentProps {
  title: string;
  count?: number;
  onAction: (id: string) => void;
}

// Type imports
import type { ReactNode } from 'react';

// Async Server Component typing
async function MyComponent(): Promise<JSX.Element> {
  const data = await fetchData();
  return <div>{data}</div>;
}

// Client Component typing
'use client';
export function MyClient({ children }: { children: ReactNode }) {
  return <div>{children}</div>;
}
```

---

## Animation with Framer Motion

```typescript
'use client';

import { motion } from 'framer-motion';

export function AnimatedCard() {
  return (
    <motion.div
      className="p-6 bg-card rounded-lg"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      whileHover={{ scale: 1.02 }}
    >
      Content
    </motion.div>
  );
}
```

---

## Icons with Lucide React

```typescript
import { Search, Menu, X, ChevronRight } from 'lucide-react';

export function IconExample() {
  return (
    <button className="flex items-center gap-2">
      <Search className="h-4 w-4" />
      <span>Search</span>
    </button>
  );
}
```

---

## Core Principles

1. **Server Components First** - Default to Server, add 'use client' only when needed
2. **Suspense for Loading** - Use Suspense boundaries, not early returns
3. **Tailwind for Styling** - Utility-first CSS with design tokens
4. **Features Organized** - components/, hooks/, lib/, types/ subdirs
5. **Next.js Image & Font** - Always use optimized components
6. **Import Aliases** - Use @/ for clean imports
7. **No Early Returns** - Prevents layout shift
8. **TypeScript Strict** - Type everything properly

---

**Skill Status**: Adapted for Next.js 15 + Tailwind CSS v4
