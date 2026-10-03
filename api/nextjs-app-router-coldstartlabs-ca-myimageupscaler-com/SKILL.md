---
name: nextjs-app-router
description: Next.js 15 App Router patterns for this project. Use when creating routes, API endpoints, server components, or client components.
---

# Next.js 15 App Router

## Directory Structure

- `app/` - Routes and API handlers
- `client/` - Client components and utilities
- `server/` - Server-side services
- `shared/` - Shared types and utilities

## Route Handlers (API)

```typescript
// app/api/example/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  const body = await request.json();
  // Validate with zod schema from shared/validation/
  return NextResponse.json({ data });
}
```

## Server Components (Default)

```typescript
// No 'use client' directive
export default async function Page() {
  const data = await fetchData(); // Direct DB/API calls
  return <div>{data}</div>;
}
```

## Client Components

```typescript
'use client';
// Required for: hooks, browser APIs, event handlers, state
import { useState } from 'react';
```

## Data Fetching

- Server Components: Direct async/await
- Client Components: Use `client/utils/api-client.ts`

## Caching

```typescript
// Revalidate every hour
export const revalidate = 3600;

// Or disable caching
export const dynamic = 'force-dynamic';
```

## Error Handling

- `error.tsx` - Error boundary per route
- `not-found.tsx` - 404 handling
- `loading.tsx` - Suspense fallback

## Metadata

```typescript
export const metadata = {
  title: 'Page Title',
  description: 'Page description',
};
```
