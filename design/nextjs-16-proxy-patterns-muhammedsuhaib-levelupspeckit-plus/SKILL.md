---
name: nextjs-16-proxy-patterns
description: Guide for Next.js 16 proxy patterns, replacing the deprecated middleware functionality. Covers the new proxy.ts file convention, async request APIs, and proper request interception. Use when implementing authentication, redirects, headers modification, or request processing at the network boundary level.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Next.js 16: Proxy Patterns

## Overview

In Next.js 16, the `middleware` file convention has been renamed to `proxy` to clarify network boundary and routing focus. This change affects how you intercept and modify requests before they reach your application.

## Next.js 16 Breaking Changes

⚠️ **CRITICAL**: This is a breaking change in Next.js 16:

1. **File Renaming**: `middleware.ts` → `proxy.ts`
2. **Function Renaming**: `export function middleware()` → `export function proxy()`
3. **Runtime Change**: Proxy runs in `nodejs` runtime (not `edge` runtime)
4. **Config Updates**: `skipMiddlewareUrlNormalize` → `skipProxyUrlNormalize`

## When to Use This Skill

Use this skill when:
- Setting up request interception (authentication, redirects, headers)
- Replacing old middleware functionality with proxy
- Implementing authentication checks before page rendering
- Adding/modify request/response headers
- Performing redirects based on request conditions
- Working with cookies or authentication in the request flow

## Migration Pattern

### Before (Next.js 15 and earlier):
```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Authentication check
  const token = request.cookies.get('auth-token')
  
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/:path*'],
}
```

### After (Next.js 16 with Proxy):
```typescript
// proxy.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export async function proxy(request: NextRequest) {
  // Next.js 16: All dynamic APIs are now async
  // Authentication check
  const cookieStore = await import('next/headers').then(m => m.cookies());
  const token = cookieStore.get('auth-token');
  
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/:path*'],
}
```

## Complete Proxy Example with Authentication

```typescript
// proxy.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export async function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl

  // Public routes that don't require authentication
  const isPublicRoute = 
    pathname === '/login' || 
    pathname === '/register' || 
    pathname.startsWith('/api/auth')

  // Protected routes that require authentication
  const isProtectedRoute = 
    pathname.startsWith('/dashboard') || 
    pathname.startsWith('/profile') ||
    pathname.startsWith('/api/private')

  if (isProtectedRoute && !isPublicRoute) {
    // In Next.js 16, access cookies asynchronously
    const cookieStore = await import('next/headers').then(m => m.cookies());
    const token = cookieStore.get('auth-token')

    if (!token) {
      // Redirect to login page
      const loginUrl = new URL('/login', request.url)
      loginUrl.searchParams.set('callbackUrl', pathname)
      return NextResponse.redirect(loginUrl)
    }
  }

  // Continue with the request
  return NextResponse.next()
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
}
```

## Configuration Update

### Before (Next.js 15):
```typescript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  skipMiddlewareUrlNormalize: true,
}

module.exports = nextConfig
```

### After (Next.js 16):
```typescript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  skipProxyUrlNormalize: true,
}

module.exports = nextConfig
```

## Key Differences

| Next.js 15 Middleware | Next.js 16 Proxy |
|----------------------|------------------|
| Runs in Edge Runtime | Runs in Node.js Runtime |
| File: `middleware.ts` | File: `proxy.ts` |
| Function: `middleware()` | Function: `proxy()` |
| Config: `skipMiddlewareUrlNormalize` | Config: `skipProxyUrlNormalize` |
| Limited request data access | Full Node.js capabilities |

## TypeScript Considerations

When using the proxy pattern in Next.js 16, keep in mind that all dynamic APIs now return promises:

```typescript
// ✅ Correct in Next.js 16
export async function proxy(request: NextRequest) {
  const headersList = await import('next/headers').then(m => m.headers());
  const userAgent = headersList.get('user-agent');
  
  // Modify response headers
  const response = NextResponse.next();
  response.headers.set('x-custom-header', 'proxy-value');
  
  return response;
}
```