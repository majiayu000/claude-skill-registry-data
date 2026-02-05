---
name: frontend-dev-guidelines
description: Frontend development guidelines for Quantum Skincare's Next.js 16 App Router application with React 19.2, Tailwind CSS v4, Clerk authentication, and TypeScript. Covers Server/Client Components, React 19.2 features (useEffectEvent, Activity component, cache signals, React Compiler auto-optimization), data fetching patterns, Tailwind styling, route groups, form validation, and performance optimization. Use when creating pages, components, API routes, styling, or working with frontend code.
---

# Frontend Development Guidelines - Quantum Skincare

## Purpose

Quick reference for Quantum Skincare's Next.js 16 App Router frontend with React 19.2, emphasizing Server Components, Tailwind CSS v4, Clerk authentication, and React Compiler auto-optimization.

## When to Use This Skill

- Creating new pages or components
- Implementing Server or Client Components
- Using React 19.2 features (React Compiler, useEffectEvent, Activity, cache signals)
- Data fetching with Server Components or client-side
- Styling with Tailwind CSS v4
- Setting up authentication with Clerk
- Form validation with Zod
- URL state management with nuqs
- Performance optimization
- TypeScript best practices

---

## Quick Start

### New Page Checklist

- [ ] Create in `app/(private)/` or `app/(public)/` route group
- [ ] Default to Server Component (async function)
- [ ] Use `currentUser()` from Clerk for auth
- [ ] Fetch data with `fetch` + `{ cache: 'no-store' }` or `backendJson()`
- [ ] Use Tailwind CSS v4 for styling
- [ ] Wrap async content in `<Suspense>` with fallback
- [ ] Add `loading.tsx` for route-level loading state
- [ ] Use `'use client'` only for interactivity
- [ ] Keep components < 150 lines (refactor at 300+)

### New Component Checklist

- [ ] Server Component by default (no 'use client')
- [ ] Add `'use client'` only if using hooks/events/browser APIs
- [ ] Use Tailwind classes for styling
- [ ] TypeScript props interface with JSDoc
- [ ] Named exports for components, default for pages
- [ ] Co-locate in feature directory (e.g., `components/history/`)
- [ ] Use `cn()` helper from tailwind-merge for conditional classes
- [ ] Consider React 19.2 features: useEffectEvent for stable callbacks, Activity for async loading

---

## React 19.2 Key Features

### React Compiler (Auto-Optimization) ⭐

**IMPORTANT: Next.js 16 includes the stable React Compiler, which automatically memoizes components and optimizes rendering.**

**This means you DON'T need `useMemo`, `useCallback`, or `React.memo` in most cases!**

**Default approach (2025):**
```typescript
'use client';

// ✅ GOOD: Write simple code first, let React Compiler optimize
const expensiveValue = complexCalculation(data);
const handleClick = () => { /* ... */ };

// ❌ AVOID: Premature optimization
const expensiveValue = useMemo(() => complexCalculation(data), [data]);
const handleClick = useCallback(() => { /* ... */ }, []);
```

**When you STILL need manual memoization:**

1. **Extremely expensive calculations** (millions of records, image processing)
2. **Third-party libraries requiring stable references**
3. **React Native apps** (more sensitive to re-renders)
4. **Effect dependencies where function identity matters**

**Golden Rule:** Write clean code first, add memoization only when profiling reveals actual performance bottlenecks.

### useEffectEvent (Stable Event Callbacks)

Use for callbacks that should NOT trigger effect re-runs:

```typescript
'use client';
import { useEffectEvent } from 'react';

export function AnalyticsTracker({ userId, pageUrl }: Props) {
    const logPageView = useEffectEvent(() => {
        analytics.track('page_view', { userId, pageUrl });
    });

    useEffect(() => {
        logPageView();
    }, [pageUrl]); // Only re-run when pageUrl changes, not userId
}
```

**When to use:** Event handlers inside effects, callbacks that need fresh data but shouldn't trigger re-runs. **Prefer this over `useCallback` for effect callbacks.**

### Activity Component

Built-in loading UI without Suspense wrapper:

```typescript
import { Activity } from 'react';

export default async function DashboardPage() {
    return (
        <div>
            <h1>Dashboard</h1>
            <Activity>
                <DashboardContent />
            </Activity>
        </div>
    );
}
```

### cache() (Server-Side Caching)

Memoize expensive server-side operations:

```typescript
import { cache } from 'react';
import 'server-only';

export const getUserData = cache(async (userId: string) => {
    const user = await db.users.findUnique({ where: { id: userId } });
    return user;
});

// Called multiple times, only runs once per request
const data1 = await getUserData('123');
const data2 = await getUserData('123'); // Cached!
```

---

## Architecture Overview

### Next.js 16 App Router Structure

```
apps/frontend/src/
├── app/
│   ├── (private)/          # Protected routes (auth required)
│   │   ├── layout.tsx      # Auth check + layout
│   │   ├── admin/          # Admin-only pages
│   │   ├── cart/           # Shopping cart
│   │   ├── history/        # Scan history
│   │   ├── profile/        # User profile
│   │   ├── shop/           # E-commerce products
│   │   └── skin-analysis/  # Camera + results
│   ├── (public)/           # Public routes
│   │   ├── login/
│   │   ├── register/
│   │   └── sso-callback/
│   ├── internal/           # API routes (proxy to backend)
│   ├── consent/            # Consent gate
│   └── layout.tsx          # Root layout (Clerk provider)
│
├── components/             # Feature-specific components
│   ├── auth/              # Auth forms + flows
│   ├── navigation/        # Navbar, footer
│   ├── skin-analysis/     # Camera + results
│   └── ui/                # Reusable UI primitives
│
├── lib/
│   ├── api/               # Client-side API functions
│   ├── server/            # Server-only utilities (backendJson)
│   ├── auth/              # Clerk adapter
│   ├── utils/             # Utility functions (cn, etc.)
│   └── validation/        # Client-side Zod validation
│
└── middleware.ts           # Clerk auth + consent checks
```

---

## Core Principles

### 1. Server Components by Default

```typescript
// ✅ Server Component (default) - better performance
export default async function HistoryPage() {
    const user = await currentUser(); // Clerk server-side auth
    const scans = await fetch(`${API_URL}/v1/history`, {
        cache: 'no-store',
        headers: { Authorization: `Bearer ${token}` }
    });
    return <HistoryList scans={scans} />;
}
```

**Benefits:** Zero JS to client, direct backend access, better SEO, automatic code splitting

### 2. Use 'use client' Only When Needed

**Require Client Component for:**
- React hooks (useState, useEffect, useEffectEvent, use, useOptimistic, useFormStatus)
- Event handlers (onClick, onChange, onSubmit)
- Browser APIs (window, document, localStorage)
- Client-only libraries

**Note:** You generally DON'T need `useMemo`, `useCallback`, or `React.memo` anymore - React Compiler handles optimization automatically.

### 3. Component Size Guidelines

- **< 150 lines**: Ideal size
- **150-300 lines**: Acceptable
- **> 300 lines**: Refactor required

**Refactoring:** Extract hooks, split into subcomponents, move utils to `lib/utils/`, extract constants/types

### 4. Tailwind CSS v4 Styling

```typescript
import { cn } from '@/lib/utils/cn';

export function Button({ variant, className, ...props }: ButtonProps) {
    return (
        <button
            className={cn(
                'px-4 py-2 rounded-lg font-medium transition-colors',
                variant === 'primary' && 'bg-blue-600 text-white hover:bg-blue-700',
                variant === 'secondary' && 'bg-gray-200 text-gray-900',
                className
            )}
            {...props}
        />
    );
}
```

For complex components, use `tailwind-variants` (`tv()`).

### 5. Authentication with Clerk

**Server Component:**
```typescript
import { currentUser } from '@clerk/nextjs/server';

export default async function DashboardPage() {
    const user = await currentUser();
    if (!user) redirect('/login');
    return <Dashboard user={user} />;
}
```

**Client Component:**
```typescript
'use client';
import { useUser } from '@clerk/nextjs';

export function UserMenu() {
    const { user, isLoaded, isSignedIn } = useUser();
    if (!isLoaded) return <Skeleton />;
    if (!isSignedIn) return <SignInButton />;
    return <div>{user.fullName}</div>;
}
```

### 6. Data Fetching

**Server Components (Preferred):**
```typescript
export default async function ProductPage({ params }: Props) {
    const product = await fetch(`${API_URL}/v1/products/${params.id}`, {
        cache: 'force-cache', // Static product data
    }).then(res => res.json());
    return <ProductDetails product={product} />;
}
```

**Client Components (Via API Routes):**
```typescript
'use client';
import { apiClient } from '@/lib/api/fetch';

export function CameraCapture() {
    const handleCapture = async (blob: Blob) => {
        // Calls /internal/v1/analysis which proxies to backend
        const result = await apiClient('/internal/v1/analysis/stream/frame/validate', {
            method: 'POST',
            body: formData
        });
    };
}
```

### 7. Form Validation with Zod

```typescript
'use client';
import { z } from 'zod';
import { personalInfoSchema } from '@quantum/shared-validation';

export function ProfileForm() {
    const [errors, setErrors] = useState<Record<string, string[]>>({});

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        const formData = new FormData(e.currentTarget);
        const data = { name: formData.get('name'), /* ... */ };

        const result = personalInfoSchema.safeParse(data);
        if (!result.success) {
            setErrors(result.error.flatten().fieldErrors);
            return;
        }
        await submitProfile(result.data);
    };

    return (
        <form onSubmit={handleSubmit}>
            <input name="name" />
            {errors.name && <span className="text-red-500">{errors.name[0]}</span>}
        </form>
    );
}
```

### 8. URL State with nuqs

```typescript
'use client';
import { useQueryState, parseAsInteger } from 'nuqs';

export function Pagination() {
    const [page, setPage] = useQueryState('page', parseAsInteger.withDefault(1));
    return (
        <div>
            <button onClick={() => setPage(page - 1)} disabled={page === 1}>Previous</button>
            <span>Page {page}</span>
            <button onClick={() => setPage(page + 1)}>Next</button>
        </div>
    );
}
```

---

## Common Imports Cheatsheet

```typescript
// React 19.2
import { Suspense, use, useOptimistic, useFormStatus } from 'react';
import { Activity } from 'react'; // Loading component
import { useEffectEvent } from 'react'; // Stable callbacks (prefer over useCallback)
import { cache, cacheSignal } from 'react'; // Server-side caching

// Memoization (only when needed - React Compiler handles most cases)
import { useMemo, useCallback } from 'react'; // Use sparingly

// Next.js 16
import type { Metadata } from 'next';
import { redirect, notFound } from 'next/navigation';
import { headers, cookies } from 'next/headers';

// Clerk Auth
import { currentUser } from '@clerk/nextjs/server';  // Server
import { useUser, useAuth } from '@clerk/nextjs';    // Client

// Server-only
import 'server-only';
import { backendJson } from '@/lib/server/backend';

// Client-side API
import { apiClient } from '@/lib/api/fetch';

// Styling
import { cn } from '@/lib/utils/cn';
import { tv } from 'tailwind-variants';

// URL State
import { useQueryState, parseAsInteger } from 'nuqs';

// Validation
import { z } from 'zod';
import { personalInfoSchema } from '@quantum/shared-validation';

// Shared Types
import type { UserApp, ScanResult } from '@quantum/shared-types';

// Icons
import { Camera, History, User } from 'lucide-react';
```

---

## Key Anti-Patterns

❌ **Don't fetch client-side when server-side works**
❌ **Don't add 'use client' without reason**
❌ **Don't call backend directly from browser** (use `/internal/*`)
❌ **Don't create routes under `/api/*`** (use `/internal/*` with `proxyToBackend()`)
❌ **Don't prematurely use `useMemo`/`useCallback`** (React Compiler handles it)
❌ **Don't forget `cache()` for repeated server queries**

See [ANTI_PATTERNS.md](ANTI_PATTERNS.md) for detailed examples.

---

## Navigation Guide

| Need to... | Pattern |
|------------|---------|
| Create a page | Add `page.tsx` in `app/(private)/` or `app/(public)/` |
| Fetch data server-side | Use `fetch` with `cache` option or `backendJson()` |
| Fetch data client-side | Use `apiClient()` from `lib/api/fetch.ts` |
| Add authentication | Use `currentUser()` (server) or `useUser()` (client) |
| Style component | Use Tailwind with `cn()` or `tv()` |
| Validate form | Use Zod from `@quantum/shared-validation` |
| Manage URL state | Use `useQueryState` from nuqs |
| Create API route | Add `route.ts` in `app/internal/*` (NEVER `/api/*`) |
| Add caching to API route | Use `proxyToBackend({ cache: { revalidate, tags } })` |
| Loading state | Use `<Suspense>`, `<Activity>`, or `loading.tsx` |
| Stable callback | Use `useEffectEvent` (React 19.2) |
| Cache expensive query | Use `cache()` wrapper |

---

## Reference Files

For detailed patterns and examples:

- **[PATTERNS.md](PATTERNS.md)** - Detailed code patterns for data fetching, styling, auth, forms, URL state
- **[ANTI_PATTERNS.md](ANTI_PATTERNS.md)** - Common mistakes and how to avoid them

---

## Related Skills

- **backend-dev-guidelines** - Backend API patterns
- **route-tester** - Testing authenticated routes

---

**Skill Status**: Updated for Quantum Skincare ✅
**Stack**: Next.js 16, React 19.2, Tailwind v4, Clerk, TypeScript
**React 19.2 Features**: React Compiler, useEffectEvent, Activity, cache, cacheSignal
**Next.js 16 Features**: Devtools MCP, enhanced App Router
**Line Count**: Under 500 lines (following Anthropic best practices) ✅
